import re

from . import pick

GOOD = (r"lovely|beautiful|gorgeous|brilliant|great|wonderful|fantastic|perfect|cracking|"
        r"smashing|nice|amazing|glorious|grand|super|fab|stunning|lush|decent")

THING = r"[a-z][a-z' -]{0,24}"

OUTSIDE = frozenset(("day", "morning", "afternoon", "evening", "weather", "sun", "sunshine",
                     "sky", "view", "sunset", "sunrise", "night", "light", "breeze"))

NOT_GOOD = frozenset("""
mess shame pity nightmare waste disaster worry state pain fuss palaver joke
""".split())

WHAT_A = re.compile(r"^(?:oh|ah|wow|ooh)[,\s]+what a\s+(?:" + GOOD + r")\s+(?P<thing>" + THING +
                    r")$|^(?:what|such) a\s+(?:" + GOOD + r")\s+(?P<thing2>" + THING + r")$")
RELIEF_LINE = re.compile(r"^(?:what|such) a (?:relief|weight off|load off)$|^that'?s? a relief$")
RESULT_LINE = re.compile(r"^(?:what|such) a (?:result|win|good result|great result)$")
NEWS_LINE = re.compile(r"^(?:lovely|great|wonderful|brilliant|smashing|nice) news$")

PLEASED = (
    "Good to hear. What are you up to today?",
    "Nice one. Make the most of it - what's the plan?",
    "That's good. Tell me about it.",
)
OUT_IN_IT = (
    "Good to hear. Are you getting out in it?",
    "Lovely. What are you up to today?",
    "That's the kind of day to be outside. What's the plan?",
)
RELIEF = (
    "That's a weight off. What was it about?",
    "Good - that's the end of it, then. What changed?",
    "Phew. What was it in the end?",
)
NEWS = (
    "Good news. What is it?",
    "Nice one. Tell me.",
    "Lovely. What's happened?",
)
RESULT = (
    "Good result. What was it for?",
    "Nice one. Tell me how it went.",
    "That's a good one. What happened?",
)


def _thing(match):
    return (match.group("thing") or match.group("thing2") or "").strip()


def answer_for(text, memory=None):
    line = " ".join((text or "").lower().split()).rstrip(" .!,;:")
    if not line or len(line.split()) > 6:
        return None
    if "?" in line:
        return None
    if RELIEF_LINE.match(line):
        return pick(list(RELIEF), memory or {}, line)
    if RESULT_LINE.match(line):
        return pick(list(RESULT), memory or {}, line)
    if NEWS_LINE.match(line):
        return pick(list(NEWS), memory or {}, line)
    match = WHAT_A.match(line)
    if not match:
        return None
    thing = _thing(match)
    words = set(thing.split())
    if not thing or words & NOT_GOOD:
        return None
    pool = OUT_IN_IT if words & OUTSIDE else PLEASED
    return pick(list(pool), memory or {}, line)
