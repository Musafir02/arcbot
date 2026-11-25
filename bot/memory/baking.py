
import re

NAMED_BAKES = re.compile(r"\b(?:lemon|orange)\s+drizzle\b", re.I)

BAKE = re.compile(
    r"\b(cakes?|loaves|loaf|bread|muffins?|cupcakes?|sponge|buns?|scones?|biscuits?"
    r"|traybake|traybakes?|brownies?)\b",
    re.I)

ASK = re.compile(
    r"^(?:so\s+|ok\s+|okay\s+|and\s+)?"
    r"(?:(?:what|how)\s+about\s+|(?:and|or|plus)\s+|"
    r"(?:can|could|should|shall|would)\s+(?:i|we)\s+(?:make|bake|do|cook)\s+|"
    r"what\s+if\s+(?:i|we)\s+(?:made|make|bake|baked|cooked|cook)\s+)",
    re.I)

TAIL = re.compile(r"\s+(?:instead|too|as well|then|please|later|tonight|now)$", re.I)

LONGEST = 4

NAME_WORD = re.compile(r"^[a-z][a-z'-]*$", re.I)


def _the_name(noun):
    words = [word for word in noun.split() if word]
    while words and TAIL.match(" " + words[-1]):
        words.pop()
    if not words:
        return ""
    named = list(words)
    while named and named[0].lower() in ("a", "an", "some", "another"):
        named.pop(0)
    if not named or len(named) > LONGEST:
        return ""
    for word in named:
        if not NAME_WORD.match(word.strip(".,!?;")):
            return ""
    return " ".join(words).strip(".,!?;:").lower()


APPLIANCES = (r"oven|grill|hob|microwave|air\s*fryer|cooker|stove|range|pressure\s*cooker|"
              r"slow\s*cooker|toaster")
LACKS = re.compile(
    r"\b(?:no|without|not\s+got|dont\s+have|don't\s+have|cant\s+use|can't\s+use)"
    r"\s+(?:a\s+|an\s+|any\s+|working\s+|my\s+)?(?:"
    + APPLIANCES + r")\b"
    r"|\b(?:" + APPLIANCES + r")\s+(?:is\s+|has\s+|has\s+gone\s+)?"
    r"(?:broken|gone|died|had\s+it|packed\s+in)\b", re.I)


def written_out(text, memory=None):
    if not isinstance(text, str):
        return None
    line = " ".join(text.strip().split())
    if not line or len(line.split()) > 12:
        return None
    asked = ASK.match(line)
    if not asked:
        return None
    rest = line[asked.end():]
    if not (BAKE.search(rest) or NAMED_BAKES.search(rest)):
        return None
    noun = _the_name(rest)
    if not noun:
        return None
    if LACKS.search(noun):
        return None
    if not (BAKE.search(noun) or NAMED_BAKES.search(noun)):
        return None
    return "how do i make " + noun
