import re

FILLER = (r"(?:(?:ok|okay|well|right|alright|and|so|then|anyway|honestly|please|thanks|ta|ha|"
          r"lol|x)\b[,;\s]+)*")

WISH = re.compile(
    FILLER
    + r"(?:"
      r"(?:good|best\s+of|all\s+the)\s+luck"
      r"(?:\s+(?:with|on|for)\s+(?:it|that|this|them|me|us|"
      r"(?:the|your|my)\s+[a-z']+(?:\s+[a-z']+)?))?"
      r"|all\s+the\s+best(?:\s+(?:with|to)\s+(?:it|that|this|you|them))?"
      r"|(?:keep\s+)?(?:your|my|our)?\s*(?:fingers|fingers and toes|thumbs)(?:\s+(?:and|n)?\s*(?:toes))?"
      r"\s*(?:crossed|are crossed)?(?:\s+for\s+(?:me|us))?"
      r"|(?:with\s+)?(?:any\s+)?luck(?:,?\s+(?:then|anyway))?"
      r"|touch\s+wood"
      r"|heres?\s+hoping"
      r"|(?:hopefully(?:,?\s+(?:then|anyway))?"
      r"(?:\s+(?:that|it|this)(?:\s+(?:works?|does(?:\s+(?:the\s+trick|it|the\s+job))?|"
      r"helps?|is\s+enough|sorts\s+it))?)?)"
      r"|(?:i\s+)?(?:really\s+|do\s+|just\s+)?hope\s+(?:so|it|that|this)"
      r"(?:\s+(?:works?|does(?:\s+(?:the\s+trick|it|the job))?|helps?|goes\s+well|lands|"
      r"is\s+enough|comes\s+off|holds|clears(?:\s+up)?|sorts\s+it))?"
      r")"
    + FILLER
    + r"[!. ]*$",
    re.I,
)

GROUPS = {
    "goodluck": (
        "Good luck with it \u2014 tell me how it goes.",
        "Good luck. Say how you get on.",
    ),
    "fingers": (
        "Fingers crossed. Tell me how it goes.",
        "Crossing mine as well. Say how you get on.",
    ),
    "luck": (
        "With luck, then. I would like to hear how it turns out.",
        "With luck. Tell me how it goes.",
    ),
    "wood": (
        "Touch wood. Tell me how it goes once you know.",
        "Touch wood, then. Say how it turns out.",
    ),
    "hope": (
        "Hope so too. Come back and say how it landed.",
        "Hoping with you. Tell me how it goes.",
    ),
}

_FINGERS = re.compile(r"\b(?:fingers|thumbs)\b", re.I)
_WOOD = re.compile(r"touch\s+wood", re.I)
_LUCK = re.compile(r"\bluck\b", re.I)


_GOOD_LUCK = re.compile(r"\b(?:good|best\s+of|all\s+the)\s+luck\b|\ball\s+the\s+best\b", re.I)


def _group(line):
    if _GOOD_LUCK.search(line):
        return "goodluck"
    if _FINGERS.search(line):
        return "fingers"
    if _WOOD.search(line):
        return "wood"
    if _LUCK.search(line):
        return "luck"
    return "hope"


FOR_SOMEONE = re.compile(r"\bhope\s+(?:you|your|he|she|they|it\s+goes|the|everything)\b", re.I)


def reading(text):
    line = str(text or "").strip()
    if not line or "?" in line:
        return False
    if FOR_SOMEONE.search(line):
        return False
    return bool(WISH.match(line))


def answer_for(text, memory):
    if not reading(text):
        return None
    pool = GROUPS[_group(str(text or ""))]
    if isinstance(memory, dict):
        count = memory.get("hope_said")
        count = count + 1 if isinstance(count, int) else 1
        memory["hope_said"] = count
        return pool[(count - 1) % len(pool)]
    return pool[0]
