import re

from .lookup import A_HOUSE_WARMING_UP, A_WEATHER_ASK, PRESENT_ASK, entry

ANSWERS = ("sport", "fitness")


def _not_a_line_about_a_box(understood):
    said = understood if isinstance(understood, dict) else {}
    text = str(said.get("text") or said.get("clean") or "").lower()
    if not re.search(r"\bbox(es)?\b|\bcartons?\b|\bcardboard\b", text):
        return True
    return bool(re.search(r"\bbox(ing|er|ercise)\b|\bgloves\b|\bspar\b|\bring\b|"
                          r"\bkickbox|\bmuay thai|\bclub\b|\bgym\b|\bclass", text))

def _not_a_timetable_that_runs(understood):
    said = understood if isinstance(understood, dict) else {}
    if str(said.get("topic") or "") != "geography-and-travel":
        return True
    text = str(said.get("text") or said.get("clean") or "").lower()
    return not re.search(r"\brun(s|ning)?\b|\bran\b", text)


WORLD_CUP = {
    1930: ("Uruguay", "the first tournament, at home in Montevideo"),
    1934: ("Italy", "at home, in a tournament that was all knock-out rounds"),
    1938: ("Italy", "the last one before the war"),
    1950: ("Uruguay", "the one England did not enter and the United States beat England in"),
    1954: ("West Germany", "the final against Hungary that nobody expected them to win"),
    1958: ("Brazil", "the tournament a 17-year-old Pele won"),
    1962: ("Brazil", "in Chile"),
    1966: ("England", "at Wembley, 4-2 against West Germany after extra time, still their only one"),
    1970: ("Brazil", "the side with Pele, Jairzinho and Carlos Alberto, often called the best"),
    1974: ("West Germany", "at home, beating the great Netherlands side in the final"),
    1978: ("Argentina", "at home, the first of their three"),
    1982: ("Italy", "in Spain"),
    1986: ("Argentina", "Maradona's tournament, the Hand of God and the goal of the century"),
    1990: ("West Germany", "a final against Argentina settled by a penalty"),
    1994: ("Brazil", "on penalties against Italy in the United States, the first final decided that way"),
    1998: ("France", "at home, 3-0 against Brazil, with Zidane scoring two headers"),
    2002: ("Brazil", "in Japan and South Korea, Ronaldo's tournament"),
    2006: ("Italy", "on penalties against France in Berlin"),
    2010: ("Spain", "against the Netherlands in South Africa, Iniesta in extra time"),
    2014: ("Germany", "1-0 against Argentina in Brazil, Gotze in extra time"),
    2018: ("France", "4-2 against Croatia in Russia"),
    2022: ("Argentina", "against France on penalties in Qatar, Messi's tournament"),
}

_PLAN_5K = (
    "Three runs a week gets most people to 5k in about eight weeks. If you cannot run five "
    "minutes yet, start with run-walk: one minute jogging, two walking, seven times. Once you can "
    "run 20 minutes without a break, make one run a week the long one and add five minutes to it "
    "until it is 30. Keep the other two short and slow enough to talk in sentences, take a rest "
    "day between runs, and keep the last week light.")
_PLAN_10K = (
    "Once you can run for half an hour without stopping, a 10k takes about ten weeks on three "
    "runs a week: one long run that grows by five to ten minutes a week, one easy run, and one "
    "with four or five short faster bursts inside it. Take the long run up to about 9km two weeks "
    "before the day, then ease off. Keep the weekly increase near 10% and put a rest day after "
    "the long one, since the distance is built in the recovery, not in the run.")
_TIME_MARATHON = (
    "A first marathon usually takes 3 hours 30 to 4 hours 45 minutes, and under 4 hours is a good club "
    "standard; under 3 hours 30 is quick. Most people run the first half too fast and lose twenty "
    "minutes in the last 10km, so aim for even splits and walk the water stations.")
_PLAN_HALF = (
    "Once you can run for an hour without stopping, a half marathon takes twelve to sixteen weeks "
    "on three or four runs a week: the long run grows by a kilometre or two a week up to about "
    "18km, three weeks before the day. The others stay easy, with one session of faster bursts "
    "if you have the energy. Nothing new on race day, and a first half is always better run a "
    "little slower than you think you can.")
_TIME_5K = (
    "A first 5k usually takes 30 to 40 minutes at a jog with walking breaks; the average parkrun "
    "time is about 28 minutes, and anything near 25 is quick. Walking the whole way is roughly 45 "
    "to 50 minutes, and most races allow far longer than that, so a first one is not something to "
    "worry about being slow at.")
_TIME_10K = (
    "A first 10k usually takes 55 to 70 minutes, and the average club runner does 50 to 55; under "
    "45 is quick. Walking breaks in the second half cost you less than you would think.")
_TIME_HALF = (
    "A first half marathon usually takes 2 hours 15 to 2 hours 30, and two hours is a good club "
    "standard; under 1 hour 45 is quick. Walking breaks early on cost you very little, and the "
    "cut-offs at most races are generous.")


_RACES = (
    ("5k",
     ("5k", "5km", "5 k", "couch to 5k", "couch 5k", "c25k", "3 miles", "three miles"),
     _PLAN_5K, _TIME_5K),
    ("10k",
     ("10k", "10km", "10 k", "couch to 10k", "6 miles", "six miles"),
     _PLAN_10K, _TIME_10K),
    ("half",
     ("half marathon", "half-marathon", "half", "21k", "21km", "13 miles"),
     _PLAN_HALF, _TIME_HALF),
)
_PLAN_WORDS = ("train", "training", "plan", "planning", "prepare", "preparing", "build up",
               "get ready", "ready", "start", "starting", "beginner", "couch", "c25k",
               "round", "finish", "complete", "improve", "faster", "signed up", "got a place",
               "first one", "want", "wanting", "into", "run", "running", "jog", "jogging",
               "too soon", "enter", "entering", "sign up", "signing up", "should i",
               "am i ready", "ready for", "if i can only", "can only run", "only run",
               "is it enough", "enough for me")
_PLAN_ASK = ("train", "training", "plan", "planning", "prepare", "preparing", "build up",
             "get ready", "ready", "start", "starting", "beginner", "couch", "c25k", "want",
             "first", "help", "how do i", "how to", "round", "finish", "complete", "improve",
             "faster", "signed up", "got a place", "work up to",
             "should i run", "should i enter", "should i sign up", "should i do", "should i try",
             "too soon", "am i ready", "ready for", "if i can only", "can only run",
             "only run", "only manage", "is it enough", "enough for me")
_PLAN_AVOID = ("far", "distance", "how fast", "pace", "what time", "good time", "faster",
                "quicker", "speed", "5k time", "10k time", "personal best",
                "want to break", "want a sub", "want to go under", "want to get under",
                "target time", "goal time",
                "knee", "knees", "hurt", "hurts", "hurting", "pain", "painful", "sore", "ache",
                "aches", "aching", "shin", "shins", "calf", "calves", "ankle", "ankles", "foot",
                "feet", "heel", "injury", "injured", "injur", "tight", "stiff", "blister")
_TIME_WORDS = ("how long does", "how long to run", "how long should it take", "how long will",
               "what time", "whats a good time", "what's a good time", "good time",
               "average time", "how fast", "how long should", "take to run", "take me to run",
               "aim for", "how many minutes", "how many hours",
               "a good time", "good", "time", "time for")
_TIME_AVOID = ("train", "training", "plan", "prepare", "preparing", "ready", "couch",
               "far", "distance", "length",
               "improve", "improving", "get faster", "go faster", "run faster", "faster",
               "quicker", "speed", "speed up", "get my time down", "bring my time down",
               "get quicker", "shave", "personal best", "pb",

               "flu", "ill", "illness", "cold", "fever", "sick", "temperature", "chest", "cough",
               "back to running", "get back to", "run again", "running again", "before i can run",
               "when can i run", "injury", "injured", "recovering", "recovery",
               "trainers", "trainer", "shoes", "shoe", "kit", "gear", "garmin",
               "wear", "wearing", "what do i wear", "what to wear", "what should i wear",
               "clothes", "put on", "rain", "raining", "rainy", "wet", "layers", "socks",
               "what time do", "what time does", "what time are", "what time is the",
               "start time", "start times", "start line", "starts", "start",
               "time of year", "best time of year", "season", "which month",
               "give myself", "good idea", "worth it",
               "rest", "resting", "after a marathon", "after a half marathon", "after the race",
               "after a race", "sore", "much time should i give",
               "stretch", "stretches", "stretching", "warm up", "warmup", "breakfast", "eat",
               "eating", "food", "fuel", "fuelling", "snack", "porridge", "toast", "carbs",
               "carb", "hydrate", "hydration", "for beginners",
               "first one", "good for me", "good for a beginner", "good for a first timer",
               "at 40", "at 50", "at 60", "at 70", "too old",
               "too young", "my age", "in my 40s", "in my 50s", "in my 60s",
               "year old", "years old", "good age", "what age", "age to run", "age for",
               "buy", "buying", "bought", "place", "places", "entry", "enter", "entries",
               "sign up", "signed up", "registration", "ballot", "charity place"
               "rested", "recover", "recovers", "recovering", "days off", "day off",
               "easy days")
_RACE_MODE_AVOID = ("walk", "walking", "walked", "drive", "driving", "drove", "cycle",
                    "cycling", "bike", "bicycle", "swim", "swimming", "swam")
_HALF_AVOID = ("half an hour", "half hour", "half a mile", "half mile", "half a kilometre",
               "half a kilometer", "half term", "an hour and a half", "hour and a half",
               "half time", "halftime", "half a day", "half the",
               "half a", "half an", "half of",
               "my dose", "dose", "dosage", "insulin", "tablets", "pills", "capsules",
               "medication", "medicines")

_CLOCK_HALF = tuple(f"half {hour}" for hour in (
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))


_SAID = ("clean", "norm_text", "text")


_GOLF_SAID = ("golf", "putt", "putts", "putted", "putting", "green", "greens", "hole", "holes",
              "tee", "handicap", "fairway", "bunker", "club", "clubs", "course", "courses",
              "irons", "driver", "slice", "hook", "swing")


_GOGGLES_FIX = (
    "Spit in each lens, rub it round and rinse it out, or wipe a drop of baby shampoo over the "
    "inside and let it dry - both leave a film the water cannot bead on. Then keep the seal "
    "still: a mask that is too tight, or goggles pressed on with the strap under a swim cap, "
    "squeezes out the warm air and fogs faster. Anti-fog sprays work for a session or two.")
_GOGGLES_REASON = (
    "The lens is colder than the warm, damp air coming off your face, so the water in that air "
    "condenses on it as droplets. Anything that keeps the two closer in temperature or puts a "
    "film on the inside stops the droplets forming - and a gap that lets the warm air out works "
    "better than a tighter seal.")
_SWIMMING_WORDS = frozenset((
    "swim", "swims", "swimming", "swimmer", "swimmers", "pool", "pools", "length", "lengths",
    "lane", "lanes", "dive", "dives", "diving", "snorkel", "snorkelling", "lido", "open water",
    "underwater", "wetsuit",
))


def the_goggles_are_for_swimming(understood):
    words = set((understood or {}).get("words") or ())
    if words & _SWIMMING_WORDS:
        return True
    said = ((str((understood or {}).get("clean") or "")) + " " +
            str((understood or {}).get("plain") or "") + " " +
            str((understood or {}).get("text") or "")).lower()
    for word in _SWIMMING_WORDS:
        if word in said:
            return True
    asks = set((understood or {}).get("asks") or ())
    return bool(asks & {"how", "what", "why"})


def _goggles_fog(memory, understood):
    said = str((understood or {}).get("text") or "").lower()
    asks = set((understood or {}).get("asks") or ())
    if "why" in said or "why" in asks:
        return _GOGGLES_REASON + " " + _GOGGLES_FIX
    return _GOGGLES_FIX


def _a_put_is_not_a_putt(understood):
    said = " ".join(str((understood or {}).get(key) or "") for key in _SAID).lower()
    words = " ".join(said.replace("-", " ").split()).split()
    if any(word in _GOLF_SAID for word in words):
        return True
    return "put" not in words


def _a_clock_half_is_not_the_race(understood):
    said = " ".join(str((understood or {}).get(key) or "") for key in _SAID).lower()
    said = " ".join(said.replace("-", " ").split())
    if "half marathon" in said:
        return True
    return not any(f" {hour} " in f" {said} " for hour in _CLOCK_HALF)

_HALF_DISTANCE = entry(
    "race-distance-half",
    (("half marathon", "half", "13.1", "13 1 miles", "21.1", "21 1 km"),
     ("far", "long", "miles", "km", "kilometres", "kilometers", "distance", "how", "length",
      "longer", "longer than", "further", "further than", "shorter", "shorter than")),
    "A half marathon is 13.1 miles, or 21.1 kilometres: half the marathon distance, which is why "
    "the number looks odd. A first one usually takes 2 hours 15 to 2 hours 30, and most plans "
    "build up to it over twelve to sixteen weeks.",
    ask=("far", "long", "miles", "km", "kilometres", "kilometers", "distance", "length", "how",
         "longer", "longer than", "further", "further than", "shorter", "shorter than"),
    avoid=(("train", "training", "plan", "prepare", "preparing", "build up", "ready", "couch",
            "longer than", "which is longer", "how much longer", "difference", "versus",
            "pace", "time", "good time", "faster",
            "taper", "tapering", "recover", "recovery", "shoes", "sore", "injury", "fuel",
            "eat", "eating", "drink", "drinking", "blister", "weather") + _HALF_AVOID))

_LONGER_AVOID = {
    "5k": ("10k", "10 km", "10km", "half marathon", "half"),
    "10k": ("half marathon", "half"),
    "half": (),
}

_RACE_ENTRIES = tuple(
    made
    for _name, _phrases, _plan, _time in _RACES
    for made in (
        entry("race-plan-" + _name, (_phrases, _PLAN_WORDS), _plan, ask=_PLAN_ASK,
              avoid=(_PLAN_AVOID + _RACE_MODE_AVOID + _LONGER_AVOID[_name]
                     + (_HALF_AVOID if _name == "half" else ())),
              guard=(_a_clock_half_is_not_the_race if _name == "half" else None),
              bias=1),
        entry("race-time-" + _name, (_phrases, _TIME_WORDS), _time,
              avoid=(_TIME_AVOID + _RACE_MODE_AVOID + _LONGER_AVOID[_name]
                     + (_HALF_AVOID if _name == "half" else ())),
              guard=(_a_clock_half_is_not_the_race if _name == "half" else None),
              bias=10))
) + (entry("first-game-after-a-break",
      (("five a side", "5 a side", "five-a-side", "football", "soccer", "rugby", "hockey",
        "basketball", "netball", "badminton", "tennis", "squash", "rounders", "cricket"),
       ("first time in years", "first time in ages", "first game", "first match", "first time",
        "havent played", "haven't played", "not played for", "not played in", "back to football",
        "back to playing", "playing again", "start playing again", "getting back into",
        "how do i not get injured", "not get injured", "avoid injury", "avoid getting hurt",
        "dont get hurt", "don't get hurt", "not hurt myself", "sore after", "ache after",
        "will i be sore", "unfit", "out of shape")),
      "Do less than you want to: play twenty minutes of it rather than the whole hour, and warm "
      "up for five with a jog and a few short sprints before the first ball, because the sprint "
      "cold is what goes. Boots with grip for the surface, water at the side, and expect to ache "
      "for two days afterwards - that soreness is normal and walking helps it. If a joint swells "
      "or gives way, or a pain is still there after a fortnight, that is a physio rather than "
      "another game.",
      avoid=("warm up", "warm-up", "warming up", "warmup", "boots", "boot", "astroturf",
             "astroturf", "studs", "moulded", "how fit", "get fit", "lose weight",
             "how often", "how many times a week", "offside", "rules", "how long is a game",
             "world cup", "watch", "on tv"),
      bias=2),
     entry("race-day-kit",
      (("10k", "5k", "parkrun", "park run", "half marathon", "marathon", "marathons", "race",
        "race day", "sportive", "triathlon", "cross country"),
       ("wear", "wearing", "kit", "clothes", "what do i put on", "put on", "what should i wear",
        "what to wear", "socks", "layers")),
      "Nothing new on race day: the socks and shoes you did your long runs in, and dress for ten "
      "minutes in - a thin wicking base layer, a warm thin layer over it and a windproof shell you "
      "can tie round your waist, a cap for rain or sun, gloves for the first two miles and a "
      "waterproof jacket if it is really coming down, because you warm up two or three miles in "
      "and one layer fewer than feels right at the door is usually the right count. Vaseline on "
      "the nipples and inner thighs, safety pins for the number, a dry top and a bin liner for "
      "your bag at the finish, and a warm layer to pull on within ten minutes of stopping, which "
      "is when the cold really lands.",
      avoid=("how long", "how fast", "what time", "what pace", "pacing", "split", "splits",
             "finish time", "training plan", "how many weeks", "how often", "bin bag",
             "lose weight", "taper", "carbs", "carb load", "what should i eat", "fuel",
             "what socks", "which socks", "socks for", "socks with", "socks to",
             "hot", "sun", "sunny", "heat", "heatwave", "boiling", "30 degrees", "35 degrees"),
      bias=2),
     _HALF_DISTANCE,
     entry("race-time-marathon",
           (("marathon", "26.2", "26 2 miles", "42.2", "42 2 km"), _TIME_WORDS),
           _TIME_MARATHON,
           avoid=_TIME_AVOID + _RACE_MODE_AVOID, bias=10))

_NOISY = ("click", "clicks", "clicking", "clunk", "clunks", "clunking", "grind", "grinds",
          "grinding", "creak", "creaks", "creaking", "pop", "pops", "popping", "crack", "cracks",
          "cracking", "noisy", "noise", "snapping")
_HURTS = ("hurt", "hurts", "hurting", "pain", "painful", "ache", "aches", "aching", "sore",
          "swollen", "swelling", "sharp", "stiff")
_KNEE_PAIN = ("Pain at the front of the knee on stairs is the kneecap being pulled off line by "
              "weak or tight muscles around it, which is common in new runners and in people who "
              "sit all day. Three times a week do sit-to-stands, step-ups and wall sits, and ease "
              "off hills and deep squats for a fortnight. See a physio if it swells, locks, or the "
              "knee gives way under you.")
_KNEE_NOISY = ("A knee that clicks or grinds without hurting is usually harmless - it is the "
               "kneecap sliding over the joint, and sometimes the gas in the joint fluid popping. "
               "It needs nothing doing. If the noise comes with pain or swelling, treat it as pain: "
               "strengthen the muscles around the knee with sit-to-stands, step-ups and wall sits "
               "three times a week, and see a physio if it swells, locks or gives way.")


def _win_years():
    found = {}
    for year, (winner, _note) in WORLD_CUP.items():
        found.setdefault(winner.lower().replace("west ", ""), []).append(year)
    return {name: sorted(years) for name, years in found.items()}


WIN_YEARS = _win_years()


def _listed(years):
    said = [str(year) for year in years]
    return said[0] if len(said) == 1 else ", ".join(said[:-1]) + " and " + said[-1]


def _world_cup(memory, understood):
    clean = understood.get("clean") or ""
    years = [int(year) for year in re.findall(r"\b(19\d\d|20[0-2]\d)\b", clean)]
    for year in years:
        if year in WORLD_CUP:
            winner, note = WORLD_CUP[year]
            return "In %d it was %s, %s." % (year, winner, note)
    if years:
        return ("The men's World Cup has been held every four years since 1930, apart from 1942 "
                "and 1946 for the war, so %d is not a tournament year." % years[0])
    lowered = clean.lower()
    for country in sorted(WIN_YEARS, key=len, reverse=True):
        if re.search(r"\b" + re.escape(country) + r"\b", lowered):
            won = WIN_YEARS[country]
            how_many = {1: "once", 2: "twice", 3: "three times", 4: "four times",
                        5: "five times"}.get(len(won), "%d times" % len(won))
            return "%s have won the men's World Cup %s: %s." % (
                country.title(), how_many, _listed(won))
    return ("Brazil have won it five times (1958, 1962, 1970, 1994, 2002) and Germany and Italy "
            "four each; Argentina won in 2022 and France in 2018, England in 1966.")


_NOT = ("not", "no", "dont", "doesnt", "didnt", "isnt", "never", "without", "hardly")


def _noisy_knee(memory, understood):
    words = set(understood.get("words") or [])
    hurts = bool(words & set(_HURTS)) and not words & set(_NOT)
    return _KNEE_PAIN if hurts else _KNEE_NOISY


_PROTEIN_TRAINING = ("muscle", "muscles", "lifting", "lift", "weights", "weight training",
                     "gym", "bulking", "bulk", "bodybuild", "bodybuilding", "stronger",
                     "training", "workout", "workouts", "gains", "protein shake", "protein shakes",
                     "protein powder", "whey")


def _protein(memory, understood):
    text = ((understood.get("clean") or "") + " " + (understood.get("norm_text") or "")).lower()
    if any(word in text for word in _PROTEIN_TRAINING):
        return ("To build muscle, aim for about 1.6-2.2g of protein for each kilo you weigh - "
                "roughly 110-155g a day at 70kg - spread over three or four meals of 25-40g: "
                "chicken, tuna, eggs, Greek yoghurt, lentils or tofu. There is no need for powder "
                "if meals get you there, and for healthy kidneys that amount is not a risk. "
                "Protein without hard training does little, so the lifting matters as much as "
                "the food.")
    return ("Aim for about 0.75g of protein for each kilo you weigh - roughly 55g a day at 75kg - "
            "which is a palm-sized portion at each meal: eggs or yoghurt at breakfast, beans, tuna "
            "or chicken at lunch, fish, lentils or mince at dinner. Lifting weights to build "
            "muscle takes it higher, to about 1.6g per kilo and over. Most people in the UK "
            "already eat enough without powder.")


_CALF_STRETCH = ("For the calf, stand with both hands on a wall, one leg back with the heel flat "
                 "on the floor and the back knee straight, and lean in until you feel it pull: "
                 "hold 30 seconds, three times each side. Then bend the back knee slightly, "
                 "keeping the heel down, for the lower calf. Stretch after you run rather than "
                 "before, when the muscle is warm, and breathe out into the stretch instead of "
                 "bouncing.")
_HAMSTRING_STRETCH = ("For the hamstring, sit or stand with one heel on a low step, keep that leg "
                      "straight and hinge forward from the hips with a flat back until you feel the "
                      "pull behind the thigh - hold 30 seconds, three times each side. No bouncing "
                      "and no reaching for your toes with a round back. Do it after the run, when "
                      "the muscle is warm.")
_QUAD_STRETCH = ("For the front of the thigh, the quad: stand tall, take one foot behind you and "
                 "pull the heel up towards your bottom with the knee pointing down at the floor and "
                 "your hips level, and hold 30 seconds each side - a hand on a wall or a chair for "
                 "balance. If the pull is at the back of the thigh instead, that is the hamstring: "
                 "heel on a low step, leg straight, hinge forward from the hips with a flat back, "
                 "30 seconds each side. Both after the exercise, when the muscle is warm.")
_WHOLE_LEG_STRETCH = ("For the whole leg, the calf first: hands on a wall, one leg back with the heel "
                      "flat on the floor and that knee straight, lean in for 30 seconds, three times "
                      "each side. Then the hamstring: one heel on a low step, that leg straight, hinge "
                      "forward from the hips with a flat back, 30 seconds each side. Both after the "
                      "exercise, when the muscles are warm, not before.")


def _stretch(memory, understood):
    words = set(understood.get("words") or ())
    if words & {"hamstring", "hamstrings"}:
        body = _HAMSTRING_STRETCH
    elif words & {"quad", "quads", "thigh", "thighs"}:
        body = _QUAD_STRETCH
    elif words & {"leg", "legs"}:
        body = _WHOLE_LEG_STRETCH
    else:
        body = _CALF_STRETCH
    if "before" in words and "after" in words:
        return ("After, when the muscle is warm, not before: holding a stretch on a cold muscle "
                "pulls it more than it loosens it, and five minutes of easy running is a better "
                "warm-up than any stretch. " + body)
    return body


_REPORTED = ("my husband is", "my wife is", "my partner is", "my boyfriend is",
             "my girlfriend is", "my son is", "my daughter is", "my friend is",
             "my brother is", "my sister is", "my mum is", "my mom is", "my dad is",
             "he is getting", "she is getting", "they are getting",
             "hes getting", "shes getting", "theyre getting",
             "he is back", "she is back", "hes back", "shes back")
_RESULTS_REPLY = (
    "I can't see last night's scores or the table - I have no way of looking them up, so I would "
    "only be guessing. A scores app or the club's own page will have it in a second. If you tell "
    "me the result I can talk it through with you."
)
_YEAR = re.compile(r"(19|20)\d\d")


_CUPS = ("fa cup", "league cup", "carabao", "world cup", "scottish cup", "copa del rey",
         "fa trophy", "playoff final", "play off final")
_LEAGUES = ("premier league", "champions league", "europa league", "conference league",
            "la liga", "serie a", "bundesliga", "ligue 1", "the championship", "county championship")
_LEAGUE_AND_CUP = (
    "A league is decided over a season: every team plays the others home and away, and the table "
    "decides who wins, so one bad afternoon only costs you three points. A cup is knockout: you "
    "play once, and losing means you are out, which is why a lower team can beat a big one on the "
    "day. That is how the same club can be top of the league and out of the cup in the same week."
)


def _league_and_cup(memory, understood):
    said = (str(understood.get("clean") or "") + " " +
            " ".join(str(word) for word in (understood.get("words") or []))).lower()
    cups = [name for name in _CUPS if name in said]
    leagues = [name for name in _LEAGUES if name in said]
    if len(cups) + len(leagues) > 1:
        return None
    if cups:
        return None
    return _LEAGUE_AND_CUP


def _cant_see_the_score(memory, understood):
    said = " ".join(str(word) for word in (understood.get("words") or []))
    said = said + " " + str((understood or {}).get("clean") or "")
    if _YEAR.search(said):
        return None
    return _RESULTS_REPLY

_BATTING_WORDS = ("bat", "batting", "batsman", "batter", "runs", "drive", "pull", "cut shot",
                  "shot", "shots", "hit")
_BOWLING_WORDS = ("bowl", "bowling", "bowler", "spin", "spin bowling", "seam", "swing", "yorker",
                  "line and length", "wickets", "take wickets")


_BASKETBALL_DRIBBLE_WORDS = ("dribble", "dribbling", "dribbled", "handle", "handles",
                              "ball handling", "ball-handling", "crossover", "bring the ball up",
                              "handling the ball", "handle the ball")


def _basketball_better(memory, understood):
    words = set(str(word).lower() for word in (understood.get("words") or []))
    words.update(str((understood or {}).get("clean") or "").lower().split())
    flat = " ".join(str((understood or {}).get("clean") or "").lower().split())
    if any(word in words or (" " in word and word in flat)
           for word in _BASKETBALL_DRIBBLE_WORDS):
        return ("Dribble low and hard with your fingertips, head up, and change pace rather than "
                "doing tricks: a slow dribble that suddenly speeds up beats a crossover nobody "
                "falls for. Pound the ball 50 times with each hand standing still, then walk the "
                "length of the court changing hands every three dribbles, then do it at a jog. "
                "Keep your body between the ball and the defender, and never pick the ball up "
                "until you have decided what you are doing with it.")
    return ("Shooting is one repeatable motion: elbow under the ball, a small dip, and push up "
            "from the legs so the ball leaves your fingertips with backspin. Start a metre from "
            "the hoop and make 20 in a row before you step back, then finish every session with "
            "20 free throws while you are tired, because that is when games are decided. Keep the "
            "guide hand off the ball and do not let the shooting elbow drift out.")


_A_BAT_WORD = frozenset("bat bats batting batsman batsmen batter batters".split())

_ABOUT_THE_GAME = frozenset("""better improve improving practise practice technique coach
    coaching training nets net batting bowling swing grip stance footwork drills drill
    warm-up warmup season match club league innings""".split())


def _not_the_coach_of_a_team(understood):
    sense = (understood or {}).get("sense") or {}
    return sense.get("coach") != "teacher"


def _a_bat_that_is_not_the_game(understood):
    sense = (understood or {}).get("sense") or {}
    if sense.get("bat") == "animal":
        return False
    if sense.get("bat") == "sport":
        return True
    words = {str(word).lower() for word in ((understood or {}).get("words") or ())}
    words.update(str((understood or {}).get("clean") or "").lower().split())
    if not (words & _A_BAT_WORD):
        return True
    return bool(words & _ABOUT_THE_GAME)


def _the_game_and_not_another(understood):
    return _not_another_bowl_game(understood) and _a_bat_that_is_not_the_game(understood)


def _not_another_bowl_game(understood):
    text = " ".join(str((understood or {}).get("clean") or " ".join(
        (understood or {}).get("words") or [])).lower().split())
    words = set(re.findall(r"[a-z0-9']+", text))
    if not (words & _BOWL_WORDS):
        return True
    return any(word in words or (" " in word and word in text)
               for word in _CRICKET_WORDS)


_BOWL_WORDS = frozenset((
    "bowl", "bowls", "bowling", "bowled", "bowler", "bowlers", "bowling's"))


_CRICKET_WORDS = frozenset((
                   "cricket", "wicket", "wickets", "over", "overs", "nets", "net",
                   "batsman", "batsmen", "batter", "batters", "batting", "bat",
                   "test", "t20", "ashes", "innings", "stumps", "stump", "pitch", "slip",
                   "cover", "midwicket", "spinner", "spinners", "spin", "seam", "seamer",
                   "keeper", "keeper's", "yorker", "bouncer", "crease", "googly", "googlies",
                   "no ball", "no balls", "wicketkeeper",
                   "off stump", "leg stump", "long on", "mid off", "cover drive",
                   "bowling action", "spin bowling", "third man", "fine leg",
                   "short leg")) - _BOWL_WORDS


def _cricket_better(memory, understood):
    words = set(str(word).lower() for word in (understood.get("words") or []))
    words.update(str((understood or {}).get("clean") or "").lower().split())
    batting = any(word in words for word in _BATTING_WORDS)
    bowling = any(word in words for word in _BOWLING_WORDS)
    if bowling and not batting:
        return ("Aim at the top of off stump over and over rather than trying a new ball each "
                "over: mark a target on the pitch and land 10 out of 12 before you change "
                "anything. Run in the same way every time, keep the front arm up and the head "
                "still, and use the crease - wide of it for a ball going across, close to it for "
                "one coming in. A wicketkeeper or a mate behind the stumps tells you more than a "
                "camera does.")
    if batting:
        return ("Batting is mostly watching and waiting: watch the ball out of the bowler's hand, "
                "keep your head still, play straight and leave anything outside off you do not "
                "have to hit. Give every net session a purpose - 20 drives, 20 forward defences, "
                "20 pulls - against a bowler better than the ones you face on a Saturday. Ten "
                "minutes of throw-downs a day beats an hour of slogging.")
    return ("Batting is where most club players lose their place, so start there: watch the ball "
            "out of the bowler's hand, keep your head still, play straight and leave anything "
            "outside off you do not have to hit. Then the other half - aim at the top of off "
            "stump over and over rather than trying a new ball every over - and catch 50 high "
            "balls a week, because catches win more club games than runs do.")


_STUDY_WORDS = frozenset("""study studies studying studied student students revise revising
revision revise exams exam mock mocks homework coursework essay essays dissertation notes
memorise memorising remember remembering learn learning learnt grade grades semester""".split())


def _not_a_study_line(understood):
    words = {str(word).lower() for word in (understood.get("words") or ())}
    return not (words & _STUDY_WORDS)


def _football_boots(memory, understood):
    text = str(understood.get("clean") or " ".join(understood.get("words") or [])).lower()
    surface = ("The surface picks the boot: moulded studs (FG) on grass, screw-in studs (SG) when "
               "it is wet and soft, astro or turf trainers (TF) on 3G and 4G, flat indoor shoes for "
               "a hall. ")
    grip = ("Astro boots on wet grass give almost no grip, which is how ankles turn.")
    fit = ("Go by fit: try them on in the afternoon with match socks on, leave a thumb's width at "
           "the toe, and go half a size up for a child whose feet are still growing. ")
    new = ("Wear a new pair around the house an evening at a time and never in a match first; a "
           "leather boot softens within a week. ")
    where = ("Buy them anywhere that lets you try them on: a sports shop, a supermarket's own "
             "brand, the big online retailers, or a club's second-hand kit sale, where "
             "out-grown pairs go for a few pounds. ")
    cheap = ("Do not spend much on a child's boots - feet grow a size a season - but do buy the "
             "right sole for the pitch, because a cheap boot in the wrong stud is worse than no "
             "stud at all. ")
    when = ("Boots are cheapest at the end of a season, in April to June, and again when a new "
            "colourway comes out and last year's drop; for a child the club's kit sale just before "
            "the season starts is the moment, because that is when the out-grown pairs come in. ")
    if any(word in text for word in ("when", "what month", "which month", "best time", "time to buy",
                                     "month")):
        return when + surface
    if any(word in text for word in ("cheap", "cheaper", "cheapest", "afford", "budget", "price",
                                     "prices", "cost", "costs", "spend", "sale", "second hand",
                                     "secondhand", "where", "shop", "shops", "store", "online",
                                     "order", "buy from")):
        return where + cheap + surface + fit
    if any(word in text for word in ("tight", "small", "smaller", "size", "sizing", "wide",
                                     "narrow", "blister", "blisters", "hurt", "hurts", "rubbed",
                                     "10 year old", "9 year old", "8 year old", "11 year old",
                                     "12 year old", "13 year old", "14 year old", "growing")):
        return fit + surface + grip
    if any(word in text for word in ("break in", "breaking in", "break them in", "new boots",
                                     "new pair", "stiff")):
        return new + surface + grip
    return surface + grip + " Try them on with match socks and leave a thumb's width at the toe."


_ASKED_AFTER = ("is my son", "is my daughter", "is my child", "is my partner", "is my wife",
                "is my husband", "is my boyfriend", "is my girlfriend", "is my friend",
                "is my brother", "is my sister", "is my mum", "is my mom", "is my dad",
                "is he", "is she", "is your son", "is your daughter", "how is my",
                "how are my", "are my kids", "are my children", "are they getting")


GROUNDS = (
    (("football pitch", "football field", "soccer pitch", "football ground"),
     "A full-size football pitch is about 105 metres by 68 metres, which is 115 by 74 yards and "
     "a bit under two acres; the laws allow 90 to 120 metres long and 45 to 90 wide, which is "
     "why pitches differ. The goal is 7.32 metres wide and 2.44 metres high."),
    (("tennis court", "tennis courts"),
     "A tennis court is 23.77 metres long, 10.97 metres wide for doubles and 8.23 metres for "
     "singles, with room to run of 6.4 metres behind each baseline and 3.66 metres at the "
     "sides. The net is 1.07 metres at the centre and 0.91 at the posts."),
    (("cricket pitch", "cricket square"),
     "A cricket pitch is 20.12 metres — 22 yards — from stump to stump and 3.05 metres wide, "
     "with the popping crease 1.22 metres in front of the stumps. The boundary round it is a "
     "different size at every ground, from about 60 metres to 75."),
    (("netball court",), 
     "A netball court is 30.5 metres long and 15.25 metres wide, split into thirds, with a "
     "shooting circle of 4.9 metres round each goalpost."),
)


def _ground_size(memory, reading):
    said = " ".join(str((reading or {}).get("clean") or "").split())
    if not said:
        return GROUNDS[0][1]
    for words, text in GROUNDS:
        if any(one in said for one in words):
            return text
    return None


_WOUND_WORDS = frozenset((
    "cut", "cuts", "wound", "wounds", "gash", "gashes", "laceration", "lacerations", "slash",
    "slashed", "sliced", "bleeding", "bled", "blood", "stitches", "sutures", "suture",
    "graze", "grazed", "scab", "tetanus", "butterfly", "steristrips", "glued"))


def _not_a_stitch_in_a_wound(understood):
    words = [str(word).lower() for word in (understood.get("words") or ())]
    if not words:
        words = (understood.get("clean") or "").split()
    for word in words:
        if word in _WOUND_WORDS:
            return False
    return True


_A_SHORTER_RACE = re.compile(r"\b(?:5\s?k|5km|five k|10\s?k|10km|ten k|parkrun)\b", re.I)
_THE_FULL_RACE = re.compile(r"\b(?:full|marathon)\b(?<!half marathon)", re.I)
_COMPARED = ("longer", "longer than", "longest", "further", "furthest", "which is longer",
             "how much longer", "difference", "compared", "compare", "versus", "vs", "twice")


def _a_shorter_race_is_the_question(understood):
    words = [str(w) for w in ((understood or {}).get("words") or ())]
    said = " ".join(words).replace("-", " ")
    if not _A_SHORTER_RACE.search(said):
        return False
    return not _THE_FULL_RACE.search(said)


def _half_is_not_the_question(understood):
    words = [str(w) for w in ((understood or {}).get("words") or ())]
    said = " ".join(words).replace("-", " ")
    half = "half" in words or "13.1" in words or "21.1" in words
    compares = "longer" in words or any(phrase in said for phrase in _COMPARED)
    if half and not _THE_FULL_RACE.search(said) and _A_SHORTER_RACE.search(said):
        return False
    return compares or not half


_MARATHON_COMPARED = ("A marathon is 26.2 miles, or 42.2 kilometres, and a half is 13.1 miles "
                      "(21.1 km), so the full race is exactly twice as far. The odd 0.2 of a mile "
                      "is there because the 1908 London course was extended to finish in front of "
                      "the royal box. A half is the obvious first step, and most plans build up to "
                      "it over about sixteen weeks.")


def _the_half_is_named(understood):
    words = [str(w) for w in ((understood or {}).get("words") or ())]
    said = " ".join(words).replace("-", " ")
    if _A_SHORTER_RACE.search(said):
        return False
    return "half" in words or "13.1" in words or "21.1" in words


_RACE_COMPARED_CARD = entry(
    "race-compare-full",
    (("marathon", "26.2", "42.2", "full marathon"),
     ("longer", "longer than", "which is longer", "how much longer", "difference", "compare",
      "compared", "versus", "vs", "twice", "further", "further than")),
    _MARATHON_COMPARED,
    guard=_the_half_is_named,
    bias=20)

_A_SHORTER_RACE_CARD = entry(
    "race-compare-shorter",
    (("half marathon", "half", "13.1", "21.1"),
     ("longer", "longer than", "further", "shorter", "bigger", "which is longer", "difference",
      "compare", "compared", "versus", "vs")),
    "A half marathon is 13.1 miles (21.1 km), which is further than a 10k at 6.2 miles and a 5k "
    "at 3.1 miles. A first half usually takes 2 hours 15 to 2 hours 30, over twelve to sixteen "
    "weeks of training.",
    guard=_a_shorter_race_is_the_question,
    bias=2)

_RECOVERY_BY_DISTANCE = (
    (("a marathon", "full marathon", "26.2", "42.2", "42k"),
     "Three to four weeks before anything hard: easy running or walking the first week, short easy "
     "runs the second, and a tempo or a long run only around a month out. The fitness comes back "
     "faster than the legs do, which is what catches people who feel fine on day five."),
    (("a half marathon", "half marathon", "half-marathon", "13.1", "21k"),
     "A week to ten days: three or four short easy runs in the first week, nothing hard for ten "
     "days, and a normal week after a fortnight. Most people feel fine after three days, and going "
     "hard then is how the second week goes wrong."),
    (("10k", "10 k", "ten k", "6.2", "six miles", "six mile"),
     "Three or four easy days and then normal training: a 10k at effort takes more out of the legs "
     "than the distance suggests, and the second day after is usually the sorest."),
    (("5k", "5 k", "five k", "three miles", "parkrun"),
     "A day or two of easy running: a hard 5k costs your legs about 48 hours, and an easy run the "
     "day after does more good than a full day off."),
)

_RECOVERY_LOOKBACK = 6


def _a_distance_is_named(understood):
    text = str(understood.get("plain") or understood.get("clean") or "").lower()
    return any(phrase in text for phrases, _line in _RECOVERY_BY_DISTANCE for phrase in phrases)


def _recovery_time(memory, understood):
    text = str(understood.get("plain") or understood.get("clean") or "").lower()
    for phrases, line in _RECOVERY_BY_DISTANCE:
        if any(phrase in text for phrase in phrases):
            return line
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in reversed(turns[-_RECOVERY_LOOKBACK:] if isinstance(turns, list) else []):
        said = str(turn.get("user") or "").lower() if isinstance(turn, dict) else ""
        for phrases, line in _RECOVERY_BY_DISTANCE:
            if any(phrase in said for phrase in phrases):
                return line
    return ("Scale it to what you did: a day or two easy after a hard 5k, three or four days after "
            "a 10k, a week to ten days after a half marathon, and three to four weeks before "
            "anything hard after a marathon. A gym session is about 48 hours for the same muscle "
            "group. Soreness shifts faster with a short easy effort than with total rest, and if "
            "you are still stiff on the stairs after a week, you went back too soon.")
def _a_circle_throw(memory, understood):
    text = str((understood or {}).get("clean") or "").lower()
    if "hammer" in text:
        return ("Swing it from a low point and keep the arms long: three or four turns that get "
                "taller and faster, the body turning first and the arms following, and a high "
                "release over the left shoulder. Stay in the circle until the ball lands, and "
                "keep the wire clear of the ground on the way round - distance comes from the "
                "turns building, not from a big first pull.")
    if "shot" in text:
        return ("A shot is pushed, not thrown: hold it in the fingers at the base of the hand, "
                "tuck it under the chin, and drive off the back leg so the hips lead and the arm "
                "follows last. Keep the elbow behind the shot until the push, and stay in the "
                "circle - stepping out over the front is a foul.")
    return ("The throw comes from the legs and the turn, not the arm: hold the discus flat, spin "
            "across the circle so the hips lead and the arm follows last, and let it go at about "
            "shoulder height with the palm down. Keep the discus close to your body through the "
            "turn. Most beginners lose distance by throwing it up and by rushing the spin.")

_A_CARD_WORDS = ("yellow", "red", "card", "cards", "booked", "booking", "bookings", "sin bin",
                 "sin-bin", "football", "footballer", "soccer", "rugby", "match", "matches",
                 "ref", "referee", "sent off", "foul", "fouls", "tackle", "tackles", "player",
                 "players", "game", "games", "league", "cup", "premier", "world cup", "offside",
                 "penalty", "var", "half time", "pitch", "goal", "goals", "keeper", "chelsea",
                 "arsenal", "liverpool", "united", "spurs", "everton", "england")


def _a_card_is_named(understood):
    reading = understood if isinstance(understood, dict) else {}
    line = " " + " ".join(str(reading.get("clean") or reading.get("text") or "").lower().split()) + " "
    return any(" " + word + " " in line or (" " + word) == line[-len(word) - 1:]
               for word in _A_CARD_WORDS)


_A_BLOCK_IN_THE_WATER = re.compile(
    r"\b(?:can'?t|cannot|couldn'?t|won'?t|unable|struggl\w*|scared|afraid|frightened|"
    r"terrified|nervous|panic\w*|hate[sd]?|dread\w*|worr\w*|refus\w*|phobia|"
    r"fear\w*|"
    r"don'?t like|do not like|not (?:able|confident|brave))\b"
    r"|\b(?:hold|holds|holding|held)\b[^.?!]{0,25}\b(?:my|his|her|their|your)\s+breath\b"
    r"[^.?!]{0,40}\b(?:under|underwater|swim\w*|pool|dive\w*|dove|water)\b"
    r"|\bhow (?:do|can|should|would) i\b|\bhow to\b|\bhelp me\b|\bteach me\b"
    r"|\blearn\w*\b|\btips?\b|\badvice\b|\bwhat can i do\b",
    re.IGNORECASE)


def _a_block_in_the_water(understood):
    return bool(_A_BLOCK_IN_THE_WATER.search(understood.get("text") or understood.get("clean") or ""))


_A_GAME_WORD = re.compile(r"\b(?:games?|play|playing|played|tonight|board|video|console|xbox|"
                          r"playstation|nintendo|switch|steam)\b", re.IGNORECASE)
_A_GOLF_WORD = re.compile(r"\b(?:golf|green|pin|flag|flagstick|club|clubs|iron|irons|wedge|"
                          r"ball|balls|fairway|putt|putts|putting|putter|tee|tees|bogey|birdie|"
                          r"par|handicap|bunker|chip shot|chip shots|pitch shot|pitch shots|"
                          r"chipping|pitching|shot|shots)\b", re.IGNORECASE)


_SHORT_GAME_JARGON = re.compile(r"\bshort game\b", re.IGNORECASE)
_A_PLAY_ASK = re.compile(r"\b(?:to play|play tonight|to play tonight|any games?|games? to play|"
                         r"board|video game|video games|console|xbox|playstation|nintendo|"
                         r"something to play|what should i play|what can i play)\b", re.IGNORECASE)


def _a_short_game_to_play(understood):
    reading = understood if isinstance(understood, dict) else {}
    line = str(reading.get("clean") or reading.get("text") or "")
    if _A_GOLF_WORD.search(line):
        return True
    if _SHORT_GAME_JARGON.search(line) and not _A_PLAY_ASK.search(line):
        return True
    return not _A_GAME_WORD.search(line)


def _says(clean, phrases):
    return re.search(r"(?<!\w)(?:%s)" % "|".join(re.escape(p) for p in phrases), clean) is not None


_WET_MATCH_PLAYING = (
    "Layers you can take off: a base layer and shorts under a thin waterproof top, "
    "gloves once it is under about 8C, and boots to suit the surface - moulded studs on grass, "
    "astro trainers on 3G, long studs only on a soft winter pitch. A towel and a dry top in the "
    "bag for after, because you cool fast once you stop."
)
_WET_MATCH_WATCHING = (
    "A waterproof over everything and something to keep your legs dry: a coat with a hood, "
    "boots or wellies, and a dry top waiting in the car. Two hours standing in wind and rain is "
    "colder than the forecast sounds, so a hat and gloves even in spring."
)
_WET_MATCH_WEATHER = ("rain", "rains", "raining", "rainy", "wet", "drizzle", "showers",
                      "cold", "freezing", "bitter", "snow", "snowing", "wind", "windy",
                      "muddy", "sleeting")
_WET_MATCH_WEAR = ("wear", "wearing", "kit", "clothes", "clothing", "outfit", "boots",
                   "shin pads", "what do i need", "what does he need", "what do we need",
                   "what should i take", "what should he take", "what should she take",
                   "bring", "bringing", "pop", "take with", "pack", "shall i wear",
                   "should i wear", "what should we wear", "what do we wear",
                   "should he wear", "should she wear", "dress him", "dress her")
_WET_MATCH_SPORT = ("football", "football match", "soccer", "rugby", "hockey", "netball",
                    "match", "matches", "five a side", "game", "cup tie", "training")
_WET_MATCH_WATCHING_WORDS = ("watch", "watching", "support", "supporter", "spectator",
                             "spectators", "stands", "touchline", "sit in the",
                             "go to the game", "my husband plays", "my partner plays")
_WET_MATCH_I_PLAY = ("im playing", "i'm playing", "i am playing", "i play", "im in the team",
                     "i'm in the team",
                     "has a match", "has a game", "has a football match", "has a rugby match",
                     "is playing", "he plays", "she plays", "they play", "we play", "were playing",
                     "we are playing")
_WET_MATCH_PLAYS = ("to play", "play ", "playing", "training", "five a side", "kick about")
_WET_MATCH_NOT = ("buy", "buying", "should i buy", "should i get", "which boots", "best boots",
                  "cheap", "price", "cost", "how much",
                  "how do i dry", "how to dry", "drying", "to dry", "dry them", "dry it",
                  "dry out", "dry my", "dry the", "dry off", "get them dry", "keep them dry",
                  "clean", "cleaning",
                  "smell", "smelly", "eat", "eating", "food", "breakfast", "before the game",
                  "after the game", "recovery", "injured", "injury", "hurt", "knee", "ankle")


def _a_wet_match(reading):
    clean = " " + str((reading or {}).get("clean") or "").lower() + " "
    if not _says(clean, _WET_MATCH_SPORT):
        return False
    if not _says(clean, _WET_MATCH_WEATHER):
        return False
    if not _says(clean, _WET_MATCH_WEAR):
        return False
    return not _says(clean, _WET_MATCH_NOT)


def _kit_for_a_wet_match(memory, understood):
    clean = " " + str((understood or {}).get("clean") or "").lower() + " "
    if _says(clean, _WET_MATCH_I_PLAY):
        return _WET_MATCH_PLAYING
    if _says(clean, _WET_MATCH_WATCHING_WORDS):
        return _WET_MATCH_WATCHING
    if _says(clean, _WET_MATCH_PLAYS):
        return _WET_MATCH_PLAYING
    return _WET_MATCH_WATCHING


_GYM_KIT_WORDS = ("what should i bring", "what do i bring", "what should i take",
                  "what do i take", "what should i wear", "what do i wear", "what to bring",
                  "what to wear", "shall i bring", "should i bring", "do i need to bring",
                  "do i need", "what do i need", "what will i need", "need to bring",
                  "need to take", "need to wear", "what kit", "kit list",
                  "bring", "bringing", "wear", "wearing", "take", "taking")
_GYM_INDUCTION_KIT = (
    "Bring trainers with a clean, non-marking sole, a towel, water and a padlock for the locker, "
    "and wear something you can move in - shorts or leggings and a t-shirt. A gym induction is a "
    "walk round with a trainer: they set the seat heights and write you a plan, so nothing else "
    "is needed on the day."
)
_GYM_INDUCTION = (
    "Take the free induction: staff walk you round the machines and set the seat heights, "
    "which is the bit that puts people off. Then keep it simple - a warm-up on the bike, "
    "then two or three sets of 8-12 reps on five or six machines covering legs, back, chest "
    "and shoulders, light enough that you could still do three or four more reps. Write the "
    "weights down and add a little next week."
)


def _the_gym_induction(memory, understood):
    clean = " " + str((understood or {}).get("clean") or "").lower() + " "
    if _says(clean, _GYM_KIT_WORDS):
        return _GYM_INDUCTION_KIT
    return _GYM_INDUCTION


ENTRIES = [
    entry("water-on-a-run",
          (("water", "hydrated", "hydration", "hydrate", "drink", "drinks", "drinking",
            "fluids", "electrolytes", "salt tablets", "bottle", "water bottle", "flask",
            "thirsty", "camelbak", "hydration vest", "water belt"),
           ("run", "runs", "running", "long run", "jog", "jogging", "ride", "cycling", "bike",
            "half marathon", "marathon", "10k", "5k", "parkrun", "race", "train", "training",
            "gym", "hot", "heat", "summer", "sweat", "workout", "work out", "exercise",
            "exercising", "spin", "class", "football", "rugby", "tennis", "netball",
            "hockey", "swim", "swimming")),
          "Under an hour you do not need to carry anything: have 300-500ml in the hour before you "
          "go and take water at fountains or taps on the way. Past an hour, or on a hot day, carry "
          "400-700ml and drink a few mouthfuls every 15-20 minutes rather than one big stop. To "
          "keep it cold, fill the bottle half full and freeze it the night before, top it up with "
          "cold water on the way out, and put it in a belt or vest rather than in your hand. Over "
          "90 minutes take electrolytes, and drink to thirst - drinking lots of plain water on a "
          "long run can make you feel worse, not better.",
          avoid=("rinse", "rinsing", "rinsed",
                 "wash", "washed", "washing", "water runs clear", "runs clear",
                 "eyes", "eye", "knee", "knees", "ankle", "ankles", "shin", "shins", "pain",
                 "hurts", "sore", "injury", "injured", "bill", "meter", "leak", "recipe",
                 "boil", "bath", "shower", "plant", "plants", "garden", "floor", "filter",
                 "softener", "swimming", "pool", "sea", "lake", "well",
                 "hot tub", "hot tubs", "hottub", "jacuzzi", "spa bath",
                 "boiler", "boilers", "radiator", "radiators", "heating", "pipe", "pipes",
                 "washing machine", "dishwasher", "kettle", "cylinder", "immersion", "valve",
                 "thermostat", "hot water", "hot tap", "noise", "noisy", "whistling", "banging",
                 "gurgling", "humming",
                 "not hot", "not hot enough", "not warm", "not warm enough", "lukewarm", "tepid",
                 "water is not hot", "water not hot", "water isn't hot", "water isnt hot",
                 "hot then cold", "hot and then cold", "hot then goes cold", "goes cold",
                 "runs cold", "airing cupboard", "stopcock", "cistern", "plumbing",
                 "hot water tank", "hot water cylinder", "immersion heater"),
          bias=2),
    entry("ground-size", (tuple(one for words, _text in GROUNDS for one in words),
                          ("big", "size", "how big", "long", "wide", "how long", "how wide",
                           "metres", "yards", "dimensions")),
          _ground_size,
          avoid=("match", "game", "games", "rules", "players", "score", "scoring", "innings",
                 "offside", "how many", "open", "opening", "opened", "closed", "close",
                 "closing", "hours", "booking", "book", "session", "lessons", "distance",
                 "far", "near me", "directions", "nearest"),
          bias=1),
    *_RACE_ENTRIES,
    entry("running-and-knees",
          (("running", "run", "jogging", "jog"),
           ("knee", "knees", "joint", "joints", "cartilage")),
          "No: running does not wear out healthy knees, and long-term studies of runners find no "
          "more knee arthritis than in people who do not run. What does cause trouble is doing "
          "too much too soon, so build the distance slowly and keep the legs strong with squats, "
          "step-ups and single-leg work. If a knee hurts for more than two weeks or swells up, "
          "get it looked at rather than running through it.",
          avoid=_HURTS + _NOISY + ("stairs", "when i run", "when i'm running", "since",
                                   "fell", "twisted", "injury", "injured", "swollen"),
          bias=2),
    entry("offside", ("offside", ("work", "explain", "rule", "rules", "mean", "mean work",
                                  "football", "soccer", "how")),
          "You are offside if, at the moment the ball is played forward to you, you are in the "
          "other team's half, closer to their goal line than both the ball and the second-last "
          "defender, and then you get involved in play. Standing there is fine — it is touching "
          "the ball or interfering that is punished. There is no offside straight from a throw-in, "
          "a goal kick or a corner.",
          avoid=("rugby", "hockey", "ice hockey")),
    entry("football-basics", (("football", "soccer"),
                              ("how long", "long", "minutes", "players", "positions", "extra time",
                               "half", "halves", "pitch", "team size")),
          "A football match is two halves of 45 minutes, with 11 a side including the keeper, and "
          "the clock keeps running — it does not stop for injuries or substitutions. The 90 "
          "minutes is why teams time-waste, and why added time at the end of each half can be long.",
          avoid=("big", "size", "wide", "metres", "yards", "dimensions", "how big")),
    entry("tennis-scoring", ("tennis", ("score", "scoring", "points", "set", "sets", "work",
                                       "deuce", "tie-break", "tiebreak", "explain")),
          "Points go 15, 30, 40, game — a point each from deuce is advantage and then game, so you "
          "have to win two in a row. Six games wins a set, but you need a two-game lead, so 6-6 "
          "goes to a tie-break. Matches are usually best of three sets, and the big men's matches "
          "are best of five."),
    entry("cricket-basics", ("cricket", ("work", "rules", "over", "wicket", "wickets", "basics",
                                        "explain", "innings", "how", "scoring", "match", "first",
                                        "beginner", "beginners", "spectator")),
          "One team bats to score runs and the other bowls and fields to get them out; an over is "
          "six balls, and an innings ends when ten batters are out or the overs run out. You are "
          "out if the ball hits your stumps, if a fielder catches it before it bounces, if you are "
          "run out, or leg before wicket — hit on the pads by a ball that was going to hit the "
          "stumps.",
          avoid=("batting", "batting technique", "batting stance", "how do i bat",
                 "practice batting", "practise batting", "score more runs", "bowling action",
                 "how do i bowl", "how do i spin")),
    entry("rugby-basics", ("rugby", ("work", "rules", "basics", "explain", "how", "points",
                                     "scoring", "positions", "union", "long", "try", "tries",
                                     "minutes")),
          "In rugby union, 15 a side, you can only pass backwards — forward movement comes from "
          "running and kicking. A try is five points, the conversion two, a penalty three; a tackle "
          "becomes a ruck where both teams push for the ball, and the offside line moves as that "
          "happens. Two 40-minute halves, and the clock stops for injuries.",
          avoid=("league", "rugby league", "six tackles")),
    entry("rugby-league", (("rugby league", "rugby league team", "union and league",
                            "league and union"),
                           ("work", "rules", "basics", "players", "how many", "tackles", "points",
                            "try", "long", "minutes", "difference", "union", "team")),
          "Rugby league is 13 a side over two 40-minute halves, and the side with the ball gets "
          "six tackles to make progress before it goes to the other team. A try is four points "
          "and a penalty two, where union scores five and three - that is the quickest way to tell "
          "the two codes apart.",
          bias=2),
    entry("scrum", (("scrum", "scrums"),
                    ("what", "whats", "mean", "means", "is", "how", "work", "rugby", "do")),
          "A scrum restarts play after a knock-on or a forward pass: the eight forwards of each "
          "side bind together and push against the other pack, the scrum-half feeds the ball into "
          "the middle, and the hooker strikes it back with a foot. The side that shoves the other "
          "back can win the ball against the head."),
    entry("yellow-card", (("yellow card", "yellow cards", "red card", "red cards", "sin bin",
                           "sin-bin", "got booked", "gets booked", "get booked", "was booked",
                           "were booked", "been booked",
                           "player booked", "players booked", "a player booked", "he booked",
                           "she booked", "they booked", "booked mean", "booked mean in",
                           "bookings has he", "bookings has she", "bookings this season",
                           "book him", "book her", "book them", "booked him", "booked her",
                           "booked them", "ref book", "ref booked", "ref has booked",
                           "ref gave him"),
                          ("what", "whats", "mean", "means", "is", "how", "work", "football",
                           "rugby", "why", "get", "point")),
          "A yellow card is a formal warning. In football two of them in a match mean a red and "
          "the player is off, and a straight red carries at least a one-match ban; in rugby a "
          "yellow means ten minutes in the sin bin, and a second one is a red too.",
          guard=_a_card_is_named,
          avoid=(
                 "hotel", "hotels", "hostel", "b and b", "guest house", "airbnb", "cottage", "flight",
                 "flights", "ferry", "train", "tickets", "ticket", "restaurant", "table", "room",
                 "rooms", "campsite", "pitch", "venue", "appointment", "dentist", "doctor", "haircut",
                 "book film", "book and film", "book the film", "book or film", "novel",
                 "novels", "audiobook", "paperback", "kindle", "author", "chapter", "spoilers",
                 "holiday", "taxi", "car hire", "parking", "court", "festival", "festivals",
                 "concert", "concerts", "gig", "gigs", "booking fee", "booking fees", "refund",
                 "refunds", "cancelled", "canceled", "cancellation", "reservation", "reserved",
                 "book a", "booked a", "booking a",
                 "read", "novel", "novels", "reading", "reader", "author", "library", "kindle",
                 "audiobook", "bookshop", "chapter", "recommend", "club", "fiction", "nonfiction",
                 "poetry", "memoir", "biography", "depressing", "miserable",
                 "chapters", "my book", "a book", "what book", "which book", "this book",
                 "the book", "book to read")),
    entry("world-cup-winners", (("world cup", "world cup final", "the world cup"),
                                ("won", "win", "wins", "winner", "winners", "who", "which year",
                                 "which team", "champion", "champions", "held", "host", "hosted")),
          _world_cup,
          avoid=("rugby", "cricket", "t20", "ashes", "league", "hockey", "netball", "olympic",
                 "olympics", "snooker", "darts", "swimming", "athletics", "skiing", "f1")),
    entry("netball-basics", ("netball", ("work", "rules", "basics", "players", "explain", "how",
                                        "seven")),
          "Netball is seven a side, and the rule that surprises people is that you cannot move "
          "with the ball: catch it, and you have to pass or shoot within three seconds, with one "
          "foot planted. Each position is limited to certain thirds of the court, which is why "
          "goal shooters barely leave the circle.",
          avoid=("how long", "how many quarters", "minutes", "how many minutes")),
    entry("netball-length", (("netball", "netball match", "netball game"),
                             ("how long", "long", "last", "minutes", "quarters", "periods",
                              "how many quarters")),
          "Four 15-minute quarters, so 60 minutes of play, and about 75 minutes all told with the "
          "breaks. The clock stops for injuries and for the ball going out, so a close game can "
          "run a little past that.",
          bias=1),
    entry("darts-scoring", ("darts", ("score", "scoring", "rules", "501", "checkout", "work",
                                      "explain", "180", "maximum", "points",
                                      "play", "playing", "how long", "how many legs",
                                      "how many sets")),
          "In 501 both players start at 501 and count down, and you finish on a double or the "
          "bullseye — going below the target or landing on one is a bust and the turn is wiped. "
          "That is why players aim for treble 20s early and switch to a tidy double once they are "
          "under 170. Three treble 20s in one visit is 180, the highest score there is.",
          bias=1,
          avoid=("better", "improve", "throw", "throwing", "aim", "aiming", "technique",
                 "practice", "practise", "grip", "consistent", "straight", "tips", "accurate",
                 "accuracy")),

    entry("darts-throw",
          (("darts", "dart", "oche", "dartboard", "darts board"),
           ("better", "improve", "throw", "throwing", "aim", "aiming", "technique", "practice",
            "practise", "grip", "tips", "accurate", "accuracy", "consistent", "straight",
            "more consistent")),
          "Stand side-on with your front foot behind the oche and your weight on it, keep the "
          "elbow up and still, and throw from the elbow rather than the shoulder: same speed, "
          "same release, every dart. Practise grouping rather than scoring - twenty darts at the "
          "20 bed, trying to land them inside a hand's width - and finish every session with ten "
          "at a double, because doubles win legs.",
          avoid=("rules", "scoring", "checkout", "how many points", "bust", "world championship",
                 "alexandra palace", "on tv", "tickets"),
          bias=1),
    entry("coach-kids-first-session", (("coach", "coaching", "coached"),
                                       ("under-8s", "under 8s", "under-9s", "under-7s", "kids",
                                        "football", "team", "first session", "first training",
                                        "training", "session")),
          "Give every child a ball and keep them moving: ten minutes of a game with a ball each "
          "(dribble and freeze), fifteen of one skill in a small game (passing through gates, or "
          "1v1 to a line), then twenty minutes of small-sided matches, four a side, no keepers. No "
          "queues, no laps, no long instructions — if they stand still for more than a minute you "
          "lose them. Finish with a game they already love and a quick handshake line.",
          avoid=("cheaper", "cheapest", "cheap", "fare", "fares", "ticket", "tickets",
                 "price", "prices", "cost", "costs", "how much", "to get"),
          ask=("kids", "kid", "children", "child", "under-8s", "under 8s", "under-9s", "under-7s",
               "football", "soccer", "players", "player", "team", "teams", "session", "sessions",
               "drill", "drills", "pitch", "juniors", "youth", "warm up", "warmup", "first")),
    entry("coach-kids-attention", (("coach", "coaching", "coached", "training", "session"),
                                   ("keep them", "interested", "attention", "bored", "listen",
                                    "behaviour", "behaviour problems")),
          "Keep instructions under twenty seconds, show it once, then let them try it in a game — "
          "children learn by playing, not by queueing to take turns. Give every child a job or a "
          "ball, praise the one who does the thing you asked, and change the game every ten "
          "minutes. Two or three restless ones are easier to manage when the rest are busy.",
          ask=("coach", "coaching", "coached", "session", "sessions", "kids", "children",
               "child", "team", "teams", "players", "player", "drill", "drills", "club",
               "group", "class", "classes", "pitch", "court", "juniors", "youth", "match",
               "under 8", "under 10", "under 12", "under 14", "warm up", "warmup"),
          bias=1),

    entry("adult-sport-start", (("sport", "football", "netball", "hockey", "basketball", "rugby",
                                 "badminton", "squash"),
                                ("start", "again", "adult", "adults", "beginner",
                                 "beginning", "back into", "40", "fifty", "forty", "old",
                                 "too old", "am i too old",
                                 "safe", "safety")),
          "Look for a club that advertises a beginners' or \"back to\" session rather than a team "
          "trials night — most sports now run them, and the standard is friendly. Try three in a "
          "month before you judge, and go twice before deciding you are unfit for it, because the "
          "first session is always the worst one. Nobody at a casual session is watching you; they "
          "are all watching the ball.",
          avoid=("join", "joining", "near me", "where can i", "taster",
                 "boots", "boot", "studs", "astro", "shin pads", "trainers", "kit", "shirt",
                 "shorts", "socks", "gloves", "gum shield", "goggles", "racket", "bat",
                 "broken", "broke", "fracture", "fractured", "cast", "plaster", "sprain",
                 "sprained", "injury", "injured", "operation", "surgery", "heal", "healing",
                 "physio", "crutches", "recovery",
                 "bad back", "bad knee", "sore", "aches", "aching", "heart condition",
                 "asthma", "pregnant", "pregnancy"),
          bias=1),
    entry("fit-timeline",
          (("how long", "how many weeks", "how many months", "how soon", "when will i",
            "how long until", "how long before"),
           ("get fit", "fitter", "fitness", "see results", "see a difference",
            "notice a difference", "feel a difference", "feel better", "stronger", "toned",
            "in shape", "shape", "start exercising", "start running", "start the gym")),
          "How you feel changes first: two to three weeks of regular sessions and the stairs and "
          "your sleep are easier. Visible change takes about six to eight weeks, and the real "
          "difference by three to six months when it shows in what you can do rather than in the "
          "mirror. Three sessions a week that you actually keep beat five you abandon.",
          avoid=("lose a stone", "lose weight", "weight", "kilos", "pounds", "lbs", "stone",
                 "diet", "slim")),
    entry("kids-sport-choose", (("sport", "club", "activity", "classes"),
                                ("shy", "nervous", "try", "choose", "which", "kids", "son",
                                 "daughter", "reluctant", "hates")),
          "Try two or three taster sessions before choosing anything: the club matters far more "
          "than the sport. Pick one where the coach learns the children's names, keeps everyone "
          "playing, and the ratio of adults to children is decent — and for a shy child, a smaller "
          "club beats a big one with a waiting list. Ask if you can watch the first session from "
          "the side.",
          avoid=("faint", "fainted", "fainting", "pass out", "passed out", "collapsed",
                 "unconscious", "went white", "seizure", "ambulance")),
    entry("adult-swim-lessons", (("swim", "swimming", "swimmer", "learn to swim",
                                  "learning to swim"),
                                 ("can't", "cant", "cannot", "adult", "learn", "lessons", "teach",
                                  "beginner", "embarrassed", "worth it",
                                  "never learnt", "never learned")),
          "Adult lessons at your local pool are the fastest route: most run classes for complete "
          "beginners, often in small groups, and every instructor has taught adults who are "
          "frightened of the water. Book a course rather than one lesson, start in the shallow end "
          "with floats, and ask for an instructor who is used to nervous beginners. Nobody in an "
          "adult class is watching anybody else.",
          ask=("learn", "learning", "learnt", "learned", "can't", "cant", "cannot", "adult",
               "adults", "lessons", "lesson", "teach", "taught", "beginner", "beginners",
               "never learned", "never learnt", "dont know how", "don't know how", "how do i swim",
               "embarrassed", "frightened", "scared", "nervous", "worth it"),
          avoid=("child", "children", "kid", "kids", "son", "daughter", "toddler", "baby",
                 "school", "nursery", "my boy", "my girl", "grandson", "granddaughter"),
          bias=2),
    entry("child-swimming",
          (("my son", "my daughter", "my kid", "my child", "my children", "our son",
            "our daughter", "our kids", "son", "daughter", "child", "children", "kid", "kids",
            "grandson", "granddaughter", "nephew", "niece", "little one", "year old",
            "years old", "reception", "primary school"),
           ("swim", "swims", "swimming", "swimmer", "learn to swim", "learning to swim",
            "cant swim", "can't swim", "cannot swim", "couldnt swim", "couldn't swim",
            "swim lesson", "swim lessons", "swimming lesson", "swimming lessons",
            "lessons", "lengths", "metres", "metre", "badge", "widths", "float", "floats",
            "float on", "armbands", "arm bands", "water wings", "noodles", "face in the water",
            "face in water", "underwater", "under water", "head under", "tread water",
            "front crawl", "backstroke", "pool", "pools", "lido", "splash", "splashing",
            "scared of the water", "frightened of the water", "afraid of the water",
            "scared of water", "frightened of water", "afraid of water",
            "scared of the pool", "frightened of the pool", "afraid of the pool",
            "hates the water", "hates water", "wont get in the water", "wont get in the pool",
            "scared of swimming", "frightened of swimming", "afraid of swimming")),
          "Most children swim somewhere between five and eight, and time in the water with you "
          "does more than a weekly class they dread: short warm visits where they choose to put "
          "their face in beat a lesson they cry through. For a nervous one, goggles and bubbles "
          "at the side first, then holding the rail and putting one ear under at a time, and "
          "never hold them under - one dunking sets a nervous swimmer back months. What they "
          "need to be safe in the shallow end is to float on their front and back, turn round, "
          "and get to the side and climb out, and the width badge usually comes a season after "
          "that. Give it a term before you worry, and if they are seven or over and still "
          "frightened, a few one-to-one lessons are worth the money.",
          avoid=("baby", "babies", "newborn", "infant", "infants", "toddler", "toddlers",
                 "3 months", "three months", "4 months", "four months", "5 months",
                 "five months", "6 months", "six months", "7 months", "seven months",
                 "8 months", "eight months", "9 months", "nine months", "10 months",
                 "ten months", "11 months", "eleven months", "months old", "month old",
                 "weeks old", "6 week", "six week", "bath", "bathtime", "nappy", "nappies",
                 "drink", "drinks", "drinking", "water intake", "how much water",
                 "not breathing", "isnt breathing", "couldnt breathe", "limp", "unresponsive",
                 "sank", "didnt come up", "fell in", "pulled out", "drowned", "drowning",
                 "blacked out", "blacking out", "passed out", "passing out",
                 "fainted", "fainting", "unconscious", "knocked out", "seizure",
                 "river", "canal", "lake", "reservoir", "sea", "beach", "lifeguard",
                 "eat", "eats", "eating", "ate", "food", "foods", "breakfast", "lunch",
                 "dinner", "snack", "snacks", "meal", "carb", "carbs", "fuel",
                 "dog", "dogs", "puppy", "vet")),
    entry("head-under-water",
          (("under water", "underwater", "under the water", "head under", "face in the water",
            "go under", "goes under", "going under", "went under", "duck under", "submerge",
            "dunk", "going under water", "go under water",
            "frightened of going under", "scared of going under", "afraid of going under",
            "frightened of the water", "scared of the water", "afraid of the water",
            "frightened of water", "scared of water", "afraid of water",
            "scared of the pool", "afraid of the pool", "frightened of the pool",
            "scared of swimming", "afraid of swimming", "scared to jump in", "afraid to jump in",
            "frightened to jump in", "scared of jumping in", "wont jump in", "wont get in",
            "scared to get in", "afraid to get in", "frightened to get in",
            "wont go in the water", "wont go in the pool", "put her face in the water",
            "put his face in the water", "put my face in the water", "face in the pool",
            "wont put her face in", "wont put his face in", "wont put my face in",
            "water in his face", "water in her face", "water in my face", "water in the face",
            "water in his eyes", "water in her eyes", "water up his nose", "water up her nose",
            "getting water in his face", "getting water in her face", "splash in his face",
            "splash in her face", "water on his face", "water on her face",
            "fear of going under", "fear of going under water", "fear of going underwater",
            "fear going under", "fear of the water", "fear of water", "fear of the pool",
            "phobia of the water", "phobia of water", "phobia of going under",
            "dread going under", "dread going under water", "dreads going under",
            "dread the water", "dread getting in",
            "hold my breath", "holds my breath", "holding my breath", "held my breath",
            "hold his breath", "holds his breath", "holding his breath",
            "hold her breath", "holds her breath", "holding her breath",
            "hold their breath", "holds their breath", "hold your breath"),
           ("head", "face", "swim", "swimming", "pool", "lesson", "lessons", "scared",
            "afraid", "frightened", "terrified", "nervous", "wont", "won't", "cant", "can't",
            "cannot", "hate", "hates", "hated", "struggle", "panic", "goggles", "nose",
            "fear", "fears", "feared", "fearful", "phobia", "dread", "dreads", "dreaded",
            "breath")),
          "Start where you can stand up: hold the rail in the shallow end and put your chin in, then "
          "your mouth, then blow bubbles with your nose and mouth under for a second, and build it up "
          "over a few visits - goggles, and a nose clip if the water up your nose is the worst of it, "
          "get most adults past this. An adult beginner class teaches exactly this in the first "
          "lesson, and the instructor has seen it a hundred times. With a child it is the same thing "
          "at their size: let them watch and splash their own face at bath time, and never hold them "
          "under - one dunking sets a nervous swimmer back months.",
          guard=_a_block_in_the_water,
          avoid=("not breathing", "isnt breathing", "isn't breathing", "couldnt breathe",
                 "couldn't breathe", "limp", "unresponsive", "blue", "didnt come up",
                 "didn't come up", "slipped", "sank", "face down", "pulled out", "fell in",
                 "blacked out", "black out", "blacking out", "passed out", "passing out",
                 "fainted", "fainting", "unconscious", "ambulance", "drowning",
                 "boiler", "leak", "leaking", "radiator", "drain", "flood", "sink",
                 "phone", "watch", "kettle", "washing machine", "dishwasher", "water broke",
                 "baby", "babies", "newborn", "infant", "6 month", "six month"),
          bias=4),
    entry("carbo-loading",
          (("carbo load", "carbo loading", "carbo-load", "carb load", "carb loading",
            "carbohydrate loading", "glycogen", "pasta party"),
           ("why", "what", "how", "athletes", "runners", "cyclists", "before", "race",
            "marathon", "does it work", "help", "worth it", "when")),
          "Carb loading tops up the glycogen in your muscles, the fuel they run on in the last "
          "hour of a long race - the reason a marathoner hits the wall near 20 "
          "miles. It only helps for events over 90 minutes: take the last two days easy and eat "
          "8 to 10g of carbohydrate per kilo of bodyweight a day, rice, pasta, bread and "
          "potatoes, keeping the fat and fibre low so it does not sit heavy. Drink and salt "
          "matter too, and nothing new on race day.",
          avoid=("diabetes", "diabetic", "blood sugar", "keto", "low carb", "weight loss",
                 "lose weight", "type 2", "insulin"),
          ask=("why", "what", "how", "does", "is", "should", "when"),
          bias=1),
    entry("parkrun-first", ("parkrun", ("what", "start", "first", "join", "do", "beginners",
                                       "walk", "slow", "how")),
          "Parkrun is a free, timed 5k every Saturday at 9am in a local park: register once online, "
          "print or screenshot your barcode, and turn up ten minutes early for the first-timers' "
          "briefing. Walkers are genuinely welcome and plenty of people walk it, so you will not be "
          "last on your own. No barcode, no time — but you can still run."),
    entry("stadium-first-time", (("stadium", "ground", "match", "tickets"),
                                 ("first time", "what to expect", "what do i need", "away",
                                  "football", "before", "arrive", "bag")),
          "Arrive 45 minutes early the first time: queues at the turnstiles and bag searches are "
          "what make people miss kick-off. Take the card you booked with, check whether your stand "
          "is seated or standing, and expect to be close to strangers and loud for two hours — that "
          "is the point. At half time, either go for food in the first five minutes or wait until "
          "the second half starts.",
          avoid=("referee", "refereeing", "run the line", "linesman", "whistle", "offside",
                 "get tickets", "buy tickets", "ticket for a match",
                 "wet", "too wet", "pitch", "waterlogged", "frozen", "snow", "frost", "muddy",
                 "called off", "play", "playing", "training", "kids", "junior")),
    entry("wet-pitch", (("wet", "raining", "rain", "waterlogged", "frozen", "snow", "frost",
                         "muddy", "mud", "ground", "pitch", "called off"),
                        ("football", "match", "game", "pitch", "ground", "play", "playing",
                         "called off", "go ahead", "training", "kids", "junior")),
          "The referee decides, not the forecast: a pitch with standing water or frozen ground is "
          "called off, and a soft, muddy one usually still plays. Take moulded studs or boots for "
          "soft ground, a change of socks and a spare towel, and check the club's page or the "
          "league's feed an hour before you leave. Junior games are called off sooner than adult "
          "ones, and there the league, not the referee, has the last word.",
          avoid=("arrive", "turnstiles", "tickets", "stadium", "stand", "seated", "kick-off",
                 "away", "premier league", "tv", "watch", "how many", "capacity", "parking",
                 "refund", "refunds", "money back", "get my money", "claiming"),
          bias=1),
    entry("wimbledon-titles", ("wimbledon", ("record", "titles", "wins", "won", "most",
                                             "most titles", "serena", "federer")),
          "Martina Navratilova has nine singles titles, the record, and Roger Federer has eight "
          "among the men. Serena Williams won seven."),
    entry("rugby-offside", ("offside", ("rugby", "ruck", "maul")),
          "Rugby offside is about where you stand relative to the ball, not the goal line: stay "
          "behind the ball, or behind the last foot of the ruck or maul, until it is played away, "
          "and come back onside before you get involved. In open play, a team-mate's kick puts you "
          "offside until you are put onside by a chase or a pass — and standing in front of the "
          "kicker and going for the ball is the one that gives away a penalty.",
          bias=1),

    entry("handball", ("handball", ("shoulder", "arm", "hand", "ball", "count", "counts",
                                    "accidental", "deliberate", "what", "rules", "mean", "means")),
          "Handball is when the ball touches the arm below where the armpit ends: the shoulder "
          "and the very top of the arm are fine. It also counts when the arm makes the body "
          "bigger, even by accident — which is why defenders tuck their arms behind their backs "
          "in the box."),
    entry("penalty-shootout", (("penalty shootout", "penalties", "shootout", "penalty"),
                               ("how", "work", "works", "what", "who", "how many", "order",
                                "taken", "five", "misses", "football", "soccer", "world cup")),
          "Five players from each team take a penalty each, in turn, and the side that scores more "
          "wins; if it is still level after all ten, it goes to sudden death, one each until one "
          "side misses. Everyone else waits on the halfway line, the keeper has to keep one foot "
          "on the line, and the same player cannot take twice until everyone who can has taken one.",
          avoid=("hockey", "ice", "rugby", "gaelic", "nfl", "american football", "handball",
                 "water polo", "parking", "speeding", "fine", "points on")),
    entry("golf-scoring", ("golf", ("score", "scoring", "par", "birdie", "bogey", "handicap",
                                    "stableford", "points", "eagle", "albatross", "under par",
                                    "over par", "how do you score", "how does scoring work")),
          "Every hole has a par, and you count the shots you take: one under is a birdie, two "
          "under an eagle, three under an albatross, and one over is a bogey, two over a double "
          "bogey. Add up the stroke count over 18 holes and "
          "the lowest total wins; your handicap is the number subtracted from your total so players "
          "of different ability can compete.",
          avoid=("swing", "slice", "hook", "grip", "putt", "putting", "chip", "chipping",
                 "drive", "driver", "improve", "fix", "fixing", "better", "practice", "lesson",
                 "lessons", "tips", "beginner", "start playing", "join")),
    entry("golf-score-names", (("birdie", "birdies", "bogey", "bogeys", "eagle", "albatross",
                               "par", "handicap", "handicaps"),
                              ("what", "whats", "mean", "means", "is", "score", "scoring",
                               "under", "over", "good")),
          "Par is the score a good player should take on the hole. One under par is a birdie, two "
          "under an eagle, three under an albatross, and one over is a bogey - two over is a "
          "double bogey. A handicap is about your average score over par, so 18 is a shot a hole "
          "over par; single figures is a strong club player and scratch is zero.",
          avoid=("how many", "how long", "course", "round", "swing", "putt")),
    entry("golf-round", (("round of golf", "golf round", "18 holes", "eighteen holes",
                          "nine holes", "9 holes", "golf group", "golf course", "golf"),
                         ("holes", "how long", "take", "takes", "long",
                          "players", "in a round")),
          "A round of golf is 18 holes, and a full round on foot takes about four hours - about "
          "two hours for nine. A group is up to four players, and the winner is whoever takes the "
          "fewest shots.",
          avoid=("score", "scoring", "par", "birdie", "bogey", "handicap", "eagle", "stableford",
                 "swing", "slice", "hook", "grip", "putt", "putting", "chip", "chipping",
                 "improve", "fix", "practice", "lesson", "lessons", "tips", "learn",
                 "beginner", "join", "club", "clubs",
                 "long is", "how far", "length", "yardage", "yards", "acres", "miles",
                 "kilometres", "kilometers", "calorie", "calories", "burn", "burned",
                 "burning", "team", "teams")),
    entry("golf-chip",
          (("chip", "chips", "chipping", "chip shot", "chip shots", "pitch", "pitching",
            "pitch shot", "pitch shots", "short game", "wedge", "lob wedge", "sand wedge",
            "golf shot", "golf shots"),
           ("golf", "green", "pin", "flag", "hole", "shot", "shots", "chip", "pitch", "club",
            "clubs", "wedge", "iron", "ball", "technique", "hit", "stop", "close", "better",
            "thin", "thinning", "chunk", "chunking", "top", "topping", "blade", "blading",
            "skull", "skulling", "fat", "distance", "roll", "carry", "lie", "rough", "fairway",
            "off the green", "onto the green", "short game", "practise", "practice",
            "practising", "practicing", "drill", "drills")),
          ("A chip is a small, low shot from just off the green, and the trick is to hit down on "
           "it rather than scoop it up: take a 7, 8 or 9 iron, put the ball back in your stance "
           "with your hands ahead of it and your weight on your front foot, and make the same "
           "small swing back and through so the club takes the ball first and the turf after. "
           "Land it about a third of the way onto the green and let it run out, and change club "
           "rather than swing harder for a longer chip - a 7 iron runs more, a wedge stops sooner. "
           "A pitch is the same idea with a fuller swing and more loft, so the ball flies most of "
           "the way and stops quickly. If you keep thinning or chunking them, you are trying to "
           "help the ball into the air: keep the hands ahead, don't flick the wrists, and brush "
           "the grass after the ball."),
          guard=_a_short_game_to_play,
          avoid=("potato", "potatoes", "chips and", "fries", "crisps", "chip shop", "chippy",
                 "chip pan", "oven", "air fryer", "deep fry", "deep fryer", "recipe", "cook",
                 "cooking", "roast", "bake", "frozen", "salt", "vinegar", "peel",
                 "windscreen", "windshield", "paint", "paintwork", "car", "van", "plate", "cup",
                 "mug", "bowl", "tile", "worktop", "table", "nail", "tooth",
                 "putt", "putting", "putter", "drive", "driver", "handicap", "score", "scoring",
                 "par", "birdie", "bogey", "eagle", "bunker", "sand", "tee", "swing", "slice",
                 "hook", "grip", "lesson", "lessons", "handicap", "stableford", "how many",
                 "calorie", "calories", "present", "gift", "money", "fiver", "tenner",
                 "contribute", "contribution", "collection", "how much", "much", "should i",
                 "office", "leaving", "colleague", "colleagues", "birthday", "wedding")),
    entry("knee-outside-pain", (("knee", "knees",
                                 "it band"),
                                ("outside", "outer", "side of my knee", "it band",
                                 "runs down the outside"),
                                ("run", "running", "jog", "jogging", "cycle", "cycling")),
          "Pain on the outside of the knee that comes on after ten or twenty minutes of running is "
          "usually the iliotibial band rubbing: it is a tracking problem, not a worn joint. Cut the "
          "run short at the first twinge rather than running through it, run on flatter, softer "
          "ground, and shorten your stride. Twice a day, foam-roll the outside of the thigh and do "
          "side-lying leg raises and clams; it settles in weeks if you keep runs short till it does.",
          bias=2,
          ask=("outside", "outer", "side of my knee", "it band", "runs down the outside"),
          avoid=("front", "stairs", "stair", "downstairs", "climbing", "swelling", "swollen",
                 "locked", "locking", "gave way", "clicking", "surgeon", "arthroscopy",
                 "cruciate", "acl", "meniscus")),
    entry("race-distances", (("5k", "10k", "10km", "parkrun distance"),
                             ("far", "long", "miles", "km", "kilometres", "kilometers",
                              "distance", "how")),
          "A 5k is 3.1 miles and a 10k is 6.2 miles; a half marathon is 13.1 miles (21.1 km) and a "
          "marathon 26.2 miles (42.2 km). Races are named in kilometres but most runners in the UK "
          "and the US talk in miles, which is why the two numbers never look related.",
          avoid=("marathon", "train", "training", "plan", "pace", "faster", "improve",
                 "save", "saves", "saving", "saved", "money", "afford", "budget", "deposit",
                 "cash", "pound", "salary", "invest", "debt", "savings",
                 "couch to 5k", "couch to five k", "c25k"),
          bias=1),
    entry("marathon-distance", ("marathon", ("long", "longer", "longest", "km", "miles", "42",
                                             "how", "length", "distance", "far",
                                             "difference", "compare", "compared", "versus",
                                             "vs", "twice", "further")),
          "A marathon is 26.2 miles, or 42.2 kilometres \u2014 the odd 0.2 is there because the "
          "1908 London course was extended to finish in front of the royal box. A half marathon "
          "is the obvious first step, and most training plans build up to it over about sixteen "
          "weeks.",
          avoid=("train", "training", "plan", "planning", "prepare", "preparing", "build up",
                 "ready", "couch", "beginner", "slowest", "pace", "time"),
          guard=_half_is_not_the_question),
    entry("marathon-training", ("marathon", ("train", "training", "plan", "prepare", "build up",
                                             "first marathon", "ready", "couch", "start running")),
          "Start where you can already run 5km comfortably and build up over about sixteen weeks: "
          "three runs a week (one long, two short and easy), and add no more than 10% to the weekly "
          "total. Your longest run only needs to reach 32km, three weeks before the day, then taper "
          "— the last two weeks are much shorter on purpose. Do not do your longest run and your "
          "fastest in the same week."),
    entry("cramp-running", (("cramp", "cramps", "cramping"),
                            ("run", "running", "jog", "jogging", "exercise", "exercising",
                             "workout", "training", "after", "walking", "walk", "playing")),
          "Cramp in a run is usually a tired muscle, not a lack of salt: it comes on late in a "
          "session and eases when you stop and stretch. Walk, then stretch the calf against a "
          "wall for 20 to 30 seconds. To keep it away, build your distance more slowly and drink "
          "water with a pinch of salt if you sweat heavily for more than an hour.",
          avoid=("period", "periods", "stomach", "tummy", "dog", "cat"),
          bias=2),
    entry("knee-noise", (_NOISY, ("knee", "knees", "kneecap", "joint", "joints")),
          _noisy_knee),
    entry("knee-pain-stairs", (("knee", "knees"),
                               ("stairs", "stair", "staircase", "steps", "climb", "climbing",
                                "downstairs", "upstairs", "up steps", "down steps")),
          "Pain at the front of the knee on stairs is the kneecap being pulled off line by weak "
          "or tight muscles around it, which is common in new runners and in people who sit all "
          "day. Three times a week do sit-to-stands, step-ups and wall sits, and ease off hills "
          "and deep squats for a fortnight. See a physio if it swells, locks, or the knee gives "
          "way under you.",
          avoid=_NOISY + ("fell", "fall", "fallen", "twisted", "landed", "can't walk",
                          "cant walk")),
    entry("protein-how-much", ("protein", ("much", "need", "needed", "day", "daily", "grams",
                                          "grammes", "enough", "target", "get")),
          _protein,
          ask=("a day", "per day", "daily", "in a day", "do i need", "i need", "need",
               "should i eat", "should i have", "to build muscle", "build muscle", "bulk",
               "bulking", "lose weight", "losing weight", "per kilo", "a kilo", "per kg",
               "my weight", "body weight", "weigh", "target", "enough", "diet", "each meal",
               "a meal", "protein powder", "grams of protein", "grammes of protein",
               "how many grams"),
          avoid=("dog", "cat", "puppy", "kitten", "rabbit", "hamster", "horse",
                 "egg", "eggs", "chicken", "beef", "steak", "pork", "fish", "salmon", "tuna",
                 "milk", "cheese", "yoghurt", "yogurt", "beans", "lentils", "tofu", "oats",
                 "porridge", "bread", "rice", "pasta", "banana", "apple", "nuts", "almonds",
                 "peanut", "powder", "shake", "burger", "bacon")),
    entry("how-often-to-run", (("run", "running", "jog", "jogging", "go out", "going out",
                                "get out for", "out for a run", "out running"),
                               ("how many days", "days a week", "times a week", "a week",
                                "days in a week", "days in the week", "rest days", "too many days",
                                "how much",
                                "how long")),
          "Three runs a week is plenty to start, with a rest day between each: two easy runs of "
          "20 to 30 minutes and one a little longer. Add a fourth only when those three feel "
          "comfortable, and keep any increase to about 10% a week. The rest days are when the "
          "fitness is built, so they are part of the plan, not a gap in it.",
          avoid=("car", "cars", "cost", "costs", "petrol", "insurance", "mot", "train", "bus",
                 "marathon", "half marathon", "10k", "5k", "parkrun", "race", "pace", "faster",
                 "calories", "weight", "shoe", "shoes", "injury", "knee", "shin", "sore", "pain",
                 "plan", "training plan", "treadmill speed", "treadmill pace",
                 "rest between", "between runs", "between each run", "how long to rest",
                 "rest after", "how long should i rest", "recovery",
                 "after eating", "after a meal", "after lunch", "after dinner", "eating",
                 "ate", "wait", "waiting", "in the cold", "cold", "cold weather", "cold out",
                 "in the heat", "the heat", "hot weather", "raining", "rain", "wind", "windy")),

    entry("start-running",
          (("couch to 5k", "couch-to-5k", "couch to 5 km", "c25k",
            "running", "run", "jogging", "jog", "ran", "jogged", "went running",
            "runner", "runners", "new runner", "beginner runner"),
                            ("start", "starting", "begin", "beginner", "never", "nothing",
                             "couch", "first", "get into", "getting into",
                             "out of breath", "out of puff", "can't run", "cant run",
                             "get back into", "getting back into",
                             "used to run", "used to jog", "havent run", "haven't run",
                             "stopped running", "start running", "running after years",
                             "jog after years", "been years",
                             "years since", "years ago", "since school",
                             "without stopping", "non stop", "nonstop", "keep going",
                             "all the way",
                             "tips", "tip", "advice", "any advice", "pointers",
                             "barely", "barely jog", "cant even", "can't even",
                             "can only", "only manage", "manage to jog", "manage to run",
                             "struggle", "struggling", "really hard", "so hard",
                             "for a minute", "two minutes", "2 minutes", "a few minutes",
                             "30 seconds", "thirty seconds")),
          "Start with run-walk: one minute of easy jogging, two minutes of walking, repeated for "
          "20 minutes, three times a week with a rest day between. Each week add a minute to the "
          "jog and take one off the walk, and in about eight weeks you will run 20 minutes "
          "without stopping. Go slowly enough to speak in short sentences - that is the pace that "
          "builds the habit.",
          avoid=("marathon", "half marathon", "10k", "parkrun", "race", "train", "training",
                 "plan", "shoe", "shoes", "sore",
                 "knees", "ankles", "shins", "calves", "achilles", "plantar", "soreness",
                 "hurt", "hurts", "hurting", "pain", "pains", "painful", "ache", "aches",
                 "aching", "stiff", "swollen", "swelling", "bend", "bending", "limp", "limping",
                 "my injury", "the injury", "an injury", "injury is", "injury has",
                 "injury wont", "injured my", "got injured", "been injured", "was injured",
                 "am injured", "is injured", "back from injury", "back from an injury",
                 "recovering from", "recovery from", "knee injury", "shin injury",
                 "ankle injury", "injury prevention",
                 "when injured", "after injury", "after an injury", "running injured",
                 "run injured", "still injured", "start running injured",
                 "im injured", "i'm injured",
                 "knee", "shin", "rest", "between",
                 "how often", "days a week", "car", "cost", "boiler", "cheaper",
                 "app", "apps", "game", "games", "phone", "laptop", "computer", "software",
                 "program", "programme", "windows", "console", "android", "iphone", "app store",
                 "operation", "surgery", "asthma", "hip", "doctor", "gp", "hospital",
                 "arthritis", "diagnosis", "disability", "wheelchair",
                 "toilet", "loo", "cistern", "tap", "taps", "flush", "flushing", "plumbing",
                 "sink", "leak", "leaking", "drip", "dripping", "engine", "motor", "fridge",
                 "freezer", "washing machine", "dishwasher",
                 "run ragged", "running ragged", "ran ragged", "run off my feet",
                 "run off our feet", "running off my feet", "off my feet",
                 "back on my feet",
                 "eat", "eats", "eating", "ate", "food", "foods", "diet", "nutrition",
                 "carbs", "carb", "fuel", "fuelling", "fueling", "breakfast", "hydration",
                 "hydrate", "drink", "drinks", "protein", "caffeine", "gel", "gels",
                 "rug", "rugs", "carpet", "carpets", "hallway", "hall", "corridor", "stairs",
                 "bean", "beans", "sledge", "sled", "plant", "plants", "creeping",
                 "runner up", "runner-up", "front runner", "frontrunner", "job", "interview",
                 "candidate", "horse", "horses", "racehorse", "race horse")
                 + _REPORTED),
    entry("run-faster-easy-miles",
          (("get better at running", "better at running", "improve my running", "run faster",
            "get faster", "running faster", "faster", "improve my 5k", "better 5k", "5k time",
            "my 5k", "10k time", "get quicker", "personal best", "pb", "pace", "sprint",
            "interval", "intervals", "hill repeats"),
           ("run", "running", "jog", "jogging", "train", "training", "faster", "quicker",
            "time", "improve", "better", "get")),
          "Speed comes from easy miles, not hard ones: run four times a week with three of those "
          "slow enough to chat through, and make the fourth the only hard session - 6 x 2 minutes "
          "quick with 2 minutes of jogging in between, at a pace where you could manage one more. "
          "Add 5 to 10% a week, keep one full rest day, and expect six to eight weeks before the "
          "same 5k feels easier. Runners who only go hard stall after a month.",
          avoid=("heart", "heartbeat", "pulse", "beat", "beats",
                 "start", "starting", "beginner", "never run", "couch", "first run", "out of breath",
                 "how far", "how long is", "miles", "km", "kilometres", "kilometers",
                 "marathon", "half marathon", "train for", "training for", "plan for",
                 "injury", "injured", "knee", "shin", "splints", "pain", "sore", "hurt",
                 "shoe", "shoes", "watch", "app", "treadmill", "program",
                 "heart", "heartbeat", "heart rate", "pulse", "beats")
                 + _REPORTED + _ASKED_AFTER,
          ask=("run", "running", "runner", "ran", "jog", "jogging", "5k", "10k", "mile",
               "miles", "marathon", "pace", "sprint", "sprints", "interval", "intervals",
               "hill", "hills", "training", "train")),
    entry("stitch", ("stitch", ("run", "running", "jog", "jogging", "side", "get", "getting",
                                "exercise", "walk")),
          "A stitch is a cramp in the sheet of muscle under the diaphragm, and it usually means "
          "you are breathing shallowly or ran too soon after eating. Slow down, breathe out hard "
          "through pursed lips, and press your fingers under the ribs on the sore side while you "
          "walk it off. Leave two hours between a proper meal and a run, and warm up for five "
          "minutes before you pick up the pace.",
          guard=_not_a_stitch_in_a_wound),
    entry("sore-after-exercise", (("sore", "aching", "achy", "stiff", "stiffness", "tender",
                                   "hurt", "hurts", "hurting", "ache", "aches"),
                                  ("gym", "workout", "exercise", "run", "running", "weights",
                                   "lifting", "next day", "day after", "two days", "walking")),
          "That ache a day or two after new exercise is normal and it is not damage: it is the "
          "muscle repairing itself after work it is not used to. Keep moving gently - a walk, an "
          "easy swim - rather than resting completely, drink water, and expect it to be worst "
          "about 48 hours in and gone within four days. Next time start with less weight or fewer "
          "repeats than you think you can do.",
          avoid=("throat", "burn", "sunburn", "mouth", "eyes", "eye", "ulcer", "cough", "cold",
                 "when i walk", "when i walking", "when i run", "when i stand", "when i sit",
                 "when i climb", "when i bend", "when i lift", "when i move", "when i type",
                 "when i wake", "when i get up", "when i go up", "aches when", "ache when",
                 "hurting when", "hurts when", "hurting when", "pain when", "all the time",
                 "every day", "every morning")),
    entry("stretch-calf", (("stretch", "stretches", "stretching", "loosen", "tight"),
                           ("calf", "calves", "achilles", "shin", "shins", "leg", "legs",
                            "after a run", "after running", "before a run", "hamstring",
                            "hamstrings", "quads", "quad", "thigh", "thighs",
                            "cycling", "cycled", "cycle ride", "after a ride", "spin class")),
          _stretch,
          bias=1,
          avoid=("bed", "sleep", "back", "neck", "shoulder", "shoulders", "hair", "canvas",
                 "ear", "ears", "leather", "shoes", "waistband", "jeans")),
    entry("rest-days", (("rest days", "rest day", "recovery days", "recovery day",
                         "days off training", "days off the gym"),
                        ("need", "many", "how", "gym", "training", "train", "week", "between",
                         "running", "exercise", "weights", "should")),
          "The rule that works for most people is one full rest day a week plus an easy day "
          "between hard ones: never two hard sessions back to back. Muscle is built while you "
          "recover, not while you lift. If you want to move every day, make the in-between days "
          "walks, easy swimming or stretching rather than another full session.",
          ),
    entry("rest-between-sessions", (("rest", "recovery"),
                                    ("after", "between", "sessions", "workout", "workouts",
                                     "lifting", "training", "gym")),
          "One easy day between hard sessions is enough, and it does not have to be a day in bed: "
          "a walk, a swim or stretching keeps you moving without loading the same muscles. Two "
          "hard sessions back to back is the pattern that leaves people sore and stale. Sleep and "
          "food do more of the rebuilding than any recovery gadget.",
          avoid=("bed", "sleep", "nap", "tired", "baby", "work", "holiday", "tweaked", "tweak",
                 "bad", "hurt", "hurts", "pulled", "injury", "injured", "slipped", "boxes",
                 "back",
                 "sets", "set", "reps", "rep", "between sets", "each set")),
    entry("how-often-exercise", (("run", "running", "jogging", "gym", "exercise", "workout",
                                  "workouts", "weights", "swim", "swimming"),
                                 ("how often", "how many times", "times a week", "days a week",
                                  "per week", "a week", "frequency", "regularly")),
          "Three sessions a week is the number to aim for, with a day off between them, and it is "
          "the same for running, the gym or swimming. The health guideline is 150 minutes of "
          "something that makes you breathe harder each week, which is three 50-minute sessions "
          "or five half hours. Two or three weeks in, that gets easier and you can add a session.",
          avoid=("rest", "marathon", "10k", "parkrun", "race"),
          guard=_not_a_timetable_that_runs),
    entry("recovery-time",
          (("recover", "recovers", "recovery", "recovering", "rest up", "ease back",
            "easy days", "legs recover"),
           ("how long", "how many days", "how much rest", "days", "how soon", "when can i",
            "time off", "how many weeks")),
          _recovery_time,
          ask=("recover", "recovers", "recovery", "recovering", "rest up", "ease back",
               "easy days", "legs recover"),
          bias=3,
          avoid=("ill", "illness", "flu", "cold", "fever", "sick", "virus", "covid",
                 "chest infection", "cough", "throat", "tonsillitis", "pneumonia",
                 "surgery", "operation", "hospital", "injury", "injured", "physio",
                 "broken", "fracture", "fractured", "sprain", "sprained", "strain",
                 "strained", "sore", "pain", "hurt", "hurts", "addiction", "grief",
                 "divorce", "breakup", "depression", "burnout", "bereavement",
                 "password", "account", "email", "file", "files", "laptop", "phone",
                 "car", "van", "vehicle", "truck", "deleted", "data", "photos",
                 "position", "room", "service", "boiler", "heat", "waste", "copper",
                 "gold", "oil", "sleep", "nap", "baby", "birth", "caesarean",
                 "cat", "cats", "dog", "dogs", "puppy", "puppies", "kitten", "kittens",
                 "pup", "vet", "neuter", "neutering", "neutered", "spay", "spayed",
                 "stitches", "wound", "scar", "burn", "bruise", "twisted", "eye", "eyes",
                 "vision", "screen", "screens", "bug", "virus", "vomit", "vomiting",
                 "diarrhoea", "stomach", "food poisoning", "migraine", "tooth", "teeth",
                 "dental", "wisdom", "extraction", "jet lag", "hangover",
                 "replacement", "replacements", "hip", "hips", "knee", "knees", "shoulder",
                 "shoulders", "joint", "joints", "heal", "heals", "healing", "healed",
                 "cast", "plaster", "physiotherapy", "physiotherapist", "consultant",
                 "operation", "operated",
                 "sets", "set", "reps", "rep", "between sets", "each set")),
    entry("rest-after-a-distance",
          (("rest", "resting", "rest up", "rest day", "rest days", "day off", "days off"),
           ("how long", "how many days", "how much rest", "days", "how soon", "time off",
            "how many weeks")),
          _recovery_time,
          guard=_a_distance_is_named,
          bias=3,
          avoid=("ill", "illness", "flu", "cold", "fever", "sick", "injury", "injured",
                 "hurt", "hurts", "pain", "sore", "surgery", "operation", "hospital",
                 "replacement", "replaced", "hip", "knee", "shoulder", "joint", "heal",
                 "healing", "cast", "plaster", "physio",
                 "meat", "steak", "roast", "roasted", "chicken", "turkey", "lamb", "beef",
                 "pork", "brisket", "ribs", "joint of", "carving", "carve", "foil", "oven",
                 "sets", "set", "reps", "between sets", "each set")),
    entry("badminton-basics", ("badminton", ("play", "rules", "score", "scoring", "how", "court",
                                             "points", "serve")),
          "Games go to 21 points, and you score on every rally whoever served, so a game is quick; "
          "win two games and you win the match. The bit that catches beginners is that the shuttle "
          "cannot be hit before it crosses the net, and a serve has to go diagonally and land past "
          "the short service line.",
          avoid=("grip", "grips", "replace", "replacing", "restring", "resting", "strings",
                 "string", "tension", "tensions", "broken", "buy", "buying", "which racket",
                 "racket", "racquet", "shoes", "net", "height", "post")),
    entry("hat-trick", ("hat trick", ("what", "what's", "mean", "means", "three", "goals",
                                          "why", "called")),
          "Three goals by the same player in one match is a hat-trick, and a perfect one is three in "
          "a row with nobody else scoring in between. The name comes from cricket, where a bowler "
          "who took three wickets with three balls was given a hat by the club."),
    entry("f1-points", (("formula 1", "formula one", "f1", "grand prix"),
                        ("points", "score", "scoring", "work", "championship", "how", "win")),
          "Points go to the top ten: 25 for a win, then 18, 15, 12, 10, 8, 6, 4, 2, 1. The bonus "
          "point for the fastest lap only ran up to 2024 and has been dropped, so do not count on "
          "it. Sprint weekends pay points to the top eight, and the driver and the team with the "
          "most points at the end of the year are the champions."),

    entry("var", (("var",), ("football", "soccer", "mean", "work", "video", "whats", "what")),
          "VAR is the video assistant referee: off-pitch officials watch replays and can tell the "
          "referee to review four things — a goal, a penalty, a straight red card, or a case of "
          " mistaken identity. The referee still makes the final call."),
    entry("keeping-kids-apart", (("chasing", "chase"), ("ball", "kids", "children", "all")),
          "Split the pitch into four small squares and put three or four children in each with "
          "one ball: everyone touches the ball, nobody can chase the whole crowd. Rotate the "
          "squares every five minutes so they meet each other, and finish with a game on a "
          "short, wide pitch so there is always someone to pass to."),
    entry("cricket-formats", (("cricket", "test match", "t20", "twenty20"), ("how long", "last",
                                                                            "days", "format",
                                                                            "formats", "how many",
                                                                            "many", "difference")),
          "A Test match is up to five days, 90 overs a day; a one-day match is 50 overs a side; a "
          "T20 is 20 overs a side and takes about three hours. Same game, very different patience "
          "required.",
          avoid=("whats an over", "what is an over", "whats a over", "an over",
                 "how many balls")),
    entry("cricket-over", (("over in cricket", "an over", "overs in an innings"),
                            ("balls", "six", "how many", "many", "mean", "means", "what", "is")),
          "An over is six balls bowled by one bowler from one end, then someone else bowls from "
          "the other end. In a limited-overs game a bowler can bowl at most a fifth of the overs "
          "- 10 in a 50-over match, 4 in a T20."),
    entry("cricket-lbw", (("lbw", "leg before wicket"), ("cricket", "mean", "rule", "out")),
          "Leg before wicket: the ball hit the batter's leg (or body) when it would have gone on "
          "to hit the stumps, and the bat wasn't involved first. The umpire has to think the ball "
          "was going on to hit, so a ball pitching outside leg, or a batter who hit it first, is "
          "not out."),
    entry("cricket-duck", (("duck",), ("cricket", "mean", "out", "score")),
          "A duck is a batter out for nought, and a golden duck is out first ball. It's just "
          "slang for zero on the scoreboard — the shape of the 0 looks like a duck's egg."),
    entry("cricket-wicket", (("wicket", "wickets"),
                             ("what", "whats", "mean", "means", "is", "how many", "three",
                              "stumps", "bails")),
          "A wicket is the set of three stumps and two bails a batter defends, and taking a "
          "wicket means getting a batter out - so ten wickets in an innings is all ten "
          "dismissals. The wicket-keeper stands behind it, with the slips beside them."),
    entry("cricket-no-ball", (("no ball", "no balls", "no-ball"),
                              ("cricket", "mean", "means", "what", "whats", "is", "why")),
          "A no ball is the bowler overstepping the popping crease, throwing instead of bowling, "
          "or sending down a full toss above waist height: the batting side gets a run and the "
          "ball is bowled again. In one-day and T20 cricket the next ball is a free hit, when a "
          "batter can only be run out."),

    entry("tennis-sets", (("tennis", "wimbledon", "grand slam"), ("how many sets", "sets", "best of",
                                                                "match")),
          "Women's matches at the Grand Slams are best of three sets and men's are best of five, "
          "except that most other tournaments are best of three for both. A set is first to six "
          "games, two clear.",
          bias=1),
    entry("tennis-grand-slam", (("grand slam", "grand slams"),
                                ("what", "whats", "is", "mean", "means", "four", "win", "won",
                                 "all four", "which")),
          "The Grand Slams are the four biggest tournaments: the Australian Open in January, the "
          "French Open at Roland-Garros on clay, Wimbledon on grass, and the US Open. Winning all "
          "four in the same year is a calendar Grand Slam - Rod Laver did it in 1969 and Steffi "
          "Graf in 1988.",
          bias=2,
          avoid=("sets", "best of", "how many sets", "deuce", "tie-break", "score", "scoring",
                 "golf", "majors", "masters", "rugby", "six nations", "triple crown")),
    entry("volleyball-basics", (("volleyball", "volley ball"),
                                ("players", "how many", "rules", "work", "score",
                                 "scoring", "team", "play", "side")),
          "Volleyball is six a side, and each team can touch the ball three times before sending "
          "it over - a block does not count as one of them. Every rally now scores a point, sets "
          "go to 25 and the deciding fifth set to 15, and you have to be two points clear."),
    entry("snooker-basics", (("snooker",), ("rules", "work", "how", "play", "147", "reds",
                                            "colours")),
          "Pot a red (1 point), then a colour (2 to 7), and put the colour back on its spot; carry "
          "on that way until the reds are gone, then take the colours in order. The maximum break "
          "is 147: fifteen reds with fifteen blacks, then all the colours."),

    entry("basketball-basics", (("basketball", "basketballs"), ("rules", "work", "how", "play",
                                                           "points", "quarters", "players")),
          "Basketball is five a side over four quarters, and you score 2 points in the basket, 3 "
          "from behind the arc, and 1 from the free-throw line. You have to keep dribbling or pass "
          "— picking the ball up and walking with it is a travel.",
          avoid=("how long", "long", "last", "minutes", "foul", "fouls", "fouled")),
    entry("basketball-length", (("basketball", "basketballs"),
                                ("how long", "long", "last", "minutes", "quarters",
                                 "periods", "how many quarters")),
          "Four quarters: 10 minutes each in international (FIBA) games, so 40 minutes of play, "
          "and 12 each in the NBA for 48. The clock stops on every whistle, so the whole game "
          "takes about two hours.",
          bias=1,
          avoid=("foul", "fouls", "fouled", "scoring", "points", "rules", "travel")),
    entry("basketball-foul", (("foul", "fouls", "fouled", "fouling"),
                              ("basketball", "mean", "means", "what", "whats", "is",
                               "how many", "before", "out", "personal")),
          "A foul is illegal contact - a push, a hold, or barging into a shooter - and the other "
          "side gets the ball, or free throws if it happened while shooting. Five fouls and you "
          "are out of the game (six in the NBA), and a team's fouls add up: once it reaches the "
          "limit in a quarter, every later foul gives the other side free throws."),
    entry("hockey-basics", (("hockey", "field hockey", "ice hockey"),
                            ("how long", "long", "players", "many", "offside", "rule", "rules",
                             "work", "basics", "minutes", "quarters", "periods", "team",
                             "game", "match")),
          "Field hockey is 11 a side over four 15-minute quarters, so 60 minutes of play, and it "
          "has no offside rule - that was dropped in 1999, though you can only score from inside "
          "the shooting circle and only with the flat side of the stick. Ice hockey is a different "
          "game: six on the ice including the goalie, three 20-minute periods, and there the blue "
          "line does make an offside.",
          bias=1,
          avoid=("f1", "formula")),
    entry("join-a-club", (("join", "joining", "club", "clubs", "start playing", "back to playing",
                           "taster session", "local club", "sport club"),
                          ("football", "netball", "hockey", "cricket", "rugby", "basketball",
                           "tennis", "swimming", "running", "badminton", "rounders", "league",
                           "adult", "beginner")),
          "Search for the sport plus your town and 'club', then email and ask about a taster "
          "session: most clubs have a beginners' or social night that costs a few pounds. Turn up "
          "to that rather than a match, and say you're new — clubs are used to it, and it's the "
          "fastest way to find people at your level.",
          avoid=("kit", "equipment", "what does", "what do i need", "what should she", "shoes",
                 "boots", "bring", "wear",
                 "too old", "am i too old"),
          bias=1),
    entry("swim-breathing", (("swimming", "swim", "front crawl", "crawl", "lengths"),
                             ("breathe", "breathing", "technique", "learn", "goggles")),
          "Breathe out slowly under the water and turn your head to the side to breathe in as one "
          "arm comes over, rather than lifting your head forwards. Practise with a float and "
          "breathe every three strokes to start; goggles make all of it easier."),
    entry("pool-kit", (("swimming", "pool"), ("take", "bring", "first time", "kit", "locker",
                                              "goggles")),
          "Take goggles, a towel, a swimming costume (not shorts for most pools), a padlock for the "
          "locker and £1 coins or a card for it. Most pools want a shower before you get in, and "
          "many have a fast lane and a slow lane — start in the slow one.",
          avoid=("kid", "kids", "child", "children", "toddler", "baby", "babies", "newborn",
                 "infant", "month old", "months old",
                 "learn to swim", "learn swimming", "swimming lessons", "swim lessons",
                 "how long does it take", "cant swim", "can't swim", "cannot swim")),
    entry("sport-kit", (("kit", "kits", "equipment", "gear", "shin pads", "boots", "trainers"),
                        ("start", "starting", "beginner", "first time", "playing", "netball",
                         "football", "hockey", "cricket", "rugby", "badminton", "rounders",
                         "sport", "son", "daughter", "child", "kid", "kids", "boy", "girl")),
          "Start with very little: trainers or astro boots, shorts or leggings, a water bottle and, "
          "for football or hockey, shin pads. Clubs lend sticks, bats and bibs to beginners, so "
          "email and ask what they provide before you buy anything.",
          avoid=("which boots", "what boots", "football boots", "studs", "studded", "moulded", "firm ground", "soft ground", "astro turf", "3g", "4g", "boot size", "what size", "break them in", "break in", "blister", "blisters", "too tight", "too small",
                 "astro boots", "turf boots", "boots for", "cheap boots", "boots cheap", "boots under", "new boots", "where to buy boots", "where can i get boots",
                 "smell", "smelly", "wash", "washing", "lost", "forgot", "leaving", "left"),
          bias=1),
    entry("protein-safety", (("protein", "high protein diet", "high protein"),
                             ("safe", "safety", "harmful", "dangerous", "bad for you", "too much",
                              "kidney", "kidneys", "bones", "heart", "side effects", "worry")),
          "For healthy kidneys, up to about two grams of protein a kilo a day is not a risk: no "
          "study has shown kidney damage in people with normal kidney function, and it does not "
          "harm your bones either. Extra protein beyond what your muscles use is simply burned, "
          "not stored as poison, and you do not need to force litres of water - drink to thirst. "
          "If you already have kidney disease, ask your doctor for a number before you raise it.",
          avoid=("baby", "babys", "toddler", "child", "children", "kid", "kids", "formula",
                 "breastfed", "breastfeeding", "pregnant",
                 "dog", "cat", "puppy", "kitten", "rabbit", "hamster", "horse")),
    entry("protein-child", (("protein", "protein powder", "protein shake"),
                            ("baby", "babies", "toddler", "toddlers", "child", "children", "kid",
                             "kids", "weaning", "6 months old", "one year old", "school age")),
          "A child needs about a gram of protein for each kilo they weigh, so around 20g a day at "
          "20kg - two small portions of meat, fish, beans or eggs. Babies under one get all they "
          "need from breast milk or formula, and from six months you add iron-rich foods twice a "
          "day: mashed lentils, egg, chicken, yoghurt. Fussy patches are normal; ask your health "
          "visitor if the weight chart worries you.",
          bias=2),
    entry("protein-shakes", (("protein", "whey", "protein powder", "protein shake",
                              "protein shakes"),
                             ("shake", "shakes", "powder", "whey", "worth it", "buy", "buying",
                              "necessary", "essential", "need it")),
          "Only if you struggle to hit the number with meals: a shake is convenient protein, not "
          "a shortcut, and food does the same job for less money. If you do buy one, a plain whey "
          "or a plant blend is fine - one scoop after training covers 20 to 25g - and the timing "
          "barely matters, because the total for the day is what builds muscle. Look for 20g or "
          "more of protein a scoop and ignore anything promising to burn fat.",
          avoid=("safe", "safety", "harmful", "dangerous", "kidney", "kidneys", "too much",
                 "for dogs", "dog", "cat", "puppy", "kitten", "allergic", "allergy", "sick",
                 "made me ill", "stomach", "nausea",
                 "baby", "babys", "toddler", "child", "children", "kid", "kids")),
    entry("warm-up-match", (("warm up", "warm-up"), ("before", "match", "game", "playing",
                                                     "football", "sport")),
          "Ten minutes is plenty: a jog to get warm, then leg swings, side-steps, lunges and a few "
          "short sprints, and finish with the ball or the equipment so the last thing you do looks "
          "like the game. Save the long stretches for afterwards.",
          bias=1),

    entry("boxing-rounds", (("boxing", "boxer", "bout"),
                            ("rounds", "how many", "long", "rules", "score", "scoring", "win")),
          "A professional championship fight is twelve rounds of three minutes with a minute "
          "between, and most ordinary fights are four, six, eight or ten. Amateur bouts are "
          "usually three rounds of three. You win on points from the judges if it goes the "
          "distance, or by knockout, and a boxer who cannot continue loses.",
          avoid=("train", "training", "exercise", "gym", "get fit", "lose weight", "start boxing",
                 "beginner", "how do i start", "class", "classes", "lesson", "lessons")),
    entry("american-football-rules", (("american football", "nfl", "super bowl"),
                                      ("work", "works", "rules", "score", "scoring", "down",
                                       "downs", "how does", "how do you play", "explain")),
          "The team with the ball gets four attempts to move ten yards, and if they make it they "
          "get four more; that is the whole rhythm of the game. A touchdown is six points, the "
          "extra kick one more, a field goal three. If the four attempts run out, the other team "
          "takes over from where the ball is."),
    entry("american-football-scoring", (("field goal", "field goals", "touchdown", "touchdowns",
                                        "extra point", "two point conversion", "safety"),
                                       ("how many", "many", "points", "point", "score",
                                        "scoring", "worth", "what", "is")),
          "A touchdown is six points, the extra point kick after it is one more, a field goal is "
          "three, and a safety - tackled behind your own goal line - is two. That is the whole "
          "scoring system in American football."),

    entry("tour-de-france", (("tour de france", "cycling race", "yellow jersey", "grand tour"),
                             ("work", "works", "win", "wins", "winner", "stages", "explain",
                              "how", "what", "mean", "means")),
          "It is about three weeks and 21 stages, and the winner is whoever finishes with the "
          "lowest total time — not the most stage wins. The yellow jersey goes to the overall "
          "leader each day, green is the points competition for sprinters, and the polka dot is "
          "for the best climber. Most of the overall lead is built in the mountain stages and the "
          "two time trials."),
    entry("which-team-to-support", (("who should", "who to support", "which team", "which club",
                                     "which side", "football team", "pick a team", "pick a club",
                                     "support a club", "support a team", "what team"),
                                    ("team", "football", "premier league", "rugby", "cricket",
                                     "sport", "league", "support")),
          "Pick the team someone you already watch with supports, or the one nearest to where you "
          "live — going to games matters more than the badge. Watch a few matches first and let it "
          "happen; supporting a team is mostly habit plus the people you watch it with. Nobody "
          "will test you on the history, whatever the internet says.",
          avoid=("won", "win", "wins", "score", "result", "table", "top of", "players", "best",
                 "points", "how many", "what is", "cup", "final", "better", "stronger", "versus",
                 "vs", "beat", "bet", "watch"),
          guard=_not_the_coach_of_a_team),

    entry("gym-first-session", (("gym", "weight room", "weights", "free weights"),
                                ("first", "first time", "start", "starting", "beginner",
                                 "never", "joined", "what should i do", "what do i do",
                                 "how do i start", "do first",
                                 "what should i try", "what do i try", "what to do",
                                 "know what to do", "no idea", "dont know", "don't know",
                                 "where do i start", "where to start", "how do i use",
                                 "use the machines", "machines", "induction",
                                 "what should i be doing", "tips", "advice")),
          _the_gym_induction,
          avoid=("cancel", "cancelling", "cancel my", "membership", "contract", "refund",
                 "quit", "leaving", "close my",
                 "sore", "soreness", "aching", "ache", "push through", "been going",
                 "started at the gym", "started going"),
          ask=("what", "how", "should", "when", "first", "start", "do i", "tips", "advice")),

    entry("choosing-a-gym", (("gym", "leisure centre", "health club", "swimming pool"),
                             ("choose", "choosing", "pick", "picking", "which gym", "best gym",
                              "good gym", "worth joining", "compare", "look for", "near me",
                              "cheap", "cheapest", "price", "prices", "join", "joining")),
          "Go at the time you would actually go, on a weekday evening if that is when you are free: "
          "a gym that is full at six is the one you stop using. Then check three things - the "
          "distance from home or work, because anything past fifteen minutes gets skipped, whether "
          "the classes you want are included in the price or cost extra, and the notice period on "
          "the contract, which is often a month and sometimes three. Ask for a day pass or a week "
          "trial before you sign, look at the changing rooms as well as the equipment, and work out "
          "the price per visit rather than per month: 40 a month is cheap at three visits a week "
          "and dear at one. The cheapest gym is the one you actually use.",
          avoid=("cancel", "cancelling", "refund", "quit", "leaving", "close my", "sore",
                 "first time", "first day", "beginner", "warm up", "what should i do",
                 "how do i start", "induction", "key fob"),
          ask=("choose", "choosing", "pick", "picking", "which", "best", "worth", "compare",
               "look for", "near me", "cheap", "price", "cost", "join", "how"),
          bias=1),

    entry("strength-after-illness", (("strength", "strong again", "muscle", "muscles", "energy",
                                      "weak", "weakness", "fitness", "stamina", "weight"),
                                     ("after illness", "after being ill", "after surgery",
                                      "after a operation", "after an operation", "after covid",
                                      "after chemo", "after hospital", "been ill", "was ill",
                                      "build up", "build back", "get back", "back to normal",
                                      "rebuild", "regain", "lost",
                                      "illness", "ill", "surgery", "operation", "chemo",
                                      "hospital", "bed", "virus", "covid", "infection")),
          "Start with two short sessions a week and leave a day between them: a chair stand or a "
          "slow sit-to-stand for the legs, a wall press or a light band row for the upper body, "
          "eight to ten slow reps each, stopping while you still have three or four left in you. "
          "Add a little - one rep or one tin of beans - only when the last session left you tired "
          "but not wrecked. Muscle comes back at roughly half the speed of the walking, so expect "
          "weeks rather than days, and put protein in every meal: a palm-sized piece of meat, "
          "fish, eggs, beans or yoghurt, three times a day. If you were in hospital, in bed for "
          "more than a few days, or had heart, lung or kidney trouble, ask your GP or the "
          "physiotherapist who saw you before you start, and stop and get advice for chest pain, "
          "breathlessness at rest, or a swollen painful calf.",
          avoid=("warm up", "programme", "program", "plan for", "marathon", "half marathon", "5k",
                 "10k", "bulk", "bulking", "cutting", "bodybuilder", "personal best", "gym",
                 "first time", "beginner", "protein powder", "creatine", "how much weight"),
          ask=("how", "what", "should", "when", "build", "get back", "start", "help", "tips")),

    entry("gym-warm-up", (("warm up", "warmup", "warm-up"),
                          ("long", "how long", "gym", "weights", "run", "running", "exercise",
                           "before", "should i")),
          "Five to ten minutes: two or three minutes on the bike, rower or cross-trainer until you "
          "are warm, then a couple of light sets of whatever you are about to do - the same "
          "movement at half the weight, for 10 reps. That is a warm-up; the long stretches are for "
          "afterwards, when the muscles are warm.",
          avoid=("match", "game", "playing", "football", "rugby", "netball", "hockey", "sport")
          + A_HOUSE_WARMING_UP),

    entry("cardio-or-weights-first", (("cardio", "run", "running", "bike", "rowing"),
                                      ("first", "before", "after", "order", "should i do",
                                       "which", "same session", "same day", "lift weights",
                                       "weights first", "cardio or weights",
                                       "weights or cardio")),
          "Do the one that is the point of the session first, because the second one gets the "
          "tired version of you: if you are there to get stronger, lift first and finish with ten "
          "minutes of cardio; if you are training for a run or a ride, do that first. Ten easy "
          "minutes on the bike before you lift is a warm-up, not cardio. The best order is the one "
          "you will keep doing twice a week.",
          ask=("weights", "weight training", "lifting", "lift", "strength", "resistance",
               "circuits", "first", "before", "after", "order", "same session", "same day"),
          bias=1,
          avoid=("run out of", "ran out of", "running out of", "runs out",
                 "money", "payday", "pay day", "paid", "wage", "wages", "salary", "rent",
                 "bill", "bills", "cash", "pounds",
                 "rest day", "rest days", "day off", "days off", "recovery day", "recovery days",
                 "breakfast", "fasted", "fasting", "eat", "eats", "eating", "ate", "food",
                 "foods", "meal", "meals", "fuel", "carbs", "carb", "protein", "pre workout",
                 "pre-workout", "stretch", "stretches", "stretching", "warm up", "warmup",
                 "warm-up", "cool down", "cooldown", "water", "hydrate", "hydration",
                 "hurt", "hurts", "hurting", "pain", "painful", "ache", "aches", "aching",
                 "sore", "soreness", "stiff", "twinge", "sciatica")),

    entry("run-every-day", (("run", "running", "jog", "jogging"),
                            ("every day", "everyday", "daily", "every single day")),
          "You can run every day eventually, but for the first couple of months three or four runs "
          "a week is the better deal - the legs get stronger on the days off, and running every day "
          "from nothing is how shins start hurting. Keep most runs easy enough to hold a "
          "conversation in; a hard run every day is the other common mistake. Add one run a week "
          "rather than one every day.",
          avoid=("marathon", "race", "parkrun", "how far", "distance",
                 "cold", "flu", "fever", "hangover", "ill", "sick", "cough",
                 "injury", "injured", "dog", "dogs", "knee", "knees", "hurt", "hurts",
                 "pain", "hurting",
                 "school run", "school runs", "nursery run", "errand run", "errand runs",
                 "supermarket run", "shop run")),

    entry("eat-before-run", (("eat", "eating", "food", "breakfast", "snack"),
                             ("before a run", "before i run", "before running", "before the gym",
                              "before i go", "before exercise", "before a workout", "running",
                              "workout", "gym",
                              "before a match", "before the match", "before a game",
                              "before the game", "before playing", "before i play",
                              "before i train", "before training", "before sport",
                              "before five a side", "five a side", "football", "rugby",
                              "netball", "hockey", "cricket", "a match", "the match")),
          "Something small and mostly carbohydrate, an hour or two before: a banana, a round of "
          "toast, a small bowl of porridge. Leave longer after a big meal - three hours - or you "
          "will feel it. For a short easy run first thing, plenty of people go out with nothing but "
          "water and are fine. The one rule is nothing new on the day of a race: try it in training "
          "first.",
          avoid=("after a run", "after the run", "after running", "after the gym", "afterwards",
                 "recover", "recovery", "after a workout", "after exercise", "post workout",
                 "post-workout", "after my run", "after i run"),
          bias=1),
    entry("league-and-cup",
          (("league", "cup", "the cup", "premier league", "champions league", "fa cup",
            "knockout", "table"),
           ("difference", "what", "why", "how does", "explain", "both", "same", "cup and league",
            "works", "between")),
          _league_and_cup,
          avoid=("my team", "we lost", "we won", "score", "kick off", "kick-off", "ticket",
                 "who won", "result",
                 "restaurant", "restaurant table", "booking", "book", "booked", "reservation",
                 "reservations", "cancel", "cancelling", "cancellation", "notice", "dinner",
                 "lunch", "dining", "table for", "pub")),

    entry("knee-gives-way", (("knee", "knees", "kneecap"),
                             ("gave way", "gives way", "gave out", "gives out", "buckled",
                              "buckles", "collapsed", "collapses", "unstable", "wobbles",
                              "not stable", "keeps giving")),
          "A knee that gives way is one to get looked at rather than train through: it usually "
          "means a ligament is not holding, or the kneecap is slipping, and a physio can work out "
          "which in one visit. Skip pivoting sports and uneven ground until then, and keep the "
          "muscles awake with sit-to-stands and step-ups. Ring your GP or a physio this week.",
          bias=2),
    entry("exercise-when-ill", (("gym", "run", "running", "jog", "exercise", "exercising",
                                 "workout", "work out", "working out", "training", "train",
                                 "football", "swim", "swimming", "cycle", "cycling", "lift",
                                 "lifting", "weights",
                                 "still run", "still train", "still go", "still play",
                                 "still swim", "still cycle"),
                                ("cold", "colds", "ill", "illness", "sick", "flu", "chest",
                                 "cough", "sore throat", "temperature", "fever", "virus", "bug",
                                 "tonsils")),
          "Use the neck rule: a runny nose, sneezing or a mild sore throat above the neck is fine "
          "for easy exercise; a chesty cough, fever, aching or a stomach bug below it means rest "
          "until you are properly over it. Come back at half your usual effort for the first "
          "session, and do not count a hard session as something that clears it.",
          avoid=("get rid", "remedy", "cure", "fast", "quickly", "best", "what helps", "chest pain",
                 "cant breathe", "can't breathe", "baby", "babies", "child", "children",
                 "kid", "kids",
                 "hands", "hand", "fingers", "feet", "foot", "toes", "toe"),
          bias=3),

    entry("run-in-the-cold", (("cold", "freezing", "winter", "frost", "minus", "icy"),
                              ("run", "running", "jog", "jogging", "cycle", "cycling", "bike",
                               "bicycle", "ride", "riding", "exercise", "exercising")),
          "Cold air does not damage healthy lungs: it is dry and it warms on the way in, so a run "
          "or a ride in the cold is fine. Start slower for the first ten minutes, cover your "
          "hands and ears, and wear a layer you can tie round your waist. If you have asthma, "
          "take your inhaler before you go out and warm up indoors first, and use a buff over "
          "your mouth on very cold days.",
          avoid=("wear", "wearing", "what to wear", "kit", "clothes", "outfit",
                 "a cold", "my cold", "with a cold", "have a cold", "run down",
                 "get a cold", "catch a cold", "cold sore",
                 "chest", "chest pain", "chest hurts", "cant breathe", "can't breathe",
                 "asthma attack",
                 "cough", "coughing", "chesty", "sore throat", "fever", "ill", "sick",
                 "hands", "hand", "fingers", "feet", "foot", "toes", "toe",
                 "pump", "pumps", "filter", "filters", "engine", "engines", "motor",
                 "generator", "machine", "air con", "aircon", "car", "cars", "van")
                 + A_WEATHER_ASK,
          bias=1),

    entry("treadmill-run",
          (("treadmill", "treadmills", "running machine", "run indoors", "running indoors"),
           ("bad", "worse", "ok", "okay", "good", "healthy", "outside", "vs", "versus",
            "better", "knees", "harder", "easier", "instead of", "worth it", "safe")),
          "A treadmill is not bad for you: the deck gives a little more than pavement does, and "
          "the machine keeps the pace honest. It is a touch easier than running outside because "
          "there is no wind or camber, so set the incline to 1% to make it match the road, and "
          "run tall rather than holding the handles. The one habit to avoid is the same flat "
          "stride every time - put a hill or a faster minute in most sessions.",
          avoid=("buy", "buying", "bought", "price", "prices", "cost", "cheapest", "which one",
                 "second hand", "second-hand", "fix", "repair", "broken", "motor", "belt",
                 "squeak", "squeaking", "noise", "noisy", "lubricant"),
          bias=1),
    entry("run-in-the-heat", (("hot", "heat", "heatwave", "warm", "boiling", "scorching",
                               "humid", "muggy", "sun", "sunny", "degrees", "30c", "25c"),
                              ("run", "running", "jog", "jogging", "cycle", "cycling", "ride",
                               "walk", "exercise", "exercising", "football", "tennis",
                               "safe")),
          "Above about 25C, slow down rather than stop: expect 20 to 30 seconds a kilometre "
          "slower for every 5C over 15C, and let the pace go. Run early or late, drink to thirst "
          "before and after, take walk breaks, and wear light, loose clothes. Stop and get into "
          "shade if you go dizzy, get a headache, feel sick or stop sweating. The first hot week "
          "is the worst one, and the body adapts in about ten days.",
          avoid=("baby", "babies", "pram", "buggy", "dog", "dogs", "car", "cars", "van",
                 "house", "flat", "bedroom", "room", "sleep", "sleeping", "radiator",
                 "heating", "boiler", "sunburn", "sun cream", "sunscreen", "spf", "uv",
                 "weather", "forecast", "washing", "laundry",
                 "oven", "ovens", "fan oven", "cooker", "hob", "grill", "bake", "baking",
                 "roast", "roasting", "gas mark", "air fryer", "barbecue", "bbq", "kiln",
                 "fever", "temperature of", "hot flush", "flushes", "menopause", "period",
                 "hot water bottle"),
          bias=1),
    entry("run-in-the-rain", (("run", "running", "jog", "jogging", "cycle", "cycling",
                               "walk", "walking", "train", "training"),
                              ("rain", "raining", "rains", "wet", "drizzle", "drizzling",
                               "downpour", "showers", "shower", "bad weather", "weather",
                               "stormy", "storm", "thunder", "lightning", "miserable")),
          "Yes, and it is usually fine: you get wet either way once you are out, and the rain "
          "cools you rather than hurting you. Wear a thin breathable jacket or a cap with a brim "
          "so the rain stays out of your eyes, something bright or reflective because drivers "
          "see less in the wet, and trainers with grip - wet leaves and painted lines are slick. "
          "Rub a little vaseline where your clothes rub, because wet skin chafes. The one thing "
          "to stop for is thunder and lightning: head indoors and wait it out. Stuff newspaper "
          "in the shoes afterwards and dry them away from a radiator so they keep their shape.",
          avoid=("phone", "iphone", "waterproof", "leak", "leaking", "roof", "gutter",
                 "washing", "laundry", "dry the washing", "put the washing out",
                 "umbrella", "coat", "bbq", "barbecue", "picnic", "wedding", "drive",
                 "drive in", "forecast", "will it rain", "is it going to rain",
                 "horrible", "awful", "hate", "dread", "cant stand", "can't stand",
                 "cold", "flu", "ill", "illness", "sick", "cough", "coughing", "chesty",
                 "fever", "sore throat", "virus", "bug", "chest infection")),

    entry("exercise-on-period", (("exercise", "exercising", "gym", "run", "running", "jog",
                                  "swim", "swimming", "workout", "work out", "working out",
                                  "train", "training", "lift", "lifting", "weights", "cycle",
                                  "cycling", "yoga", "pilates", "netball", "football", "hockey",
                                  "still go", "still run", "still train", "rest", "skip",
                                  "keep going", "stretch", "dance", "class", "spin"),
                                 ("period", "periods", "on my period", "time of the month",
                                  "menstrual", "monthlies", "day one", "day 1",
                                  "first day of my period", "first day of the period",
                                  "first day of it", "first day on my period")),
          "Yes - easy to moderate exercise is fine on your period, and it usually helps: moving "
          "lifts the endorphins and blood flow that take the edge off cramps. Go by how you feel "
          "rather than by the calendar: a walk, a swim or an easy run is fine on a heavy day, and "
          "if day one is rough keep it short and gentle and pick it up later in the week. "
          "Ibuprofen about half an hour before helps if cramps are the problem. For swimming, use "
          "whatever you already use - a tampon or a cup - and change it straight after.",
          avoid=("pain", "painful", "painkillers", "heavy", "heavier", "flooding", "bleeding",
                 "bleed", "missed", "late", "stopped", "irregular", "pregnant", "pregnancy",
                 "test", "contraception", "pill", "implant", "coil", "menopause",
                 "why", "what causes", "normal", "should my period",
                 "horrible", "awful", "hate", "dread", "cant stand", "can't stand"),
          bias=1),
    entry("tennis-serve", (("serve", "serving", "toss", "second serve"),
                           ("tennis", "improve", "better", "practise", "practice", "consistent",
                            "power", "fix", "long", "net", "fault", "faults", "double fault",
                            "inconsistent", "inconsistency", "keeps", "goes long",
                            "double", "faults")),
          "Two things fix most serves: a toss you can repeat and meeting the ball out in front. "
          "Practise 50 tosses without hitting, catching at the same spot each time, then serve at "
          "half speed from the service line and only move back when 8 of 10 land in. Toss first, "
          "power later - the pace comes from the leg bend and the shoulder turn, not from swinging "
          "harder.",
          avoid=("volleyball", "badminton", "squash", "table tennis", "tennis elbow",
                 "dinner", "food", "guests", "wine", "coffee", "drinks", "pint",
                 "dns", "wifi", "fault with", "my fault", "at fault")),
    entry("football-boots", (("boot", "boots", "football boots", "studs", "studded", "moulded",
                              "cleats", "astro boots", "astro turf", "turf boots", "firm ground",
                              "soft ground", "sg boots", "fg boots", "predators"),
                             ("grass", "astro", "astroturf", "3g", "4g", "turf", "indoor",
                              "moulded studs", "studded studs",
                              "futsal", "sports hall", "muddy", "wet", "surface", "which",
                              "what", "son", "daughter", "child", "kid", "need", "get", "wear",
                              "buy", "size", "first pair", "shin pads", "break in",
                              "breaking in", "break them in", "blister", "blisters", "too tight",
                              "cheap", "cheaper", "cheapest", "afford", "budget", "price",
                              "prices", "cost", "spend", "sale", "second hand", "secondhand",
                              "where", "shop", "shops", "store", "online", "order", "pair",
                              "pairs", "years old", "year old", "age", "foot", "feet",
                              "when", "what month", "which month", "best time", "time to buy")),
          _football_boots,
          guard=_not_a_study_line,
          avoid=("hiking", "walking", "walk", "wellies", "wellington", "welly", "snow boots",
                 "ski", "skis", "skiing", "ski boots", "ski boot", "snowboard", "snowboarding",
                 "piste", "slope", "slopes", "mountain", "chalet", "apres", "apres ski",
                 "winter", "winter boots", "snow", "ice", "icy", "grit", "slush", "frost",
                 "riding boots", "horse", "car boot", "boot sale", "boots the chemist", "job",
                 "boot of my car", "boot of the car", "boot of a car", "boot of our car",
                 "in the boot", "the boot of", "boot space",
                 "jobs", "work boots", "steel toe", "dr martens", "timberland", "ankle boot",
                 "boot cut", "bootcut",
                 "stain", "stains", "stained", "mark", "marks", "scuff", "scuffs", "smell",
                 "smells", "smelly", "wax", "polish", "dubbin", "waterproof", "clean",
                 "cleaning", "washing", "wash",
                 "ceiling", "ceilings", "wall", "walls", "wallpaper", "bathroom", "shower",
                 "damp", "damp patch", "condensation", "mildew", "black mould", "black mold",
                 "spore", "spores", "grout", "sealant", "bedroom", "bedrooms", "room", "rooms",
                 "window", "windows", "sill", "corner", "corners", "kitchen", "floor", "floors",
                 "flat", "house", "curtain", "curtains", "cupboard", "wardrobe", "tile", "tiles",
                 "skirting", "loft", "attic", "airing cupboard", "windowsill",
                 "bread", "loaf", "loaves", "toast", "sandwich", "cake", "cheese", "jam",
                 "yoghurt", "yogurt", "fruit", "vegetable", "vegetables", "food", "foods",
                 "leftovers", "leftover", "eat", "eating", "ate", "edible", "safe to eat",
                 "throw away", "throw it away", "bin it", "loaf of", "slice of")),


    entry("swim-in-the-sea", (("swim", "swimming", "swimmer", "paddle", "paddling", "dip",
                               "wild swim", "bathe"),
                              ("sea", "beach", "lido", "lake", "river", "reservoir", "cove",
                               "open water", "outdoors", "outside", "tarn", "loch")),
          "Yes, with a few things done right. Pick a lifeguarded beach and swim between the flags, "
          "go with someone rather than alone, and check the tide and the wind before you get in. "
          "The cold is the real danger at a British beach: it takes your breath away in the first "
          "few seconds, so walk in, let yourself gasp, and only then swim - and get out well before "
          "you start shivering. If a current pulls you sideways, do not fight it: swim parallel to "
          "the beach until you are out of it, then come in. No alcohol before you go in, and a "
          "wetsuit or a tow float on a cold day.",
          avoid=("pool", "chlorine", "learn to swim", "lessons", "front crawl", "breaststroke",
                 "stroke", "goggles", "after eating", "cramp", "ear", "earache", "shoulder",
                 "how long", "how far", "calories", "burn"),
          bias=1),

    entry("swim-after-eating",
          (("swimming", "swim", "pool", "sea", "bathe", "lido"),
           ("after eating", "after a meal", "after lunch", "after dinner", "wait", "waiting",
            "how long after", "how long before", "how long do i have to wait",
            "how long should i wait", "how long till i can swim after",
            "before swimming", "cramp", "cramps", "straight after")),
          "There is no need to wait a full hour: the old cramp rule comes from one small study and "
          "the evidence does not back it up. Go in when you feel comfortable, which for most people "
          "is half an hour after a big meal and straight away after a snack - just keep off alcohol "
          "before you get in, because that one really does matter.",
          avoid=("cook", "recipe", "meal plan", "kids", "children", "toddler", "baby", "dog")),

    entry("football-improve",
          (("football", "soccer", "five-a-side", "five a side"),
           ("better", "improve", "improvement", "practise", "practice", "training", "train",
            "coach", "skill", "skills", "touch", "passing", "drills")),
          "The two things that lift a park player fastest are a first touch that keeps the ball "
          "close and being able to pass with both feet: twenty minutes of wall passes a few times "
          "a week does both. Then add scanning - a look over your shoulder before the ball arrives "
          "- so you know your next pass before it reaches you.",
          avoid=("offside", "how long", "minutes", "rules", "positions", "join", "club",
                 "television", "tv", "world cup", "who won", "score", "watch", "injury", "injured",
                 "knee", "ankle", "hamstring")),
    entry("kick-a-football",
          (("kick", "kicks", "kicking", "kick it", "strike", "striking", "shoot", "shooting",
            "curl", "curled", "chip", "volley"),
           ("football", "soccer", "ball", "goal", "goals", "laces", "harder", "further",
            "properly", "power", "spin", "top corner", "free kick", "penalty", "corner",
            "long ball", "cross", "shot", "shots")),
          "Strike it with the laces, not the toe: plant the standing foot beside the ball with "
          "the knee over it, keep the ankle locked and swing through the middle of the ball, "
          "then follow through where you want it to go. For a pass, use the inside of the foot "
          "with the ankle at a right angle - the toe is what makes it balloon.",
          ask=("how", "what", "where", "should", "any"),
          avoid=("habit", "kick off", "kick-off", "kickoff", "kickboxing", "kicked out",
                 "rules", "offside", "how long", "who won", "watch", "tickets",
                 "rugby", "basketball", "american football", "gaelic", "penalty shootout"),
          bias=1),

    entry("fishing-licence",
          (("fish", "fishing", "angling", "angler", "coarse fishing", "fly fishing", "carp",
            "trout", "rod", "pike", "tench", "bream", "magot", "maggots"),
           ("licence", "license", "licencing", "licensing", "permit", "day ticket", "ticket",
            "legal", "illegal", "allowed", "need", "need one", "do i need", "rule", "rules",
            "close season", "closed season", "fishing season", "what is the close season",
            "when is the close season", "what is the fishing season", "when is the fishing season",
            "season starts", "season opens", "open season",
            "when can i", "get started", "start",
            "get into", "getting into", "beginner", "beginners", "equipment", "kit",
            "where do i", "what do i need", "can i", "am i allowed", "is it allowed")),
          ("In England and Wales you need a rod licence from the Environment Agency for any "
           "freshwater fishing, even for a day, and it is separate from the permission to fish: "
           "the lake or club sells a day ticket on top. Buy it online or at a Post Office - about "
           "£7 for a day, £13 for eight days, £35 for a season, per rod, and under-13s free. "
           "Scotland needs none for coarse or trout, but salmon does. Fishing without one is a "
           "fine."),
          bias=2,
          avoid=("cook", "cooking", "bake", "baked", "fry", "fried", "oven", "recipe", "eat",
                 "eating", "salmon fillet", "fish pie", "fishcakes", "how long to cook",
                 "sea", "beach", "boat", "harbour", "mackerel", "crab", "prawn", "smell",
                 "smells", "smelly", "polluted", "swim", "swimming", "pet", "tank",
                 "freeze", "freezer", "freezing", "frozen", "refreeze", "defrost", "thaw",
                 "thawed", "fridge", "leftovers",
                 "give my cat", "give my dog", "give the cat", "give the dog", "feed my cat",
                 "feed my dog", "feed the cat", "feed the dog", "give my kitten", "give my puppy",
                 "feed fish", "feeds fish", "feeding fish", "fed fish", "a fish fed",
                 "feed a fish", "feed the fish", "feed my fish", "feeding the fish",
                 "fish food", "goldfish", "aquarium", "tropical fish", "fish tank",
                 "can my cat eat", "can my dog eat", "can cats eat", "can dogs eat",
                 "my cat eat", "my dog eat", "can i give my", "is fish safe for",
                 "safe for cats", "safe for dogs", "safe for my cat", "safe for my dog",
                 "shelf life", "gone off", "still good", "use by", "sell by", "cooked", "raw",
                 "leftover fillet",
                 "oxygen", "breathe", "breathes", "breathing", "gills", "underwater",
                 "under water", "why do fish", "do fish need air", "need air",
                 "have with", "have it with", "eat with", "goes with", "go with", "serve with",
                 "serving with", "pairs with", "alongside", "on the side", "as a side",
                 "side dish", "same with",
                 "make with", "make from", "make out of", "do with", "use up", "using up",
                 "cook with", "cooking with", "recipe for", "a recipe", "smoked fish",
                 "smoked haddock", "smoked mackerel", "smoked trout", "kipper", "kippers",
                 ) + PRESENT_ASK),
    _RACE_COMPARED_CARD,
    _A_SHORTER_RACE_CARD,
]

ENTRIES += [
    entry("cycle-duration",
          (("cycle", "cycles", "cycling", "bike", "bikes", "bicycling", "ride", "riding"),
           ("how long", "how far", "how many minutes", "how many miles", "how many km",
            "how much time", "duration", "distance")),
          "Thirty to sixty minutes at a pace where you can still talk is the everyday ride worth "
          "doing - roughly 10 to 20km - and three or four of those a week beats one long ride at "
          "the weekend. Add ten minutes to a ride a week rather than jumping to a long one, and "
          "take an easy day after a hard ride.",
          ask=("how long", "how far", "how many minutes", "how many miles", "how many km",
               "how much time", "duration", "distance"),
          avoid=("buy", "buying", "worth", "cost", "price", "cheap", "puncture", "chain",
                 "saddle", "gears", "helmet", "e-bike", "ebike", "electric", "good for me",
                 "worth it", "benefits", "how often",
                 "washing machine", "washer", "wash cycle", "spin cycle", "dishwasher",
                 "tumble dryer", "dryer")),
    entry("swim-mile",
          (("swim", "swimming", "swimmer", "front crawl", "breaststroke", "lengths", "laps",
            "pool"),
           ("how long", "how many lengths", "how many laps", "how far", "a mile", "mile",
            "how many minutes")),
          "A mile is 1,600m, so 64 lengths of a 25m pool or 32 of a 50m one. A steady front-crawl "
          "swimmer takes about 30 to 40 minutes, and breaststroke or a first season 45 to 60. "
          "Build up 200m at a time - four lengths more each swim - rather than trying the mile on "
          "your first session.",
          ask=("how long", "how many lengths", "how many laps", "how far", "a mile", "mile",
               "how many minutes"),
          bias=2,
          avoid=("learn", "lessons", "cant", "can't", "cannot", "scared", "frightened", "afraid",
                 "cost", "price", "open water", "sea", "triathlon", "goggles", "cap", "near me",
                 "eat", "eats", "eating", "ate", "cramp", "cramps", "stomach", "meal", "food",
                 "should i swim", "swim a length", "beginner", "beginners", "starting out",
                 "how do i start", "get into swimming", "start swimming", "swim again",
                 "baby", "babies", "newborn", "infant", "toddler", "month old", "months old")),
    entry("run-to-lose-weight",
          (("run", "running", "jog", "jogging", "cardio"),
           ("lose weight", "losing weight", "weight loss", "fat")),
          "The weekly total does more than any single run: build to 150 to 250 minutes a week of "
          "easy running, which is four or five half hours. A half hour of steady running burns "
          "roughly 300 calories, so the food you do not eat matters more than the extra mile - "
          "run somewhere you can still hold a conversation and keep it up rather than going hard "
          "twice and stopping.",
          ask=("lose", "losing", "weight", "fat", "how long", "how much", "how far",
               "how many", "should i", "best"),
          bias=1,
          avoid=("every day", "everyday", "daily", "how often", "days a week", "times a week")),
    entry("couch-to-5k", (("couch to 5k", "c25k", "couch to five k"),
                          ("plan", "work", "works", "how", "start", "weeks", "long", "app",
                           "explain", "what is", "does it", "5k")),
          "Couch to 5k is nine weeks of three runs a week, starting with 60 seconds of jogging "
          "alternating with 90 seconds of walking. Each week the jogging gets longer and the "
          "walking shorter, and by week nine you run 30 minutes without stopping. The free NHS "
          "podcast tells you exactly when to run and when to walk, which is the bit that makes it "
          "work for people who have never run."),
    entry("five-a-side-kit", (("five a side", "5 a side", "5aside", "five aside",
                               "seven a side", "small sided"),
                              ("wear", "kit", "shin pads", "bring", "need",
                               "astro", "indoor", "outdoor")),
          "Astro trainers or moulded boots, shin pads, shorts and a top you do not mind sweating "
          "in, plus water. Most places play on 3G astro, so no studs, and a lot of leagues ask for "
          "the same colour top for the whole team - ask the organiser before you buy anything. A "
          "size 4 ball is the usual one for five a side, and someone always brings one.",
          avoid=("wash", "washing", "smell", "smelly", "lost", "forgot", "left",
                 "improve", "get better", "better at", "skills", "training", "practise",
                 "practice", "tactics",
                 "boot", "boots", "studs", "moulded", "screw-in", "firm ground", "soft ground",
                 "astro trainers", "which boots", "what boots"),
          bias=1),
    entry("detraining", (("lose fitness", "lost fitness", "fitness loss", "detrain", "out of shape",
                          "lose my fitness", "how quickly do i lose"),
                         ("weeks", "couple", "two weeks", "time off", "break", "stop", "stopped",
                          "injury", "injured", "ill", "holiday", "true", "how long")),
          "You lose very little in a week or two: the fitness you built comes back quickly and "
          "rest can even leave you fresher. Real losses start after about two to four weeks off, "
          "and even then most of it returns within a few weeks of training again. What drops first "
          "is the top end - sprint speed and the pace you can hold hard - not your easy running. "
          "Come back at about 70% of where you left off for a week, then build."),
    entry("start-boxing", (("boxing", "boxer", "boxercise", "muay thai", "kickboxing"),
                          ("start", "starting", "begin", "beginner", "first", "learn", "get into",
                           "classes", "class", "join", "club", "gym", "how do i", "how to")),
          "Find a club that teaches technique rather than a fitness boxercise class - most amateur "
          "clubs run beginners' sessions and lend gloves and wraps for the first few. Go twice a "
          "week, expect the first month to be footwork, stance and the basic four punches on your "
          "own, and tell the coach you have not boxed before so nobody puts you in to spar. Boots, "
          "wraps and your own gloves are the only kit worth buying early.",
          avoid=("rounds", "how many rounds", "judges", "knockout", "knock out", "points",
                 "out of breath", "breathless", "short of breath", "knackered", "dizzy",
                 "felt sick", "feel sick", "sore", "aching", "hurt", "injury", "injured",
                 "i was", "i felt",
                 "heavy box", "heavy boxes", "cardboard box", "cardboard boxes", "a box of",
                 "packing boxes", "moving boxes", "stack of boxes", "lifting a",
                 "lift a", "moving house", "parcel", "parcels", "suitcase", "sofa", "wardrobe"),
          guard=_not_a_line_about_a_box),
    
    entry("sports-results", (("who won", "team won", "the score", "final score", "the result",
                              "the results", "who is winning", "who's winning",
                              "league table"),
                             ("match", "game", "play", "played", "playing", "won", "score",
                              "result", "results", "table", "last night", "yesterday", "tonight",
                              "weekend", "cup", "final", "league")),
          _cant_see_the_score,
          ask=("match", "game", "games", "play", "played", "playing", "football", "rugby", "cricket",
               "tennis", "sport", "sports", "team", "teams", "league", "cup", "final", "score",
               "nil", "half", "kick off", "table", "season", "club", "united", "city", "fc"),
          avoid=("who should i", "which team should", "support", "rules", "offside", "how does",
                 "whats the league table", "what is the league table", "whats a league table",
                 "what is a league table", "league table mean", "league table work")),
]

ENTRIES += [
    entry("back-to-running",
          (("running", "run", "jogging", "jog", "training", "gym", "exercise", "swim",
            "swimming", "cycling", "cycle"),
           ("run again", "how long", "before i run", "before running", "before a run",
            "running again", "back to running", "get back to", "return to", "time off",
            "after being ill", "after the flu", "after a cold", "after a week off",
            "after illness", "after having flu", "start running again",
            "when can i", "when can i run", "when can i start", "how soon can i")),
          "Above the neck and no temperature - a cold, a sore throat - and an easy run is fine "
          "once you feel up to it. Flu or a fever means a week of easy effort after the fever has "
          "gone, building back up over two or three weeks, because the fatigue outlasts the "
          "illness. For a strain or a niggle, walk pain-free first, then run and walk in "
          "alternate minutes, and add a little each week rather than starting where you left off.",
          bias=4,
          ask=("flu", "cold", "ill", "illness", "fever", "sick", "virus", "bug",
               "chest infection", "cough", "throat", "hospital", "operation", "surgery",
               "week off", "time off", "run again", "running again", "back to running",
               "get back to", "return to", "start running again",
               "poorly", "covid", "tonsillitis", "sprain", "strain", "injury", "injured",
               "niggle", "glandular", "bronchitis", "pneumonia", "sinusitis", "ear infection",
               "food poisoning", "been off", "in bed", "off work", "off sick", "bed all week",
               "unwell", "not well", "run down", "recovering", "recovery", "got over",
               "getting over", "temperature"),
          avoid=("rest days", "rest day", "between sessions", "between runs", "between workouts",
                 "in the cold", "cold weather", "cold out", "freezing", "hot weather",
                 "in the heat", "the heat", "wind", "windy", "raining", "rain",
                 "stretch", "stretches", "stretching", "warm up", "warming up", "warmup",
                 "cool down", "cooling down",
                 "eat", "eats", "eating", "food", "breakfast", "fuel", "carb", "carbs",
                 "drink", "drinks", "drinking", "hydrate", "hydration", "water",
                 "getting back", "back into", "after a break", "got out of the habit",
                 "want to start", "wants to start", "wanting to start", "want to get back",
                 "thinking of starting", "keen to start", "hoping to start", "out of shape",
                 "rest before running", "rest before a run", "rest before i run", "how much rest",
                 "how often", "days a week",
                 "learn to swim", "learning to swim", "learn swimming", "swim lessons",
                 "swimming lessons", "swim school", "cannot swim", "cant swim", "can not swim",
                 "couch to 5k", "marathon", "10k", "half", "parkrun", "plan", "training plan",
                 "tweaked", "pulled", "sprain", "sprained", "knee", "shin", "ankle", "calf",
                 "achilles", "hurt", "hurts", "pain", "injury", "injured",
                 "after years", "years ago", "years off", "been years", "used to run",
                 "used to jog", "stopped running", "years since",
                 "fracture", "fractures", "fractured", "stress fracture", "broken bone",
                 "hairline", "cracked bone")),
    entry("stress-fracture",
          (("stress fracture", "stress fractures", "fracture", "fractures", "fractured",
            "hairline crack"),
           ("run", "running", "jog", "jogging", "sport", "exercise", "training", "train",
            "shin", "shins", "foot", "feet", "leg", "legs", "again", "off",
            "weeks", "how long", "heal", "healing",
            "have", "has", "got", "ive", "diagnosed", "doctor", "gp", "x-ray", "xray")),
          "Six to eight weeks off running is the usual answer for a stress fracture, and the bone "
          "decides rather than the calendar. A foot one often gets a walking boot for a few "
          "weeks. Keep some fitness with swimming or cycling if that is pain-free, and come back "
          "with walk-run: a minute of jogging to two of walking, adding a minute a week. Get it "
          "looked at if one small spot is tender to a fingertip or it hurts sitting still.",
          avoid=("think", "thinking", "might have", "could be", "not sure", "do i have",
                 "is it broken", "is it a fracture", "is it a stress fracture", "broken or sprained",
                 "shin splints", "how do i tell", "how to tell", "tell the difference",
                 "show on", "x-ray", "xray", "scan", "mri",
                 "arm", "arms", "wrist", "wrists", "hand", "hands", "finger", "fingers",
                 "rib", "ribs", "collarbone", "shoulder", "shoulders", "hip replacement",
                 "back", "backs", "spine", "spinal", "neck", "vertebra",
                 "osteoporosis", "bone density", "heart", "heartbroken", "phone", "screen",
                 "wind", "voice",
                 "off work", "sick note", "fit note", "back to work", "hairline fracture",
                 "how do i know", "do i know", "can i tell", "is my", "do i have one",
                 "feel like")),
    entry("goggles-that-fog",
          (("goggles", "goggle", "mask", "lens", "lenses", "swim cap"),
           ("fog", "fogging", "fogged", "foggy", "steam", "steams", "steamed", "steaming",
            "mist", "misting", "misted", "clear", "blurred", "condensation", "swim", "swim",
            "swimming", "pool", "lens")),
          _goggles_fog,
          avoid=("car", "driving", "headlights", "windscreen", "wipers", "motorway", "road",
                 "mirror", "bathroom", "shower", "window", "windows", "spectacles",
                 "glasses", "walking", "walk"),
          guard=the_goggles_are_for_swimming,
          bias=2),
    entry("basketball-layup",
          (("layup", "lay up", "lay-up", "layups", "lay ups", "drive to the basket",
            "finish at the rim", "under the basket"),
           ("basketball", "basket", "hoop", "rim", "backboard", "ball", "how")),
          "Go up off the foot opposite your shooting hand - right hand, left foot - and take the "
          "last dribble with the outside hand a stride before you jump. Bring the ball up in two "
          "hands and let it go softly off the backboard into the top corner of the square, rather "
          "than throwing it at the rim. Aim to jump up rather than forward: most missed layups are "
          "a jump that was too long and too fast.",
          ask=("how", "what", "should", "help", "better"),
          avoid=("rules", "foul", "points", "positions", "travel", "travelling", "highway")),
    entry("spin-a-cricket-ball",
          (("spin", "spinner", "spinning", "leg spin", "off spin", "turn the ball", "ripping"),
           ("cricket", "ball", "bowl", "bowling", "bowler", "off break", "leg break", "googly",
            "seam", "fingers")),
          "Spin comes from the fingers and the wrist, not the shoulder: hold the ball across the "
          "seam in the fingers rather than deep in the palm, and as the arm comes over give it a "
          "sharp clockwise rip from the third finger so it turns off the pitch. Keep the arm "
          "straight and the run-up slow - spin is a skill of the hand, and the slower ball turns "
          "more. Practise on a line until the ball lands where you look.",
          ask=("how", "what", "should", "help", "better"),
          avoid=("rules", "points", "wicket", "score", "overs", "match", "spin class",
                 "spin cycle", "washing machine", "spin dryer", "spin doctor", "spinning class",
                 "spin bike", "road bike"),
          bias=2),
    entry("tennis-backhand",
          (("backhand", "back hand", "two handed backhand", "one handed backhand",
            "double hander"),
           ("tennis", "court", "racket", "racquet", "ball", "how", "hit", "swing")),
          "Turn your shoulders as the ball comes and take the racket back with both hands if it is "
          "a two-hander, then meet the ball out in front of your front hip with a flat face and "
          "swing low to high so the ball lifts. Hold the finish over your shoulder rather than "
          "stopping at the ball - the follow-through is where the control comes from. Practise "
          "the turn first: most backhands fail on the shoulders, not the arm.",
          ask=("how", "what", "should", "help", "better"),
          avoid=("backhanded compliment", "backhanded remark", "backhanded comment",
                 "a compliment", "rules", "score", "butternut", "roast squash", "squash soup",
                 "squash the", "table tennis", "padel", "drive"),
          bias=2),
    entry("rugby-drop-goal",
          (("drop goal", "drop goals", "drop kick", "dropkick", "drop kicked", "three points"),
           ("rugby", "posts", "over the posts", "conversion", "penalty try", "score")),
          "For a drop goal, catch the pass and hold the ball out in front of you with its point "
          "down, then drop it and kick it off the ground as it starts to bounce - the ball has to "
          "touch the ground first, so the timing is the whole skill. Watch the ball rather than "
          "the posts, keep your head down, and strike through the bottom half so it goes up and "
          "over. Practise from ten metres until you can do it without looking at your feet.",
          ask=("how", "what", "should", "help", "better"),
          avoid=("goal setting", "set a goal", "smart goal", "goals for", "new year", "target",
                 "aim", "resolution"),
          bias=2),
    entry("football-throw-in",
          (("throw in", "throw-in", "throw ins", "throw-ins", "throw the ball in",
            "take a throw", "long throw"),
           ("football", "soccer", "touchline", "pitch", "keeper", "corner", "byline",
            "the line", "how")),
          "Both feet stay on the ground behind the line, and the ball goes back over your head "
          "with both hands on it from behind - a foot over the line or a hand that comes round "
          "the side turns it over. Plant both feet shoulder width, get some bend in the elbows and "
          "throw it flat to a teammate's feet rather than high and looping. The long throw is a "
          "run-up and a bigger arch of the back, and it is worth learning only if you can reach "
          "the box.",
          ask=("how", "what", "should", "help", "better"),
          avoid=("bin", "bins", "rubbish", "trash", "away", "out", "recycle", "laundry",
                 "washing", "clothes", "old", "throw the ball at", "throw up")),
    entry("learn-to-skateboard",
          (("skateboard", "skateboards", "skateboarding", "skate", "longboard", "ollie",
            "cruiser"),
           ("learn", "start", "beginner", "first", "how", "begin", "ride", "balance")),
          "Find flat, empty tarmac and a line to stand on, and learn to push and stop before you "
          "try anything else: front foot across the board at an angle, back foot on the ground, "
          "and three pushes then both feet on. Bend your knees and keep your weight over the "
          "board rather than leaning back, and look where you are going, not at your feet. A "
          "helmet and wrist guards cost less than an evening in A&E, and pads make you braver.",
          ask=("how", "what", "should", "help", "start", "begin"),
          avoid=("price", "cheap", "buy", "gift", "present", "brand", "skating on thin ice",
                 "ice", "rules", "on the road", "road", "roads", "traffic", "street",
                 "cycle lane", "pavement")),
    entry("snooker-break-off",
          (("break off", "break off shot", "breaking off", "opening shot", "break shot",
            "first shot"),
           ("snooker", "cue", "billiards", "pool table", "reds", "baulk", "pack", "frame",
            "table")),
          "Put the cue ball just off the side cushion and hit the outside of the pack thinly with "
          "screw, so the cue ball comes back up the table and tucks behind baulk rather than "
          "sitting in the open. A soft, thin contact brings a red out to the side pocket for the "
          "next shot, and the safety is the point: the break-off is not a shot to win the frame "
          "with. Do not hit the pack straight on, because that leaves the cue ball in the middle.",
          ask=("how", "what", "should", "help", "better"),
          avoid=("rules", "points", "score", "ball count", "how many", "take a break", "break up",
                 "break in", "breaking in", "tea break", "lunch")),
    entry("golf-putting",
          (("putt", "putts", "putting", "putter", "green", "lag putt", "three putt"),
           ("golf", "hole", "score", "better", "improve", "how", "practice", "practise")),
          "For most club golfers the pace matters more than the line: pick a spot a foot past the "
          "hole on the high side and try to roll the ball over it, because a putt that finishes "
          "close is holed eventually and one that is hit too hard is not. Keep the wrists still "
          "and rock the shoulders, with the same length back and through. On long putts, aim to "
          "leave it inside a metre rather than to hole it.",
          ask=("how", "what", "should", "help", "better", "improve"),
          avoid=("put the kettle", "put off", "put on", "put up with", "put down", "put away",
                 "putting on", "putting off", "putting up", "put it", "rules", "handicap",
                 "improve my putting", "better at putting", "putting tips", "my putting",
                 "putting stroke", "putting lesson",
                 "zip", "zips", "zipper", "zippers", "sew", "sewing", "seam", "hem")),
    entry("tennis-get-better",
          (("get better", "get better at", "improve", "better at", "practise", "practice",
            "technique", "training", "my forehand", "my backhand", "my game"),
           ("tennis", "forehand", "backhand", "racket", "racquet", "court", "baseline")),
          "Club tennis is won by keeping the ball in, so play the percentages: height over the net "
          "and length to the back of the court, and count how many cross-court balls you can rally "
          "without missing - 20, then 30. Two sessions a week of that beats a new racket. Then "
          "practise the shot that actually loses you games: 50 serves to the same corner, and 50 "
          "returns down the middle.",
          avoid=("table tennis", "ping pong", "paddle", "serve", "serving", "toss",
                 "double fault", "how big", "how long", "size",
                 "dimensions", "resting", "cost", "price", "best racket", "which racket",
                 "elbow", "wrist", "shoulder",
                 "hurt", "hurts", "hurting", "pain", "pains", "painful", "sore", "soreness",
                 "ache", "aches", "aching", "injury", "injured", "injuring", "tennis elbow",
                 "stiff", "strain", "strained", "swollen", "swelling", "torn", "physio",
                 "physiotherapy", "doctor", "nhs", "gp")),
    entry("first-touch",
          (("first touch", "first touches", "touch", "control", "cushion", "improve", "get better",
            "practice", "practise"),
           ("first touch", "my touch", "touch", "control the ball", "ball control",
            "controlling the ball", "touch and control", "cushion", "first")),
          "A first touch is a cushion, not a stop: as the ball arrives, take the pace out of it and "
          "push it a stride ahead into the space you are about to run into. Kick a ball against a "
          "wall 200 times a day with each foot, using the inside and the sole, then have a partner "
          "pass at speed. Twenty minutes of wall work a day fixes more first touches than any drill "
          "with cones.",
          avoid=("remote", "tv", "television", "birth control", "the pill", "pest control",
                 "weeds", "mould", "damp", "temper", "lose control")),
    entry("dribbling",
          (("dribbling", "dribble", "close control", "keep the ball"),
           ("football", "soccer", "improve", "better", "practice", "practise", "cones")),
          "Keep the ball within a stride of you and touch it every step or two - small touches "
          "with the inside and outside of both feet, head up so you can see the pass before you "
          "make it. Four cones two metres apart, through them slow enough to be perfect, then "
          "faster, then with someone shadowing you. A change of pace beats a change of direction: "
          "slow, then push it past and go.",
          avoid=("basketball", "hoop", "boots", "rules", "offside", "how many players")),
    entry("golf-swing",
          (("get better", "get better at", "improve", "practice", "practise", "fix", "stop",
            "stopping", "swing", "swings", "off the tee", "slice", "slicing", "hook",
            "hooking", "half swing", "ball striking", "my drive", "my tee shot", "my driver",
            "hit my driver", "hit my drive", "hit my irons"),
           ("golf", "swing", "swings", "drive", "driver", "drivers", "tee", "slice", "hook",
            "chipping", "putting", "irons", "fairway", "bunker")),
          "For most club golfers it is not the swing but the aim and the tempo: check that feet, "
          "hips and shoulders all point where you want the ball to start, then swing at eight out "
          "of ten with a smooth one-two count. Practise half-swings with a 7 iron and brush the "
          "grass - the divot should come after the ball. Two or three lessons with a pro filming "
          "you will save a season of guessing.",
          avoid=("bread", "loaf", "loaves", "cake", "onion", "onions", "garlic", "meat", "roast",
                 "ham", "cheese", "finger", "fingers", "hand", "kitchen", "knife",
                 "garden", "park", "playground", "swing seat", "swingball", "mood", "moods",
                 "shift", "vote", "voting", "election", "how many holes",
                 "how long", "handicap", "rules", "score", "scoring", "cost", "price",
                 "driving test", "driving lesson", "driving licence", "driving license",
                 "driving theory", "hard drive", "flash drive", "usb", "printer", "back up",
                 "car", "cars", "at driving", "driving a car", "driving on", "learn to drive",
                 "driving school", "drive to", "laptop", "laptops", "coat hook",
                 "wall hook", "picture hook", "curtain", "curtains", "hooks on the wall",
                 "stain", "stains", "stained", "driveway", "drive way", "off the drive",
                 "on the drive", "moss", "pressure wash", "jet wash", "paving",
                 "learner", "learners", "learner driver", "provisional", "driving with",
                 "practice driving", "practise driving", "driving practice", "driving practise",
                 "dual controls", "instructor", "parallel park", "bay park", "test route",
                 "coat", "coats", "on a coat", "jacket", "jackets", "hanger", "hangers",
                 "curtain rail", "picture rail"),
          guard=_a_put_is_not_a_putt),
    entry("cricket-get-better",
          (("get better", "get better at", "improve", "better at", "practice", "practise",
            "technique", "batting", "bowling", "score runs", "my batting", "my bowling",
            "bowl", "bowled", "bowling a", "how do i bowl", "my action", "run up", "no ball",
            "no balls", "yorker"),
           ("cricket", "nets", "bowler", "batting", "bowling", "wicket", "batsman", "batter",
            "yorker", "bouncer", "googly", "off stump", "leg stump", "crease", "seam",
            "bowling action", "spin bowling", "how do i bowl")),
          _cricket_better,
          avoid=("rules", "work", "lbw", "leg before", "how long", "how many overs", "t20",
                 "ashes", "world cup", "history", "duck", "how many players",
                 "lawn bowls", "crown green", "indoor bowls", "bowls club", "bowls match",
                 "play bowls", "playing bowls", "game of bowls", "bowls green", "jack high"),
          guard=_the_game_and_not_another),
    
    entry("basketball-get-better",
          (("shooting", "shoot", "my shot", "jump shot", "free throws", "free throw", "get better",
            "improve", "practice", "practise", "technique",
            "dribble", "dribbling", "dribbled", "ball handling", "ball-handling",
            "bring the ball up", "crossover"),
           ("basketball", "hoop", "foul line", "free throw line", "three point",
            "ball handling", "ball-handling", "dribbling a basketball")),
          _basketball_better,
          avoid=("rules", "work", "points", "quarters", "how many players", "how long",
                 "court size", "how big",
                 "football", "soccer", "foot", "feet", "netball")),
    entry("darts-get-better",
          (("get better", "improve", "practice", "practise", "technique", "my throw", "throwing",
            "accuracy", "consistent"),
           ("darts", "treble", "double", "oche", "board", "180")),
          "Change nothing but the aim: same stance, same grip, same speed every throw, elbow up, "
          "and a follow-through that finishes with your hand pointing at the target. Practise in "
          "blocks - 20 darts at treble 20, then 20 at the doubles round the board, and always "
          "finish on a double. If the darts drift, slow the throw down rather than throwing "
          "harder; speed is what scatters them.",
          avoid=("rules", "501", "checkout", "scoring", "score", "how many", "how long")),
    entry("badminton-get-better",
          (("get better", "improve", "practice", "practise", "technique", "footwork", "my serve"),
           ("badminton", "shuttle", "shuttlecock", "racket", "racquet")),
          "Badminton is won with the feet: after every shot get back to the middle of the court, "
          "and split-step as your opponent hits so you can move either way. Learn the overhead "
          "clear hit high and deep to the back line, then the drop shot from the same action, so "
          "your opponent cannot read it. Twenty minutes of shadow footwork with a racket in your "
          "hand beats an hour of hitting.",
          avoid=("rules", "scoring", "score", "how many points", "how long", "court size")),
    entry("volleyball-serve",
          (("serve", "serving", "my serve", "overhand serve", "underhand serve", "float serve",
            "jump serve", "serves", "goes long", "keeps going long", "keeps going out"),
           ("volleyball", "volley ball", "volley-ball", "over the net", "the net")),
          "Toss the ball low and just in front of your hitting shoulder - a high toss behind you "
          "is why serves go long - then hit it with the heel of your hand, arm swinging fast and "
          "straight, and aim at a spot (deep middle, or the gap between two passers) rather than "
          "just over the net. Practise twenty a session and count the ones that land in: a serve "
          "that goes in beats an ace you miss.",
          avoid=("dinner", "food", "drink", "wine", "portion", "tennis", "badminton", "squash",
                 "padel", "legal", "notice", "papers", "prison", "time"),
          bias=1),
    entry("volleyball-get-better",
          (("get better", "improve", "practice", "practise", "technique", "my pass",
            "spike", "spiking", "dig", "digging", "block", "blocking", "setting", "set"),
           ("volleyball", "volley ball", "volley-ball")),
          "Volleyball starts with the pass: get your feet there early, lock your arms into a "
          "platform and let the ball come to you instead of swinging at it - it should go up and "
          "to the setter, not forward. A spike is the last touch of three: high approach, arm back, "
          "and hit the top half of the ball so it drives down; a dig is the same low platform, "
          "absorbing the ball rather than swinging at it. Serve overhand for consistency, and call "
          "the ball loudly.",
          avoid=("beach", "rules", "how many players", "how long")),
    entry("rowing-technique",
          (("get better", "improve", "technique", "form", "practice", "practise", "split",
            "properly", "proper", "good form", "right way", "catch", "drive",
            "how do i", "how to", "learn"),
           ("rowing", "row", "rows", "rowed", "rower", "erg", "ergo", "ergometer",
            "rowing machine", "concept 2", "oars", "scull", "sculls", "eight", "cox",
            "boat", "boats", "a boat", "the boat", "indoor rower")),
          "Rowing is legs, then body, then arms on the drive, and arms, body, then slide on the way "
          "back. Keep the handle level and pull it to the same spot at the bottom of the ribs every "
          "stroke, and rate 20 to 22 rather than thrashing at 30. Ten minutes of steady pieces "
          "with someone filming you side-on will show the timing errors faster than any coaching "
          "cue.",
          bias=1,
          avoid=("argument", "row with", "row about", "arguing", "quarrel", "fight", "seats",
                 "houses", "terraced", "front row", "death row", "rules",
                 "had a row", "having a row", "a row with", "our row", "massive row",
                 "huge row", "proper row", "bitter row", "row last night", "rows with")),
    entry("cycling-get-better",
          (("get better", "improve", "faster", "training", "train", "practice", "practise"),
           ("cycling", "cycle", "bike", "bicycle", "rides", "riding")),
          "Ride easy miles before hard ones: three or four rides a week with one long steady one, "
          "spinning at 80 to 90 turns a minute in a gear you can hold. Add one session of 4 x 5 "
          "minutes hard with 5 minutes easy between, and put the hills in the long ride. Check "
          "saddle height first - a saddle too low costs power and sore knees.",
          avoid=("motorbike", "motorcycle", "scooter", "moped", "which bike", "best bike",
                 "buy", "cost", "price", "child", "son", "daughter", "toddler", "learn to ride",
                 "stabilisers", "puncture", "chain", "brakes", "helmet",
                 "horse", "horses", "pony", "ponies", "equestrian", "trot", "canter",
                 "gallop", "stirrups", "riding hat", "riding school", "hacking",
                 "train ride", "train journey", "train trip", "coach trip", "coach journey",
                 "bus journey", "bus trip", "by train", "on a train", "on the train",
                 "by coach", "on a coach")),
    entry("horse-riding",
          (("get better", "improve", "learn", "ride", "riding", "sit", "canter", "trot",
            "stop bouncing", "how do i"),
           ("horse", "horses", "pony", "ponies", "equestrian", "trot", "canter", "gallop",
            "stirrups", "riding hat", "riding school", "hacking")),
          "Sit deep and still: a long leg with the heel down and a soft hand that follows the "
          "horse's mouth does more than any amount of kicking. Learn to absorb the movement in "
          "your hips rather than your hands - walk and trot without stirrups, on the lunge if you "
          "can - and ride a well-schooled horse at a riding school for a term; the feel of a "
          "trained one teaches faster than a green horse will.",
          avoid=("buy", "buying", "cost", "price", "how much", "race", "racing", "bet", "bets",
                 "fall", "fell off", "injury", "injured", "back hurts", "vet")),
    entry("pool-table-get-better",
          (("get better", "get good", "get good at", "improve", "practice", "practise", "play",
            "playing", "cue ball", "my break", "position"),
           ("pool", "billiards", "eight ball", "8 ball", "pool table", "cue", "snooker",
            "cue ball control", "control the cue", "controlling the white", "control the white",
            "spin", "pot", "table")),
          "Cue games are won with the cue ball, not the pot: before every shot decide where the "
          "white has to finish for the next one, and hit it with the pace that leaves the easiest "
          "next shot rather than the hardest pot. Play the shot you can make nine times out of ten. Practise "
          "a straight pot up and down the table 50 times, stopping the cue ball dead, then "
          "following through and screwing back.",
          bias=1,
          avoid=("swim", "swimming", "lengths", "lido", "water", "car pool", "carpool", "typing",
                 "gene pool", "pool of",
                 "table tennis", "ping pong", "tennis",
                 "phone", "app", "apps", "video game", "on my tablet", "online game",
                 "anger", "angry", "temper", "emotions", "impulse", "drinking", "appetite",
                 "blame", "my feelings", "anxiety", "stress",
                 "spin class", "spin classes", "spinning class", "spinning classes",
                 "at spinning", "my spinning", "indoor cycling", "exercise bike", "peloton",
                 "soulcycle", "rpm")),
    entry("run-form",
          (("form", "technique", "cadence", "posture", "overstriding", "over striding",
            "heel strike", "running style", "run properly"),
           ("run", "running", "jog", "jogging", "my run", "runs")),
          "Run tall and quiet: a slight lean from the ankles, feet landing under your hips rather "
          "than out in front, and a quicker, shorter stride - about 170 to 180 steps a minute. "
          "Think light and quick, not long. Finish an easy run with 4 x 30 seconds of fast relaxed "
          "strides, and film yourself side-on once: overstriding is the fault nearly everyone "
          "has.",
          avoid=("fill in", "fill out", "fill", "application", "tax", "school", "sick note",
                 "consent", "form for", "this form", "the form", "printing", "printer", "visa"),
          bias=1),
]

ENTRIES += [
    entry("tennis-love", (("love",), ("in tennis", "tennis", "score", "scoring", "40", "nought",
                                      "mean", "means")),
          "Love is nought in tennis, said to come from the French for an egg. A new game starts "
          "at love-all, and 40-0 is called forty love.",
          bias=2),
    entry("tennis-deuce", (("deuce", "advantage", "tie break", "tiebreak", "tie-break"),
                           ("what", "whats", "mean", "means", "is", "score", "scoring", "how",
                            "work", "tennis", "why", "called")),
          "40-40 is deuce: from there you need two points in a row, and the first of them is "
          "advantage, so a game can go on a long time. At 6-6 in a set a tie-break decides it - "
          "first to seven points, two clear.",
          bias=2,
          avoid=("work", "shift", "lunch", "job", "boss", "employer", "overtime")),
    entry("snooker-frames", (("snooker",), ("frames", "frame", "how many", "long", "match",
                                            "final")),
          "A frame is one game of snooker, and a match is a set number of them: tour finals are "
          "usually best of 19 frames and the World Championship final is best of 35, played over "
          "two days in four sessions.",
          bias=1),
    entry("football-subs", (("football", "soccer", "premier league"),
                            ("subs", "substitutes", "substitution", "substitutions", "bench")),
          "Five substitutions from three stoppage windows in the Premier League and most "
          "competitions, plus a sixth in extra time; it was three until 2020. A bench of nine is "
          "named, so most of the squad gets a game.",
          ask=("football", "soccer", "premier league"),
          bias=1),
    entry("start-watching-football",
          (("football", "soccer", "premier league", "the premier league", "champions league",
            "match of the day", "the football"),
           ("get into", "getting into", "start watching", "begin watching", "keep up with",
            "keep up", "follow", "learn about", "understand", "beginner", "beginners",
            "know nothing", "dont know anything", "don't know anything", "new to",
            "where to start", "who should i support", "which team should i support",
            "which team", "how do i watch", "watch football", "watching football",
            "talk about football", "on tv")),
          "Start with one team and one weekly programme rather than the whole sport: pick the club "
          "nearest you, or the one your family and friends already argue about, and watch its "
          "highlights every week - Match of the Day or ten minutes on the club's app. Learn three "
          "things and the rest follows: offside, what a VAR check is stopping play for, and how "
          "the league table works (three points for a win, one for a draw, most points wins). A "
          "local non-league or Sunday game costs a fiver and teaches you more in ninety minutes "
          "than a month of television, and listening to one weekly podcast gives you the names "
          "everyone else already knows.",
          ask=("football", "soccer", "premier league", "watch", "follow", "understand"),
          avoid=("play", "playing", "played", "boots", "shin pads", "five a side", "5 a side",
                 "tickets", "ticket", "bet", "betting", "odds", "accumulator", "fantasy",
                 "fpl", "fifa", "video game", "cricket", "rugby", "tennis", "golf", "f1",
                 "formula 1", "netball", "hockey", "darts", "kids", "child", "son", "daughter",
                 "nursery", "school")),

    entry("transfer-window", (("transfer window", "transfer windows", "transfer deadline",
                              "deadline day"),
                             ("what", "whats", "mean", "means", "is", "how", "work", "works",
                              "when", "closes", "open", "football")),
          "It is the period when a club can register new players: a long summer window, roughly "
          "June to the start of September, and a short one through January. Outside them nobody "
          "can move, which is why deadline day is frantic.",
          bias=2),
    entry("pit-stop", (("pit stop", "pit stops", "pitstop", "pit lane"),
                       ("what", "whats", "mean", "means", "is", "how", "work", "long", "tyres",
                        "f1", "formula 1")),
          "A pit stop is the stop for fresh tyres: the crew changes all four in about two "
          "seconds, and with the drive down the pit lane at the speed limit it costs roughly 20 "
          "seconds of race time. Most races are one or two stops.",
          bias=2),
    entry("rugby-knock-on", (("knock on", "knock-on", "knocked on", "forward pass"),
                             ("what", "whats", "mean", "means", "is", "rugby", "happens", "why",
                              "rule")),
          "A knock-on is losing the ball forward out of your hands, or it bouncing forward off "
          "your arm: play stops and the other side gets a scrum where it happened. A forward pass "
          "is the same offence thrown instead of dropped.",
          bias=2,
          avoid=("door", "doors", "neighbour", "neighbor", "visitor", "caller")),
    entry("rugby-lineout", (("lineout", "line out", "line-out"),
                            ("what", "whats", "mean", "means", "is", "rugby", "how", "work",
                             "rule")),
          "A lineout restarts play after the ball goes into touch: the forwards of both sides "
          "line up in two rows, a hooker throws the ball straight down the middle, and the "
          "jumpers are lifted to catch it. The throwing side usually wins their own ball.",
          bias=2),
    entry("rugby-maul", (("maul", "mauls", "ruck", "rucks"),
                         ("what", "whats", "mean", "means", "is", "rugby", "how", "work",
                          "rule", "difference")),
          "A maul is a ball carrier held up with teammates bound on to him, everyone on their "
          "feet; a ruck is the same idea with the ball on the ground. In both, players must stay "
          "on their feet, join from behind the ball, and the side going forward gets the "
          "advantage.",
          bias=2,
          avoid=("carpet", "carpets", "rug", "rugs", "floor", "floors", "flooring", "underlay",
                 "gripper", "grippers", "laminate", "lino", "linoleum", "mat", "mats")),
]

ENTRIES += [
    entry("golf-grand-slam", (("grand slam", "grand slams", "majors", "major"),
                              ("golf", "golfer", "masters", "open championship", "pga")),
          "The four men's majors are the Masters at Augusta in April, the PGA Championship in "
          "May, the US Open in June and the Open Championship in July. Winning all four in one "
          "year is the calendar Grand Slam - only Bobby Jones, in 1930, and Tiger Woods, in 2000 "
          "and 2001 across two years, have come close.",
          bias=3,
          avoid=("tennis", "wimbledon")),
    entry("rugby-grand-slam", (("grand slam", "grand slams", "triple crown"),
                               ("rugby", "six nations", "wales", "ireland", "england", "scotland",
                                "france", "italy")),
          "In the Six Nations a Grand Slam is winning all five of your matches in the same "
          "season, which also brings three bonus points; a Triple Crown is one of the home "
          "nations beating the other three.",
          bias=3,
          avoid=("tennis", "wimbledon", "golf")),
    entry("nfl-length", (("nfl", "american football", "super bowl"),
                         ("how long", "long", "last", "hours", "minutes", "game", "watch")),
          "Four 15-minute quarters, so 60 minutes of play, but the clock stops on every "
          "incomplete pass and the whole game runs about three hours, and longer for the "
          "Super Bowl with its half-time show.",
          bias=2),
]

ENTRIES += [
    entry("triple-crown", (("triple crown",), ("what", "whats", "is", "mean", "means", "rugby",
                                              "six nations", "horse", "racing", "win", "won")),
          "In rugby's Six Nations, the Triple Crown goes to whichever of England, Ireland, "
          "Scotland or Wales beats the other three in the same season. In US horse racing it is "
          "winning the Kentucky Derby, the Preakness and the Belmont Stakes in one year.",
          bias=2),
]


ENTRIES += [
    entry("squash-the-game",
          (("squash", "squash court", "racquetball"),
           ("play", "playing", "rules", "court", "rak", "racket", "racquet", "game", "beginner",
            "better", "start", "serve", "serve")),
          "Squash is two players in a room, and you win a point only when you serve: hit the ball "
          "above the middle line and below the top line onto the front wall, and let it bounce "
          "once on the floor. If it goes out, hits the tin or bounces twice, the point is over. "
          "Stand near the T in the middle after your shot - whoever holds the middle wins.",
          ask=("how", "what", "whats", "should", "any", "rules"),
          avoid=("roast", "roasted", "recipe", "cook", "cooking", "oven", "butternut", "bake",
                 "soup", "squash recipe", "cordia", "cordial", "drink", "grow", "growing",
                 "allotment", "plant", "plants", "seed", "seeds"),
          bias=1),
    entry("discus",
          (("discus", "discus throw", "shot put", "shotput", "hammer throw", "hammer"),
           ("how do i", "throw", "throwing", "technique", "better", "far", "further", "coach",
            "training", "rules")),
          _a_circle_throw,
          ask=("how", "what", "should", "any", "far", "further"),
          avoid=("washing machine", "machine", "cycle", "tumble", "blanket", "blankets",
                 "cushion", "dryer", "towel", "tumble dryer", "load", "nail", "picture",
                 "wall", "thumb", "toe"),
          bias=1),
    entry("javelin",
          (("javelin", "javelin throw", "throw a javelin", "throwing a javelin"),
           ("how do i", "throw", "throwing", "technique", "better", "far", "further", "coach",
            "training", "rules", "what")),
          "A javelin is thrown over the shoulder from a run: a straight run-up of about eight "
          "strides building through the last three, the arm back and high with the point level "
          "by your ear, then the front foot plants and the hips turn before the arm comes "
          "through. Let it go with the tip up and run through past the line, because the throw is "
          "measured where the tip lands. The length comes from the run-up and the hip turn, not "
          "from muscling it.",
          ask=("how", "what", "should", "any", "far", "further"),
          avoid=("washing machine", "machine", "cycle", "phone", "pen", "pencil", "arrow"),
          bias=1),
    entry("googly",
          (("googly", "leg spin", "leg break", "off spin", "off break", "offbreak", "offspin",
            "wrist spin", "finger spin", "what is a googly", "wrong un", "wrongun",
            "bowl a googly", "bowling a googly", "bowl leg spin"),
           ("what", "whats", "is", "mean", "means", "bowl", "bowling", "spin", "bowler",
            "how", "how do i", "work")),
          "Spin is the bowler turning the ball off the pitch: a leg break turns away from a "
          "right-hander, an off break turns in, and a googly is a leg-spinner's ball that turns "
          "the other way - it looks like a leg break out of the hand, but the wrist rolls the "
          "other way. Batsmen read it off the pitch rather than the hand, because the wrist gives "
          "it away late.",
          ask=("what", "whats", "what's", "is", "mean", "means", "explain", "define",
               "how", "how do i", "bowl", "bowling"),
          bias=1),
    entry("running-injury",
          (("injury", "injuries", "get injured", "stay injury free", "injured", "sore knees",
            "shin splints", "overtraining"),
           ("running", "run", "jogging", "jog", "training", "avoid", "prevent", "marathon",
            "half marathon", "10k", "5k")),
          "Nearly all running injuries come from doing more, sooner than the body can repair: add "
          "no more than about 10 per cent to your weekly distance, keep every second run easy, "
          "and take a rest day after a long one. Two short strength sessions a week - calf raises, "
          "squats, a single-leg balance - and shoes that are not worn through do the rest. Sharp "
          "pain that changes how you run means stop.",
          ask=("how", "what", "any", "prevent", "avoid", "should"),
          avoid=("already", "i hurt", "i have hurt", "it hurts", "he hurt", "she hurt", "pain now",
                 "swollen", "bleeding", "sprain", "broke"),
          bias=1),
    entry("running-breathing",
          (("breathe", "breathing", "out of breath", "breathless", "breath"),
           ("running", "run", "jogging", "jog", "while i run", "when i run", "long runs",
            "marathon", "5k", "10k")),
          "Breathe in through the nose and mouth together, into the belly rather than the chest, "
          "and let the rhythm follow your steps - two in, two out, then three and three when the "
          "pace is easy. If you can only speak a few words at a time, slow down: most breathless "
          "running is a pace problem, not a lung problem. Cold air is fine, just warm up first.",
          ask=("how", "what", "should", "any"),
          avoid=("asthma", "inhaler", "wheeze", "wheezing", "cough", "coughing", "covid",
                 "chest pain", "can't breathe", "cant breathe", "cannot breathe", "choking"),
          bias=1),
    entry("golf-handicap",
          (("handicap", "handicaps", "handicap index", "playing handicap"),
           ("golf", "work", "works", "what is", "how does", "lower", "get", "calculate",
            "explain")),
          "A handicap is how many shots you get: it is roughly your best scores, averaged, "
          "against the course rating, so a 20-handicapper gets a shot on the 18 hardest holes and "
          "plays the course as a scratch golfer would. It goes down when you score better than "
          "your handicap - you need a few rounds, not one - and it is why two players of "
          "different ability can have a fair match.",
          ask=("what", "whats", "what's", "is", "how", "explain", "mean", "means", "does"),
          bias=1),
    entry("triathlon-training",
          (("triathlon", "triathlons", "ironman", "sprint triathlon", "olympiad distance"),
           ("train", "training", "how do i", "start", "beginner", "first", "prepare", "ready",
            "plan")),
          "Train the bike mostly, because it is the longest leg and the one you can do most of "
          "without damage: two rides a week, one long and one with short hard efforts, plus two "
          "swims of 20 to 30 minutes and two short runs. Practise the changeovers - a brick "
          "session of bike then run - because the first five minutes off the bike feel strange. "
          "A sprint distance (750m, 20k, 5k) is a good first race.",
          ask=("how", "what", "should", "any", "where"),
          avoid=("watch", "watching", "on tv", "results", "winner", "world championship",
                 "hawaii", "kona", "price", "cost", "bike to buy", "wetsuit"),
          bias=1),
    entry("table-tennis",
          (("table tennis", "ping pong", "pingpong"),
           ("play", "playing", "rules", "how do i", "better", "score", "scoring", "serve",
            "bat", "beginner", "start")),
          "Games go to 11 and you serve every two points, so a game turns faster than it looks: "
          "serve short and low, keep the ball on the table rather than hitting it hard, and step "
          "back only when you have to. The basics win club games - a heavy spin serve, a steady "
          "block, and returning the serve rather than trying to win the point with it.",
          ask=("how", "what", "whats", "rules", "should", "any"),
          avoid=("dining table", "tablecloth", "table top", "table runner", "furniture",
                 "buy", "price", "cheap", "restaurant",
                 "clean", "cleaning", "wipe", "dust", "stain", "storage", "store", "storing",
                 "fold", "folding", "bat case", "net"),
          bias=1),
]

ENTRIES += [
    entry("badminton-shots",
          (("smash", "smashing", "jump smash", "drop shot", "drop shots", "net shot", "net shots",
            "overhead clear", "deception"),
           ("badminton", "shuttle", "shuttlecock", "racket", "racquet", "court")),
          "A smash is hit steeply down from above your head: get behind the shuttle, meet it high "
          "and in front, and snap the wrist through it as you step forward. The drop shot and the "
          "net shot are the same action with a slower swing, the first landing just over the net "
          "and the second taken close in so the shuttle tumbles over. A smash is the last shot to "
          "learn: a weak one hands your opponent the attack.",
          ask=("what", "whats", "what's", "how", "explain", "mean", "means"),
          avoid=("window", "windows", "windscreen", "car", "cars", "crash", "crashing",
                 "potato", "potatoes", "pumpkin", "avocado", "burger", "glass", "tennis",
                 "squash", "hit and run", "smash hit", "boxing", "wrestling"),
          bias=1),
    entry("netball-positions",
          (("positions", "position", "roles", "role", "each player", "players do", "who can shoot",
            "goal shooter", "goal attack", "wing attack", "wing defence", "goal defence",
            "shooting circle"),
           ("netball", "netball court", "shooting circle", "goal shooter", "goal attack",
            "wing attack", "wing defence", "goal defence")),
          "Only the two shooters can score: goal shooter stays in the attacking third and goal "
          "attack works the circle edge with her, and the two defenders - goal keeper and goal "
          "defence - are the mirror of them at the other end. Wing attack and wing defence carry "
          "the ball through the middle thirds and centre takes the pass-offs, so the positions "
          "are really about which thirds you may enter.",
          ask=("what", "whats", "which", "who", "how", "explain", "does", "do"),
          avoid=("how long", "how many quarters", "minutes", "substitute", "substitutes",
                 "injury", "injured", "swap", "roll", "rolling"),
          bias=2),
    entry("golf-grip",
          (("grip", "grips", "hold the club", "hold my club", "hold a club", "holding the club",
            "how do i hold", "grip the club", "interlocking", "overlapping", "baseball grip"),
           ("golf", "club", "clubs", "driver", "iron", "irons", "putter", "tee", "shot")),
          "Hold it in the fingers of your left hand, not the palm, with the handle running from "
          "the base of the little finger to the knuckle of the index finger, then lay the right "
          "hand over the top so both Vs point at your right shoulder. Squeeze about three out of "
          "ten: a tight grip stops the wrists hinging, which is where the distance comes from.",
          ask=("how", "what", "which", "should", "any", "explain"),
          avoid=("badminton", "tennis", "squash", "racket", "racquet", "tyre", "tyres", "tire",
                 "wheel", "phone", "camera", "towel", "strength", "grip strength", "bar",
                 "steering", "pen", "pencil", "boot", "boots", "shoes", "floor", "stairs",
                 "handrail", "rail", "train", "bus"),
          bias=2),
    entry("watch-a-tournament",
          (("world cup", "the world cup", "euros", "euro 2028", "european championship",
            "olympics", "olympic games", "world championship", "world championships",
            "commonwealth games", "tournament", "cup final"),
           ("watch", "watching", "on tv", "tv", "television", "stream", "streaming", "channel",
            "where can i", "how do i watch", "tickets", "kick off", "kick-off", "what time")),
          "In the UK the World Cup, the Euros and the Olympics are free to air - BBC and ITV share "
          "the football, and the BBC carries the Olympics with a stream per sport, so pick the "
          "sport rather than hunting the channel. Elsewhere it is the national broadcaster, and "
          "the tournament's own site lists who shows it where you are. Group games sit at fixed "
          "times, so check the kick-off before you plan the evening.",
          ask=("how", "where", "what", "which", "can", "should"),
          avoid=("won", "win", "winner", "winners", "who won", "host", "hosted", "qualify",
                 "qualified", "price", "prices", "cost", "how much", "rugby", "cricket",
                 "darts", "snooker", "results", "highlights", "when did"),
          bias=1),

]
_RACE_WORDS = ("marathon", "marathons", "half marathon", "10k", "5k", "parkrun", "race",
               "races", "ultra", "triathlon", "cross country", "fun run")
_MATCH_WORDS = ("match", "matches", "kick off", "kick-off", "kickoff", "game", "football",
                "rugby", "cricket", "netball", "hockey", "fixture", "derby")
_GIG_WORDS = ("concert", "concerts", "gig", "gigs", "festival", "glastonbury", "gig ")
_FIREWORK_WORDS = ("fireworks", "firework", "bonfire", "display")

_EVENT_START = {
    "race": ("Mass races start early and in waves: most city marathons and half marathons go off "
             "between 8 and 10 in the morning, a 10k usually between 9 and 10, and a parkrun at 9 "
             "on a Saturday. Your race email has your own wave and the time the pens close, which "
             "is the one people miss - and the earlier wave is often the one with the friendlier "
             "cut-offs."),
    "match": ("Most Saturday football kicks off at 3pm and Sunday games at 2pm or 4.30pm, but a "
              "televised game moves by hours, so the club's or the ticket page's fixture list is "
              "the only reliable one. Turn up an hour before for a big ground, because the queues "
              "at the turnstiles are what make people late."),
    "gig": ("Doors for a gig usually open an hour before the support act, and the headline act "
            "comes on about two hours after doors; most venues have a curfew at half past ten or "
            "eleven, so that is roughly when it ends. A big venue also has a bag check, so add "
            "twenty minutes. The venue's own page or your ticket email gives the door time, and "
            "check the last train home before the encore."),
    "fireworks": ("A firework display goes up after dark, so most are between 7 and 9 in the "
                  "evening in November and later in midsummer, and the organiser's page gives the "
                  "exact time because it depends on sunset. Wrap up warm and stand upwind, and get "
                  "there early if you are driving, since car parks empty slowly."),
}

_EVENT_START_GENERIC = ("I can't see the schedule from here, so the organiser's page or your "
                        "confirmation email is the one to trust. Ask about the gate or start pen "
                        "closing time as well, because that is usually earlier than the start, "
                        "and plan to be there half an hour before it.")


def _event_start(memory, understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    found = []
    for kind, words in (("race", _RACE_WORDS), ("match", _MATCH_WORDS),
                        ("gig", _GIG_WORDS), ("fireworks", _FIREWORK_WORDS)):
        if any(word in said for word in words):
            found.append(kind)
    if len(found) == 1:
        return _EVENT_START[found[0]]
    if found:
        return _EVENT_START_GENERIC
    return None


ENTRIES += [
    entry("event-start",
          (("what time", "when do", "when does", "when is", "start time", "what time is",
            "kick off", "kick-off", "kickoff", "doors"),
           ("start", "starts", "starting", "kick off", "kick-off", "kickoff", "doors open",
            "begin", "begins", "go off", "goes off", "what time", "when",
            "marathon", "marathons", "half marathon", "10k", "5k", "parkrun", "race", "races",
            "match", "matches", "game", "football", "rugby", "cricket", "netball", "hockey",
            "concert", "concerts", "gig", "gigs", "festival", "fireworks", "firework",
            "bonfire", "display", "triathlon", "ultra", "fun run", "fixture")),
          _event_start,
          avoid=("parkrun", "park run", "pharmacy", "chemist", "shop", "supermarket", "bank",
                 "post office", "pub",
                 "contracts", "contract", "completion", "complete", "exchange", "keys", "key",
                 "house", "flat", "mortgage", "solicitor", "conveyancer", "sale", "seller",
                 "buyer", "landlord", "tenancy",
                 "restaurant", "open", "opens", "opening", "close", "closes", "closing", "shut",
                 "shuts", "pill", "pills", "tablet", "tablets", "dose", "insulin", "ferry",
                 "flight", "train", "bus", "sunrise", "sunset", "shift", "appointment",
                 "meeting", "interview", "school", "class", "lesson", "service", "opening times"),
          ask=("start", "starts", "starting", "kick off", "kick-off", "kickoff", "doors",
               "begin", "begins", "go off", "goes off", "what time", "when")),
]



_BALL_ASK = ("how", "what", "should", "can", "help", "tips", "technique", "better", "practice",
             "practise")

ENTRIES += [
    entry("penalty-kick",
          (("penalty", "penalties", "penalty kick", "spot kick", "twelve yards"),
           ("take", "taking", "score", "scoring", "shoot", "shooting", "strike", "hit", "shootout",
            "in a match", "into the corner", "side foot", "laces", "practice", "practise",
            "technique", "nervous", "missed", "kept missing")),
          "Pick your corner before the run starts, keep it low and side-foot it inside the post, and "
          "do not change your mind on the last step: a firm, repeatable penalty beats a clever one. "
          "Practise ten to the same corner at the end of training so the run, the plant foot and the "
          "strike are one habit.",
          avoid=("shootout", "sudden death", "how many", "who takes", "order", "world cup",
                 "keeper has to", "the rules", "how does", "the line"),
          bias=2),
    entry("save-a-penalty",
          (("penalty", "penalties", "spot kick", "twelve yards"),
           ("save", "saving", "stop", "stopping", "keeper", "goalkeeper", "in goal", "dive",
            "diving", "guess", "read the taker")),
          "Stay tall and wait: most takers decide their corner early, so watch the standing foot and "
          "the hips rather than the ball, and dive late with a strong hand. Keep your weight on the "
          "balls of your feet so the first step can go either way.",
          avoid=("shootout", "sudden death", "how many", "who takes", "how does", "the rules"),
          bias=2),
    entry("corner-kick",
          (("corner", "corners", "corner kick", "corner flag"),
           ("take", "taking", "kick", "kicking", "swing", "inswing", "outswing", "cross",
            "delivery", "head it", "practice", "practise", "where do i aim")),
          "Aim for the six-yard box rather than the penalty spot: drive it inswinging and low with "
          "the inside of the foot, and send two players across the near post so the keeper has to "
          "decide. Practise one corner ten times - the ball you can repeat beats the clever one.",
          avoid=("shop", "street", "room", "garden", "table", "bed", "photos", "picture",
                 "cupboard", "car", "parking", "hockey", "rugby", "gaelic", "netball", "cricket",
                 "corner shop", "corner of the room"),
          bias=2),
    entry("volley-a-football",
          (("volley", "volleys", "half volley", "on the volley", "volley it"),
           ("football", "ball", "soccer", "practice", "practise", "strike", "technique", "how")),
          "Watch the ball onto your foot instead of swinging at it: get side-on, keep your knee over "
          "the ball and your toe down, and strike through the middle so it stays low. Start with a "
          "ball tossed up and volleyed into a wall, then ask a partner for a low pass to hit first "
          "time.",
          bias=3),
    entry("head-a-football",
          (("header", "headers", "head it", "heading a ball", "head a football", "head the ball",
            "headed goal", "a header", "a header in football", "do a header"),
           ("football", "ball", "soccer", "practice", "practise", "technique",
            "clear it", "score", "hurts", "hurt", "better", "properly", "do it", "how")),
          "Head the ball with your forehead, not the top of your head: attack it, keep your eyes "
          "open, keep your neck firm and head it back where it came from rather than up in the air. "
          "For a clearance, jump early and put your shoulders through it, and learn the timing with "
          "a soft ball so the head does not do the flinching.",
          avoid=("garlic", "nail", "head hurts", "headache", "headaches", "head of hair",
                 "shampoo", "headboard", "bald", "head injury", "concussion", "helmet",
                 "pillow", "dizzy", "head cold", "headlights", "head start",
                 "email", "document", "word", "spreadsheet", "page", "logo", "css", "http",
                 "letterhead", "cv", "template", "website",
                 "head office", "head teacher", "head of", "ahead", "overhead", "head to toe",
                 "head and shoulders", "shower", "beer", "pint", "lettuce", "cabbage",
                 "broccoli", "cauliflower", "bed", "mattress", "comb", "haircut"),
          bias=1),
    entry("juggle-a-football",
          (("juggle", "juggling", "keepy uppies", "keepie uppies", "keep ups", "keepie uppies",
            "football tricks"),
           ("football", "ball", "soccer", "how", "learn", "practice", "practise", "better",
            "without dropping")),
          "Use the laces, keep the knee soft and let the ball drop to your foot instead of reaching "
          "up for it: drop the ball, touch it once and catch it, then add one touch a day. Ten "
          "minutes a day for a fortnight beats an hour once.",
          bias=1),
    entry("strike-a-ball-with-the-laces",
          (("laces", "laces of the boot", "instep", "top of the boot"),
           ("football", "ball", "soccer", "kick", "kicking", "strike", "shoot", "shooting",
            "harder", "far", "how")),
          "Strike it with the laces, not the toes: plant your standing foot beside the ball, point "
          "the toe down, and follow through towards the target so the ball stays low. The power "
          "comes from the follow-through and a locked ankle, not from swinging harder.",
          avoid=("tie my laces", "tie laces", "tying laces", "coming undone", "untied"),
          bias=2),
    entry("match-tickets",
          (("ticket", "tickets", "season ticket", "away end", "home end"),
           ("match", "matches", "football", "soccer", "game", "stadium", "club", "fixture",
            "fixtures", "premiership", "league", "cup final", "rugby", "cricket")),
          "Go through the club's own site rather than a reseller: home tickets usually need a "
          "membership or a ballot first, and the club's official resale page is the only safe way "
          "to get a sold-out one at face value. Buy two or three weeks ahead, before the ballot "
          "closes, and check the kick-off time again the day before because it moves for television.",
          ask=("how", "where", "when", "can", "should", "what"),
          avoid=("concert", "gig", "festival", "train", "rail", "flight", "plane", "cinema",
                 "parking", "speeding", "fine", "parking fine", "expenses", "claim back"),
          bias=2),
    entry("referee-a-football-match",
          (("referee", "refereeing", "ref", "linesman", "assistant referee", "run the line"),
           ("become", "course", "qualification", "qualify", "qualified", "start", "train",
            "training", "match", "football", "game", "whistle", "how", "get into")),
          "Take the FA's free online Laws of the Game course first, then book the basic referee "
          "course through your county FA - about 20 hours, a theory exam and a practical run-out - "
          "and join a local league. Ask for a mentor for your first games, arrive an hour early and "
          "blow the whistle loud: players test a quiet one.",
          avoid=("paid", "pay", "earn", "salary", "reference", "feed the referee", "var",
                 "how many points",
                 "be my referee", "my referee", "referee for my", "referee for a job",
                 "job reference", "for a job application", "for my job application"),
          bias=1),
    entry("referee-pay",
          (("referee", "referees", "ref", "whistle", "linesman", "assistant referee"),
           ("pay", "paid", "money", "earn", "earnings", "salary", "wage", "wages", "how much",
            "get paid", "per match", "a game")),
          "Read the fee off the league's own handbook rather than a round number: grassroots referees "
          "in England are paid a match fee by the competition - around 30 to 45 pounds for an adult "
          "Saturday game - plus mileage, and the level above is a good deal more. Ask the league "
          "secretary what the fee and the travel rate are before your first appointment.",
          avoid=("job", "reference", "references", "employer", "cv", "application"),
          bias=2),

    entry("kit-for-a-wet-match",
          (_WET_MATCH_SPORT, _WET_MATCH_WEAR + _WET_MATCH_WEATHER),
          _kit_for_a_wet_match,
          ask=_WET_MATCH_WEAR, guard=_a_wet_match, bias=3),
]
