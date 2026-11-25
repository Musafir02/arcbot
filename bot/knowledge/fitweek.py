import re

from .lookup import entry

from .home import SMALL_APPLIANCES, WHITE_GOODS
MACHINE_WORDS = tuple(dict.fromkeys(
    [word for pair in WHITE_GOODS + SMALL_APPLIANCES for word in pair]
    + ["appliance", "appliances", "white goods"]))

ANSWERS = ("fitness", "sport")

ENTRIES = [
entry("cool-down",
      (("cool down", "cool-down", "cooldown", "cooling down", "stretch after", "after a workout",
        "after a session", "after a run", "after exercise", "finish a workout", "finish a run"),
       ("how", "should", "need", "do i", "what", "worth", "best", "long", "properly")),
      "Walk or cycle easily for five minutes until your breathing is normal, then hold two or "
      "three stretches for 20 to 30 seconds each - that is the whole cool-down, and it will not "
      "stop next-day soreness. Stretching before a run does not prevent injuries either; "
      "starting slowly does. If you are short of time, skip the stretches and take the extra "
      "ten minutes of sleep.",
      avoid=("hamstring", "calf", "cramp", "how do i stretch", "stretches for", "before or after",
             "warm up", "aching", "ache", "sore", "doms", "stiff",
             "room", "bedroom", "house", "flat", "summer", "weather", "dog", "baby",
             "car", "drink", "fever", "temperature", "bath", "shower",
             MACHINE_WORDS,
             "eat", "eating", "ate", "food", "protein", "carb", "carbs", "snack", "snacks",
             "meal", "breakfast", "lunch", "dinner", "shake", "calories",
             "curry", "chilli", "chili", "stew", "sauce", "soup", "rice", "pasta", "casserole"),
      bias=1),

entry("back-to-exercise",
      (("back into exercise", "getting back into exercise", "get back into exercise",
        "start exercising again", "exercise again", "havent exercised", "have not exercised",
        "havent trained",
        "years off", "stopped exercising", "restart exercise",
        "starting again with exercise", "unfit", "really unfit", "long break"),
       ("how", "best", "should", "start", "again", "after", "long", "years", "slowly",
        "beginner", "where do i")),
      "Start at about half of what you think you can manage and go every other day for the "
      "first two weeks - 20 minutes of walking or easy cycling is plenty, and the aim is to "
      "finish feeling you could have done more. Add about a tenth a week after that, and expect "
      "the second day to be sorer than the first, which is normal, while a joint that hurts is "
      "a stop. Give it six weeks before you judge it, because the habit and the tendons come "
      "back more slowly than the muscle.",
      avoid=("gym", "membership", "swim", "kettlebell", "dumbbell", "running plan", "couch to 5k",
             "run", "runs", "running", "ran", "jog", "jogs", "jogging", "5k", "10k",
             "marathon", "half marathon", "parkrun",
             "explain", "explaining", "explanation", "cv", "resume", "work history",
             "employment", "employer", "interview", "recruiter", "maternity", "career break",
             "how many times", "how often", "times a week", "days a week", "a week", "per week",
             "rest days", "every day"),
      bias=1),

entry("every-day-exercise",
      (("exercise", "exercising"),
       ("every day", "everyday", "daily", "seven days", "7 days", "each day", "every single day",
        "all week", "no rest", "every morning", "every evening", "twice a day")),
      "Yes, for anything you can hold a conversation through - a walk, a bike ride, a swim - and "
      "that is the kind of movement most people can do every day. What needs a day in between is "
      "hard strength work on the same muscles: lift hard today and leave that muscle 48 hours, "
      "because the muscle is built on the rest day, not in the session. Two or three hard "
      "sessions a week plus easy movement on the other days beats five hard ones, which is where "
      "sore joints and stalled progress come from.",
      avoid=("how much exercise", "how long", "how many minutes", "how long should i exercise",
             "minutes a day", "150", "minutes a week", "a week",
             "per week", "times a week", "days a week", "enough", "steps", "how many steps",
             "10000", "10,000", "get back into", "havent exercised", "have not exercised",
             "unfit", "beginner", "start exercising", "rest day", "rest days",
             "dog", "dogs", "puppy", "puppies", "cat", "cats", "kitten", "horse", "rabbit",
             "guitar", "piano", "practise", "practice", "revision", "revise", "study")),

entry("home-gym-kit",
      (("home gym", "kettlebell", "kettlebells", "dumbbell", "dumbbells", "resistance band",
        "resistance bands", "barbell", "pull up bar", "pull-up bar", "bench", "weights",
        "gym equipment", "gym kit"),
       ("budget", "cheap", "cheaper", "buy", "buying", "bought", "need", "worth", "best",
        "which", "start", "starting", "small space", "flat", "set up",
        "get started", "first")),
      "Buy one adjustable dumbbell or one kettlebell and nothing else to begin with: about "
      "6 to 10 kg suits most beginners and 10 to 16 kg if you are already strong, and a used "
      "one goes for £40 to £80. Add a resistance band for about £10 and a step or a sturdy "
      "chair, and that covers squats, rows, presses and carries - a mat only if your floor is "
      "hard. Skip the bench and the multi-gym until you have trained for six months, because "
      "the routine is what makes the difference, not the rack.",
      avoid=("treadmill", "rower", "spin bike", "exercise bike", "trampoline", "rent",
             "delivery", "assembly",
             "bench press", "deadlift", "squat", "squats", "lifting", "lift", "reps", "rep",
             "sets", "one rep max", "1rm", "heavier", "load", "form",
             "weight",
             "wash", "washed", "washing", "stink", "stinks", "stinks of", "smell", "smells",
             "smelly", "odour", "odor", "laundry", "sweat", "sweaty", "musty", "damp"),
      bias=1),

entry("running-load",
      (("keep getting injured", "injured again", "always injured", "injuries when i run",
        "injury when i run", "injury every time", "too much too soon", "increase my mileage",
        "increase my distance", "how much should i increase", "shin splints", "niggles"),
       ("run", "running", "mileage", "distance", "week", "again", "keep", "every time",
        "how much")),
      "It is nearly always the weekly distance going up too fast: keep the increase under "
      "about a tenth a week and hold it steady every fourth week. Run most of it easy enough "
      "to talk in full sentences, with one faster session and one longer run, and do two short "
      "strength sessions a week for calves, glutes and hips, which is what covers most running "
      "injuries. The same pain in the same spot three runs in a row is a physio visit, not a "
      "new pair of shoes.",
      avoid=("knee", "knees", "ankle", "achilles", "foot", "feet", "hip", "shoe", "shoes",
             "blister", "cramp", "side stitch"),
      bias=1),

entry("fasted-exercise",
      (("empty stomach", "fasted", "without eating", "no breakfast", "before breakfast",
        "without breakfast", "havent eaten"),
       ("exercise", "exercising", "work out", "working out", "workout", "run", "running",
        "train", "training", "gym", "cycle", "swim", "ok", "okay", "bad", "good", "fine")),
      "It is fine for anything up to about an hour: there is enough fuel stored to cover it, "
      "and it makes no difference to how much fat you burn over a day. Eat something small and "
      "mostly carbohydrate if you are going longer or harder than that, and always if you feel "
      "light-headed, because that is a sign to eat first rather than push on. Water matters "
      "more than food at that length of session.",
      avoid=("intermittent", "16:8", "5:2", "ramadan", "blood test", "operation", "surgery",
             "tablet", "medication", "insulin", "diabetes",
             "paracetamol", "ibuprofen", "nurofen", "painkiller", "painkillers", "aspirin",
             "co codamol", "co-codamol", "antibiotic", "antibiotics", "medicine", "medicines",
             "pill", "pills", "prescription", "capsule", "capsules", "dose", "mg",
             "tablet", "tablets", "medication", "insulin", "diabetes",
             "ibuprofen", "paracetamol", "aspirin", "naproxen", "painkiller", "painkillers",
             "medicine", "medicines", "antibiotic", "antibiotics", "steroid", "steroids",

             "battery", "batteries", "phone", "iphone", "android", "on charge",
             "laptop", "running out", "runs out", "ran out",
             "coffee", "tea", "caffeine", "espresso", "latte", "green tea", "drink", "drinks",
             "drinking", "milk", "juice", "smoothie", "alcohol", "wine", "beer", "banana",
             "fruit", "yoghurt", "yogurt", "porridge", "toast", "breakfast food"),
      bias=1),

entry("training-injuries",
      (("gym", "gyms", "lifting", "weights", "weight training", "workout", "workouts",
        "training", "run", "running", "runs", "jogging", "marathon", "parkrun", "squats",
        "deadlifts", "bench", "class", "classes", "exercise", "exercising"),
       ("injury", "injuries", "injured", "hurt", "hurts", "hurting", "hurt myself",
        "getting hurt", "pain", "pains", "ache", "aches", "aching", "niggles", "niggle",
        "safe", "safely", "avoid", "prevent", "prevention", "stop", "damage", "overdo",
        "overdoing", "too much", "strain")),
      "Most training injuries come from a jump in load, not bad luck: add about a tenth a week "
      "at most, to the weight or to the miles. Warm up for five minutes, take a lighter first "
      "set, and keep the form good on the last set or drop the weight - a sloppy last rep is "
      "where most of them happen. Never train through a sharp pain. If an ache lasts more than "
      "two weeks, or a joint gives way, see a physio rather than resting it for a month.",
      avoid=("how often", "how many times", "every day", "rest day", "warm up", "warmup",
             "cool down", "stretch", "stretches", "stretching", "sore after", "dom",
             "doms", "supplement", "supplements", "protein", "creatine", "how much", "cost",
             "price", "membership", "gym membership", "equipment", "kit", "shoes", "buy",
             "stopped going", "stopped training", "stopped the gym", "stop going",
             "quit", "quits", "quitting", "gave up", "give up", "packed it in",
             "cancelled", "cancels", "cancelling", "cancel my", "left the gym",
             "nose", "noses", "eye", "eyes", "loo", "toilet", "cistern", "tap", "taps", "hose",
             "sink", "drain", "plughole", "shower", "bath", "boiler", "radiator", "heater",
             "dishwasher", "washing machine", "software", "app", "apps", "programme", "program",
             "campaign", "school run", "errand run",
             "knee", "knees", "shoulder", "shoulders", "back", "backs", "achilles", "shin",
             "shins", "shin splints", "plantar", "hamstring", "hamstrings", "elbow", "elbows",
             "wrist", "wrists", "ankle", "ankles", "hip", "hips", "groin", "sciatica",
             "cramp", "cramps", "blister", "blisters", "dizzy", "faint", "chest pain",
             "slimming", "weight loss", "lose weight", "losing weight", "lost weight",
             "lose the weight", "losing the weight", "lose a stone", "lose some weight",
             "lose a few pounds", "lose fat", "losing fat", "dropping weight",
             "self harm", "self-harm", "kill myself", "cut myself", "want to die", "end it all",
             "end my life", "suicide", "suicidal", "not be here anymore",
             "toilet", "toilets", "loo", "loos", "cistern", "cisterns", "flush", "flushes",
             "flushing", "flush button", "ball valve", "fill valve", "flush valve", "tap",
             "taps", "faucet", "sink", "sinks", "drain", "drains", "plughole", "radiator",
             "radiators", "boiler", "washing machine", "dishwasher", "shower", "bath",
             "overflow", "overflowing", "pipes", "pipework"),
      guard=lambda u: not _the_hurt_already_happened(u)),
]

_ALREADY_HURT = re.compile(
    r"\b(?:i|ive|i've|i have|he|she|we|they)\s+(?:have\s+|has\s+|had\s+|got\s+|just\s+)?"
    r"(?:hurt|injured)\b")


def _the_hurt_already_happened(understood):
    reading = understood if isinstance(understood, dict) else {}
    line = " ".join(str(reading.get("clean") or reading.get("text") or "").lower().split())
    return bool(_ALREADY_HURT.search(line))
