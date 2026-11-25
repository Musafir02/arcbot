
from .lookup import entry

ANSWERS = ("cooking", "food-and-drink")

_EXERCISE = ("before a run", "before running", "before exercise", "before the gym", "for a run",
             "exercise", "gym", "workout", "stretches", "stretching", "jog", "jogging", "sprints",
             "injury", "injured", "match", "football", "netball", "training session",
             "cool down", "after a run", "muscles")

_BREADS = ("naan", "naans", "naan bread", "pitta", "pita", "pitta bread", "pita bread",
           "tortilla", "tortillas", "wrap", "wraps", "flatbread", "flat bread", "chapati",
           "chapatis", "roti", "rotis", "baguette", "french bread", "bread roll", "bread rolls",
           "rolls", "bun", "buns", "bagel", "bagels", "ciabatta", "focaccia", "garlic bread",
           "bread", "pide",
           "scone", "scones", "crumpet", "crumpets", "teacake", "teacakes",
           "pancake", "pancakes", "waffle", "waffles")

_WARM_WORDS = ("warm up", "warm", "warming", "warm through", "reheat", "reheating", "heat up",
               "hot", "hot again", "crisp", "crispy", "crisp up", "soft again", "soften",
               "fresh again", "refresh", "not cold", "cold bread", "toaster", "in the toaster",
               "in a pan", "dry pan", "toast", "toasting")

_NOT_WARMING = _EXERCISE + (
    "make", "making", "bake", "baking", "recipe", "dough", "sourdough", "yeast", "flour",
    "how long does", "keep", "keeps", "freeze", "freezing", "frozen", "stale",
    "stale bread", "bread sauce", "bread and butter pudding", "crumbs", "breadcrumbs",
    "stuffing", "make toast", "how do i make toast", "toast it", "beans on toast",
    "cheese on toast", "sandwich", "which bread",
    "healthiest",
    "gluten", "carbs", "calories", "how many calories", "buy", "best bread", "sliced",
)

_BREAD_REPLY = (
    "Splash it with a little water and give it 3 to 4 minutes in a 180C (160C fan) oven - 6 to 8 "
    "for a whole loaf - foil around it for a soft bread like naan or pitta, straight on the shelf "
    "for a crusty one. "
    "Twenty seconds in the microwave works if you eat it at once, and a wrap or pitta only "
    "wants 20 to 30 seconds a side in a dry hot pan or a toaster, with an air fryer doing the "
    "same job in 3 minutes at 160C.")

_TOASTING = frozenset(("toast", "toasting", "toaster"))
_OVEN_WORDS = frozenset(("oven", "bake", "baking", "warm", "warming", "reheat", "reheating",
                         "heat", "grill"))
_TOAST_REPLY = (
    "A toaster or a dry hot pan does it in 20 to 30 seconds a side - cut a pitta or a bagel open "
    "first, and watch it, because they go from pale to burnt in seconds. Under the grill it is a "
    "minute at most, turning once.")


def _bread_reply(memory, reading):
    words = {str(word).lower() for word in (reading.get("words") or ())}
    if words & _TOASTING and not words & _OVEN_WORDS:
        return _TOAST_REPLY
    return _BREAD_REPLY


_PASTRY = ("sausage roll", "sausage rolls", "pasty", "pastie", "pastries", "pasty", "samosa",
           "samosas", "spring roll", "spring rolls", "croissant", "croissants", "quiche",
           "quiches", "pie", "pies", "turnover", "turnovers", "pigs in blankets", "vol au vent",
           "vol au vents", "danish pastry", "pain au chocolat", "baklava", "empanada",
           "empanadas", "cornish pasty", "filo parcel", "filo parcels")

_REHEAT_WORDS = ("reheat", "reheating", "heat up", "heating up", "warm up", "warm", "hot again",
                 "cold", "microwave", "in the oven", "oven", "air fryer", "crisp", "crispy",
                 "crisp up",
                 "defrost", "defrosting", "thaw", "thawing")

_NOT_REHEATING = (
    "make", "making", "bake", "baking", "recipe", "dough", "rough puff", "shortcrust",
    "puff pastry", "filo", "pastry case", "blind bake", "blind baking", "line a tin", "roll out",
    "how long does", "keep", "keeps", "freeze", "freezing", "use by", "still ok",
    "safe to eat", "gone off", "how long can", "calories", "how many calories", "healthy",
    "buy", "where can i", "bakery", "supermarket", "filling", "what goes in",
    "base", "soggy base", "blind", "always", "how do i stop", "how do i stop that",
    "comes out",
    "mince", "steak and", "chicken pie", "apple pie", "shepherds pie", "cottage pie",
    "fish pie", "who makes",
    "how long do i cook", "how long to cook", "how long do you cook", "how long should i cook",
    "how long does it take to cook", "how long do i bake",
    "how long to bake", "how long should i bake", "how long does it take to bake",
)

_PASTRY_REPLY = (
    "Give it 8 to 10 minutes at 180C (160C fan) on a bare shelf, or 4 to 5 minutes in an air "
    "fryer at 160C, and it is hot when a skewer into the middle comes out hot. A microwave heats "
    "the middle but leaves the pastry limp, so if you use one give it 2 minutes in the oven after "
    "to crisp the outside.")

_FROM_FROZEN = frozenset(("frozen", "freezer", "defrost", "defrosting", "defrosted",
                          "from frozen", "still frozen", "thaw", "thawing", "thawed"))
_THAWING = frozenset(("defrost", "defrosting", "thaw", "thawing"))
_HEATING = frozenset(("reheat", "reheating", "heat up", "heating up", "warm up", "warm",
                      "warming", "hot again"))
_FROZEN_CLAUSE = (" From frozen it wants defrosting first - overnight in the fridge, or 25 to 30 "
                  "minutes at 160C from frozen, then the 8 to 10 minutes at 180C to crisp it.")

_DEFROST_REPLY = (
    "Defrost it overnight in the fridge - a pie or quiche on a plate on the bottom shelf, still in "
    "its packaging - then give it 8 to 10 minutes at 180C (160C fan) on a bare shelf, or 4 to 5 "
    "minutes in an air fryer at 160C, to heat the middle through and crisp the pastry. Do not "
    "defrost one on the worktop.")


def _pastry_reply(memory, reading):
    words = {str(word).lower() for word in (reading.get("words") or ())}
    text = (reading.get("clean") or "").lower()
    cold = bool(words & _FROM_FROZEN) or "frozen" in text
    if words & _THAWING and not words & _HEATING:
        return _DEFROST_REPLY
    if cold:
        return _PASTRY_REPLY + _FROZEN_CLAUSE
    return _PASTRY_REPLY


ENTRIES = (
    entry("warm-bread", (_BREADS, _WARM_WORDS), _bread_reply, avoid=_NOT_WARMING, bias=2),
    entry("reheat-pastry", (_PASTRY, _REHEAT_WORDS), _pastry_reply, avoid=_NOT_REHEATING,
          bias=2),
)
