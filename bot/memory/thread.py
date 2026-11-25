import re

from ..understanding import understand
from ..understanding.kinds import NEGATIVE, POSITIVE, VERB_FORMS, VERBISH
from ..understanding.normalize import IRREGULAR_PARTICIPLES
from ..understanding.topics import PLACES as PLACE_WORDS
from ..compose import pick
from . import detail
from . import _from_the_bot, _to_the_bot
from .facts import no_tone

THIN = frozenset(("ok", "okay", "k", "cool", "nice", "great", "good", "yeah", "yep", "yes",
                  "no", "nah", "nope", "lol", "haha", "ha", "mm", "hmm", "right", "fair",
                  "sure", "same", "true", "thanks", "thx", "ta", "cheers", "please"))

CLOSINGS = frozenset(("night", "nite", "goodnight", "goodnite", "nighty", "bed", "bedtime",
                      "bye", "byebye", "cya", "sleep"))

CLOSING_FILLER = frozenset(("right", "ok", "okay", "well", "anyway", "im", "i", "am", "we",
                            "were", "re", "going", "gonna", "gotta", "off", "to", "the", "a",
                            "now", "so", "then", "just", "time", "for", "up"))

SIGNS_OFF = re.compile(
    r"^(?:(?:" + "|".join(sorted(CLOSING_FILLER, key=len, reverse=True)) + r")\s+)*"
    r"(?:" + "|".join(sorted(CLOSINGS, key=len, reverse=True)) + r")$")

WEAK = frozenset(("name", "time", "day", "week", "weekend", "month", "year", "thing", "lot",
                  "bit", "way", "kind", "sort", "part", "place", "trip", "plan", "idea",
                  "question", "answer", "chat", "talk", "conversation", "help", "advice"))

NON_NOUN = WEAK | THIN | frozenset((
    "before", "after", "again", "still", "just", "only", "maybe", "perhaps", "really",
    "nervous", "worried", "scared", "fine", "ok", "better", "worse", "best", "worst",
    "one", "ones", "two", "three", "first", "last", "next", "ask", "asked", "say", "said",
    "want", "need", "try", "trying", "started", "start", "stop", "make", "made", "get",
    "getting", "think", "thought", "going", "went", "come", "came", "much", "many", "more",
    "less", "all", "any", "some", "else", "something", "anything", "everything", "nothing",
    "remember", "recall", "forget", "said", "saying", "talked", "covered", "discussed", "meant",
    "rid",
))

LEAD = ("by the way", "btw", "anyway", "anyways", "so", "and", "but", "ok", "okay", "well",
        "oh", "ah", "right", "great", "sorry", "also", "then", "now", "ha", "hmm", "just",
        "cool", "nice", "yes", "yeah")

MODAL = frozenset(("would", "should", "will", "can", "could", "may", "might", "must", "shall",
                   "ought"))
AUX = frozenset(("am", "is", "are", "was", "were", "do", "does", "did", "have", "has", "had",
                 "can", "could", "will", "would", "shall", "should", "may", "might", "must"))
WH = frozenset(("what", "why", "how", "when", "where", "who", "whom", "whose", "which"))
PRONOUN = frozenset(("i", "we", "you", "it", "they", "he", "she", "this", "that", "there",
                     "the", "a", "an", "my", "our", "your"))
SUBJECTISH = PRONOUN | frozenset(("people", "anyone", "someone", "everyone", "kids", "children"))

FLIP = {"i": "you", "me": "you", "my": "your", "mine": "yours", "myself": "yourself",
        "we": "you", "us": "you", "our": "your", "ours": "yours", "ourselves": "yourselves",
        "i'm": "you're", "i've": "you've", "i'd": "you'd", "i'll": "you'll",
        "we're": "you're", "we've": "you've", "we'd": "you'd", "we'll": "you'll",
        "im": "you're", "ive": "you've", "am": "are"}

PLACE_NAMES = frozenset(("place", "name"))
CALENDAR = frozenset("""today tomorrow yesterday tonight morning afternoon evening night week
weekend month year hour minute second monday tuesday wednesday thursday friday saturday sunday
january february march april may june july august september october november december
spring summer autumn winter christmas easter holidays""".split())
QUALITY = POSITIVE | NEGATIVE

CONTRACTIONS = frozenset(("it's", "that's", "there's", "they're", "we're", "he's", "she's",
                          "you're", "i'm", "i've", "i'd", "i'll", "there", "it", "this",
                          "that", "they", "these", "those", "here"))


def _asks_about_the_bot(reading):
    return bool(reading.get("about_bot"))


def _asks_about_the_chat(text, memory, skip):
    return bool(skip) and bool(skip(text, memory))


def _turns(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    return turns if isinstance(turns, list) else []


def earlier_turn(memory):
    return any(isinstance(turn, dict) and (turn.get("user") or turn.get("reply"))
               for turn in _turns(memory))


_ONLY_THE_ARRIVAL = re.compile(
    r"^(?:(?:hi|hiya|hey|hello|ok|okay|right|so|well|anyway)[,\s]+)*"
    r"(?:im|i am|iam|we are|were|we're)?\s*back"
    r"(?:\s+(?:again|home|now|too|from\s+(?:work|the\s+\w+|holiday|holidays|town|"
    r"school|shopping|the\s+shop|hospital|abroad|lunch|a\s+break)))?"
    r"[\s.!?]*$")


def only_the_arrival(text):
    said = str(text or "").strip().lower().replace("'", "")
    said = re.sub(r"[.,!?]+", " ", said)
    return bool(_ONLY_THE_ARRIVAL.match(" ".join(said.split())))


def user_lines(memory):
    out = []
    for turn in _turns(memory):
        text = turn.get("user") if isinstance(turn, dict) else None
        if isinstance(text, str) and text.strip():
            out.append((text, understand(text, {})))
    return out


RECEIPT_WORDS = frozenset("""
got it alright then will do ok okay right noted thanks thank you ta cheers sure cool great
nice one lovely perfect brilliant grand fine fair enough no worries problem understood
makes sense course yes yeah yep yup mhm okay-doke done
""".split())
RECEIPT_LONGEST = 4


def _is_a_receipt(reading):
    words = [w.strip(".,!?-\u2014\u2013()") for w in reading.get("words") or []]
    words = [w.lower() for w in words if w]
    return bool(words) and len(words) <= RECEIPT_LONGEST and \
        all(w in RECEIPT_WORDS for w in words)


def _is_thin(reading):
    words = [w.strip(".,!?") for w in reading.get("words") or []]
    if not words:
        return True
    if _is_a_receipt(reading):
        return True
    return len(words) <= 2 and all(w in THIN for w in words)


def signs_off(text):
    reading = understand(text, {})
    words = [w.strip(".,!?") for w in reading.get("words") or []]
    if not words:
        return False
    if reading.get("intent") == "farewell":
        return True
    return bool(SIGNS_OFF.match(" ".join(words)))


def carries_subject(text):
    said = restate(text) or ""
    return bool(said) and _is_subject_phrase(said)


def thin(text):
    reading = understand(text, {})
    return _is_thin(reading) or _is_memory_line(reading)


POINTS_BACK = re.compile(
    r"^(?:and |so |but |or |ok |okay |well |no |nah |yes |yeah |right |actually |sorry |please"
    r"|how about |what about )*"
    r"(?:"
    r"(?:the )?same(?: one| thing)?"
    r"(?: as (?:before|last time|last night|last week|last year|yesterday|the other day"
    r"|the usual|usual|that|then|them|it|earlier))?"
    r"|(?:just )?like (?:before|last time|last night|last week|yesterday|the usual|that|them|it)"
    r"|(?:anything|something|what) else like (?:that|before|it|them)"
    r"|the usual"
    r"|as (?:we|i) (?:said|discussed|agreed)"
    r"|(?:the )?(?:other|second|first|last) one"
    r"|(?:that|this) one"
    r"|(?:the )?(?:same|other) thing"
    r"|(?:do |try |use )?what (?:you|we) said"
    r"|the thing (?:you|we) said"
    r"|(?:sorry )?(?:i|we) meant (?:the )?(?:other|that)(?: one| thing)?"
    r")"
    r"(?: (?:then|please|again|really|though|now|too|instead))*$")


def points_back(text):
    low = " ".join(str(text or "").lower().replace("'", "").split()).strip(" .!?,")
    return bool(low) and len(low.split()) <= 6 and bool(POINTS_BACK.match(low))


POINTING_WORD = re.compile(r"\b(?:it|that|this|them|those|these|one|ones|there)\b", re.I)
ASK_WORD = frozenset("""how what when where why which who whose do does did doing done can could
should would will shall am is are was were be been being have has had may may might must i you we
me my our your it that this them those these there one ones a an the and or but so then again
please about for of in on at to with from much many long soon often far time worth better best
good right now just really any ok okay well hey hmm hm oh ah sorry up down off out back
away over around through""".split())
ASK_VERB = frozenset("""do does did make makes get gets take takes cost costs try use uses go goes
work works need needs start starts keep keeps put puts cook cooks buy buys fix fixes help helps
worth better eat eats drink drinks say says""".split())


A_CHOICE = re.compile(r"\bwhich\b[^?]*\b(?:should|better|best|instead)\b"
                      r"|\bshould i\b[^?]*\b(?:buy|choose|pick|go for)\b", re.I)


def points_at_a_word_alone(text):
    low = " ".join(str(text or "").lower().replace("'", "").split()).strip(" .!?,")
    words = re.findall(r"[a-z]+", low)
    if not words or not POINTING_WORD.search(low):
        return False
    if A_CHOICE.search(low):
        return False
    other = [word for word in words if word not in ASK_WORD and word not in ASK_VERB]
    if not other:
        return any(word in ASK_VERB for word in words)
    if len(other) > 1:
        return False
    at = words.index(other[0])
    return at + 1 < len(words) and bool(POINTING_WORD.fullmatch(words[at + 1]))


WHAT_I_SAID = re.compile(
    r"\bwhat (?:was|were) (?:it )?(?:i|we) (?:(?:was|were|am|are|had been) )?"
    r"(?:worried|upset|angry|annoyed|sad|unhappy|thinking|saying)(?: (?:about|of))?\b", re.I)


def asks_what_i_said(text):
    return bool(WHAT_I_SAID.search(str(text or "")))


def nothing_said(memory):
    return not any(carries_subject(str(turn.get("user") or "")) for turn in _turns(memory))


def _is_memory_line(reading):
    return reading.get("topic_own") in ("about-the-bot", "memory") or \
        reading.get("intent") in ("about_bot", "greeting") or \
        reading.get("kind") in ("greeting", "memory")


def _named_entities(reading):
    out = []
    if _is_memory_line(reading):
        return out
    for entity in reading.get("entities") or []:
        if not isinstance(entity, dict):
            continue
        name = (entity.get("text") or "").strip()
        core = name.lower()
        if not name or core in WEAK or core in FLIP or core in THIN or len(core) <= 2:
            continue
        if core.split()[0] in CONTRACTIONS:
            continue
        if core in MEASURE or name[:1].isdigit():
            continue
        out.append(entity)
    return out


def _groups(entities, reading):
    text = reading.get("norm_text") or ""
    groups = []
    for entity in entities:
        name = entity["text"].strip()
        if groups:
            last = groups[-1]
            joined = last[-1]["text"].strip() + " " + name
            if joined.lower() in text:
                last.append(entity)
                continue
        groups.append([entity])
    return groups


VERB_BEFORE = AUX | frozenset(("i", "we", "you", "they", "he", "she", "it", "not",
                              "please", "lets", "let's", "who", "dont", "doesnt", "didnt",
                              "cant", "wont", "wouldnt", "couldnt", "shouldnt"))


def _is_the_verb(reading, word):
    words = [str(w).strip(".,!?").lower() for w in (reading.get("words") or [])]
    for index in range(len(words) - 1, -1, -1):
        token = words[index]
        if token != word.lower() and not token.startswith(word.lower()):
            continue
        return index > 0 and words[index - 1] in VERB_BEFORE
    return False


def _verb_after_a_subject(reading, word):
    if not word.endswith("s") or word.endswith("ss") or len(word) < 3:
        return False
    words = [str(w).strip(".,!?").lower() for w in (reading.get("words") or [])]
    for index in range(len(words) - 1, -1, -1):
        token = words[index]
        if token != word.lower() and not token.startswith(word.lower()):
            continue
        if index < 2:
            return False
        before, owner = words[index - 1], words[index - 2]
        return owner in DETERMINERS or owner in ("my", "our", "your", "his", "her", "their")
    return False


def _word_behind_prep(reading, word):
    words = [str(w).lower() for w in (reading.get("words") or [])]
    for index in range(len(words) - 1, -1, -1):
        if words[index] != word.lower():
            continue
        before = index - 1
        while before >= 0 and words[before] in DETERMINERS:
            before -= 1
        if before >= 0 and words[before] in PREP:
            return True
    return False


def _behind_a_prep(reading, entity):
    words = reading.get("words") or []
    at = entity.get("at")
    if not isinstance(at, int) or at <= 0 or at > len(words):
        return False
    before = [w.lower() for w in words[max(0, at - 2):at]]
    while before and before[-1] in DETERMINERS:
        before.pop()
    return bool(before) and before[-1] in PREP


def _the_phrase_around(reading, word):
    words = [str(w).strip(".,!?").lower() for w in (reading.get("words") or [])]
    for index, token in enumerate(words):
        if token != word.lower() and not token.startswith(word.lower()):
            continue
        before = words[index - 1] if index else ""
        if before in ("my", "our", "your"):
            return ("your", word)
        if before in DETERMINERS:
            return (before, word)
        return ()
    return ()


def _phrase_for(text, reading, named_only=False):
    keywords = [w for w in reading.get("keywords") or [] if w not in WEAK and w not in THIN]
    entities = _named_entities(reading)
    chosen = None
    for kind in ("place", "person", "name", "thing"):
        groups = _groups([e for e in entities if e.get("type") == kind], reading)
        if kind in ("person", "thing"):
            groups = [g for g in groups if not _behind_a_prep(reading, g[0])]
        if groups:
            chosen = groups[-1]
            break
    if chosen:
        name = " ".join(e["text"].strip() for e in chosen)
        before = _qualifier(reading, name, keywords)
        if before:
            name = before + " " + name
        name = _same_spelling(text, name)
        kind = chosen[0].get("type")
        if name.lower().startswith("my "):
            name = "your " + name[3:]
        if kind in PLACE_NAMES or kind == "name" or name[:1].isupper():
            return _place_case(name)
        if name.lower().startswith(("your ", "a ", "an ", "the ")):
            return name
        return "the " + name
    nouns = [w for w in keywords
             if not w.endswith(("ing", "ed")) and w not in NON_NOUN
             and w not in QUALITY and w not in CALENDAR
             and not _is_the_verb(reading, w)
             and not _verb_after_a_subject(reading, w)]
    if not nouns:
        return None
    things = [w for w in nouns if w not in VERB_FORMS]
    if things:
        nouns = things
    kept = [w for w in nouns if w in PLACE_WORDS or not _word_behind_prep(reading, w)]
    if kept and len(kept) < len(nouns):
        nouns = kept
    if nouns[-1] in PLACE_WORDS:
        return _place_case(_same_spelling(text, nouns[-1]))
    around = _the_phrase_around(reading, nouns[-1])
    if named_only and not around:
        return None
    if around and around[0] == "your":
        return "your " + nouns[-1]
    return "the " + nouns[-1]


def _place_case(name):
    words = name.split()
    if not words:
        return name
    if name.lower() in PLACE_WORDS or all(w.lower() in PLACE_WORDS for w in words):
        return " ".join(_capital(w) for w in words)
    return name


def _same_spelling(text, phrase):
    lowered = text.lower()
    index = lowered.find(phrase.lower())
    if index >= 0:
        return text[index:index + len(phrase)]
    return phrase


DETERMINERS = frozenset(("a", "an", "the", "my", "your", "our", "their", "his", "her",
                         "its", "this", "that", "these", "those", "some", "any", "many",
                         "much", "no", "every", "each"))


def _qualifier(reading, phrase, keywords):
    text = reading.get("norm_text") or ""
    index = text.find(phrase.lower())
    if index <= 0:
        return None
    words = text[:index].split()
    if len(words) < 2:
        return None
    before = words[-1].strip(".,!?")
    if before not in keywords or words[-2].strip(".,!?") not in DETERMINERS:
        return None
    return before


def about(memory, skip=None):
    lines = [(text, reading) for text, reading in user_lines(memory)
             if not _is_thin(reading) and not _is_memory_line(reading)
             and not _asks_about_the_chat(text, memory, skip)
             and not _asks_about_the_bot(reading)
             and not signs_off(text)]
    for pass_kind in ("entity", "statement", "any"):
        for text, reading in reversed(lines):
            names_something = bool(_named_entities(reading))
            if pass_kind == "entity" and not names_something:
                continue
            if pass_kind == "statement" and reading.get("kind") == "question" \
                    and not names_something:
                continue
            if pass_kind != "entity" and (reading.get("intent") == "feeling"
                                          or reading.get("topic_own") == "feelings"):
                continue
            phrase = _phrase_for(text, reading, named_only=pass_kind == "any")
            if phrase and _is_subject_phrase(phrase):
                return phrase
    return _from_topics(memory)


BARE_VERBS = frozenset("""do give get go try keep sort call tell know feel be been have wait
    stop start find leave come put use take see say think love like want look check help send
    make book buy fix sort plan""".split())


NUMBER_WORD_HEADS = frozenset("""
zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen
sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety
hundred thousand million
""".split())


def _is_subject_phrase(phrase):
    words = [w.strip(",.;:") for w in str(phrase or "").split()]
    if len(words) > 1 and words[0].lower() in DETERMINERS:
        words = words[1:]
    head = words[0].lower() if words else ""
    if not head:
        return False
    try:
        from ..memory import topics as _topics
    except ImportError:
        return True
    if head.isdigit() or head in NUMBER_WORD_HEADS:
        return False
    return not (head in _topics.GREET or head in _topics.ACKS or head in BARE_VERBS)


def _from_topics(memory):
    try:
        from ..memory import topics
    except ImportError:
        return None
    phrase = " ".join(str(topics.subject(memory) or "").split())
    if not phrase:
        return None
    if not _is_subject_phrase(phrase):
        return None
    words = phrase.split()
    if words[0].lower() in DETERMINERS or words[0][:1].isupper():
        return phrase
    return "the " + phrase


ASK_WORDS = {"how_long": ("how", "long"), "how_much": ("how", "much"),
             "how_many": ("how", "many"), "how_far": ("how", "far"),
             "how_often": ("how", "often")}


def _is_wh(word):
    core = str(word or "").strip(".,!?").lower().replace("'", "").replace("\u2019", "")
    if core in WH:
        return True
    return core.endswith("s") and core[:-1] in WH


def _with_wh(reading, words):
    if reading.get("kind") != "question" or not words:
        return words
    if _is_wh(words[0]):
        return words
    held = {str(word).strip(".,!?;:").lower() for word in words}
    norm = [str(word).strip(".,!?").lower() for word in reading.get("norm") or []]
    for index, word in enumerate(norm):
        if word not in WH:
            continue
        phrase = []
        for word2 in norm[index:index + 3]:
            if phrase and (word2 in AUX or word2 in SUBJECTISH or word2 in ("the", "a", "an")):
                break
            phrase.append(word2)
        if phrase and str(phrase[0]).lower() not in held:
            return phrase + list(words)
        break
    for ask in reading.get("asks") or []:
        phrase = ASK_WORDS.get(ask) or ((ask,) if ask in WH else ())
        if phrase and str(phrase[0]).lower() not in held:
            return list(phrase) + list(words)
    return words


def _strip_lead(words):
    words = list(words)
    changed = True
    while changed and words:
        changed = False
        for lead in LEAD:
            parts = lead.split()
            if words[:len(parts)] == parts:
                words = words[len(parts):]
                changed = True
    return words


ADDRESSEE = {"you": "me", "your": "my", "yours": "mine", "yourself": "myself",
             "you're": "i am", "youve": "i have", "you've": "i have", "you'd": "i would",
             "you'll": "i will"}
SUBJECT_YOU = "I"


LOST_SUBJECT = frozenset((
    "cant", "can't", "couldnt", "couldn't", "dont", "don't", "didnt", "didn't", "wont", "won't",
    "havent", "haven't", "hadnt", "hadn't", "wouldnt", "wouldn't", "shouldnt", "shouldn't",
))

DROPPED_SUBJECT = LOST_SUBJECT | frozenset(("am", "is", "are", "was", "were", "will", "might"))

SECOND_PERSON = {"am": ("you", "are"), "is": ("you", "are"), "are": ("you", "are"),
                 "was": ("you", "were"), "were": ("you", "were")}


def _with_you(words):
    if not words:
        return ["you"]
    first = (words[0].strip(".,!?;:") or "").lower()
    lead = SECOND_PERSON.get(first)
    if lead is not None:
        return list(lead) + list(words[1:])
    return ["you"] + list(words)


FIRST_PERSON_AUX = {"are": "am", "were": "was", "is": "am", "am": "am"}


def _first_person_aux(word):
    core = word.strip(".,!?;:")
    tail = word[len(core):]
    return FIRST_PERSON_AUX.get(core.lower(), core) + tail


def _flip(words, addressee=False):
    out = []
    for index, word in enumerate(words):
        core = word.strip(".,!?;:")
        tail = word[len(core):]
        if addressee and core in ADDRESSEE:
            before = words[index - 1].strip(".,!?;:").lower() if index else ""
            if core == "you" and (not index or before in AUX or before in WH):
                if out:
                    out[-1] = _first_person_aux(out[-1])
                out.append(SUBJECT_YOU + tail)
            else:
                out.append(ADDRESSEE[core] + tail)
            continue
        out.append(FLIP.get(core, core) + tail)
    return out


EXPAND = {
    "i'm": "i am", "im": "i am", "i've": "i have", "i'd": "i would", "i'll": "i will",
    "it's": "it is", "that's": "that is", "there's": "there is", "what's": "what is",
    "we're": "we are", "they're": "they are", "you're": "you are", "he's": "he is",
    "she's": "she is", "don't": "do not", "doesn't": "does not", "didn't": "did not",
    "can't": "cannot", "won't": "will not", "isn't": "is not", "aren't": "are not",
    "wasn't": "was not", "weren't": "were not", "haven't": "have not", "hasn't": "has not",
    "couldn't": "could not", "wouldn't": "would not", "shouldn't": "should not",
}


def your_words(text):
    words = str(text or "").split()
    return " ".join(_flip(words))


def _expand(text):
    words = [EXPAND.get(word.strip(".,!?;:").lower(), word) for word in str(text or "").split()]
    return " ".join(words).strip(" ,;:").rstrip(".")


def _as_text(value):
    if isinstance(value, (list, tuple)):
        return " ".join(str(w) for w in value).strip()
    return str(value or "").strip()


PREDICATE = frozenset((
    "safe", "ok", "okay", "normal", "fine", "good", "bad", "better", "worse", "worth",
    "hard", "easy", "difficult", "available", "allowed", "legal", "dangerous", "broken",
    "working", "fixed", "cheap", "cheaper", "expensive", "possible", "true", "wrong",
    "open", "closed", "included", "covered", "needed", "sick", "ill", "dead", "alive",
    "serious", "urgent", "done", "ready", "likely", "fair", "free", "late", "busy",
    "hot", "cold", "warm", "healthy", "insured", "enough"))
PREP = frozenset(("to", "for", "in", "on", "at", "with", "from", "by", "about", "of",
                  "than", "after", "before", "during", "into", "over", "under", "out",
                  "up", "down", "when", "if", "because", "as", "so", "like", "near"))
MEASURE = frozenset((
    "pound", "pounds", "quid", "euro", "euros", "dollar", "dollars", "cent", "cents", "penny",
    "kilo", "kilos", "kilogram", "kilograms", "gram", "grams", "ounces", "ounce", "stone",
    "litre", "litres", "liter", "liters", "mile", "miles", "kilometre", "kilometres",
    "kilometer", "kilometers", "percent", "degree", "degrees", "minute", "minutes", "hour",
    "hours"))

ADVERB = frozenset(("just", "ever", "already", "actually", "really", "first", "originally",
                    "previously", "recently", "still", "also", "always", "never", "even"))


def _subjects_at(words, index, names=()):
    if index >= len(words):
        return False
    core = words[index].strip(".,!?").lower()
    return core in SUBJECTISH or core in names


def _np_end(words, start, most=3):
    if start >= len(words):
        return start
    if words[start].strip(".,!?;:").lower() not in DETERMINERS:
        return start + 1
    end = start + 1
    while end < len(words) and end - start < most:
        core = words[end].strip(".,!?;:").lower()
        if core in AUX or core in WH or core in PREDICATE or core in PREP or core in ADVERB:
            break
        end += 1
    return max(end, start + 1)


def _embed(words, names=()):
    for index in range(len(words) - 1):
        aux = words[index].strip(".,!?;:").lower()
        if aux not in AUX:
            continue
        start = index + 1
        if not _subjects_at(words, start, names):
            continue
        end = _np_end(words, start)
        subject, tail = words[start:end], words[end:]
        if aux in MODAL and index > 0 and len(subject) > 1 and not tail:
            subject, tail = subject[:-1], subject[-1:]
        if aux in ("do", "does", "did"):
            verb = 0
            while verb < len(tail) and tail[verb].strip(".,!?;:").lower() in ADVERB:
                verb += 1
            if verb < len(tail):
                tail[verb] = _agree(tail[verb], aux)
            elif len(subject) > 1 and subject[-1].strip(".,!?;:").lower() not in (
                    DETERMINERS | PREDICATE | MEASURE):
                subject, tail = subject[:-1], [_agree(subject[-1], aux)]
            return words[:index] + subject + tail
        return words[:index] + subject + [words[index]] + tail
    return words


POSSESSIVE = re.compile(r"([A-Za-z]+)(?:'s|\u2019s)\b")
IS_NOT_POSSESSIVE = frozenset("""it that this there here what who he she one everyone nobody
somebody anyone""".split())


def _keep_possessives(clause, clean):
    stems = {match.group(1).lower() for match in POSSESSIVE.finditer(clean or "")}
    if not stems:
        return clause
    words = str(clause or "").split()
    out = []
    for index, word in enumerate(words):
        core = word.strip(".,!?;:")
        if index == len(words) - 1:
            out.append(word)
            continue
        if (core.lower() in stems and "'" not in core and "\u2019" not in core
                and core.lower() not in IS_NOT_POSSESSIVE):
            out.append(core + "'s" + word[len(core):])
        else:
            out.append(word)
    return " ".join(out)


def _truncated(clause, clean):
    if not clause or not clean:
        return False
    focus_words = clause.replace("?", "").lower().split()
    clean_words = clean.replace("?", "").lower().split()
    return len(focus_words) < len(clean_words) and clean_words[:len(focus_words)] == focus_words


NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?")


def _numbers(text, clause):
    typed = {match.group(0).replace(",", ""): match.group(0) for match in NUMBER.finditer(text or "")}
    if not typed:
        return clause
    def keep(match):
        return typed.get(match.group(0)) or match.group(0)
    return re.sub(r"\d[\d,]*(?:\.\d+)?", keep, clause)


def restate(text):
    reading = understand(text, {})
    clean = (reading.get("clean") or "").strip()
    clause = _as_text(reading.get("focus"))
    if not clause:
        clause = (reading.get("norm_text") or "").split(" | ")[-1].strip()
    if _truncated(clause, clean):
        clause = clean
    if not clause:
        clause = clean
    first_word = (clause.split() or [""])[0].strip(".,!?;:").lower()
    line_words = {word.strip(".,!?;:").lower() for word in clean.split()}
    if clean and (first_word in PREP or (first_word and first_word not in line_words)):
        clause = _expand(clean)
    words = _strip_lead(clause.replace("?", "").split())
    if not words:
        return None
    words = _with_wh(reading, words)
    typed = [word.strip(".,!?;:").lower() for word in str(text or "").split()]
    typed_aux = next((word for word in typed if word in ("do", "does", "did")), None)
    if typed_aux:
        for index, word in enumerate(words):
            core = word.strip(".,!?;:").lower()
            if core in ("do", "does", "did") and core != typed_aux:
                words[index] = typed_aux + word[len(word.strip(".,!?;:")):]
                break
    first = words[0].strip(".,!?").lower()
    names = {(entity.get("text") or "").strip().lower() for entity in reading.get("entities") or []
             if isinstance(entity, dict)}

    if first in AUX or first in WH or first in DROPPED_SUBJECT:
        words = _flip(words, addressee=True)
        if first in DROPPED_SUBJECT and reading.get("kind") != "question":
            words = _with_you(words)
            said = " ".join(_embed(words, names))
            clause = said
        else:
            said = " ".join(_embed(words, names))
            clause = ("whether " + said) if first in AUX else said
    else:
        clause = _from_the_bot(" ".join(_flip(_to_the_bot(" ".join(words)).split())))
    clause = _conditional(clause)
    clause = _keep_possessives(clause, clean)
    if reading.get("kind") == "question":
        core = {word.strip(".,!?;:").lower() for word in clause.split()}
        opening = (clause.split() or [""])[0]
        if not (core & (AUX | WH)) and not _is_wh(opening) and "whether" not in core:
            return None
    clause = _numbers(text, clause)
    clause = no_tone(clause)
    if not clause:
        return None
    return _restore_case(text, clause.strip(" ,;:")) or None


PAST = {
    "say": "said", "tell": "told", "go": "went", "get": "got", "make": "made", "take": "took",
    "buy": "bought", "think": "thought", "see": "saw", "do": "did", "have": "had", "eat": "ate",
    "drink": "drank", "come": "came", "find": "found", "give": "gave", "know": "knew",
    "leave": "left", "pay": "paid", "put": "put", "read": "read", "run": "ran", "send": "sent",
    "sit": "sat", "speak": "spoke", "spend": "spent", "write": "wrote", "fly": "flew",
    "drive": "drove", "meet": "met", "hear": "heard", "feel": "felt", "keep": "kept",
    "sleep": "slept", "win": "won", "lose": "lost", "break": "broke", "choose": "chose",
    "begin": "began", "become": "became", "bring": "brought", "build": "built",
    "catch": "caught", "cost": "cost", "cut": "cut", "fall": "fell", "forget": "forgot",
    "hold": "held", "hit": "hit", "hurt": "hurt", "lend": "lent", "let": "let",
    "mean": "meant", "sing": "sang", "teach": "taught", "understand": "understood",
    "wear": "wore", "wake": "woke",
}


def _past(word):
    core = word.strip(".,!?;:")
    suffix = word[len(core):]
    if core in PAST:
        return PAST[core] + suffix
    if not core or not core[-1:].isalpha():
        return word
    if core.endswith("e"):
        return core + "d" + suffix
    if len(core) > 2 and core.endswith("y") and core[-2] not in "aeiou":
        return core[:-1] + "ied" + suffix
    return core + "ed" + suffix


def _agree(verb, aux):
    if aux == "did":
        return _past(verb)
    if aux == "does":
        return _third(verb)
    return verb


THIRD = {"have": "has", "be": "is", "do": "does", "go": "goes", "say": "says"}


def _third(verb):
    core = verb.strip(".,!?;:")
    suffix = verb[len(core):]
    low = core.lower()
    if not core or not core[-1:].isalpha():
        return verb
    if low in THIRD:
        return THIRD[low] + suffix
    if low in AUX:
        return verb
    if low.endswith(("s", "sh", "ch", "x", "z", "o")):
        return core + "es" + suffix
    if len(low) > 2 and low.endswith("y") and low[-2] not in "aeiou":
        return core[:-1] + "ies" + suffix
    return core + "s" + suffix


def _conditional(clause):
    if clause.startswith("if "):
        return "what happens " + clause
    return clause


def _restore_case(text, clause):
    typed = [w.strip(".,!?;:") for w in str(text or "").split()]
    capitals = {w.lower() for w in typed[1:] if w[:1].isupper()}
    out = []
    for word in clause.split():
        core = word.strip(".,!?;:")
        out.append(_capital(core) + word[len(core):] if core in capitals else word)
    return " ".join(out)


def _capital(text):
    return text[:1].upper() + text[1:] if text else text


NOT_A_THING = frozenset(("keep", "keeps", "kept", "do", "does", "did", "get", "gets",
                         "got", "go", "goes", "going", "went", "want", "wants", "wanted",
                         "need", "needs", "needed", "try", "tries", "tried", "make",
                         "makes", "made", "start", "starts", "started", "stop", "stops",
                         "say", "says", "said", "think", "thought", "happen", "happens",
                         "happening", "thing", "things", "it", "something", "anything"))


ON_THE_TABLE_TURNS = 12
ON_THE_TABLE_MISSES = 3


def on_the_table(memory, limit=3):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return []
    recent = turns[-ON_THE_TABLE_TURNS:]
    out = []
    misses = 0
    for size in range(len(recent), 0, -1):
        shorter = dict(memory)
        shorter["turns"] = recent[:size]
        phrase = about(shorter)
        if not phrase:
            continue
        head = (phrase.split() or [""])[-1].strip(".,!?")
        if head in NOT_A_THING:
            continue
        if not _said_in_the_chat(phrase, recent[:size]):
            continue
        if any(phrase.lower() == one.lower() for one in out):
            misses += 1
            if misses >= ON_THE_TABLE_MISSES:
                break
            continue
        out.append(phrase)
        misses = 0
        if len(out) >= limit:
            break
    return out


def _said_in_the_chat(phrase, turns):
    words = str(phrase or "").lower().split()
    if not words:
        return False
    if words[0] == "your":
        words = ["my"] + words[1:]
    head = words[-1]
    for turn in turns:
        text = turn.get("user") if isinstance(turn, dict) else None
        if not isinstance(text, str):
            continue
        said = text.lower().split()
        run = len(words)
        for start in range(len(said) - run + 1):
            if said[start:start + run] == words:
                return True
        if head in VERB_WORDS:
            continue
        for entity in understand(text, {}).get("entities") or ():
            if entity.get("type") not in ("thing", "person"):
                continue
            if (entity.get("text") or "").lower() != head:
                continue
            if _said_as_a_state(head, text):
                continue
            return True
    return False


COPULA = frozenset("""im i'm am is are was were been being feel feels felt feeling look looks
    seem seems get gets got getting become""".split())
STATE_FILLER = frozenset("""a an the bit little very really so quite pretty too that this
    honestly actually just totally proper still always kinda sorta dead well rather""".split())


def _said_as_a_state(head, text):
    said = text.lower().replace("\u2019", "'").split()
    seen = False
    for i, word in enumerate(said):
        if word.strip(".,!?;:\"'") != head:
            continue
        seen = True
        j = i - 1
        while j >= 0 and said[j].strip(".,!?;:\"'") in STATE_FILLER:
            j -= 1
        if j < 0 or said[j].strip(".,!?;:\"'") not in COPULA:
            return False
    return seen


VERB_WORDS = VERB_FORMS | VERBISH


def in_a_list(phrases):
    items = [str(one).strip() for one in (phrases or []) if str(one).strip()]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]


def topic_index(memory, skip=None):
    keep = []
    for index, (text, reading) in enumerate(user_lines(memory)):
        if _is_thin(reading) or _is_memory_line(reading):
            continue
        if _asks_about_the_chat(text, memory, skip):
            continue
        keep.append((index, text, reading))
    for require_entity in (True, False):
        for index, text, reading in reversed(keep):
            if require_entity and not _named_entities(reading):
                continue
            if not require_entity and (reading.get("intent") == "feeling"
                                       or reading.get("topic_own") == "feelings"):
                continue
            if _phrase_for(text, reading):
                return index
    return None


def last_ask(memory, skip=None, not_before=None):
    lines = user_lines(memory)
    for index in range(len(lines) - 1, -1, -1):
        if not_before is not None and index < not_before:
            break
        text, reading = lines[index]
        if _is_memory_line(reading) or _asks_about_the_chat(text, memory, skip):
            continue
        if reading.get("kind") == "question" or "?" in text:
            said = restate(text)
            if said:
                return said
    return None


DETAIL_OPENER = re.compile(r"^\s*(?:its|it's|it is|thats|that's|that is|theyre|they're|"
                           r"they are|hes|he's|she's|shes)\s+", re.I)


def _only_a_detail(text):
    line = " ".join(str(text or "").split()).strip(" .!?")
    rest = DETAIL_OPENER.sub("", line)
    if rest == line:
        return False
    got = detail.the_detail(line)
    if not got:
        return False
    words = lambda t: [w.lower() for w in str(t or "").split()]
    return words(got) == words(rest)


def last_said(memory, skip=None):
    said, past_a_closing = last_said_past_closings(memory, skip)
    if past_a_closing and said and about(memory, skip):
        return None
    return said


def last_said_past_closings(memory, skip=None):
    past_a_closing = False
    for text, reading in reversed(user_lines(memory)):
        if _is_thin(reading) or reading.get("kind") == "question" or _is_memory_line(reading):
            continue
        if signs_off(text):
            past_a_closing = True
            continue
        if _asks_about_the_chat(text, memory, skip):
            continue
        if _only_a_detail(text):
            continue
        said = restate(text)
        if said:
            return said, past_a_closing
    return None, past_a_closing


def named(memory, limit=2):
    out = []
    for _text, reading in reversed(user_lines(memory)):
        for entity in reading.get("entities") or []:
            if not isinstance(entity, dict):
                continue
            name = (entity.get("text") or "").strip()
            if entity.get("type") == "thing" or not name or name.lower() in WEAK:
                continue
            if name.lower() in FLIP or len(name.strip(".,")) <= 2:
                continue
            if name.lower().startswith("my "):
                name = "your " + name[3:]
            if name.lower() in (n.lower() for n in out):
                continue
            out.append(name)
            if len(out) >= limit:
                return out
    return out


CHECK_VERDICT = re.compile(
    r"^(?:(?:and|but|so|ok(?:ay)?|right|oh|hmm|well|then)[, ]+)*"
    r"(?:(?:is|will|would|does|do|was)\s+(?:that|it|this)"
    r"(?:\s+be)?"
    r"|(?:that|it|this)(?:'s|s|\s+is)?)"
    r"\s+(?:alright|all right|ok|okay|fine|safe|allowed|work|works)"
    r"(?:\s+for (?:me|us|him|her|them))?"
    r"(?:\s+(?:though|then|now))?"
    r"|^(?:(?:and|but|so|ok(?:ay)?|right|oh|hmm|well|then)[, ]+)*"
    r"(?:are|r)\s+(?:you\s+)?(?:really\s+)?sure"
    r"(?:\s+(?:about|of)\s+(?:that|it|this))?$"
    r"|^(?:you\s+)?(?:really\s+)?sure(?:\s+(?:about|of)\s+(?:that|it|this))?$", re.I)

VERDICT_SAID = re.compile(
    r"^(?:still\s+(?:a\s+)?)?(yes|no|afraid not|no, sorry|no, afraid not)\s*[:\u2014\u2013-]\s*(.+)$",
    re.I | re.S)

NO_FRAMES = ("Afraid not \u2014 {reason}.", "Still a no \u2014 {reason}.",
             "No, sorry \u2014 {reason}.")
YES_FRAMES = ("Yes \u2014 {reason}.", "Still yes \u2014 {reason}.")
NO_USED = (("afraid not", 1), ("still a no", 2), ("no, sorry", 0))
YES_USED = (("yes \u2014", 1), ("still yes", 0))


def checking_the_verdict(text, memory):
    if not isinstance(memory, dict):
        return None
    said = " ".join(str(text or "").lower().split()).strip(" .!?,")
    if not said or len(said.split()) > 9 or not CHECK_VERDICT.match(said):
        return None
    turns = memory.get("turns")
    last = ""
    if isinstance(turns, list) and turns:
        last = str(turns[-1].get("bot") or "").strip()
    verdict = VERDICT_SAID.match(last)
    if not verdict:
        return None
    reason = _first_clause(verdict.group(2))
    if not reason:
        return None
    if verdict.group(1).lower() == "yes":
        return _next_frame(YES_FRAMES, YES_USED, last).format(reason=reason)
    return _next_frame(NO_FRAMES, NO_USED, last).format(reason=reason)


CHECK_A_FACT = re.compile(
    r"^(?:(?:and|but|so|ok(?:ay)?|right|oh|hmm|well|then|thanks|ta|great|good|nice)[, ]+)*"
    r"(?:"
    r"(?:is|was|are)\s+(?:that|it|this|they|those)"
    r"(?:\s+(?:really|actually|definitely|all|exactly|still))?"
    r"\s+(?:right|true|correct|accurate|the right (?:answer|thing)|how it works|what you meant)"
    r"(?:\s+(?:then|though|now|yeah|yes|or not|or what))?"
    r"|(?:that|it|this)(?:'s|s|\s+is)?\s+(?:right|true|correct|accurate)"
    r"|(?:right|correct|true)"
    r")\s*[?.!]*$", re.I)
NO_FACT_SAID = re.compile(
    r"^(?:i'm not sure|i am not sure|i don't know|i do not know|i'd rather not guess|"
    r"that's beyond what i know|not something i know)", re.I)
FACT_FRAMES = ("That's right.", "Yes — that's the usual guidance.",
               "That is the answer I have, yes.", "That's how I understand it too.",
               "Yes — that's the standard advice.", "That's right, as far as I know.")
NOT_A_FACT = re.compile(
    r"(?:^|\b)(?:i'll remember|i will remember|noted\b|got it\b|alright then|sounds good|"
    r"fair enough|i'm listening|say more|tell me more|back on the table)", re.I)


def checking_a_fact(text, memory):
    if not isinstance(memory, dict):
        return None
    said = " ".join(str(text or "").lower().split()).strip(" .!?,")
    if not said or len(said.split()) > 7 or not CHECK_A_FACT.match(said):
        return None
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns:
        return None
    last = turns[-1] if isinstance(turns[-1], dict) else {}
    answer = " ".join(str(last.get("bot") or "").split())
    if not answer or answer.endswith("?"):
        return None
    if not _fact_from(answer):
        if len(answer.split()) < 8 or NO_FACT_SAID.match(answer) or NOT_A_FACT.search(answer):
            return None
        from . import topics
        if topics.an_entry_for(str(last.get("user") or "")) is None:
            return None
    return _a_frame_not_said(FACT_FRAMES, memory)


def _fact_from(answer):
    low = answer.lower()
    return any(low.startswith(frame.lower().rstrip(".")) for frame in FACT_FRAMES)


def _a_frame_not_said(frames, memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    said = [" ".join(str(turn.get("bot") or "").lower().split())
            for turn in (turns or []) if isinstance(turn, dict)][-6:]
    for frame in frames:
        stem = frame.lower().rstrip(".")
        if not any(line.startswith(stem) for line in said):
            return frame
    return frames[0]


def _next_frame(frames, used, said):
    stem = " ".join(str(said or "").split()).lower()
    for lead, going_to in used:
        if stem.startswith(lead):
            return frames[going_to]
    return frames[0]


def _first_clause(said, limit=13):
    said = " ".join(str(said or "").split())
    if not said:
        return ""
    cut = re.split(r"(?<=[.!?])\s|;\s|,\s+(?:and|so|but)\s", said, maxsplit=1)[0]
    cut = cut.strip(" .,;:")
    words = cut.split()
    if len(words) > limit:
        cut = " ".join(words[:limit]).rstrip(",;:")
    return cut


WENT_ASK = re.compile(
    r"^(?:(?:so|and|then|but|well|ok|okay|right|oh|ah|hey|great|good|nice|hmm+|anyway|go on|"
    r"aw+|yes|yeah)\b[\s,]*)*"
    r"(?:"
    r"how\s+(?:did|does|has|have|was|were)?\s*(?:it|that|things|everything)\s*"
    r"(?:go|gone|been|turn\s+out|work\s+out)?(?:\s+(?:ok|okay|well|fine|alright|good|bad))?"
    r"|how(?:'s|d|s)?\s+(?:it|that)\s+(?:go|gone|been|turn\s+out)"
    r"|how'd\s+(?:it|that)\s+go"
    r"|did\s+(?:it|that|things|everything)\s+(?:go|turn\s+out)"
    r"(?:\s+(?:ok|okay|well|fine|alright|good|bad))?"
    r"|how\s+(?:did|was|were)\s+(?:the|your|my|that)\s+(?P<thing>[a-z][a-z' -]{1,40}?)"
    r"(?:\s+(?:go|gone|turn\s+out))?"
    r")"
    r"(?:[\s,]*(?:then|though|today|tonight|in the end|honestly|please|anyway|huh|so far))*"
    r"[\s?.!]*$", re.I)
NOT_THE_THING = frozenset((
    "day", "days", "week", "weeks", "weekend", "weekends", "evening", "evenings", "morning",
    "mornings", "afternoon", "night", "nights", "holiday", "holidays", "break", "time",
    "weather", "sleep"))
NEVER_A_THING_THAT_WENT = frozenset((
    "baby", "birth", "stillbirth", "miscarriage", "loss", "death", "passing", "funeral",
    "news", "fall", "tumble", "panic", "attack", "seizure", "fit", "convulsion", "bleed",
    "bleeding", "symptom", "diagnosis", "result", "fever", "pain", "ache", "flu", "bug",
    "infection", "migraine", "headache", "period", "cramp", "rash", "shock", "scare", "fright"))
_A_STATE_ITSELF = frozenset((
    "day", "week", "night", "morning", "afternoon", "evening", "weekend", "holiday", "break",
    "time", "cold", "temperature", "argument", "row", "cry", "crying", "upset", "tiredness"))
_A_NAME_FOR_IT = frozenset(("first", "second", "third", "last", "next", "final", "new", "other"))
_A_DESCRIPTION = frozenset(("some", "any", "such", "really", "very", "quite", "rather", "proper",
                            "bit", "lot", "few", "another", "little", "bad", "awful", "terrible",
                            "rough", "dreadful", "horrible", "hard", "tough", "rotten"))
HAPPENED = re.compile(r"\b(?:today|tonight|this\s+(?:morning|afternoon|evening)|last\s+night|"
                      r"yesterday|earlier)\b", re.I)
HAD_IT = re.compile(r"\b(?:i|we)\s+(?:had|went\s+(?:for|to|on)|did|took|sat|attended|started|"
                    r"finished|gave)\s+(?:an|a|my|our|the)?\s*(?P<thing>[a-z][a-z' -]{1,40})", re.I)
IT_WAS = re.compile(r"\bmy\s+(?P<thing>[a-z][a-z' -]{2,40}?)\s+(?:was|were|is|are)"
                    r"(?:\s+(?:today|tonight|yesterday|this\s+[a-z]+|last\s+night|earlier))?"
                    r"(?:\s*[,;]?\s*(?:and|but|so)\b.*)?\s*$",
                    re.I)
THING_END = frozenset(("today", "tonight", "yesterday", "this", "last", "and", "but", "so",
                       "then", "which", "because", "when", "where", "it", "that", "was", "were",
                       "is", "at", "in", "on", "with", "for", "to", "after", "before", "earlier"))
_A_THING_DONE = frozenset((
    "go", "try", "look", "glance", "peek", "chat", "talk", "word", "think", "laugh", "cry",
    "moan", "nag", "row", "argument", "argue", "fight", "lie", "bath", "shower", "wash",
    "rest", "nap", "snooze", "kip", "sleep", "sit", "drink", "bite", "cuddle", "listen",
    "wobble", "turn", "moment", "blip", "dip"))
THING_PARTICLE = frozenset(("off", "out", "up", "down", "away", "back", "over", "round",
                            "around", "through", "along", "about", "in", "on"))
DONE_WORDS = frozenset(("cut", "put", "set", "shut", "hit", "let", "cost", "hurt", "burst",
                        "spread", "rid", "shed", "split", "stuck", "sent", "built", "frozen"))


def _a_done_word(word):
    return word.endswith("ed") or word in DONE_WORDS or word in IRREGULAR_PARTICIPLES
WENT_FRAMES = ("So how did the {thing} go? You'd know before I would.",
               "You tell me \u2014 how did the {thing} go?",
               "Go on then: how did the {thing} go?",
               "How did the {thing} go? I only know what you tell me.")
WENT_FRAMES_NO_THING = ("Then you'll have to tell me \u2014 how did it go?",
                        "Go on then, how did it go?",
                        "I can't see your day from here. How did it go?")
WENT_AGAIN = ("I've no way of seeing it from here \u2014 you'll have to tell me.",
              "Still yours to tell me: how did it go?",
              "I can't see it from where I am, so tell me how it went.")
A_VERDICT = re.compile(
    r"\b(?:it|that|they)\s+(?:was|were|is|are)\s+(?P<v>fine|good|great|ok|okay|all right|alright|"
    r"lovely|brilliant|awful|terrible|horrible|dreadful|rubbish|a disaster|a nightmare)"
    r"|\bwent\s+(?P<w>well|fine|badly|great|ok|okay|awful|terrible)", re.I)
_WENT_WELL = frozenset(("fine", "good", "great", "ok", "okay", "all right", "alright", "lovely",
                        "brilliant", "well"))
WENT_TOLD_WELL = ("Good \u2014 you told me it was {v}. That's the main thing.",
                  "{V} is a relief, then. Tell me more if there's more in it.",
                  "So it went {v}. Nothing for me to ask there.")
WENT_TOLD_BAD = ("Sorry it went {v}. What happened?",
                 "{V} \u2014 that's rough. Tell me the worst bit, if you want to.",
                 "That's a rotten one to have had. What went wrong?")


def _the_verdict_they_gave(line):
    low = " ".join(str(line or "").lower().split())
    match = A_VERDICT.search(low)
    if not match:
        return ""
    return (match.group("v") or match.group("w") or "").lower()


def _the_thing_they_had(line):
    low = " ".join(str(line or "").lower().split())
    if not low or not HAPPENED.search(low):
        return ""
    for pattern in (IT_WAS, HAD_IT):
        match = pattern.search(low)
        if not match:
            continue
        words = []
        for word in match.group("thing").split():
            if word in THING_END:
                break
            words.append(word)
        thing = " ".join(words).strip(" ,;:-")
        if not thing or thing in NOT_THE_THING:
            continue
        if words and words[0] in _A_THING_DONE:
            continue
        if any(word in NEVER_A_THING_THAT_WENT for word in words):
            continue
        if words[-1] in _A_STATE_ITSELF and not any(word in _A_NAME_FOR_IT for word in words):
            continue
        if any(word in _A_DESCRIPTION for word in words):
            continue
        if any(word in THING_PARTICLE for word in words):
            continue
        if words and _a_done_word(words[-1]):
            words = words[:-1]
            thing = " ".join(words).strip(" ,;:-")
            if len(words) < 2 or thing in NOT_THE_THING:
                continue
        elif any(_a_done_word(word) for word in words[:-1]):
            continue
        return thing
    return ""


def went(text, memory):
    if not isinstance(text, str) or not isinstance(memory, dict):
        return None
    said = " ".join(text.lower().split()).strip(" ?.!,")
    match = WENT_ASK.match(said)
    if not match:
        return None
    turns = [turn for turn in _turns(memory) if isinstance(turn, dict)]
    if not turns:
        return None
    asked_before = _asked_already(turns[-1].get("bot") or turns[-1].get("reply"))
    thing = ""
    verdict = ""
    for turn in reversed(turns):
        thing = _the_thing_they_had(turn.get("user"))
        if thing:
            verdict = _the_verdict_they_gave(turn.get("user"))
            break
    asked_about = (match.groupdict().get("thing") or "").strip()
    if asked_about:
        if not thing or asked_about in NOT_THE_THING or asked_about in _A_THING_DONE:
            return None
        thing = asked_about
    if not thing:
        return None
    if verdict:
        frames = WENT_TOLD_WELL if verdict in _WENT_WELL else WENT_TOLD_BAD
        return pick([frame.format(v=verdict, V=verdict.capitalize()) for frame in frames], memory)
    if asked_before:
        return pick(list(WENT_AGAIN), memory)
    return pick([frame.format(thing=thing) for frame in WENT_FRAMES], memory)


def _asked_already(reply):
    said = " ".join(str(reply or "").lower().split())
    if not said.endswith("?"):
        return False
    return bool(WENT_ASK.match(said.rstrip("?").strip())) or bool(
        re.search(r"how (?:did|was) (?:it|that|the|your)\b.*\bgo\b", said))
