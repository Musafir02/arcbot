import re

A_LOSS = re.compile(
    r"\b(?:i|ive|i have)\s+lost\s+(?P<how>"
    r"half\s+a\s+stone|a\s+stone|"
    r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s*"
    r"(?:kilos?|kg|kgs|pounds?|lbs?|stone)|"
    r"(?:some|a\s+lot\s+of)\s+weight|weight)\b", re.I)

A_PLAN_TO_LOSE = re.compile(
    r"\b(?:lose|losing|lost|slim|slimming|diet|dieting|weight|kg|kilos?|pounds?|lbs?|"
    r"stone|calories|cutting\s+down|get\s+fitter|fitness)\b", re.I)

GLUED_UNIT = re.compile(r"(?<=\d)(kgs?|kilos?|pounds?|lbs?|stone)\b", re.I)

SAID_BACK = (
    "{X} off is a real loss, and slow is the way it stays off. It is on file.",
    "{X} down is the plan working, which is the only thing that matters here.",
    "That is {x2} of the plan doing its job. I'll keep the meals on the lean side when you ask.",
)
FIRST = (
    "{X} off - good going, and at a rate that stays off. What is working so far?",
    "{X} down is real progress: slow enough to keep, which is the part most people miss.",
    "Nice one: {X} off, and no starving yourself for it. Say if you want meal ideas that hold up.",
)

HOW_GOING = re.compile(
    r"^(?:so\s+|and\s+|ok(?:ay)?\s+,?\s+)?"
    r"(?:how\s+am\s+i\s+(?:doing|getting\s+on|going)|how\s+(?:is|s)\s+it\s+going|"
    r"how\s+am\s+i\s+getting\s+on|how\s+is\s+the\s+(?:diet|plan)\s+going|"
    r"how\s+much\s+have\s+i\s+lost|how\s+much\s+weight\s+have\s+i\s+lost|"
    r"(?:is|was)\s+that\s+(?:good|ok|okay|alright|any\s+good)\s+(?:going|so\s+far)?|"
    r"am\s+i\s+doing\s+(?:well|ok|okay|alright|it))\s*[.!?]*$", re.I)

PROGRESS_REPLY = (
    "{X} so far, by your own count - and slow is the rate that stays off, so that is going well. "
    "Say if you want the meals tightened up.",
    "{X} down and still going, which is the part most people lose. Nothing to change if it is "
    "still coming off slowly.",
    "You have {x2} off since you started. That is on the good side of the pace, so keep the plan "
    "as it is unless it stalls.",
)

_NUMBER_WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven",
                 8: "eight", 9: "nine", 10: "ten"}


def _tidy(how):
    said = GLUED_UNIT.sub(lambda m: " " + m.group(1), " ".join(str(how or "").split()))
    said = " ".join(said.split())
    return said[:1].upper() + said[1:] if said else said


def _the_plan_to_lose(memory):
    if not isinstance(memory, dict):
        return False
    user = memory.get("user") if isinstance(memory.get("user"), dict) else {}
    said = []
    for key in ("plan", "goal", "aim", "diet"):
        value = user.get(key)
        if isinstance(value, str):
            said.append(value)
    for key in ("plans", "goals"):
        value = user.get(key)
        if isinstance(value, (list, tuple)):
            said.extend(str(item) for item in value)
    return any(A_PLAN_TO_LOSE.search(text) for text in said if text)


def _the_turn_that_said_it(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    seen = 0
    for turn in list(turns or []):
        if isinstance(turn, dict) and A_LOSS.search(str(turn.get("user") or "")):
            seen += 1
    return seen


def the_loss_that_was_the_plan(text, memory):
    match = A_LOSS.search(str(text or ""))
    if not match:
        return ""
    if not _the_plan_to_lose(memory):
        return ""
    how = _tidy(match.group("how"))
    pool = FIRST if _the_turn_that_said_it(memory) <= 1 else SAID_BACK
    turns = memory.get("turns") if isinstance(memory, dict) else None
    reply = pool[len(turns or ()) % len(pool)]
    if "{X}" in reply:
        reply = reply.replace("{X}", how)
    else:
        reply = reply.replace("{x2}", how[:1].lower() + how[1:])
    if isinstance(memory, dict) and isinstance(memory.get("user"), dict):
        memory["user"]["progress"] = {"lost": how}
    return reply


def _the_progress(memory):
    if not isinstance(memory, dict):
        return ""
    user = memory.get("user") if isinstance(memory.get("user"), dict) else {}
    progress = user.get("progress") if isinstance(user.get("progress"), dict) else {}
    lost = str(progress.get("lost") or "").strip()
    return lost if lost and lost.lower() not in ("weight", "some weight") else ""


def a_progress_asked(text, memory):
    if not HOW_GOING.match(" ".join(str(text or "").lower().split())):
        return ""
    lost = _the_progress(memory)
    if not lost:
        return ""
    turns = memory.get("turns") if isinstance(memory, dict) else None
    reply = PROGRESS_REPLY[len(turns or ()) % len(PROGRESS_REPLY)]
    return reply.replace("{X}", lost).replace("{x2}", lost[:1].lower() + lost[1:])
