import re

from ..compose import pick

_GOING = r"(?:travelling|traveling|flying|driving|heading|off|away|on holiday|going away|going)"
SAID_WITH = re.compile(
    r"\b(?:i'?m|im|i am|we'?re|were|we are)\s+" + _GOING + r"\s+"
    r"(?:off\s+|away\s+|there\s+|down\s+)?with\s+(?P<who>[a-z][a-z'\u2019 -]{1,40})", re.I)
OFF_TO_WITH = re.compile(
    r"\b(?:i'?m|im|i am|we'?re|were|we are)\s+" + _GOING + r"\s+(?:to|into|for|back to)\s+"
    r"[a-z][a-z'\u2019 -]{1,25}?\s+with\s+(?P<who>[a-z][a-z'\u2019 -]{1,40})", re.I)
TAKING = re.compile(
    r"\b(?:i'?m|im|i am|we'?re|were|we are)\s+(?:taking|bringing)\s+(?P<who>[a-z][a-z'\u2019 -]{1,40})",
    re.I)
COMING_WITH = re.compile(
    r"\b(?P<who>(?:my|our)\s+[a-z][a-z'\u2019-]{1,20}"
    r"(?:\s+and\s+(?:her|his|their|my|our)\s+[a-z][a-z'\u2019-]{1,20})?)"
    r"(?:\s+is|\s+are|'?s|s)?\s+(?:coming|going|travelling|traveling)\b", re.I)
_NOT_COMING_ALONG = re.compile(
    r"\b(?:to stay|to visit|to live|to dinner|to lunch|to pick me up|home|back|round|over|"
    r"out|down|up)\b|\bin\s*$", re.I)
_STOP = re.compile(
    r"\b(?:to|from|on|at|in(?!-law)|for|next|this|tomorrow|tonight|because|but|so|then|and then|"
    r"who|which|when|if|as|while|by|via|through|until|till|after|before)\b|[,.;:!?]", re.I)
_A_PERSON = re.compile(
    r"^(?:(?:my|our|the|a|an|his|her|their|two|three|four|five|six|a few|some)\s+)?"
    r"(?:mum|mom|mam|mummy|mother|dad|father|daddy|papa|son|daughter|wife|"
    r"husband|partner|sister|brother|kids?|children|friend|friends|mate|mates|parents|family|"
    r"granny|gran|nan|grandma|grandad|grandpa|aunt|auntie|uncle|cousin|niece|nephew|"
    r"boyfriend|girlfriend|colleague|neighbou?r|in-?laws?|mother-in-law|father-in-law)"
    r"(?:\s+and\s+.*)?$", re.I)
EITHER_SIDE = re.compile(
    r"\b(?:me|i)\s+and\s+(?P<who>(?:my|our|the)\s+[a-z][a-z'\u2019-]{1,20}"
    r"(?:\s+and\s+(?:her|his|their)\s+[a-z][a-z'\u2019-]{1,20})?)\s+"
    r"(?:are|is|were|was)\s+(?:going|off|flying|driving|travelling|traveling|heading)\b"
    r"|\b(?P<other>(?:my|our|the)\s+[a-z][a-z'\u2019-]{1,20})\s+and\s+(?:me|i)\s+(?:are|were)\s+"
    r"(?:going|off|flying|driving|travelling|traveling|heading)\b", re.I)

ASK = re.compile(
    r"\bwho(?:'?s| is| are| else is| else)? (?:else )?(?:coming|going|travelling|traveling|"
    r"flying|driving)\s+(?:with|along with)\s+(?:me|us)\b"
    r"|\bwho (?:am i|are we) (?:going|travelling|traveling|flying|driving|heading)\s+with\b"
    r"|\bis (?:anyone|anybody|someone|somebody) (?:coming|going|travelling|traveling)\s+with\s+"
    r"(?:me|us)\b"
    r"|\bam i (?:going|travelling|traveling)\s+(?:with anyone|with anybody|alone|on my own)\b"
    r"|\bwho did (?:i|you) say (?:is |was )?(?:coming|going)\b", re.I)
IS_COMING_TOO = re.compile(
    r"\bis\s+(?P<who>(?:my|our)\s+[a-z][a-z'\u2019 -]{1,20}?)\s+"
    r"(?:coming|going|travelling|traveling|flying|driving)\b", re.I)

ASKS_FOR_A_DETAIL = re.compile(
    r"^\W*(?:and |so |but |oh |right |also |ok(?:ay)?[ ,]+)*"
    r"(?:when(?:'?s| is| are| was| am| do| does| did| will| would)?\b"
    r"|where\b|why\b|which (?:day|date)\b|what (?:day|date|time)\b"
    r"|how (?:long|soon|many days)\b)", re.I)

_ABOUT_SOMEONE_ELSE = re.compile(r"\bwith\s+(?:my|our|your)\s+\w+", re.I)
PUT_RIGHT = re.compile(
    r"\b(?:actually |no,? )?(?:it'?s |its |it is |they'?re |they are |that'?s |thats |"
    r"it was |the one is )?(?P<new>[a-z][a-z'\u2019 -]{1,25}?)\s+not\s+"
    r"(?:the |my |our )?(?P<old>[a-z][a-z'\u2019 -]{1,25})$", re.I)


def _bare(who):
    words = str(who or "").lower().split()
    while words and words[0] in ("my", "our", "the", "a", "an", "your"):
        words.pop(0)
    return " ".join(words)


def _the_companion(text):
    said = " ".join(str(text or "").split())
    said = re.sub(r"\b([a-z]+)\s+in[\s-]+(laws?)\b", r"\1-in-\2", said, flags=re.I)
    if not said or said.rstrip().endswith("?"):
        return ""
    for pattern in (SAID_WITH, OFF_TO_WITH, TAKING, COMING_WITH, EITHER_SIDE):
        match = pattern.search(said)
        if not match:
            continue
        who = match.group("who") or match.group("other") or ""
        cut = _STOP.search(who)
        if cut:
            who = who[:cut.start()]
        who = who.strip(" ,.;:-'\u2019")
        if not who:
            continue
        if " and " in who:
            first, rest = who.split(" and ", 1)
            if _A_PERSON.match(rest) or _A_PERSON.match("my " + rest):
                who = first + " and " + rest
            else:
                who = first
        words = who.split()
        if len(words) > 5:
            continue
        if pattern is COMING_WITH and _NOT_COMING_ALONG.search(said):
            continue
        if not (_A_PERSON.match(who) or _A_PERSON.match("my " + who)):
            continue
        return who
    return ""


def _as_you_would_say_it(who):
    said = who.strip()
    for mine, yours in (("my ", "your "), ("our ", "your "), ("i ", "you "), ("me", "you"),
                        ("we ", "you "), ("myself", "yourself")):
        if said.startswith(mine):
            return yours + said[len(mine):]
    return said


def _more_than_one(who):
    low = who.lower()
    return " and " in low or low.split()[-1].endswith("s")


def _the_correction(text, memory):
    held = memory.get("company")
    if not isinstance(held, dict) or not held.get("who"):
        return ""
    match = PUT_RIGHT.search(" ".join(str(text or "").lower().split()))
    if not match:
        return ""
    old = _bare(match.group("old"))
    if not old or old != _bare(held["who"]):
        return ""
    new = match.group("new").strip(" ,.;:-")
    return new if _A_PERSON.match(new) or _A_PERSON.match("my " + new) else ""


ON_THEIR_OWN = re.compile(r"\b(?:on my own|alone|by myself|solo|just me)\b", re.I)


def _a_trip_is_here(memory):
    user = memory.get("user") if isinstance(memory, dict) else None
    plans = (user or {}).get("plans") or []
    return any(str(plan or "").strip() for plan in plans)


def _on_their_own(memory):
    user = memory.get("user") if isinstance(memory, dict) else None
    plans = (user or {}).get("plans") or []
    return any(ON_THEIR_OWN.search(str(plan or "")) for plan in plans)


_ASKS = re.compile(r"^\W*(?:is|are|was|were|will|would|can|could|should|shall|do|does|did|"
                   r"who|what|when|where|why|how)\b", re.I)


_THE_MONTHS = re.compile(
    r"\b(?:january|february|march|april|may|june|july|august|september|october|november|"
    r"december|jan|feb|mar|apr|jun|jul|aug|sept|sep|oct|nov|dec)\b", re.I)
_TO_THE_TRIP = re.compile(
    r"\b(?:going|off|flying|driving|travelling|traveling|heading|moving|off to|away to)\s+"
    r"(?:to|into|for|off to|down to|back to)\s+(?P<rest>.+)$", re.I)


def _the_phrase_a_frame_can_say(plan):
    plan = " ".join(str(plan or "").split()).strip(" .")
    found = _TO_THE_TRIP.search(plan)
    if found and found.group("rest").strip(" ."):
        plan = found.group("rest").strip(" .")
    if not plan:
        return ""
    plan = _THE_MONTHS.sub(lambda m: m.group(0).capitalize(), plan)
    return plan[:1].upper() + plan[1:]


def _the_trip_on_the_table(memory):
    user = memory.get("user") if isinstance(memory, dict) else None
    places = (user or {}).get("places") or []
    if not places:
        return ""
    place = str(places[-1]).strip(" .")
    plan = str((user or {}).get("plan") or "").strip(" .")
    if not place or (plan and place.lower() not in plan.lower()):
        return ""
    return _the_phrase_a_frame_can_say(plan) or place


def _new_to_the_chat(who, memory):
    bare = _bare(who)
    if not bare:
        return False
    said = re.compile(r"\b" + re.escape(bare) + r"\b", re.I)
    turns = [str(t.get("user") or "") for t in (memory.get("turns") or [])
             if isinstance(t, dict)]
    if turns and turns[-1].strip() == str(memory.get("understood", {}).get("text") or "").strip():
        turns = turns[:-1]
    return not any(said.search(line) for line in turns)


def _the_one_person_asked_about(text, memory):
    low = " ".join(str(text or "").lower().split())
    if not low or _NOT_COMING_ALONG.search(low):
        return None
    if ASKS_FOR_A_DETAIL.search(low):
        return None
    found = IS_COMING_TOO.search(low)
    if not found:
        return None
    named = _bare(found.group("who"))
    if not named or not _A_PERSON.match(named) and not _A_PERSON.match("my " + named):
        return None
    held = memory.get("company")
    if not isinstance(held, dict) or not held.get("who"):
        if not _a_trip_is_here(memory):
            return None
        return pick(["Nothing said about your " + named + " - you have not said who is coming "
                     "with you.",
                     "You have not told me who is coming, so I cannot say about your " + named +
                     "."], memory, seed_text=low) or None
    who = _as_you_would_say_it(held["who"])
    if named == _bare(held["who"]):
        return pick(["Yes - you said " + who + " is coming with you.",
                     "You said " + who + " is coming, so yes.",
                     who.capitalize() + " - that is who you said was coming."],
                    memory, seed_text=low) or None
    return pick(["You only said " + who + " was coming - nothing about your " + named + ".",
                 "Nothing said about your " + named + " - it was " + who + " you told me about."],
                memory, seed_text=low) or None


def _the_companion_joins(text, memory):
    low = " ".join(str(text or "").lower().split())
    if not low or low.rstrip().endswith("?") or _ASKS.match(low):
        return None
    place = _the_trip_on_the_table(memory)
    if not place:
        return None
    who = _the_companion(text)
    if not who or not _new_to_the_chat(who, memory):
        return None
    said = _as_you_would_say_it(who)
    if _the_plan_is_this_line(text, memory):
        return pick([
            "Nice - " + place + " with " + said + ".",
            "Lovely - " + place + " with " + said + ".",
            place + " with " + said + " - good.",
        ], memory, seed_text=low) or None
    options = [
        said.capitalize() + " as well - good. " + place + " is better with company.",
        "Nice, " + said + " coming too. " + place + " goes better shared.",
        "Good - " + said + " along for " + place + ", then.",
    ]
    return pick(options, memory, seed_text=low) or None


def _the_plan_is_this_line(text, memory):
    line = " ".join(str(text or "").lower().split()).strip(" .")
    plan = " ".join(str(((memory or {}).get("user") or {}).get("plan") or "")
                    .lower().split()).strip(" .")
    return bool(line) and bool(plan) and (plan == line or line in plan or plan in line)


def observe(text, memory):
    fixed = _the_correction(text, memory)
    if fixed:
        memory["company"] = {"who": fixed, "turns": len(memory.get("turns") or []),
                             "corrected": True}
        return None
    who = _the_companion(text)
    if not who:
        return None
    memory["company"] = {"who": who, "turns": len(memory.get("turns") or [])}
    return None


def answer(text, memory):
    low = " ".join(str(text or "").lower().split())
    if not ASK.search(low) or _ABOUT_SOMEONE_ELSE.search(low):
        one = _the_one_person_asked_about(text, memory)
        if one:
            return one
        return _the_companion_joins(text, memory)
    held = memory.get("company")
    if not isinstance(held, dict) or not held.get("who"):
        if not _a_trip_is_here(memory):
            return None
        if _on_their_own(memory):
            return pick(["You said you were going on your own.",
                         "On your own, you said - nobody else was named."], memory, seed_text=low) or None
        return pick(["You haven't said who's going with you.",
                     "Nobody yet - you haven't said who is going with you."],
                    memory, seed_text=low) or None
    who = _as_you_would_say_it(held["who"])
    verb = "are" if _more_than_one(who) else "is"
    if low.rstrip().endswith(("alone", "on my own")):
        return "Not on your own - " + who + " " + verb + " coming with you."
    options = ["You said " + who + " " + verb + " coming with you.",
               who.capitalize() + " - that is who you said you were going with.",
               "You said " + who + " " + verb + " coming with you, and that is all I know."]
    if who.startswith("your "):
        options.insert(1, "Your " + who.split(" ", 1)[1] + ", you told me.")
    reply = pick(options, memory, seed_text=low)
    return reply or None
