import re

LEAD = re.compile(
    r"^\W*(?:(?:ok|okay|right|so|yes|yeah|and)\b[\s,]*)*"
    r"(?:(?:and|but|or)\s+)?"
    r"(?:(?:what|how)\s+about|what\s+of|and|also|plus)\b[\s,]*", re.I)
REPAIR = re.compile(
    r"^\W*(?:(?:no|nope|sorry|apologies|actually|wait|hold on|oops)[\s,.!-]+)*"
    r"(?:i\s+(?:mean|meant|said)(?:\s+to\s+say)?|(?:you\s+)?mean|i\s+did\s+mean)"
    r"[\s,.!-]+", re.I)
TAKE_BACK = re.compile(
    r"^\W*(?:(?:no|nope|wait|hold on|or rather|scratch that|oops)[\s,.!-]+)+", re.I)
A_COURTESY = frozenset("""
    thanks thank thankyou ta cheers mate love hun pal duck fella sir madam
    worries worry anyway anyhow though please fine alright ok okay all much
    """.split())
A_CLAUSE = re.compile(
    r"\b(?:is|are|was|were|isnt|arent|wasnt|werent|does|did|do|doesnt|didnt|dont|has|have|had"
    r"|hasnt|havent|hadnt|will|would|wont|wouldnt|can|cant|could|couldnt|should|shouldnt|must"
    r"|im|ive|id|ill|weve|youre|its|thats|theres)\b", re.I)


def _after_a_take_back(said):
    lead = TAKE_BACK.match(said)
    if not lead:
        return None
    rest = TAIL_OFF.sub("", said[lead.end():].strip(" ?!.,")).strip(" ?!.,")
    if not rest or len(rest.split()) > 3 or A_CLAUSE.search(rest):
        return None
    return rest


THING = re.compile(r"^(?:(?:a|an|the|some|any|another)\s+)?([a-z][a-z' -]{0,24})$", re.I)
ASKS_A_THING = re.compile(
    r"^(?:what|which|how|why|when|where|who|whose|whom)\b"
    r"|^(?:can|could|should|would|will|shall|do|does|did|is|are|was|were|have|has|had|am|may"
    r"|might|must|need)\s+(?:i|we|you|they|it|he|she)\b", re.I)
TAIL_OFF = re.compile(r"[\s,]*(?:\b(?:too|as well|also|instead|then|now|though|please|thanks)\b"
                      r"[\s,.!?]*)+$", re.I)
HEDGE_OFF = re.compile(
    r"[\s,]*(?:\b(?:probably|maybe|perhaps|possibly|definitely|likely|obviously|actually|"
    r"really|sure|suppose|supposedly|hopefully|honestly|frankly)\b"
    r"|\b(?:i|we)\s+(?:think|guess|suppose|reckon|imagine|hope)\b"
    r"|\bof course\b|\bfor now\b|\bright\b|\bok(?:ay)?\b)[\s,.!?]*$", re.I)
DEICTIC = frozenset((
    "it", "its", "it's", "that", "this", "them", "they", "those", "these", "him", "her",
    "one", "ones", "the same", "same", "the other", "rest", "more", "less", "instead",
    "then", "now", "there", "here", "you", "me", "us", "my", "your", "mine", "yours",
))
STOP = frozenset((
    "a", "an", "the", "and", "or", "but", "if", "of", "for", "to", "in", "on", "at", "with",
    "about", "as", "by", "from", "into", "over", "after", "before", "than", "then", "so",
    "i", "im", "i'm", "me", "my", "we", "you", "your", "it", "its", "is", "are", "was",
    "were", "be", "am", "do", "does", "did", "done", "can", "could", "should", "would",
    "will", "shall", "may", "might", "must", "have", "has", "had", "get", "got", "give",
    "make", "much", "many", "long", "how", "what", "when", "where", "which", "who", "why",
    "any", "some", "good", "best", "better", "more", "most", "not", "no", "yes", "please",
    "there", "here", "that", "this", "these", "those", "them", "they", "he", "she", "his",
    "her", "him", "want", "need", "like", "one", "also", "just", "really", "very", "know",
    "tell", "think", "say", "said", "help", "idea", "ideas", "thing", "things", "anything",
    "something", "way", "ways", "time", "times", "kind", "kinds", "sort", "sorts",
))
OPENERS = ("how", "what", "when", "where", "which", "who", "why", "can", "could", "should",
           "would", "do", "does", "did", "is", "are", "was", "were", "will", "shall")
ASK = frozenset(("whats", "hows", "wheres", "whos", "whys", "whens", "whatre", "hows"))


def _said(text):
    return " ".join(str(text or "").lower().split())


def _stem(word):
    word = word.strip("?.!,;:")
    for end in ("ies", "es", "s"):
        if len(word) > 4 and word.endswith(end):
            return word[: -len(end)]
    return word


def thing(text):
    said = _said(text).strip(" ?!.")
    if not said:
        return None
    lead = LEAD.match(said)
    repaired = False
    if lead:
        rest = said[lead.end():]
    else:
        lead = REPAIR.match(said)
        if lead:
            rest = said[lead.end():]
            repaired = True
        else:
            rest = _after_a_take_back(said)
            if rest is None:
                return None
    if repaired and A_CLAUSE.search(rest):
        return None
    rest = TAIL_OFF.sub("", rest.strip(" ?!.,")).strip(" ?!.,")
    for _ in range(3):
        hedged = HEDGE_OFF.sub("", rest).strip(" ?!.,")
        if hedged == rest:
            break
        rest = hedged
    if not rest or len(rest.split()) > 4:
        return None
    found = THING.match(rest)
    if not found:
        return None
    name = found.group(1).strip()
    words = [word for word in re.split(r"[ ']", name) if word]
    if len(words) > 1 and words[0] in OWNER_WORDS:
        words = words[1:]
        name = " ".join(words)
    if not words or len(words) > 3:
        return None
    if name in DEICTIC or " ".join(words) in DEICTIC:
        return None
    if any(word in DEICTIC for word in words):
        return None
    if ASKS_A_THING.search(name):
        return None
    if all(word in STOP for word in words):
        return None
    if all(word in A_COURTESY or word in STOP for word in words):
        return None
    return name


PERSON_LEAD = re.compile(
    r"^\W*(?:(?:ok|okay|right|so|yes|yeah|and)\b[\s,]*)*"
    r"(?:(?:and|but|or)\s+)?"
    r"(?:(?:what|how)\s+about|what\s+of|and|also|plus)\b[\s,]*"
    r"(?:something\s+for|one\s+for|a\s+gift\s+for|the\s+same\s+for|presents?\s+for)?[\s,]*", re.I)
PERSON_FILLER = frozenset((
    "for", "to", "about", "with", "then", "too", "also", "instead", "please", "thanks",
    "the", "a", "an", "get", "buy", "got", "them", "him", "her", "and", "as", "well",
    "his", "hers", "their", "birthday", "christmas", "present", "gift", "presents",
    "gifts",
))


def someone(text):
    from .topics import person

    said = _said(text).strip(" ?!.")
    if not said or len(said.split()) > 6:
        return None
    lead = PERSON_LEAD.match(said) or REPAIR.match(said)
    if not lead:
        return None
    rest = said[lead.end():].strip(" ?!.,")
    who = person(rest)
    if not who:
        return None
    left = re.sub(r"'s\b", "", re.sub(r"\b(?:my|our)\s+" + re.escape(who) + r"\b", " ", rest))
    spare = [word for word in re.split(r"[ ']", left)
             if word and word not in PERSON_FILLER and word not in STOP]
    if spare:
        return None
    return who


def _earlier(memory, text, n=4, wide=False):
    from . import recent

    here = _said(text)
    found = []
    for turn in reversed([t for t in recent(memory, n + 2) if isinstance(t, dict)]):
        question = _said(turn.get("user"))
        if question and (question == here or question == here.rstrip(" ?!.")):
            continue
        answer = _said(turn.get("bot"))
        if len(question.split()) < 3:
            continue
        first = question.split()[0].strip("?,!")
        if not wide and "?" not in question and first not in OPENERS and first not in ASK:
            continue
        found.append((question, answer))
        if len(found) >= n:
            break
    return found


OWNER = frozenset(("my", "our", "your", "their", "his", "her", "the", "a", "an", "some",
                   "this", "that"))


def _about(question):
    from ..understanding import understand

    try:
        read = understand(question, {})
    except Exception:
        return None
    subject = _said((read or {}).get("subject") if isinstance(read, dict) else "")
    subject = subject.strip(" ?!.,")
    if not subject or len(subject.split()) > 3:
        return None
    words = subject.split()
    while words and words[0] in OWNER:
        words = words[1:]
    if not words or all(word in STOP for word in words):
        return None
    return " ".join(words)


OWNER_WORDS = frozenset(("my", "our", "your", "their"))


def _reads_as_a_question(line):
    words = line.split()
    if not words:
        return False
    if "?" in line:
        return True
    first = words[0].strip("?,!")
    return first in OPENERS or first in ASK


def _word(question, answer, new_words, taken_up):
    words = [w.strip("?.!,;:") for w in question.split()]
    for word in reversed(words):
        if word in STOP or len(word) < 3 or not word.isalpha():
            continue
        if word in new_words or word in DEICTIC or word in ASK:
            continue
        if taken_up and not (_stem(word) and _stem(word) in answer):
            continue
        return word
    return None


def _replace(question, word, new):
    found = re.search(r"\b(?:(a|an)\s+)?" + re.escape(word) + r"\b", question, re.I)
    if not found:
        return None
    if found.group(1):
        lead = "an " if new[:1] in "aeiou" else "a "
    else:
        lead = ""
    rewritten = question[:found.start()] + lead + new + question[found.end():]
    rewritten = re.sub(r"\b(\w+)\s+\1\b", r"\1", rewritten)
    if rewritten == question:
        return None
    head = new.split()[-1].lower()
    if len(new.split()) > 1 and rewritten.lower().count(head) > 1:
        return None
    return rewritten


def _spans(question, subject):
    words = [w.strip("?.!,;:") for w in question.split()]
    if " " in subject or subject not in words:
        return [subject]
    at = words.index(subject)

    def may_be_it(word):
        return bool(word) and word.isalpha() and word not in STOP and word not in DEICTIC \
            and word not in ASK

    spans = []
    for back in (2, 1):
        if at - back >= 0 and all(may_be_it(w) for w in words[at - back:at]):
            spans.append(" ".join(words[at - back:at + 1]))
    if at + 1 < len(words) and may_be_it(words[at + 1]):
        spans.append(" ".join(words[at:at + 2]))
    spans.append(subject)
    for back in (2, 1):
        if at - back >= 0 and all(may_be_it(w) for w in words[at - back:at]):
            spans.append(" ".join(words[at - back:at]))
    found, out = set(), []
    for span in spans:
        if span and span not in found:
            found.add(span)
            out.append(span)
    return out


def is_repair(text):
    said = _said(text).strip(" ?!.")
    return bool(REPAIR.match(said)) or _after_a_take_back(said) is not None


def candidates(text, memory, most=3):
    new = thing(text)
    if not new:
        return []
    repaired = is_repair(text)
    new_words = set(re.split(r"[ ']", new))
    place = bool(_the_preposition_of(new))
    found = []
    for question, answer in _earlier(memory, text, wide=repaired):
        subject = _about(question)
        words = []
        if place:
            had = _the_place_after_the_same_preposition(question, new)
            if had:
                words.append(had)
        words += _spans(question, subject) if subject else []
        words += [_word(question, answer, new_words, True),
                  _word(question, answer, new_words, False)]
        for word in words:
            if not word:
                continue
            line = placed(question, word, new) if place else _replace(question, word, new)
            if not line or _a_second_place(question, line, new):
                continue
            if any(line == had for had, _old in found):
                continue
            found.append((line, word))
            if len(found) >= most:
                return found
    return found


def rewritten(text, memory):
    new = thing(text)
    if not new:
        return None
    new_words = set(re.split(r"[ ']", new))
    earlier = _earlier(memory, text, wide=True)
    asked = [(line, answer) for line, answer in earlier if _reads_as_a_question(line)]
    told = [(line, answer) for line, answer in earlier if not _reads_as_a_question(line)]
    for taken_up in (True, False):
        for question, answer in asked:
            if not answer:
                continue
            swap = _word(question, answer, new_words, taken_up)
            if not swap:
                continue
            candidate = placed(question, swap, new)
            if candidate and candidate != question:
                return candidate, swap
    in_between = thing(earlier[0][0]) if earlier else None
    head = new.split()[-1].strip("?.!,;:").lower() if len(new.split()) > 1 else ""
    if in_between and head not in in_between.split():
        return None
    for question, answer in told:
        if not answer:
            continue
        subject = _about(question)
        for swap in (_spans(question, subject) if subject else []):
            candidate = placed(question, swap, new)
            if candidate and candidate != question:
                return candidate, swap
    return None


def _named_somebody(memory, text, n=4):
    from . import recent

    here = _said(text)
    found = []
    for turn in reversed([t for t in recent(memory, n + 2) if isinstance(t, dict)]):
        line = _said(turn.get("user"))
        if not line or line == here or line == here.rstrip(" ?!."):
            continue
        if len(line.split()) < 3:
            continue
        found.append((line, _said(turn.get("bot"))))
        if len(found) >= n:
            break
    return found


def rewritten_person(text, memory):
    from .topics import person

    who = someone(text)
    if not who:
        return None
    for question, _answer in _named_somebody(memory, text):
        old = person(question)
        if not old or old == who:
            continue
        named = re.compile(r"\b(my|our)\s+" + re.escape(old) + r"\b", re.I)
        found = named.search(question)
        if not found:
            continue
        candidate = named.sub(lambda m: m.group(1) + " " + who, question, count=1)
        if candidate != question:
            return candidate, old
    return None


def names_person(old, answer, text, last=""):
    who = someone(text)
    said = _said(answer)
    if not who or not said:
        return False
    if old and re.search(r"\b" + re.escape(old) + r"\b", said):
        return False
    return not last or said != _said(last)


DETERMINER = frozenset("""the a an my your his her its their our this that these those some any
another""".split())
PREPOSITION = frozenset("""in on at for with from by to near inside outside under over behind
above below beneath underneath between beside besides alongside around across along through
against towards toward onto upon within without off out up down past opposite round via
about""".split())
PREPOSITION_TAIL = frozenset("""next close right just all the top bottom front back inside
outside end side""".split())


def _the_preposition_of(new):
    words = str(new or "").split()
    if not words:
        return ""
    head = words[0].strip("?.!,;:").lower()
    return head if head in PREPOSITION else ""


def _the_place_after_the_same_preposition(question, new):
    head = _the_preposition_of(new)
    if not head:
        return None
    said = question.split()
    for at, word in enumerate(said):
        if word.strip("?.!,;:").lower() != head:
            continue
        after = at + 1
        while after < len(said) and said[after].strip("?.!,;:").lower() in DETERMINER:
            after += 1
        span = []
        for follow in said[after:]:
            bare = follow.strip("?.!,;:")
            if not bare.isalpha() or bare.lower() in STOP or bare.lower() in PREPOSITION:
                break
            span.append(bare)
            if len(span) == 2:
                break
        if span:
            return " ".join(span)
    return None


def _a_second_place(question, line, new):
    head = _the_preposition_of(new)
    if not head:
        return False

    def count(text):
        return sum(1 for word in str(text or "").split()
                   if word.strip("?.!,;:").lower() == head)

    return count(line) > count(question)


def placed(question, old, new):
    words = question.split()
    new_words = new.split()
    at = next((i for i, word in enumerate(words) if word.strip("?.!,;:") == old), None)
    if at is None or not new_words:
        return None
    head = new_words[0].strip("?.!,;:").lower()
    if head in PREPOSITION or head in PREPOSITION_TAIL:
        start = at
        while start > 0 and words[start - 1].strip("?.!,;:").lower() in DETERMINER:
            start -= 1
        if start == 0 or words[start - 1].strip("?.!,;:").lower() not in PREPOSITION:
            return " ".join(words[:start] + new_words + words[at + 1:])
        start -= 1
        if start > 0 and words[start - 1].strip("?.!,;:").lower() in PREPOSITION_TAIL:
            start -= 1
        return " ".join(words[:start] + new_words + words[at + 1:])
    rewritten = question.replace(old, new, 1)
    head = new_words[-1].strip("?.!,;:").lower()
    if len(new_words) > 1 and rewritten.lower().count(head) > 1:
        return None
    return rewritten


def _said_again(answer, memory):
    if not isinstance(memory, dict):
        return False
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns or not isinstance(turns[-1], dict):
        return False
    last = str(turns[-1].get("bot") or "")
    if not last.strip():
        return False
    return (" ".join(str(answer or "").lower().split())
            == " ".join(last.lower().split()))


def _brings_its_own_place(new):
    words = str(new or "").split()
    return bool(words) and words[0].strip("?.!,;:").lower() in PREPOSITION


def names(old, answer, text, memory=None, question=None):
    new = thing(text)
    said = _said(answer)
    if not new or not said:
        return False
    if _said_again(answer, memory):
        return False
    fresh = [word for word in re.split(r"[ ']", new) if word and word not in STOP]
    if any(_stem(word) in said for word in fresh):
        return True
    if _brings_its_own_place(new):
        asked = [word for word in re.split(r"[ ']", _said(question))
                 if word and word not in STOP]
        return any(_stem(word) in said for word in asked)
    return _stem(old or "") not in said
