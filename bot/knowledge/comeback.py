
import re

from .lookup import entry

ANSWERS = ("fitness", "sport")

RETURN_WORDS = ("again", "back on the bike", "back on my bike", "back on a bike",
                "back in the saddle", "restart", "restarting", "used to", "out of the habit",
                "lapsed", "years off", "havent", "haven't", "not run", "not ridden",
                "not cycled", "stopped running", "stopped cycling", "stopped jogging")

ILL_OR_HURT = ("ill", "illness", "sick", "sickness", "flu", "fever", "cold", "cough", "virus",
               "bug", "infection", "temperature", "chest", "hospital", "operation", "surgery",
               "hurt", "hurts", "hurting", "pain", "painful", "injury", "injured", "injuries",
               "sprain", "sprained", "tweak", "tweaked", "pulled", "knee", "knees", "shin",
               "ankle", "calf", "achilles", "back pain", "physio", "gp", "doctor", "pregnant",
               "pregnancy", "after the baby", "postnatal",
               "fracture", "fractured", "broken bone", "broken foot", "broken leg",
               "broken ankle")

RUNS_BUT_IS_NOT_YOU = (
    "toilet", "loo", "loos", "lav", "lavatory", "wc", "bog", "cistern", "flush", "ballcock",
    "faucet", "sink", "drain", "plughole",
    "shower", "hose", "sprinkler", "irrigation", "boiler", "radiator", "heater",
    "aircon", "air conditioning", "fridge", "freezer", "dishwasher", "washing machine",
    "tumble dryer", "hoover", "vacuum", "dyson", "generator", "compressor",
    "app", "apps", "software", "update", "updates", "computer", "laptop", "phone",
    "tablet", "printer", "clock", "meter", "nose", "mascara", "makeup", "paint", "ink",
    "glue", "candle", "campaign",
    "school run", "school runs", "nursery run", "errand run", "errand runs",
    "supermarket run", "shop run", "banks run")

TEAM_SPORTS = ("football", "rugby", "netball", "hockey", "basketball", "soccer", "gaelic",
               "lacrosse", "cricket", "squash", "badminton", "five a side", "5 a side",
               "tennis", "table tennis", "ping pong", "padel", "volleyball", "rounders",
               "softball", "baseball", "handball", "racketball", "racquetball")
TEAM_RETURN_WORDS = RETURN_WORDS + ("play again", "playing again", "playing football again",
                                    "play football again", "back playing", "back to training",
                                    "training again", "back on the pitch", "back on the field",
                                    "take up", "take it up", "took up", "took it up", "pick it up", "pick up a racket",
                                    "havent played", "haven't played", "not played",
                                    "stopped playing", "since school", "since i was",
                                    "when i was", "back to playing", "start playing again")
CLUB_SEARCH = ("club", "clubs", "join", "joining", "near me", "taster", "trial", "trials",
               "where can i", "find a team", "find a club", "local team", "local club",
               "watch", "watching", "ticket", "tickets", "on telly", "sky sports", "fixture",
               "fixtures", "league table", "how much", "price", "cost")


_FIRST_PERSON_WITHOUT_THE_PRONOUN = re.compile(
    r"\b(?:want|wants|wanting|used to|thinking (?:of|about)|hoping to|planning to|trying to|"
    r"decided to|going to start|back in|back on|took (?:it )?up|picked (?:it )?up|"
    r"started playing|havent|haven't|not played|since school|since college|since uni|"
    r"years off|out of the habit|lapsed)\b")

A_CHILD = re.compile(r"\b(?:kids?|child|children|toddler|son|daughter|under-?\d+|junior|schoolboy|schoolgirl)\b")
MY_OWN_CHILDHOOD = re.compile(
    r"\b(?:since|when|as) i was (?:a )?(?:kid|young|little|small|a boy|a girl|\d+)")


_A_RETURN_WORD = ("again", "back", "used to", "since", "havent", "haven't", "not played",
                  "stopped", "years off", "out of the habit", "lapsed", "restart",
                  "any more", "no longer")


def _a_return_to_team_sport(reading):
    reading = reading or {}
    said = " ".join(str(reading.get("clean") or reading.get("text") or "").split()).lower()
    if not said:
        return False
    if any(word in said for word in CLUB_SEARCH):
        return False
    if A_CHILD.search(said) and not MY_OWN_CHILDHOOD.search(said):
        return False
    if not any(word in said for word in _A_RETURN_WORD):
        return False
    if re.search(r"\b(?:i|im|i'm|ive|i've|we|my)\b", said):
        return True
    return bool(_FIRST_PERSON_WITHOUT_THE_PRONOUN.search(said))


ENTRIES = [
entry("running-again",
      (("running", "run", "jogging", "jog", "5k", "10k", "parkrun", "treadmill"),
       ("again", "back", "back into", "start", "starting", "restart", "restarting", "used to",
        "stopped running", "stop running", "havent run", "haven't run", "not run", "years",
        "years off", "out of the habit", "lapsed", "return", "take it up", "got back",
        "running again", "run again", "jog again", "shoes", "kit")),
      "Come back at about half of what you used to do: run-walk to start, one minute of easy "
      "jogging to two of walking, twenty minutes, three times a week, and add a minute of running "
      "a week for six weeks before you think about pace. Keep every run slow enough to talk, take "
      "a day off between them, and expect the first fortnight to feel harder than the numbers "
      "say. Sort the shoes first if yours have been in a cupboard for years - worn-out cushioning "
      "is what makes a comeback hurt.",
      bias=5,
      ask=RETURN_WORDS,
      avoid=ILL_OR_HURT + RUNS_BUT_IS_NOT_YOU +
      ("bath", "tap", "water", "engine", "car", "bus", "train", "late",
             "business", "shop", "errand", "machine", "ballot",
             "class", "course", "club", "parkrun time", "marathon", "half",
             "plan", "training plan", "couch to 5k", "dog", "child", "kids")),

entry("cycling-again",
      (("cycling", "cycle", "bike", "bicycle", "pushbike", "riding"),
       ("again", "back", "back into", "start", "starting", "restart", "restarting", "used to",
        "stopped cycling", "stop cycling", "havent ridden", "haven't ridden", "not ridden",
        "not cycled", "years", "years off", "out of the habit", "lapsed", "return",
        "take it up", "got back", "cycling again", "ride again", "get back on")),
      "Ride less than you think: twenty to thirty minutes on a flat, quiet route, every other "
      "day, and add about ten minutes a week rather than going for the ride you used to do. Give "
      "the bike ten minutes first - tyres pumped hard, brakes that stop it, a chain with a drop of "
      "oil - and set the saddle so your knee is almost straight at the bottom of the pedal, "
      "because a saddle too low is what makes a first ride hurt. Stay in an easy gear and spin "
      "rather than push.",
      bias=5,
      ask=RETURN_WORDS,
      avoid=ILL_OR_HURT +
      ("period", "periods", "menstrual", "monthly", "cycle day", "ovulation", "wash cycle",
             "washing machine", "dishwasher", "spin class", "motorbike", "motorcycle",
             "scooter", "moped", "engine", "puncture", "chain came off", "brakes squeal",
             "gears slip", "fix my bike", "how much is a bike", "which bike", "buy a bike",
             "child", "kids", "toddler", "balance bike",
             "processor", "cpu", "gpu", "chip", "chips", "ryzen", "intel", "graphics",
             "motherboard", "ram", "memory", "ssd", "hard drive", "charge cycle", "duty cycle",
             "life cycle", "product cycle", "menstrual cycle")),
entry("team-sport-again", (TEAM_SPORTS, TEAM_RETURN_WORDS),
      "Fitness and touch come back at different speeds, and it is the second one that gets people "
      "hurt. Train twice a week for a fortnight before you play any match at all, then a half, "
      "then a full one - about six weeks from the first session to playing as you did. If it was "
      "an injury that stopped you, the date is the physio's and not the calendar's: the usual guide "
      "is a week of easy training for every week you were out, and nothing at match pace until you "
      "can sprint and turn without thinking about it.",
      ask=TEAM_RETURN_WORDS,
      bias=5,
      guard=_a_return_to_team_sport,
      avoid=ILL_OR_HURT + CLUB_SEARCH +
      ("playstation", "xbox", "video game", "games console", "fantasy", "betting", "bet",
             "school team", "school match", "school sports day",
             "butternut", "roast", "roasted", "soup", "eat", "eaten", "eating", "cook",
             "cooked", "cooking", "recipe", "bake", "baked", "grow", "grown", "growing",
             "seeds", "chips")),
]
