import re

from . import fallback, pick

LIVE_DECIDE = (
    "I can't see the {kind} from here, sorry. {check} Then it's your call, and I can help you "
    "weigh it: what would each way cost you?",
    "I can't see the {kind} from here, sorry. {check} Nobody can call that but you \u2014 say what "
    "you'd lose either way and I'll lay both out with you.",
)
LIVE_CHECK = {
    "weather": ("A weather app has the next few days in one tap, with the feels-like temperature.",
                "weather"),
    "hours": ("The venue's own page or its map listing has today's hours, holiday changes and "
              "all.", "opening times"),
    "prices": ("What it costs turns on which one it is, where you buy it and the day, and the "
               "seller's own site has today's figure.", "prices"),
    "news": ("A news site has the latest.", "news"),
    "travel": ("The operator's app or a journey planner has the next one and any disruption.",
               "times or delays"),
}
LIVE_DECIDE_ASKS = re.compile(
    r"\b(?:should i|shall i|is it worth|is it better|would it be better|do i need|do you think "
    r"i should|what would you do|not sure|unsure|dont know|do not know|no idea|cant decide|"
    r"torn between|in two minds|whether to|if i can)\b")
NOTE_KIND = {line: kind for kind, _phrases, pool in fallback.LIVE_KINDS for line in pool}
NO_MARK = re.compile(r"['\u2019`]")


def answer_for(text, memory=None, reply=""):
    kind = NOTE_KIND.get(str(reply or "").strip())
    if not kind:
        return None
    check, word = LIVE_CHECK.get(kind, ("", ""))
    if not check:
        return None
    said = NO_MARK.sub("", str(text or "").lower())
    if not LIVE_DECIDE_ASKS.search(said):
        return None
    options = tuple(line.format(check=check, kind=word) for line in LIVE_DECIDE)
    read = memory.get("understood") if isinstance(memory, dict) else None
    return pick(options, read, said)
