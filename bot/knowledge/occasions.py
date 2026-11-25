import re

from bot.knowledge.geography import crosses_a_border
from bot.knowledge.lookup import entry

ANSWERS = ("cooking", "food-and-drink")

BRING_WORDS = ("bring", "brings", "bringing", "take", "takes", "taking", "make", "makes",
               "making", "cook", "cooks", "cooking", "bake", "bakes", "baking",
               "food", "foods")

BRING_ASKS = ("what can i bring", "what should i bring", "what do i bring", "what to bring",
              "anything i can bring", "shall i bring", "should i bring", "do i need to bring",
              "what can i take", "what should i take", "what do i take", "what to take",
              "shall i take", "should i take",
              "what can i make", "what should i make", "what do i make", "what to make",
              "shall i make", "should i make",
              "what can i bake", "what should i bake", "what to bake", "should i bake",
              "what can i cook", "what should i cook", "what do i cook", "what to cook",
              "shall i cook", "should i cook",
              "food for", "food to", "what food", "which food",
              "bring food", "bringing food", "bring some food", "bring a plate",
              "bring something to eat", "take food", "taking food")

BRING_DISH = (
    (("the wake", "a wake", "for the wake", "for a wake", "after the wake", "after a wake",
      "at the wake", "at a wake", "funeral", "funeral tea"),
     "Sandwiches, a big pot of soup and a traybake: food that can sit out and be eaten whenever "
     "people arrive, and that reheats for the family afterwards. Take it in a dish you do not "
     "want back, and offer one specific job - pouring tea, washing up - rather than asking what "
     "you can do."),
    (("picnic", "picnics"),
     "Take something that survives a warm car: a frittata cut in wedges, a salad with the dressing "
     "in the bottom of the jar, or cold roast chicken with a bag of ice packs. Flapjacks and fruit "
     "travel better than anything with cream in it."),
    (("barbecue", "barbecues", "bbq", "bbqs", "barbeque", "cookout"),
     "Take something that needs nothing from the grill: a big bowl of slaw, garlic bread, or "
     "halloumi and vegetable skewers if you want something cooked. Ice and a bottle of something "
     "land harder than another bag of crisps."),
    (("potluck", "pot luck", "pot lucks", "bring and share"),
     "Take a dish that holds its heat and needs nothing at the last minute: a tray of roast "
     "vegetables, a big grain salad, or a chilli to plug in. Ask what is already coming first, so "
     "you are not the third pasta bake."),
    (("bake sale", "cake sale", "cake stall", "school fair", "summer fair", "fete", "fayre"),
     "Traybakes cut into squares travel and sell best: brownies, flapjacks or a Victoria sponge "
     "traybake. Write the allergens on a card and take a tin or a box, because a stall always runs "
     "out of somewhere to put things."),
    (("buffet", "buffets", "christening", "christenings", "hen do", "leaving do", "retirement do",
      "naming ceremony", "leaving party", "retirement party"),
     "Cold things that hold for an hour and need no oven: cheese straws, mini quiches, cocktail "
     "sausages, hummus with breadsticks, and a bowl of something green. Two hot trays are plenty, "
     "and everything else can be made the day before."),
    (("dinner party", "dinner parties", "friends house", "friends place", "friend house",
      "their house", "round for dinner", "over for dinner", "for dinner at", "for dinner"),
     "Take a bottle and something for after - a pudding, cheese and biscuits, or a box of "
     "chocolates - so you are not competing for their oven. Ask what they are cooking, then bring "
     "the thing that goes with it."),
)

BRING_HOST_NAMES = ("dinner party", "dinner parties", "friends house", "friends place",
                    "friend house", "their house", "round for dinner", "over for dinner",
                    "for dinner at", "for dinner")
BRING_CARRY_WORDS = ("bring", "brings", "bringing", "take", "takes", "taking",
                     "made", "bought", "picked", "ordered")

BRING_GUESTS = ("take my friend", "bring my friend", "my friend to", "my friend along",
                "my friend come", "bring a friend", "take a friend", "my friend with me",
                "take my partner", "bring my partner", "my partner to", "my partner along",
                "take my husband", "bring my husband", "take my wife", "bring my wife",
                "take my mum", "bring my mum", "take my mother", "bring my mother",
                "take my dad", "bring my dad", "take my father", "bring my father",
                "take my parents", "bring my parents")

_TRIP = ("beach", "the beach", "road trip", "the park", "park", "walk in the woods", "the woods",
         "mountain", "mountains", "hike", "hiking", "rambling", "long walk", "walk", "camping",
         "campsite", "campervan", "caravan", "day out", "day trip", "journey", "for the journey",
         "car journey", "train journey", "wild swim", "on the river", "up a hill")

BRING_NOT_FOOD = (("my dog", "the dog", "our dog", "my cat", "the cat", "my baby",
                   "the baby", "our baby", "my kids", "my children", "my son", "my daughter",
                   "wheelchair", "buggy", "pushchair", "pram", "car seat",
                   "my phone", "my laptop", "my camera")
                  + BRING_GUESTS + _TRIP)

_NOT_A_DISH = ("how much", "how many", "how often", "how long")

_HOST_OWN = ("im hosting", "i'm hosting", "we're hosting", "were hosting", "im having",
             "i'm having", "we're having", "were having", "im throwing", "i'm throwing",
             "im putting on", "i'm putting on", "im organising", "i'm organising",
             "im organizing", "i'm organizing", "hosting a", "hosting an")

_MAKE_ASKS = ("shall i make", "should i make", "shall i cook", "should i cook",
              "can i make", "should i bake", "shall i bake")
_COOKING_ASKS = _MAKE_ASKS + ("can i cook", "to cook for", "to make for", "to bake for",
                              "should i cook for", "what should i cook", "what can i cook",
                              "what to cook", "what should i make", "what can i make",
                              "what to make")
_SPREAD_WORDS = ("tea", "spread", "buffet", "lunch", "dinner", "supper", "brunch")


def _same(word, wanted):
    word = str(word).lower().strip("'")
    wanted = str(wanted).lower()
    if word == wanted:
        return True
    return word in (wanted + "s", wanted + "es") or wanted in (word + "s", word + "es")


def _words_of(understood):
    said = understood.get("words") or []
    if not isinstance(said, list):
        said = str(said).split()
    clean = str(understood.get("clean") or "")
    return re.findall(r"[a-z0-9']+", (" ".join(str(word).lower() for word in said) + " "
                                      + clean.lower()))


def what_to_bring(memory, understood):
    clean = str(understood.get("clean") or "").lower()
    if any(phrase in clean for phrase in _NOT_A_DISH):
        return None
    words = _words_of(understood)
    if any(phrase in clean for phrase in _HOST_OWN):
        return None
    if (any(phrase in clean for phrase in _MAKE_ASKS)
            and any(phrase in clean.split() for phrase in _SPREAD_WORDS)
            and not any(_same(word, carry_word) for word in words
                        for carry_word in ("bring", "take"))):
        return None
    carry = any(_same(word, carry_word) for word in words for carry_word in BRING_CARRY_WORDS)
    if str(understood.get("wants") or "") == "place":
        return None
    asker = any(phrase in clean for phrase in BRING_ASKS)
    if any(phrase in clean for phrase in _COOKING_ASKS) and not carry:
        return None
    for names, hint in BRING_DISH:
        for name in names:
            if name in BRING_HOST_NAMES and not carry:
                continue
            parts = name.split()
            for start in range(len(words) - len(parts) + 1):
                if all(_same(words[start + offset], parts[offset])
                       for offset in range(len(parts))):
                    return hint
    if (asker and not crosses_a_border(clean)
            and not any(phrase in clean for phrase in _NOT_A_DISH_TO_CARRY + _TRIP)):
        if any(_same(word, food) for word in words for food in GENERIC_FOOD):
            return _ANY_DISH
    return None


GENERIC_FOOD = ("food", "foods", "dish", "dishes", "plate", "plates", "something to eat")

_NOT_A_DISH_TO_CARRY = ("birthday", "birthdays", "housewarming", "house warming", "engagement",
                        "baby shower", "wedding", "christening present", "present", "presents",
                        "gift", "gifts", "interview", "work", "office", "fridge", "freezer",
                        "on the plane", "on a plane", "flight",
                        "through security", "hand luggage", "cabin bag",
                        "restaurant", "restaurants", "cafe", "cafes", "the pub", "takeaway",
                        "ferry", "on the ferry", "on a ferry", "on the train", "on a train",
                        "on the coach", "on the bus")

_ANY_DISH = ("Take something that needs nothing from anyone else's kitchen: a big bowl of pasta "
             "salad, a tray of sausages or a quiche, cheese and crackers, or a traybake cut into "
             "squares. Nothing with cream in it if it will sit out, and take it in a dish you do "
             "not need back. If the host says not to bring anything, take a bottle or something "
             "for after - and ask what is already coming so you are not the third pasta bake.")

OCCASION_NAMES = tuple(name for names, _hint in BRING_DISH for name in names) + GENERIC_FOOD

ENTRIES = [
    entry("bring-dish", (BRING_WORDS, OCCASION_NAMES), what_to_bring, ask=BRING_ASKS,
          avoid=BRING_NOT_FOOD, bias=1),
]
