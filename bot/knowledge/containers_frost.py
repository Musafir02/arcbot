
import re

from .lookup import entry

ANSWERS = ("garden-and-plants",)

_IN_A_POT = ("pots", "pot", "plant pots", "patio pots", "containers", "container", "tubs",
             "tub", "planters", "planter", "hanging baskets", "window boxes", "geraniums",
             "geranium", "pelargoniums", "fuchsias", "begonias", "bedding plants",
             "tender plants", "bay tree", "bay trees", "olive tree", "olive trees",
             "lemon tree", "citrus", "agapanthus", "canna", "cannas", "dahlias",
             "succulents", "houseplants", "house plants")

_THE_COLD_AND_THE_MOVE = ("frost", "frosts", "frosty", "freezing", "freeze", "cold", "cold snap",
                          "tonight", "overnight", "winter", "wintering", "snow", "minus",
                          "bring in", "bring inside", "take in", "move", "moving", "moved",
                          "leave out", "left out", "outside", "indoors", "inside", "shelter",
                          "stay out", "over winter", "in", "in for the winter")

_ASK = ("bring in", "bring them in", "bring it in", "bring inside", "bring my", "take in",
        "take them in", "move", "should i move", "leave out", "leave them out", "covered",
        "cover them", "cover my", "tonight", "overnight", "too late", "stay out",
        "over winter", "leave out", "left out", "bring my")

_HAS_ALREADY_FROZEN = re.compile(
    r"\b(?:have|has|had|got|been|is|are|was|were)\s+(?:been\s+)?(?:frozen|caught|blackened|dead)\b"
    r"|\bblackened\b|\bdead\b|\bdied\b|\bkilled\b", re.I)


def _the_night_is_still_coming(understood):
    said = ""
    if isinstance(understood, dict):
        said = str(understood.get("text") or understood.get("clean") or "")
        if not said:
            words = understood.get("words")
            said = " ".join(str(word) for word in words) if isinstance(words, (list, tuple)) else ""
    return not _HAS_ALREADY_FROZEN.search(str(said or ""))


_REPLY = ("Bring them in if you can, because a pot freezes from every side: the roots sit above the "
          "frost line, so a night that a border shrugs off can see off a plant in a tub. If they "
          "are too heavy to move, stand them together against a house wall on pot feet, wrap the "
          "pot rather than the leaves in bubble wrap or a sack, and push them under the eaves - "
          "grouping them and getting them out of the wind does most of the work. A forecast of 2C "
          "or below at ground level is the one to act on, and anything tender left out after that "
          "is worth bringing in for good.")

ENTRIES = [
    entry("a-pot-is-not-a-border",
          (_IN_A_POT, _THE_COLD_AND_THE_MOVE),
          _REPLY,
          bias=3,
          ask=_ASK,
          guard=_the_night_is_still_coming,
          avoid=("cracked", "broken", "chip", "chipped", "glaze", "terracotta pot broke",
                 "repot", "repotting", "potting on", "compost", "soil", "saucepan", "casserole",
                 "slow cooker", "paint", "plant pot saucer", "buy", "price", "cheap", "where can i",
                 "allotment", "plot", "tenancy", "greenhouse heater", "heater", "paraffin")),
]
