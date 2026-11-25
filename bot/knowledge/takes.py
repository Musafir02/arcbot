from .lookup import entry as _entry

_ASK = ("how long", "how soon", "how many minutes", "how many hours", "how many days",
        "how many weeks", "how many months", "how much longer", "how much time",
        "how long till", "how long until")


def _typed(*words):
    flat = []
    for word in words:
        if isinstance(word, (tuple, list)):
            flat.extend(word)
        else:
            flat.append(word)

    def guard(understood):
        said = str(understood.get("clean") or understood.get("text") or "").lower()
        return any(word in said for word in flat)
    return guard


def _asks_a_length(text):
    low = str(text).lower()
    return any(part in low for part in _ASK)


_COAT_FINISHES = (
    ("varnish",
     ("varnish", "varnishing", "varnished", "polyurethane", "lacquer", "varnish coats",
      "coat of varnish", "coats of varnish"),
     "Two coats, four to six hours apart for a water-based varnish - and 8 to 24 hours for an "
     "oil-based polyurethane, which is what most furniture varnish is, so read the tin before the "
     "second coat. Touch it first: hard and not tacky means it is ready, and a second coat on a "
     "tacky surface drags the first about."),
    ("wood-stain",
     ("wood stain", "woodstain", "woodstain coats", "stain", "staining", "stained",
      "stain coats", "coats of stain", "coat of stain"),
     "One coat of wood stain is usually enough on new wood and two on anything that has gone "
     "grey, and a second coat goes on after four to six hours - sooner than that and it lifts the "
     "first. Wipe off the excess before it dries, because stain that pools sets patchy."),
    ("oil-finish",
     ("danish oil", "teak oil", "tung oil", "linseed oil", "boiled linseed oil", "wood oil",
      "hardwax oil", "oil finish", "oak oil"),
     "Two or three coats, 8 to 24 hours apart for a danish, teak, tung or linseed oil - thin "
     "coats, the excess wiped off after half an hour, and the tin's own figure wins. It is dry to "
     "the touch in a few hours but not ready for the next coat, and an oil finish soaks into bare "
     "wood rather than sitting on it as a film."),
    ("gloss",
     ("gloss", "gloss paint", "eggshell", "satin", "satinwood", "undercoat", "oil based",
      "oil-based", "coat of gloss", "coats of gloss"),
     "Two coats of gloss over an undercoat, a night apart: gloss, eggshell, satin and anything "
     "oil-based want 16 hours or more, so a door or a skirting board is a two-day job. Rub it down "
     "lightly between coats so the second one grips."),
)

_A_FINISH_NAMED = tuple(word for _finish, words, _said in _COAT_FINISHES for word in words)

_COAT_ASK = _ASK + ("how many coats", "how many coats of")

ANSWERS = ("cars", "home-and-diy", "cooking", "food-and-drink", "health", "fitness",
           "technology", "sport", "friends-and-relationships")

ENTRIES = [
    _entry("mot-takes",
           key=(("mot", "the mot", "an mot", "mot test"), ("take", "takes", "taking")),
           ask=_ASK,
           guard=_typed(("mot",)),
           shape=(_asks_a_length,),
           reply="The test itself takes 45 minutes to an hour, and a retest about 20 minutes. "
                 "Stay at the garage if you can, because the tester can show you the fail on the "
                 "ramp, and you can drive it home afterwards unless the fail sheet says dangerous.",
           avoid=("last", "lasts", "lasting", "valid", "validity", "yearly", "annually",
                  "how often", "every year", "expire", "fail sheet", "retake"),
           bias=2),
    _entry("driving-test-takes",
           key=(("driving test", "practical driving test", "practical test"),
                ("how long", "long", "take", "takes", "taking")),
           ask=_ASK,
           guard=_typed(("driving test", "practical test")),
           shape=(_asks_a_length,),
           reply="The test itself is about 40 minutes of driving, and the whole appointment "
                 "about an hour with the eyesight check and the show-me questions first. The "
                 "examiner tells you the result before you leave, so you are not waiting for it.",
           avoid=("book", "booking", "cancel", "cost", "price", "how much", "theory", "passed",
                  "pass", "fail", "failed", "nervous", "next week", "tomorrow", "on the 14th",
                  "how do i", "how can i"),
           bias=2),
    _entry("kitchen-renovation-takes",
           key=("kitchen renovation", "kitchen refit", "renovation", "refit"),
           ask=_ASK,
           guard=_typed(("renovation", "refit")),
           shape=(_asks_a_length,),
           reply="Six to ten weeks on site for a kitchen once the units arrive, and three to "
                 "five for a bathroom. The units are the long wait - order them six to eight "
                 "weeks before you want the work done - so work the order date back from the day "
                 "you want it finished.",
           avoid=("cost", "price", "how much", "cheaper", "quote", "quotes", "budget", "save",
                  "myself", "yourself", "diy"),
           bias=2),
    _entry("paint-between-coats",
           key=("between coats", "coats of paint", "second coat", "next coat", "recoat",
                "painting take"),
           ask=_ASK,
           guard=_typed(("coat", "recoat", "paint", "varnish", "stain", "staining")),
           shape=(_asks_a_length,),
           reply="Two to four hours between coats of emulsion, and a full day before you push "
                 "furniture back against it. Gloss and anything oil-based want overnight, wood "
                 "stain and water-based varnish four to six hours, and an oil-based varnish 8 to "
                 "24. Touch it first: hard and not tacky means it is ready, and the tin wins "
                 "where it disagrees.",
           avoid=_A_FINISH_NAMED,
           bias=2),
    _entry("charge-a-phone-takes",
           key=("charge my phone", "charge a phone", "charge the phone", "charge my iphone",
                "charging my phone", "charging a phone", "charging the phone", "charge my mobile",
                "charge my tablet", "charge my laptop", "charge a laptop", "charge a tablet",
                "charging a laptop", "phone charge", "charging time", "charge it up",
                "charge up my phone"),
           ask=_ASK,
           guard=_typed(("charge", "charging")),
           shape=(_asks_a_length,),
           reply="An hour and a half to two hours takes a phone, tablet or laptop from nearly "
                 "flat to full, and half an hour on a fast charger gets you about half way. "
                 "Overnight is fine - a modern one stops charging at 100% - but heat is what ages "
                 "a battery, so take it out of a thick case and off the radiator.",
           avoid=("not charging", "wont charge", "will not charge", "draining", "drains", "hot",
                  "warm", "cable", "charger", "battery health", "overnight", "yesterday"),
           bias=2),

    _entry("defrost-a-chicken-takes",
           key=("defrost a chicken", "defrost the chicken", "defrosting a chicken",
                "defrost chicken", "thaw a chicken", "thawing a chicken", "defrost a turkey",
                "defrost a bird", "frozen chicken", "defrost meat", "defrost mince",
                "defrost fish", "defrosting meat"),
           ask=_ASK,
           guard=_typed(("defrost", "thaw", "frozen")),
           shape=(_asks_a_length,),
           reply="A whole chicken takes about 24 hours in the fridge, pieces take 8 to 12, and a "
                 "turkey two to three days. Keep it on the bottom shelf in a bowl, and never "
                 "defrost meat on the worktop or in the sink - the outside warms long before the "
                 "middle.",
           avoid=("cook", "cooking", "roast", "oven", "microwave", "how do i", "how does",
                  "safe", "went warm", "left out"),
           bias=2),

    _entry("after-a-filling-takes",
           key=("after a filling", "after my filling", "after the filling",
                "after a tooth filling", "after a dental filling", "after an extraction",
                "after a tooth out", "numb after a filling", "numbness after a filling"),
           ask=_ASK,
           guard=_typed(("filling", "extraction")),
           shape=(_asks_a_length,),
           reply="An hour to three hours, until the numbness has gone - after that you can eat, "
                 "though keep to soft, cool food for the rest of the day. Chewing a hot or hard "
                 "meal while you are still numb is how people bite their cheek or burn their "
                 "mouth.",
           bias=2),
    _entry("a-bruise-takes",
           key=("bruise heal", "a bruise take", "bruises take", "bruise last", "bruising take",
                "black eye take", "bruise fade"),
           ask=_ASK,
           guard=_typed(("bruise", "black eye")),
           shape=(_asks_a_length,),
           reply="One to two weeks for a bruise to fade, going purple, then green, then yellow "
                 "as the blood is cleared. A cold pack for 20 minutes at a time over the first "
                 "day keeps it smaller, and a bruise that turns up with no knock behind it, or "
                 "that you keep getting, is worth a blood test.",
           bias=2),
    _entry("swimming-after-eating-takes",
           key=("swimming after eating", "swim after eating", "swim after lunch",
                "swim after a meal", "swimming after a meal", "after eating before swimming",
                "before swimming"),
           ask=_ASK,
           guard=_typed(("swim", "swimming")),
           shape=(_asks_a_length,),
           reply="About half an hour after a big meal, and no wait at all after a snack: the "
                 "cramp rule comes from one small study and the evidence does not back it up. "
                 "Keep out of deep water if you have been drinking, and don't swim on a stomach "
                 "that feels too full.",
           bias=2),

    _entry("learn-to-swim-takes",
           key=(("learn to swim", "learning to swim", "learn swimming", "swim lessons",
                 "swimming lessons", "adult swimming lessons", "lessons to swim", "swim a length",
                 "swim 25 metres"),
                ("how long", "long", "take", "takes", "taking", "till", "until")),
           ask=_ASK,
           guard=_typed(("swim", "swimming")),
           shape=(_asks_a_length,),
           reply="Most adults go from nervous to swimming a length in one course of weekly "
                 "lessons, which is 10 to 12 weeks. Swimming 25 metres without stopping takes a "
                 "term, and two terms if you are frightened of the water - lessons twice a week "
                 "get there faster than once a week, because the water stops feeling strange.",
           avoid=("toddler", "baby", "child", "children", "kid", "kids", "son", "daughter",
                  "year old", "years old", "school", "nursery"),
           bias=2),
    _entry("swim-a-mile-takes",
           key=(("swim a mile", "swim one mile", "swim 1 mile", "swim a kilometre",
                 "swim 1600m", "swim a km"), ("how long", "take", "takes", "taking")),
           ask=_ASK,
           guard=_typed(("swim", "mile", "kilometre", "km")),
           shape=(_asks_a_length,),
           reply="A steady front crawl does a mile - 64 lengths of a 25m pool - in about 30 to "
                 "40 minutes. Breaststroke, or a first season of swimming, is 45 minutes to an "
                 "hour, and building up 200m at a time gets there better than trying the mile "
                 "straight away.",
           bias=2),
    _entry("get-over-a-breakup-takes",
           key=("get over a breakup", "get over a break up", "over a breakup", "get over my ex",
                "get over him", "get over her", "broken heart", "breakup", "break up",
                "end of a relationship"),
           ask=_ASK,
           guard=_typed(("breakup", "break up", "break-up", "ex", "relationship", "broken heart")),
           shape=(_asks_a_length,),
           reply="The sharpest part is usually six to eight weeks, and most people feel like "
                 "themselves again in three to six months. It does not go in a straight line - a "
                 "bad day at three months is not a relapse - and seeing people on the days you "
                 "least want to is what makes the weeks go faster.",
           avoid=("bereav", "died", "passed away", "funeral", "grief", "widow", "lost my"),
           bias=2),
    _entry("a-hair-mask-takes",
           key=("leave a hair mask on", "leave a mask on", "leave the mask on",
                "leave a hair mask", "hair mask on", "hair masks on", "hair mask for",
                "hair mask in", "deep conditioning mask"),
           ask=_ASK,
           guard=_typed(("mask",)),
           shape=(_asks_a_length,),
           reply="10 to 20 minutes is all a hair mask needs, and the label's own time is the one "
                 "to follow. Longer adds nothing - hair can only take so much - and a warm towel "
                 "wrapped round it does more than another ten minutes.",
           avoid=("last", "lasts", "expire", "shelf life", "go off", "gone off", "keep"),
           bias=2),
]

for _finish, _words, _said in _COAT_FINISHES:
    ENTRIES.append(_entry("between-coats-of-" + _finish,
                          key=(_words,
                               ("between coats", "coats", "coat", "second coat", "next coat",
                                "recoat")),
                          ask=_COAT_ASK,
                          guard=_typed(_words),
                          shape=(_asks_a_length,),
                          reply=_said,
                          bias=3))
