import re

from ..understanding import lexicon
from ..understanding.kinds import NEGATIVE, POSITIVE
from .filler import without_the_shrug
from . import quotes as quoted

WORD = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")

STOPWORDS = frozenset("""
a an the and or but if so of to in on at for with without about as by from into over after
before between during out up down off again further then once here there when where why how all
any both each few more most other some such no nor not only own same than too very can could
should would will shall may might must do does did doing have has had having am is are was were
be been being i me my we us our you your he him his she her it its they them their this that
these those what which who whom whose
i'm i've i'll i'd don't doesn't didn't can't won't isn't aren't wasn't weren't it's that's
# A pronoun typed without its apostrophe is still a pronoun, and it is not a thing a line is
# about: "shes 84, what can we do" is "she is 84" with the apostrophe left off, and read as a
# word of its own "shes" stems to "sh", which no entry in the world is about. So the line was
# read as naming a subject of its own, the entry the chat was already on was dropped as not
# being about it, and a follow-up about the falls answer went to a search hedge - while the same
# line written "she is 84" was answered. The set is pronouns only: a word like "shed" or "his"
# that is spelt the same with or without an apostrophe is left alone.
shes hes theyre theyve theyll theyd himself herself themselves itself
like just really quite maybe perhaps also still even much many lot lots want needs need get got
make makes okay ok right well yeah one ones youd youre im ive id ill
actually honestly literally basically simply truly
""".split())

ACKS = frozenset("""
ok okay k kk cool nice great good yeah yep yes no nah nope lol haha ha hmm sure right wow oh ah yum
aha eh meh same thanks thx ty cheers ta fine alright aw brilliant perfect awesome interesting
true agreed indeed not much nothing much idk dunno maybe probably sounds sound idea love lovely
definitely exactly fair enough makes sense got it see later
""".split())

GREET = frozenset("hi hello hey hiya morning evening afternoon night bye goodbye".split())

REFERRING = frozenset("""
it its that this these those they them there their one ones he she him her his other same
""".split())

ORDERING = frozenset("""
start starts started starting first next then else begin beginning later more again
""".split())

ABOUT_ANOTHER = re.compile(r"\b(?:what|how) about\b")


PART_OF_THE_ONE = re.compile(
    r"\b(?:the|these|those|my|your|its)\s+(?:leftovers?|rest|remainder|extras?|offcuts?|"
    r"trimmings|scraps?|peels?)\b|\bwhat(?:'s| is) left\b")

CONTINUATION_START = frozenset("""
and so but then also what how why when where which who whom whose can could should would will
is are do does did have has was were if
""".split())

MEASURE_WORDS = frozenset("""
long much many far often hot warm temperature temp temps degrees centigrade fahrenheit
time heat size price setting what which
""".split())

PROPERTY = re.compile(r"\bhow (?:long|much|many|far|often|hot|warm)\b|"
                      r"\bwhat (?:temperature|temp|temps|degrees|centigrade|fahrenheit|"
                      r"time|heat|size|price|setting)\b|"
                      r"\bper (?:kilo|kg|500g|person|head|each)\b")

KIND_ASK = re.compile(r"\b(?:what|which)\s+(?:kind|sort|type|breed|brand|model|make|size|one)\s*\?"
                      r"|\bwhich\s+(?:one|brand|model|make)\b"
                      r"|\bwhat\s+(?:kind|sort|type|breed)\b")
SWITCHERS = ("actually", "never mind", "nevermind", "by the way", "btw", "back to", "anyway",
             "new question", "different question", "forget that", "instead", "changing the subject",
             "sorry", "apologies", "my mistake", "correction", "no wait")

RETURN_LEAD = re.compile(
    r"^(?:(?:ok|okay|so|right|anyway|sorry|and|but|well|oh|then|great|nice|yes|yeah|hmm|aha|ah)"
    r"[\s,]*)*(?:back\s+to|as\s+i\s+was\s+saying|as\s+i\s+said|coming\s+back\s+to|"
    r"where\s+were\s+we(?:\s+on)?|return(?:ing)?\s+to)\b\s*")

CASUAL_LEAD = re.compile(
    r"^(?:(?:ok|okay|so|right|anyway|and|well|oh)\s*[,\s]\s*)*(?:anyway\s*[,\s]\s*)")
CASUAL_OPEN = frozenset("a an the my our your that this those these".split())
CASUAL_VERB = frozenset("""
is are was were am be been being has have had got get gets went go goes called calls said say
says told tell tells keeps keep kept needs need wants want likes like loves love works work
doing does did do can could should would will
""".split())

RETURN_TIME = frozenset("""
tomorrow today tonight now later soon monday tuesday wednesday thursday friday saturday sunday
week weekend month year morning afternoon evening night
""".split())

RETURN_ASKS = frozenset("""
what how why when where which who whom whose can could should would will shall is are was were
am do does did have has had if whether
whats hows whys whens wheres whichs whos
""".split())


RETURN_ASKS = RETURN_ASKS | frozenset(
    word + "s" for word in ("what", "how", "where", "who", "when", "why", "which"))


def words(text):
    out = []
    for word in WORD.findall(str(text).lower().replace("’", "'")):
        if word.endswith("'s"):
            word = word[:-2]
        out.append(word.replace("'", ""))
    return [word for word in out if word]


def stem(word):
    if len(word) > 4 and word.endswith("ies"):
        return word[:-3] + "y"
    if len(word) > 3 and word.endswith("es") and word[-3] in "sxzh":
        return word[:-2]
    if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def keywords(text):
    out = []
    for word in words(text):
        if word in STOPWORDS or len(word) < 3 or word.isdigit():
            continue
        key = stem(word)
        if key not in out:
            out.append(key)
    return out


NOT_DOING = re.compile(r"\b(?:wont|won'?t|doesnt|doesn'?t|didnt|didn'?t|cant|can'?t|couldnt|"
                       r"couldn'?t|never|refuses? to|stopped|not)\s+([a-z']+)", re.IGNORECASE)


def _what_they_are_not_doing(text):
    out = set()
    for found in NOT_DOING.finditer(" ".join(str(text or "").lower().split())):
        word = found.group(1)
        if word and word not in STOPWORDS and len(word) >= 3:
            out.add(stem(word))
    return out


ENDINGS = ("ing", "ed")


def forms(word):
    word = str(word or "")
    out = {word}
    for ending in ENDINGS:
        if len(word) > len(ending) + 2 and word.endswith(ending):
            root = word[:-len(ending)]
            if len(root) >= 4:
                out.add(root)
            out.add(root + "e")
            if len(root) > 3 and root[-1] == root[-2] and root[-1] not in "aeiou":
                out.add(root[:-1])
    return out


def content(text):
    out = []
    for word in words(text):
        if len(word) < 3 or word.isdigit():
            continue
        if word in STOPWORDS:
            continue
        key = stem(word)
        if key in STOPWORDS or forms(key) & STOPWORDS:
            continue
        if key not in out:
            out.append(key)
    return out


def is_ack(text):
    clean = " ".join(words(text))
    if not clean:
        return True
    if clean in ACKS or clean in GREET:
        return True
    parts = clean.split()
    if len(parts) <= 4 and any(w in ACKS or w in GREET for w in parts):
        return all(w in ACKS or w in GREET or w in STOPWORDS or len(w) <= 3 for w in parts)
    return False


def is_small_talk(text, kind=None):
    if kind in ("empty", "greeting", "thanks"):
        return True
    return is_ack(text)


def _a_place_the_line_moves(text):
    from . import facts as _facts
    return _facts.a_moved_place(text)


def _asks_about_the_bot(read):
    return isinstance(read, dict) and bool(read.get("about_bot"))


def _note(memory, text, kind=None):
    read = memory.get("understood")
    if isinstance(read, dict):
        aim_length = _the_length_of_the_aim(read, memory)
        if aim_length is not None:
            memory["understood"] = aim_length
            read = aim_length
    if isinstance(read, dict) and read.get("change_of_subject"):
        kept = " ".join(str(read.get("clean") or "").split())
        if kept:
            text = kept
    _keep_person(memory, text)
    if is_small_talk(text, kind):
        return None
    if _asks_about_the_bot(read):
        return None
    moved_to = _a_place_the_line_moves(text)
    if moved_to:
        record = {"turn": len(memory.get("turns") or []), "text": text.strip(),
                  "words": keywords(text)}
        previous = memory.get("topic")
        if isinstance(previous, dict) and previous.get("text") == record["text"]:
            return previous
        memory["topic"] = record
        topics = memory.get("topics")
        if not isinstance(topics, list):
            topics = memory["topics"] = []
        if not topics or topics[-1].get("text") != record["text"]:
            topics.append(record)
        return record
    target = return_target(text)
    if target:
        record = find(memory, target)
        if record:
            _resume(memory, record, target, text)
            return memory["topic"]
        if not _asks(target):
            return current(memory)
    leans = isinstance(read, dict) and bool(read.get("followup"))
    if is_follow_up(text, memory) or leans:
        record = current(memory)
        if record and not _after_an_emergency(memory):
            back = _the_record_they_came_back_to(text, memory, record)
            if back is not None:
                return _back_to(memory, back, text)
        if record and not _after_an_emergency(memory) \
                and (not _names_another_subject(text, record, memory)
                     or _a_part_of_the_record(read, record)):
            if not _switches(text) or _only_details(text, record):
                extra = [w for w in keywords(_without_switchers(text))
                         if w not in record.get("words", [])]
                record["words"] = (list(record.get("words") or []) + extra[:4])[:12]
                return record
    constraint = _only_names_the_constraint(text, memory)
    if (_adds_a_detail(text, memory) or _only_adds_a_person_to_the_thing(text, current(memory))
            or constraint):
        record = current(memory)
        if record is not None and not _after_an_emergency(memory):
            if constraint:
                return record
            extra = [w for w in keywords(text) if w not in record.get("words", [])]
            record["words"] = (list(record.get("words") or []) + extra[:4])[:12]
            return record
    if _is_a_when_or_how_often(text, memory):
        record = current(memory)
        if record is not None and not _after_an_emergency(memory):
            extra = [w for w in keywords(text) if w not in record.get("words", [])]
            record["words"] = (list(record.get("words") or []) + extra[:4])[:12]
            return record
    if _asks_which_kind(text, memory):
        record = _about_record(memory)
        if record and not _after_an_emergency(memory) and not _reaches_another_thing(text, memory):
            extra = [w for w in keywords(text) if w not in record.get("words", [])]
            record["words"] = (list(record.get("words") or []) + extra[:4])[:12]
            return record
    if _asks_an_aspect_of_the_thing(text, memory):
        record = current(memory)
        if (record is not None and not _after_an_emergency(memory)
                and not _names_a_place_of_its_own(text, record, memory)):
            extra = [w for w in keywords(text) if w not in record.get("words", [])]
            record["words"] = (list(record.get("words") or []) + extra[:4])[:12]
            return record
    kept = _the_plan_a_correction_renames(memory, text)
    if kept is not None:
        return kept
    keys = keywords(text)
    if len(keys) < 2 and len(words(text)) < 4:
        read = memory.get("understood")
        labels = read.get("topics") if isinstance(read, dict) else None
        labels = [str(label) for label in (labels or ()) if label]
        if not labels:
            return None
        record = {"turn": len(memory.get("turns") or []), "text": text.strip(), "words": keys,
                  "id": labels[0], "label": labels[0]}
        previous = memory.get("topic")
        if isinstance(previous, dict) and previous.get("text") == record["text"]:
            return previous
        memory["topic"] = record
        topics = memory.get("topics")
        if not isinstance(topics, list):
            topics = memory["topics"] = []
        if not topics or topics[-1].get("text") != record["text"]:
            topics.append(record)
        return record
    detail = _a_detail_of_what_we_are_on(text, memory)
    record = {"turn": len(memory.get("turns") or []), "text": text.strip(), "words": keys}
    aim = _the_aim_without_its_deadline(text)
    if aim:
        record["text"] = aim
        record["words"] = keywords(aim)
    if detail is not None:
        record["of"] = str(detail.get("text") or "")
    previous = memory.get("topic")
    if isinstance(previous, dict) and previous.get("text") == record["text"]:
        return previous
    memory["topic"] = record
    topics = memory.get("topics")
    if not isinstance(topics, list):
        topics = memory["topics"] = []
    if not topics or topics[-1].get("text") != record["text"]:
        topics.append(record)
    return record


def _the_record_they_came_back_to(text, memory, record):
    found = set(keywords(text))
    if not found or found & set(record.get("words") or ()):
        return None
    if found <= ORDERING:
        return None
    topics = memory.get("topics")
    if not isinstance(topics, list):
        return None
    for older in reversed(topics[-4:]):
        if older is record or (older.get("text") or "") == (record.get("text") or ""):
            continue
        if found & set(older.get("words") or ()) - set(REFERRING):
            return older
    return None


def _back_to(memory, record, text):
    said = dict(record)
    kept = list(record.get("words") or ())
    said["words"] = (kept + [w for w in keywords(text) if w not in kept])[:12]
    memory["topic"] = said
    topics = memory.get("topics")
    if isinstance(topics, list):
        topics[:] = [other for other in topics if other is not record
                     and (other.get("text") or "") != (said.get("text") or "")]
        topics.append(said)
    return said

AIM_FRAME = re.compile(r"^\s*(?:(?:so|ok|okay|and|also|well|right|yeah|hi|hello)\b[, ]+)*"
                       r"(?:i'?m|im|i am|we'?re|we are)\s+"
                       r"(?:trying|aiming|hoping|planning|meaning|learning)\b", re.I)
A_DEADLINE = re.compile(r"\b(?:before|by|until|till|in time for|ready for|ahead of)\b", re.I)


def _the_aim_without_its_deadline(text):
    line = " ".join(str(text or "").strip().split())
    match = AIM_FRAME.match(line)
    if not match:
        return ""
    rest = line[match.end():]
    cut = A_DEADLINE.search(rest)
    if not cut:
        return ""
    aim = re.sub(r"^\s*to\s+", "", rest[:cut.start()], flags=re.I).strip(" .,;:-")
    words = aim.split()
    if not 1 <= len(words) <= 8 or not re.search(r"[a-z]{3}", aim, re.I):
        return ""
    return aim[0].upper() + aim[1:] if aim[:1].islower() else aim


def _asks_which_kind(text, memory):
    if not KIND_ASK.search(" ".join(str(text or "").lower().split())):
        return False
    return bool(subject(memory))


ASPECT_OF_IT = re.compile(
    r"\bwhat(?:'s| is| are| was| were)\s+(?:the\s+|their\s+|its\s+|his\s+|her\s+)?"
    r"[a-z][a-z'-]*(?:\s+[a-z][a-z'-]*){0,2}\s+like\b"
    r"|\bhow(?:'s| is| are| was| were)\s+(?:the\s+|their\s+|its\s+)?"
    r"[a-z][a-z'-]*(?:\s+[a-z][a-z'-]*){0,2}\s*$"
    r"|\bis\s+the\s+[a-z][a-z'-]*(?:\s+[a-z][a-z'-]*){0,2}\s+"
    r"(?:any\s+good|good|worth\s+it|worth\s+doing|ok|okay|decent|safe|expensive|cheap|nice)\b",
    re.I)


ASPECT_IS_A_PRONOUN = frozenset("""
    you me him her them us i we they he she your my our mine yours
""".split())


def _asks_an_aspect_of_the_thing(text, memory):
    if not ASPECT_OF_IT.search(" ".join(str(text or "").lower().split())):
        return False
    if person(text):
        return False
    if any(word in ASPECT_IS_A_PRONOUN for word in words(text)):
        return False
    if any(stem(word) in WHO for word in words(text)):
        return False
    return bool(subject(memory))


def _reaches_another_thing(text, memory):
    mine = _entry(text)
    if mine is None:
        return False
    thing = subject(memory)
    if not thing:
        return False
    return not _names_it(words(thing), mine)


OWN_THING = re.compile(r"\b(?:my|our|your|his|her|their|the)\s+([a-z]+)")


def _names_a_thing_of_its_own(text, record, memory=None):
    known = set(record.get("words") or [])
    for found in OWN_THING.finditer(" " + " ".join(words(text)) + " "):
        word = stem(found.group(1))
        if word in WHO or word in known:
            continue
        return True
    return _names_a_place_of_its_own(text, record, memory)


def _names_a_place_of_its_own(text, record, memory=None):
    read = memory.get("understood") if isinstance(memory, dict) else None
    if not isinstance(read, dict) or read.get("kind") == "question":
        return False
    known = set(record.get("words") or [])
    said = set(words(record.get("text") or ""))
    for found in read.get("entities") or ():
        if not isinstance(found, dict) or found.get("type") != "place":
            continue
        name = str(found.get("text") or "").strip().lower()
        if not name:
            continue
        if any(stem(part) in known for part in name.split()):
            continue
        if any(part in said for part in name.split()):
            continue
        return True
    return False


def _only_adds_a_person_to_the_thing(text, record):
    if not isinstance(record, dict) or not record.get("text"):
        return False
    line = " ".join(words(text))
    if not line or len(line.split()) > 14:
        return False
    if _entry(text) is not None:
        return False
    named = person(text)
    theirs = person(record.get("text") or "")
    if named is None and theirs is None:
        return False
    if JOINS_THE_THING.search(line) and named is not None:
        return True
    return (ABOUT_THE_PERSON.search(line) is not None and theirs is not None
            and PRONOUN_PERSON.search(line) is not None)


JOINS_THE_THING = re.compile(
    r"\b(?:too|as well|along|coming|comes|with (?:me|us))\b")
ABOUT_THE_PERSON = re.compile(
    r"\b(?:loves?|loved|likes?|liked|adores?|prefers?|collects?|plays?|wants?|enjoys?|hates?|"
    r"into|is (?:mad|crazy|obsessed) about|is a fan of|fans? of|is afraid of)\b")
PRONOUN_PERSON = re.compile(r"\b(?:he|she|they|him|her|them)\b")


MEASURE = frozenset({"maths-and-numbers"})


def _another_area(text, said):
    if not said:
        return False
    from ..understanding import understand
    there = (understand(said, {}) or {}).get("topic_own")
    mine = (understand(text, {}) or {}).get("topic_own")
    if mine in MEASURE:
        return False
    return bool(there and mine and there != mine)


def _a_detail_of_what_we_are_on(text, memory):
    record = current(memory)
    if not isinstance(record, dict) or not record.get("text"):
        return None
    if _this_line(record, memory) or _after_an_emergency(memory):
        return None
    if _names_a_thing_of_its_own(text, record, memory):
        return None
    turn = record.get("turn")
    if isinstance(turn, int) and len(memory.get("turns") or []) - turn > RECENT_TURNS:
        return None
    thing = gist(record.get("text") or "")
    if not thing:
        return None
    widened = _entry(str(text) + " " + thing)
    if widened is None:
        return None
    keyed = _key_words_of(widened)
    thing_words = [word for word in keywords(thing) if len(word) > 2]
    if not thing_words or not any(alike(word, key) for word in thing_words for key in keyed):
        return None
    own = _entry(text)
    if (own is not None
            and not any(alike(word, key) for word in keywords(text) for key in keyed)
            and _another_area(text, record.get("text") or "")):
        return None
    if own is widened:
        return None
    if own is not None and not any(alike(word, key) for word in _key_words_of(own)
                                   for key in keyed):
        return None
    if keeps_away(str(text) + " " + thing, record.get("text") or "", widened):
        return None
    return record


def _a_part_of_the_record(read, record):
    if not isinstance(read, dict) or not isinstance(record, dict):
        return False
    leaned = " ".join(words((read.get("leans_on") or {}).get("text") or ""))
    return bool(leaned) and leaned == " ".join(words(record.get("text") or ""))


def _names_another_subject(text, record, memory=None):
    if (_leads_a_question(text) and _leans_back(text, record)
            and _points_at_the_record(text, record, memory)):
        return False
    mine = _entry(text)
    if mine is None:
        return False
    theirs = _entry(str(record.get("text") or ""))
    return theirs is not None and theirs.id != mine.id


def _leans_back(text, record):
    found = words(text)
    if any(word in REFERRING for word in found):
        return True
    if PROPERTY.search(" ".join(found)):
        return True
    if PART_OF_THE_ONE.search(" ".join(found)):
        return True
    if ABOUT_ANOTHER.search(" ".join(found)):
        return True
    return bool(set(keywords(text)) & set(record.get("words") or ()))



def _points_at_the_record(text, record, memory=None):
    found = words(text)
    if a_placeholder_pronoun(text):
        found = [word for word in found if word != "it"]
    if any(word in REFERRING for word in found):
        return True
    if PART_OF_THE_ONE.search(" ".join(found)):
        return True
    if ABOUT_ANOTHER.search(" ".join(found)):
        return True
    mine = set(keywords(text))
    if not mine - MEASURE_WORDS:
        return True
    if mine & set(record.get("words") or ()):
        return True
    said = ""
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if isinstance(turns, list) and turns and isinstance(turns[-1], dict):
        said = str(turns[-1].get("bot") or "")
    return bool(mine and said and mine & set(words(said)))


def _leads_a_question(text):
    found = words(text)
    return "?" in text or (bool(found) and found[0] in RETURN_ASKS)


def _switches(text):
    low = " ".join(words(text))
    return any(low.startswith(s) or (" " + s + " ") in (" " + low + " ") for s in SWITCHERS)


_LEADS_IN = re.compile(r"^(?:(?:ok|okay|k|kk|so|well|oh|ah|and|but|um+|uh+|er+|hmm+|right|yeah|yep|"
                       r"also|plus|now)[\s,.!-]+)*", re.I)


def opens_by_switching(text):
    low = _LEADS_IN.sub("", " ".join(words(text)))
    return any(low.startswith(switcher) for switcher in SWITCHERS)


CORRECTION_NOISE = frozenset("""sorry apologies apology correction correcting wrong mistake
mean meant rather wait oh""".split())


DETAIL_WORDS = frozenset("""
january february march april may june july august september october november december
jan feb mar apr jun jul aug sep sept oct nov dec
monday tuesday wednesday thursday friday saturday sunday weekend weekday
morning afternoon evening night tonight today tomorrow yesterday day days week weeks
month months year years hour hours minute minutes oclock am pm
people person persons guest guests adult adults child children kid kids
pound pounds quid euro euros dollar dollars pence penny
kilo kilos kg gram grams litre litres liter liters pint pints cup cups tablespoon tablespoons
half quarter dozen
""".split())


def _without_switchers(text):
    parts = [part for switcher in SWITCHERS for part in switcher.split()]
    return " ".join(word for word in words(text)
                    if word not in parts and word not in CORRECTION_NOISE and word not in ACKS)


def _only_details(text, record):
    have = set(record.get("words") or [])
    fresh = [key for key in keywords(_without_switchers(text)) if key not in have]
    return all(key in DETAIL_WORDS for key in fresh)


A_THING_ON_ITS_WAY = re.compile(
    r"\b(?:thinking\s+(?:of|about)|planning\s+(?:on|to)|hoping\s+to|considering|going\s+to|"
    r"about\s+to|thinking\s+we\s+might|might|may|could)\s+"
    r"(?:get|getting|have|having|adopt|adopting|buy|buying|rescue|rescuing|rehome|rehoming|"
    r"look\s+at|look\s+for|find|finding|pick|picking\s+up|collect|collecting|bring\s+home)\b"
    r"|\b(?:looking\s+(?:at|for)|shopping\s+for|on\s+the\s+lookout\s+for)\s+(?:a|an|another)\b"
    r"|\b(?:getting|adopting|rescuing|rehoming|wanting|want|wanted)\s+(?:a|an|another|one)\b", re.I)
NAMES_THE_THING = re.compile(
    r"^\W*(?:(?:ok|okay|so|well|oh|ah|no|nope|sorry|actually|wait|hmm|erm?|um)\b[\s,.!-]*)*"
    r"(?:its|it'?s|it\s+is|that'?s|that\s+is|i\s+mean|i\s+meant|make\s+that)\s+"
    r"(?:an?\s+|the\s+|just\s+|only\s+|really\s+)?[a-z][a-z' -]{2,30}"
    r"(?:\s*[,.!-]*\s*(?:sorry|apologies|thanks|thank\s+you|actually|though|then|i\s+think|hmm))*$",
    re.I)
FRESH_NAMES = 3


def _the_plan_a_correction_renames(memory, text):
    record = current(memory)
    if not isinstance(record, dict) or _after_an_emergency(memory):
        return None
    if not NAMES_THE_THING.match(" ".join(str(text or "").lower().split())):
        return None
    if not A_THING_ON_ITS_WAY.search(str(record.get("text") or "")):
        return None
    extra = [key for key in keywords(text) if key not in (record.get("words") or ())]
    if not extra:
        return None
    record["words"] = (list(record.get("words") or []) + extra[:FRESH_NAMES])[:12]
    return record

MY_THING_IS = re.compile(r"^\W*(?:my|our|the)\s+([a-z]+)\s+(?:is|are|was|were)\b")
SHORTHAND = re.compile(r"^\d+(?:\.\d+)?\s*[km]$|^\d+(?:\.\d+)?\s*(?:k|m)\b")
RECENT_TURNS = 3
FRESH_WORDS = 2


def _is_a_quantity(reading):
    for number in reading.get("numbers") or []:
        if not isinstance(number, dict):
            continue
        if number.get("unit"):
            return True
        if SHORTHAND.match(str(number.get("text") or "").strip()):
            return True
    return False


WHEN_OR_AMOUNT = re.compile(
    r"\b(?:since|for|about|around|started|began|start|most|every|each|last|this|next|"
    r"a day|a week|a month|a year|once|twice|times)\b|\b\d+\b")
NAMED_THING = re.compile(r"\b(?:my|our|your|his|her|their|the|a|an|some|any)\s+[a-z]")


def _is_a_when_or_how_often(text, memory):
    read = memory.get("understood")
    if not isinstance(read, dict) or read.get("kind") != "statement":
        return False
    found = words(text)
    if not found or len(found) > 8:
        return False
    if WHEN_OR_AMOUNT.search(" ".join(found)) is None:
        return False
    if NAMED_THING.search(" " + " ".join(found) + " "):
        return False
    if len(keywords(text)) > 4:
        return False
    if _entry(text) is not None:
        return False
    record = current(memory)
    if record is None:
        return False
    turn = record.get("turn")
    if isinstance(turn, int) and len(memory.get("turns") or []) - turn > RECENT_TURNS:
        return False
    return True


CONSTRAINT_IS = re.compile(
    r"^(?:my|our|the)\s+(?:budget|price|cost|age|salary|wage|wages|income|savings|time|"
    r"spending|tariff|allowance)\s+(?:is|was|'s)\b")
ON_A_BUDGET = re.compile(
    r"^(?:we|i|were|im)(?:\s+(?:are|am|was))?\s+(?:on|under|within|keeping to|sticking to|"
    r"trying to keep to)\s+(?:a|the|our|my|tight|small|strict)?\s*budget\b")


def _only_names_the_constraint(text, memory):
    read = memory.get("understood")
    if not isinstance(read, dict) or read.get("kind") != "statement":
        return False
    said = " ".join(words(text))
    on_a_budget = ON_A_BUDGET.match(said) is not None
    if CONSTRAINT_IS.match(said) is None and not on_a_budget:
        return False
    if on_a_budget:
        if not re.search(r"\d", said):
            return False
    elif not _is_a_quantity(read):
        return False
    record = current(memory)
    if record is None:
        return False
    turn = record.get("turn")
    if isinstance(turn, int) and len(memory.get("turns") or []) - turn > RECENT_TURNS:
        return False
    return True


def _adds_a_detail(text, memory):
    read = memory.get("understood")
    if not isinstance(read, dict) or read.get("kind") != "statement":
        return False
    if not _is_a_quantity(read):
        return False
    record = current(memory)
    if record is None:
        return False
    turn = record.get("turn")
    if isinstance(turn, int) and len(memory.get("turns") or []) - turn > RECENT_TURNS:
        return False
    named = MY_THING_IS.match(" ".join(words(text)) + " ")
    if named and stem(named.group(1)) not in (record.get("words") or []):
        return False
    numeric = set()
    for number in read.get("numbers") or []:
        if isinstance(number, dict):
            numeric.update(stem(word) for word in words(number.get("text") or ""))
    known = set(record.get("words") or [])
    fresh = [w for w in keywords(text) if w not in known and w not in numeric]
    return len(fresh) <= FRESH_WORDS


WHO = frozenset("""
mum mom mam mummy mumma mother dad daddy father papa son daughter child kid baby toddler
partner husband wife spouse boyfriend girlfriend fiance fiancee sister brother sibling stepsister
stepbrother stepson stepdaughter nan nana gran granny grandma grandmother grandad grandpa
granddad grandfather grandparents grandparent aunt auntie uncle cousin nephew niece friend
flatmate housemate neighbour neighbor landlord landlady lodger manager
tutor childminder carer hairdresser barber instructor
""".split())

WHO_SAID = re.compile(r"\b(?:my|our)\s+(" + "|".join(sorted(WHO, key=len,
                                                             reverse=True)) + r")(?:'s|s)?\b")
WHO_SAID_THIRD = re.compile(r"\b(?:his|her|their)\s+(" + "|".join(sorted(WHO, key=len,
                                                                         reverse=True))
                            + r")(?:'s|s)?\b")


def person(text):
    found = WHO_SAID.search(" ".join(words(text)))
    return found.group(1) if found else None


A_BARE_PRONOUN_SUBJECT = re.compile(
    r"\A(?:and|but|so|then|now|also|still)?\s*(?:he|she|they|hes|shes|theyre)(?:'s|'re)?\b")
A_QUESTION_THEY_ASK = re.compile(
    r"\b(?:asks?|asked|asking|keeps? asking|kept asking|wonders?|wondered|wondering|"
    r"wants? to know|wanted to know|says?|said|tells?|told|thinks?|thought|forgets?|forgot|"
    r"remembers?|remembered)\b[^.?!]*?\b(?:where|what|when|why|how|who|if|whether)\b")


def _named_inside_a_question(text):
    line = " ".join(words(str(text or "").lower().replace("\u2019", "'")))
    if not A_BARE_PRONOUN_SUBJECT.search(line):
        return False
    return bool(A_QUESTION_THEY_ASK.search(line))


def person_named(text, memory=None):
    who = person(text)
    if who:
        if about(memory) is not None and _named_inside_a_question(text):
            return None
        return who
    if about(memory) is not None:
        return None
    found = WHO_SAID_THIRD.search(" ".join(words(text)))
    return found.group(1) if found else None


def about(memory):
    record = memory.get("person") if isinstance(memory, dict) else None
    return record if isinstance(record, dict) and record.get("who") else None


PERSON_TROUBLE = (
    ("homeward", re.compile(
        r"\b(?:out of|home from|back from|discharged from|released from|let out of|"
        r"came out of|come out of|got out of|getting out of)\s+(?:the\s+)?hospital\b")),
    ("hospital", re.compile(
        r"\b(?:admitted|taken|took|rushed|whisked|brought|moved|transferred)\s+"
        r"(?:in|into|to|back to)\s+(?:the\s+)?(?:hospital|ward|icu|itu|a&e|a and e|resus)\b|"
        r"\b(?:went|gone|been|is|are|was|were|kept|staying|stuck)\s+(?:in|into|back in|"
        r"back into)\s+(?:the\s+)?hospital\b|"
        r"\bwent (?:in)?to (?:the )?hospital\b"
        r"(?![^.?!]{0,18}\b(?:visit|see|collect|pick|drop|meet)\b)|"
        r"(?<!work )(?<!works )(?:on|in)\s+the\s+(?:ward|stroke unit|coronary care)\b|"
        r"\bkept in (?:overnight|in|for observation|for tests)\b|"
        r"\b(?:in|into) (?:intensive care|icu|itu|resus)\b|"
        r"\bdiagnosed (?:with|as having)\s+(?:cancer|a (?:brain |lung |bowel |breast |bone )?"
        r"tumou?r|leukaemia|leukemia|lymphoma|motor neurone|parkinsons?|a terminal|"
        r"something serious)\b")),
    ("hospital", re.compile(
        r"\b(?:in|at|on|still in) (?:the )?hospital\b|\bhad an operation\b|\boperation\b|"
        r"\bsurgery\b|\bbeing (?:seen|treated|looked after)\b")),
    ("known", re.compile(
        r"\b(?:diagnosed|diagnosis|has dementia|has alzheimers|already (?:has|had|sees)|"
        r"since the diagnosis|under the (?:doctor|hospital|memory clinic))\b")),
    ("care", re.compile(
        r"\b(?:care home|nursing home|residential home|in a home now|a home now)\b")),
    ("memory", re.compile(
        r"\b(?:forget(?:s|ting|ful)?|forgot|memory|remember(?:ing)? (?:things|where|names)|"
        r"confus(?:ed|ing)|muddled|dementia|alzheimers?|wandering|getting lost|"
        r"gets? lost|got lost|went missing|lost (?:her|his|their) way|"
        r"wander(?:s|ed|ing)? off|took a wrong turn|losing track|"
        r"repeat(?:s|ing)? (?:himself|herself|themselves|the same "
        r"(?:thing|story|tale|question))|"
        r"say(?:s|ing)? (?:me |us )?the same (?:thing|story|tale|question)|"
        r"tel(?:l|ls|ling) (?:me |us )?the same (?:thing|story|tale)|"
        r"ask(?:s|ing)? the same question|"
        r"wrong (?:name|word|words|thing)|call(?:s|ed)? (?:me|him|her|us|them) "
        r"(?!(?:all|every|each|when|if|about|back|later|again|whenever|once|twice|from|at|"
        r"in|on|to|for|with|so|yesterday|today|tomorrow|constantly|loads|lots|more|less|too|"
        r"up|out|off|over|and|or|but|urgent)\b)\w+|mixed up|"
        r"says? the same thing|told me the same|the wrong day)\b")),
    ("falls", re.compile(
        r"\b(?:fell|fallen|fall|falls|falling|tripped|tripping|trip|unsteady|wobbly on "
        r"(?:his|her|their) feet|balance)\b")),
    ("low", re.compile(
        r"\b(?:low mood|low spirits|feeling low|seems? low|so low|very low|a bit low|"
        r"won'?t go out|wont go out|not eating|off (?:his|her|their) food|not themselves|"
        r"no appetite)\b")),
    ("sleep", re.compile(
        r"\b(?:not sleeping|not sleeping through|sleeping badly|not sleeping well|"
        r"up all night|awake all night|waking (?:up )?(?:all|every) night|not sleeping at night)"
        r"\b")),
    ("ill", re.compile(
        r"\b(?:poorly|unwell|chest infection|"
        r"keeps (?:getting|having) (?:a |an |the )?(?:\w+ ){0,2}"
        r"(?:infections?|colds?|coughs?|cough|temperatures?|chest|bugs?|viruses?|virus|"
        r"migraines?|headaches?|nosebleeds?|faints?|blackouts?|tremors?|shakes?|"
        r"dizzy|dizziness|breathless|sick|unwell|worse|pain|pains|swollen)|getting worse|"
        r"got worse|in pain|aches?|aching|breathless|swollen|dizzy|dizziness|"
        r"doctor said|hospital|diagnosed)\b")),
)


YOUNG_PERSON = re.compile(
    r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|[1-9]|1[0-2])\s*"
    r"(?:months?|years?)?\s*old\b|\bis (?:one|two|three|four|five|six|seven|eight|nine|ten|"
    r"eleven|twelve)\b|\b(?:baby|toddler|newborn|little one|little boy|little girl|"
    r"schoolboy|schoolgirl|reception class)\b")
FELL_OUT = re.compile(r"\bf(?:ell|all|alls|alling|allen)\s+out\b(?!\s+of\b)|\bfell\s+about\b")
FALLS_FINE = re.compile(
    r"\b(?:laughed|laughed it off|no harm|wasn'?t hurt|was not hurt|unhurt|not a scratch|"
    r"slept it off|got straight (?:back )?up|jumped (?:straight )?up|ran off|carried on|"
    r"waved it off|no damage)\b|"
    r"\b(?:he|she|they|it|hes|shes|theyre)(?:'s|'re)?\s+(?:is |was |seems |looks )?"
    r"(?:fine|ok|okay|alright)\b")
A_JOB_AT = re.compile(
    r"\b(?:works?|working|worked|starts?|started|starting|got a job|gets a job|getting a job|"
    r"hired|employed|shifts?|night shift|day shift|late shift|early shift|job|jobs|career|"
    r"boss|colleague|colleagues|manager|salary|wages|pay|overtime|contract)\b"
    r"[^.!?]{0,40}?\b(?:at|in|on|for|as)\b[^.!?]{0,14}?\b(?:the\s+)?(?:hospital|ward|unit|"
    r"icu|itu|a&e|a and e|care home|nursing home|hospice|clinic|surgery|pharmacy|practice)\b|"
    r"\b(?:my|his|her|their|our)\s+(?:new\s+)?(?:job|work|shift)\b|"
    r"\b(?:works?|working|worked)\s+(?:there|here|nights|days|shifts|full time|part time)\b")
SOMETHING_WRONG = re.compile(
    r"\b(?:ill|unwell|poorly|sick|sickness|pain|painful|hurts?|hurting|aching|aches|worse|worst|"
    r"fell|fallen|falling|fainted|collapsed|diagnosed|diagnosis|dementia|alzheimers|cancer|"
    r"operation|surgery|admitted|in hospital|on the ward|intensive care|icu|a&e|"
    r"cant|cannot|can'?t|unable|stopped|keeps|kept|forgetting|forgetful|confused|"
    r"confusion|weak|weaker|breathless|bleeding|infection|temperature|"
    r"tests?|results?|scan|appointment|worried|worrying|worry|decline|declining|"
    r"not (?:been )?(?:himself|herself|themselves)|unsteady|dizzy)\b")
CHANGE = re.compile(
    r"\b(?:new|newly|worse|worsening|suddenly|all of a sudden|since|these days|lately|recently|"
    r"stopped|no longer|used to|gone downhill|going downhill|declin(?:e|ed|ing)|"
    r"getting (?:worse|more|confused|forgetful)|"
    r"(?:this|last) (?:week|month|couple of|few)|over the (?:last|past))\b")


A_WORRY_AFTER = re.compile(
    r"\b(?:but|however|though|except)\b|\bstill\s+(?:very\s+|quite\s+|really\s+)?"
    r"(?:weak|poorly|unwell|bad|badly|tired|no better|not himself|not herself|not themselves)\b")


A_CHILDS_PERSON = re.compile(
    r"\b(?:son|daughter|kid|kids|child|children|little one|little boy|little girl|baby|"
    r"toddler|newborn|schoolboy|schoolgirl)\b|"
    r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|"
    r"fourteen|fifteen|sixteen|seventeen|\d{1,2})[\s-]*(?:year|yr)s?[\s-]*old\b")
A_GROWN_AGE = re.compile(r"\b(?:1[89]|[2-9]\d)\b|\b(?:eighteen|nineteen|twenty|thirty|"
                         r"forty|fifty|sixty|seventy|eighty|ninety)\b")
REPEATED_SAID = re.compile(
    r"\brepeat(?:s|ing)? the same (?:story|tale|question)|"
    r"\bsay(?:s|ing)? (?:me |us )?the same (?:thing|story|tale|question)|"
    r"\btel(?:l|ls|ling) (?:me |us )?the same (?:thing|story|tale)|"
    r"\bask(?:s|ing)? the same question\b")


def trouble(text):
    low = " ".join(str(text).lower().replace("\u2019", "'").split())
    if A_JOB_AT.search(low) and not SOMETHING_WRONG.search(low):
        return None
    for kind, pattern in PERSON_TROUBLE:
        if not pattern.search(low):
            continue
        if kind == "known" and not CHANGE.search(low):
            continue
        if kind == "memory" and REPEATED_SAID.search(low) \
                and A_CHILDS_PERSON.search(low) and not A_GROWN_AGE.search(low):
            continue
        if kind == "homeward" and A_WORRY_AFTER.search(low):
            continue
        if kind == "falls" and (YOUNG_PERSON.search(low) or FALLS_FINE.search(low)
                                or FELL_OUT.search(low)):
            continue
        return kind
    return None


def _keep_person(memory, text):
    turn = len(memory.get("turns") or [])
    who = person_named(text, memory)
    kind = trouble(text)
    if who:
        kept = about(memory) or {}
        if kept.get("who") != who or kept.get("said") != text.strip():
            memory["person"] = {"who": who, "said": text.strip(), "turn": turn}
        record = memory["person"]
    else:
        record = about(memory)
        if record is not None:
            record["turn"] = turn
    if record is not None and kind:
        if record.get("trouble") != kind:
            record["trouble_turn"] = turn
        record["trouble"] = kind
    return record


def _after_an_emergency(memory):
    turns = memory.get("turns")
    if isinstance(turns, list) and turns and isinstance(turns[-1], dict):
        return turns[-1].get("module") == "safety"
    return False


CORRECTION_LINE = re.compile(
    r"^[\W]*(?:oh|sorry|no|nope|actually|oops|wait|hang on)\b[^!?]{0,60}\bnot\b|"
    r"\b(?:i\s+meant|i\s+mean|make\s+that)\b|\bnot\s+(?:a|an|the)\s+[a-z]", re.I)


def _after_a_correction(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns or not isinstance(turns[-1], dict):
        return False
    said = turns[-1].get("user")
    if not isinstance(said, str) or not said.strip():
        return False
    return bool(CORRECTION_LINE.search(" ".join(said.lower().split())))


INSIDE_A_SAFETY_THREAD = ("carers_turn", "safety_cards")


def in_a_safety_thread(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return False
    for turn in reversed([t for t in turns if isinstance(t, dict)][-3:]):
        module = turn.get("module")
        if module == "safety":
            return True
        if module in INSIDE_A_SAFETY_THREAD or module in ("greeting", None):
            continue
        return False
    return False


WH_WORD_WITHOUT_ITS_APOSTROPHE = re.compile(r"\b(what|how|when|where|why|who|which)s\b")


def _the_apostrophe_back(low):
    return WH_WORD_WITHOUT_ITS_APOSTROPHE.sub(r"\1 is", low)


def return_target(text):
    low = _the_apostrophe_back(" ".join(words(text)))
    found = RETURN_LEAD.match(low)
    if found:
        rest = low[found.end():].strip(" ,.?!")
        return _the_thing(rest)
    casual = CASUAL_LEAD.match(low)
    if not casual:
        return ""
    target = low[casual.end():].strip(" ,.?!")
    parts = target.split()
    if not parts or parts[0] not in CASUAL_OPEN:
        return ""
    return _the_thing(target)


HELPER_ASKS = frozenset("""
is are was were am do does did have has had can could should would will shall if whether
""".split())
ING_VERBS = frozenset("""
aching acting adding asking baking beating becoming beginning biting bleeding boiling breaking
breathing bringing building burning buying calling carrying catching changing clicking climbing
closing coming cooking costing coughing counting crying cutting dancing dealing deciding digging
doing drawing dreaming dressing driving dropping drying eating expecting failing falling feeding
feeling filling finding finishing fitting flying following forgetting getting giving going growing
happening hating having hearing helping hiding hitting holding hoping hurting itching jumping
keeping kicking knocking landing laughing leaking leaning learning leaving lifting listening
living looking losing making meaning meeting missing moving needing opening paying picking playing
pointing pressing pulling pushing putting raining reaching reading relaxing remembering riding
ringing rising running saying seeing selling sending shaking showing singing sitting sleeping
sliding smelling smiling sneezing speaking spending spilling standing starting staying stealing
sticking stopping struggling studying swimming taking talking tasting teaching telling thinking
throwing ticking tightening trying turning waking walking wanting washing watching wearing
weighing winning wondering working worrying writing
""".split())
VERB_PHRASE_AFTER = frozenset("""
been being had got gotten not no never still always just already also now going getting doing
making taking coming putting seeing saying starting trying
""".split())


MODALS = frozenset("would could should can will shall may might must ought".split())


def _a_question_after_the_thing(rest, split):
    parts = rest.split()
    if split >= len(parts) or parts[split] not in HELPER_ASKS:
        return True
    after = parts[split + 1].strip(".,!?;:") if split + 1 < len(parts) else ""
    if not after:
        return True
    if parts[split] in MODALS and (after in ING_VERBS or after.endswith("ed")):
        return True
    return not (after in VERB_PHRASE_AFTER or after in ING_VERBS or after.endswith("ed"))


def _the_thing(rest):
    asked = re.search(r"[,?!;]|\b(?:" + "|".join(sorted(RETURN_ASKS)) + r")\b", rest)
    head = rest[:asked.start()] if asked else rest
    if asked and not _a_question_after_the_thing(rest, len(head.split())):
        return ""
    parts = head.split()
    while parts and (parts[-1] in CASUAL_OPEN or parts[-1] in STOPWORDS):
        parts.pop()
    if not parts or len(parts) > 3:
        return ""
    if any(part in CASUAL_VERB or part in RETURN_TIME for part in parts):
        return ""
    return " ".join(parts)


def _asks(text):
    if "?" in text:
        return True
    return any(word in RETURN_ASKS for word in text.split())


def asks_after(line, thing):
    low = _the_apostrophe_back(" ".join(words(line)))
    named = " ".join(words(thing))
    at = low.find(named) if named else -1
    if at >= 0:
        low = low[at + len(named):]
    return _asks(low)


def the_thing_asked_again(memory, text=""):
    record = resumed(memory)
    if not isinstance(record, dict) or not record.get("asks"):
        return ""
    thing = " ".join(str(record.get("asked") or "").lower().split())
    line = " ".join(str(text or "").lower().split())
    if not thing or not line:
        return ""
    at = line.find(thing)
    if at < 0:
        return ""
    tail = line[at + len(thing):].strip(" ,;:.-")
    if not tail:
        return ""
    return thing + " " + tail


def the_thing_went_back_to(memory):
    record = resumed(memory)
    if not isinstance(record, dict) or not record.get("asks"):
        return ""
    return " ".join(str(record.get("asked") or "").lower().split())


def _resume(memory, record, target, line=""):
    said = dict(record)
    said["subject"] = " ".join(words(target)) if target else said.get("subject") or ""
    memory["topic"] = said
    topics = memory.get("topics")
    if not isinstance(topics, list):
        topics = memory["topics"] = []
    topics[:] = [other for other in topics if other is not record
                 and (other.get("text") or "") != (said.get("text") or "")]
    topics.append(said)
    memory["return_to"] = said.get("text") or target
    memory["returned"] = {"text": said.get("text") or target, "asked": target,
                          "asks": asks_after(line, target),
                          "turn": len(memory.get("turns") or [])}
    _the_answer_on_the_return(memory, said)
    return said


def _the_answer_on_the_return(memory, said):
    kept = memory.get("entry_answers")
    if not isinstance(kept, list) or len(kept) < 2:
        return
    wanted = {form for word in keywords(said.get("text") or "") for form in (word, stem(word))}
    wanted -= STOPWORDS
    if not wanted:
        return
    best, best_score = None, 0
    for record in kept:
        if not isinstance(record, dict):
            continue
        forms = {form for key in set(record.get("keys") or ()) for form in (key, stem(key))}
        score = len(wanted & (forms - STOPWORDS))
        if score > best_score:
            best, best_score = record, score
    if not best or best is kept[-1]:
        return
    kept.remove(best)
    kept.append(best)
    memory["entry_answer"] = best


def resumed(memory):
    record = memory.get("returned")
    if not isinstance(record, dict) or not record.get("text"):
        return None
    if record.get("turn") != len(memory.get("turns") or []):
        return None
    return record


def current(memory):
    record = memory.get("topic")
    if isinstance(record, dict) and record.get("text"):
        return record
    return None


def _forms(word):
    forms = [word]
    if len(word) > 5 and word.endswith("ing"):
        base = word[:-3]
        forms += [base, base + "e"]
    elif len(word) > 4 and word.endswith("ed"):
        base = word[:-2]
        forms += [base, base + "e"]
    return forms


def alike(one, other):
    for left in _forms(one):
        for right in _forms(other):
            if left == right:
                return True
            if len(left) >= 4 and len(right) >= 4 and (left.startswith(right)
                                                       or right.startswith(left)):
                return True
            if len(left) >= 5 and len(right) >= 5 and left[:5] == right[:5]:
                return True
    return False


def find(memory, text):
    wanted = keywords(text)
    if not wanted:
        return None
    for record in reversed(memory.get("topics") or []):
        have = record.get("words") or []
        if any(alike(word, other) for word in wanted for other in have):
            return record
    return None


LEAD_ACKS = ACKS | GREET


def _this_line(record, memory):
    turn = len(memory.get("turns") or []) if isinstance(memory, dict) else 0
    return record.get("turn") == turn


def is_follow_up(text, memory):
    record = current(memory)
    if not record:
        return False
    if _this_line(record, memory):
        return False
    clean = " ".join(words(text))
    if not clean or is_ack(text) or clean in GREET:
        return False
    rest = [word for word in words(text)]
    while rest and rest[0] in LEAD_ACKS:
        rest = rest[1:]
    if rest:
        clean = " ".join(rest)
    low = clean
    if _switches(clean):
        return False
    found = words(text)
    if len(found) > 16:
        return False
    topic_words = set(record.get("words") or [])
    fresh = [k for k in keywords(text) if k not in topic_words]
    if KIND_ASK.search(low) and len(found) <= 10:
        return True
    if found[0] in CONTINUATION_START:
        if len(fresh) <= 2 and len(found) <= 8:
            return True
        if PROPERTY.search(low) and len(fresh) <= 3 and len(found) <= 10:
            return True
    if any(word in REFERRING for word in found) and len(fresh) <= 3:
        return True
    return len(fresh) <= 1 and len(found) <= 8


def context(memory, n=2):
    records = memory.get("topics")
    if not isinstance(records, list):
        return []
    return [r.get("text", "") for r in records[-n:] if r.get("text")]


def expand(text, memory):
    record = current(memory)
    if record and is_follow_up(text, memory):
        earlier = context(memory) or [record["text"]]
        return text + " (earlier: " + " / ".join(earlier) + ")"
    return text


MEASURED = frozenset(("how_long", "how_much", "how_many", "how_often", "time", "heat",
                      "money", "amount", "temperature"))
PROCEED = ("what should i do", "what do i do", "what now", "what next", "then what",
           "what about now", "where do i go from here")
ASK_ONLY = frozenset("""
long much many time times often usually cost costs price prices worth expensive cheap cheaper
temperature hot warm cold heat minute minutes hour hours day days week weeks month months year years
step steps best first next last thing things way ways take takes long quick quickly soon
start finish it that them they there this these those one ones again
""".split())

_LEAD_QUESTION = re.compile(r"^(?:whats?|which|how|when|where|who|why|do|does|did|is|are|"
                            r"can|could|should|would|will)\s+", re.I)

_RELATION = re.compile(r"\b(?:for|with|to|about|because|from)\s+(?:my|our|his|her|their)\b")

_FRAME_ASK = re.compile(r"\b(?:how|what|which|where|when|any way|ways|can|could|should|help)\b")
_WITHOUT_CLAUSE = re.compile(r"\s*\bwithout\b.*$")
_VERBS = ("bake", "cook", "make", "build", "write", "paint", "plant", "grow", "fix", "clean",
          "decorate", "buy", "book", "prepare", "host", "throw", "plan", "learn", "start",
          "assemble", "sew", "knit", "roast", "boil", "fry", "grill", "set", "sort", "get",
          "replace", "repair", "install", "paint", "renovate", "organise", "organize")
_WISH = ("thinking", "thought", "thinking about", "considering", "planning", "hoping", "wanting",
         "looking", "interested", "keen", "trying", "dreaming", "weighing up")
_ACTION = ("get", "getting", "have", "having", "lose", "losing", "go", "going", "save", "saving",
           "learn", "learning", "try", "trying", "start", "starting", "stop", "stopping",
           "quit", "quitting", "book", "booking", "take", "taking", "do", "doing", "see",
           "seeing", "buy", "buying", "move", "moving", "change", "changing", "adopt",
           "adopting", "rescue", "rescuing")


_PHRASAL = (
    "get rid of", "getting rid of", "got rid of", "get out of", "getting out of",
    "get on top of", "getting on top of", "get on with", "look after", "looking after",
    "look into", "looking into", "cope with", "coping with", "deal with", "dealing with",
    "put up with", "putting up with", "run out of", "running out of", "ran out of",
    "take care of", "taking care of", "keep up with", "keeping up with", "kept up with",
    "keep on top of", "keeping on top of", "keep track of", "keeping track of",
)
_PHRASAL_RE = re.compile(r"\b(?:" + "|".join(sorted((re.escape(p) for p in _PHRASAL),
                                                    key=len, reverse=True)) + r")\b")


def _gerund(verb):
    if verb.endswith("ie"):
        return verb[:-2] + "ying"
    if verb.endswith("e") and not verb.endswith(("ee", "ye", "oe")):
        return verb[:-1] + "ing"
    if (len(verb) > 2 and verb[-1] not in "aeiouwxy" and verb[-2] in "aeiou"
            and verb[-3] not in "aeiou"):
        return verb + verb[-1] + "ing"
    return verb + "ing"


_VERB_WORDS = tuple(sorted({v for v in _VERBS} | {_gerund(v) for v in _VERBS if len(v) > 2}))
_WISH_RE = re.compile(
    r"^(?:(?:please|so|and|but|well|ok|okay)\s+)?"
    r"(?:i'?m|im|i\s+am|we'?re|we\s+are|i\s+have|i'?ve|"
    r"(?:i|we|you|they|he|she)\s+(?:am|are|is|was|were))?"
    r"(?:\s+(?:also|still|just|really|probably|maybe|now|only))?\s*"
    r"(?:" + "|".join(sorted(set(_WISH) | set(_ACTION), key=len, reverse=True))
    + r")\b(?:\s+(?:to|of|about|on|at|into|up|for))?\s+(?:(?:a|an|the|another|some|any|my|our)\s+)?")
_LEAD = re.compile(r"^(?:please\s+)?(?:i'?m|im|i\s+am|i\s+(?:want|need|would like|'?d like)|"
                   r"we'?re|we\s+are|i'?ve|i\s+have)?\s*"
                   r"(?:to\s+)?(?:(?:" + "|".join(_VERB_WORDS) + r")\s+)"
                   r"(?:a|an|the|my|our|some|any|two|three|this|that)?\s*")

_CORRECTION_LEAD = re.compile(
    r"^(?:(?:no|nope|sorry|apologies|actually|oops|correction|wait)[\s,.!-]+|"
    r"my\s+mistake[\s,.!-]+|"
    r"i\s+(?:mean|meant|said|did\s+meant|didn'?t\s+mean)\s+(?:to\s+say\s+)?|"
    r"(?:its|it'?s|that'?s)\s+(?:actually\s+)?)+", re.I)
_TIME_WORDS = frozenset("""monday tuesday wednesday thursday friday saturday sunday
january february march april may june july august september october november december
week weekend month year morning afternoon evening night tonight today tomorrow yesterday
soon later midday noon am pm clock oclock""".split())
_CONSIDERING = re.compile(
    r"^(?:(?:i'?m|im|i am|we'?re|we are)\s+)?(?:"
    r"(?:thinking (?:of|about)|looking (?:at|for|into|round at)|considering|in the market for|"
    r"keen (?:on|to)|after)"
    r"|(?:getting|buying)(?=\s+(?:a|an|the|some|any|another|my|our|your|their|his|her|its|this|"
    r"that|these|those|new|used|second|old|decent|proper|cheap|good|nice|little|big|small|first|"
    r"one|two|three)\b))\s+")
_BUYING_A_STATE = re.compile(
    r"^(?:(?:i'?m|im|i\s+am|we'?re|we\s+are)\s+)?(?:get|getting|buy|buying)\b(?!\s+(?:a|an|the|"
    r"some|any|another|my|our|your|their|his|her|its|this|that|these|those|new|used|second|old|"
    r"decent|proper|cheap|good|nice|little|big|small|first|one|two|three)\b)")
_MAX_SUBJECT = 4


def _strip_considering(source):
    while True:
        stripped = _CONSIDERING.sub("", source)
        if stripped == source:
            return source
        source = stripped


_A_FIGURE = frozenset("""pound pounds quid euro euros dollar dollars grand kilos kilo kg stone
    stones lb lbs ounce ounces gram grams litre litres pint pints mile miles minute minutes hour
    hours week weeks month months year years""".split())


_HANDOFF_THROAT = re.compile(
    r"^(?:(?:and|oh|ooh|ok|okay|so|but|right|ah|er|um|hmm|also|plus|hey|ta|anyway|then|just|"
    r"well|sorry)[\s,:-]*)+")


def _only_a_handoff(head):
    text = " ".join(str(head or "").lower().split()).strip(" ,.;:!?-")
    text = _HANDOFF_THROAT.sub("", text).strip(" ,.;:!?-")
    for lead in sorted(lexicon.HANDOFF_LEADS, key=len, reverse=True):
        if text == lead or (text.startswith(lead) and not keywords(text[len(lead):])):
            return True
    return False


_DATE_OCCASIONS = frozenset(stem(word) for word in
                             """birthday birthdays anniversary christmas xmas easter""".split())
_DATE_FILLER = frozenset("""next last this coming on in at the of""".split())
_MAKING_A_THING = re.compile(
    r"\b(?:make|making|bake|baking|cook|cooking|prepare|preparing|build|building|do|doing)\s+"
    r"(?:\w+\s+){0,2}?(?:a|an|the|some)\s+[a-z']+")


_PEOPLE = frozenset()


def _the_people():
    global _PEOPLE
    if not _PEOPLE:
        from .facts import RELATIONS
        _PEOPLE = frozenset(form for word in RELATIONS for form in (word, stem(word)))
    return _PEOPLE


def _a_word_of_a_date(word):
    forms_ = (word, stem(word))
    return (any(form in _DATE_OCCASIONS for form in forms_)
            or any(form in _TIME_WORDS for form in forms_)
            or word in _DATE_FILLER
            or any(form in _A_FIGURE for form in forms_)
            or any(form in _the_people() for form in forms_))


def _only_a_date(clause):
    kept = keywords(clause)
    if not kept or not any(stem(word) in _DATE_OCCASIONS for word in kept):
        return False
    return all(_a_word_of_a_date(word) for word in kept)


def _the_thing_after_a_date(text):
    parts = re.split(r"\b(?:and|but)\b|[,;]", text, maxsplit=1)
    if len(parts) < 2:
        return ""
    head, tail = parts
    if not _only_a_date(head) or not keywords(tail):
        return ""
    return tail if _MAKING_A_THING.search(tail) else ""


def gist(text):
    source = " ".join(str(text or "").lower().split())
    source = _CORRECTION_LEAD.sub("", source)
    for switcher in sorted(SWITCHERS, key=len, reverse=True):
        if source.startswith(switcher):
            source = source[len(switcher):].lstrip(" ,.!-")
            break
    dated = _the_thing_after_a_date(source)
    if dated:
        source = dated
    source = " ".join(_PHRASAL_RE.sub(" ", source).split())
    source = _RELATION.split(source)[0]
    whole = source
    if _FRAME_ASK.search(source):
        trimmed = _WITHOUT_CLAUSE.sub("", source).strip(" ,.;:!?")
        if trimmed and keywords(trimmed):
            source = trimmed
    source = _strip_considering(source)
    buying = bool(_BUYING_A_STATE.match(source))
    wished = False
    for _ in range(3 if not buying else 0):
        stripped = _WISH_RE.sub("", source)
        if stripped == source or not stripped.strip(" ,.;:!?"):
            break
        source = stripped
        wished = True
    before_split = source
    segments = re.split(r"\b(?:for|tonight|today|tomorrow|yesterday|this|next)\b", source)
    source = segments[0]
    if not wished and not buying:
        source = _LEAD.sub("", source.strip(" ,.;:!?"))
        while True:
            trimmed = _LEAD_QUESTION.sub("", source)
            if trimmed == source or not trimmed.strip():
                break
            source = trimmed
    source = _strip_considering(source)
    head, _, after_handoff = source.partition(",")
    source = after_handoff if after_handoff.strip() and _only_a_handoff(head) else \
        re.split(r"[,;]", source)[0]
    kept = [word for word in keywords(source) if word not in ASK_ONLY]
    while kept and kept[-1] in _TIME_WORDS:
        kept.pop()
    if kept and all(word in _A_FIGURE for word in kept):
        for part in segments[1:]:
            later = [word for word in keywords(part)
                     if word not in ASK_ONLY and word not in _TIME_WORDS]
            if later and not all(word in _A_FIGURE for word in later):
                kept = later
                break
    if not kept and wished:
        for source in (before_split, whole):
            kept = [word for word in keywords(source)
                    if word not in ASK_ONLY and word not in _TIME_WORDS]
            if kept:
                break
    if not kept:
        return ""
    return " ".join(kept[:_MAX_SUBJECT])


_ROOM_LIMIT = re.compile(
    r"^(?P<head>(?:my|our|the|his|her|their|this|that|your)?\s*[a-z' ]{0,18}?)\s*"
    r"(?:is|are|was|were|seems|feels|gets)?\s*"
    r"(?:a bit |really |quite |very |so |too |dead |proper )*(?:small|tiny|cramped|poky|narrow)$")

_HOME_SPACES = frozenset((
    "flat", "house", "home", "room", "rooms", "kitchen", "bedroom", "bedrooms", "bathroom",
    "lounge", "hall", "hallway", "landing", "garage", "loft", "attic", "basement", "cellar",
    "study", "porch", "conservatory", "utility",
))


def _room_limit(text):
    words_ = " ".join(str(text or "").lower().split())
    found = _ROOM_LIMIT.match(words_)
    if not found:
        return ""
    head = found.group("head").strip(" ,.;:!?-")
    if not head:
        return ""
    return head if head.split()[-1] in _HOME_SPACES else ""


def _thing_of(memory, record):
    if not isinstance(record, dict):
        return None
    back = str(record.get("of") or "")
    if not back:
        return None
    for other in reversed(memory.get("topics") or []):
        if isinstance(other, dict) and str(other.get("text") or "") == back:
            return other
    return None


def _about_record(memory):
    records = memory.get("topics")
    if not isinstance(records, list):
        return current(memory) or {}
    for record in reversed(records):
        if not isinstance(record, dict) or _room_limit(record.get("text")):
            continue
        if _names_nothing(record):
            continue
        return record
    return current(memory) or {}


def _names_nothing(record):
    if " ".join(str(record.get("subject") or "").split()):
        return False
    return not gist(record.get("text") or "")


def subject(memory):
    known = memory.get("user") if isinstance(memory.get("user"), dict) else {}
    record = _about_record(memory)
    thing = _thing_of(memory, record)
    if thing is not None:
        record = thing
    now = " ".join(str(record.get("subject") or "").split()) or gist(record.get("text") or
                                                                    topic_text(memory))
    planned = gist(known.get("plan") or "")
    if planned and now and planned in now:
        return planned
    return now or planned


def topic_text(memory):
    record = current(memory)
    return record["text"] if record else ""


DURATION_ASK = re.compile(r"\bhow (?:long|many (?:hours|days|weeks|months|minutes|years))\b")

DURATION_WORDS = frozenset("""
how long many much hours hour days day weeks week months month minutes minute years year will
would does do did is was it that this one they them take takes taken cost costs last lasts
to for the a an in at on about
""".split())

ACTION = frozenset("""
learn lose get fix build paint clean save train study grow cook bake make do sort finish write
read find repair install set move pack apply book plant hire buy sell replace service bleed
insulate lay tile sand plaster dig compost prune knit sew drive fly travel play practise
practice teach organise organize plan prepare recover heal quit stop start cut reduce pay earn
pass sit cycle swim run walk redecorate declutter tidy clear chop boil roast freeze iron mend
patch sharpen assemble
""".split())

MAX_ACTION = 6

PERSON_LEAD = frozenset("""
i we me us my our she he they her his their them 'm im am was were is are have had been
really just also still only
want wanna wanted need needed try trying plan planning plans hope hoping think thinking
like 'd would will going keep keeping kept start started starting get getting got
""".split())

ACTION_AFTER = frozenset("to of about".split())


def _the_action_word(line):
    for index, word in enumerate(line):
        found = forms(word) & ACTION
        if not found:
            continue
        before = line[:index]
        if before and before[-1] in ACTION_AFTER:
            pass
        elif any(word not in PERSON_LEAD for word in before):
            continue
        return index, sorted(found, key=len)[0]
    return None, None


def action(memory):
    said = " ".join(words(topic_text(memory)))
    if not said:
        return ""
    line = said.split()
    index, base = _the_action_word(line)
    if index is None:
        return ""
    tail = " ".join(line[index:])
    tail = re.split(r"\b(?:and|but|because|so|then|when|if|before|after)\b", tail)[0]
    words_of_the_action = tail.split()[:MAX_ACTION]
    words_of_the_action[0] = base
    return " ".join(words_of_the_action).strip()


def written_out(text, memory):
    low = " ".join(words(text))
    if not low or not DURATION_ASK.search(low):
        return None
    if any(word not in DURATION_WORDS for word in low.split()):
        return None
    done = action(memory)
    if not done:
        return None
    said = " ".join(str(text).split()).rstrip("?.! ")
    return said + " to " + done + "?"


ONE_ATTRIBUTE = (
    (re.compile(r"\b(?:temperature|heat)\b"), "oven temperature for {thing}"),
    (re.compile(r"\b(?:time|timing|duration)\b"), "how long does {thing} take"),
    (re.compile(r"\b(?:size)\b"), "what size {thing} do i need"),
    (re.compile(r"\b(?:price|cost)\b"), "how much does {thing} cost"),
)
ATTRIBUTE_WORDS = frozenset("""the a an and so ok okay or what which how about oven temp
temperature heat time timing duration size price cost much long does do i need it take
for of""".split())
NOT_A_THING = frozenset("""it its that this these those they them there here thing things one
ones more less some any people person someone anyone everybody everyone you u me us we i""".split())
A_STATE = frozenset("""late early broken broke leaking noisy loud quiet slow fast cold hot warm
freezing boiling dirty clean empty full stuck blocked jammed wrong old new cheap expensive
rubbish useless dead faulty missing gone off mouldy soggy dry wet burnt raw undercooked""".split())


def _named_a_thing(line):
    thing = gist(line)
    if not thing or thing in NOT_A_THING:
        return ""
    if all(word in ATTRIBUTE_WORDS for word in thing.split()):
        return ""
    if thing.split()[-1] in A_STATE:
        return ""
    return thing


def _the_thing_on_the_table(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return ""
    for turn in list(reversed(turns))[:4]:
        line = str((turn or {}).get("user") or "") if isinstance(turn, dict) else ""
        thing = _named_a_thing(line)
        if thing:
            return thing
    return ""


def attribute_of_the_thing(text, memory):
    low = " ".join(words(text))
    if not low or len(low.split()) > 5:
        return None
    if any(word not in ATTRIBUTE_WORDS for word in low.split()):
        return None
    frame = None
    for pattern, said in ONE_ATTRIBUTE:
        if pattern.search(low):
            frame = said
            break
    if frame is None:
        return None
    thing = _the_thing_on_the_table(memory)
    if not thing:
        return None
    return frame.format(thing=thing)


DETAIL = re.compile(
    r"\b(?:allerg\w*|intoleran\w*|vegetarian|vegan|coeliac|gluten|free\b|diet\w*|budget|cheaper|"
    r"expensive|afford|only (?:got|have)|no (?:time|room|oven|car)|can't|cannot|couldn't|"
    r"doesn't|don't|won't|hate[sd]?|love[sd]?|prefer[s]?|instead|substitut\w+|swap|without|"
    r"left ?over|freez\w*|reheat\w*|shelf life|keeps? for)\b", re.I)


def key_subject(text, memory=None):
    if memory is not None:
        for record in reversed(memory.get("topics") or []):
            if not isinstance(record, dict) or str(record.get("text") or "") != str(text):
                continue
            if _this_line(record, memory):
                break
            thing = _thing_of(memory, record)
            if thing is not None:
                found = _key_subject(str(thing.get("text") or ""))
                if found:
                    return found
            break
    found = _key_subject(text)
    if found:
        return found
    if memory is not None:
        for record in reversed(memory.get("topics") or []):
            text_ = record.get("text") if isinstance(record, dict) else None
            found = _key_subject(str(text_ or ""))
            if found:
                return found
    return keywords(text)[:3]


ASK_PART = frozenset("""how what when where why which who whose long much many time often far
soon""".split())

PRICE_ASK = frozenset("""charge charges charging costing cost costs price prices priced quote
quotes quoted fee fees rate rates expensive cheaper afford free worth payable""".split())

ASKS_FOR_ADVICE = frozenset("""tip tips advice advise advising hint hints help helps helping
ideas idea suggestion suggestions thoughts thought recommend recommended""".split())


def _the_part_a_complaint_is_about(text):
    from ..knowledge.body import the_part_that_hurts
    return the_part_that_hurts(text)


CAUSE_OF_THE_COMPLAINT = re.compile(r"\b(?:since|after|because|from)\b")


def _the_cause_words(text):
    found = CAUSE_OF_THE_COMPLAINT.search(str(text or "").lower())
    if not found:
        return set()
    return set(words(str(text or "").lower()[found.end():]))


def _subject_words_to_carry(record, text, memory):
    topic_text = str((record or {}).get("text") or "") if isinstance(record, dict) else ""
    subject = key_subject(topic_text, memory)
    part = _the_part_a_complaint_is_about(topic_text)
    cause = _the_cause_words(topic_text)
    if part and cause and part not in words(text) and not _the_part_a_complaint_is_about(text):
        kept = [word for word in subject if word not in cause or word == part]
        if part not in kept:
            kept.insert(0, part)
        return kept
    return subject


def _key_subject(text):
    found = words(text)
    item = _entry(text)
    if item is None:
        return None
    out = []
    for part in item.key:
        for alternative in (part if isinstance(part, tuple) else (part,)):
            if not isinstance(alternative, str) or not _said(alternative, found):
                continue
            part_words = words(alternative)
            if not ASK_PART.intersection(part_words):
                out.extend(part_words)
            break
    return out or None


def _said(phrase, found):
    wanted = [stem(word) for word in words(phrase) if word not in STOPWORDS]
    if not wanted:
        return False
    if isinstance(found, (set, frozenset)):
        return all(word in {stem(one) for one in found} for word in wanted)
    have = [stem(word) for word in found]
    n = len(wanted)
    return any(have[i:i + n] == wanted for i in range(len(have) - n + 1))


def _where_the_topic_lands(topic):
    found = _entry(topic)
    if found is None:
        return None
    asked = set()
    for part in getattr(found, "ask", ()):
        for phrase in (part if isinstance(part, tuple) else (part,)):
            if isinstance(phrase, str):
                asked.update(words(phrase))
    if not asked:
        return found
    kept = [word for word in words(topic) if stem(word) not in asked and word not in asked]
    if len(kept) == len(words(topic)):
        return found
    other = _entry(" ".join(kept))
    if other is None or other is found:
        return found
    if len(_key_words_of(other) & set(keywords(topic))) < 2:
        return found
    return other


def an_entry_for(text):
    return _entry(text)


def _entry(text):
    from ..knowledge.lookup import find
    return find({"clean": str(text), "words": words(text)})


REFERRING_WORDS = frozenset("""it its that this these those they them there their one ones
he she him her his""".split())

DUMMY_IT = re.compile(
    r"\b(?:is|was|would|will)(?:n't)?\s+it\s+(?=(?:worth|ok|okay|better|best|rude|normal|"
    r"fine|safe|possible|legal|allowed|weird|strange|acceptable|polite|sensible|wise|cheaper|"
    r"easier|harder|a good idea|a good thing|too late|too soon)\b"
    r"[^?]*\b(?:a|an|the|some|any|my|your|our|their|his|her|another|one|two|three)\s+\w)")

ASK_MORE = frozenset("""often frequent frequently regularly sooner soonest longer quick quicker
soon best good""".split())
STAND_IN = frozenset("""go going gone get getting do doing done use using happen happening
happens be is are was were should shall can could would will want wants need needs have has
take taking start starting help helps helping check checks checking put putting place try tries
trying fix fixing sort sorting ease easing improve improving avoid avoiding prevent preventing
change changes changing add adding expect expecting""".split())


ABOUT_THE_CHAT = re.compile(
    r"\b(?:what\s+(?:do|did)\s+you\s+(?:know|remember|have|hear|got)"
    r"|what\s+have\s+(?:i|you)\s+(?:told|said|mentioned|got)"
    r"|what\s+did\s+i\s+(?:say|tell|mention)"
    r"|what\s+(?:am\s+i|are\s+we)\s+(?:up\s+to|on\s+about|planning|doing)"
    r"|remind\s+me\s+(?:what|who|when|where)"
    r"|what\s+were\s+we\s+(?:talking|speaking|on)\s+about"
    r"|do\s+you\s+(?:remember|know)\s+(?:me|my|what|who|that))\b")


ASK_CUE = re.compile(
    r"\?|(?:^|\b)(?:what|which|how|why|when|where|who|whose)(?:'?s|'?re)?\b"
    r"|(?:^|\b)(?:should|shall|can|could|would|will|does|did|is|are|am|any|anything"
    r"|something\s+else)\b")


ELIDED_ASK = re.compile(
    r"^(?:(?:ok|okay|so|and|also|plus|or|then|right|yeah|yes|oh|em|um)\s+)*"
    r"(?:any|anything|something|more|else|another|other|rest|what\s+about|how\s+about|"
    r"idea|ideas|tip|tips|thoughts|suggestions)\b")


SAME_ASK = re.compile(r"^(?:(?:ok|okay|so|and|also|plus|or|then|right|yeah|yes|oh)\s+|"
                      r"(?:what|how)\s+about\s+)", re.I)
COUNTING = frozenset("""one two three four five six seven eight nine ten eleven twelve a an some
few couple half slice slices piece pieces cup cups bowl bowls portion portions glass glasses
handful handfuls tin tins can cans spoon spoons tablespoon tablespoons teaspoon teaspoons each
more""".split())

THE_TAIL = re.compile(r"\b(?:in|for|of|at|on|with|from|into|about)\b", re.I)


def _the_last_question(memory):
    from ..understanding import understand
    for turn in reversed([one for one in (memory.get("turns") or []) if isinstance(one, dict)]):
        said = str(turn.get("user") or "").strip()
        if "?" in said or understand(said, memory).get("asks"):
            return said
    return ""


def how_much_of_the_thing_in_hand(line, memory):
    said = str(line or "").strip()
    if not SAME_ASK.match(said):
        return ""
    body = SAME_ASK.sub("", said)
    counted = words(gist(body))
    if not counted or not all(word in COUNTING or word.isdigit() for word in counted):
        return ""
    asked = _the_last_question(memory)
    if not asked:
        return ""
    head = ""
    for match in THE_TAIL.finditer(asked):
        head = asked[:match.end()]
    from ..understanding import understand
    if not head or not understand(head + " " + body, memory).get("asks"):
        return ""
    turns = [one for one in (memory.get("turns") or []) if isinstance(one, dict)]
    before = str((turns[-1] if turns else {}).get("user") or "")
    thing = [word for word in words(gist(before))
             if word not in words(head) and word not in words(said)]
    if not thing:
        return ""
    read = " ".join(words(head) + counted + thing)
    if not read or _entry(read) is None:
        return ""
    return read


def elided_ask(text):
    said = str(text or "").lower().strip()
    if not said or len(words(said)) > 5:
        return False
    if not ELIDED_ASK.match(said):
        return False
    asked = re.sub(r"^(?:(?:ok|okay|so|and|also|plus|or|then|right|yeah|yes|oh|em|um)\s+)*"
                   r"(?:how|what)\s+about\s+", "", said)
    return not re.search(r"\b(?:how|when|where|why|which|who)\b", asked)


def names_nothing(text):
    return not _content_words(text)


def _content_words(text):
    if ABOUT_THE_CHAT.search(str(text or "").lower()):
        return []
    return [word for word in words(text)
            if word not in STOPWORDS and word not in ASK_ONLY and word not in ASK_MORE
            and word not in STAND_IN]


LONG_IT_TAKES = re.compile(
    r"^\s*(?P<head>how long (?:does|do|will|would|is|are|should|can|could))\s+"
    r"(?:it|that|this|they|he|she)\s+take\s*[?.!]*$", re.I)
TOPIC_OPENS_WITH = re.compile(r"^\s*(?:i(?:'m|m| am| have| 've| want| need)?|we(?:'re|re| are)?|"
                              r"i've|ive|i'd|id)\s+", re.I)


def _the_topic_phrase(topic):
    said = " ".join(str(topic or "").lower().split()).strip(" .,;:!?")
    said = TOPIC_OPENS_WITH.sub("", said).strip()
    return said if len(said.split()) >= 2 else ""


def _a_length_of_the_job(item):
    for part in getattr(item, "key", ()) or ():
        said = set()
        for phrase in (part if isinstance(part, tuple) else (part,)):
            if isinstance(phrase, str):
                said.update(words(phrase))
        if said & {"take", "takes", "taking"} and said & {"how", "long", "time"}:
            return True
    return False
STAY_ASK = re.compile(r"\b(?:how (?:many|much) (?:days|nights|time)|how long)\b")
STAY_ONLY = frozenset("""how many much long days day nights night should shall i we you go going
there it for a an the in of time stay staying spend would will do can could need needs then""".split())
TRIP_FRAME = re.compile(
    r"\b(?:going|go|goes|off|trip|holiday|vacation|visit|visiting|fly|flying|travelling|traveling|"
    r"travel|heading|head|booked|booking|break|away|weekend|nights?|days)\b", re.I)
LIVES_THERE = re.compile(
    r"\b(?:live|lives|living|lived|move|moves|moved|moving|relocate|relocating|relocated|"
    r"emigrate|emigrating|grew up|grow up|born|work|works|working|commute|commuting)\b", re.I)


def the_city_of(topic):
    from ..knowledge.travel import CITY_DAYS, _find_in
    return _find_in(str(topic or "").lower(), CITY_DAYS)


def the_country_of(topic):
    from ..knowledge.travel import WHERE_TO_GO, _find_in
    return _find_in(str(topic or "").lower(), WHERE_TO_GO)


def asks_how_long_to_stay(line):
    return bool(STAY_ASK.search(str(line or "").lower()))


def going_there(place, topic):
    said = str(topic or "").lower()
    for match in LIVES_THERE.finditer(said):
        if str(place) in said[match.end():match.end() + 40]:
            return False
    return bool(TRIP_FRAME.search(said))


def a_stay_with_the_place(line, topic):
    lowered = str(line or "").lower()
    if not STAY_ASK.search(lowered):
        return None
    if [word for word in words(lowered) if word not in STAY_ONLY]:
        return None
    from ..knowledge.travel import CITY_DAYS, _find_in
    if _find_in(lowered, CITY_DAYS):
        return None
    place = the_city_of(topic) or the_country_of(topic)
    if not place or not going_there(place, topic):
        return None
    return lowered.strip().rstrip("?.!").strip() + " in " + place

POINTING_WORD = re.compile(r"\b(?:it|that|this|those|these|them|they|one|ones)\b", re.I)


def _the_ways_of_saying_it(stem_of, line, cands):
    for cand in cands:
        carried = " ".join(cand)
        yield stem_of + " " + carried, carried
    if POINTING_WORD.search(str(line or "")):
        for cand in cands:
            carried = " ".join(cand)
            yield " ".join(POINTING_WORD.sub(carried, str(line), count=1).lower().split()), carried


A_VERDICT = NEGATIVE | POSITIVE

A_BARE_MEASURE = re.compile(r"\b(?:how much|how many|how often|how long|how far|how soon)\b")
MEASURE_WORDS = frozenset("""cost costs costed price priced charge much many more less long often
far soon take takes taking time times need needs needed spend spent pay paid get got worth
there it that this""".split())


def _the_last_answer(memory):
    turns = (memory or {}).get("turns") or ()
    for one in reversed(turns):
        said = str((one or {}).get("bot") or "")
        if said:
            return said
    return ""


def _the_topics_on_the_chat(topic=None, memory=None):
    out = []
    for one in reversed((memory or {}).get("topics") or ()):
        said = str((one or {}).get("text") or "")
        if said and said not in out:
            out.append(said)
    said = str(topic or "")
    if said in out:
        out.remove(said)
    if said:
        out.insert(0, said)
    return out


def _the_thing_a_measure_is_of(line, topic=None, memory=None):
    if not _the_last_answer(memory):
        return None
    said = str(line or "")
    if not A_BARE_MEASURE.search(said.lower()):
        return None
    on_the_chat = set()
    for one in _the_topics_on_the_chat(topic, memory):
        on_the_chat.update(keywords(_the_topic_phrase(one) or one))
    for word in keywords(said):
        if word in MEASURE_WORDS or word in on_the_chat:
            continue
        return word
    return None


def _with_the_word_before(line, word, thing):
    said = str(line or "")
    for found in re.finditer(r"[A-Za-z']+", said):
        if stem(found.group(0).lower()) == thing:
            return (said[:found.start()] + word + " " + said[found.start():]).strip()
    return None


def _how_they_feel(word):
    word = str(word or "")
    if not word:
        return False
    if word in A_VERDICT:
        return True
    return any(form in A_VERDICT for form in forms(word))


def _keyed_to(keyed, word):
    word = str(word or "")
    if word in keyed or stem(word) in keyed:
        return True
    return any(word in forms(key) for key in keyed)


def _a_measure_of_the_topic(line, topic=None, memory=None):
    thing = _the_thing_a_measure_is_of(line, topic, memory)
    if thing is None:
        return None
    said = set(words(line))
    for one in _the_topics_on_the_chat(topic, memory):
        for word in keywords(_the_topic_phrase(one) or one):
            if word in said or word in MEASURE_WORDS:
                continue
            widened = _with_the_word_before(line, word, thing)
            if not widened:
                continue
            found = _entry(widened)
            if found is None:
                continue
            keyed = _key_words_of(found)
            if thing in keyed and _keyed_to(keyed, word):
                return widened
    return None


def carry_the_ask(line, topic, understood=None, memory=None):
    lowered = str(line or "").lower()
    if ABOUT_THE_CHAT.search(lowered):
        return None
    if any(phrase in lowered for phrase in PROCEED):
        return None
    elided = elided_ask(line)
    if not ASK_CUE.search(str(line or "").lower()) and not elided:
        return None
    carried = _carry_the_words(line, topic)
    if carried is not None:
        return carried
    doing = _the_ask_with_its_doing(line, topic)
    if doing is not None:
        return doing
    measured = _a_measure_of_the_topic(line, topic, memory)
    if measured is not None:
        return measured
    if elided and not _the_answer_covers_it(line, memory, understood):
        return _an_elided_ask_situated(line, topic, understood)
    return None



ADVICE_ONLY = re.compile(
    r"^(?:so|and|but|ok|okay|well|then|hmm|erm|um|oh|ah|right|alright|just|also)?[\s,]*"
    r"(?:should|shall|can|could|do|must)\s+i\s+"
    r"(?:stop|quit|give\s+up|carry\s+on|keep\s+going|keep\s+at\s+it|cut\s+back|hold\s+off"
    r"|rest|wait|go\s+on|start|start\s+again|bother)"
    r"(?:\s+(?:now|then|for\s+now|for\s+today|today|tonight|talking|chatting|going\s+on))?"
    r"[\s.!?]*$", re.I)


def _the_ask_with_its_doing(line, topic, last_id=None):
    if not ADVICE_ONLY.match(str(line or "")):
        return None
    whole = _entry(str(topic or ""))
    said = words(line)
    for word in keywords(str(topic or "")):
        if word in said:
            continue
        tried = str(line or "").strip() + " " + word
        found = _entry(tried)
        if found is None or found is whole:
            continue
        if last_id and getattr(found, "id", None) == last_id:
            continue
        return tried
    return None


def the_advice_ask_with_its_doing(understood, memory):
    if not isinstance(understood, dict) or not isinstance(memory, dict):
        return None
    line = str(understood.get("clean") or understood.get("text") or "").strip()
    if not line:
        return None
    record = memory.get("topic")
    if not isinstance(record, dict) or not record.get("text"):
        return None
    last = memory.get("last_answer")
    last_id = last.get("id") if isinstance(last, dict) else None
    doing = _the_ask_with_its_doing(line, str(record.get("text") or ""), last_id)
    if doing is None:
        return None
    reading = dict(understood)
    reading["clean"] = " ".join(doing.lower().split())
    reading["words"] = words(reading["clean"])
    return reading

def _the_answer_covers_it(line, memory, understood=None):
    if not isinstance(memory, dict) or not memory:
        return False
    from . import detail
    asked = [str(line or "")]
    typed = str(understood.get("text") or "") if isinstance(understood, dict) else ""
    if typed and typed not in asked:
        asked.append(typed)
    asked += [put_back for put_back in (_with_the_article(one) for one in asked) if put_back]
    return any(detail.answers_the_line(one, memory) for one in asked)


ABOUT_A_BARE_THING = re.compile(
    r"^(?P<open>(?:(?:ok|okay|so|and|but|also|well|yeah|right)\s+)*(?:what|how)\s+about)\s+"
    r"(?P<thing>(?!the\b|a\b|an\b|this\b|that\b|these\b|those\b|both\b|just\b)\w+)",
    re.I)


def _with_the_article(line):
    found = ABOUT_A_BARE_THING.match(str(line or ""))
    if found is None:
        return None
    said = str(line)
    return found.group("open") + " the " + said[found.start("thing"):]


A_FREQUENCY = re.compile(
    r"\b(?:all|most|half|the\s+whole|every|each|any|much\s+of)\s+(?:of\s+)?(?:the\s+)?"
    r"(?:time|times|day|days|week|weeks|month|months|while)\b"
    r"|\bat\s+the\s+moment\b|\bthese\s+days\b", re.I)


def _only_said_as_a_frequency(topic):
    text = str(topic or "")
    left = set(words(A_FREQUENCY.sub(" ", text)))
    return {word for word in words(text) if word not in left}


PROPERTY_ASK = re.compile(r"^\s*(?:and|so|ok|okay|also|but)?\s*[,:]?\s*(?:what|which|how)\b")


def _asks_a_property_and_nothing_else(text):
    low = str(text or "").strip().lower()
    if not PROPERTY_ASK.match(low):
        return False
    found = keywords(low)
    return bool(found) and all(word in MEASURE_WORDS for word in found)


def _carry_the_words(line, topic):
    lowered = str(line or "").lower()
    long_take = LONG_IT_TAKES.match(str(line or ""))
    if long_take:
        phrase = _the_topic_phrase(topic)
        tried = long_take.group("head") + " " + phrase + " take" if phrase else ""
        found = _entry(tried) if tried else None
        if found is not None and _a_length_of_the_job(found) and not keeps_away(tried, phrase, found):
            keyed = _key_words_of(found)
            carried = set(keywords(phrase))
            if len(carried) >= 2 and all(word in keyed or stem(word) in keyed or forms(word) & keyed
                                         for word in carried):
                return tried
    lowered = str(line or "").lower()
    if (the_city_of(topic) is not None or the_country_of(topic) is not None) \
            and STAY_ASK.search(lowered):
        stay = a_stay_with_the_place(line, topic)
        if stay is not None:
            return stay
        return None
    said = words(line)
    have = set(said)
    elsewhere = _the_trip_of_theirs(str(topic or "")) and not _a_sky_ask(line)
    lends_no_property = _asks_a_property_and_nothing_else(str(topic or ""))
    known = [word for word in keywords(str(topic or "")) if word not in have
             and not (lends_no_property and word in MEASURE_WORDS)
             and not (elsewhere and (word in MONTH_NAMES or word in SEASONS))]
    if not known:
        return None
    anchor = (_where_the_topic_lands(str(topic or "")) if names_nothing(line)
              else _entry(str(topic or "")))
    if anchor is not None:
        keyed = _key_words_of(anchor)
        extra = [word for word in known
                 if word in keyed or stem(word) in keyed or _said(word, keyed)]
        frequency = _only_said_as_a_frequency(topic)
        if extra and frequency and all(word in frequency for word in extra):
            extra = []
        if not extra:
            anchor = None
            extra = known
    else:
        extra = known
    if not extra:
        return None
    stem_of = line.strip().rstrip("?.!").strip()
    cands = [extra] + [[one, two] for one in extra for two in extra if one != two] \
        + [[one] for one in extra]
    text = item = borrowed = None
    for tried, carried in _the_ways_of_saying_it(stem_of, str(line or ""), cands):
        borrowed = carried
        found = _entry(tried)
        if found is None:
            continue
        keyed = _key_words_of(found)
        if not all(word in keyed or stem(word) in keyed or _said(word, keyed)
                   for word in carried.split()):
            continue
        text, item = tried, found
        break
    if item is None:
        return None
    keyed = _key_words_of(item)
    lean = [word for word in borrowed.split()
            if word in keyed or stem(word) in keyed or _said(word, keyed)]
    if 0 < len(lean) < len(borrowed.split()):
        tried = stem_of + " " + " ".join(lean)
        found = _entry(tried)
        if found is not None:
            text, item, borrowed = tried, found, " ".join(lean)
    if not _names_it(said, item) and not names_nothing(line) and item is not anchor:
        return None
    if anchor is not None and item is not anchor:
        if len(_key_words_of(item) & _key_words_of(anchor)) < 2:
            return None
    elif anchor is None and len(_key_words_of(item) & set(keywords(str(topic or "")))) < 2:
        if len(set(keywords(str(topic or "")))) > 1:
            return None
    if keeps_away(text, borrowed, item):
        return None
    return text


_elided_situated_cache = {}


def _an_elided_ask_situated(line, topic, understood=None):
    said = words(line)
    have = set(said)
    known = [word for word in keywords(str(topic or "")) if word not in have]
    if not known:
        return None
    if not isinstance(understood, dict) or not understood:
        return None
    from ..knowledge.lookup import about_the_topic
    stem_of = line.strip().rstrip("?.!").strip()
    situation = (stem_of, " ".join(known[:8]), understood.get("topic"))
    memo = _elided_situated_cache.get(situation)
    if memo is not None:
        return memo or None
    found = None
    for word in known[:8]:
        text = stem_of + " " + word
        item = _entry(text)
        if item is None or not _names_it(said, item):
            continue
        if not about_the_topic(item, understood):
            continue
        if keeps_away(text, word, item):
            continue
        found = text
        break
    if len(_elided_situated_cache) > 32:
        _elided_situated_cache.clear()
    _elided_situated_cache[situation] = found or ""
    return found
ABOUT_NAMED = re.compile(
    r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|alright)\W+)*"
    r"(?:what|how)\s+about\s+(?P<thing>[^.?!]+?)\s*$", re.I)
_ABOUT_TAIL_PRONOUN = re.compile(r"\s+(?:for|about|with)\s+(?:it|them|him|her|that|this)\s*$", re.I)
ABOUT_MOST_WORDS = 5
DEFINITE_OPEN = re.compile(r"^(?:the|my|our|your|his|her|its|their|this|that|these|those)\b", re.I)


ANSWER_OPENING = 90


def _the_same_answer_again(item, memory):
    reply = " ".join(str(getattr(item, "reply", "") or "").lower().split())
    if not reply:
        return False
    opening = reply[:ANSWER_OPENING]
    for turn in [one for one in (memory.get("turns") or []) if isinstance(one, dict)][-2:]:
        said = " ".join(str(turn.get("bot") or "").lower().split())
        if said and (opening in said or said[:ANSWER_OPENING] in reply):
            return True
    return False


def the_thing_the_subject_brings(understood, memory):
    if not isinstance(understood, dict):
        return None
    text = " ".join(str(understood.get("clean") or understood.get("text") or "").lower().split())
    raw = " ".join(str(understood.get("text") or understood.get("clean") or "").lower().split())
    lines = [text, raw]
    for turn in [one for one in (memory.get("turns") or []) if isinstance(one, dict)][-1:]:
        typed = " ".join(str(turn.get("user") or "").lower().split())
        if typed:
            lines.insert(0, typed)
    for said_as in lines:
        found = ABOUT_NAMED.match(said_as)
        if found:
            break
    else:
        return None
    thing = _ABOUT_TAIL_PRONOUN.sub("", found.group("thing").strip()).strip()
    if not thing or len(thing.split()) > ABOUT_MOST_WORDS:
        return None
    typed = _ABOUT_TAIL_PRONOUN.sub("", said_as[found.end():].strip())
    if DEFINITE_OPEN.match(thing) or DEFINITE_OPEN.match(typed):
        return None
    kind = typed or thing
    if not re.search(r"^(?:a|an|some)\b", kind, re.I):
        last = (kind.split() or [""])[-1]
        if not (last.endswith("s") and not last.endswith("ss") and len(last) > 3):
            return None
    thing_words = [word for word in words(thing)
                   if word not in STOPWORDS and word not in ASK_ONLY and len(word) > 2]
    if not thing_words:
        return None
    record = carried_topic(memory, text)
    if record is None:
        return None
    spoke_of = set()
    for turn in [one for one in (memory.get("turns") or []) if isinstance(one, dict)][-2:]:
        spoke_of.update(stem(word) for word in words(str(turn.get("bot") or "")))
    if any(stem(word) in spoke_of for word in thing_words):
        return None
    subject_words = [word for word in key_subject(str(record.get("text") or ""), memory)
                     if word not in thing_words]
    if not subject_words:
        return None
    for subject in subject_words:
        for candidate in (thing + " for " + subject, thing + " " + subject):
            item = _entry(candidate)
            if item is None:
                continue
            keyed = _key_words_of(item)
            named = any(word in keyed or stem(word) in keyed or _said(word, keyed)
                        for word in thing_words)
            about_the_subject = any(word in keyed or stem(word) in keyed or _said(word, keyed)
                                    for word in subject_words)
            if not (named and about_the_subject):
                continue
            anchor = _entry(str(record.get("text") or ""))
            if anchor is not None and item is not anchor:
                if _the_same_answer_again(item, memory):
                    continue
            return candidate
    return None


def follows_on(understood, text):
    if not isinstance(understood, dict):
        return False
    text = DUMMY_IT.sub(" ", str(text))
    points_back = any(word in REFERRING_WORDS for word in words(text))
    if not points_back:
        return False
    if understood.get("followup"):
        return True
    ref = understood.get("ref")
    return isinstance(ref, dict) and bool(ref.get("followup"))


def keeps_away(line, topic, item=None):
    if item is None:
        item = _entry(line)
    avoid = getattr(item, "avoid", ()) if item is not None else ()
    said = words(topic)
    return any(_kept_away_from(phrase, said) for phrase in avoid if isinstance(phrase, str))


def _kept_away_from(phrase, said):
    if not any(word in STOPWORDS for word in words(phrase)):
        return _said(phrase, said)
    wanted = [stem(word) for word in words(phrase)]
    if not wanted or not all(word in (stem(one) for one in said) for word in wanted):
        return False
    return _said(phrase, said)


def _names_it(found, item):
    content = set(found) - STOPWORDS
    asked_only = not (content - (ASK_PART | ASKS_FOR_ADVICE))
    for part in getattr(item, "key", ()):
        for phrase in (part if isinstance(part, tuple) else (part,)):
            if not isinstance(phrase, str):
                continue
            named = set(words(phrase)) - STOPWORDS
            if named and not named - (ASK_PART | ASKS_FOR_ADVICE) and not asked_only:
                continue
            if _said(phrase, found):
                return True
    return False


def _key_words_of(item):
    found = set()
    for part in getattr(item, "key", ()) if item is not None else ():
        for phrase in (part if isinstance(part, tuple) else (part,)):
            if isinstance(phrase, str):
                found.update(words(phrase))
    return found


def _names_it_as_written(found, item):
    for part in getattr(item, "key", ()):
        for phrase in (part if isinstance(part, tuple) else (part,)):
            if not isinstance(phrase, str) or not _said(phrase, found):
                continue
            have = {str(word).lower() for word in found}
            if any(word.lower() in have for word in words(phrase)):
                return True
    return False


def _asked_only(found, item):
    named = False
    for part in getattr(item, "key", ()):
        for phrase in (part if isinstance(part, tuple) else (part,)):
            if not isinstance(phrase, str) or not _said(phrase, found):
                continue
            if set(words(phrase)) <= (ASK_PART | PRICE_ASK):
                continue
            named = True
    return not named


def _a_sky_ask(line):
    return any(word in WEATHER_WORDS for word in words(line))


def _the_step_they_report(line):
    try:
        from . import already, repeat
        return bool(already.the_step_they_took(line) or repeat._tried(line))
    except Exception:
        return False


def widen(line, subject_words, topic_text):
    if a_placeholder_pronoun(line):
        return None
    if _the_step_they_report(line):
        return None
    topic_entry = _entry(topic_text)
    have = words(line)
    elsewhere = _the_trip_of_theirs(topic_text) and not _a_sky_ask(line)
    extra = [word for word in subject_words
             if word not in have and not (elsewhere and (word in MONTH_NAMES or word in SEASONS))]
    if not extra:
        return None
    text = line + " " + " ".join(extra)
    item = _entry(text)
    if item is None or item is topic_entry:
        return None
    if not _names_it(have, item):
        return None
    if _asked_only(have, item) and not _names_it_as_written(extra, item):
        return None
    if keeps_away(text, topic_text, item):
        return None
    return text


CONSTRAINT = re.compile(
    r"\b(?:\d+|one|two|three|four|five|ten|fifteen|twenty|thirty|forty|fifty|sixty|ninety"
    r"|an hour|half an hour)\b[^.!?]{0,14}?\b(?:minutes?|mins?|hours?|hrs?)\b"
    r"|\b\d+(?:\.\d+)?\s?(?:kg|g|lb|lbs|oz|pints?|litres?|l|ml)\b"
    r"|\bin a (?:hurry|rush)\b|\bshort (?:of|on) time\b|\bno time\b"
    r"|\bnot (?:much|long) time\b", re.I)
CONSTRAINT_FILLER = frozenset("""a an the and but so though then just only really very about
at for in on of to be been is are was were have has had got get ive i im it its me my
that this there here now today tonight morning afternoon evening lunchtime midday night
week weeknight weekday left spare weve we you he she they one some more like most
think guess say said times""".split())


def adds_only_a_constraint(line):
    text = str(line or "")
    match = CONSTRAINT.search(text)
    if match is None:
        return None
    rest = words(text[:match.start()] + " " + text[match.end():])
    if [word for word in rest if word not in CONSTRAINT_FILLER and not word.isdigit()]:
        return None
    return match.group(0)


def _constrains_the_ask(line, topic_text):
    if adds_only_a_constraint(line) is None:
        return None
    asked = str(topic_text or "").strip()
    if not asked:
        return None
    mine = _entry(asked)
    text = asked + " " + str(line).strip()
    item = _entry(text)
    if item is None or (mine is not None and item is not mine):
        return None
    return text


SENTENCE = re.compile(r"(?<=[.!?])\s+")
JOINED_ON = re.compile(r"^(?:and|then|so|but|also|now|next|plus|instead|otherwise)"
                       r"(?:\s*,\s*|\s+)", re.I)
NUMBER = re.compile(r"\d")
TIME = re.compile(r"\d[^.]{0,15}?\b(?:min\w*|hour\w*|hrs?)\b", re.I)
AMOUNT = re.compile(r"\b\d+(?:\.\d+)?\s?(?:kg|g|lb|oz|pints?|litres?|l|ml|inches|inch|cm|mm)\b",
                    re.I)
AMOUNT_ANSWER = re.compile(
    r"(?:[\u00a3$\u20ac]\s?\d+(?:[\d,.]*)?(?:\s*(?:-|to|and|\u2013)\s*[\u00a3$\u20ac]?\s?"
    r"\d+(?:[\d,.]*)?)?"
    r"|\b\d+(?:\.\d+)?(?:\s*(?:-|to|and|\u2013)\s*\d+(?:\.\d+)?)?\s*"
    r"(?:mg|mcg|\u00b5g|g|kg|ml|l|litres?|liters?|tbsp|tsp|tablespoons?|teaspoons?|cups?|"
    r"parts?|people|slices?|tins?|oz|lbs?|pounds?|tablets?|capsules?|drops?|puffs?|sprays?|"
    r"units?|iu|kcal|calories|pouches?|sachets?|scoops?)\b)", re.I)
RATE = re.compile(r"\bper (?:kilo|kg|500g|pound|lb|person|head|each)\b", re.I)
RATE_BY_WEIGHT = re.compile(r"\b(\d+(?:\.\d+)?)\s*(?:minutes?|mins?)\s+per\s+"
                            r"(\d+(?:\.\d+)?)\s*(kg|g|lb|lbs|pound|pounds|oz|ounce|ounces)\b", re.I)
OWN_SIZE = re.compile(r"\b(?:so an?\s+|for\s+)(\d+(?:\.\d+)?)\s*"
                      r"(kg|g|lb|lbs|pound|pounds|oz|ounce|ounces)\b", re.I)
PLUS_MINUTES = re.compile(r"\bplus\s+(\d+)\s*(?:minutes?|mins?)\b", re.I)
WEIGHT_IN_GRAMS = {"g": 1.0, "kg": 1000.0, "lb": 453.59237, "lbs": 453.59237,
                   "pound": 453.59237, "pounds": 453.59237, "oz": 28.3495,
                   "ounce": 28.3495, "ounces": 28.3495}
TIME_SPAN = re.compile(r"\b\d+(?:\.\d+)?(?:\s*(?:-|to|and)\s*\d+(?:\.\d+)?)?\s*"
                       r"(?:minutes?|mins?|hours?|hrs?)(?:\s+(?:and\s+)?\d+(?:\s*(?:-|to)\s*\d+)?"
                       r"\s*(?:minutes?|mins?)?)?", re.I)
DURATION = re.compile(
    r"\b(?:\d+(?:\s*(?:-|–|to)\s*\d+)?|half an|an?)\s*"
    r"(?:minutes?|mins?|hours?|hrs?|seconds?|days?|weeks?)\b"
    r"|\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|a few|a couple of|"
    r"several|couple of)"
    r"(?:\s*(?:-|–|to)\s*(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten))?\s*"
    r"(?:days?|weeks?)\b", re.I)
SPAN_ADJECTIVE = re.compile(
    r"\b\d+\s*[-\u2013]\s*(?:minute|min|hour|hr|day|week|month|year)s?\b", re.I)
LENGTH_ASK = re.compile(
    r"\bhow long\b|\bhow much time\b|\bhow many (?:minutes?|mins?|hours?|hrs?|days?|weeks?)\b"
    r"|\btime\b|\bduration\b", re.I)
THRESHOLD_SPAN = re.compile(
    r"\b(?:more than|longer than|fewer than|less than|at least|at most|over|under|beyond|up to)\s+"
    r"(?:\d+|a|an|one|two|three|four|five|six|seven|eight|nine|ten|a few|several|couple of)?\s*"
    r"(?:minutes?|mins?|hours?|hrs?|days?|weeks?|months?|fortnights?|years?)\b", re.I)
CLAUSE = re.compile(r"\s*(?:,|;|:|\u2014| - )\s*"
                    r"|\s+or\s+(?!\d|\b(?:a|an|one|two|three|four|five|six|seven|eight|nine|"
                    r"ten|eleven|twelve|fifteen|twenty|thirty|forty|fifty|hundred|half|couple|"
                    r"several|few)\b)")
ASIDE = re.compile(r"\([^()]*\)")
SHIELD = "\x00"


def _clauses_of(sentence):
    shielded = ASIDE.sub(lambda found: found.group(0).replace(",", SHIELD), str(sentence or ""))
    return [piece.replace(SHIELD, ",") for piece in CLAUSE.split(shielded)]


WARNING_SPAN = re.compile(
    r"\b(?:still there|still not|still the same|not better|no better|not gone|not settled|"
    r"not cleared|gets? worse|getting worse|keeps? (?:on|coming)|comes? back|bleeds?"
    r"|is a reason to|ring (?:the )?(?:surgery|gp|doctor|nhs|111|999)"
    r"|(?:ring|call|see|contact|speak to) (?:a |the |your )?(?:gp|doctor|nurse|pharmacist|"
    r"surgery|111|999|a&e|hospital))\b",
    re.I)
FREQUENCY = re.compile(
    r"\b(?:once|twice)\s*(?:a|per|every)\s*(?:day|week|month|year|fortnight|weekend|morning|"
    r"evening|night)\b|"
    r"\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|a couple of|a few)\s*times?"
    r"\s*(?:a|per|every)\s*(?:day|week|month|year|fortnight|weekend|morning|evening|night)\b|"
    r"\bevery\s+(?:other\s+)?(?:day|week|month|morning|evening|night|year)\b|"
    r"\bevery\s+(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|twelve|couple of|"
    r"few|several|a couple of|a few)(?:\s*(?:-|to|or)\s*(?:\d+|one|two|three|four|five|six|"
    r"seven|eight|nine|ten|twelve))?\s+(?:days?|weeks?|months?|years?|nights?|mornings?|"
    r"evenings?)\b|"
    r"\b(?:daily|weekly|nightly|monthly)\b",
    re.I)

NOT_A_QUANTITY = r"(?!\s+(?:take|last|need|cook|roast|bake|boil|keep|stay|be done|finish|work out))"
HYPOTHETICAL = re.compile(
    r"\b(?:what if|what happens if|in case|if it (?:goes|doesn't|does not|fails?|sinks?|burns?)|"
    r"supposing|suppose|what would|should i risk|(?:would|will) it" + NOT_A_QUANTITY + r")\b", re.I)

ANSWER_KEPT = 4


def remember_answer(memory, reply, keys):
    if not isinstance(reply, str) or not reply.strip():
        return
    record = {
        "text": reply,
        "keys": sorted(str(key) for key in (keys or ())),
    }
    memory["entry_answer"] = record
    kept = memory.get("entry_answers")
    if not isinstance(kept, list):
        kept = []
    kept.append(record)
    memory["entry_answers"] = kept[-ANSWER_KEPT:]


def entry_answer(memory, topic_text):
    turns = memory.get("turns")
    if not isinstance(turns, list):
        return None
    kept = memory.get("entry_answers")
    if not isinstance(kept, list) or not kept:
        kept = [memory.get("entry_answer")]
    mine = {form for word in keywords(topic_text) for form in (word, stem(word))}
    best, best_score = None, 0
    for record in kept:
        if not isinstance(record, dict):
            continue
        text = str(record.get("text") or "").strip()
        if not text:
            continue
        opening = " ".join(text.lower().split()[:8])
        if not any(isinstance(turn, dict)
                   and " ".join(str(turn.get("bot") or "").lower().split()).startswith(opening)
                   for turn in turns[-ANSWER_KEPT:]):
            continue
        keys = set(record.get("keys") or ())
        if not keys:
            continue
        forms = {form for key in keys for form in (key, stem(key))}
        score = len(mine & forms - STOPWORDS)
        if score and score >= best_score:
            best, best_score = text, score
    return best


ACKED_IN_BETWEEN = 2


def answer_in_hand(memory):
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    if not turns:
        return None
    index = len(turns) - 1
    stepped = 0
    while index > 0 and stepped < ACKED_IN_BETWEEN and is_ack(turns[index].get("user")):
        index -= 1
        stepped += 1
    return turns[index]


def newest_answer(memory):
    kept = memory.get("entry_answers")
    if not isinstance(kept, list) or not kept:
        kept = [memory.get("entry_answer")]
    turns = memory.get("turns")
    if not isinstance(turns, list):
        return None
    for record in reversed(kept):
        if not isinstance(record, dict):
            continue
        text = str(record.get("text") or "").strip()
        if not text:
            continue
        opening = " ".join(text.lower().split()[:8])
        if any(isinstance(turn, dict)
               and " ".join(str(turn.get("bot") or "").lower().split()).startswith(opening)
               for turn in turns[-ANSWER_KEPT:]):
            return text
    return None


REPEAT = (
    "Same as before: {reply}",
    "As I said: {reply}",
    "Same again: {reply}",
)

REPEAT_LEADS = (("same", "as", "before"), ("as", "i", "said"), ("same", "again"))


def _carries(said, mine):
    if not said:
        return False
    if said == mine:
        return True
    for lead in REPEAT_LEADS:
        if said == " ".join(lead) + " " + mine:
            return True
    return False


ACK = re.compile(r"^(?:got it|noted|right|ok|okay|fair enough|thanks|cheers|sure|cool"
                  r"|sounds good|no problem|not a problem|any time|you're welcome"
                  r"|understood|makes sense|good to hear|lovely to hear)\b", re.I)
WARM_ACK = re.compile(r"\b(?:glad|pleased|happy|delighted)\b", re.I)
ACK_COURTESY = re.compile(
    r"\b(?:say the word|let me know|shout if|just ask|any ?time|good luck"
    r"|hope (?:that|it|this) (?:helps|is useful|lands))\b", re.I)


A_CLOSE = re.compile(r"\b(?:good luck|best of luck|all the best|enjoy (?:it|the rest)|have fun"
                     r"|hope (?:it|that) goes well)\b", re.I)
CLOSE_FILLER = frozenset("alright ok okay right well then great lovely nice and so with it that "
                         "your the rest of day time too now very much you i me a an".split())


def _only_a_close(text):
    found = A_CLOSE.search(text)
    if not found:
        return False
    rest = (text[:found.start()] + " " + text[found.end():]).split()
    for word in rest:
        word = word.strip(".,!?-\u2014\u2013\"'()").lower()
        if word and word not in CLOSE_FILLER:
            return False
    return True


SHORT_TURN = 12


def only_acknowledges(said):
    text = str(said or "").strip()
    if not text or len(text.split()) > SHORT_TURN:
        return False
    if ACK.match(text):
        return True
    if _only_a_close(text):
        return True
    return bool(WARM_ACK.search(text)
                and (ACK_COURTESY.search(text) or "," not in text))

LOOK_BACK = 3


def _hands_the_subject_back(said, memory):
    kept = memory.get("hand_backs") if isinstance(memory, dict) else None
    return isinstance(kept, list) and said in kept


FIGURE = re.compile(r"\b\d+(?:[.,]\d+)?\b")

POINTS_AT_THE_ANSWER = frozenset("""
back instead anyway though
""".split())


def _the_opening_of(reply):
    body = str(reply or "").strip()
    parts = quoted.sentences(body, SENTENCE)
    if len(parts) < 2:
        return body
    if len(parts[0]) >= 60:
        kept = parts[:1]
    else:
        kept = parts[:2]
    return quoted.closed(" ".join(part.strip() for part in kept), parts[len(kept):], body)


def said_again(reply, memory, line=None):
    from . import again as _frames
    if _frames.carries_a_lead_in(reply):
        return None
    mine = " ".join(words(reply))
    if line is not None and pairing(line):
        return None
    if line is not None:
        from . import returned

        if returned.says_it_happened_again(line):
            return None
    if line is not None and (
            [word for word in keywords(line)
             if word not in ASK_ONLY and word not in POINTS_AT_THE_ANSWER]
            or FIGURE.search(str(line))):
        return None
    turns = memory.get("turns")
    if not mine or not isinstance(turns, list):
        return None
    times = 0
    seen = 0
    for turn in reversed(turns):
        if not isinstance(turn, dict):
            break
        if seen >= LOOK_BACK:
            break
        seen += 1
        said = words(turn.get("bot") or "")
        if _carries(" ".join(said), mine) or mine in " ".join(said):
            times += 1
            continue
        if _hands_the_subject_back(" ".join(said), memory) or only_acknowledges(turn.get("bot")):
            continue
        break
    if not times:
        return None
    short = _the_opening_of(reply)
    if short and " ".join(words(short)) != mine:
        reply = short
    return REPEAT[min(times, len(REPEAT)) - 1].format(reply=reply)
def _said_later_than(turn, record):
    mine = turn.get("turn") if isinstance(turn, dict) else None
    theirs = record.get("turn") if isinstance(record, dict) else None
    if not isinstance(mine, int):
        return False
    if not isinstance(theirs, int):
        return True
    return mine > theirs


def _the_turn_we_lean_on(understood, memory):
    lean = understood.get("leans_on") if isinstance(understood, dict) else None
    text = str(lean.get("text") or "") if isinstance(lean, dict) else ""
    wanted = " ".join(words(text))
    if not wanted:
        return None
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return None
    for back, turn in enumerate(reversed(turns[-8:])):
        if not isinstance(turn, dict):
            continue
        said = str(turn.get("user") or "")
        if " ".join(words(said)) == wanted:
            return {"turn": len(turns) - 1 - back, "text": said, "words": words(said)}
    return None


def _the_turn_that_answered(answer, memory, keep=6):
    wanted = words(answer)[:12]
    for turn in reversed((memory.get("turns") or [])[-keep:]):
        if not isinstance(turn, dict):
            continue
        if words(str(turn.get("bot") or ""))[:12] == wanted:
            return turn
    return None


_ASKING_VERBS = frozenset(_VERB_WORDS) | frozenset(_ACTION)


def _answer_about(line, memory, keep=6):
    asking = bool(_FRAME_ASK.search(line.lower()))
    wanted = frozenset(stem(word) for word in keywords(line)
                       if word not in ASK_ONLY
                       and not (asking and stem(word) in _ASKING_VERBS))
    if not wanted:
        return None
    turns = [turn for turn in (memory.get("turns") or [])[-keep:] if isinstance(turn, dict)]
    if len(turns) < 2:
        return None
    last = str(turns[-1].get("bot") or "")
    last_score = len(wanted & frozenset(stem(w) for w in keywords(last)))
    best, best_score = None, last_score
    for turn in turns[:-1]:
        if turn.get("module") != "answers":
            continue
        said = str(turn.get("bot") or "")
        score = len(wanted & frozenset(stem(w) for w in keywords(said)))
        if score > best_score:
            best, best_score = said, score
    return best


def answer_about(line, memory):
    return _answer_about(line, memory)


def _the_trip_of_theirs(text):
    from . import facts
    found = facts.extract(text) or {}
    if not found.get("plan"):
        return set()
    return {str(place).strip().lower() for place in found.get("places") or [] if str(place).strip()}


def the_place_they_are_on(memory):
    turns = [turn for turn in (memory.get("turns") or [])
             if isinstance(turn, dict) and turn.get("user")]
    corrected = isinstance(memory, dict) and bool(memory.get("correction"))
    if not corrected:
        for turn in reversed(turns[-2:]):
            here = _the_trip_of_theirs(str(turn.get("user") or ""))
            if here:
                return here
    plan = (memory.get("user") or {}).get("plan") if isinstance(memory, dict) else None
    if isinstance(plan, str) and plan.strip():
        here = _the_trip_of_theirs("we are going to " + plan.strip())
        if here:
            return here
    return set()


def about_a_place_they_left_behind(answer, memory):
    here = the_place_they_are_on(memory)
    if not here:
        return False
    told = {str(place).strip().lower()
            for place in ((memory.get("user") or {}).get("places") or []) if str(place).strip()}
    left = told - here
    if not left:
        return False
    return bool(left & set(words(str(answer or ""))))


ASKS_A_FREQUENCY = re.compile(r"\bhow (?:often|regularly|frequently)\b|\bhow many times\b", re.I)


def same_as_before(understood, memory):
    if not isinstance(understood, dict):
        return None
    line = understood.get("clean") or understood.get("text") or ""
    if pairing(line):
        return None
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns or not isinstance(turns[-1], dict):
        return None
    last = turns[-1]
    drawn = answer_in_hand(memory) or last
    if understood.get("kind") != "question":
        return None
    proceed = any(phrase in line.lower() for phrase in PROCEED)
    if not (leans_on_topic(understood, memory) or asks_only(understood)):
        return None
    record = carried_topic(memory, line)
    if left_for_a_blank(memory, line):
        return None
    asked = str((record or {}).get("text") or "")
    earlier = _answer_about(line, memory)
    if earlier is not None and not [word for word in keywords(line) if word not in ASK_ONLY]:
        on_the_table = _entry(asked)
        answered_by = _the_turn_that_answered(earlier, memory)
        its_subject = _entry(str((answered_by or {}).get("user") or ""))
        if on_the_table is not None and its_subject is not on_the_table:
            earlier = None
    measured = set(understood.get("asks") or ()) & MEASURED
    fresh = [word for word in keywords(line) if word not in ASK_ONLY]
    if earlier is None and measured and fresh \
            and not set(key_subject(line)) & set(key_subject(asked)):
        mine, theirs = _entry(line), _entry(asked)
        if mine is not None and theirs is not None and mine is not theirs:
            return None
    if (not asks_only(understood) and _repeats_the_question(line, asked)) \
            or HYPOTHETICAL.search(str(line)):
        return None
    whole = entry_answer(memory, asked)
    if not any(word in keywords(asked) for word in keywords(line)):
        whole = newest_answer(memory) or whole
    if whole and asks_only(understood):
        moved = _the_thing_the_chat_moved_to(whole, line, memory)
        if moved is not None:
            from .narrow import narrow as _the_part
            answer = str(getattr(moved, "reply", "") or "")
            part = _the_part(answer, line)
            if part:
                bare = part.strip(" .").lower()
                for sentence in (one.strip() for one in SENTENCE.split(answer)):
                    if sentence and bare and bare in sentence.lower():
                        return sentence
                return part
            return None
    if drawn.get("module") != "answers" and whole is None:
        return None
    answer = whole or str(drawn.get("bot") or "")
    if about_a_place_they_left_behind(answer, memory):
        return None
    sized = _worked_out_for_this_line(understood, line, answer)
    if not (leans_on_topic(understood, memory) or asks_only(understood) or sized):
        return None
    worked = sized_reply(answer, line, memory)
    if worked:
        return worked
    if earlier and earlier != answer:
        answer = whole = earlier
        from .narrow import narrow
        part = narrow(answer, line)
        if part:
            return part
    sentences = quoted.sentences(answer, SENTENCE)
    if proceed:
        if _opening_instruction(sentences[0], True):
            return None
        doing = _doing_part(sentences, memory)
        if doing and not _says_it_again(doing, sentences[0]):
            return doing
        return None
    if len(sentences) < 2 and whole is None:
        return None
    from .narrow import part_in_the_unit
    part = part_in_the_unit(answer, line)
    if part and " ".join(words(part)) != " ".join(words(str(last.get("bot") or ""))):
        return said_again(part, memory, line=line) or part
    if ASKS_A_FREQUENCY.search(line.lower()):
        from .narrow import narrow
        part = narrow(answer, line)
        if part and words(part) != words(answer):
            return part
    chosen = _pick_sentence(line, understood, answer, memory)
    if chosen:
        opening = quoted.sentences(str(answer or ""), SENTENCE)
        if opening and words(opening[0]) == words(chosen):
            return said_again(chosen, memory, line=line) or chosen
        return chosen
    return _earlier_subject_sentence(line, understood, memory, record)


ADVICE_ASK = re.compile(
    r"\b(?:what|anything|something|is there anything) (?:can|could|should|would|do|shall) "
    r"(?:i|we|you) (?:do|try|use)\b|\bwhat(?:'s| is) the (?:best )?(?:thing|way) to do\b|"
    r"\bwhat do i do\b|"
    r"\bhow (?:do|can|should|could|would|might) (?:i|we) "
    r"(?:fix|sort|stop|help|ease|improve|avoid|prevent|deal with|get rid of)\b|"
    r"\bwhat (?:would |could |might |will |does |do )?(?:help|helps|helped|works|worked)\b|"
    r"\bwhat (?:should|can|could|would) (?:i|we) (?:put|set|have) in place\b", re.I)
ADVICE_NAMES_A_THING = re.compile(
    r"\b(?:do|try|use)\s+(?:with|for|in|on)\s+"
    r"(?!(?:it|that|this|them|these|those)\b)", re.I)
PAIRING = re.compile(r"\b(?:have|eat|drink|serve|pair|put|go(?:es)?)\s+(?:with|alongside)\s+"
                     r"(?:it|that|this|these|those|them)\b", re.I)
PAIRING_OWN = re.compile(r"\b(?:sauce|gravy|dressing|dip|jam|relish|chutney|salsa|mayo|"
                         r"mayonnaise|mustard|ketchup|wine|beer)\b", re.I)
def pairing(text):
    return bool(PAIRING.search(text or "")) and not PAIRING_OWN.search(text or "")
IMPERATIVE = frozenset("""
add apply avoid ask bake bleed book buy call change check chill choose clean clear close cover cut
deal don't do drink dry ease eat fill fit freeze get give go have heat hold ice keep kill leave let
lie look lower make mix offer open peel phone pick plan prune put raise remove replace rest rid ring
rinse run say see set sit soak sort speak start stay stop swap take talk tell text think throw
tighten top try turn use wait walk wash watch wear weed wipe write
""".split())
SENDS_YOU_ON = frozenset("""see call phone ring book ask get""".split())


WHEN = frozenset("""once twice three four five six seven two a an every each daily nightly morning
afternoon evening night day week month year hour minute second time times""".split())


def _doing_word(text):
    words = str(text or "").split()
    for index, word in enumerate(words):
        core = word.strip(",;:-\u2014\u2013").lower()
        if core in WHEN and index < 5:
            continue
        return core
    return ""


def _opening_instruction(sentence, allow_pointer):
    first = _doing_word(sentence)
    if first not in IMPERATIVE:
        return False
    return allow_pointer or first not in SENDS_YOU_ON


RED_FLAG = re.compile(
    r"^(?:get (?:it|that|one|them|him|her) (?:looked at|checked|seen)"
    r"|have (?:it|that|one) (?:looked at|checked)"
    r"|ring (?:111|999|911|nhs 24)|call (?:111|999|911)"
    r"|go (?:to|into) (?:a&e|a and e|the hospital|hospital|the emergency department)"
    r"|see (?:a|your|the) (?:gp|doctor|nurse|pharmacist|midwife)"
    r"|speak to (?:a|your|the) (?:gp|doctor)"
    r"|if (?:it|that|they) (?:is |are )?(?:still|gets? worse|does not settle|doesnt settle"
    r"|has not settled|had not settled|keeps? (?:on|coming)))", re.I)


ASKS_THEM_BACK = re.compile(
    r"\b(?:tell me|let me know|say (?:which|what|how|if|when|where|who)|send me|give me|pick one)\b"
    r"|\b(?:and|then)\s+i(?:'ll| will)\b"
    r"|\?\s*$", re.I)


def _doing_part(sentences, memory):
    for allow_pointer in (False, True):
        for sentence in sentences:
            if RED_FLAG.match(sentence):
                continue
            head, sep, tail = sentence.partition(":")
            if sep and tail.strip() and _opening_instruction(tail, allow_pointer):
                said = tail.strip()
                said = said[0].upper() + said[1:]
                if not said.endswith((".", "!", "?")):
                    said += "."
                if RED_FLAG.match(said) or ASKS_THEM_BACK.search(said):
                    continue
                if not already_said(memory, said):
                    return said
            if _opening_instruction(sentence, allow_pointer) \
                    and not ASKS_THEM_BACK.search(sentence):
                if not already_said(memory, sentence):
                    return sentence
    return None


def _says_it_again(part, sentence):
    words = re.findall(r"[a-z']+", str(part or "").lower())
    said = re.findall(r"[a-z']+", str(sentence or "").lower())
    if not words or not said:
        return False
    head = words[:6]
    for index in range(len(said) - len(head) + 1):
        if said[index:index + len(head)] == head:
            return True
    return sum(1 for word in words if word in said) >= 0.8 * len(words)


A_CEILING_ASK = re.compile(
    r"\b(?:too much|too many|max(?:imum)?|limit|how much can i (?:take|have|drink|eat)"
    r"|how many can i (?:take|have|drink|eat)|how much is safe|how many is safe)\b", re.I)
A_CEILING_WORD = re.compile(
    r"\b(?:at most|no more than|max(?:imum)?|limit|up to|not (?:more|over)|safe|ceiling)\b",
    re.I)


_A_RATE = re.compile(
    r"\b(?:a|an|per|each|every)\s+(day|week|month|year)\b"
    r"|\b(daily|weekly|monthly|yearly|annually)\b", re.I)


def _the_rates_in(text):
    out = set()
    for found in _A_RATE.finditer(str(text or "")):
        for word in found.groups():
            if word:
                out.add(word.lower().rstrip("s"))
    for word, one in (("daily", "day"), ("weekly", "week"), ("monthly", "month"),
                      ("yearly", "year"), ("annually", "year")):
        if re.search(r"\b" + word + r"\b", str(text or ""), re.I):
            out.add(one)
    return out


def _a_rate_that_fits(line, sentence):
    asked = _the_rates_in(line)
    if not asked:
        return True
    given = _the_rates_in(sentence)
    return bool(asked & given) or not given


def _a_comma_that_ends_a_clause(sentence, start):
    at = sentence.find(",", start)
    while at >= 0:
        before = sentence[at - 1] if at else ""
        after = sentence[at + 1] if at + 1 < len(sentence) else ""
        if not (before.isdigit() and after.isdigit()):
            return at
        at = sentence.find(",", at + 1)
    return -1


def _pick_amount(sentences, memory, line=""):
    screen = " ".join(words(str((memory.get("turns") or [{}])[-1].get("bot") or ""))) \
        if isinstance(memory, dict) else ""
    wants_limit = bool(A_CEILING_ASK.search(str(line or "")))
    if wants_limit:
        for sentence in sentences:
            if AMOUNT_ANSWER.search(sentence) and A_CEILING_WORD.search(sentence):
                return sentence
        for sentence in sentences:
            if AMOUNT_ANSWER.search(sentence):
                return sentence
    named = [word for word in keywords(line) if len(word) > 2 and word not in ASK_ONLY]
    for sentence in sentences:
        if (AMOUNT_ANSWER.search(sentence) and " ".join(words(sentence)) not in screen
                and _a_rate_that_fits(line, sentence)):
            if named and not any(word in keywords(sentence) for word in named):
                continue
            if not _the_rates_in(line) and _the_rates_in(sentence) and re.search(
                    r"\bone\b", str(line or ""), re.I):
                continue
            return sentence
    for sentence in sentences:
        found = AMOUNT_ANSWER.search(sentence)
        if not found or not _a_rate_that_fits(line, sentence):
            continue
        if named and not any(word in keywords(sentence) for word in named):
            continue
        if not _the_rates_in(line) and _the_rates_in(sentence) and re.search(
                r"\bone\b", str(line or ""), re.I):
            continue
        before = max(sentence.rfind(":", 0, found.start()),
                     sentence.rfind(";", 0, found.start()))
        after = _a_comma_that_ends_a_clause(sentence, found.end())
        start = before + 1 if before >= 0 else 0
        end = after if after >= 0 else len(sentence)
        part = sentence[start:end].strip(" .,;:")
        if part and len(part.split()) >= 2:
            return part[:1].upper() + part[1:] + "."
        return sentence
    return None


def _pick_sentence(line, understood, answer, memory, strict=False):
    return said_on_its_own(_the_sentence_it_answers(line, understood, answer, memory, strict))


def said_on_its_own(sentence):
    if not isinstance(sentence, str):
        return sentence
    said = sentence.strip()
    if not said:
        return None
    joined = JOINED_ON.match(said)
    if joined:
        said = said[joined.end():]
        if said:
            said = said[:1].upper() + said[1:]
    return said or None


def _the_sentence_it_answers(line, understood, answer, memory, strict=False):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    last = turns[-1] if isinstance(turns, list) and turns and isinstance(turns[-1], dict) else {}
    sentences = quoted.sentences(answer, SENTENCE)
    if not sentences:
        return None
    wanted = [stem(word) for word in keywords(line)]
    asks = set(understood.get("asks") or {})
    if "how_long" in asks:
        part = _pick_duration(sentences, wanted, memory, line)
        if part:
            return part
    if re.search(r"\bhow much\b", line, re.I):
        part = _pick_amount(sentences, memory, line)
        if part:
            return part
    if ADVICE_ASK.search(line) and ADVICE_NAMES_A_THING.search(line) is None \
            and not _names_something_new(line, answer):
        doing = _doing_part(sentences, memory)
        if doing:
            return doing
    best, best_score = 0, 0
    for index, sentence in enumerate(sentences):
        said = [stem(word) for word in keywords(sentence)]
        score = sum(1 for word in wanted if word in said)
        if score > best_score:
            best, best_score = index, score
    if best_score:
        sentence = sentences[best]
        if not already_said(memory, sentence):
            return sentence
    if strict:
        return None
    if asks & {"steps", "how"}:
        first = sentences[0]
        if _names_something_new(line, answer):
            return None
        if ADVICE_ASK.search(line) and not ADVICE_NAMES_A_THING.search(line):
            doing = _doing_part(sentences, memory)
            if doing:
                return doing
        return None if already_said(memory, first) else first
    if "how_long" in asks:
        amount = AMOUNT.search(line)
        worked = _sized_reply(answer, line, memory)
        if amount and worked:
            return worked
        for sentence in sentences[1:]:
            if not (TIME.search(sentence) and not already_said(memory, sentence)):
                continue
            if amount and amount.group(0).replace(" ", "") not in re.sub(r"\s+", "", sentence):
                if RATE.search(answer) and not already_said(memory, answer, turns_back=1):
                    return answer
                continue
            return sentence
        if sentences and TIME.search(sentences[0]) and not already_said(memory, sentences[0]):
            span = _time_of(sentences[0])
            if span:
                return span[0].upper() + span[1:] + "."
        part = _pick_duration(sentences, wanted, memory, line)
        if part:
            return part
    if "how_often" in asks:
        for sentence in sentences:
            found = FREQUENCY.match(sentence)
            if not found or already_said(memory, sentence):
                continue
            return _phrase(found.group(0))
    return None


AFTERWARDS = re.compile(r"\b(?:then|rest|cool|stand|leave|sit|wait|soak|drain|cold water|"
                        r"ice|fridge|freezer|oven off|heat off)\b", re.I)
TOTAL = re.compile(r"\b(?:so|takes|total|in all|altogether)\b", re.I)


def _time_of(sentence):
    clauses = [clause for clause in (CLAUSE.split(str(sentence or "")) or [str(sentence or "")])
               if not _not_a_length(clause)]
    first = ""
    for clause in clauses:
        spans = list(TIME_SPAN.finditer(clause))
        if not spans:
            continue
        span = spans[-1].group(0).strip(" ,;")
        if TOTAL.search(clause):
            return span
        if not first and not AFTERWARDS.search(clause):
            first = span
    if first:
        return first
    spans = [match for clause in clauses for match in TIME_SPAN.finditer(clause)]
    return spans[-1].group(0).strip(" ,;") if spans else ""


OPTION = re.compile(r"^\s*(\d+(?:\.\d+)?(?:\s*(?:-|to|and)\s*\d+(?:\.\d+)?)?)"
                    r"\s*(minutes?|mins?|hours?|hrs?|seconds?|secs?)?\s+for\b", re.I)


def _option_range(sentence):
    found = []
    for part in CLAUSE.split(str(sentence or "")):
        match = OPTION.match(part)
        if match:
            found.append(match)
    if len(found) < 2:
        return ""
    unit = next((match.group(2) for match in found if match.group(2)), "")
    if not unit:
        return ""
    first = found[0].group(1).split()[0]
    last = found[-1].group(1).split()[-1]
    if first == last:
        return ""
    try:
        if float(re.sub(r"[^0-9.]", "", last)) <= float(re.sub(r"[^0-9.]", "", first)):
            return ""
    except ValueError:
        return ""
    return f"{first} to {last} {unit.lower()}"


QUOTE_MARK = re.compile(r"(?<![A-Za-z])'|'(?![A-Za-z])|\"")


def _quoted(part):
    text = str(part or "")
    return len(QUOTE_MARK.findall(text)) % 2


OPTION_ANY = re.compile(
    r"(\d+(?:\.\d+)?(?:\s*(?:-|to|and)\s*\d+(?:\.\d+)?)?)"
    r"\s*(minutes?|mins?|hours?|hrs?|seconds?|secs?)?\s+for\b", re.I)


def _the_option_for_the_topic(sentence, line, memory):
    text = str(sentence or "")
    found = list(OPTION_ANY.finditer(text))
    if len(found) < 2:
        return None
    topic = str((carried_topic(memory, line) or {}).get("text") or "")
    subject = set(keywords(topic))
    if not subject:
        return None
    hits, unit = [], ""
    for index, found_one in enumerate(found):
        end = found[index + 1].start() if index + 1 < len(found) else len(text)
        piece = text[found_one.start():end]
        for _ in range(2):
            piece = re.sub(r"[\s,;:]+$", "", piece)
            piece = re.sub(r"\s+(?:and|or|to)$", "", piece)
        unit = found_one.group(2) or unit
        if set(keywords(piece)) & subject:
            hits.append((found_one, piece, unit))
    if len(hits) != 1:
        return None
    found_one, piece, unit = hits[0]
    if unit and not found_one.group(2):
        cut = found_one.end(1) - found_one.start()
        piece = piece[:cut] + " " + unit.lower() + piece[cut:]
    return piece[:1].upper() + piece[1:] + "."


TIME_ONLY = frozenset("""a an one two three four five six seven eight nine ten eleven twelve
    day days week weeks month months year years out before ahead after now from to in on at the
    of""".split())


def _only_a_marker(part):
    words = re.findall(r"[a-z0-9']+", str(part or "").lower())
    if not words:
        return True
    return all(word in TIME_ONLY or DURATION.match(word) for word in words)


def _duration_clauses(sentence):
    parts = []
    for part in _clauses_of(sentence):
        part = part.strip(" .")
        if _quoted(part):
            continue
        if part.lower().startswith("then "):
            part = part[5:]
        if part.lower().startswith("and "):
            part = part[4:]
        if WARNING_SPAN.search(part):
            continue
        if not part or _only_a_marker(part):
            continue
        if _not_a_length(part):
            continue
        if DURATION.search(part) or SPAN_ADJECTIVE.search(part):
            parts.append(part[0].upper() + part[1:] + ".")
    return parts


def _only_a_cadence(part):
    return bool(FREQUENCY.search(part)) and not DURATION.search(FREQUENCY.sub(" ", part))


A_WEATHER_WINDOW = re.compile(
    r"\b(?:forecast|rain|showers?|dry|damp|frost|wind|sunshine?|weather|mild|warm|cold)\b"
    r"[^.;:,]{0,25}\bfor\s+$", re.I)


def _a_window_in_the_weather(part):
    found = sorted(list(DURATION.finditer(part)) + list(SPAN_ADJECTIVE.finditer(part)),
                   key=lambda match: match.start())
    if not found:
        return False
    for match in found:
        if not A_WEATHER_WINDOW.search(part[:match.start()]):
            return False
    return True


def _not_a_length(part):
    return _only_a_cadence(part) or _a_window_in_the_weather(part)


def _duration_clause(sentence):
    parts = _duration_clauses(sentence)
    return parts[0] if parts else None


def _shorten(part):
    text = str(part or "")
    if len(text.split()) > 9:
        found = DURATION.search(text)
        if found and not text[found.end():].strip(" .,;:!?"):
            span = found.group(0).strip(" .")
            return span[:1].upper() + span[1:] + "."
    return part


PERIODS = {"minute": 0, "second": 0, "hour": 1, "day": 2, "week": 3, "month": 4, "year": 5}
PERIOD_ASK = re.compile(r"\b(?:a|an|each|every|per|one)\s+"
                        r"(seconds?|minutes?|hours?|days?|weeks?|months?|years?)\b", re.I)

PERIOD_LEAD = re.compile(r"^(?:[a-z]+ed|takes?|lasts?|runs?)\s+(?:for|about|around|roughly)?\s*",
                         re.I)


def _asked_period(line):
    found = PERIOD_ASK.search(str(line or ""))
    if found is None:
        return None
    unit = found.group(1).lower().rstrip("s")
    return PERIODS.get(unit)


FIGURED = re.compile(
    r"\d|\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen|twenty|"
    r"thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|couple|few|several|dozen|half|quarter)\b",
    re.I)


def _in_period(part, period):
    if period is None:
        return True
    if not FIGURED.search(str(part or "")):
        return False
    found = DURATION.search(str(part or ""))
    if found is None:
        return False
    counted = found.group(0).lower()
    for name, rank in PERIODS.items():
        if name in counted:
            return rank <= period
    return False


def _pick_duration(sentences, wanted, memory, line=""):
    if LENGTH_ASK.search(line or ""):
        sentences = [sentence for sentence in sentences
                     if DURATION.search(sentence) or SPAN_ADJECTIVE.search(sentence)]
        if not sentences:
            return None
        spans = [sentence for sentence in sentences if not THRESHOLD_SPAN.search(sentence)]
        if spans:
            sentences = spans
    wanted = set(wanted)
    best_overlap, best_index = 0, 0
    for index, sentence in enumerate(sentences):
        words = {stem(word) for word in keywords(sentence)}
        overlap = len(wanted & words)
        if overlap > best_overlap:
            best_overlap, best_index = overlap, index
    if best_overlap:
        sentence = sentences[best_index]
        period = _asked_period(line)
        if period is not None:
            parts = [part for part in _duration_clauses(sentence)
                     if _in_period(part, period)]
            part = _step_they_asked_for(parts, wanted)
            if part:
                part = PERIOD_LEAD.sub("", part)
                if not part[:1].isupper():
                    part = part[:1].upper() + part[1:]
            return _shorten(part) if part else None
        if not already_said(memory, sentence):
            return sentence
        parts = [part for part in _duration_clauses(sentence)
                 if not already_said(memory, part)]
        part = _step_they_asked_for(parts, wanted)
        return _shorten(part) if part else None
    if not best_overlap:
        choices = _option_range(sentences[0]) if sentences else ""
        if choices:
            return choices
        part = _the_option_for_the_topic(sentences[0], line, memory) if sentences else None
        if part:
            return part
    period = _asked_period(line)
    parts = [part for sentence in sentences for part in _duration_clauses(sentence)
             if not already_said(memory, part) and _in_period(part, period)]
    part = _step_they_asked_for(parts, wanted)
    return _shorten(part) if part else None


def _step_they_asked_for(parts, wanted):
    kept = [part for part in parts
            if not AFTERWARDS.search(part) or set(keywords(part)) & set(wanted)]
    if kept:
        return kept[-1]
    return parts[-1] if parts else None

def _time_in_words(minutes):
    minutes = int(round(minutes / 5.0)) * 5
    hours, rest = divmod(minutes, 60)
    if not hours:
        return f"{rest} minutes"
    hours_text = f"{hours} hour" + ("" if hours == 1 else "s")
    return f"{hours_text} {rest}" if rest else hours_text


def time_for_amount(answer, line):
    amount = AMOUNT.search(str(line or ""))
    rate = RATE_BY_WEIGHT.search(str(answer or ""))
    if not amount or not rate:
        return None
    each, per, unit = rate.groups()
    said_unit = re.sub(r"[\d.\s]", "", amount.group(0)).lower()
    if said_unit not in WEIGHT_IN_GRAMS or unit.lower() not in WEIGHT_IN_GRAMS:
        return None
    want = float(re.sub(r"[^\d.]", "", amount.group(0))) * WEIGHT_IN_GRAMS[said_unit]
    base = float(per) * WEIGHT_IN_GRAMS[unit.lower()]
    if base <= 0 or want <= 0:
        return None
    total = float(each) * want / base
    extra = PLUS_MINUTES.search(str(answer))
    if extra:
        total += float(extra.group(1))
    if not 5 <= total <= 12 * 60:
        return None
    return _time_in_words(total)


def _already_for_this_size(line, answer):
    asked, told = AMOUNT.search(str(line or "")), OWN_SIZE.search(str(answer or ""))
    if not asked or not told:
        return False
    grams = _in_grams(asked.group(0))
    said = _in_grams(told.group(1) + told.group(2))
    return grams is not None and grams == said


def _in_grams(text):
    found = re.match(r"\s*(\d+(?:\.\d+)?)\s*(kg|g|lb|lbs|pound|pounds|oz|ounce|ounces)\b",
                     str(text or ""), re.I)
    if not found:
        return None
    return round(float(found.group(1)) * WEIGHT_IN_GRAMS[found.group(2).lower()], 1)


def _names_another_thing(line, answer, about=()):
    said = set(stem(word) for word in keywords(answer))
    said |= set(stem(word) for word in about or ())
    for word in keywords(line):
        if AMOUNT.search(word) or word in ASK_ONLY:
            continue
        if stem(word) not in said:
            return True
    return False


def sized_reply(answer, line, memory, about=()):
    if _names_another_thing(line, answer, about) or _already_for_this_size(line, answer):
        return None
    return _sized_reply(answer, line, memory)


def _sized_reply(answer, line, memory):
    amount = AMOUNT.search(str(line or ""))
    if not amount:
        return None
    sized = time_for_amount(answer, line)
    if not sized:
        return None
    rule = _rate_said(answer)
    if not rule:
        return None
    said = amount.group(0)
    times = _times_asked(line, memory)
    if times >= 2:
        return f"{sized.capitalize()} for {said}, the same rule: {rule}."
    if times == 1:
        return f"Still {sized} for {said}: {rule}."
    return f"About {sized} for {said}: {rule}."


def _times_asked(line, memory):
    wanted = " ".join(str(line or "").lower().split())
    count = 0
    for turn in reversed(memory.get("turns") or []):
        if not isinstance(turn, dict):
            break
        if " ".join(str(turn.get("user") or "").lower().split()) != wanted:
            break
        count += 1
    return count


def _rate_said(answer):
    for sentence in SENTENCE.split(str(answer or "")):
        if not RATE_BY_WEIGHT.search(sentence):
            continue
        head = re.split(r"[,;]?\s+so\b", sentence, maxsplit=1)[0].strip(" .,;")
        head = re.sub(r"^about\s+", "", head, flags=re.I).strip(" .,;")
        return head[:1].lower() + head[1:] if head[:1].isupper() else head
    return ""


def _phrase(text):
    text = str(text or "").strip(" ,;:")
    return text[:1].upper() + text[1:] + "." if text else ""


def has_time(text):
    return bool(TIME.search(str(text or "")))


def _worked_out_for_this_line(understood, line, answer):
    if not isinstance(understood, dict) or "how_long" not in (understood.get("asks") or ()):
        return None
    return time_for_amount(answer, line)


_ASKS_WHAT_I_AM = re.compile(
    r"^\s*(?:(?:so|ok|okay|and|but|hey|well)\s+)*"
    r"(?:where|what|who|which)\s+(?:are|r)\s+(?:you|u|ya)\b"
    r"(?:\s+(?:from|based|exactly|then|though|really|actually|now))?\s*\??\s*$")


def asks_only(understood):
    if not isinstance(understood, dict) or not (understood.get("asks") or ()):
        return False
    line = understood.get("clean") or understood.get("text") or ""
    if _ASKS_WHAT_I_AM.match(str(line).lower()):
        return False
    return not [word for word in keywords(line) if word not in ASK_ONLY]


def _earlier_subject_sentence(line, understood, memory, skip, turns_back=2):
    records = memory.get("topics")
    if not isinstance(records, list):
        return None
    mine = {stem(word) for word in keywords(line)}
    seen = 0
    for record in reversed(records):
        if not isinstance(record, dict) or record is skip:
            continue
        asked = str(record.get("text") or "")
        if not asked or already_said(memory, record.get("bot")):
            continue
        if not mine & {stem(word) for word in keywords(asked)}:
            continue
        seen += 1
        if seen > turns_back:
            return None
        answer = entry_answer(memory, asked) or str(record.get("bot") or "")
        chosen = _pick_sentence(line, understood, answer, memory, strict=True)
        if chosen:
            return chosen
    return None


def _repeats_the_question(line, asked):
    wanted = [stem(word) for word in keywords(line)]
    if not wanted:
        return True
    said = [stem(word) for word in keywords(asked)]
    return sum(1 for word in wanted if word in said) >= 0.6 * len(wanted)


def already_said(memory, text, turns_back=3):
    said = " ".join(str(text or "").lower().split())
    if not said:
        return True
    for turn in (memory.get("turns") or [])[-turns_back:]:
        if isinstance(turn, dict) and " ".join(str(turn.get("bot") or "").lower().split()) == said:
            return True
    return False


STEP_ASK_WORDS = frozenset("""
how what when where which who why do does did i we you me my it this that they he she
fix sort make get work use put keep go come start stop change deal help try take set tell say
give find need want know best should can could would will shall may might
""".split())


def _names_something_new(line, answer):
    said = {stem(word) for word in keywords(answer)}
    for word in keywords(line):
        if word in STEP_ASK_WORDS or stem(word) in said:
            continue
        return True
    return False




REQUEST_A_THING = re.compile(r"\b(?:find|give|send|show|get|recommend|suggest|list|write|make)"
                             r" me\b|\bdo you have\b|\bany chance\b"
                             r"|\bcan you (?:find|give|send|show|recommend|suggest|list\b)", re.I)
A_THING = frozenset("a an the my our another some this that".split())


def _named_a_fresh_thing(text, record, answer=""):
    if REQUEST_A_THING.search(str(text or "")):
        return False
    known = {stem(word) for word in (record or {}).get("words") or []}
    known |= {stem(word) for word in words(str(answer or ""))}
    said = words(str(text or ""))
    for at, word in enumerate(said[:-1]):
        if word.lower() in A_THING and stem(said[at + 1]) not in known:
            return True
    return False


MOVED_KEEP = 8


def _the_thing_the_chat_moved_to(whole, line, memory, keep=MOVED_KEEP):
    from .narrow import SPANS, kind_of
    turns = [turn for turn in (memory.get("turns") or [])[-keep:] if isinstance(turn, dict)]
    wanted = words(str(whole or ""))[:8]
    at = None
    for index, turn in enumerate(turns):
        if words(str(turn.get("bot") or ""))[:8] == wanted:
            at = index
    if at is None:
        return None
    was = _entry(str(turns[at].get("user") or ""))
    if was is None:
        return None
    figure = SPANS.get(kind_of(line))
    if figure is None:
        return None
    for turn in reversed(turns[at + 1:]):
        said = str(turn.get("user") or "")
        if not said or words(said) == words(str(line or "")):
            continue
        if turn.get("module") in (None, "answers"):
            continue
        named = _entry(said)
        if named is None or named == was:
            continue
        if figure.search(str(getattr(named, "reply", "") or "")):
            return named
    return None


def left_for_a_blank(memory, line):
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns or not isinstance(turns[-1], dict):
        return False
    last = turns[-1]
    if " ".join(words(str(last.get("user") or ""))) == " ".join(words(str(line or ""))):
        return False
    if last.get("module") == "answers":
        return False
    asked = str(last.get("user") or "")
    if not _a_question(asked):
        return False
    if not POINTS_BACK.search(str(line or "")):
        return False
    record = carried_topic(memory, line)
    answer = entry_answer(memory, str((record or {}).get("text") or "")) or str(last.get("bot") or "")
    return _named_a_fresh_thing(asked, record, answer)


POINTS_BACK = re.compile(r"\b(?:it|that|this|those|these|they|them|its)\b|\bthe one\b", re.I)

A_QUESTION = re.compile(r"\?\s*$|^\s*(?:and|also|or|so|but|then)\s+\S+"
                        r"|^\s*(?:what|how|which|where|when|who|why|whose|is|are|was|were|do"
                        r"|does|did|can|could|should|would|will|shall|must|have|has|had|am)\b",
                        re.I)


def _a_question(text):
    return bool(A_QUESTION.search(str(text or "")))


BARE_ASK = re.compile(r"\b(?:what|which|how|where|when)\b(?![^?.!]{0,40}\b(?:did|have|has)\s+i\b)"
                      r"[^?.!]{0,40}\b(?:should|shall|can|could|ought)\b"
                      r"|^\s*(?:so\s+)?(?:should|shall|can|could|must|do)\s+(?:i|we)\b", re.IGNORECASE)
BARE_WORDS = 8


def bare_question(understood, memory):
    if not isinstance(understood, dict) or understood.get("kind") != "question":
        return False
    line = " ".join(str(understood.get("clean") or understood.get("text") or "").lower().split())
    if not line or len(line.split()) > BARE_WORDS or is_ack(line):
        return False
    if not BARE_ASK.search(line):
        return False
    if carried_topic(memory, line) is None:
        return False
    if follows_on(understood, line):
        return False
    if ASKS_ABOUT_THEMSELVES.search(line):
        return False
    return _entry(line) is None


ASKS_ABOUT_THEMSELVES = re.compile(
    r"\b(?:what|where|when|who|which|how|why)\s+(?:am|are|was|were|did)\s+(?:i|we)\b")


def _still_the_topic(record, memory):
    if not isinstance(record, dict):
        return False
    index = record.get("turn")
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(index, int) or not isinstance(turns, list):
        return True
    from ..understanding import understand
    for turn in turns[index + 1:]:
        if not isinstance(turn, dict):
            continue
        said = " ".join(str(turn.get("user") or "").lower().split())
        if not said or is_ack(said) or said in GREET:
            continue
        if str(understand(said).get("intent") or "") == "smalltalk":
            return False
    return True


def carried_topic(memory, text):
    line = " ".join(words(text))
    records = memory.get("topics")
    if isinstance(records, list):
        for record in reversed(records):
            if not isinstance(record, dict):
                continue
            if " ".join(words(record.get("text") or "")) != line:
                return _thing_of(memory, record) or record
    return current(memory)


def leans_on_topic(understood, memory):
    if not isinstance(understood, dict):
        return False
    if _after_an_emergency(memory):
        return False
    if _after_a_correction(memory):
        return False
    said = understood.get("clean") or understood.get("text") or ""
    text = without_the_shrug(said)
    if any(phrase in text.lower() for phrase in PROCEED):
        return False
    record = carried_topic(memory, text)
    if record is None or not text.strip() or is_ack(text):
        return False
    if opens_by_switching(said):
        return False
    if DETAIL.search(text):
        known = set(record.get("words") or [])
        fresh = [word for word in keywords(text) if stem(word) not in known]
        return len(fresh) <= 4 and len(words(text)) <= 14
    if follows_on(understood, text):
        return True
    carried = carry_the_ask(text, record.get("text") or "", understood, memory)
    if carried is None:
        return bare_question(understood, memory)
    return names_nothing(text) or _only_the_topics_own_words(text, record)


def _only_the_topics_own_words(text, record):
    known = [word for word in (record or {}).get("words") or [] if isinstance(word, str)]
    if not known:
        return False
    return not [word for word in _content_words(text)
                if not any(alike(word, said) for said in known)]


NEXT_SLOT = re.compile(r"^(?:and|also|plus|then|ok|okay|so)\s+(?:what\s+)?for\s+([a-z0-9' ]{2,24})$")
ASK_SLOT = re.compile(r"\bfor\s+([a-z0-9' ]{2,24})$")
ASK_WORDS = re.compile(r"\b(?:what|which|how|where|when|who|why|should|shall|can|could|would|any)\b")


def next_slot_reading(understood, memory):
    if not isinstance(understood, dict) or not isinstance(memory, dict):
        return None
    line = " ".join(str(understood.get("clean") or understood.get("text") or "").lower().split())
    slot = NEXT_SLOT.match(line)
    if slot is None or understood.get("kind") == "question":
        return None
    turns = memory.get("turns")
    previous = ""
    if isinstance(turns, list) and turns:
        previous = str((turns[-1] or {}).get("user") or "")
    asked = " ".join(previous.lower().split())
    if not asked or ASK_WORDS.search(asked) is None:
        return None
    tail = ASK_SLOT.search(asked)
    if tail is None:
        return None
    thing = slot.group(1).strip()
    if not thing or thing == tail.group(1).strip():
        return None
    reading = dict(understood)
    reading["clean"] = (asked[:tail.start()] + "for " + thing).strip()
    reading["text"] = reading["clean"]
    reading["words"] = words(reading["clean"])
    reading["kind"] = "question"
    reading["intent"] = "question"
    return reading


TWO_PETS_ASK = re.compile(
    r"^(?:and |so |but )?(?:will (?:they|the two(?: of them)?|both(?: of them)?) (?:get on|get along|"
    r"fight|like each other|settle)"
    r"(?: (?:ok|okay|alright|fine|together))?"
    r"(?: with (?:each other|one another))?"
    r"|are they going to (?:get on|get along|fight)"
    r"|(?:can|could|will) (?:they|the two) (?:live|get) (?:together|along))"
    r"[\s?.!]*$",
    re.I)
PET_WORD = re.compile(
    r"\b(kittens?|cats?|pupp(?:y|ies)|dogs?|rabbits?|bunn(?:y|ies)|hamsters?|guinea pigs?|"
    r"ferrets?|parrots?|budgies?)\b", re.I)
PET_ONE = {
    "kittens": "kitten", "cats": "cat", "puppies": "puppy", "dogs": "dog",
    "rabbits": "rabbit", "bunnies": "bunny", "hamsters": "hamster",
    "guinea pigs": "guinea pig", "ferrets": "ferret", "parrots": "parrot",
    "budgies": "budgie",
}
PET_ARRIVING = re.compile(
    r"\b(?:getting|bringing|bringing home|joining|coming|arriving|arrives|arrive|"
    r"next (?:week|month|year)|in (?:january|february|march|april|may|june|july|august|"
    r"september|october|november|december)|soon)\b", re.I)
PET_EXISTING = re.compile(r"\b(?:already|existing|older|old|has been|have had)\b", re.I)


def _introduction_covered(new, old):
    cats = {"cat", "kitten"}
    dogs = {"dog", "puppy"}
    return ((new in cats and old == "cat")
            or (new in cats and old in dogs)
            or (new in dogs and old in cats))


def introduction_question(text, memory):
    if not isinstance(text, str) or not isinstance(memory, dict) or not TWO_PETS_ASK.search(text):
        return ""
    known = memory.get("user")
    if not isinstance(known, dict):
        return ""
    animals = []
    for pet in known.get("pets") or ():
        animal = pet.get("animal") if isinstance(pet, dict) else None
        animal = str(animal or "").strip().lower()
        animal = PET_ONE.get(animal, animal)
        if animal and animal not in animals:
            animals.append(animal)
    if len(animals) != 2:
        return ""
    plan = known.get("plan")
    named = PET_WORD.search(plan) if isinstance(plan, str) else None
    new = ""
    if named is not None:
        new = PET_ONE.get(named.group(1).lower(), named.group(1).lower())
    else:
        arriving = []
        for fact in memory.get("facts_log") or ():
            if not isinstance(fact, dict) or fact.get("key") != "pet":
                continue
            said = str(fact.get("text") or "")
            found = PET_WORD.search(said)
            if found is None or not PET_ARRIVING.search(said) or PET_EXISTING.search(said):
                continue
            animal = PET_ONE.get(found.group(1).lower(), found.group(1).lower())
            if animal not in arriving:
                arriving.append(animal)
        if len(arriving) == 1:
            new = arriving[0]
    if not new:
        return ""
    others = [animal for animal in animals if animal != new]
    if len(others) != 1:
        return ""
    old = others[0]
    if not _introduction_covered(new, old):
        return ""
    return "how do i introduce a new %s to my older %s" % (new, old)
WEATHER_WORDS = frozenset("""
weather hot hotter cold colder warm warmer cool freezing boiling rain rains raining rainy
showers shower sunny sun sunshine cloudy cloud clouds wind windy humid humidity temperature
degrees forecast snow snowing coat coats jacket layers jumper
""".split())

MONTH_NAMES = frozenset("""january february march april may june july august september october
november december""".split())

WEATHER_NOISE = frozenset("""
ok okay k so and but the a an in on at for to of it its this that these there here what whats
how will would be is was were am get getting go going we you they i me my our us week weeks
day days month months time much many like look looks outside today tomorrow tonight now then do
does did shown show get better need bring bring take maybe probably out up over all there
""".split())

NOW_AND_HERE = re.compile(
    r"\b(?:today|tonight|tomorrow|now|right now|outside|here|this afternoon|this evening"
    r"|this morning|at the moment|currently)\b")

WEATHER_ASKS = re.compile(
    r"\?|^(?:is|are|do|does|will|would|can|could|should|shall)\b"
    r"|\b(?:what|whats|how|when|where|which|will|would|can|could|should|any|much|many|need)\b")


def the_weather_ask(understood):
    line = str(understood.get("clean") or understood.get("text") or "")
    said = words(line)
    if not any(word in WEATHER_WORDS for word in said):
        return False
    if ASK_CUE.search(line.lower()) is None and WEATHER_ASKS.search(line.lower()) is None:
        return False
    return all(word in WEATHER_WORDS or word in WEATHER_NOISE for word in said)


def the_place_and_month(text):
    low = " ".join(str(text or "").lower().split())
    if not low:
        return None, None
    from ..knowledge.travel import CITY_CLIMATE
    for name in sorted(CITY_CLIMATE, key=len, reverse=True):
        if re.search(r"(?<![a-z])" + re.escape(name) + r"(?![a-z])", low) is None:
            continue
        month = next((word for word in sorted(MONTH_NAMES, key=len, reverse=True)
                      if re.search(r"(?<![a-z])" + word, low)), None)
        return name, month
    return None, None


PERIOD_ONLY = frozenset("""
and or but also so in on at for about during of the a an what whats how when to it that there
weather like is will be gonna going get have we i you they month months next this coming
""".split())

SEASONS = frozenset("spring summer autumn fall winter".split())


def _the_period_in(text):
    low = " ".join(str(text or "").lower().split())
    for name in sorted(MONTH_NAMES | SEASONS, key=len, reverse=True):
        for found in re.finditer(r"(?<![a-z])" + name + r"(?![a-z])", low):
            before = low[:found.start()].split()
            after = low[found.end():].strip(" ?!.,")
            if not before or before[-1] in ("in", "next", "this", "the", "early", "late", "mid",
                                            "until", "til", "by", "for", "about", "of", "and"):
                return found.group(0)
            if name not in ("may", "march", "fall") or not after:
                return found.group(0)
    return ""


def _a_period_and_nothing_else(line):
    said = words(line)
    if not _the_period_in(line):
        return False
    return all(word in PERIOD_ONLY or word in MONTH_NAMES or word in SEASONS for word in said)


def the_period_they_ask_about(understood, memory):
    line = str(understood.get("clean") or understood.get("text") or "")
    if not _a_period_and_nothing_else(line):
        return None
    period = _the_period_in(line)
    record = carried_topic(memory, line)
    asked = str((record or {}).get("text") or "")
    was = _the_period_in(asked)
    if was == period:
        return None
    if not was:
        if not _the_answer_was_about_the_weather(memory):
            return None
        place = _the_place_the_chat_is_on(line, memory)
        if place is None:
            return None
        return f"what is the weather like in {place} in {period}"
    if ASK_CUE.search(asked.lower()) is None and WEATHER_ASKS.search(asked.lower()) is None:
        return None
    return _with_the_period(asked, was, period)


def _the_answer_was_about_the_weather(memory):
    for turn in reversed(memory.get("turns") or []):
        if not isinstance(turn, dict):
            continue
        said = str(turn.get("bot") or "")
        if not said.strip():
            continue
        return bool(WEATHER_WORDS & set(words(said)))
    return False


def _the_place_the_chat_is_on(line, memory):
    mine = " ".join(words(line))
    for said in _the_lines_said(memory):
        if " ".join(words(said)) == mine:
            continue
        if the_weather_ask({"clean": said, "text": said}):
            continue
        if _a_period_and_nothing_else(said):
            continue
        if A_TRIP_TAKEN.search(" ".join(str(said).lower().split())):
            return None
        place, _month = the_place_and_month(said)
        if place is not None:
            return place
        return None
    return None


def _with_the_period(asked, was, now):
    out = re.sub(r"(?<![a-z])" + re.escape(was) + r"(?![a-z])", now, asked, count=1)
    return " ".join(out.lower().split())


MEAL_NAMES = frozenset("""breakfast lunch dinner supper brunch""".split())
MEAL_ONLY = frozenset("""
a an about also and anything at but can could do does eat for have how i instead is it make me
or should so something that the then there to we what whats will would you
""".split())


OPENS_A_FOLLOW_UP = re.compile(r"^(?:and|also|then|or|so|what about|how about|whats|same)\b", re.I)


def _the_meal_in(text):
    low = " ".join(str(text or "").lower().split())
    for name in sorted(MEAL_NAMES, key=len, reverse=True):
        if re.search(r"(?<![a-z])" + name + r"(?![a-z])", low):
            return name
    return ""


def _a_meal_and_nothing_else(line):
    said = words(line)
    if not _the_meal_in(line):
        return False
    return all(word in MEAL_ONLY or word in MEAL_NAMES for word in said)


def the_meal_they_ask_about(understood, memory):
    line = str(understood.get("clean") or understood.get("text") or "")
    if not _a_meal_and_nothing_else(line):
        return None
    meal = _the_meal_in(line)
    record = carried_topic(memory, line)
    asked = str((record or {}).get("text") or "")
    was = _the_meal_in(asked)
    if not was:
        if not OPENS_A_FOLLOW_UP.match(line):
            return None
        return "what can i have for " + meal
    if was == meal:
        return None
    if ASK_CUE.search(asked.lower()) is None:
        return None
    return _with_the_meal(asked, was, meal)


def meal_follow_up(understood, memory):
    meal = the_meal_they_ask_about(understood, memory)
    if not meal:
        return None
    reading = dict(understood)
    reading["clean"] = meal
    reading["words"] = words(meal)
    if "norm_text" in reading:
        reading["norm_text"] = meal
    return reading


def _with_the_meal(asked, was, now):
    out = re.sub(r"(?<![a-z])" + re.escape(was) + r"(?![a-z])", now, asked, count=1)
    return " ".join(out.lower().split())


def the_weather_of_the_trip(understood, memory):
    if not the_weather_ask(understood):
        return None
    line = str(understood.get("clean") or understood.get("text") or "")
    place, month = the_place_and_month(line)
    if place is not None:
        return None
    if NOW_AND_HERE.search(line.lower()):
        return None
    place, month = the_place_and_month(_the_trip_said(line, memory))
    if place is None or month is None:
        return None
    return f"what is the weather like in {place} in {month}"


A_TRIP_TAKEN = re.compile(
    r"\b(?:(?:i|we|he|she|they)\s+(?:went|were|was|been|had|did|stayed|visited|flew|drove)"
    r"|got\s+back|came\s+back|back\s+from|just\s+back|returned)\b", re.I)


def _the_trip_said(line, memory):
    mine = " ".join(words(line))
    for said in _the_lines_said(memory):
        if " ".join(words(said)) == mine:
            continue
        if the_weather_ask({"clean": said, "text": said}):
            continue
        place, month = the_place_and_month(said)
        if place is None or month is None:
            return ""
        if A_TRIP_TAKEN.search(" ".join(said.lower().split())):
            return ""
        return said
    return ""


def _the_lines_said(memory):
    if not isinstance(memory, dict):
        return []
    out = []
    for turn in reversed(memory.get("turns") or []):
        said = str((turn or {}).get("user") or "") if isinstance(turn, dict) else ""
        if said.strip():
            out.append(said)
    return out


THING_ITSELF = re.compile(r"\b(it|its|them|they)\b", re.I)
IT_IS_PART_OF_THE_PHRASE = (
    "make it up", "making it up", "put it right", "make it right", "put it behind",
    "take it out on", "took it out on", "let it go", "let it lie", "get it wrong",
    "got it wrong", "getting it wrong", "said it wrong", "put it down to", "have it out with")
BABY_OF = {"puppy": "dog", "kitten": "cat"}
WHAT_IT_COSTS = re.compile(r"\b(?:cost|costs|costing|price|prices|worth|expensive|cheap|cheaper|"
                           r"pay|paid|fee|fees|insurance|bill|bills|money|afford)\b", re.I)
WORTH_DECIDING = re.compile(
    r"\b(?:is|would|will)\s+(?:it|that|this|they)\s+"
    r"(?:worth|better|best|cheaper|cheapest|smarter)\b[^?]*"
    r"\b(?:fix|repair|replac|restor|servic|renew|upgrad|pay|spend|buy"
    r"|keep|sell|insur|invest|switch)\w*", re.I)


PLACEHOLDER_PRONOUN = re.compile(
    r"\bworth\s+(?:getting|having|buying)|\bworth\s+(?:get|have|buy)\b", re.IGNORECASE)
A_NEW_ONE = re.compile(
    r"\b(?:new|another|bigger|smaller|different|better|second|cheaper|proper)\s+one\b"
    r"|\bone\s+instead\b|\bone\s+of\s+(?:those|them)\b", re.IGNORECASE)


def a_placeholder_pronoun(line):
    text = str(line or "")
    return bool(PLACEHOLDER_PRONOUN.search(text) and not A_NEW_ONE.search(text))


def the_ask_about_the_thing_it_points_at(understood, memory):
    if not isinstance(understood, dict) or not isinstance(memory, dict):
        return None
    line = " ".join(str(understood.get("clean") or understood.get("text") or "").split())
    if not line or not THING_ITSELF.search(line):
        return None
    if any(phrase in line.lower() for phrase in PROCEED):
        return None
    if any(phrase in line.lower() for phrase in IT_IS_PART_OF_THE_PHRASE):
        return None
    if WHAT_IT_COSTS.search(line):
        return None
    ref = understood.get("ref") if isinstance(understood.get("ref"), dict) else None
    if not isinstance(ref, dict) or ref.get("kind") != "thing":
        return None
    thing = ref.get("it") or ref.get("that")
    if not isinstance(thing, str):
        return None
    thing = " ".join(thing.split())
    if not thing or len(thing.split()) > 3 or thing in ("it", "that", "them", "they", "you", "me"):
        return None
    if thing in line.lower():
        return None
    filled = " ".join(THING_ITSELF.sub("my " + thing, line, count=1).split())
    reading = dict(understood)
    reading["clean"] = filled
    reading["words"] = words(filled)
    return reading


POINTING_WORDS = ("it", "they", "them", "that", "this", "he", "she")


def the_pronoun_written_as_what_it_stands_for(understood, memory):
    if not isinstance(understood, dict) or not isinstance(memory, dict):
        return None
    line = " ".join(str(understood.get("clean") or understood.get("text") or "").split())
    if not line:
        return None
    ref = understood.get("ref") if isinstance(understood.get("ref"), dict) else None
    if not isinstance(ref, dict):
        return None
    if understood.get("kind") != "question":
        return None
    if any(phrase in line.lower() for phrase in PROCEED):
        return None
    if any(phrase in line.lower() for phrase in IT_IS_PART_OF_THE_PHRASE):
        return None
    if _entry(line) is not None:
        return None
    last = memory.get("last_answer") if isinstance(memory.get("last_answer"), dict) else {}
    record = carried_topic(memory, line)
    topic_entry = _entry(str((record or {}).get("text") or "")) if record else None
    topic_domain = getattr(topic_entry, "domain", None) if topic_entry is not None else None
    for word in POINTING_WORDS:
        thing = ref.get(word)
        if not isinstance(thing, str):
            continue
        thing = " ".join(thing.split())
        if not thing or thing.lower() in ("it", "that", "them", "they", "you", "me", "there"):
            continue
        if re.search(r"\b%s\b" % re.escape(thing.lower()), line.lower()):
            continue
        if not re.search(r"\b%s\b" % word, line, re.IGNORECASE):
            continue
        for phrase in _the_thing_with_a_determiner(thing):
            filled = re.sub(r"\b%s\b" % word, phrase, line, count=1, flags=re.IGNORECASE)
            filled = " ".join(filled.lower().split())
            entry = _entry(filled)
            if entry is None:
                continue
            if not _the_entry_is_about_the_thing(entry, thing.split()[-1].lower()):
                continue
            if not _the_entry_answers_the_ask(entry, filled):
                continue
            if topic_domain and getattr(entry, "domain", None) != topic_domain:
                continue
            if last.get("id") and entry.id == last.get("id"):
                continue
            reading = dict(understood)
            reading["clean"] = filled
            reading["words"] = words(filled)
            if "norm_text" in reading:
                reading["norm_text"] = filled
            return reading
    return None


WITHOUT_A_DETERMINER = frozenset("""
    it they them that this he she i you we me my your our their his her its
    a an the some any no every each
""".split())


def _the_thing_with_a_determiner(thing):
    ways = []
    first = thing.split()[0].lower()
    if first not in WITHOUT_A_DETERMINER:
        article = "an" if first[:1] in "aeiou" else "a"
        ways.extend([article + " " + thing, "the " + thing, "my " + thing])
    ways.append(thing)
    return ways


def the_thing_it_is(understood, memory):
    if not isinstance(understood, dict) or not isinstance(memory, dict):
        return None
    line = str(understood.get("clean") or understood.get("text") or "").strip()
    if not line or not ASK_CUE.search(line.lower()) or not THING_ITSELF.search(line):
        return None
    if any(phrase in line.lower() for phrase in PROCEED):
        return None
    if WORTH_DECIDING.search(line) or a_placeholder_pronoun(line):
        return None
    if not WHAT_IT_COSTS.search(line):
        thing = the_pet_the_line_before_named(memory)
        if not thing:
            return None
        filled = THING_ITSELF.sub(thing, line, count=1)
        if _entry(filled) is None:
            return None
        reading = dict(understood)
        reading["clean"] = " ".join(filled.lower().split())
        reading["words"] = words(reading["clean"])
        return reading
    if _entry(line) is not None:
        return None
    last = memory.get("last_answer") if isinstance(memory, dict) else None
    last_id = last.get("id") if isinstance(last, dict) else None
    for thing, word in _the_things_the_pronoun_stands_for(memory, line):
        filled = THING_ITSELF.sub(thing, line, count=1)
        entry = _entry(filled)
        if entry is None:
            continue
        if not _the_entry_is_about_the_thing(entry, word):
            continue
        if not _the_entry_answers_the_ask(entry, filled):
            continue
        if last_id and entry.id == last_id:
            continue
        reading = dict(understood)
        reading["clean"] = " ".join(filled.lower().split())
        reading["words"] = words(reading["clean"])
        return reading
    return None


SOMETHING_IS_BROKEN = re.compile(
    r"\b(?:broke|broken|not working|stopped working|wont work|won't work|faulty|leaking|"
    r"isnt working|isn't working|packed in|given up)\b", re.I)


def _the_things_the_pronoun_stands_for(memory, line):
    out = []
    pet = the_pet_the_line_before_named(memory)
    if pet:
        out.append((pet, pet.split()[-1]))
    record = carried_topic(memory, line)
    text = " ".join(str((record or {}).get("text") or "").lower().split())
    if not text or SOMETHING_IS_BROKEN.search(text):
        return out
    said = " " + text
    mine = _what_they_called_theirs(said)
    if mine:
        return out + [pair for pair in mine if pair not in out]
    for word in key_subject(text, memory):
        if word in words(line):
            continue
        phrase = word
        if " my " + word in said or text.startswith("my " + word):
            phrase = "my " + word
        elif " the " + word in said or text.startswith("the " + word):
            phrase = "the " + word
        if (phrase, word) not in out:
            out.append((phrase, word))
    return out


THEIR_OWN = re.compile(r"\b(my|the)\s+([a-z']+)", re.I)
NOT_THEIR_OWN = frozenset("""
own self way turn go mind head opinion fault point lot bit time while moment
life day week month year today house home place
""".split())
_SMALL = frozenset("""
a an the and or but of to in on at for with is was are were be been has have had got
""".split())


def _what_they_called_theirs(text):
    out = []
    for lead, word in THEIR_OWN.findall(text):
        if len(word) < 3 or word in _SMALL or word in NOT_THEIR_OWN:
            continue
        pair = (lead.lower() + " " + word, word)
        if pair not in out:
            out.append(pair)
    return out[:3]


NAMES_THE_RUNNING = re.compile(
    r"\b(?:run|runs|running|use|uses|using|used|electricity|electric|energy|power|cycle|cycles"
    r"|hour|hours|kwh|gas|water|heating)\b", re.I)


def _the_entry_answers_the_ask(entry, line):
    if str(getattr(entry, "id", "")).endswith("running-cost") or str(
            getattr(entry, "id", "")).endswith("running-costs"):
        return bool(NAMES_THE_RUNNING.search(line))
    return True


def _the_entry_is_about_the_thing(entry, word):
    return any(word in group for group in entry.key)


WHAT_IT_IS_LIKE = frozenset("""
    expensive cheap pricey costly affordable far near close long short quick slow fast easy hard
    difficult simple complicated warm hot cold wet dry busy crowded quiet noisy loud heavy light
    big small tall serious dangerous risky safe legal allowed normal common free fresh healthy
    filling fattening spicy sweet salty sour stale raw ready open tidy good bad better worse fine
""".split())
WHAT_STANDS_IN = re.compile(r"\b(?:it|its|they|them|that|this|those|these)\b", re.I)
STANDS_IN = frozenset("it its they them that this those these".split())
MONEY = frozenset("""
    expensive cheap cheaper pricey costly affordable dear reasonable spend afford price cost costs
""".split())
YES_NO = re.compile(
    r"^\s*(?:(?:and|but|so|ok|okay|then|also|now|hmm|oh)\s+|what\s+about\s+|how\s+about\s+)?"
    r"(?:is|are|was|were|will|would|do|does|did|should|can|could|any)\b", re.I)


PROGNOSIS = {
    "go": "go away", "goes": "go away", "going": "go away", "gone": "go away",
    "away": "go away", "clear": "clear up", "clears": "clear up", "clearing": "clear up",
    "heal": "heal", "heals": "heal", "healing": "heal", "settle": "settle",
    "settles": "settle", "last": "last", "lasts": "last", "lasting": "last",
    "get": "get better", "gets": "get better", "getting": "get better",
    "improve": "get better", "improves": "get better", "pass": "pass",
    "passes": "pass", "fade": "fade", "fades": "fade", "down": "go down",
}


def the_prognosis_the_line_asks(understood, memory):
    if not isinstance(understood, dict) or not isinstance(memory, dict):
        return None
    line = str(understood.get("clean") or understood.get("text") or "").strip()
    if not line or not YES_NO.search(line) or not WHAT_STANDS_IN.search(line):
        return None
    said = words(line)
    outcomes = [PROGNOSIS[word] for word in said if word in PROGNOSIS]
    if not outcomes:
        return None
    left = [word for word in said
            if word not in STOPWORDS and word not in STANDS_IN and word not in PROGNOSIS
            and word not in WHAT_IT_IS_LIKE]
    if left:
        return None
    if isinstance(memory.get("person"), dict) and memory.get("person"):
        return None
    thing = subject(memory)
    named = words(thing) if thing else []
    if len(named) != 1 or set(named) & WHO:
        return None
    word = named[0]
    already = _entry(topic_text(memory))
    for outcome in dict.fromkeys(outcomes + ["last", "get better"]):
        for written in _the_thing_as_a_question_names_it(named):
            if outcome == "last":
                ask = "how long does " + written + " last"
            else:
                ask = "how long does " + written + " take to " + outcome
            entry = _entry(ask)
            if entry is None:
                continue
            if not _the_entry_is_about_the_thing(entry, word):
                continue
            if not _keyed_on_how_long(entry):
                continue
            if already is not None and entry.key == already.key:
                continue
            reading = dict(understood)
            reading["clean"] = " ".join(ask.split())
            reading["words"] = words(reading["clean"])
            if "norm_text" in reading:
                reading["norm_text"] = reading["clean"]
            return reading
    return None


HOW_LONG_KEY = frozenset([
    "how long", "last", "lasts", "lasting", "duration",
    "week", "weeks", "month", "months", "day", "days", "long",
])


def _keyed_on_how_long(entry):
    return any(phrase in group for group in getattr(entry, "key", ())
               for phrase in HOW_LONG_KEY)


def _the_thing_as_a_question_names_it(named):
    whole = " ".join(named)
    if named[0] in ("my", "a", "an", "the", "his", "her", "our", "their", "your"):
        return [whole]
    return [whole, "a " + whole, "the " + whole]


def the_property_of_the_thing(understood, memory):
    if not isinstance(understood, dict) or not isinstance(memory, dict):
        return None
    line = str(understood.get("clean") or understood.get("text") or "").strip()
    if not line or not YES_NO.search(line) or not WHAT_STANDS_IN.search(line):
        return None
    said = set(words(line))
    if not said & WHAT_IT_IS_LIKE:
        return None
    left = [w for w in words(line)
            if w not in WHAT_IT_IS_LIKE and w not in STOPWORDS and w not in STANDS_IN]
    if left:
        return None
    if isinstance(memory.get("person"), dict) and memory.get("person"):
        return None
    thing = subject(memory)
    if not thing or set(words(thing)) & WHO:
        return None
    item = None
    already = None
    looked = 0
    fallback = None
    money = bool(set(words(line)) & MONEY)
    for candidate in _fills_from_the_things(line, understood, thing, memory):
        looked += 1
        if looked > LIKE_LOOKUPS:
            break
        found = _entry(candidate)
        if found is None:
            continue
        if already is None:
            already = _entry(topic_text(memory))
        if already is not None and found.key == already.key:
            continue
        if money and not (_key_words_of(found) & MONEY):
            if fallback is None:
                fallback = (candidate, found)
            continue
        filled, item = candidate, found
        break
    if item is None and fallback is not None:
        filled, item = fallback
    if item is None:
        return None
    reading = dict(understood)
    reading["clean"] = " ".join(filled.lower().split())
    reading["words"] = words(reading["clean"])
    if "norm_text" in reading:
        reading["norm_text"] = reading["clean"]
    return reading


LIKE_LOOKUPS = 4


LIMIT_ASK = re.compile(
    r"\bhow (?:much|many)\b[^?.!]{0,24}?\btoo (?:much|many)\b|"
    r"\b(?:is|are|was) (?:it|that|this|they|these) too (?:much|many)\b", re.I)
THE_LIMIT_ITSELF = frozenset("""how much many is are was it that this they these too day days week
    weeks time of should shall i we you a an the have be can per""".split())
THE_LIMIT = ("how much {thing} is too much", "how much {thing} a day is too much",
             "{thing} limit")


def the_limit_of_the_thing(understood, memory):
    if not isinstance(understood, dict) or not isinstance(memory, dict) or not memory:
        return None
    line = str(understood.get("clean") or understood.get("text") or "").strip()
    if not line or not LIMIT_ASK.search(line):
        return None
    if [word for word in words(line) if word not in THE_LIMIT_ITSELF and word not in STOPWORDS]:
        return None
    if isinstance(memory.get("person"), dict) and memory.get("person"):
        return None
    thing = subject(memory)
    if not thing or set(words(thing)) & WHO:
        return None
    already = _entry(topic_text(memory))
    seen = set()
    for candidate in _the_limit_written_out(line, thing, memory):
        if candidate in seen:
            continue
        seen.add(candidate)
        if len(seen) > LIKE_LOOKUPS:
            break
        found = _entry(candidate)
        if found is None:
            continue
        keyed = _key_words_of(found)
        if not (keyed & {"limit", "limits", "safe"}):
            continue
        if already is not None and found.key == already.key:
            continue
        reading = dict(understood)
        reading["clean"] = candidate
        reading["words"] = words(candidate)
        if "norm_text" in reading:
            reading["norm_text"] = candidate
        return reading
    return None


def _the_limit_written_out(line, thing, memory):
    whole = " ".join(str(thing or "").split())
    named = [word for word in whole.split() if not _a_doing_word(word)]
    parts = named + [whole] + [word for word in whole.split() if word not in named]
    try:
        key = key_subject(line, memory)
    except Exception:
        key = []
    for word in key or ():
        if isinstance(word, str) and word.strip() and word.strip() not in parts:
            parts.append(word.strip())
    for one in parts:
        for said in THE_LIMIT:
            yield said.format(thing=one)


def _a_doing_word(word):
    from ..understanding import kinds
    return word in kinds.VERB_FORMS or word in kinds.VERBISH


def _fills_from_the_things(line, understood, thing, memory):
    seen = set()
    things = [thing]
    try:
        key = key_subject(str(understood.get("clean") or understood.get("text") or ""), memory)
    except Exception:
        key = []
    for word in key or ():
        if isinstance(word, str) and word.strip():
            things.append(word)
    for one in things:
        for ask in _fills(line, one):
            if ask not in seen:
                seen.add(ask)
                yield ask


def _fills(line, thing):
    whole = " ".join(str(thing).split())
    said = WHAT_STANDS_IN.sub(whole, line, count=1)
    if set(words(line)) & MONEY:
        return ["how much does " + whole + " cost", "is " + whole + " expensive"]
    return [said]


HE_OR_SHE_OPENS = re.compile(
    r"^(?P<lead>(?:and |so |but |well |ok |okay |also )?)(?P<pron>he|she)\b(?!')", re.I)


ASKS_HOW_EARLY_THERE = re.compile(
    r"\b(?:how early|how long before|what time (?:should|do|shall|must) i|"
    r"when (?:should|do|shall|must) i)\b", re.I)
A_FLIGHT_IN_THE_TOPIC = re.compile(
    r"\b(?:flight|flights|flying|fly|airport|terminals?|departure|departing|plane|boarding)\b",
    re.I)
THE_AIRPORT = "at the airport"


def the_airport_there_is(understood, memory):
    if not isinstance(understood, dict) or not isinstance(memory, dict):
        return None
    line = str(understood.get("clean") or understood.get("text") or "").strip()
    if not line or "there" not in words(line) or not ASKS_HOW_EARLY_THERE.search(line):
        return None
    trip = topic_text(memory)
    if not trip or not A_FLIGHT_IN_THE_TOPIC.search(trip):
        return None
    filled = re.sub(r"\bthere\b", THE_AIRPORT, line, count=1, flags=re.I)
    if filled == line:
        return None
    found = _entry(filled)
    if found is None:
        return None
    already = _entry(trip)
    if already is not None and found.key == already.key:
        return None
    reading = dict(understood)
    reading["clean"] = " ".join(filled.lower().split())
    reading["words"] = words(reading["clean"])
    if "norm_text" in reading:
        reading["norm_text"] = reading["clean"]
    return reading


def the_animal_the_subject_is(understood, memory):
    if not isinstance(understood, dict) or not isinstance(memory, dict):
        return None
    line = str(understood.get("clean") or understood.get("text") or "").strip()
    if not line or PET_WORD.search(line):
        return None
    opens = HE_OR_SHE_OPENS.match(line)
    if opens is None:
        return None
    ref = understood.get("ref") if isinstance(understood.get("ref"), dict) else {}
    who = str(ref.get("he") or ref.get("she") or "")
    if not who or not PET_WORD.search(who):
        return None
    thing = the_pet_the_line_before_named(memory) or _called(who)
    filled = opens.group("lead") + thing + " " + line[opens.end():].lstrip()
    item = _entry(filled)
    if item is None:
        return None
    if item is _entry(line):
        return None
    kind = thing.split()[-1].lower().rstrip("s")
    keyed = _key_words_of(item)
    if kind not in keyed and kind not in {stem(word) for word in keyed}:
        return None
    reading = dict(understood)
    reading["clean"] = " ".join(filled.lower().split())
    reading["words"] = words(reading["clean"])
    return reading


CHILD_CARE = re.compile(
    r"\b(?:child|children|baby|babies|toddler|toddlers|kid|kids|nursery|nappy|nappies|cot|"
    r"pushchair|highchair|breastfeed\w*|childminder|schoolchild)\b", re.I)


def _the_kind_of_animal(text):
    found = set()
    for word in PET_WORD.findall(str(text or "")):
        word = PET_ONE.get(word.lower(), word.lower()).rstrip("s")
        found.add(BABY_OF.get(word, word))
    return found


def answers_about_another_creature(answer, what_the_line_is):
    said = " ".join(str(answer or "").split()[:60])
    if not said:
        return False
    if CHILD_CARE.search(said):
        return True
    kind = _the_kind_of_animal(what_the_line_is)
    named = _the_kind_of_animal(said)
    return bool(named) and not (kind & named)


def _called(who):
    who = " ".join(str(who or "").strip().lower().split())
    if not who:
        return ""
    return who if who.split()[0] in {"my", "our", "the", "a"} else "my " + who




def _the_pet_the_turns_before_named(memory, back=3):
    thing = the_pet_the_line_before_named(memory)
    if thing:
        return thing
    turns = memory.get("turns") if isinstance(memory.get("turns"), list) else []
    user = memory.get("user") if isinstance(memory.get("user"), dict) else {}
    lines = []
    for turn in reversed(turns):
        said = turn.get("user") if isinstance(turn, dict) else None
        if isinstance(said, str) and said.strip():
            lines.append(said)
        if len(lines) > back:
            break
    for line in lines[1:back + 1]:
        found = the_pet_the_line_before_named({"turns": [{"user": line}], "user": user})
        if found:
            return found
    return ""


def a_detail_of_the_thing_we_hold(understood, memory):
    return bool(_the_kind_the_line_leaves_out(understood, memory))


def _the_kind_the_line_leaves_out(understood, memory):
    if not isinstance(understood, dict) or not isinstance(memory, dict):
        return None
    line = str(understood.get("clean") or understood.get("text") or "").strip()
    if not line or not ASK_CUE.search(line.lower()):
        return None
    if PET_WORD.search(line) or any(phrase in line.lower() for phrase in PROCEED):
        return None
    thing = _the_pet_the_turns_before_named(memory)
    if not thing:
        return None
    kind = thing.split()[-1]
    if kind in words(line):
        return None
    return line, kind


def the_thing_a_detail_belongs_to(understood, memory):
    found = _the_kind_the_line_leaves_out(understood, memory)
    if not found:
        return None
    line, kind = found
    filled = line + " " + kind
    item = _entry(filled)
    if item is None:
        return None
    keyed = _key_words_of(item)
    if kind not in keyed and stem(kind) not in keyed:
        return None
    said = [word for word in words(line)
            if word not in ASK_PART and word not in ASK_ONLY and word not in STAND_IN
            and word not in STOPWORDS]
    trouble = [word for word in said if word not in IMPERATIVE]
    if not _names_it(trouble or said, item):
        return None
    reading = dict(understood)
    reading["clean"] = " ".join(filled.lower().split())
    reading["words"] = words(reading["clean"])
    return reading


def the_pet_the_line_before_named(memory):
    turns = memory.get("turns") if isinstance(memory.get("turns"), list) else []
    before = ""
    for turn in reversed(turns):
        said = turn.get("user") if isinstance(turn, dict) else None
        if isinstance(said, str) and said.strip():
            before = said
            break
    if not before:
        return ""
    named = {}
    for word in PET_WORD.findall(before):
        word = PET_ONE.get(word.lower(), word.lower())
        named.setdefault(BABY_OF.get(word, word), word)
    user = memory.get("user") if isinstance(memory.get("user"), dict) else {}
    babies = set()
    for pet in user.get("pets") or []:
        if not isinstance(pet, dict):
            continue
        kind = str(pet.get("animal") or "").strip().lower().rstrip("s")
        if kind in BABY_OF:
            babies.add(BABY_OF[kind])
    from ..understanding import breeds as _breeds
    for match in _breeds.BREED_RE.finditer(before):
        if not _breeds.a_frame_before(before, match.start()):
            continue
        kind = _breeds.the_kind_of(match.group(0))
        if kind and kind not in babies:
            named.setdefault(kind, kind)
    if not named:
        return ""
    for pet in reversed(user.get("pets") or []):
        if not isinstance(pet, dict):
            continue
        kind = pet.get("animal")
        if not isinstance(kind, str) or not kind.strip():
            continue
        kind = BABY_OF.get(kind.strip().lower().rstrip("s"), kind.strip().lower().rstrip("s"))
        if kind in named:
            return "my " + named[kind]
    return ""


KEEP_IT_UP = re.compile(
    r"\bhow\s+(?:do|can|should|would|could)\s+i\s+"
    r"(?:keep\s+(?:it|this|that)\s*(?:up|going|on)?|"
    r"keep\s+(?:going|on|at\s+it)|"
    r"keep\s+on\s+(?:with\s+)?(?:it|this|that)|"
    r"stick\s+(?:with|at|to)\s+(?:it|this|that)|"
    r"stay\s+(?:with|at)\s+(?:it|this|that))\b", re.I)
STAYING_WITH_IT = "how do i stay motivated"
AN_ACTIVITY = re.compile(
    r"\b(?:i'?m|i am|i'?ve been|i have been|i'?m still|i am still|"
    r"i'?ve started|i have started|i started|i began|i'?ve begun|i have begun|"
    r"i want to|i'?d like to|i'?m trying to|i am trying to|i'?ve been trying to)\s+"
    r"(?:learning|studying|practising|practicing|reading|writing|playing)\b|"
    r"\b(?:i'?m|i am|i'?ve been|i have been|i'?m still|i am still|i started|i'?ve started|"
    r"i began|i want to|i'?d like to|i'?m trying to|i am trying to)\s+"
    r"(?:learn|study|practise|practice|read|write|play)\b", re.I)


def _carrying_on(understood, memory):
    line = str(understood.get("clean") or understood.get("text") or "")
    found = KEEP_IT_UP.search(line)
    if not found:
        return None
    record = carried_topic(memory, line) or {}
    text = str(record.get("text") or "")
    if not text.strip() or not AN_ACTIVITY.search(text):
        return None
    text = (line[:found.start()] + STAYING_WITH_IT + line[found.end():]).strip()
    reading = dict(understood)
    reading["clean"] = " ".join(text.lower().split())
    reading["words"] = words(reading["clean"])
    if "norm_text" in reading:
        reading["norm_text"] = reading["clean"]
    return reading

LIMIT_LINE = re.compile(
    r"^\s*(?:oh\s+|and\s+|also\s+)?(?:no|nope|not|without|skip|minus|except|but\s+no)\b"
    r"\s+(?P<thing>[a-z']{3,20}(?:\s+[a-z']{3,20}){0,2}?)"
    r"\s*(?:though|tho|then|please|for\s+me|thanks|sorry)?\s*[.!]*\s*$", re.I)


def _what_the_turn_took_away(record, memory):
    if not isinstance(record, dict):
        return set()
    said = " ".join(str(record.get("text") or record.get("user") or "").lower().split())
    found = LIMIT_LINE.match(said)
    if not found:
        return set()
    taken = set()
    for word in found.group("thing").split():
        if word in STOPWORDS or len(word) < 3:
            continue
        taken.add(stem(word))
    return taken


def _widened(line, understood, record, memory):
    from .when import asks_what_today_is

    if asks_what_today_is(line):
        return None
    if not isinstance(record, dict):
        return None
    topic_text = str(record.get("text") or "")
    if not topic_text.strip():
        return None
    taken = _what_the_turn_took_away(record, memory)
    if leans_on_topic(understood, memory):
        subject_words = _subject_words_to_carry(record, line, memory)
        if taken:
            subject_words = [word for word in subject_words
                             if stem(str(word).lower()) not in taken]
        if not subject_words or all(word in words(line) for word in subject_words):
            return None
        text = widen(line, subject_words, topic_text)
        if text is not None:
            return text
        return carry_the_ask(line, topic_text)
    return carry_the_ask(line, topic_text)


def _the_length_of_the_aim(understood, memory):
    line = str(understood.get("clean") or understood.get("text") or "")
    if not line:
        return None
    try:
        from . import named

        asked = named.a_goal_measured(line, memory)
    except Exception:
        return None
    if not asked:
        return None
    reading = dict(understood)
    reading["clean"] = asked
    reading["words"] = words(asked)
    if "norm_text" in reading:
        reading["norm_text"] = asked
    return reading

GATHERING_WORDS = frozenset("""barbecue bbq party picnic birthday brunch supper do
gathering get-together potluck housewarming""".split())
TOO_SOON_TO_COOK = re.compile(r"\b(?:tonight|today|this (?:evening|afternoon)|in an hour|in a few hours|"
                              r"right now|already)\b", re.I)
FOR_SOMEBODY = re.compile(
    r"\b(?:kid|kids|child|children|toddler|teen|teens|teenager|teenagers)\b|"
    r"\b\w+[- ]year[- ]old\b|\b\d+\s*(?:st|nd|rd|th)?\s*birthday\b|"
    r"\b(?!\d+\s)(?:for|of) (?:my|his|her|our|a|an)\s+(?:mum|mom|dad|father|mother|son|daughter|"
    r"wife|husband|partner|friend|sister|brother|nan|nana|gran|granny|grandma|grandad|grandpa|"
    r"colleague|boss|niece|nephew|cousin|aunt|uncle|godson|goddaughter)\b", re.I)
PUTTING_ON = re.compile(r"\b(?:we|i)(?:'?re| are| am|'?m)?\s+"
                        r"(?:having|doing|throwing|hosting|planning|organising|organizing|"
                        r"holding|arranging)\b")


def _a_gathering_read_as_the_food(understood, line, memory):
    if not isinstance(understood, dict):
        return None
    if understood.get("kind") != "statement" or understood.get("asks"):
        return None
    said = set(words(line))
    gathering = said & GATHERING_WORDS
    if not gathering or not PUTTING_ON.search(line):
        return None
    if _entry(line) is not None:
        return None
    if TOO_SOON_TO_COOK.search(line):
        return None
    if FOR_SOMEBODY.search(line):
        return None
    for candidate in [" ".join(sorted(gathering)) + " food", "party food"]:
        if _entry(candidate) is not None:
            return candidate
    return None


def _the_whole_topic(line, record_text, memory=None):
    if not _leads_a_question(line):
        return None
    best, best_score = None, -1
    for said in _the_things_the_chat_named(record_text, memory, line):
        widened = str(line) + " " + said
        reached = _entry(widened)
        if reached is None:
            continue
        last = (memory or {}).get("last_answer")
        if isinstance(last, dict) and last.get("id") == getattr(reached, "id", None):
            continue
        if _already_answered_here(reached, memory):
            continue
        if not _the_answer_is_about_what_the_line_names(reached, line):
            continue
        score = _how_much_of_the_thing_the_entry_uses(reached, said)
        if score > best_score:
            best, best_score = widened, score
    return best


ASK_SHAPE_WORDS = frozenset("""
start starts started starting begin begins beginning beginning first next thing things step
steps part parts bit bits way ways point best better good useful help advice tip tips
""".split())


def _the_answer_is_about_what_the_line_names(entry, line):
    asked = [word for word in keywords(line) if len(word) > 3]
    if not asked:
        return True
    named = [word for word in asked if word not in ASK_SHAPE_WORDS]
    if not named:
        return False
    said = words(str(getattr(entry, "reply", "") or ""))
    return any(alike(word, token) for word in named for token in said)


def _already_answered_here(entry, memory):
    reply = str(getattr(entry, "reply", "") or "").strip()
    if not reply:
        return False
    opening = " ".join(reply.lower().split()[:8])
    for turn in (memory or {}).get("turns") or []:
        if not isinstance(turn, dict):
            continue
        said = " ".join(str(turn.get("bot") or "").lower().split())
        if said and said.startswith(opening):
            return True
    return False


def _how_much_of_the_thing_the_entry_uses(entry, said):
    keyed = _key_words_of(entry)
    return len([word for word in keywords(said)
                if len(word) > 2 and any(alike(word, key) for key in keyed)])


def _the_things_the_chat_named(record_text, memory, line=""):
    seen = []
    texts = [str(record_text or "")]
    if _leads_a_question(line):
        for record in reversed(list((memory or {}).get("topics") or [])[-4:]):
            if isinstance(record, dict):
                texts.append(str(record.get("text") or ""))
    for text in texts:
        said = " ".join(text.lower().split())
        if not said or len(said.split()) > 12:
            continue
        if " ".join(words(said)) in seen:
            continue
        seen.append(" ".join(words(said)))
        yield said


def followup_reading(understood, memory):
    if not isinstance(understood, dict):
        return understood
    carrying_on = _carrying_on(understood, memory)
    if carrying_on is not None:
        return carrying_on
    slot = next_slot_reading(understood, memory)
    if slot is not None:
        return slot
    if _after_an_emergency(memory):
        return understood
    if _after_a_correction(memory):
        return understood
    aim_length = _the_length_of_the_aim(understood, memory)
    if aim_length is not None:
        return aim_length
    filled_in = the_pronoun_written_as_what_it_stands_for(understood, memory)
    if filled_in is not None:
        return filled_in
    pointed = the_thing_it_is(understood, memory)
    if pointed is not None:
        return pointed
    prognosis = the_prognosis_the_line_asks(understood, memory)
    if prognosis is not None:
        return prognosis
    property_ask = the_property_of_the_thing(understood, memory)
    if property_ask is not None:
        return property_ask
    animal = the_animal_the_subject_is(understood, memory)
    if animal is not None:
        return animal
    airport = the_airport_there_is(understood, memory)
    if airport is not None:
        return airport
    limit_ask = the_limit_of_the_thing(understood, memory)
    if limit_ask is not None:
        return limit_ask
    line = without_the_shrug(str(understood.get("clean") or understood.get("text") or ""))
    gathering = _a_gathering_read_as_the_food(understood, line, memory)
    if gathering is not None:
        reading = dict(understood)
        reading["clean"] = gathering
        reading["words"] = words(gathering)
        if "norm_text" in reading:
            reading["norm_text"] = gathering
        return reading
    period = the_period_they_ask_about(understood, memory)
    if period is not None:
        reading = dict(understood)
        reading["clean"] = period
        reading["words"] = words(period)
        if "norm_text" in reading:
            reading["norm_text"] = period
        return reading
    meal = meal_follow_up(understood, memory)
    if meal is not None:
        return meal
    trip = the_weather_of_the_trip(understood, memory)
    if trip is not None:
        reading = dict(understood)
        reading["clean"] = trip
        reading["words"] = words(trip)
        if "norm_text" in reading:
            reading["norm_text"] = trip
        return reading
    record = carried_topic(memory, line)
    if record is None or left_for_a_blank(memory, line):
        return understood
    same_ask = how_much_of_the_thing_in_hand(line, memory)
    if same_ask:
        reading = dict(understood)
        reading["clean"] = same_ask
        reading["words"] = words(same_ask)
        if "norm_text" in reading:
            reading["norm_text"] = same_ask
        return reading
    brought = the_thing_the_subject_brings(understood, memory)
    if brought is not None:
        reading = dict(understood)
        reading["clean"] = brought
        reading["words"] = words(brought)
        if "norm_text" in reading:
            reading["norm_text"] = brought
        return reading
    if elided_ask(line):
        situated = carry_the_ask(line, str(record.get("text") or ""), understood, memory)
        if situated is not None:
            reading = dict(understood)
            reading["clean"] = " ".join(str(situated).lower().split())
    leaning = _the_turn_we_lean_on(understood, memory)
    if leaning is not None and _said_later_than(leaning, record):
        newer = _widened(line, understood, leaning, memory)
        if newer is not None:
            reading = dict(understood)
            reading["clean"] = " ".join(str(newer).lower().split())
            reading["words"] = words(reading["clean"])
            if "norm_text" in reading:
                reading["norm_text"] = reading["clean"]
            return reading
    if understood.get("intent") == "correction":
        text = str((record or {}).get("text") or "")
        if not text.strip() or " ".join(words(text)) == " ".join(words(line)):
            return understood
    elif bare_question(understood, memory) and carry_the_ask(
            line, str(record.get("text") or ""), understood, memory) is None:
        extra = []
        not_doing = _what_they_are_not_doing(record.get("text") or "")
        for word in _subject_words_to_carry(record, line, memory):
            if word in not_doing:
                continue
            if _how_they_feel(word):
                continue
            if word not in words(line) and word not in extra:
                extra.append(word)
        if not extra:
            return understood
        widened = line + " " + " ".join(extra)
        found = _entry(widened)
        if found is None:
            said_whole = " ".join(str(record.get("text") or "").split() + [line])
            item = _entry(said_whole)
            if item is None or not any(_keyed_to(_key_words_of(item), word) for word in extra):
                return understood
            text = said_whole
        else:
            text = widened
    elif not _still_the_topic(record, memory):
        return understood
    elif leans_on_topic(understood, memory):
        subject_words = _subject_words_to_carry(record, line, memory)
        if not subject_words or all(word in words(line) for word in subject_words):
            return understood
        text = widen(line, subject_words, str(record.get("text") or ""))
        if text is None:
            text = carry_the_ask(line, str(record.get("text") or ""), understood, memory)
        if text is None:
            text = _constrains_the_ask(line, str(record.get("text") or ""))
        if text is None:
            text = _the_whole_topic(line, str(record.get("text") or ""), memory)
        if text is None:
            return understood
    else:
        text = carry_the_ask(line, str(record.get("text") or ""), understood, memory)
        if text is None:
            text = _constrains_the_ask(line, str(record.get("text") or ""))
        if text is None:
            text = _the_whole_topic(line, str(record.get("text") or ""), memory)
        if text is None:
            return understood
    reading = dict(understood)
    reading["clean"] = " ".join(str(text).lower().split())
    reading["words"] = words(reading["clean"])
    if "norm_text" in reading:
        reading["norm_text"] = reading["clean"]
    return reading


WORDS_THIS_TURN = "words_this_turn"
TURN_TOPIC = "topic_this_turn"


def note(memory, text, kind=None):
    _the_step_back_is_undone(memory)
    before = _the_words_before_the_turn(memory)
    previous = current(memory)
    record = _note(memory, text, kind)
    _the_words_this_turn(memory, before, record, previous)
    return record


def _the_reply_to_the_turn_before(memory):
    for turn in reversed(list(memory.get("turns") or ())):
        if isinstance(turn, dict) and turn.get("bot"):
            return str(turn.get("bot") or "")
    return ""


def _the_step_back_is_undone(memory):
    if not (WORDS_THIS_TURN in memory or TURN_TOPIC in memory):
        return None
    said = _the_reply_to_the_turn_before(memory)
    if not said:
        memory.pop(WORDS_THIS_TURN, None)
        memory.pop(TURN_TOPIC, None)
        return None
    return the_step_back_takes_its_words_back(memory, said)


def _the_words_before_the_turn(memory):
    held = {}
    for record in _the_records(memory):
        held[str(record.get("text") or "")] = list(record.get("words") or ())
    return held


def _the_records(memory):
    for record in [memory.get("topic")] + list(memory.get("topics") or ()):
        if isinstance(record, dict):
            yield record


def _the_words_this_turn(memory, before, record, previous):
    memory.pop(WORDS_THIS_TURN, None)
    memory.pop(TURN_TOPIC, None)
    if not isinstance(record, dict):
        return
    said = str(record.get("text") or "")
    added = [word for word in (record.get("words") or ()) if word not in before.get(said, ())]
    if added:
        memory[WORDS_THIS_TURN] = {"text": said, "words": added}
    memory[TURN_TOPIC] = {"text": said, "of": str(record.get("of") or ""),
                          "was": str(previous.get("text") or "") if isinstance(previous, dict) else ""}


def _a_step_back(reply):
    from ..compose import fallback
    try:
        return bool(fallback.is_a_hedge(str(reply or "").strip()))
    except Exception:
        return False


def _the_detail_steps_back(memory, reply):
    noted = memory.pop(TURN_TOPIC, None)
    if not isinstance(noted, dict) or not _a_step_back(reply):
        return None
    back = str(noted.get("of") or "") or str(noted.get("was") or "")
    if not back or back == str(noted.get("text") or ""):
        return None
    record = current(memory)
    if not isinstance(record, dict) or str(record.get("text") or "") != str(noted.get("text") or ""):
        return None
    older = None
    for kept in (memory.get("topics") or ()):
        if isinstance(kept, dict) and str(kept.get("text") or "") == back:
            older = kept
    if not isinstance(older, dict):
        return None
    said = dict(older)
    memory["topic"] = said
    topics = memory.get("topics")
    if isinstance(topics, list):
        topics[:] = [other for other in topics if other is not older
                     and str((other or {}).get("text") or "") != back]
        topics.append(said)
    return said


def the_step_back_takes_its_words_back(memory, reply):
    _the_detail_steps_back(memory, reply)
    noted = memory.pop(WORDS_THIS_TURN, None)
    if not isinstance(noted, dict) or not _a_step_back(reply):
        return None
    words = list(noted.get("words") or ())
    if not words:
        return None
    took_back = None
    for kept in _the_records(memory):
        if str(kept.get("text") or "") != str(noted.get("text") or ""):
            continue
        kept["words"] = [word for word in (kept.get("words") or ()) if word not in words]
        took_back = kept["words"]
    return took_back
