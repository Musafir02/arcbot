import re

from ..understanding import breeds as breed_words
from .topics import words

SCAFFOLD = frozenset("""
what whats which who whom whose how when whens where why whether that this these those it its
was were is are am be been being do does did done doing have has had having
you u ya i im ive id ill me my mine our ours we us your yours dont doesnt didnt isnt wasnt
arent wont cant couldnt wouldnt
again also still yet now then just only even ever before already first last next other
remember recall forget forgot know knew knews say said saying says tell told telling remind
else more again
please pls can could would will shall may might should must about of for to in at on
with by any anything something everything one ones thing things much many more most
the a an and or but so or right ok okay fine really actually honestly anyway well oh ah hmm
call called calls calling
you u ur your yours youve youre youd youll i me my mine we us our ours ya chat chats
conversation talk
up
got get gets getting gotten
give gimme hand
far
myself yourself yourselves ourselves themselves itself himself herself
""".split())

REMEMBERING = re.compile(r"^(?:remind|rememb|forget|forgot|know|knew|kno|say|said|say|tell|"
                         r"told|recall|summar|recap|remind|mention|"
                         r"learn|learnt|learned|studied|picked)", re.I)

KNOWING = re.compile(r"\b(?:know|knew|knows|knowing|remember|remembers|remembered|recall|"
                     r"recalls|summar(?:y|ise|ize)|recap|learn|learns|learned|learnt|"
                     r"learning|studied|pick|picks|picked|picking)\b", re.I)

LEAD = re.compile(
    r"^\s*(?:(?:ok|okay|k|kk|right|so|and|but|oh|ah|well|thanks|thank you|thx|ty|cheers|ta|hi|"
    r"hello|hey|morning|yes|yeah|yep|no|nah|great|cool|nice|perfect|brilliant|lovely|good|sure|"
    r"hmm|sorry|got it|i see|fair enough|makes sense)[\s,.!?;:—-]+)+", re.I)

RETURNING = re.compile(
    r"^\s*(?:(?:and\s+)?(?:back|going\s+back|coming\s+back|returning)\s+to\s+"
    r"(?:the|my|our|that|this|your)\s+[a-z'’-]+|(?:about|on|re|regarding|for)\s+"
    r"(?:the|my|our|that|this|your)\s+[a-z'’-]+|the\s+[a-z'’-]+|(?:anyway|also|oh\s+and|and\s+also|"
    r"separate\s+thing)\b)[\s,.!?;:—-]*", re.I)

SUBJECTS = (
    ("allergy", ("allergic", "allergy", "allergies", "intolerant", "intolerance", "avoid",
                 "avoided", "avoiding")),
    ("budget", ("budget", "spend", "spending", "spent", "afford", "cost")),
    ("diet", ("diet", "diets", "dieting", "vegan", "vegetarian", "vegetarian", "pescatarian",
              "keto", "paleo")),
    ("pet", ("pet", "pets", "dog", "dogs", "cat", "cats", "puppy", "kitten", "rabbit", "hamster",
             "budgie", "parrot", "horse")),
    ("birthday", ("birthday", "birthdays", "bday", "dob", "birthdate")),
    ("weight", ("weigh", "weighs", "weight", "weights", "kilos", "kilo", "stone", "pounds",
                "heavy")),
    ("height", ("height", "tall", "taller", "tallest", "centimetres", "centimetres", "cm")),
    ("name", ("name", "named", "nickname")),
    ("city", ("live", "lives", "living", "lived", "home", "based", "address", "resident")),
    ("job", ("job", "jobs", "work", "works", "worked", "role", "career", "profession",
             "employer", "employed")),
)

LIMIT_WORDS = frozenset("""
eat eats eating eaten have has having drink drinks drinking food foods meal meals
breakfast lunch dinner tea supper snack snacks pudding dessert anything else starchy sugary
avoid avoiding allowed ok okay safe should shouldnt shouldn not no though tho then
cant cannot dont doesnt didn could couldnt mustnt shouldn would wouldnt anymore
""".split())
LIMIT = re.compile(
    r"\b(?:can't|cant|can not|cannot|don't|dont|do not|shouldn't|shouldnt|mustn't|mustnt|never|"
    r"not|avoid|avoiding|no)\b[^?.!]{0,24}?"
    r"\b(?:eat|eats|eating|have|has|having|drink|drinks|drinking|food|foods)\b"
    r"|\b(?:eat|eats|eating|drink|drinks|drinking|food|foods)\b[^?.!]{0,24}?"
    r"\b(?:can't|cant|cannot|not|shouldn't|shouldnt|avoid|avoiding)\b"
    r"|\bwhat (?:should|shall|must|do) i (?:avoid|stay away from|keep away from)\b", re.I)

PEOPLE = frozenset("""
daughter daughters son sons kid kids child children baby toddler boy girl family wife husband
partner mum mom mother dad father parent parents sister brother flatmate housemate friend
friends neighbour colleague boss
""".split())

RECALL_MODIFIERS = frozenset(("new", "old", "older", "current", "previous", "former"))
HOW_OLD = re.compile(r"\bhow old\b", re.I)

ME = re.compile(
    r"\babout me\b|\bof me\b|\bwhat have i (?:told|said|mentioned)\b|\bhave i (?:told|mentioned)\b|"
    r"\bdid i (?:tell|say|mention)\b|\bsummar(?:y|ise|ize)\b|\brecap\b|\brun me through\b"
    r"|\bwhat do you remember about (?:it|that|this)\s*\??$", re.I)

HOW_KNOW = re.compile(
    r"\bhow (?:do|does|did|would|will|can|could|should|might) (?:i|you|we) (?:\w+ly )?"
    r"(?:know|tell)\b", re.I)

WHY = re.compile(r"\bwhy\b", re.I)

ADVICE = re.compile(r"\bshould\b|\bshall\b", re.I)
KEEPING_TRACK = re.compile(
    r"\bhow\s+(?:do|can|could|should|would|to)\s+(?:i|you|we|u)?\s*"
    r"(?:remember|keep\s+track|track|stop\s+forgetting|never\s+forget)\b"
    r"|\b(?:tips?|advice|ways?|tricks?|trick)\b[^.?!]{0,30}?\b(?:remember|remembering|"
    r"keep\s+track)\b"
    r"|\bbest\s+way\s+to\s+remember\b|\bis\s+there\s+a\s+way\s+to\s+remember\b"
    r"|\bhow\s+to\s+remember\b", re.I)
SAY_NOW = re.compile(
    r"\bwhat (?:do|can|could|would|will) (?:i|we) (?:say|tell)\b", re.I)
_ACTION = (r"do|use|try|make|clean|cook|get|put|keep|fix|buy|say|start|stop|avoid|wear|take|"
           r"give|move|store|wash|paint|grow|sort|plan|change|improve|prevent|protect|choose|"
           r"pick|find|save|spend|eat|drink|add|remove|repair|replace|help")
ACTION_ASK = re.compile(
    r"\b(?:what|how|anything|something|where|is there)\b[^?]{0,60}?"
    r"\b(?:i|we)\s+(?:can|could|should|shall|would|will)\s+(?:" + _ACTION + r")\b"
    r"|\b(?:what|how|anything|something)\b[^?]{0,60}?"
    r"\b(?:can|could|should|shall|would|will)\s+(?:i|we)\s+(?:" + _ACTION + r")\b", re.I)
RECALLING = re.compile(r"\b(?:again|remind|reminds|remember|recall|was|were|did|said|told|knew)\b", re.I)
WORLD_SUBJECT = re.compile(
    r"^(?:will|would|can|could|may|might|should|shall|is|are|does|do)\s+"
    r"(?:a|an|the|my|our|your|this|that|these|those|any|one|two|both)\s+\S+", re.I)
DECIDING = re.compile(
    r"\b(?:can|could|should|shall|may|might|would)\s+(?:we|i|you)\s+(?:still\s+)?"
    r"(?:get|have|keep|adopt|buy|rescue|own|afford|take on)\b"
    r"(?=\s+(?!(?:it|that|this|one|ones|them|those|these|more|anything)\b)\S)"
    r"|\bare\s+(?:we|you|i)\s+(?:allowed|able)\s+to\b"
    r"|\bis it (?:ok|okay|fine|wise|allowed)\s+to\b", re.I)
DECIDED_ABOUT = ("pet", "budget")
PERSONAL = ("name", "job", "city", "allergy", "budget", "diet", "birthday", "weight", "height")

USER = re.compile(r"\b(?:my|mine|i|i'm|im|i've|ive|i'd|id|i'll|ill|me|we|our|ours|us)\b", re.I)

KNOWN_OBJECT = re.compile(r"\b(?:me|my|mine|myself)\b", re.I)

CALL_NAME = re.compile(
    r"\bwhat (?:am i|was i|do you|did you|would you) call(?:ed)?\b|\bcall me\b|"
    r"\bi(?:'m| am| was)\s+called\b", re.I)

CALL_A_THING = re.compile(r"\bcall(?:ed)?\s+(?:a|an)\s+[a-z]", re.I)
A_PERSON_BY_WHAT_THEY_DO = re.compile(
    r"\bcall(?:ed)?\s+(?:a|an)?\s*(?:person|people|man|woman|boy|girl|child|kid|someone|"
    r"somebody|thing|one|guy|bloke|lady)\s+(?:who|that|which|whose)\b", re.I)
A_PERSON = re.compile(
    r"\bcall(?:ed)?\s+(?:a|an)\s+(?:person|people|man|woman|boy|girl|child|kid|someone|"
    r"somebody|thing|one|guy|bloke|lady)\b", re.I)


def asks_for_a_word(line):
    line = line or ""
    return bool(CALL_A_THING.search(line)) and not (
        A_PERSON.search(line) or A_PERSON_BY_WHAT_THEY_DO.search(line))


DRIVE_ASK = re.compile(
    r"\bwhat (?:do|did|am) i driv(?:e|ing)\b|\bwhich car\b|\bwhat car\b|"
    r"\bwhat (?:kind|make|model) of car\b|\bwhat(?:'s|s| is| was) my (?:car|van)\b", re.I)

AVOID = re.compile(r"\b(?:have|has|had|need|needs|needed|got|ought) to avoid\b", re.I)

HOW_TO_TELL = re.compile(
    r"\bhow (?:do|can|should|would|could|will|might) (?:i|we|you) "
    r"(?:know|tell|check|spot|see|notice|work out|find out|make sure)\b", re.I)
TELLS_APART = re.compile(
    r"\b(?:when|if|whether|that)\b|\b(?:is|are|am)\s+(?:\w+\s+){0,2}?"
    r"(?:enough|ok|okay|happy|sad|ill|sick|unwell|in pain|ready|too|allergic|missing|done|safe|off)\b"
    r"|\benough\b", re.I)

SPENT_ON_A_THING = re.compile(r"\b(?:on|for)\s+\S.*$", re.I)
SPENDING = re.compile(r"\b(?:spent|paid)\b|\b(?:did|have|has|had)\s+(?:i|we)\s+(?:spend|pay)\b",
                       re.I)

LIVING = re.compile(r"\bfor a living\b|\bdo(?:es)? for a job\b", re.I)

EMPLOYER_WORDS = frozenset(("employer", "employers", "employed", "employment"))
WANTS_THE_FACT = re.compile(
    r"\b(?:what|which|who|whom|whose|where|when|how|why)\b|\bremind|\bremember|\bknow\b|"
    r"\btell me\b|\bsay again\b", re.I)

TIME_WORDS = frozenset("""
week weeks weekend weekends month months year years day days today tonight tomorrow yesterday
morning mornings afternoon afternoons evening evenings night nights midnight noon
minute minutes hour hours second seconds ago fortnight fortnightly daily weekly monthly yearly
monday tuesday wednesday thursday friday saturday sunday
january february march april may june july august september october november december
earlier lately recently sometime once
""".split())

QUESTION_START = frozenset("""
what what's whats which who whom whose how when whens where why is are was were am do does did have
has can could would should will remind remember know tell say anything
""".split())


def _key(word):
    if breed_words.the_kind_of(word):
        return "pet"
    for key, names in SUBJECTS:
        if word in names:
            return key
        if len(word) > 4 and any(word.startswith(name[:4]) and name[:4] in ("alle", "budg")
                                 for name in names):
            return key
    return None


OPENS_WITH = re.compile(r"\s*([A-Za-z]+['\u2019][A-Za-z]+)")
SUBJECT_CONTRACTION = frozenset("we i they you he she it that there this these those".split())


def _a_contraction_opens(text):
    found = OPENS_WITH.match(text or "")
    if not found:
        return False
    return found.group(1).lower().replace("\u2019", "'").split("'")[0] in SUBJECT_CONTRACTION


def _asked(text, low):
    if "?" in text:
        return True
    if not low:
        return False
    if low[0] in QUESTION_START and _a_contraction_opens(text):
        return False
    if REMEMBERING.match(low[0]):
        return True
    if " ".join(low[:2]) in ("do you", "did you", "you know", "did i", "do i", "can you"):
        return True
    return low[0] in QUESTION_START


def _asked_them(line):
    low = words(line)
    if not low:
        return False
    if low[0] in ("do", "did", "are", "can", "could", "would", "will") and "you" in low[:2]:
        return False
    return True


def _the_slot(line):
    low = words(line)
    for i, word in enumerate(low):
        if word == "the" and i + 1 < len(low) and _key(low[i + 1]):
            return True
    return False


def _without_the_lead(text):
    line = LEAD.sub("", text).strip(" ,.!?;:-")
    named = None
    for _ in range(3):
        cut = RETURNING.match(line)
        if not cut:
            break
        said = words(cut.group(0))
        if said:
            named = _key(said[-1]) or named
        line = line[cut.end():].strip(" ,.!?;:-")
    return line, named


def ask(text, why=False):
    if not isinstance(text, str):
        return None
    line, returning = _without_the_lead(" ".join(text.split()))
    if not line or len(line.split()) > 12:
        return None
    if WHY.search(line) and not why:
        return None
    if KEEPING_TRACK.search(line):
        return None
    limit = bool(LIMIT.search(line))
    if (ADVICE.search(line) or SAY_NOW.search(line)) and not RECALLING.search(line) and not limit:
        return None
    if (ACTION_ASK.search(line) and not RECALLING.search(line) and not limit
            and not re.search(r"\bhow (?:much|many)\b|\bfor a living\b", line)):
        return None
    how_to = HOW_TO_TELL.search(line)
    if how_to and TELLS_APART.search(line[how_to.end():]):
        return None
    if DRIVE_ASK.search(line):
        return "car"
    spend_tail = SPENT_ON_A_THING.search(line) if SPENDING.search(line) else None
    if spend_tail and line[:spend_tail.start()].strip(" ,."):
        line = line[:spend_tail.start()].strip(" ,.")
    low = words(line)
    if not low or not _asked(line, low):
        return None
    if (CALL_NAME.search(line) and not asks_for_a_word(line)
            and not A_PERSON_BY_WHAT_THEY_DO.search(line)):
        return "name"
    if AVOID.search(line) and USER.search(line):
        return "allergy"
    if re.search(r"\bdate of birth\b|\bbirth date\b", line, re.I):
        return "birthday"
    content = [word for word in low
               if word not in SCAFFOLD and word not in TIME_WORDS and len(word) > 1
               and not REMEMBERING.match(word)]
    if content and not WANTS_THE_FACT.search(line) \
            and all(word in EMPLOYER_WORDS for word in content):
        return None
    if not content:
        if returning:
            return returning
        if limit:
            return "limit"
        if HOW_KNOW.search(line):
            return None
        if ME.search(line):
            return "me"
        if USER.search(line) and _asked_them(line) and KNOWING.search(line) \
                and KNOWN_OBJECT.search(line):
            return "me"
        return None
    if not USER.search(line) and not (RECALLING.search(line) and _the_slot(line)):
        return None
    if LIVING.search(line):
        return "job"
    if any(word in PEOPLE for word in content):
        return None
    if limit and not [word for word in content if word not in LIMIT_WORDS]:
        return "limit"
    modifierless = []
    for at, word in enumerate(content):
        after = content[at + 1] if at + 1 < len(content) else ""
        if (word in RECALL_MODIFIERS and after and _key(after)
                and not (word in ("old", "older") and HOW_OLD.search(line))):
            continue
        modifierless.append(word)
    content = modifierless
    keys = []
    for word in content:
        key = _key(word)
        if not key:
            return None
        keys.append(key)
    if (DECIDING.search(line) and not RECALLING.search(line)
            and any(key in keys for key in DECIDED_ABOUT)):
        return None
    if (WORLD_SUBJECT.match(line) and not RECALLING.search(line)
            and any(key not in PERSONAL for key in keys)):
        return None
    for key, _ in SUBJECTS:
        if key in keys:
            return key
    return None


__all__ = ["ask", "SUBJECTS", "SCAFFOLD", "PEOPLE", "ME", "ADVICE"]


LOOKS_BACK = re.compile(
    r"\b(?:again|remind|reminds|reminded|reminding|remember|remembers|remembered|"
    r"recall|recalls|recalled|forget|forgets|forgot|forgotten)\b"
    r"|\b(?:did|do|does|was|were|am|are|have|has|had)\s+(?:i|we)\b"
    r"|\bwhat\s+(?:was|were)\s+(?:my|our)\b"
    r"|\bwhat(?:'s|s|\s+is)\s+(?:my|our)\b"
    r"|\bhow\s+(?:many|much)\b"
    r"|\b(?:was|were)\s+(?:that|it|they|those|these)\b"
    r"|\b(?:you|u)\s+(?:said|told)\b|\btold\s+me\b"
    r"|\b(?:earlier|before)\b|\bback\s+to\b|\bsame\s+(?:again|one)\b", re.I)

_ASKING_FRAME = frozenset("""
again remind reminds reminded reminding remember remembers remembered recall recalls recalled
forget forgets forgot forgotten me my our us we i you u your yours the a an and or so but
how many much what which who when where why was were is are am do does did done have has had
long far old big tall heavy short wide deep high low often soon much
said say says saying tell told telling earlier before back to same one ones that this it
please pls can could would will about of for in at on with by any anything something thing
""".split())


def looks_back(text):
    if not isinstance(text, str):
        return ""
    found = LOOKS_BACK.search(" ".join(text.lower().split()))
    return found.group(0).strip() if found else ""


def _stems(said):
    from .topics import stem
    return {stem(word) for word in words(said) if word}


def the_earlier_turn(text, memory=None):
    cue = looks_back(text)
    if not cue:
        return None
    thing = " ".join(word for word in words(text) if word not in _ASKING_FRAME)
    want = _stems(thing)
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return None
    if not want:
        said = [str((turn or {}).get("user") or "") for turn in turns[::-1]
                if isinstance(turn, dict) and (turn or {}).get("user")]
        said = said[:3]
        return {"cue": cue, "thing": ask(text) or "", "said": said} if said else None
    everywhere = set()
    for turn in turns:
        if isinstance(turn, dict):
            everywhere |= _stems(str(turn.get("user") or ""))
    unsaid = want - everywhere
    said = []
    for turn in reversed(turns):
        line = str((turn or {}).get("user") or "") if isinstance(turn, dict) else ""
        have = _stems(line) if line else set()
        if len(want & have) >= 2 and (want - have) <= unsaid:
            said.append(line)
        elif line and want <= have:
            said.append(line)
        if len(said) == 3:
            break
    if not said:
        return None
    return {"cue": cue, "thing": thing, "said": said}
