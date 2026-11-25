import re

from .lookup import entry

ANSWERS = ("sleep", "health")

_A_BODYS_ENERGY = (
    "no energy", "energy up", "keep my energy", "keep energy", "my energy", "energy levels",
    "energy level", "more energy", "less energy", "low energy", "lack of energy",
    "energy crash", "energy dip", "energy slump", "energy drops", "energy goes",
    "energy down", "energy left", "energy back", "energy all day",
)

_IN_THE_DAY = (
    "afternoon", "afternoons", "after lunch", "after my lunch", "after eating lunch",
    "midday", "mid-afternoon", "middle of the day", "in the day", "daytime", "after work",
    "2pm", "3pm", "4pm", "3 o'clock", "2 o'clock", "4 o'clock", "post-lunch", "lunchtime",
    "every afternoon", "most afternoons", "all afternoon",
)

_THE_HOUSE = re.compile(
    r"\b(?:tariff|tariffs|economy\s*7|off-?peak|peak|kwh|kilowatt|meter|metre|reading|"
    r"bill|bills|billed|standing charge|direct debit|supplier|switch|tariffs|"
    r"electric|electricity|gas|heating|boiler|radiator|immersion|"
    r"washing machine|washer|tumble dryer|dryer|dishwasher|immersion|charge|charging|"
    r"battery|car|van|cheapest|cheaper|cheap|price|prices|cost|costs|unit rate)\b",
    re.IGNORECASE)


def _the_energy_is_the_bodys(understood):
    reading = understood or {}
    words = " ".join(str(one) for one in (reading.get("words") or ()))
    text = str(reading.get("clean") or reading.get("text") or "") or words
    return not _THE_HOUSE.search(text)


ENTRIES = [
    entry("the-afternoon-dip",
          (_A_BODYS_ENERGY, _IN_THE_DAY),
          "That dip after lunch is your body clock, not laziness or a lack of willpower, and it "
          "passes. Eat a lunch with protein and fibre rather than a big plate of white carbs, "
          "then get ten minutes of daylight and a short walk at the low point instead of another "
          "coffee. Drink water, keep the caffeine to before 2pm so it does not cost you tonight, "
          "and if you can, take a 15-minute nap rather than a long one.",
          bias=2,
          guard=_the_energy_is_the_bodys),
]
