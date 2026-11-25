from bot.knowledge.cooking import JOINT_BEEF, JOINT_PORK, _roast_joint
from bot.knowledge.lookup import entry

ANSWERS = ("cooking", "food-and-drink")

_BOTH = JOINT_BEEF + " " + JOINT_PORK

_PORK_IN_SHORT = "Pork is 30 minutes a 500g at 180C (160C fan) and 70C in the middle."


_SLOW_COOKER = (
    "A joint up to 2 kilos takes 6 to 8 hours on low, or 4 to 5 on high: stand it on a trivet or a "
    "bed of onion and carrot with 150 to 250ml of stock, and keep the lid on. Pork is done at 70C "
    "inside; a joint you want to pull wants 90C, which is another few hours on low. No crackling in "
    "a slow cooker - finish that under a hot grill.")


_WEIGHTS = ("kilo", "kilos", "kg", "kgs", "kilogram", "kilograms", "pound", "pounds")
_MEATS = ("pork", "beef", "lamb", "veal", "mutton", "ham")
_NUMBERS = ("1", "2", "3", "4", "5", "6", "7", "8", "9")
_BY_WEIGHT = (tuple(weight + " of " + meat for weight in _WEIGHTS for meat in _MEATS)
              + tuple(number + unit + " of " + meat
                      for number in _NUMBERS for unit in ("kg", "kgs", "lb", "lbs", "G")
                      for meat in _MEATS))


def _joint_by_weight(memory, understood):
    said = _roast_joint(memory, understood)
    if said == _BOTH:
        return JOINT_BEEF + " " + _PORK_IN_SHORT
    return said

_SLOW_WORDS = ("slow cooker", "slow cook", "slowcooker", "slow-cooker", "crockpot", "crock pot",
               "crock-pot")


def _not_a_gammon_in_the_oven(understood):
    words = " ".join(str(w) for w in (understood.get("words") or []))
    if "gammon" not in words:
        return True
    return any(phrase in words for phrase in _SLOW_WORDS)


def _joint_time(memory, understood):
    words = " ".join(str(w) for w in (understood.get("words") or []))
    if any(phrase in words for phrase in _SLOW_WORDS):
        return _SLOW_COOKER
    return _joint_by_weight(memory, understood)


ENTRIES = [
    entry("joint-time",
          (("joint", "gammon", "ham") + _BY_WEIGHT,
           ("how long", "time", "roast", "roasting", "oven", "temperature", "cook", "cooking",
            "minutes", "done", "kilos", "kilo", "kg", "kgs", "pounds", "pound", "lbs",
            "slow cooker", "slow cook", "slowcooker", "slow-cooker", "crockpot", "crock pot",
            "crock-pot")),
          _joint_time,
          avoid=(
              "joint of", "roast joint", "leg of", "shoulder of", "beef joint", "pork joint",
              "chicken", "turkey", "duck", "goose", "bird", "mince",
              "my joint", "joints hurt", "joint pain", "knee", "knees", "hip", "hips",
              "shoulder hurts", "shoulder", "shoulders", "brisket", "briskets",
              "slow roast", "slowly", "low and slow", "overnight", "pulled",
              "calorie", "calories", "kcal", "how many calories",
              "how much is", "how much are", "how much does a kilo", "price", "prices",
              "cost", "costs", "per kilo", "a kilo cost", "cheapest", "cheaper", "offer",
              "on offer", "supermarket", "butcher charge",
              "defrost", "defrosting", "thaw", "thawing", "frozen", "freeze", "freezer",
              "from frozen", "rest", "resting", "rests", "rested", "keep", "keeps", "keeping",
              "fridge", "ice", "icing", "heal", "healing", "heals", "recover", "recovery"),
          guard=_not_a_gammon_in_the_oven),
]
