import re

from bot.knowledge import cooking

ENTRIES = []

MEAT_IN_A_CARD_SWAPS = (
    (re.compile(r"\bmeat juices\b", re.I), "vegetable juices"),
    (re.compile(r"\b(?:chicken|beef|ham|turkey|lamb|pork|fish)\s+stock\b", re.I),
     "vegetable stock"),
    (re.compile(r"\b(?:chicken|beef|ham|turkey|lamb|pork)\s+stocks?\s+cubes?\b", re.I),
     "vegetable stock cubes"),
)

MEAT_OR_FISH = ("meat", "fish")


def swapped_out(text, line="", avoided=None):
    if not isinstance(text, str) or not text.strip():
        return text
    if avoided is not None and not (set(avoided) & set(MEAT_OR_FISH)):
        return text
    if cooking.PLANT_SAID.search(text):
        return text
    said_here = str(line or "").lower()
    for pattern, swap in MEAT_IN_A_CARD_SWAPS:
        if pattern.search(said_here):
            continue
        text = cooking._rewritten_outside_swaps(text, pattern, swap)
    return text
