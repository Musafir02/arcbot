import re

A_DAY_WEIGHED = re.compile(
    r"\b(?:too|warm enough|mild enough|dry enough|cold enough|good enough)\s+"
    r"(?:hot|cold|wet|windy|warm|cool|dry|muggy|humid)?\s*(?:to|for)\s+"
    r"(?:go\s+)?(?:run|running|walk|walking|cycle|cycling|jog|jogging|hike|hiking|"
    r"play|playing|gardening|garden|barbecue|bbq|swim|swimming|paint|painting|"
    r"the\s+dog|a\s+run|a\s+walk|the\s+wash)\b", re.I)
A_DAY_ASKED = re.compile(
    r"\b(?:is|will|would|should)\s+it\s+(?:be\s+)?(?:too\s+|warm\s+enough|dry\s+enough|"
    r"cold\s+enough|nice\s+enough\s+)?(?:hot|cold|wet|windy|warm|muggy|cool|dry)\b"
    r"(?:\s+(?:out|outside|today|tomorrow|later|this\s+\w+))?\s*\??\s*$", re.I)

TOO_HOT = (
    "What is too hot is personal, but the thing that catches people out is the muggy air rather "
    "than the number: above the mid twenties with no breeze, go early or go shorter, and take water "
    "even if you do not feel like it. A weather app has today's figure and the humidity - what time "
    "were you thinking of going?",
    "Heat is judged on the air as well as the temperature: still, humid and in the sun is a lot "
    "harder than the same number with a breeze. If it is close or over about 25 the answer is "
    "early, shorter, and water. The app will have the figure for today - morning or evening for "
    "you?",
)

TOO_COLD = (
    "Cold is the easier one to get wrong: it is wind and wet that turn a cold day into a bad one, "
    "and a dry still frost is fine walking weather once you are moving. Two thin layers and "
    "something for your ears beat one thick coat. The app will have today's wind chill - how long "
    "are you out for?",
    "What decides a cold day is the wind, not the number: the same 3 degrees is fine in a still "
    "street and bitter on a hill. Layers you can open when you warm up, and gloves even when it "
    "does not look like it. A weather app has the wind chill for today.",
)

A_COLD_DAY = re.compile(r"\b(?:cold|freezing|chilly|frost\w*|ice|icy|snow\w*|wind\w*|gale\w*|blowing)\b", re.I)

POOLS = (TOO_HOT, TOO_COLD)


def for_the_ask(clean, repaired=None):
    for line in (clean, repaired):
        said = str(line or "")
        if not said:
            continue
        if A_DAY_WEIGHED.search(said) or A_DAY_ASKED.search(said.strip()):
            return TOO_COLD if A_COLD_DAY.search(said) else TOO_HOT
    return None
