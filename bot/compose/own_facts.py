import re

from . import pick

STOP_WORDS = frozenset("""about the a an and or but that this it its was were is are be been
did do does say said tell told mention mentioned you your me my i we us our again""".split())

OWN_WORDS = frozenset((
    "mum", "mom", "mother", "dad", "father", "parent", "parents", "brother", "brothers",
    "sister", "sisters", "sibling", "siblings", "son", "sons", "daughter", "daughters", "kid",
    "kids", "child", "children", "baby", "wife", "husband", "partner", "nan", "nana", "gran",
    "granny", "grandma", "grandad", "grandpa", "grandparents", "aunt", "auntie", "uncle",
    "cousin", "cousins", "niece", "nephew", "inlaws", "family", "flatmate", "housemate",
    "landlord", "neighbour", "neighbours", "boss", "manager", "colleague", "carer",
    "name", "surname", "middlename", "nickname", "age", "birthday", "birthdate", "dob",
    "address", "postcode", "house", "flat", "home", "rent", "mortgage", "job", "work", "shift",
    "shifts", "rota", "wage", "wages", "salary", "pay", "holiday", "holidays", "leave",
    "appointment", "appointments", "referral", "prescription", "meds", "medication", "tablets",
    "results", "record", "records", "account", "bill", "bills", "order", "budget", "savings",
    "dog", "dogs", "cat", "cats", "pet", "pets", "puppy", "kitten", "car", "van", "bike",
))

HOW_MANY = re.compile(r"^how (many|much)\s+(.+?)\s+(?:do|did) i have(?: left)?$")
HOW_MANY_GOT = re.compile(r"^how (many|much)\s+(.+?)\s+have i got(?: left)?$")
HOW_OLD = re.compile(r"^how old am i$")
WHAT_MY = re.compile(r"^what(?:s| is| was)?\s+my\s+(.+?)$")
WHEN_MY = re.compile(r"^(?:when|what time)(?:s| is| was)?\s+my\s+(.+?)$")
WHEN_AUX_MY = re.compile(r"^(?:when|what time)\s+(?:does|do|did|will|should|can)\s+my\s+(.+?)$")
WHERE_MY = re.compile(r"^where(?:s| is| was)?\s+my\s+(.+?)$")

HAVEN_T_SAID = (
    "You haven't told me {q}, so I've no way to know - tell me and I'll remember it.",
    "I don't know {q}: that's yours, not something I can look up. Tell me and I'll keep it.",
    "I only know what you tell me, and you've not said {q}. What's the answer?",
)
AS_THE_QUESTION = (
    "{Q}? You've not said, so only you know - tell me and I'll remember it.",
    "{Q}? I can't look that up: it's about you. Say it once and I'll keep it.",
)

HOW_TO = re.compile(r"\bhow (?:do|can|could|should|would|might) i\b")
ABOUT_BOT = re.compile(r"\b(?:you|your|yours|yourself)\b")

CHAT_WORDS = frozenset((
    "chat", "chats", "conversation", "conversations", "message", "messages", "history",
    "transcript", "transcripts", "logs",
))
A_HAND_ON_THEM = re.compile(
    r"\b(?:see|read|open|look at|look back|check|bring up|pull up|access|scroll back|"
    r"go back to|remember|recall|keep|store|save|hold|show me|do with)\b")
THE_OTHER_CHATS = re.compile(
    r"\b(?:see|read|open|look at|look back|check|bring up|pull up|access|scroll back|"
    r"go back to|remember|recall|find|keep|store|save|hold|show me|know about|do with)\b")
OTHER_THAN_THIS = re.compile(
    r"\b(?:before|earlier|previous|previously|past|old|last|other|others|yesterday|prior|"
    r"last time|history)\b")
A_RECORD_OF_THEM = re.compile(
    r"\b(?:is|are) there (?:a |any |some )?\b.{0,24}\b(?:list|record|records|history|log|"
    r"logs|copy|transcript)\b|\bdo you (?:have|keep|store) (?:a |any )?(?:record|records|"
    r"list|history|log|logs|copy|transcript)\b")
SAID_IN_A_PAST_CHAT = re.compile(
    r"\b(?:what|everything|all) (?:we|i) (?:said|talked about|wrote|asked)\b.{0,30}"
    r"\b(?:before|earlier|yesterday|last time|previous|in another chat|in other chats)\b")
LEARNING_ASK = re.compile(
    r"\b(?:learn|learns|learning|train|trains|training|trained|teach|teaches|teaching|"
    r"update|updates|updating|improve|improves|improving|pick (?:things |stuff )?up|"
    r"pick up on)\b|\b(?:do|will|would|are|did)\s+(?:you|u)\s+get(?:ting)?\s+better\b")
TAUGHT_BY_THIS = re.compile(
    r"\b(?:teach|teaches|show|shows|tell|tells|give|gives|feed|feeds)\s+(?:you|u)\b|"
    r"\b(?:you|u)\s+(?:learn|learning|train|training|pick\w*)\b.{0,30}"
    r"\b(?:from|on|off)\s+(?:me|what i|us|this|my|our|these|the chats)\b|"
    r"\b(?:learn|train)\w*\s+(?:on|from)\s+(?:my|our|these|this)\b|"
    r"\blearn from me\b|\b(?:do|will|would|are|did)\s+(?:you|u)\s+get(?:ting)?\s+better\b")
SAID_BEFORE = re.compile(r"\b(?:again|remind me|did i say|did i tell you)\b")

NO_OTHER_CHATS = (
    "No: each chat starts empty for me, so nothing from another conversation comes through. "
    "Everything you tell me in this one stays with me, though - say it here and I'll use it. "
    "What was it about?",
    "I can't open earlier chats - a new one starts with nothing in it. What you and I say in "
    "this chat I do keep, so tell me here and I'll pick it up from there. What were you trying "
    "to find?",
    "There's no history on my side: what we say stays in this conversation, and a new chat "
    "begins blank. So say it once more here and I'll have it. What was it?",
)

NO_TRAINING = (
    "No training as we talk: I'm a program with a lot of everyday things in it, and what I pick "
    "up is only what you say here, while we are in this chat. Nothing you tell me teaches me for "
    "the next person.",
    "I don't learn from the chat, no - nothing is fed back in. I'm the same program at the end of "
    "it as at the start, with everything you said in front of me while we talk.",
    "Nothing I hear changes what I know: no training, no memory of it afterwards. What you say "
    "does get used - here, in this conversation, as we go.",
)

THEIR_OWN_WORD = frozenset((
    "my", "our", "the", "these", "those", "your", "all", "any", "every", "this", "that",
    "previous", "past", "old", "last", "earlier", "other", "another", "same",
))


def _names_their_chats(clean):
    tokens = re.findall(r"[a-z']+", clean)
    for index, word in enumerate(tokens):
        if word not in CHAT_WORDS:
            continue
        if index and tokens[index - 1] in THEIR_OWN_WORD:
            return True
        if index > 1 and tokens[index - 2] in THEIR_OWN_WORD:
            return True
        if index > 1 and tokens[index - 2] in CHAT_WORDS:
            return True
    return False


def about_earlier_chats(text, memory):
    if not text:
        return None
    clean = " ".join(text.lower().replace("\u2019", "'").split()).strip(" ?.!,")
    if not clean:
        return None
    if not _names_their_chats(clean) and not SAID_IN_A_PAST_CHAT.search(clean):
        return None
    if _names_their_chats(clean):
        if not (THE_OTHER_CHATS.search(clean) or A_RECORD_OF_THEM.search(clean)):
            return None
        if not (OTHER_THAN_THIS.search(clean) or A_RECORD_OF_THEM.search(clean)
                or A_HAND_ON_THEM.search(clean)):
            return None
    if not re.search(r"\b(?:you|your|u|show me)\b", clean) \
            and not A_RECORD_OF_THEM.search(clean):
        return None
    return pick(NO_OTHER_CHATS, memory, text)


def learns_from_the_chat(text, memory):
    if not text:
        return None
    clean = " ".join(text.lower().replace("\u2019", "'").split()).strip(" ?.!,")
    if not clean or not LEARNING_ASK.search(clean):
        return None
    if not re.search(r"\b(?:you|u)\b", clean):
        return None
    if not TAUGHT_BY_THIS.search(clean):
        if not (_names_their_chats(clean)
                and re.search(r"\b(?:these|this|our|the)\b", clean)):
            return None
    if re.search(r"\b(?:help|teach|show) me\b", clean) \
            or re.search(r"\bhow (?:do|can|could) i\b", clean):
        return None
    return pick(NO_TRAINING, memory, text)


WHEN_I = re.compile(r"^(?:when|what time|what day|which day|what days|which days|how many hours)"
                    r"\s+(?:do|did|will|should|am|can|have)\s+i\b(.*)$")
PAY_DAY = re.compile(r"^when(?:s| is| was)?\s+(?:my\s+)?pay ?day$")

ROTA_WORDS = frozenset(("work", "works", "working", "shift", "shifts", "rota", "hours",
                        "overtime", "oncall"))
ROTA_NOUNS = frozenset(("shift", "shifts", "rota", "hours", "overtime", "oncall"))
PAY_WORDS = frozenset(("paid", "payday", "wage", "wages", "salary"))

ON_THE_ROTA = (
    "Your rota isn't something I can see, so read the hours off it and tell me and I'll keep them.",
    "That lives on your rota rather than anywhere I can see, so tell me what it says.",
    "No window on your rota from this end, sorry, so say the hours and I'll remember them.",
)
ON_THE_PAYSLIP = (
    "A pay date is set in your contract, not known here, so tell me the date and I'll keep it.",
    "Your pay date is on the contract you signed, so say it once and I'll remember it.",
)
_THE_PLACE = {"rota": ON_THE_ROTA, "payslip": ON_THE_PAYSLIP}


def _the_place(text):
    if PAY_DAY.match(text):
        return "payslip"
    for pattern in (WHEN_I, WHEN_MY, WHEN_AUX_MY):
        found = pattern.match(text)
        if not found:
            continue
        tail = set(re.findall(r"[a-z]+", found.group(1)))
        if tail & PAY_WORDS or ("pay" in tail and ("in" in tail or "into" in tail)):
            return "payslip"
        if tail & ROTA_WORDS:
            said = found.group(1)
            if not (tail & ROTA_NOUNS):
                if re.search(r"\bon[-\s]?call\b", said):
                    return "rota"
                said = re.sub(r"\bwork(?:s|ing)?\s+(?:out|on)\b", "", said)
                tail = set(re.findall(r"[a-z]+", said))
                if tail & ROTA_WORDS:
                    return "rota"
                return None
            return "rota"
        return None
    return None


def _has_a_shape(text):
    if HOW_MANY.match(text) or HOW_MANY_GOT.match(text) or HOW_OLD.match(text):
        return True
    return any(pattern.match(text) for pattern in (WHAT_MY, WHEN_MY, WHERE_MY))


def _as_clause(text):
    found = HOW_MANY.match(text) or HOW_MANY_GOT.match(text)
    if found:
        many, thing = found.groups()
        return f"how {many} {thing} you have"
    if HOW_OLD.match(text):
        return "how old you are"
    for pattern in (WHAT_MY, WHEN_MY, WHERE_MY):
        found = pattern.match(text)
        if found:
            tail = found.group(1).strip()
            if re.search(r"\bcalled$", tail):
                return f"what your {tail}"
            if pattern is WHEN_MY:
                return f"when your {tail} is"
            if pattern is WHERE_MY:
                return f"where your {tail} is"
            return f"what your {tail} is"
    return None


def _as_question(clause):
    if clause.startswith(("how many", "how much")):
        return clause.replace(" you have", " do you have")
    if clause.startswith("how old you are"):
        return "how old are you"
    for head, ask in (("what your ", "what is "), ("when your ", "when is "),
                      ("where your ", "where is ")):
        if clause.startswith(head):
            tail = clause[len(head):]
            if tail.endswith(" is"):
                tail = tail[:-3]
            return ask + "your " + tail
    return clause


NOT_A_NOUN_PHRASE = re.compile(r"\b(?:to|for|with|about|at|in|on|from|by|due|like|doing|going|"
                               r"coming|getting|allowed|before|after|now|then|anymore|"
                               r"originally|anyway)\b|\w+ing\b")


def _the_thing(text):
    words = re.findall(r"[a-z]+", text)
    for word in words:
        if word in OWN_WORDS:
            return word
    for word in words:
        if word.endswith("s") and word[:-1] in OWN_WORDS:
            return word[:-1]
    return None


def _second_person(text):
    out = re.sub(r"\b(whats|wheres|whens|hows)\b",
                 lambda m: {"whats": "what's", "wheres": "where's", "whens": "when's",
                            "hows": "how's"}[m.group(1)], text)
    out = re.sub(r"\bmy\b", "your", out)
    out = re.sub(r"\bdo i have\b", "do you have", out)
    out = re.sub(r"\bhave i got\b", "have you got", out)
    out = re.sub(r"\bam i\b", "are you", out)
    return out


def _capital(clause):
    return clause[:1].upper() + clause[1:]


def answer_for(text, memory):
    if not text:
        return None
    clean = " ".join(text.lower().replace("\u2019", "'").split()).strip(" ?.!,")
    if not clean or len(clean.split()) > 10:
        return None
    if ABOUT_BOT.search(clean) or HOW_TO.search(clean):
        return None
    place = _the_place(clean)
    if place:
        return pick(_THE_PLACE[place], memory, text)
    if SAID_BEFORE.search(clean):
        return None
    if not _the_thing(clean) and not HOW_OLD.match(clean):
        return None
    if not _has_a_shape(clean):
        return None
    clause = _as_clause(clean)
    if clause and NOT_A_NOUN_PHRASE.search(clause.split("your", 1)[-1]):
        clause = None
    if clause is None:
        return pick(AS_THE_QUESTION, memory, text).format(
            Q=_capital(_second_person(clean)), q=clean)
    pool = HAVEN_T_SAID if len(clause.split()) > 4 else AS_THE_QUESTION
    line = pick(pool, memory, text)
    question = _capital(_second_person(clean))
    return line.format(q=clause, Q=question)


SAID_ASK = re.compile(
    r"\b(?:(where|what|when|why|who|how\s+often|how\s+many\s+times)\s+)?"
    r"did\s+(?:i|we)\s+(?:ever\s+)?(?:say|tell\s+you|mention)\b", re.I)
FREQUENCY_ASK = re.compile(r"\bhow\s+(?:often|many\s+times)\b", re.I)
PROPERTY_ASK = re.compile(
    r"\bhow\s+(?:old|big|heavy|long|far|tall|late|early)\b|\bwhat\s+colou?r\b", re.I)

A_RATE = re.compile(r"\b\d+\s*(?:times?|x)\b|\b(?:once|twice|daily|weekly|monthly)\b"
                    r"|\bevery\s+(?:day|week|month|year|morning|night)\b")
GENERIC_WORDS = frozenset("""go goes going went do does doing get gets got have has had make makes
made take takes took put see saw look start stop carry""".split())
SAID_POOL = (
    "You told me: \u201c{said}\u201d",
    "That was you, not me: \u201c{said}\u201d",
    "From your own words: \u201c{said}\u201d",
)
NOT_A_RECORD = (
    "You've not said that to me yet, so there's nothing to hand back - tell me and I'll keep it.",
    "I've nothing on that from you: it's yours to tell me, and then it's kept.",
)
NOT_A_RECORD_BUT = (
    "You've not said that to me, but the nearest you've given me is: \u201c{said}\u201d",
    "Nothing of yours on that yet - the closest is \u201c{said}\u201d, and I'll keep the rest when you say it.",
)


def _their_own_lines(memory):
    lines = []
    for turn in reversed((memory or {}).get("turns") or []):
        said = str((turn or {}).get("user") or "").strip()
        if said and said.lower() not in [line.lower() for line in lines]:
            lines.append(said)
    for topic in reversed((memory or {}).get("topics") or []):
        said = str((topic or {}).get("text") or "").strip()
        if said and said.lower() not in [line.lower() for line in lines]:
            lines.append(said)
    return lines


def _stem(word):
    word = word.lower()
    for tail in ("ing", "ed", "es", "s"):
        if len(word) > 4 and word.endswith(tail):
            return word[: -len(tail)]
    return word


def said_back(text, memory):
    if not text:
        return None
    clean = " ".join(text.lower().replace("\u2019", "'").split()).strip(" ?.!,")
    found = SAID_ASK.search(clean)
    if not found:
        return _the_one_rate_on_record(clean, memory, text)
    lines = [line for line in _their_own_lines(memory)
             if _stemmed(line) != _stemmed(clean)]
    if not lines:
        return pick(NOT_A_RECORD, memory, text)
    if FREQUENCY_ASK.search(clean):
        for line in lines[:8]:
            if A_RATE.search(line):
                return pick(SAID_POOL, memory, text).format(said=line)
    asked = [_stem(word) for word in re.findall(r"[a-z']+", clean[found.end():])
             if word not in STOP_WORDS and _stem(word) not in GENERIC_WORDS]
    best, best_score = lines[0], 0
    for line in lines[:8]:
        words = {_stem(word) for word in re.findall(r"[a-z']+", line)}
        score = sum(1 for word in asked if word in words)
        if score > best_score:
            best, best_score = line, score
    if asked and not best_score:
        return pick(NOT_A_RECORD_BUT, memory, text).format(said=lines[0])
    if PROPERTY_ASK.search(clean) and not re.search(r"\d", best):
        return pick(NOT_A_RECORD_BUT, memory, text).format(said=best)
    return pick(SAID_POOL, memory, text).format(said=best)


HOW_OFTEN_MINE = re.compile(r"^how\s+(?:often|many\s+times)\s+(?:do|did|does)\s+(?:i|we)\s+"
                            r"(\w+)(?:\s+(?:it|that|this|them|now))?$", re.I)


def _stemmed(line):
    return " ".join(_stem(word) for word in re.findall(r"[a-z']+", str(line or "").lower()))


def _the_one_rate_on_record(clean, memory, text):
    found = HOW_OFTEN_MINE.match(clean)
    if not found:
        return None
    rates = [rate for rate in (memory or {}).get("rates") or [] if rate.get("said")]
    if len(rates) != 1:
        return None
    rate = rates[0]
    verb = _stem(found.group(1))
    what = _stem(re.sub(r"[^a-z]", " ", str(rate.get("what") or "").lower()).split()[0]) \
        if rate.get("what") else ""
    if verb not in GENERIC_WORDS or verb == what:
        return None
    return pick(SAID_POOL, memory, text).format(said=rate["said"])
