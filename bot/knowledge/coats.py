import re

from .lookup import entry

ANSWERS = ("home-and-diy", "shopping", "nature-and-weather")

OUT_WHEN = ("today", "tonight", "tomorrow", "this morning", "this afternoon", "this evening",
            "in the morning", "in the afternoon", "in the evening", "right now", "later",
            "later on", "out", "outside", "weather", "forecast", "cold out", "chilly out",
            "warm out", "raining", "rain today", "enough", "the weekend",
            "this weekend", "saturday", "sunday", "monday", "tuesday", "wednesday", "thursday",
            "friday", "after work", "school run", "when i go out",
            "to work", "at work", "for work", "to school", "at school", "for school",
            "to the office", "at the office", "in the office",
            "this pm", "this am", "in the morning", "before work")

OUT_TAKE = ("Take it: being cold or wet for an hour costs you far more than carrying something "
            "you never put on, and it is the bright morning that catches people out. Read the "
            "forecast for the hours you will actually be out, because the day's high is at two "
            "in the afternoon and the cold and the showers come later; under it a thin layer you "
            "can take off is worth more than a thicker coat, and if you will be standing about "
            "after dark, that is the case for the warm one.")

_NOT_ABOUT_TODAY = ("what coat", "what jacket", "which coat", "which jacket", "should i get",
                    "should i buy", "worth it", "is it worth", "buy", "buying", "bought", "price",
                    "cheap", "expensive", "best", "recommend", "shop", "sale", "size", "fits",
                    "fit me", "too small", "too big", "outgrew", "needs a new", "need a new",
                    "a new coat", "a new jacket", "new coat", "new jacket", "brand new",
                    "zip", "zipper", "torn", "ripped", "stain", "smell", "store", "storage",
                    "put away", "moth", "wash", "clean", "repair", "waterproof it", "reproof",
                    "leak", "paint", "second coat", "coats of", "jacket potato", "potato",
                    "antivirus", "laptop", "computer", "macbook", "city break", "weekend away",
                    "holiday", "packing", "for the trip", "winter coat", "warm coat",
                    "coat thats", "coat that is", "waterproof coat", "puffer",
                    "ordered", "order", "medium", "small", "large", "arrived", "delivery",
                    "wore", "worn", "inside out", "yesterday", "all day",
                    "big enough", "long enough", "too long", "too short", "sleeves", "sleeve",
                    "shoulders", "alter", "altering", "tailor")


_OUT_WHEN = re.compile(r"\b(?:" + "|".join(re.escape(word) for word in
                                           sorted(OUT_WHEN, key=len, reverse=True)) + r")\b")


_LOST_OR_TAKEN = re.compile(
    r"\b(?:swiped|stolen|stole|nicked|robbed|burgled|pickpocket\w*|went missing|gone missing|"
    r"is missing|are missing|left (?:it|them|mine|his|hers|my|the) (?:on|in|at)|"
    r"someone took|took my|taken my|"
    r"los(?:t|ing|es) (?:his|her|their|my|our|the|it|them))\b",
    re.IGNORECASE)


_A_CLOCK = re.compile(r"\b\d{1,2}\s?(?:am|pm)\b", re.IGNORECASE)


def _a_garment_to_take(understood):
    said = " ".join(str(understood.get(key) or "") for key in ("words", "clean", "text")).lower()
    for filler in "[],'":
        said = said.replace(filler, " ")
    for word in ("how do i", "how do you", "how can i", "how to") + _NOT_ABOUT_TODAY:
        if word in said:
            return False
    if _LOST_OR_TAKEN.search(said):
        return False
    return bool(_OUT_WHEN.search(said) or _A_CLOCK.search(said))


ENTRIES = [
    entry(
        "coat-out-today",
    (("coat", "coats", "jacket", "jackets", "raincoat", "brolly", "umbrella", "umbrellas",
      "warm layer", "jumper", "fleece", "cardigan", "hat", "gloves", "scarf"),
     ("need", "take", "bring", "pack", "wear", "wearing", "put on", "should i", "do i", "will i",
      "shall i", "bother"),
     OUT_WHEN),
    OUT_TAKE,
    guard=_a_garment_to_take,
    avoid=("pram", "pushchair", "car seat", "travel system",
           "hiking", "hike", "hill", "hills", "walking", "walk", "cycling", "running",
           "football", "rugby", "match", "camping", "festival", "wedding", "funeral",
           "interview", "uniform", "suit",
           ),
    bias=2),
]
