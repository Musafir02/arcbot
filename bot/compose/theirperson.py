import re

from . import pick

SOMEONE = (
    "best friend", "best mate", "close friend", "old friend", "friend", "mate", "pal", "buddy",
    "flatmate", "housemate", "workmate", "schoolmate", "colleague", "boss", "partner",
    "husband", "wife", "boyfriend", "girlfriend", "fiance", "fiancee", "ex",
    "mum", "mom", "mam", "mother", "dad", "father", "son", "daughter", "child", "kid", "baby",
    "sister", "brother", "sibling", "stepson", "stepdaughter", "stepmum", "stepdad",
    "nan", "nana", "gran", "granny", "grandma", "grandad", "grandpa", "grandmother",
    "grandfather", "aunt", "auntie", "uncle", "cousin", "nephew", "niece", "neighbour",
    "neighbor", "parents", "kids", "children", "sisters", "brothers", "friends", "mates",
)
BETWEEN = (r"(?:(?:best|closest|close|poor|old|little|big|lil|eldest|youngest|older|younger|"
           r"grown[-\s]?up|step|new|other)\s+)*")
A_PERSON_OF_THEIRS = re.compile(
    r"\b(?:my|our)\s+" + BETWEEN
    + "(?:" + "|".join(word.replace(" ", r"[\s-]?") for word in
                       sorted(SOMEONE, key=len, reverse=True)) + r")\b", re.I)

A_ROUGH_PATCH = re.compile(r"""
    ^\s*(?:
        (?:is|are|was|were|has|have|had)\b
      | s\s+been\b
      | been\b
    )
    # "really struggling", "still having a hard time", "been a bit down": the adverbs a person
    # puts in front of it, and "been" twice over ("has been really down").
    (?:\s+(?:really|very|so|just|still|properly|proper|completely|totally|quite|pretty|a\s+bit|
            well|dead|awful|genuinely|seriously|always|also|obviously|clearly|been|badly))*\s+
    (?:
        having\s+(?:a\s+|one\s+hell\s+of\s+a\s+|such\s+a\s+|the\s+worst\s+)?
          (?:(?:really|very|proper|properly|awful|bit\s+of\s+a|lot\s+of|terrible)\s+)?
          (?:hard|tough|rough|bad|rubbish|awful|terrible|difficult|stressful|horrible|lousy|
             miserable|shit|shitty|grim|dreadful)\s+
          (?:time|patch|spell|week|month|year|day|run)\b
      | struggling\b(?!\s+with\b)
      | finding\s+(?:it|things|everything|life|work|the\s+job)\s+
          (?:a\s+bit\s+|really\s+|very\s+|so\s+|quite\s+)?hard\b
      | going\s+through\s+(?:a\s+lot|a\s+(?:rough|hard|tough|bad)\s+(?:time|patch|spell)|hell|
                             it|something\s+bad|a\s+bad\s+patch)\b
      | in\s+a\s+bad\s+way\b
      | at\s+breaking\s+point\b
    )
""", re.I | re.X)
A_NOT_COPING = re.compile(r"""
    ^\s*(?:(?:is|are|was|were)\s+not|isn'?t|aren'?t|wasn'?t|hasn'?t|havent|weren'?t|not|
            never)\b
    (?:\s+(?:really|very|so|just|still|been|at\s+the\s+moment|at\s+all))*\s+
    coping\b.*$
""", re.I | re.X)
A_LOW = re.compile(r"""
    ^\s*(?:(?:is|are|was|were|has|have)\b|s\s+been\b|been\b)
    (?:\s+(?:really|very|so|a\s+bit|quite|pretty|proper|properly|just|always|still|been))*\s+
    (?:down|low)\b
    (?:\s+(?:at\s+the\s+moment|lately|these\s+days|just\s+now|right\s+now|again|too|still|today|
              this\s+week|since\s+[a-z0-9']+|about\s+[a-z0-9']+|in\s+(?:him|her)sel(?:f|ves)|
              and\s+[a-z0-9' ]+))?\s*[.!?]*\s*$
""", re.I | re.X)

A_CONDITION = re.compile(r"""
    ^\s*(?:
        (?:has|have|had|got)
      | ['\u2019]?s\s+got
      | (?:is|are|was|were)
      | (?:could|might|may|must)\s+be
      | (?:seems?|appears?)\s+(?:to\s+be)?
    )
    (?:\s+(?:really|very|probably|possibly|likely|also|now|actually|officially|just|
             only|maybe|perhaps|definitely|already|too))*\s*
    (?:a\s+bit\s+of\s+|a\s+touch\s+of\s+|an?\s+|mild\s+|suspected\s+)?
    (?P<condition>dyslexi\w*|dyspraxi\w*|dyscalculi\w*|adhd|add|autis\w*|asperger\w*|
      ocd|tourette\w*|non[\s-]?verbal|speech\s+delay|sensory\s+processing|deaf|
      hard\s+of\s+hearing|blind|partially\s+sighted|down'?s?\s+syndrome|
      learning\s+disabilit\w*|on\s+the\s+spectrum)\b
""", re.I | re.X)
A_WONDERING = re.compile(r"^\s*(?:could|might|may|must)\s+(?:be|have)\b|\bmaybe\b", re.I)
A_CONDITION_STATED = (
    "Thanks for telling me. Is there something about your {who} you're trying to work out?",
    "Good to know - I'll remember that about your {who}. Anything you're trying to sort out?",
    "Thanks. What's the part you're working on with your {who} just now?",
)
A_CONDITION_WONDERED = (
    "That's the hard part, the waiting. What have you noticed so far?",
    "It's rough sitting with a maybe like that. Write down what you see and when - that is what "
    "anyone you ask will want first. What made you start wondering?",
    "Not knowing yet is the worst of it. What has made you wonder?",
)

STANDS_DOWN = re.compile(r"""
    \b(?:
        hip|knee|knees|back|shoulder|arm|arms|leg|legs|foot|feet|ankle|wrist|hand|hands|head|
        headache|migraine|stomach|belly|chest|throat|tooth|teeth|ear|ears|eye|eyes|skin|joint|
        joints|spine|neck|heart|lung|lungs|blood|pain|pains|hurt|hurts|hurting|ache|aches|aching|
        ill|sick|sickness|unwell|hospital|doctor|gp|surgery|operation|chemo|cancer|tumour|tumor|
        diagnos\w*|scan|scans|medication|tablets|pills|dose|prescription|depress\w*|anxiety|
        panic|suicid\w*|self[-\s]?harm|addiction|drinking|drunk|sober|withdraw\w*|
        died|dying|die|death|dead|funeral|bereave\w*|grief|grieving|passed\s+away|
        tests|exam|exams|redundancy|divorce|money|rent|bills
    )\b
    | \? | \b(?:what|how|should|advice|tips|help|why|when|where|who)\b
""", re.I | re.X)

POOL = (
    "That's hard, watching someone you're close to go through it. What's been happening?",
    "Sorry to hear it. Being the one who notices is its own weight - how are they doing in "
    "themselves?",
    "That's a worry to be carrying for someone else. What's going on at the moment?",
    "Hard when you can see it and can't fix it. Do they know you've noticed?",
    "That's a lot for them - and for you to watch. What would help most: someone to listen, or "
    "something practical?",
    "I'm sorry. It's rough being the one at the side of it. What's the hardest part for you just "
    "now?",
)
NAMED = (
    "That's hard, watching your {who} go through it. What's been happening?",
    "Sorry to hear it. How is your {who} in themselves?",
    "That's a lot for your {who} to carry, and for you to watch. What would help most?",
)


def _said(text):
    words = re.findall(r"[a-z0-9'?!]+", str(text or "").lower())
    return " " + " ".join(words) + " " if words else ""


def _who(person, said):
    phrase = said[person.start():person.end()].strip()
    return re.sub(r"^(?:my|our)\s+", "", phrase, flags=re.I)


def reply_for(text, memory=None):
    said = _said(text)
    if not said.strip():
        return None
    if STANDS_DOWN.search(said):
        return None
    person = A_PERSON_OF_THEIRS.search(said)
    if not person:
        return None
    tail = said[person.end():]
    a_condition = A_CONDITION.match(tail)
    if a_condition and re.match(r"^\s*(?:could|might|may|must)\s+have\b", tail):
        return None
    if not (a_condition or A_ROUGH_PATCH.match(tail) or A_NOT_COPING.match(tail)
            or A_LOW.match(tail)):
        return None
    if a_condition and re.match(r"^\s*(?:and|&)\s+(?:i|me)\b", tail):
        return None
    if re.match(r"^\s*(?:and|&)\s+(?:i|me)\b", tail):
        return None
    read = memory.get("understood") if isinstance(memory, dict) else None
    read = read if isinstance(read, dict) else {}
    plural = bool(re.match(r"^\s*(?:are|were|have|have\s+been|were\s+being)\b", tail))
    if a_condition:
        pool = A_CONDITION_WONDERED if A_WONDERING.search(tail) else A_CONDITION_STATED
    else:
        pool = POOL if plural else POOL + NAMED
    who = _who(person, said)
    worded = [line.replace("{who}", who) for line in pool]
    turns = memory.get("turns") if isinstance(memory, dict) else None
    last = turns[-1].get("bot") if turns and isinstance(turns[-1], dict) else None
    if last and last in worded and len(worded) > 1:
        worded = [line for line in worded if line != last]
    return pick(worded, read, said.strip())


def may_replace(reply, text=""):
    said = str(reply or "").strip()
    if not said:
        return False
    from . import fallback

    if fallback._is_a_hedge(said) or fallback._in_a_pool(said, (fallback.NEUTRAL,)):
        return True
    mine = fallback._the_words(text)
    theirs = fallback._the_words(said)
    if len(mine) < 2 or not theirs:
        return False
    shared = mine & theirs
    return len(shared) >= 2 and len(shared) / len(mine) >= 0.6
