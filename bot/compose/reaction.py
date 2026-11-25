import re

PHRASES = {
    "wow": "awe", "woah": "awe", "whoa": "awe", "wowsers": "awe", "wowee": "awe",
    "omg": "awe", "gosh": "awe", "blimey": "awe", "crikey": "awe", "cor": "awe",
    "geez": "awe", "jeez": "awe",
    "really": "doubt", "seriously": "doubt", "honestly": "doubt", "truly": "doubt",
    "surely": "doubt", "no way": "doubt", "for real": "doubt", "get out": "doubt",
    "you what": "doubt", "come on": "doubt", "say what": "doubt", "my word": "awe", "good god": "awe",
    "my god": "awe", "oh my god": "awe", "oh my word": "awe", "good heavens": "awe",
}
LEAD = frozenset((
    "oh", "ah", "aw", "ooh", "uh", "um", "well", "so", "and", "but", "my", "god", "jesus",
    "christ", "jeez", "geez", "good", "bloody", "damn", "just", "huh", "hmm", "ok", "okay",
    "no", "for", "get", "out", "the", "hell", "heck", "come", "on", "you", "what", "say",
    "yeah", "yes",
))
AWE_REPLIES = (
    "It sounds like more than it is — the whole thing is usually one step. Which bit do you "
    "want to start with?",
    "It is easier once you have done it once. Do you want that as a list you can follow?",
    "Most of it is one small thing done properly. Shall I say which part matters most?",
    "That is the whole trick of it, honestly. Anything in there you want me to go over?",
)
DOUBT_REPLIES = (
    "Yes, really — and it is the small part that does the work. Which bit do you want me to go "
    "over?",
    "It is true, honestly. Is there a part of it that sounds off to you?",
    "I know it sounds odd — that is the whole answer though. Which bit would you not bet on?",
    "It is right, yes. Which part surprised you?",
)
NO_ANSWER = re.compile(
    r"\b(?:999|911|112|111|ambulance|a&e|casualty|emergency|urgent care|a search|search online|"
    r"rather not guess|sorry|sad news|condolence\w*|passed away|passed on|funeral|grief|"
    r"grieving|bereave\w*|miss (?:him|her|them)|died|death|dying|"
    r"hurt yourself|harm yourself|end your life|crisis|samaritans|suicide|116 123)\b")

A_CARE_ANSWER = re.compile(
    r"\b(?:gp|doctor|dentist|dental|nurse|pharmac\w*|111|999|a&e|nhs|clinic|"
    r"ring (?:them|us|the)|get it (?:looked at|checked|seen)|needs? (?:looking at|checking|seeing)|"
    r"ache|aching|aches|pain|sore|swelling|swollen|lump|rash|inflamed|fever|bleeding|burn|"
    r"sprain)\b")
A_BODY_LINE = re.compile(
    r"\b(?:my|his|her|their|our|your|the left|the right)\s+(?:tooth|teeth|gums?|jaw|back|knee|"
    r"knees|hip|shoulder|neck|throat|chest|stomach|belly|tummy|arm|arms|leg|legs|foot|feet|ankle|"
    r"wrist|hand|hands|finger|fingers|thumb|toe|toes|head|headache|migraine|ear|ears|eye|eyes|"
    r"skin|nose|sinus|lump|rash|itch|itchy|sore|ache|aching|aches|pain|painful|hurt|hurts|"
    r"hurting|swollen|swelling|bleed|bleeding|fever|cough|burn|burning|blister|sprain|sting|"
    r"infection|gland|glands)\b"
    r"(?!\s+(?:garden|yard|door|room|wall|seat|gate|fence|window|path|drive|field|lane|page|"
    r"cover|button|pocket|light|start|of\b))"
    r"|\b(?:toothache|headaches?|migraine|tooth|gums|sore throat|backache|stomach ache)\b")
CARE_REPLIES = (
    "It is worth getting that looked at rather than waiting on it. Anything in there you want "
    "me to go over?",
    "Nothing there is meant to scare you - it is just worth getting it seen. Any part you want "
    "me to say again?",
    "Yes - that one is a ring-them-today sort of thing. Do you want me to say what to ask when "
    "you call?",
    "That is the size of it, honestly. Shall I say what to mention when you get it looked at?",
)


_ASK = (r"(?:ok|okay|alright|fine|sensible|sound|wise|right|fair|"
        r"make\s+(?:any\s+)?sense|worth\s+it|a\s+good\s+idea|"
        r"a\s+good\s+choice|the\s+right\s+(?:thing|way))")
_TAIL = r"(?:\s+(?:then|though|honestly|yeah|for\s+me))?\s*[.?!]*\s*$"
CHECK = re.compile(
    r"\b(?:do|would|could)\s+(?:you|u)\s+(?:think|reckon|say|agree)\b[^.?!]{0,24}?\b" + _ASK
    + _TAIL
    + r"|^\s*(?:and\s+|but\s+|so\s+)?(?:is|are|was|were|does|did|would)\s+(?:that|this)\s+"
    r"(?:be\s+|sound\s+|look\s+|seem\s+)?" + _ASK + _TAIL
    + r"|\bare\s+you\s+sure" + _TAIL, re.I)
OWN_PLAN = re.compile(
    r"\b(?:i'?m|im|i am|we'?re|were|we are)\s+(?:going|gonna|planning|thinking (?:of|about)|"
    r"intending|about)\b|\b(?:i|we)\s+(?:want|need|have decided|decided)\s+to\b|"
    r"\b(?:i|we)\s+(?:might|may)\s+\w+", re.I)
NO_STANCE = re.compile(
    r"\b(?:i (?:don't|do not|cannot|can't) (?:know|say)|not know enough|rather not guess|"
    r"a search|search online|look it up)\b", re.I)
CHECK_REPLIES = (
    "Yes, as far as what you have told me goes - and if a detail is different, the answer changes "
    "with it. Which part are you least sure of?",
    "I would stand by it as advice. What I cannot check is the part only you know - which bit is "
    "worrying you?",
    "It holds up as far as I can tell. Tell me the bit that feels off and I will build the answer "
    "around it.",
    "Yes. It is the answer I would give again, and if one thing in it does not fit your side of "
    "it, say which.",
)


THEIR_REACTION = re.compile(r"\bam i\b|\boverreacting\b|\bbeing (?:silly|daft|mad)\b", re.I)


def _checking(text):
    said = " ".join(str(text or "").lower().split())
    if THEIR_REACTION.search(said):
        return False
    return bool(CHECK.search(said))


def _bare(text):
    clean = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    clean = clean.strip(" .,!?;:\"'")
    words = re.findall(r"[a-z']+", clean)
    if not words or len(words) > 5:
        return ""
    for size in (3, 2, 1):
        for start in range(0, len(words) - size + 1):
            kind = PHRASES.get(" ".join(words[start:start + size]))
            if not kind:
                continue
            rest = words[:start] + words[start + size:]
            if all(word in LEAD for word in rest):
                return kind
    return ""


def _an_answer(reply):
    line = " ".join(str(reply or "").split())
    if len(line) < 60:
        return False
    if line.endswith("?"):
        return False
    if NO_ANSWER.search(line.lower()):
        return False
    return True


def reply_for(text, memory):
    kind = _bare(text)
    if not kind:
        kind = "check" if _checking(text) else ""
    if not kind:
        return None
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return None
    last = turns[-1] if isinstance(turns[-1], dict) else {}
    if not _an_answer(last.get("bot")):
        return None
    said = str(last.get("user") or "").lower()
    if kind == "check" and OWN_PLAN.search(said):
        return None
    if kind == "check":
        from . import fallback as _fallback
        plan, plan_line = _fallback._the_plan_and_its_line(memory)
        if plan or plan_line:
            return None
    above_text = str(last.get("bot") or "").lower()
    if kind == "check" and NO_STANCE.search(above_text):
        return None
    care = A_BODY_LINE.search(said) and A_CARE_ANSWER.search(above_text)
    if kind == "check" and care:
        return None
    if kind == "check":
        pool = CHECK_REPLIES
    elif care:
        pool = CARE_REPLIES
    else:
        pool = AWE_REPLIES if kind == "awe" else DOUBT_REPLIES
    seen = sum(1 for turn in turns if isinstance(turn, dict))
    above = " ".join(str(last.get("bot") or "").lower().split())
    seed = " ".join(str(text or "").lower().split()) + "|" + str(seen) + "|" + above
    index = sum((i + 1) * ord(letter) for i, letter in enumerate(seed)) % len(pool)
    return pool[index]


def main(argv=None):
    import sys
    args = list(sys.argv[1:] if argv is None else argv)
    said = args[0] if args else "wow"
    after = ""
    if "--after" in args:
        rest = args[args.index("--after") + 1:]
        after = rest[0] if rest else ""
    if not after:
        print(_bare(said) or "(nothing)")
        return
    print(reply_for(said, {"turns": [{"user": "", "bot": after}]}) or "(nothing)")


if __name__ == "__main__":
    main()
