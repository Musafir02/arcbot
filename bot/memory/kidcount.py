import random
import re

CHILD_RELATIONS = ("son", "daughter", "child", "kid", "baby", "twin", "boy", "girl", "stepson",
                   "stepdaughter", "teenager", "lad", "lass", "sons", "daughters", "children",
                   "kids", "boys", "girls", "twins", "lads", "lasses")

THE_ASK = re.compile(
    r"\bhow\s+many\b(?P<rest>[^.?!]*)", re.I)
THEIR_OWN = re.compile(r"\b(?:i|we|my|our|us)\b", re.I)
SOMEONE_ELSE = re.compile(
    r"\b(?:does|do|did|has|have|had)\s+(?:my|her|his|their|your|she|he|they|the|that)\b", re.I)
A_CHILD = re.compile(r"\b(?:" + "|".join(CHILD_RELATIONS) + r")\b", re.I)
NOT_THEIR_OWN = re.compile(
    r"\b(?:in|at|per|into)\s+(?:a|an|the|my|our)\s+(?:class|classroom|school|nursery|team|"
    r"group|year|country|world)\b", re.I)


def _asks(text):
    low = str(text or "").strip().lower()
    match = THE_ASK.search(low)
    if not match:
        return False
    rest = match.group("rest")
    if not A_CHILD.search(rest):
        return False
    if SOMEONE_ELSE.search(low):
        return False
    if NOT_THEIR_OWN.search(low):
        return False
    return bool(THEIR_OWN.search(low)) or len(rest.split()) <= 2


def _named_children(memory):
    held = set()
    for entry in memory.get("others") or []:
        if not isinstance(entry, dict):
            continue
        name = str(entry.get("name") or "").strip().lower()
        who = str(entry.get("who") or "").strip().lower()
        if not name or name in held:
            continue
        if str(entry.get("of") or entry.get("whose") or "").strip():
            continue
        if who in CHILD_RELATIONS or not who:
            held.add(name)
    return held


def _relations(memory):
    held = []
    for who in (memory.get("user") or {}).get("people") or []:
        word = str(who or "").strip().lower()
        if word in CHILD_RELATIONS and word not in held:
            held.append(word)
    for entry in memory.get("others") or []:
        if not isinstance(entry, dict):
            continue
        word = str(entry.get("who") or "").strip().lower()
        if word in CHILD_RELATIONS and word not in held:
            held.append(word)
    return held


def count(memory):
    user = memory.get("user") or {}
    if user.get("kids"):
        return None
    named = _named_children(memory)
    relations = _relations(memory)
    held = max(len(named), len(relations))
    if held < 2:
        return None
    return held


WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
         10: "ten", 11: "eleven", 12: "twelve"}


def _vary(options, memory):
    turns = memory.get("turns") or []
    recent = {t.get("bot") for t in turns[-5:] if isinstance(t, dict)}
    fresh = [o for o in options if o not in recent] or list(options)
    return random.Random(len(turns)).choice(fresh)


def reply_for(text, memory):
    if not isinstance(memory, dict) or not _asks(text):
        return None
    held = count(memory)
    if not held:
        return None
    word = WORDS.get(held, str(held))
    noun = "children"
    return _vary(["You've got " + word + " " + noun + ".",
                  word.capitalize() + " " + noun + " \u2014 that's what you've told me.",
                  "That makes " + word + " " + noun + " you've mentioned."], memory)
