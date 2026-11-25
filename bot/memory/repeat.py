import re

from ..compose import pick
from ..compose.whole import a_whole_cut
from ..understanding import understand
from . import counts, facts, history, limits, narrow, recall, topics

ASK = frozenset("""
    what whats how where when which why who
    do does doing done now next then instead else anything something
    look looking start begin fix sort try use get make buy take stop
    should shall can could would will may might have has had
    i me my we you your it its that this these those there
    the a an again more better please tell say said too as well
    go going work help helps helped helping suggest recommend about at on in with
    first begin beginning step steps change advice tip tips thing things
""".split())

ASK_VERB = frozenset("""
    check checking ask asking bring bringing pick picking choose choosing spend spending
    watch watching expect expecting pack packing book booking
    first next step steps part bit
""".split())

DOINGS = (
    ("make", "makes", "made", "making", "cook", "cooks", "cooked", "cooking", "bake",
     "bakes", "baked", "baking", "prepare", "preparing", "serve", "serving"),
    ("buy", "buys", "buying", "bought", "get", "gets", "getting", "got", "pick", "picks",
     "picking", "choose", "chooses", "choosing", "chose", "shop", "shopping", "spend",
     "spending"),
    ("check", "checks", "checking", "look", "looking", "inspect", "test", "testing",
     "watch", "watching"),
    ("ask", "asks", "asking", "say", "says", "saying", "tell", "telling", "word", "words"),
    ("bring", "bringing", "take", "taking", "pack", "packing", "wear", "wearing"),
    ("try", "tries", "trying", "use", "using", "start", "starting", "begin", "beginning"),
)

WHOLE_OF_IT = frozenset("""
    do does doing done next then else now step steps first also more again
""".split())


def _doings(text):
    words = set(topics.words(text or ""))
    return {i for i, family in enumerate(DOINGS) if words & set(family)}


def asks_for_the_same_work(text, memory):
    if not names_nothing(text):
        return False
    if history.about_the_chat(text):
        return False
    asked = _doings(text)
    if not asked and not (set(topics.words(text or "")) & WHOLE_OF_IT):
        return False
    whole = bool(set(topics.words(text or "")) & WHOLE_OF_IT)
    for back, question, said in _recent_answers(memory):
        if back > 1 and not _about_the_same_thing(question, said, memory):
            continue
        return whole or bool(asked & _doings(question))
    return False


FILLER = frozenset("and so ok okay but well alright right then just maybe perhaps also too "
                   "good best".split())

TIME = frozenset("""tonight today tomorrow morning afternoon evening night later soon week
    weekdays weekend month""".split())

SELF = frozenset("myself yourself himself herself itself oneself ourselves yourselves themselves".split())

QUESTION = re.compile(r"^\s*(?:and\s+|so\s+|ok\s+|okay\s+|but\s+|well\s+|right\s+)*"
                      r"(?:what|whats|how|where|now|next|then)\b", re.I)


RESET_LEAD = re.compile(
    r"^\s*(?:nvm(?:\s+(?:that|this|it))?|never\s*mind(?:\s+(?:that|this|it))?|nevermind|"
    r"forget\s+(?:it|that|this)|ignore\s+(?:it|that|this)|"
    r"scrap\s+(?:it|that|this)|anyway|anyways|new\s+question|different\s+question|"
    r"changing\s+the\s+subject|change\s+of\s+subject)\b[\s,.:;-]*", re.I)


def without_a_reset(text):
    return RESET_LEAD.sub("", (text or "").strip(), count=1)

LOSS_WORDS = frozenset("""dont know idea sure stuck really not even lost help someone
    thought anymore loss at myself""".split())

AT_A_LOSS = re.compile(
    r"^\s*(?:and\s+|so\s+|ok\s+|okay\s+|but\s+|well\s+|right\s+|honestly\s+)*"
    r"(?:i\s+)?(?:really\s+|just\s+)?(?:don'?t|dont|do not|didn'?t|didnt)\s+"
    r"(?:really\s+)?know\s+(?:what|how|where|who|which|when)\s+"
    r"(?:to\b|next\b|else\b|any\s?more\b|first\b)"
    r"|\b(?:(?:have|got)\s+)?no\s+idea\s+(?:what|how|where)\s+to\b"
    r"|\b(?:not\s+sure|stuck|at\s+a\s+loss)\s+(?:what|how|where)\s+to\b", re.I)

ANSWER_MODULES = ("answers", "memory_store")

A_STORE_ANSWER = 120

HEDGE = re.compile(r"\b(?:i'?m not sure|i don'?t know enough|that'?s beyond what i know|"
                   r"a quick search|searching for it|i'?d rather not guess|"
                   r"can'?t call that one|not mine to decide|nothing so far|"
                   r"search should sort you out|tell me what you find|"
                   r"what would be most useful|anything you'?d like a hand with)", re.I)

LEADS = (
    "You've got it: {said}",
    "That's the one: {said}",
    "It's what I said a moment ago: {said}",
    "Same answer: {said}",
    "From just now: {said}",
)

BARE_ASK = re.compile(
    r"^(?:(?:sorry|er|erm|um|uh|oh|ah|ok|okay|and|so|but|wait|hmm|hey)\W+)*"
    r"(?P<word>huh|eh|come again|what was that|what did you say|say what|wha|hm|what|sorry|pardon)"
    r"(?:\s+(?:please|again|then|now|sorry))*\W*$", re.I)
BARE_ASK_NEEDS_A_QUESTION = frozenset("what sorry pardon".split())

SAY_AGAIN_LEADS = (
    "Again: {said}",
    "Sorry, again: {said}",
    "Said again: {said}",
)

TRIED_LEADS = (
    "Then it is worth going a step further: {step}",
    "If that is not shifting it, the next move is this: {step}",
    "Right - then the thing that is left is to go further: {step}",
)

NEXT_STEP_EMERGENCY = re.compile(
    r"\b(?:999|911|112|a&e|accident and emergency|emergency (?:services|department|room)|"
    r"crisis line|116 123|988|samaritans)\b", re.I)
NEXT_STEP = re.compile(r"\b(?:gp|doctor|nurse|pharmacist|chemist|dentist|vet|optician|midwife|"
                       r"health visitor|111|999|911|helpline|a&e|hospital|council|"
                       r"citizens advice|plumber|electrician|engineer|gas safe|mechanic|"
                       r"locksmith|roofer|builder|technician|specialist)\b", re.I)

MOVE_ASK = re.compile(r"\b(?:help|helps|helped|helping|first|start|begin|next|step|steps|"
                      r"change|try|do|advice|tip)\b",
                      re.I)

PUT_RIGHT = re.compile(
    r"\b(?:save|saved|salvage|salvageable|rescue|rescuable|revive|recover|redeem|fix|fixed|"
    r"repair|ruined|wasted|undo|undoable)\b", re.I)
PUT_RIGHT_ASK = re.compile(
    r"^\s*(?:and\s+|so\s+|ok\s+|okay\s+|but\s+|well\s+|right\s+)*"
    r"(?:can|could|can'?t|is|are|will|would|should|does|do|any|anything|is there|any chance)\b",
    re.I)
PUT_RIGHT_WORDS = frozenset("""
    save saved saving salvage salvageable rescue rescuable revive recover recoverable redeem
    fix fixed fixing repair repaired ruined waste wasted undo undoable gone dead done late still
    worth anyway any way ways chance point hope
""".split())

AND_NOW = re.compile(r"^\s*(?:and\s+|so\s+|ok\s+|okay\s+|right\s+)?now(?:\s+then)?[\s?.!]*$",
                     re.I)

PUT_RIGHT_LEADS = (
    "Worth a go: {step}.",
    "Yes, there is something: {step}.",
    "Not too late: {step}.",
    "There is still this: {step}.",
)

USE_WITH = re.compile(r"\b(?:what|anything)\s+(?:can|could|should|do|would)\s+"
                      r"(?:i|you|we)\s+do\s+with\s+(?:that|this|it|them|those)\b", re.I)

NEXT_ASK = re.compile(r"\b(?:what|anything)\s+else\b|\bwhat\s+next\b|\bnext\s+one\b|"
                      r"\bwhat\s+now\b|\bwhat\s+other\b|\band\s+then\b|\band\s+after\s+that\b|"
                      r"\bthen\s+what\b",
                      re.I)

NEXT_LEADS = (
    "Next up: {step}.",
    "The next one: {step}.",
    "Then this: {step}.",
    "After that: {step}.",
)

ALSO_LEADS = (
    "Also in that answer: {step}.",
    "And this: {step}.",
    "It also said this: {step}.",
    "There is this too: {step}.",
)

MOVE_LEADS = (
    "Start with this: {step}.",
    "The thing to do first: {step}.",
    "I would start here: {step}.",
    "The first thing to do: {step}.",
)

STEP_SAYS_FIRST = re.compile(r"^(?:start|begin|first)\b", re.I)
LEAD_SAYS_FIRST = re.compile(r"\b(?:start|begin|first)\b", re.I)
NOW_LEADS = (
    "The one to do now: {step}.",
    "The one I would pick: {step}.",
    "Do this one: {step}.",
)


LOST_LEADS = (
    "Start with this: {step}.",
    "One thing to do first: {step}.",
    "Begin here: {step}.",
    "That's alright. Start with this: {step}.",
)

BE_FORM = frozenset("be been being is are was were am its it's thats that's".split())
POINTING_AT = frozenset("it that this".split())

AGREEING = frozenset("""
ok okay k right yes yeah yep yup got it good cool nice alright oh ah so then just too as well and
but actually honestly really well great perfect thanks cheers course fine sure indeed exactly
""".split())

AGREEMENT_TAIL = frozenset("""
then too well right ok okay yes yeah yep yup both is
""".split())
AGREES_ON_ITS_OWN = frozenset("""
ok okay k right yes yeah yep yup good cool nice alright great perfect thanks cheers course
fine sure indeed exactly
""".split())

AGREES_IN_A_PHRASE = re.compile(
    r"\b(?:got|get|gets|that's|thats|is|was|does|did)\s+(?:it|that|this|you)\b", re.I)

CHANGE_ASK = re.compile(r"\b(?:change|changed|fix|tackle|improve)\b", re.I)
CHANGE_LEADS = (
    "The first thing I would change: {step}.",
    "What I would change first: {step}.",
    "Change this first: {step}.",
)

MORE_LEADS = (
    "Also from that answer: {step}.",
    "Another one from it: {step}.",
    "Worth trying as well: {step}.",
    "There is this one too: {step}.",
)

MOVE_VERBS = (
    "track", "run", "note", "list", "lift", "simmer", "scrub", "wipe", "weigh", "sort",
    "split", "tip", "pour", "stir", "seal", "label", "spray", "blot", "trim", "tie",
    "cap", "dab", "pick", "chip", "sand", "scrape", "air", "dose", "feed", "renew", "fix",
    "swap out", "cut out", "turn off", "shut", "lock", "charge", "defrost", "descale", "dilute",
    "bring", "anchor", "aim", "count", "hold off", "leave out", "cut back", "write down",
    "undo", "unscrew", "screw", "pull", "push", "lift out", "prise", "wiggle", "dry", "brush",
    "vacuum", "mop", "dust", "sweep", "empty", "shake", "tape", "glue", "clamp", "snip",
    "preheat", "grease", "knead", "prove", "dust off", "wash out", "scrub out", "air out",
)

STEP_WORDS = 20
STEP_WITH_ITS_METHOD = 30
CUT_WORDS = 12
SHORT_STEP = 6
NEEDS_COMPLEMENT = frozenset("put place set leave keep wrap cover soak spray apply dip store "
                             "hang lay pour fill seal".split())

QUALIFIER = re.compile(r"\b(?:because|so that|which|if|unless|before|after|until|while|when|"
                       r"once|in case|as long as|rather than)\b", re.I)

LEADING_PHRASE = frozenset("""half quarter each every once twice three two four five one times
    day days week weeks month months year years minute minutes hour hours night nights morning
    mornings evening evenings afternoon per in on at for after before during gently slowly
    carefully lightly quickly easily really also just only about""".split())

AN_ARTICLE = frozenset("a an the".split())

LEADING_PHRASE_MAX = 3


def _the_first_instruction_in_a_long_piece(head, verbs):
    piece = str(head or "").split(",")[0].strip(" ,;:.")
    words = piece.split()
    if len(words) < SHORT_STEP:
        return None
    if words[0].lower() in verbs or _a_verb_after_a_leading_phrase(piece, verbs):
        return piece
    return None


def _a_verb_after_a_leading_phrase(head, verbs):
    tokens = [word.strip(" ,-").lower() for word in str(head or "").split()]
    for at in range(1, min(LEADING_PHRASE_MAX + 1, len(tokens))):
        if tokens[at] not in verbs:
            continue
        phrase = tokens[:at]
        if phrase[0] in AN_ARTICLE:
            continue
        if all(word in LEADING_PHRASE or word in AN_ARTICLE for word in phrase):
            return True
    return False


OPENERS = frozenset("with in into onto inside on at by from to for of under over through".split())

DANGLING = frozenset("is are was were be been being am what that which who whom whose how why "
                     "the a an of to for and or but with in on at by from as it its this these "
                     "those his her their my your our there here than then so if even when while "
                     "because unless until plus yet".split())

PIECE_END = re.compile(r":\s|:|(?<!\d),(?!\d)| - |;| \u2014 ")

NOT_A_STEP = re.compile(r"^(?:tell|let|send|give|show|ask|name)\s+(?:me|us)\b", re.I)
A_MENU = re.compile(r"\b(?:whichever|whatever|whenever|either|any of them)\b", re.I)

SENTENCE = re.compile(r"(?<=[.!?])\s+")
LEAD_SPLIT = re.compile(r"(?<=[.!?;])\s+")
QUOTE_PAIRS = (("\"", "\""), ("\u201c", "\u201d"))
MOST = 240
LEAD_IN = 45

LOOK_BACK = 3
LOOK_BACK_FOR_LESS = 6

ASKS = re.compile(r"^\s*(?:and\s+|so\s+|ok(?:ay)?\s+|but\s+|well\s+|right\s+|also\s+)*"
                  r"(?:is|are|was|were|do|does|did|can|could|should|shall|would|will|"
                  r"have|has|had|am|may|might|must|any|anything|anyone)\b", re.I)

ASKING_THEM = re.compile(r"\btell me\b|\blet me know\b|\bwhat(?:'s| is| have you)\b|"
                         r"\bsay which\b|\bwhat about\b", re.I)




REFER_BACK = re.compile(r"\b(?:the list i gave you|what i said (?:above|a moment ago)|"
                        r"down the list|first, then|i said (?:just )?now|same answer|"
                        r"you'?ve got it|that'?s the one|from just now|my answer above|"
                        r"the rest of what i said|the other things i said|first move|"
                        r"follows from (?:that|it)|comes after it)\b", re.I)


ABOUT_THE_BOT = re.compile(r"\b(?:you|your|you'?re|u|ur)\b", re.I)


WORDS_WANTED = re.compile(r"\b(?:say|tell|write|phrase|word(?:ed|s)?|put\s+it|email|text|message|"
                          r"reply|respond|explain|ask\s+for|apologise)\b", re.I)




ECHO_FRAME = frozenset("""got not right ok okay yes noted good to know remember that thats
    ill i you your youre its it and the a an of in on at for with so then anything like hand
    question theres there here me my""".split())
STALL = re.compile(r"\b(?:say more if it helps|go on|keep going|tell me the rest|"
                   r"i'?m with you|i'?m listening|i'?m here if you want|anything you'?d like a "
                   r"hand with|i'?ll remember that|noted|good to know|i'?ve got that|"
                   r"i'?ll keep that in mind)\b", re.I)


def only_said_it_back(line, said):
    said = str(said or "").strip()
    if not said:
        return False
    low = said.lower()
    spoken = [w for w in topics.words(str(line or ""))
              if w not in topics.STOPWORDS and w not in ECHO_FRAME and len(w) > 1]
    if not spoken:
        return False
    kept = sum(1 for w in spoken if w in low)
    return len(spoken) >= 2 and kept >= max(2, (len(spoken) * 3) // 4)


def _an_echo(turn):
    said = str(turn.get("bot") or "").strip()
    if only_said_it_back(turn.get("user") or "", said):
        return True
    return bool(said) and bool(STALL.search(said.lower()))


def _names_no_topic(turn):
    line = str(turn.get("user") or "")
    if not line.strip():
        return False
    try:
        return not (understand(line, None).get("topics") or [])
    except Exception:
        return False


def _only_echoes_between(memory, back):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    between = turns[len(turns) - back + 1:] if back > 1 else []
    return bool(between) and all(_an_echo(turn) and _names_no_topic(turn) for turn in between)


JUST_A_NOD = re.compile(
    r"^\s*(?:ok|okay|alright|all right|right|fine|good|great|cool|cheers|ta|thanks|nice)"
    r"(?:\s+(?:then|thanks|cheers|mate|ok|okay|so))*[\s.,!?]*$", re.I)

HELP_SHAPE = re.compile(
    r"\b(?:any\s?way|anything|something\s+(?:that|which|to)|is there|are there)\b", re.I)
HELP_ASK_QUESTION_FIRST = re.compile(
    r"\b(?:can|could|should|shall)\s+(?:i|we)\s+do\s+(?:anything|something)\b"
    r"|\bis\s+there\s+(?:anything|something)\s+(?:i|we)\s+"
    r"(?:can|could|should|might|would)\s+do\b", re.I)
NAMED_AFTER_IT = re.compile(r"\b(?:my|our|his|her|their|your|the|a|an)\s+[a-z]")


def _a_help_ask(text):
    line = str(text or "")
    if not HELP_SHAPE.search(line):
        return False
    if HELP_ASK_QUESTION_FIRST.search(line) and not NAMED_AFTER_IT.search(line):
        return True
    if a_more_ask(line):
        return False
    return bool(understand(line).get("help_ask"))


def asks_for_the_move(text):
    line = str(text or "")
    return bool(says_where_to_start(line) or HOW_IT.search(line) or _a_help_ask(line))


def names_nothing(text):
    if JUST_A_NOD.match(text or ""):
        return False
    lost = bool(AT_A_LOSS.search(text or ""))
    help_ask = _a_help_ask(text)
    if not (QUESTION.match((text or "").strip()) or lost or help_ask):
        return False
    if ABOUT_THE_BOT.search(text or ""):
        return False
    if WORDS_WANTED.search(text or ""):
        return False
    if topics.pairing(text or ""):
        return False
    if help_ask:
        return True
    return bool(topics.words(text)) and not _names_a_thing_of_its_own(text)


NOT_A_THING = frozenset((
    "think", "reckon", "want", "suppose", "guess", "even", "actually", "back", "again", "one",
    "ones", "thing", "things", "stuff", "lot", "bit", "kind", "sort", "way", "ways", "time",
    "times", "people", "anyone", "someone", "everything", "anything", "something", "nothing"))


def _names_a_thing_of_its_own(text):
    lost = bool(AT_A_LOSS.search(text or ""))
    said = ASK | ASK_VERB | TIME | FILLER | NOT_A_THING
    if lost:
        said = said | LOSS_WORDS
    return [word for word in topics.words(text or "")
            if len(word) > 2 and word not in said and word not in SELF
            and not word.isdigit() and word not in topics.STOPWORDS]


CONDITION_CLAUSE = re.compile(r"^\s*(?:if|unless|when|whenever|once|in case|should|as long as)\b",
                              re.I)
NOT_A_MOVE = re.compile(
    r"^(?:ask|ring|call|see|phone|speak to|talk to|book|visit|check)\b[^.!?]{0,30}\b"
    r"(?:gp|doctor|doctors|dentist|nurse|pharmacist|chemist|optician|vets?|hospital|ae|"
    r"a&e|plumber|electrician|engineer|specialist)\b", re.I)

STEP_VERBS = frozenset("delete remove clear keep pick choose check replace".split())

ORDER = re.compile(r"\b(?:first|next|then|before|after that)\b", re.I)


def asks_to_put_it_right(text):
    line = str(text or "").strip()
    if not PUT_RIGHT.search(line) or not PUT_RIGHT_ASK.match(line):
        return False
    if topics.pairing(line) or ABOUT_THE_BOT.search(line):
        return False
    words = [w for w in topics.words(line) if w not in ASK and w not in FILLER
             and not w.isdigit() and w not in SELF and w not in PUT_RIGHT_WORDS
             and w not in topics.STOPWORDS]
    return not words


def a_step_of_the_same_answer(text):
    if not ORDER.search(text or "") or not MOVE_ASK.search(text or ""):
        return False
    if topics.pairing(text or "") or ABOUT_THE_BOT.search(text or ""):
        return False
    words = [w for w in topics.words(text) if w not in ASK and w not in FILLER
             and not w.isdigit() and w not in topics.STOPWORDS]
    return bool(words) and set(words) <= STEP_VERBS


def _recent_answers(memory):
    out = []
    seen_a_card = False
    for back, turn in enumerate(reversed((memory.get("turns") or [])[-LOOK_BACK:]), 1):
        if not isinstance(turn, dict):
            break
        if turn.get("module") not in ANSWER_MODULES:
            continue
        said = str(turn.get("bot") or "").strip()
        if not said or HEDGE.search(said) or len(said) < 50:
            continue
        if len(said) < A_STORE_ANSWER and turn.get("module") != "answers":
            continue
        if said.rstrip().endswith("?") or QUESTION.match(said):
            continue
        if topics.about_a_place_they_left_behind(said, memory):
            continue
        out.append((back, str(turn.get("user") or ""), said))
    return out


def _the_answer_about_what_we_are_on(memory, recent):
    here = topics.current(memory)
    mine = {word for word in topics.keywords(str((here or {}).get("text") or ""))}
    mine |= {str(word).lower() for word in ((here or {}).get("words") or ())}
    if not recent or not mine:
        return recent
    if mine & set(topics.keywords(recent[0][1])) or mine & set(topics.keywords(recent[0][2])):
        return recent
    about_it = [item for item in recent if mine & set(topics.keywords(item[1]))]
    return about_it or recent


def _nothing_but_acknowledgements(back, memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if back <= 1 or back > len(turns):
        return True
    for turn in turns[len(turns) - back + 1:]:
        if turn.get("module") == "answers":
            return False
        line = str(turn.get("user") or "")
        if len(line.split()) > 6 and not ATTEMPT.search(line):
            return False
    return True


def _about_the_same_thing(asked, said, memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if turns and HEDGE.search(str(turns[-1].get("bot") or "")):
        return True
    subject = [w for w in topics.words(topics.subject(memory) or "")
               if w not in topics.STOPWORDS]
    if not subject:
        return True
    theirs = {w for w in topics.words(asked) if len(w) > 2 and w not in topics.STOPWORDS}
    mine = {w for w in topics.words(said) if len(w) > 2 and w not in topics.STOPWORDS}
    mine = mine | {w for w in _the_keys_of(said, memory) if len(w) > 2}
    if theirs and not (mine & theirs):
        return False
    broken = set(topics.words(asked)) | set(topics.words(said))
    if broken & set(subject):
        return True
    mine = {w for w in topics.words(said) if len(w) > 2 and w not in topics.STOPWORDS}
    for turn in (memory.get("turns") or [])[-3:]:
        if not isinstance(turn, dict):
            continue
        line = str(turn.get("user") or "")
        if not ATTEMPT.search(line):
            continue
        if len(mine & {w for w in topics.words(line) if len(w) > 2}) >= 2:
            return True
    return False


def _the_chat_is_still_on(said_before, memory):
    topic = memory.get("topic") if isinstance(memory, dict) else None
    now = {w for w in topics.words(str((topic or {}).get("text") or ""))
           if len(w) > 2 and w not in topics.STOPWORDS}
    if not now:
        return True
    then = {w for w in topics.words(said_before) if len(w) > 2 and w not in topics.STOPWORDS}
    return bool(then & now)


def _short(said):
    parts = [p.strip() for p in SENTENCE.split(said.strip()) if p.strip()]
    if not parts:
        return ""
    short = parts[0]
    if len(short) < LEAD_IN and len(parts) > 1:
        short = short + " " + parts[1]
    if len(short) > MOST:
        short = short[:MOST].rsplit(" ", 1)[0].rstrip(",;:") + "..."
    return short


FIRST_THING = re.compile(
    r"^(?P<move>.{4,120}?)\s+is\s+(?:the|your|my)\s+(?:first thing|thing to do first|"
    r"best first (?:step|move)|first (?:step|move)|best (?:step|move)|place to start|"
    r"one thing|fix|change|main thing|thing that helps|bit that helps|part that matters)", re.I)


_WEIGHS_ONE_AGAINST = re.compile(r"\s(?:rather than|instead of)\s", re.I)

_AFTER_A_NOUN = frozenset("at in on from of for to with by near under behind over into about".split())


_SUBJECT_OPEN = re.compile(r"^(?:they|it|it's|its|he|he's|she|she's|this|that|that's|these|those"
                           r"|there|there's|we|we're)\b", re.I)
_EXPLANATION_WORDS = 5


def _explains(sentence):
    text = str(sentence or "").strip()
    if not _SUBJECT_OPEN.match(text):
        return False
    head = re.split(r":|,|;| - | \u2014 ", text, 1)[0]
    return len(head.split()) > _EXPLANATION_WORDS


def _a_step_comes_after(part):
    text = str(part or "")
    for match in _SO_THE_STEP_FOLLOWS.finditer(text):
        if _opens_an_instruction(text[match.end():]):
            return True
    return False


def _opens_an_instruction(text):
    from ..compose.verdict import IMPERATIVES

    words = text.strip(" ,.:;").split()
    return bool(words) and words[0].lower().strip(" ,.;:") in IMPERATIVES


_HANGS = frozenset("and or but then with to of the a an in on at for is are that this".split())

_NEGATES = re.compile(r"^(?:do not|don't|dont|never|avoid)\b", re.I)

_SO_COMES_THE_STEP = re.compile(r"^(?:and\s+|but\s+)?so\b[,\s]+", re.I)
_SO_THE_STEP_FOLLOWS = re.compile(r"[,;]\s*(?:and\s+)?so\b[,\s]+", re.I)
_SO_DOES_NOT_ASK_SOMETHING_OF_THEM = re.compile(
    r"^do(?:es)?\b(?!\s+(?:it|that|this|these|those|them|the|a|an|your|my|his|her|their|our|both"
    r"|one|all|more|less|as|so)\b)", re.I)




def _opening_move(part):
    from ..compose.verdict import IMPERATIVES

    lead = re.split(r"\s+[-\u2014]\s+", str(part).strip())[0]
    if lead.strip() and lead.strip() != str(part).strip() and len(lead.split()) <= 12:
        found = _opening_move(lead)
        if found:
            return found

    leads_with_the_plan = bool(re.match(r"(?:start|begin) with\b", part.strip(), re.I))
    pieces = [part] + part.split(":")
    explaining = _explains(part)
    for index, piece in enumerate(pieces):
        if index and explaining:
            continue
        head = _SO_COMES_THE_STEP.sub("", piece.strip(" ,.:;"))
        if topics.RED_FLAG.match(head):
            continue
        words = head.split()
        if not 3 <= len(words) <= 40:
            continue
        first = words[0].lower().strip(" ,.;:")
        if first != words[0].lower() and not _opens_an_instruction(" ".join(words[1:])) \
                and not _NEGATES.match(" ".join(words[1:])):
            continue
        if first not in IMPERATIVES:
            if not (leads_with_the_plan and index > 1):
                continue
        elif words[1].lower().strip(" ,.;:") in _AFTER_A_NOUN:
            continue
        elif re.match(r"(?:start|begin) with\b", head, re.I) and ":" in part:
            continue
        elif (_WEIGHS_ONE_AGAINST.search(head) and index + 1 < len(pieces)
              and _opens_an_instruction(pieces[index + 1])):
            continue
        head = re.split(r"\s+rather than\b", head)[0].strip(" ,;:-")
        if len(head.split()) < 2 or topics.RED_FLAG.match(head):
            continue
        if ":" not in head and ", then " in head:
            shorter = head.split(", then ")[0].strip(" ,;:-")
            if (3 <= len(shorter.split()) <= 8 and _opens_an_instruction(shorter)
                    and shorter.split()[-1].lower() not in _HANGS):
                head = shorter
        return head[0].lower() + head[1:]
    return None


def _a_question(said):
    text = str(said or "").strip()
    if text.endswith("?"):
        return True
    return bool(QUESTIONS_THAT_ARE_NOT_STEPS.match(text))


def _a_move(said, questions_are_steps=False):
    move = _a_move_in(said, questions_are_steps=questions_are_steps)
    if move and len(move.split()) > STEP_WITH_ITS_METHOD:
        return None
    return move


def _a_move_in(said, questions_are_steps=False):
    parts = [p.strip() for p in SENTENCE.split(str(said).strip()) if p.strip()]
    if parts:
        opening = _opening_move(parts[0])
        if opening and (questions_are_steps or not _a_question(opening)):
            return opening
    for part in reversed(parts):
        if topics.RED_FLAG.match(part):
            continue
        named = FIRST_THING.match(part)
        if named:
            move = named.group("move").strip(" ,;:")
            if (2 <= len(move.split()) <= 20 and not topics.RED_FLAG.match(move)
                    and (questions_are_steps or not _a_question(move))):
                return move[0].lower() + move[1:]
        head = _opening_move(part)
        if (head and not CONDITION_CLAUSE.match(head) and not NOT_A_MOVE.match(head)
                and (questions_are_steps or not _a_question(head))):
            return head

        if _explains(part) and not _a_step_comes_after(part):
            continue

        for piece in [part] + part.split(":"):
            from ..compose.verdict import IMPERATIVES
            clauses = re.split(r"(?<!\d),(?!\d)| - |;| \u2014 |\. ", piece)
            conditional = False
            in_a_bracket = 0
            for clause in clauses:
                head = clause.strip(" .:;")
                if not head:
                    continue
                opened_inside = in_a_bracket > 0
                in_a_bracket = max(0, in_a_bracket + head.count("(") - head.count(")"))
                if opened_inside:
                    continue
                a_conclusion = bool(_SO_COMES_THE_STEP.match(head))
                head = _SO_COMES_THE_STEP.sub("", head)
                if not head:
                    continue
                if head.count("(") != head.count(")"):
                    continue
                if a_conclusion and _SO_DOES_NOT_ASK_SOMETHING_OF_THEM.match(head):
                    continue
                if CONDITION_CLAUSE.match(head):
                    conditional = True
                    continue
                if conditional:
                    continue
                if topics.RED_FLAG.match(head):
                    continue
                if NOT_A_MOVE.match(head):
                    continue
                words = head.split()
                if not 2 <= len(words) <= (STEP_WITH_ITS_METHOD if a_conclusion else 14):
                    continue
                if words[0].lower() not in IMPERATIVES:
                    continue
                if not questions_are_steps and _a_question(head):
                    continue
                break
            else:
                continue
            if re.match(r"(?:start|begin) with\b", head, re.I) and ":" in part:
                continue
            return head[0].lower() + head[1:]

    return None


_A_JUDGEMENT = re.compile(
    r"^\s*(?:when|once|if|as soon as|next time)\b[^,]{0,60}?\b(?:sounds?|feels?|you'?re happy|"
    r"you are happy|you can live with|you'?re ok(?:ay)? with|you are ok(?:ay)? with)\b", re.I)


def _a_conditional_move(said):
    parts = [p.strip() for p in SENTENCE.split(str(said).strip()) if p.strip()]
    for part in parts:
        if topics.RED_FLAG.match(part) or NOT_A_MOVE.match(part):
            continue
        match = CONDITION_CLAUSE.match(part)
        if not match:
            continue
        step = re.split(r"\s+[-\u2014]\s+|\s+\(", part.strip())[0].strip(" ,.;:")
        after = step.split(",", 1)
        rest = (after[1] if len(after) > 1 else step[match.end():]).strip(" ,")
        if not 3 <= len(rest.split()) <= 14:
            continue
        if not _opens_an_instruction(rest):
            continue
        if _A_JUDGEMENT.match(step):
            continue
        if not 4 <= len(step.split()) <= 24:
            continue
        if _explains(step):
            continue
        return step[0].lower() + step[1:]
    return None


def asks_for_more(text):
    if len(re.findall(r"[a-z']+", str(text or "").lower())) > 4:
        return False
    return bool(NEXT_ASK.search(str(text or "")))


def a_hand_back(said, memory):
    wanted = str(said or "").strip().lower()[:60]
    if not wanted:
        return False
    return any(wanted in str(line or "").lower() for line in (memory.get("repeated") or []))


def _handed_back_last(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return False
    return a_hand_back(turns[-1].get("bot"), memory)


def _another_part(said, memory):
    spare = ""
    for part in (p.strip() for p in SENTENCE.split(str(said).strip())):
        part = part.rstrip(" .")
        if len(part.split()) < 4 or len(part) > MOST:
            continue
        if topics.RED_FLAG.match(part) or ASKING_THEM.search(part):
            continue
        if _already_repeated(part, memory):
            continue
        part = re.sub(r"^(?:and\s+|but\s+|so\s+|then\s+|after\s+that,?\s+|next,?\s+)", "",
                      part, flags=re.I)
        part = re.sub(r"^then\s+", "", part, flags=re.I)
        if len(part) > 110:
            head = part.split(": ")[0].strip(" ,;")
            if len(head.split()) >= 4:
                under = [one.strip(" ,;:") for one in re.split(r",\s+", part.split(": ", 1)[1])]
                under = [one for one in under if one]
                if under and _already_repeated(under[0], memory):
                    for clause in under[1:]:
                        if _says_what_to_do(clause) and not _already_repeated(clause, memory):
                            return clause, True
                    continue
                part = head
                if _already_repeated(part, memory):
                    continue
        if _says_what_to_do(part):
            return part, True
        if not spare:
            spare = part
    if spare and not _said_in_a_turn(spare, memory):
        return (spare, False)
    return ("", False)


def _said_in_a_turn(short, memory):
    said = str(short or "").strip()[:60].lower()
    if not said:
        return False
    for turn in memory.get("turns") or []:
        if isinstance(turn, dict) and said in str(turn.get("bot") or "").lower():
            return True
    return False


def _says_what_to_do(part):
    from ..compose.verdict import IMPERATIVES

    words = [w.strip(" ,;:.") for w in str(part).lower().split()]
    orders = bool(re.search(r"\bdo not\b|\bdon'?t\b", str(part), re.I))
    at = next((index for index, word in enumerate(words) if word in IMPERATIVES), None)
    if at is None:
        return orders
    if any(word in ("is", "are", "was", "were", "means", "sounds") for word in words[:at]):
        return orders
    return True


CLAIMS_IT_WAS_SAID = (
    "it's what i said a moment ago",
    "you've got it",
    "that's the one",
    "same answer",
    "from just now",
    "said again",
    "sorry, again",
    "as i said",
    "again",
)


def _said_in_the_chat(said, memory):
    opening = " ".join(" ".join(str(said or "").lower().replace("...", " ").split()).split()[:10])
    if not opening:
        return False
    for turn in memory.get("turns") or []:
        if isinstance(turn, dict) and opening in " ".join(str(turn.get("bot") or "").lower().split()):
            return True
    return False


def _claims_what_it_never_said(reply, memory):
    line = str(reply or "").strip()
    low = line.lower()
    for head in CLAIMS_IT_WAS_SAID:
        if not low.startswith(head):
            continue
        rest = line[len(head):].lstrip(" :-,\u2014").strip()
        if rest and not _said_in_the_chat(rest, memory):
            return rest[:1].upper() + rest[1:]
        return line
    return line


def _handed_back(memory, reply):
    reply = _claims_what_it_never_said(reply, memory)
    kept = memory.get("repeated")
    if not isinstance(kept, list):
        kept = memory["repeated"] = []
    kept.append(reply)
    del kept[:-8]
    return reply


_FRAME_HEADS = []


def _frame_heads():
    if _FRAME_HEADS:
        return _FRAME_HEADS[0]
    heads = set()
    for value in list(globals().values()):
        if not isinstance(value, (tuple, list)):
            continue
        for item in value:
            if not isinstance(item, str):
                continue
            head = item.split("{", 1)[0].strip()
            if "{" in item and head:
                heads.add(head.lower())
    _FRAME_HEADS.append(tuple(sorted(heads, key=len, reverse=True)))
    return _FRAME_HEADS[0]


def framed(said):
    line = (said or "").strip().lower()
    return bool(line) and line.startswith(_frame_heads())


def handed_back(memory, reply):
    return _handed_back(memory, reply)


def _already_repeated(short, memory):
    said = short.strip()[:60].lower()
    if not said:
        return False
    seen = 0
    for turn in memory.get("turns") or []:
        if not isinstance(turn, dict):
            continue
        if said in str(turn.get("bot") or "").lower():
            seen += 1
    for line in memory.get("repeated") or []:
        if said in str(line or "").lower():
            seen += 1
    return seen >= 2


def _handed_back_already(step, memory):
    said = step.strip()[:60].lower()
    if not said:
        return False
    for turn in memory.get("turns") or []:
        if not isinstance(turn, dict):
            continue
        reply = str(turn.get("bot") or "").strip().lower()
        if not reply or said not in reply:
            continue
        if len(said) * 3 >= len(reply):
            return True
    for line in memory.get("repeated") or []:
        if said in str(line or "").lower():
            return True
    return False


LESS = re.compile(
    r"\b(?:make (?:it|that)|keep it|be|say it|put it|give it to me|give me it)\s+"
    r"(?:a bit |a lot |really |much |nice and )?"
    r"(?:short|shorter|brief|briefer|quick|quicker|snappy|concise)\b"
    r"|\b(?:short|shorter|brief|briefly|concisely)\s+please\b"
    r"|\b(?:shorter|tldr|tl;?dr|summarise|summarize|sum it up|sum up|short version|"
    r"cut it down|cut to the chase|get to the point|skip the detail|less detail|"
    r"in (?:a|one) (?:sentence|line)|one line|just the (?:gist|answer|short version))\b"
    r"|\b(?:simpl(?:e|er|ify|ified)|in plain (?:english|terms|words)|plain english|"
    r"(?:in )?simple (?:english|terms|words)|no jargon|jargon[- ]free|layman'?s? ?terms?|"
    r"explain (?:it|that)(?: (?:all )?(?:again|to me))? (?:simply|in english|in simple words)|"
    r"put it (?:simply|plainly|in plain (?:english|words))|dumb (?:it|that)? ?down|"
    r"plainly\b|like (?:i'?m|im|i am) (?:5|five))\b",
    re.I)

LESS_WORDS = frozenset("""make made it that keep be say put give me a bit lot really much
    nice short shorter brief briefer briefly quick quicker snappy concise please tldr tl dr
    summarise summarize sum gist answer version cut chase point skip detail details less
    sentence line one just and so ok okay right then now again too long word words
    more fewer condensed simple simpler simply simplify simplified plain english terms words
    jargon free layman laymans explain plainly like im i'm five 5 dumb dumbed easy easier wordy""".split())

LESS_LEADS = (
    "{short}",
    "Shorter: {short}",
    "In short: {short}",
    "Briefly: {short}",
)

OWN_LEAD = re.compile(r"^[^:!?.\n]{1,45}:\s")
OWN_LEAD_WORDS = 5


def _a_lead_of_its_own(short):
    match = OWN_LEAD.match(str(short or ""))
    return bool(match) and len(match.group(0).split()) <= OWN_LEAD_WORDS


KEEP_CLAUSE = re.compile(
    r"\b(?:but\s+)?(?:keep|keep\s+in|leave\s+in|don'?t\s+(?:leave\s+out|drop|lose)|without\s+"
    r"(?:losing|dropping)|making\s+sure\s+(?:to\s+)?(?:keep|say))\s+(?P<what>.+)$", re.I)
FIGURES = re.compile(r"\b(?:timings?|times?|numbers?|figures?|ratios?|amounts?|quantit(?:y|ies)|"
                     r"temperatures?|degrees?|weights?|measures?|proportions?)\b", re.I)
DIGIT = re.compile(r"[0-9]")


def _kept_clause(text):
    match = KEEP_CLAUSE.search(" ".join(str(text or "").split()))
    return match.group("what").strip(" .!?,") if match else ""


HOW_TO = re.compile(
    r"\bhow\b(?:\s+\w+){0,3}\s+(?:do|can|should|would|could|might|shall)\s+(?:i|we|you)\b",
    re.I)


BREVITY_WORDS = frozenset("""brief briefly short shorter concise concisely tldr gist sentence
    condensed summarise summarize sum version line""".split())


def asks_for_less(text):
    clean = " ".join(str(text or "").split())
    if not clean:
        return False
    if HOW_TO.search(clean):
        return False
    asked = KEEP_CLAUSE.sub("", clean) if KEEP_CLAUSE.search(clean) else clean
    said = topics.words(asked)
    left = [w for w in said
            if w not in LESS_WORDS and w not in FILLER and w not in ASK
            and w not in ASK_VERB and w not in topics.STOPWORDS]
    if left:
        return False
    if not (LESS.search(clean) or any(w in BREVITY_WORDS for w in said)):
        return False
    settled = [w for w in (said or topics.words(clean))
               if w not in FILLER and w not in topics.STOPWORDS]
    return bool(settled) and (settled[-1] in LESS_WORDS or settled[-1] in BREVITY_WORDS)


KEEPING = (
    "Keeping {keep}: {short}",
    "With {keep} in: {short}",
)

ALREADY_SHORT = (
    "That's about as short as it gets: {short}",
    "That is the short version: {short}",
)

NO_SHORTER_STILL = (
    "That is the short version - there is nothing left in it to take out.",
    "Nothing left to cut: every part of that answer you have now had on its own.",
)

NOTHING_TO_CUT = (
    "Nothing to cut down yet - ask me something and I'll keep it short.",
    "Nothing in hand to shorten - ask away and I'll keep it brief.",
)

JUST_THIS = (
    "Just this: {short}",
    "The one thing in it: {short}",
)


WELCOMES = "greeting"


def _recent_lines(memory):
    out = []
    for turn in reversed((memory.get("turns") or [])[-LOOK_BACK_FOR_LESS:]):
        if not isinstance(turn, dict):
            break
        said = str(turn.get("bot") or "").strip()
        if not said or HEDGE.search(said):
            continue
        if turn.get("module") == WELCOMES and not _the_quotation(said):
            continue
        if said in (memory.get("repeated") or []):
            continue
        if len(said.split()) < 6 or said.rstrip().endswith("?"):
            continue
        out.append((len(out) + 1, said))
    return out


SENTENCE_END = re.compile(r"([.!?;][\"\u201d]?)\s+")


def _sentences(said):
    text = str(said or "").strip()
    out, last = [], 0
    for end in SENTENCE_END.finditer(text):
        piece = text[last:end.end()].rstrip()
        if _unbalanced(piece):
            continue
        if piece.strip():
            out.append(piece.strip())
        last = end.end()
    tail = text[last:].strip()
    if tail:
        out.append(tail)
    return out


def _most_condensed(said, memory=None):
    parts = [p.strip().strip(",;:") for p in _sentences(str(said).strip())]
    parts = [p for p in parts if 4 <= len(p.split()) <= 30 and not topics.RED_FLAG.match(p)]
    parts = [p for p in parts if not _already_repeated(p, memory or {})]
    if not parts:
        long_parts = [p.strip().strip(",;:") for p in _sentences(str(said).strip())]
        long_parts = [p for p in long_parts if 4 <= len(p.split()) <= 45
                      and not topics.RED_FLAG.match(p)]
        long_parts = [p for p in long_parts if not _already_repeated(p, memory or {})]
        if long_parts:
            return min(long_parts, key=lambda p: len(p.split()))
    if not parts:
        return ""
    return min(parts, key=lambda p: len(p.split()))


SHORT_ENOUGH = 26
CLAUSE_SPLIT = re.compile(r"(?<=[,;])\s+")
CUT_MID_SENTENCE = frozenset("""and but so or because which that while with rather than to of the
    a an in on for if when as also then it its your my their there""".split())


def _short_enough(cut):
    cut = str(cut or "").strip()
    if len(cut.split()) <= SHORT_ENOUGH:
        return _ended(cut)
    head = _read_up_to_the_colon(cut)
    if len(head.split()) <= SHORT_ENOUGH:
        return _ended(head)
    parts = [p.strip() for p in CLAUSE_SPLIT.split(head) if p.strip()]
    out = ""
    for part in parts:
        together = (out + " " + part).strip()
        if out and len(together.split()) > SHORT_ENOUGH:
            break
        out = together
    words = out.rstrip(",;").split()
    while words and words[-1].lower().strip(",;") in CUT_MID_SENTENCE:
        words = words[:-1]
    out = " ".join(words).rstrip(",;")
    if len(out.split()) < 6:
        return _ended(head)
    return _ended(out)


def _ended(cut):
    cut = str(cut or "").strip().rstrip(",;:")
    if cut[-1:] in ".!?":
        return cut
    if cut[-1:] in "\"\u201d" and cut[-2:-1] in ".!?":
        return cut
    return cut + "."


def _unbalanced(piece):
    said = str(piece or "")
    for opens, closes in QUOTE_PAIRS:
        if opens == closes:
            if said.count(opens) % 2:
                return True
        elif said.count(opens) != said.count(closes):
            return True
    return False


def _the_quotation(said):
    said = str(said or "")
    for opens, closes in QUOTE_PAIRS:
        at = said.find(opens)
        while at != -1:
            end = said.find(closes, at + len(opens))
            if end != -1:
                quote = said[at + len(opens):end].strip()
                if len(quote.split()) >= 4 and len(quote.split()) * 2 >= len(said.split()):
                    return quote
            at = said.find(opens, at + len(opens))
    return ""


def _closing_the_quote(cut, said):
    cut = str(cut or "").strip()
    whole = str(said or "").strip()
    if not cut or not _unbalanced(cut) or cut not in whole:
        return cut
    rest = whole[whole.index(cut) + len(cut):]
    for end in re.finditer(r"[.!?][\"\u201d]?", rest):
        longer = (cut + rest[:end.end()]).strip()
        if not _unbalanced(longer):
            return longer
    return cut


def _read_up_to_the_colon(said):
    head = str(said).partition(":")[0]
    if head != str(said) and 8 <= len(head.split()) < len(str(said).split()):
        return head.strip()
    return str(said)


def _keeps(said, what):
    parts = [p.strip() for p in SENTENCE.split(str(said).strip()) if p.strip()]
    words = set(topics.words(what)) - set(topics.STOPWORDS) - {"timings", "timing", "numbers",
                                                               "figures", "details"}
    named = [p for p in parts if words & set(topics.words(p))]
    if named:
        return max(named, key=len)
    if FIGURES.search(what):
        counted = [p for p in parts if DIGIT.search(p)]
        if counted:
            return counted[0]
    return ""


def shorter_for(text, memory):
    if not isinstance(memory, dict) or not asks_for_less(text):
        return None
    said_any = ""
    for back, said in _recent_lines(memory):
        if back > 2:
            break
        parts = [p.strip().strip(";") for p in _sentences(said)]
        said_any = said_any or said
        lead = parts[0] if len(parts) > 1 else ""
        if lead and len(lead.split()) < 8 and len(parts) > 1:
            lead = parts[1]
        if not lead:
            lead = _read_up_to_the_colon(str(said)).strip()
        kept = _kept_clause(text)
        if kept:
            carry = _keeps(said, kept)
            if carry:
                return _handed_back(memory, pick(KEEPING, memory, text).format(
                    keep=kept, short=carry))
        quote = _the_quotation(said)
        if quote and quote.strip() != str(said).strip() \
                and not _already_repeated(quote, memory):
            return _handed_back(memory, pick(JUST_THIS, memory, text).format(short=quote))
        for pool, cut in ((LESS_LEADS, lead),
                          (JUST_THIS, _most_condensed(said, memory))):
            cut = _closing_the_quote(_short_enough(cut), said)
            if not cut or _unbalanced(cut):
                continue
            if cut.strip().lower() == said.strip().lower():
                continue
            if _already_repeated(cut, memory):
                continue
            line = pick(pool, memory, text)
            if line != "{short}" and _a_lead_of_its_own(cut):
                line = "{short}"
            return _handed_back(memory, line.format(short=cut))
    if not said_any:
        return _handed_back(memory, pick(NOTHING_TO_CUT, memory, text))
    if said_any:
        one = _most_condensed(said_any, memory)
        if one:
            return _handed_back(memory, pick(ALREADY_SHORT, memory, text).format(
                short=_ended(one)))
        return _handed_back(memory, pick(NO_SHORTER_STILL, memory, text))
    return None


A_LENGTH_ASK = re.compile(r"\bhow\s+long\b|\bhow\s+many\s+(?:days|weeks|months|hours|minutes)\b",
                          re.I)
A_BARE_TIME = re.compile(
    r"^\s*(?:about|around|roughly|usually|at least|up to|only|just|no more than)?\s*"
    r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen|twenty|"
    r"thirty|forty|fifty|sixty|ninety|half an?|an?)\s*"
    r"(?:to\s+\w+\s*)?"
    r"(?:minutes?|mins?|hours?|hrs?|days?|weeks?|months?|years?)\b", re.I)


def _a_bare_time(part):
    if not isinstance(part, str):
        return None
    part = " ".join(part.split()).strip()
    if not part or len(part.split()) > 6 or not A_BARE_TIME.match(part):
        return None
    return part[0].upper() + part[1:]


LENGTH_BACK = 3


A_PRICE_ASK = re.compile(
    r"\bhow\s+much\b|\bhow\s+expensive\b|\bwhat\s+(?:does|do|would|will|did)\s+(?:that|it|this)\s+cost"
    r"|\bwhat\s+(?:is|was)\s+the\s+price\b", re.I)

POINTING_BACK = frozenset("that this it those these they them ones one".split())
PRICE_WORDS = frozenset("""
how much many expensive price priced cost costs costing cheap cheaper cheapest usually typical
normally roughly about approximately altogether total altogether pay paying spend spends by for
at a an the per each and so then do does did would will is was are were be be a lot really
here there again any more of on in to get got buy buying round roughly average range
""".split())


def _names_no_thing_of_its_own(text):
    words = topics.words(text or "")
    if not words or not any(word in POINTING_BACK for word in words):
        return False
    return all(word in POINTING_BACK or word in PRICE_WORDS or word in topics.STOPWORDS
               for word in words)


def _the_price_the_answer_gave(text, memory):
    part = _the_price_in_hand(text, memory)
    if not part:
        return None
    if _a_length_already_handed(part, memory):
        return None
    return _handed_back(memory, part)


def asks_what_that_costs(text, memory):
    return bool(_the_price_in_hand(text, memory))


def _the_price_in_hand(text, memory):
    line = str(text or "")
    if not A_PRICE_ASK.search(line) or narrow.kind_of(line) != "money":
        return None
    if not _names_no_thing_of_its_own(line):
        return None
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return None
    last = str(turns[-1].get("bot") or "")
    if not last:
        return None
    found = {" ".join(hit.group(0).lower().split())
             for hit in narrow.SPANS["money"].finditer(last)}
    if len(found) != 1:
        return None
    part = narrow.narrow(last, line)
    if not part or not narrow.SPANS["money"].search(part):
        return None
    part = " ".join(part.split())
    if len(part.split()) > 8:
        return None
    if not part.endswith((".", "!", "?")):
        part += "."
    return part[0].upper() + part[1:]


def _the_time_an_earlier_answer_gave(text, memory):
    said_line = str(text or "")
    if not A_LENGTH_ASK.search(said_line) or narrow.kind_of(said_line) != "time":
        return None
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if len(turns) < 2:
        return None
    last = str(turns[-1].get("bot") or "")
    if last and _a_bare_time(narrow.narrow(last, said_line)):
        return None
    for back, asked, said in _recent_answers(memory):
        if back < 2 or back > LENGTH_BACK or not narrow.SPANS["time"].search(said):
            continue
        if not _about_the_same_thing(asked, said, memory):
            continue
        if not _the_chat_is_still_on(asked + " " + said, memory):
            continue
        part = _a_bare_time(narrow.narrow(said, said_line))
        if part and not _a_length_already_handed(part, memory):
            return _handed_back(memory, part)
    return None


def _a_length_already_handed(part, memory):
    kept = memory.get("repeated")
    if not isinstance(kept, list):
        return False
    flat = " ".join(str(part).lower().split()).strip(" .")
    return any(flat == " ".join(str(said).lower().split()).strip(" .") for said in kept)


def _a_what_to_do_answer(memory):
    from ..knowledge.plans import FREE_TIME
    if not isinstance(memory, dict):
        return False
    answer = memory.get("entry_answer")
    if not isinstance(answer, dict):
        return False
    blocks = {"plan", "plans", "planning", "weekend", "weekends", "bored", "dayoff"}
    for one in FREE_TIME:
        words = [word for word in str(one).lower().split() if len(word) > 3]
        if words and all(word in blocks for word in words):
            blocks.update(words)
    return bool({str(key).lower() for key in (answer.get("keys") or ())} & blocks)


def _a_city_guide_is_the_answer_in_front(memory):
    from ..knowledge import travel
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return False
    return travel.a_city_card_is_in_front(turns[-1].get("bot"))


def answer_for(text, memory):
    from ..compose import limit as limit_line
    if asks_for_the_move(text) and isinstance(memory, dict) \
            and _a_city_guide_is_the_answer_in_front(memory):
        from ..knowledge import travel
        if travel.asks_which_one_first(text):
            return None
    more = asks_for_more(text) and _handed_back_last(memory)
    if USE_WITH.search(str(text or "")) and not _a_what_to_do_answer(memory):
        return None
    if WORDING.search(str(text or "")):
        return None
    time_said = _the_time_an_earlier_answer_gave(text, memory)
    if time_said:
        return time_said
    price_said = _the_price_the_answer_gave(text, memory)
    if price_said:
        return price_said
    put_right = asks_to_put_it_right(text)
    if not (names_nothing(text) or a_step_of_the_same_answer(text)) and not (
            more or says_where_to_start(text) or HOW_IT.search(str(text or ""))
            or a_more_ask(text) or put_right):
        return None
    if IDEAS_ONLY.match(str(text or "")) and _an_entry_answers_it(text, memory):
        return None
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    which_part = asks_for_the_move(text)
    if turns and not which_part and REFER_BACK.search(str(turns[-1].get("bot") or "")):
        return None
    if turns and limit_line.restates_the_answer(str(turns[-1].get("bot") or "")):
        return None
    tried = str(turns[-1].get("user") or "") if turns else ""
    wanted = narrow.kind_of(text)
    for back, asked, said in _the_answer_about_what_we_are_on(memory, _recent_answers(memory)):
        if (back > 1 and not _about_the_same_thing(asked, said, memory)
                and not _only_echoes_between(memory, back)
                and not _nothing_but_acknowledgements(back, memory)):
            continue
        if _a_new_work(text, asked):
            return None
        if wanted is not None and not narrow.carries(said, wanted):
            continue
        nothing_more = False
        if more:
            part, doing = _another_part(said, memory)
            if part:
                leads = NEXT_LEADS if doing else ALSO_LEADS
                return _handed_back(
                    memory, pick(leads, memory, text).format(step=part[:1].upper() + part[1:]))
        if (tried and not QUESTION_MORE.search(tried)
                and (_tried(tried) or _a_step_done(tried, said))):
            later = _later_part(tried, said)
            if later:
                short = _short(later)
                return _handed_back(memory, _a_lead_and_a_step(
                    _a_lead_for(_the_lead_for(text, short), short, memory, text), short))
            if not a_more_ask(text):
                continue
        if a_more_ask(text):
            step = _the_next_step(said, memory)
            if step:
                _wording = step[:1].upper() + step[1:]
                return _handed_back(memory, pick(MORE_LEADS, memory, text).format(step=_wording))
            nothing_more = True
        if asks_for_the_move(text):
            step = _the_first_step(said)
            if step and not _handed_back_already(step, memory) \
                    and not _they_say_they_tried(step, memory):
                _wording = step[:1].upper() + step[1:]
                return _handed_back(memory, _a_lead_and_a_step(
                    _a_lead_for(_leads_for(text), _wording, memory, text), _wording))
        if MOVE_ASK.search(text) or put_right or AND_NOW.match(text or ""):
            step = _a_move(said)
            if step is None and AT_A_LOSS.search(text or ""):
                step = _a_conditional_move(said)
            if step and not _already_repeated(step, memory) \
                    and not _they_say_they_tried(step, memory):
                said = step[:1].upper() + step[1:]
                if put_right:
                    leads = PUT_RIGHT_LEADS
                else:
                    leads = LOST_LEADS if AT_A_LOSS.search(text or "") else _leads_for(text)
                return _handed_back(memory, _a_lead_and_a_step(
                    _a_lead_for(leads, said, memory, text), said))
            if step:
                _wording = step[:1].upper() + step[1:]
                return _handed_back(memory, _a_lead_and_a_step(
                    _a_lead_for(_the_lead_for(text, step), _wording, memory, text), _wording))
        if more and not a_more_ask(text):
            return None
        if nothing_more:
            return None
        short = _short(said)
        if short and not _already_repeated(short, memory):
            leads = SAY_AGAIN_LEADS if _a_bare_ask(text) else _the_lead_for(text, short)
            return _handed_back(memory, _a_lead_and_a_step(
                _a_lead_for(leads, short, memory, text), short))
    return None


_AN_ENTRY_IS_LOOKING = [False]


def _an_entry_answers_it(text, memory):
    if _AN_ENTRY_IS_LOOKING[0]:
        return False
    _AN_ENTRY_IS_LOOKING[0] = True
    try:
        from ..modules import answers as entries
        reply = entries.respond(str(text or ""), dict(memory or {}))
    except Exception:
        return False
    finally:
        _AN_ENTRY_IS_LOOKING[0] = False
    said = _words(reply)
    if not said:
        return False
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)] if isinstance(
        memory, dict) else []
    opening = " ".join(_words(turns[-1].get("bot") if turns else "")[:8])
    if opening and opening in " ".join(said):
        return False
    return True


def _words(text):
    return re.findall(r"[a-z']+", str(text or "").lower())


def _a_bare_ask(text):
    match = BARE_ASK.match(str(text or "").strip())
    if not match:
        return False
    if match.group("word").lower() in BARE_ASK_NEEDS_A_QUESTION and "?" not in str(text or ""):
        return False
    return True


def _a_lead_and_a_step(lead, step):
    said = str(step or "").rstrip()
    return re.sub(r"\.{2,}$", ".", re.sub(r"\.\.\s+", ". ", lead.format(step=said, said=said)))


A_COUNT_OF_MORE_THAN_ONE = re.compile(
    r"^\W*(?:two|three|four|five|six|seven|eight|nine|ten|both|a couple|a pair|a few|the two|"
    r"the three)\b", re.I)


def _the_lead_for(text, step=""):
    leads = LOST_LEADS if AT_A_LOSS.search(str(text or "")) else LEADS
    if A_COUNT_OF_MORE_THAN_ONE.match(str(step or "")):
        leads = tuple(lead for lead in leads if "one thing" not in lead.lower()) or leads
    return leads


def _content(text):
    return {w for w in topics.words(text or "") if w not in topics.STOPWORDS and len(w) > 2}


def _trouble(text):
    return bool(TROUBLE.search(text or ""))


TROUBLE = re.compile(r"\b(?:can'?t|cant|cannot|won'?t|wont|doesn'?t|doesnt|isn'?t|isnt|"
                     r"keeps?|still|never|again|worse|worst|luck|helping|working|nothing)\b",
                     re.I)

OWNED = re.compile(r"\b(?:my|our|his|her|their)\s+([a-z]{2,})")


SOMEONE_ELSES_LIMIT = re.compile(
    r"\b(?:he|she|they|him|her|them|mum|mom|mother|dad|father|nan|nana|gran|granny|grandma"
    r"|grandad|grandpa|son|daughter|child|kid|boy|girl|husband|wife|partner|brother|sister"
    r"|friend|baby|toddler|little one)\b[^.!?]{0,60}?"
    r"\b(?:can(?:no|')?t\s+(?:have|eat|drink|take|manage)|cant\s+(?:have|eat|drink|take|manage)"
    r"|cannot\s+(?:have|eat|drink|take)|must\s+not\s+(?:have|eat|drink|take)"
    r"|(?:does|do|did)(?:n'?t|nt|\s+not)\s+(?:eat|drink|like|touch)"
    r"|(?:is|are)(?:n'?t|\s+not)\s+allowed|allergic\s+to|intolerant\s+to|stays?\s+away\s+from"
    r"|has\s+to\s+avoid|cuts?\s+out)\b", re.I)


def _a_thing_of_its_own(line, said):
    named = set(OWNED.findall(str(line or "").lower()))
    if not named:
        return False
    words = set(re.findall(r"[a-z']+", str(said or "").lower()))
    stems = {w.rstrip("s") for w in words}
    return not any(word in words or word.rstrip("s") in stems for word in named)

ACK_OPENS = re.compile(
    r"^\s*(?:ok(?:ay)?\s+)?(?:thanks|thank you|thankyou|thank u|thx|ty|ta|cheers|cheerz|"
    r"much appreciated|appreciated)\b[^.!?]{0,20}[.!?]+\s*\S", re.I)


ACK_AND_REST = re.compile(
    r"^\s*(?:ok(?:ay)?\s+|right\s+|ah\s+|oh\s+|aw\s+)?"
    r"(?:thanks|thank you|thankyou|thank u|thx|ty|ta|cheers|cheerz|much appreciated|appreciated)"
    r"(?:\s+(?:so|very|much|a lot|again|loads|tonnes))?"
    r"[^a-z0-9]{0,20}"
    r"(?P<rest>[a-z0-9].*)$", re.I | re.S)


def after_an_ack(text):
    match = ACK_AND_REST.match(str(text or "").strip())
    if not match:
        return ""
    rest = match.group("rest").strip(" ,.!?;:-\u2014")
    rest = re.sub(r"^(?:mate|love|pet|hun|hunny|duck|sunshine|chief|fella|sweetheart)\b[,!.]*\s*",
                  "", rest, flags=re.I)
    if re.match(r"for\b", rest, re.I):
        return ""
    named = [word for word in topics.words(rest) if word not in CLOSES_THE_TURN]
    return rest if len(named) >= 2 else ""


CLOSES_THE_TURN = frozenset("""that this it helps helped helping help works worked work working
    does did will would good great fine perfect nice handy useful brilliant lovely amazing awesome
    fantastic ok okay much loads lot lots again everything all so very really too just then now
    know noted needed needs glad cheers thanks please mate love pet
    thats kind kindest thoughtful generous sweet of you""".split())


BROODING = re.compile(
    r"\b(?:"
    r"(?:going|goes|went)\s+(?:over|round|around)\b|"
    r"round\s+in\s+(?:my|our)\s+(?:head|mind)|\bin\s+my\s+head\b|\bon\s+my\s+mind\b|"
    r"(?:cant|can'?t|cannot|keep|keeps|kept)\s+(?:stop\s+)?thinking\b|"
    r"think(?:ing)?\s+about\s+it\b|\bthoughts?\s+(?:racing|going)\b|"
    r"my\s+mind\s+(?:is\s+)?(?:racing|going|spinning)"
    r")", re.I)


def _a_feeling(text):
    from ..compose.fallback import NEGATIVE_CUES

    if BROODING.search(text or ""):
        return True
    return bool(set(topics.words(text or "")) & NEGATIVE_CUES)


def _the_doing(sentence):
    head, sep, rest = str(sentence).strip().partition(":")
    if sep and not _opens_a_doing(head) and len(head.split()) <= 12 and len(rest.strip()) >= 20:
        whole = rest.strip()
        whole = whole[0].upper() + whole[1:]
    else:
        whole = str(sentence).strip()
    whole = a_whole_cut(whole, MOST)
    last = whole.rstrip("'\"\u2019\u201d")
    return whole + "." if whole and not last.endswith((".", "!", "?")) else whole


def _the_advice(said):
    from ..compose.verdict import IMPERATIVES

    best, most = "", 1
    for part in [p.strip() for p in SENTENCE.split(str(said).strip()) if p.strip()]:
        if topics.RED_FLAG.match(part) or ASKING_THEM.search(part):
            continue
        words = [w.strip(" ,;:.") for w in part.lower().split()]
        count = sum(1 for w in words if w in IMPERATIVES)
        count += 1 if re.search(r"\bdo not\b|\bdon'?t\b", part, re.I) else 0
        if count > most:
            best, most = part, count
    return best


def the_next_move(memory, text=""):
    for back, asked, said in _recent_answers(memory):
        if back > 1 and not _about_the_same_thing(asked, said, memory):
            continue
        if NEXT_STEP_EMERGENCY.search(said):
            return ""
        step = _next_step(said)
        if step and not _already_repeated(step, memory):
            step = step[:1].upper() + step[1:]
            return pick(TRIED_LEADS, memory, text or "").format(step=step)
        return ""
    return ""


def _next_step(said):
    sentences = [s.strip() for s in SENTENCE.split(str(said or "")) if s.strip()]
    for sentence in reversed(sentences[1:]):
        if NEXT_STEP.search(sentence):
            return sentence
    return ""


def _later_part(tried, said):
    def shared(part, words):
        return sum(1 for w in _content(part)
                   if any(w == v or (len(w) >= 5 and len(v) >= 5 and w[:5] == v[:5])
                          for v in words))

    parts = [p.strip() for p in SENTENCE.split(str(said).strip()) if p.strip()]
    tried_words = _content(tried)
    best_i, most = -1, 0
    for i, part in enumerate(parts):
        count = shared(part, tried_words)
        if count > most:
            best_i, most = i, count
    if best_i >= 0:
        later = []
        for part in parts[best_i + 1:]:
            if topics.RED_FLAG.match(part) or ASKING_THEM.search(part):
                continue
            if shared(part, tried_words) >= most:
                continue
            doing = _the_doing(part)
            if len(doing) >= 25:
                later.append(doing)
        for doing in later:
            if _opens_a_doing(doing):
                return doing
        return later[0] if later else ""
    best = ""
    for part in parts[1:]:
        if topics.RED_FLAG.match(part) or ASKING_THEM.search(part):
            continue
        doing = _the_doing(part)
        if len(doing) >= 25:
            best = doing
    return best


def _opens_a_doing(sentence):
    from ..compose.verdict import IMPERATIVES

    words = str(sentence).strip(" .,:;").split()
    if not words:
        return False
    first = words[0].lower().strip(".,;:")
    if first in IMPERATIVES or first in MOVE_VERBS:
        return True
    if first.endswith("ing") and len(first) > 4:
        stem = first[:-3]
        bare = [stem, stem + "e"]
        if len(stem) > 2 and stem[-1] == stem[-2]:
            bare.append(stem[:-1])
        return any(candidate in IMPERATIVES for candidate in bare)
    return False


def _the_untried(tried, memory):
    for back, _question, said in _recent_answers(memory):
        if back != 1:
            return None
        best = _later_part(tried, said)
        if best and not _already_repeated(best, memory):
            return _handed_back(memory, best)
    return None


TRIED = re.compile(r"\b(?:i|we|he|she|they)\s+(?:already\s+)?(?:tried|done)\b|"
                   r"\b(?:i(?:'ve|ve| have)|we(?:'ve|ve| have)|he(?:'s|s| has)|"
                   r"she(?:'s|s| has)|they(?:'ve|ve| have))\s+(?:already\s+)?"
                   r"(?:tried|done|had)\b|\balready\s+(?:tried|done|had)\b|"
                   r"\b(?:tried|done)\s+(?:that|it|this)\b", re.I)
NOT_TRIED = re.compile(r"\b(?:not|never|havent|hasnt|didnt|haven't|hasn't|didn't)\s+"
                       r"(?:\w+\s+){0,2}(?:tried|done|had)\b", re.I)
QUESTION_MORE = re.compile(r"\b(?:how|what|when|why|which|should)\b", re.I)


def _tried(text):
    return bool(TRIED.search(text or "")) and not NOT_TRIED.search(text or "")

def _says_they_agree(clean):
    words = [word.strip(".,!;:\"'").lower() for word in clean.split()]
    if any(word in AGREES_ON_ITS_OWN for word in words):
        return True
    if AGREES_IN_A_PHRASE.search(clean):
        return True
    return len(words) <= 8 and bool(words) and words[-1] in AGREEMENT_TAIL


def _the_thing_they_named(clean, part):
    kept = []
    for word in clean.split():
        bare = word.strip(".,!;:\"'").lower()
        if not bare or bare in AGREEING:
            continue
        kept.append(word.strip(".,!;:\"'"))
    while len(kept) > 1 and kept[0].lower() in BE_FORM | POINTING_AT:
        kept = kept[1:]
    if not kept or len(kept) > 4 or kept[0].lower() in BE_FORM | POINTING_AT:
        return ""
    if kept[0].lower() in OPENERS:
        return ""
    return " ".join(kept)


def agreement_with_the_answer(text, memory):
    clean = (text or "").strip()
    if (not clean or clean.endswith("?") or QUESTION.match(clean) or ASKS.match(clean)
            or len(clean.split()) > 20):
        return ""
    if ABOUT_THE_BOT.search(clean) or WORDS_WANTED.search(clean):
        return ""
    asked = _content(clean)
    if len(asked) < 2:
        return ""
    for back, question, said in _recent_answers(memory):
        if back > 1 and not _about_the_same_thing(question, said, memory):
            continue
        best, shared = "", 0
        for part in [p.strip() for p in SENTENCE.split(said) if p.strip()]:
            if topics.RED_FLAG.match(part) or ASKING_THEM.search(part):
                continue
            count = len(asked & _content(part))
            if count > shared:
                best, shared = part, count
        if shared < len(asked) or not _says_they_agree(clean):
            continue
        named_thing = _the_thing_they_named(clean, best)
        if named_thing:
            return _agreed(named_thing, memory)
    return ""


def _agreed(named, memory):
    low = named[:1].lower() + named[1:]
    up = named[:1].upper() + named[1:]
    return pick([up + ", yes.",
                 "Yes \u2014 " + low + ".",
                 up + " it is.",
                 "That's it: " + low + ".",
                 up + ", that's the main thing."], memory, named)


DONE = re.compile(
    r"\b(?:i|we|he|she|they)\s+(?:(?:have|had|already|just|finally|now|then|since)\s+)*"
    r"(?P<verb>[a-z]+)\b", re.I)
IRREGULAR_PAST = {
    "did": "do", "done": "do", "made": "make", "took": "take", "given": "give", "got": "get",
    "left": "leave", "kept": "keep", "cut": "cut", "put": "put", "set": "set", "ran": "run",
    "bled": "bleed", "hung": "hang", "wore": "wear", "fed": "feed", "found": "find",
    "built": "build", "sent": "send", "spent": "spend", "threw": "throw", "dug": "dig",
    "held": "hold", "lit": "light", "swept": "sweep", "bought": "buy", "caught": "catch",
    "taught": "teach", "told": "tell", "sold": "sell", "froze": "freeze", "drew": "draw",
    "shut": "shut", "spread": "spread", "paid": "pay", "struck": "strike", "shook": "shake",
}
NO_LONGER_TO_DO = frozenset("""not never no havent hasnt didnt doesnt dont wont cant
    haven't hasn't didn't doesn't don't won't can't""".split())


def _the_stems(word):
    word = str(word or "").lower()
    out = set()
    if word.endswith("ied") and len(word) > 4:
        out.add(word[:-3] + "y")
    if word.endswith("ed"):
        base = word[:-2]
        out.add(base)
        out.add(base + "e")
        if len(base) > 2 and base[-1] == base[-2]:
            out.add(base[:-1])
    elif word.endswith("d") and len(word) > 3:
        out.add(word[:-1])
    return out


def _the_act(word):
    from ..compose.verdict import IMPERATIVES

    base = IRREGULAR_PAST.get(word)
    if base and (base == "do" or base in IMPERATIVES):
        return base
    for stem in _the_stems(word):
        if stem in IMPERATIVES:
            return stem
    return None


STANDS_IN = frozenset("it them that this one ones those these there".split())
OBJECT_END = frozenset("""for to in on at with by from into onto and but then so because when
    while before after again twice once already yesterday today tonight now later still
    earlier this morning evening week month year""".split())


def _the_object(clean, at):
    tail = []
    for word in str(clean or "")[at:].lower().replace(",", " ").split():
        bare = word.strip(" .;:!?()[]\"")
        if not bare or bare in OBJECT_END:
            break
        if bare in STANDS_IN:
            return None
        tail.append(bare)
    said = frozenset(word for word in tail if len(word) > 2 and word not in topics.STOPWORDS)
    return said or None


def _the_steps_done(text):
    acts = set()
    clean = str(text or "")
    for match in DONE.finditer(clean):
        before = clean[:match.start()].lower().split()[-3:]
        if any(w.strip(" ,.;:!?'") in NO_LONGER_TO_DO for w in before):
            continue
        act = _the_act(match.group("verb").lower())
        if act:
            acts.add((act, _the_object(clean, match.end())))
    return acts


def _the_answer_gives(said, act):
    for word in str(said or "").lower().replace("'", "").split():
        word = word.strip(" ,.;:!?()[]\"")
        if word == act or act in _the_stems(word):
            return True
    return False


def _a_step_done(text, said):
    acts = _the_steps_done(text)
    if not acts or not said:
        return False
    given = _content(said)
    for act, thing in acts:
        by_object = act == "do"
        if not by_object and not _the_answer_gives(said, act):
            continue
        if thing is None:
            if not by_object:
                return True
            continue
        if thing & given:
            return True
    return False


def _the_step_just_given(text, memory):
    for back, _question, said in _recent_answers(memory):
        return back == 1 and _a_step_done(text, said)
    return False


REJOINDER = re.compile(r"\b(?:though|although|already|but|anyway|still|mind you|to be fair)\b",
                       re.I)


def carried_on(text, memory):
    clean = (text or "").strip()
    asked_after = without_a_reset(clean)
    if QUESTION.match(asked_after) or ASKS.match(asked_after):
        clean = asked_after
    if (not clean or clean.endswith("?") or QUESTION.match(clean) or ASKS.match(clean)
            or len(clean.split()) > 20):
        return None
    if ABOUT_THE_BOT.search(clean) or WORDS_WANTED.search(clean):
        return None
    if ASKING_TO_START.search(clean):
        return None
    if ACK_OPENS.match(clean):
        return None
    if limits.names_a_limit(clean):
        return None
    if not QUESTION_MORE.search(clean) and (_tried(clean) or _the_step_just_given(clean, memory)):
        return _the_untried(clean, memory)
    if isinstance(memory, dict) and (memory.get("understood") or {}).get("routine") \
            and not REJOINDER.search(clean):
        return None
    asked = _content(clean)
    if len(asked) < 2:
        return None
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    which_part = asks_for_the_move(text)
    if turns and not which_part and REFER_BACK.search(str(turns[-1].get("bot") or "")):
        return None
    for back, question, said in _recent_answers(memory):
        if back > 1 and not _about_the_same_thing(question, said, memory):
            continue
        best, shared = "", 0
        for part in [p.strip() for p in SENTENCE.split(said) if p.strip()]:
            if topics.RED_FLAG.match(part) or ASKING_THEM.search(part):
                continue
            count = len(asked & _content(part))
            if count > shared:
                best, shared = part, count
        if shared < 2:
            best = (_the_advice(said) if back == 1 and _trouble(clean) and not _a_feeling(clean)
                    and not _a_thing_of_its_own(clean, said)
                    and not SOMEONE_ELSES_LIMIT.search(clean) else "")
            if not best:
                continue
        elif shared >= len(asked) and _says_they_agree(clean):
            named = _the_thing_they_named(clean, best)
            if named:
                return _agreed(named, memory)
        doing = _the_doing(best)
        if len(doing) < 25 or _already_repeated(doing, memory):
            continue
        return _handed_back(memory, doing)
    return None

recent_answers = _recent_answers
same_subject = _about_the_same_thing
said_recently = _already_repeated
handed_back = _handed_back

_A_STALL = (r"(?:keeps? putting (?:it |things )?off|puts? (?:it |things )?off"
            r"|putting (?:it |things )?off|keeps? avoiding (?:it|them|this)"
            r"|does not know (?:how|where) to start"
            r"|doesn[\u2019']?t know (?:how|where) to start|not sure (?:how|where) to start"
            r"|can[\u2019']?t get started|cannot get started|has not started|hasn[\u2019']?t started"
            r"|not even started|leaves? it to the last minute|hates? starting)")
ASKING_TO_START = re.compile(
    r"(?:\b(?:he|she|they)\b|\bthe (?:kids?|children)\b"
    r"|\bmy (?:son|daughter|child|kid|boy|girl|mum|mom|dad|father|mother|partner|husband|wife"
    r"|brother|sister|friend|nephew|niece|grandson|granddaughter)\b)"
    r"[^.!?]{0,30}?\b" + _A_STALL + r"\b", re.I)

START_ASK = re.compile(r"\b(?:where|how)\s+(?:do|does|should|shall|can|could|would|might|to)\s+"
                       r"(?:(?:i|we|you)\s+)?(?:start|begin)(?:ed|ing)?\b|"
                       r"\bhow do (?:i|we) get (?:started|going)\b|"
                       r"\b(?:do|try|change|fix|sort|put|write|tackle|get)\s+first\b|"
                       r"\bfirst (?:thing|step|move)\b|\bnext step\b", re.I)

STARTING_WHAT = re.compile(
    r"\b(?:where|how)\s+(?:do|does|should|shall|can|could|would|might|to)\s+"
    r"(?:(?:i|we|you)\s+)?(?:start|begin)(?:ed|ing)?\s+([a-z']+)(?:\s+([a-z']+))?", re.I)

STARTING_BACK = frozenset("""
it this that them these those one again over now today here then though please anyway
small slowly simple easy gently early off out up
""".split())
STARTING_AT = frozenset(("with", "on", "about"))

STARTING_OUT = re.compile(
    r"\b(?:start|begin)(?:ed|ing)?\s+(?:out|off)\s+([a-z']+)(?:\s+([a-z']+))?", re.I)
STARTING_INTO = frozenset(("in", "into", "at", "for", "as"))


def _starting_out_names_a_thing(line):
    found = STARTING_OUT.search(line)
    if found is None:
        return False
    first, second = found.group(1), found.group(2) or ""
    if first in STARTING_INTO or first in STARTING_AT:
        return bool(second) and second not in STARTING_BACK
    return first not in STARTING_BACK


def says_where_to_start(text):
    line = str(text or "")
    if not START_ASK.search(line):
        return False
    if _starting_out_names_a_thing(line):
        return False
    found = STARTING_WHAT.search(line)
    if found is None:
        return len(_names_a_thing_of_its_own(line)) < 2
    first, second = found.group(1), found.group(2) or ""
    if first in STARTING_AT:
        return not second or second in STARTING_BACK
    return first in STARTING_BACK

MORE_ASK = re.compile(r"\bwhat else (?:can|could|should|would) (?:i|we)\b|"
                      r"\bwhat else (?:is there|works|helped|helps|do i do)\b|"
                      r"\banything else (?:i|we) (?:can|could|should) (?:do|try)\b|"
                      r"\bis there anything else\b|"
                      r"\b(?:and )?what else\b(?!\s+(?:could|would|might|is|are|was|were)\s+it\b)",
                      re.I)

IDEAS_ASK = (r"anything (?:else|more|other)|"
             r"(?:any|some) (?:other |more |different )?"
             r"(?:ideas?|suggestions?|thoughts?|recommendations?|options?|tips?)|"
             r"what (?:do|would|can|should) you (?:suggest|recommend|pick|choose|go for|advise)|"
             r"what would you (?:pick|choose|go for|do)|"
             r"your (?:ideas|suggestions|thoughts|recommendations)|"
             r"ideas|suggestions")
IDEAS_ONLY = re.compile(
    r"^\W*(?:(?:and|so|ok|okay|right|well|alright|then|but)\b[\s,]+)*(?:" + IDEAS_ASK + r")" +
    r"\W*(?:[\s,]+(?:then|please|now|tho|though|thanks|ta))?\W*$", re.I)


def a_more_ask(text):
    said = str(text or "")
    return bool(MORE_ASK.search(said) or IDEAS_ONLY.match(said))


WORDING = re.compile(r"\bhow (?:do|can|should|could|would|might) (?:i|we)\s+(?:"
                     r"(?:word|write|say|phrase|put|explain|draft|reply|tell|ask|answer)\b"
                     r"|(?:bring|raise|mention|broach|approach)\s+"
                     r"(?:it|that|this|them|the (?:subject|issue|matter|problem))\b"
                     r")", re.I)

HOW_IT = re.compile(r"\bhow (?:do|can|should|could|would|might|shall) (?:i|we)\s+"
                    r"(?:[a-z']+\s+){0,3}(?:it|that|this|them|these|those)\b", re.I)


def _places_to_cut(head):
    spots = []
    for found in QUALIFIER.finditer(head):
        after = head[found.end():].strip().split()
        if not after:
            continue
        if after[0].lower() in OPENERS:
            continue
        spots.append(found.start())
    for index, char in enumerate(head):
        if char == "(" and ")" in head[index:]:
            spots.append(index)
    return sorted(set(spots))


def _inside_a_bracket(text, at):
    return text.count("(", 0, at) > text.count(")", 0, at)


LIST_LEAD = re.compile(r"\b(?:works?|working|helps?|helped|things to do|to do|steps?|rules?|"
                       r"habits?|ways?|tips?|start|begin|try|keep|stick to|do these|do this)\b",
                       re.I)

NOT_A_TAIL = re.compile(r"\b(?:things|rest|following|list|these|those|steps|rules|ways|tips|"
                        r"habits|ideas|examples|reasons)\b", re.I)

NOT_A_DOING = re.compile(r"\b(?:you|your|i|we|they|he|she|it|its|their)\b|"
                         r"\b(?:is|are|was|were|has|have|had|means|meant)\b", re.I)


def _a_list_item(part):
    if ":" not in part:
        return ""
    lead = part.split(":")[0]
    if not LIST_LEAD.search(lead):
        return ""
    items = [p.strip(" .:;") for p in _pieces(part)][1:]
    items = [p for p in items if p]
    if len(items) < 2:
        return ""
    first = items[0]
    words = first.split()
    if not 3 <= len(words) <= 8:
        return ""
    if NOT_A_DOING.search(first) or topics.RED_FLAG.match(first) or NOT_A_STEP.match(first):
        return ""
    from ..compose.verdict import IMPERATIVES

    verbs = set(IMPERATIVES) | set(MOVE_VERBS)
    if any(word.strip(".,!?;:'\"").lower() in verbs for word in words):
        return ""
    return first


def _pieces(part):
    marks = [f for f in PIECE_END.finditer(part) if not _inside_a_bracket(part, f.start())]
    out, start, listed = [], 0, False
    for index, found in enumerate(marks):
        if found.group().strip() == "," and not listed:
            end = marks[index + 1].start() if index + 1 < len(marks) else len(part)
            after = part[found.end():end].strip(" ,;:.")
            after = re.sub(r"^(?:and|then|but|also|so|next|plus)\s+", "", after, flags=re.I)
            if not _opens_on_a_verb(after):
                continue
        if found.group().strip() == ":" and not listed:
            keeps, at = _the_colon_tail_kept(part, marks, index, start, found)
            if keeps is None:
                start, listed = len(part), True
                continue
            if keeps:
                if at is None:
                    continue
                out.append(keeps)
                start = at
                listed = True
                continue
        out.append(part[start:found.start()])
        start = found.end()
        listed = listed or found.group().strip() == ":"
    out.append(part[start:])
    return out


A_QUESTION = re.compile(r"^\s*(?:who|what|which|when|where|why|how|whether)\b", re.I)


def _the_tail_asks_a_question(part, marks, index, found):
    end = marks[index + 1].start() if index + 1 < len(marks) else len(part)
    return bool(A_QUESTION.match(part[found.end():end].strip(" ,;.")))


def _the_colon_tail_kept(part, marks, index, start, found):
    head = part[start:found.start()].strip(" ,;")
    if not _opens_on_a_verb(head):
        return "", None
    if NOT_A_TAIL.search(head) and not _the_tail_asks_a_question(part, marks, index, found):
        return None, None
    tail = part[found.end():]
    if len((head + ": " + tail).split()) <= STEP_WITH_ITS_METHOD:
        return head + ": " + tail.rstrip(" ,;"), None
    for later in marks[index + 1:]:
        if later.group().strip() not in (",", ";"):
            continue
        first = part[found.end():later.start()].strip(" ,;")
        if not first:
            continue
        piece = head + ": " + first
        if len(piece.split()) <= STEP_WITH_ITS_METHOD:
            return piece, later.end()
        return "", None
    return "", None


def _opens_on_a_verb(text):
    from ..compose.verdict import IMPERATIVES

    words = text.strip(" .,:;").split()
    if not words:
        return False
    return words[0].lower() in IMPERATIVES or words[0].lower() in MOVE_VERBS


DECLARATIVE = re.compile(r"^(?:[a-z']+\s+)(?:is|are|was|were|has|have|had|can|cannot|will|would|"
                         r"should|takes?|gives?|means?|costs?|comes?|goes?|does|did|gets?|keeps?)\b",
                         re.I)
QUESTIONS_THAT_ARE_NOT_STEPS = re.compile(
    r"^(?:what|which|how|when|where|who|why|tell me|let me know)\b", re.I)


def _the_steps(said):
    from ..compose.verdict import IMPERATIVES

    verbs = frozenset(IMPERATIVES) | frozenset(MOVE_VERBS)
    for part in [p.strip() for p in SENTENCE.split(str(said).strip()) if p.strip()]:
        if topics.RED_FLAG.match(part):
            continue
        if CONDITION_CLAUSE.match(part):
            continue
        found = []
        for piece in _pieces(part):
            head = piece.strip(" .:;")
            head = re.sub(r"^(?:and|then|but|also|so|next|plus)\s+", "", head, flags=re.I)
            if not head or topics.RED_FLAG.match(head) or NOT_A_STEP.match(head):
                continue
            if A_MENU.search(head):
                continue
            if DECLARATIVE.match(head):
                continue
            if head.endswith("?") or QUESTIONS_THAT_ARE_NOT_STEPS.match(head):
                continue
            words = head.split()
            if ":" in head:
                limit, cut_words = STEP_WITH_ITS_METHOD, STEP_WITH_ITS_METHOD
            else:
                limit, cut_words = STEP_WORDS, CUT_WORDS
            if len(words) > cut_words and words[0].lower() not in NEEDS_COMPLEMENT:
                cut = None
                for at in _places_to_cut(head):
                    if _inside_a_bracket(head, at):
                        continue
                    left = head[:at].strip(" ,;:.").split()
                    if len(left) < SHORT_STEP:
                        continue
                    if left[-1].lower() in DANGLING:
                        continue
                    cut = at
                    break
                if cut:
                    head = head[:cut].strip(" ,;:.")
                    words = head.split()
            if not 3 <= len(words) <= limit:
                first_half = _the_first_instruction_in_a_long_piece(head, verbs)
                if first_half is None:
                    continue
                head, words = first_half, first_half.split()
            if words[0].lower() not in verbs \
                    and not _a_verb_after_a_leading_phrase(head, verbs):
                continue
            trimmed = re.sub(r"\s+(?:first|next)$", "", head, flags=re.I)
            if trimmed.split() and trimmed.split()[-1].lower() not in DANGLING:
                head = trimmed
            found.append(head[0].lower() + head[1:])
        for step in found:
            yield step
        if not found:
            item = _a_list_item(part)
            if item:
                yield item[0].lower() + item[1:]


def _the_next_step(said, memory):
    steps = list(_the_steps(said))
    for step in steps[1:]:
        if topics.RED_FLAG.match(step):
            continue
        if _already_repeated(step, memory) or _they_say_they_tried(step, memory):
            continue
        return step
    return None


def _the_first_step(said):
    for step in _the_steps(said):
        return step
    return None


WHAT_IT_IS = re.compile(r"^\s*(?:what(?:'s|s| is| are| does| do| did)\b|"
                        r"tell me (?:about|what)\b|define\b|meaning of\b)", re.I)


def _a_new_work(text, asked):
    line = str(text or "")
    if asks_to_put_it_right(line) or HOW_IT.search(line):
        return False
    if not WHAT_IT_IS.match(str(asked or "")):
        return False
    return bool(_doings(line))


def asks_which_part(text):
    line = str(text or "")
    if not line.strip() or WORDING.search(line):
        return False
    return bool(asks_for_the_move(line)) and not HOW_IT.search(line)


def _leads_for(text):
    return CHANGE_LEADS if CHANGE_ASK.search(text or "") else MOVE_LEADS


def _a_lead_for(leads, step, memory, text):
    if STEP_SAYS_FIRST.search(str(step or "").strip()):
        leads = tuple(lead for lead in leads
                      if not LEAD_SAYS_FIRST.search(re.sub(r"\{[a-z_]+\}", " ", lead)))
        leads = leads or NOW_LEADS
    return pick(leads, memory, text)


def the_move(text, said, memory):
    if not isinstance(said, str) or not said.strip():
        return None
    if not asks_for_the_move(text):
        return None
    if WORDING.search(str(text or "")):
        return None
    if re.search(r"\bhow (?:long|much|many|often|far|hot|soon)\b", str(text or ""), re.I):
        return None
    step = _the_first_step(said)
    if not step or _already_repeated(step, memory):
        return None
    if not isinstance(memory, dict):
        return None
    if _they_say_they_tried(step, memory):
        return None
    _wording = step[:1].upper() + step[1:]
    return _handed_back(memory, _a_lead_and_a_step(
        _a_lead_for(_leads_for(text), _wording, memory, text), _wording))


def _they_say_they_tried(step, memory):
    mine = {word for word in re.findall(r"[a-z']+", step.lower()) if len(word) > 2}
    if not mine:
        return False
    for turn in (memory.get("turns") or [])[-3:]:
        if not isinstance(turn, dict):
            continue
        line = str(turn.get("user") or "").lower()
        if not ATTEMPT.search(line):
            continue
        said = {word for word in re.findall(r"[a-z']+", line) if len(word) > 2}
        shared = mine & said
        if len(shared) >= 2 or any(len(word) >= 5 for word in shared):
            return True
    return False


ATTEMPT = re.compile(r"\b(?:tried|trying|already|gave it|had a go|no luck|used)\b", re.I)


FIGURE_ASKS = (
    ("time", re.compile(
        r"\bhow\s+(?:long|soon|quick(?:ly)?|longer)\b"
        r"|\bhow\s+many\s+(?:seconds?|minutes?|mins?|hours?|hrs?|days?|weeks?|months?|years?|nights?)\b"
        r"|\bwhat\s+(?:time|timing)\b", re.I),
     re.compile(
        r"\b(?:\d+(?:\.\d+)?|a|an|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
        r"fifteen|twenty|thirty|forty|forty-five|fifty|sixty|ninety)\s*(?:\w+\s+to\s+)?"
        r"(?:seconds?|secs?|minutes?|mins?|hours?|hrs?|days?|weeks?|wks?|months?|years?|nights?)\b",
        re.I)),
    ("heat", re.compile(r"\bhow\s+(?:hot|warm)\b|\bwhat\s+(?:temperature|heat|gas\s+mark)\b", re.I),
     re.compile(r"\b(?:\d{2,3}\s*(?:°|degrees?|c\b|celsius|f\b|fahrenheit)|gas\s+mark\s+\d|"
                r"mark\s+\d\b)", re.I)),
    ("amount", re.compile(r"\bhow\s+(?:much|many)\b", re.I),
     re.compile(r"(?:£\s?\d|\b\d+\s*(?:g|kg|grams?|ml|l|litres?|pints?|cups?|tbsp|tsp|oz|ounces?)\b)",
                re.I)),
    ("often", re.compile(r"\bhow\s+often\b|\bhow\s+many\s+times\b", re.I),
     re.compile(r"\b(?:once|twice|three\s+times|\d+\s+times)\b[^.?!]{0,25}"
                r"\b(?:a|per|every)\s+(?:day|week|month|year|night)\b", re.I)),
)

FIGURE_WORDS = frozenset("""
    how long soon quickly quick longer much many often hot warm what time timing temperature heat
    gas mark should shall can could would will may might must do does did is are was were am
    i we you they he she it its that this these those them there and so ok okay but then again
    also just really leave left need use take cook bake keep wait soak boil simmer rest run
    sit stand stay lie hang dry cool warm heat set settle marinate marinade prove rise chill
    exercise give put apply wear change replace before after for in on at to it too much
    before afterwards after that
""".split())

FIGURE_SAYING = frozenset("""
    ask asking say saying tell telling mention mentioning bring bringing raise raising
    broach broaching approach approaching him her them
""".split())


def the_figure_asked(text, memory):
    if not isinstance(memory, dict):
        return None
    clean = " ".join(str(text or "").lower().split())
    if not clean:
        return None
    asked = None
    for _name, ask, figure in FIGURE_ASKS:
        if ask.search(clean):
            asked = ask, figure
            break
    if asked is None:
        return None
    ask, figure = asked
    rest = [word for word in re.findall(r"[a-z']+", ask.sub(" ", clean))
            if word not in FIGURE_WORDS and word not in FIGURE_SAYING]
    if rest:
        return None
    seen_a_card = False
    for back, turn in enumerate(reversed((memory.get("turns") or [])[-LOOK_BACK:]), 1):
        if not isinstance(turn, dict):
            break
        if turn.get("module") != "answers":
            continue
        said = str(turn.get("bot") or "").strip()
        if not said or HEDGE.search(said) or said.rstrip().endswith("?"):
            continue
        if len(said) < 50 and not figure.search(said):
            continue
        if back > 1 and not _about_the_same_thing(str(turn.get("user") or ""), said, memory):
            continue
        for part in _sentences(said):
            part = part.strip().rstrip(" ;")
            if part and figure.search(part) and not _already_repeated(part, memory):
                return part[:1].upper() + part[1:] + ("" if part[-1:] in ".!?" else ".")
    return None


STILL_SAFE = re.compile(
    r"\bstill\s+(?:ok|okay|good|fine|safe|edible|alright)\b|\bis\s+(?:it|that|this)\s+"
    r"(?:safe|alright|fine|ok|okay|good)\b|\bcan\s+i\s+still\b|\bsafe\s+(?:to|for)\b",
    re.I)
SAID_SAFE = re.compile(
    r"\b(?:safe|fine|okay|ok|keep|keeps|kept|bin|binned|binning|throw|thrown|eat|eaten|edible|"
    r"cooked|refreeze|put\s+back|nothing\s+needs|no\s+need)\b", re.I)
DO_I_NEED_TO = re.compile(
    r"\bdo\s+i\s+(?:need|have)\s+to\b|\bhave\s+i\s+got\s+to\b|\bshould\s+i\b|"
    r"\bam\s+i\s+meant\s+to\b|\bdo\s+you\s+have\s+to\b", re.I)
A_MOVE = re.compile(
    r"\b(?:prick|cut|turn|stir|cover|leave|put|add|check|wash|rinse|soak|rest|shake|score|"
    r"season|test|wait|ask|keep|write|print|sign|ring|call|book|take|use|give|hold|open|close|"
    r"run|cook|bake|boil|simmer|freeze|defrost|empty|clean|wipe|change|replace)\b", re.I)
WHERE_TO_START = re.compile(
    r"\bwhere\s+(?:do|should|would|can|shall)\s+i\s+(?:really\s+|even\s+)?(?:start|begin)\b"
    r"|\bwhere\s+to\s+start\b|\bwhat\s+(?:do|should)\s+i\s+(?:do|try)\s+first\b"
    r"|\bhow\s+do\s+i\s+(?:start|begin|get\s+going)\b|\bwhere\s+do\s+i\s+(?:go|look)\b",
    re.I)

PART_ASKS = (
    ("time", re.compile(r"\bwhen\s+(?:does|do|will|would|should|can|is|are)\b|"
                        r"\bhow\s+(?:soon|long)\b|\bhow\s+(?:much\s+)?longer\b", re.I), FIGURE_ASKS[0][2]),
    ("start", WHERE_TO_START, None),
    ("safe", STILL_SAFE, SAID_SAFE),
    ("move", DO_I_NEED_TO, A_MOVE),
)

PART_STAND_INS = frozenset("""
    food foods stuff thing things bit bits part parts piece pieces kit gear item items
    water drink milk meat rest lot lots everything anything something nothing else
    job work house home place places one plant plants garden washing clothes
""".split())


def _the_keys_of(said, memory):
    head = " ".join(str(said or "").split())[:60]
    for record in (memory or {}).get("entry_answers") or ():
        if not isinstance(record, dict):
            continue
        text = " ".join(str(record.get("text") or "").split())
        if text and text[:60] == head:
            return {str(key).lower() for key in (record.get("keys") or ())}
    return set()


NOT_ALONE = re.compile(r"^(?:then|after that|afterwards?|next|also|and|but|or|so|instead|"
                       r"either|once|while|because|which|that|this|it|they|them|he|she)\b", re.I)
PART_OPENS = frozenset("""
    then afterwards next also and but or so instead either once while because which
""".split())


def answers_nothing(reply):
    if not reply:
        return False
    from ..compose import fallback
    from ..compose import verdict
    if fallback._is_a_hedge(reply) or fallback._nothing_to_stand_behind(reply):
        return True
    return fallback._in_a_pool(reply, (fallback.SAME_AGAIN,
                                       fallback.HELP_ALREADY,
                                       fallback.TIPS_LINES,
                                       fallback.TIPS_THING,
                                       fallback.TRIED_NO_CHANGE_ELSEWHERE,
                                       verdict.ALL_OF_IT_LINES))


def the_advice_was_to_get_seen(memory):
    from . import stuck
    return stuck.the_advice_was_to_get_seen(memory)


def the_part_asked(text, memory):
    if not isinstance(memory, dict):
        return None
    clean = " ".join(str(text or "").lower().split())
    if not clean:
        return None
    kind = None
    for name, ask, mark in PART_ASKS:
        if ask.search(clean):
            kind = name, mark
            break
    if kind is None:
        return None
    name, mark = kind
    if name == "move" and not _whether_to(clean):
        return None
    asked_words = topics.words(clean)
    if name == "move":
        for _name2, ask2, _mark2 in PART_ASKS:
            if _mark2 is None:
                continue
            found = ask2.search(clean)
            if not found:
                continue
            asked_words = [word for word in asked_words
                           if word not in re.findall(r"[a-z']+", found.group(0))]
            break
    if name == "move":
        _step = _whether_to(clean)
        if not [word for word in _step.split()[2:] if word not in PART_STAND_INS][1:]:
            return None
    asked = [word for word in asked_words
             if len(word) > 2 and not word.isdigit() and word not in topics.STOPWORDS
             and word not in ASK and word not in ASK_VERB and word not in TIME
             and word not in FILLER and word not in SELF and word not in PART_STAND_INS]
    doing = ""
    still = STILL_ASKS.match(clean)
    if still:
        doing_words = re.findall(r"[a-z']+", still.group("rest"))
        if doing_words:
            doing = _a_stem(doing_words[0])
    seen_a_card = False
    for back, turn in enumerate(reversed((memory.get("turns") or [])[-LOOK_BACK:]), 1):
        if not isinstance(turn, dict):
            break
        if turn.get("module") != "answers":
            continue
        said = str(turn.get("bot") or "").strip()
        if not said or HEDGE.search(said) or said.rstrip().endswith("?"):
            continue
        if len(said) < 50:
            continue
        keys = _the_keys_of(said, memory)
        on_the_card = bool(asked) and bool(set(asked) & keys)
        if not asked and seen_a_card:
            continue
        seen_a_card = True
        if asked and back > 1 and not on_the_card and not _about_the_same_thing(
                str(turn.get("user") or ""), said, memory):
            continue
        if not asked and back > 1 and not _the_chat_is_still_on(said, memory):
            continue
        for index, part in enumerate(_sentences(said)):
            part = part.strip().rstrip(" ;")
            if len(part.split()) < 4:
                continue
            if part.lower().endswith("?"):
                continue
            if NOT_ALONE.match(part):
                continue
            if name == "start":
                if index > 0:
                    break
            else:
                if not mark.search(part):
                    continue
                if CONDITION_CLAUSE.match(part) or NOT_A_MOVE.match(part):
                    continue
            if asked and not on_the_card and not any(word in part.lower() for word in asked):
                continue
            if doing and doing not in {_a_stem(word) for word in re.findall(r"[a-z']+",
                                                                            part.lower())}:
                continue
            if _already_repeated(part, memory):
                continue
            return part[:1].upper() + part[1:] + ("" if part[-1:] in ".!?" else ".")
    return None


WHERE_TO_LOOK = {
    "cooking": "the packet or a cookery site",
    "food-and-drink": "the label or a cookery site",
    "health": "the NHS site or a pharmacist",
    "fitness": "a coach or the NHS site",
    "sleep": "the NHS site",
    "money": "the official page, gov.uk or your bank",
    "work": "your contract or ACAS",
    "school-and-study": "the school's own notice or the exam board",
    "science": "a textbook or the Royal Society site",
    "history": "a museum's own page",
    "geography-and-travel": "a map app or the operator's own site",
    "technology": "the maker's support page",
    "home-and-diy": "the maker's instructions or a qualified trade",
    "garden-and-plants": "the RHS site or the plant's own label",
    "pets": "your vet",
    "family-and-parenting": "your GP or the NHS site",
    "friends-and-relationships": "the person themselves",
    "shopping": "the shop's own listing",
    "cars": "the handbook or a garage",
    "entertainment": "a listings site",
    "sport": "the club or the governing body's site",
    "language-and-writing": "a dictionary",
    "feelings": "a friend who knows you, or your GP",
    "maths-and-numbers": "a calculator",
    "nature-and-weather": "the Met Office site",
}
WHERE_TO_LOOK_DEFAULT = "a search"

WHERE_TO_LOOK_WORDS = (
    (("baby", "formula", "bottle", "breastfeed", "nappy", "weaning"), "the NHS site or a health visitor"),
    (("boiler", "radiator", "thermostat", "bleed"), "the maker's instructions or a gas engineer"),
    (("extractor", "socket", "fuse", "appliance", "plug", "wiring"), "the maker's manual or an electrician"),
    (("oven", "roast", "bake", "boil", "fry", "pan", "saucepan", "dough", "oven's"), "the packet or a cookery site"),
    (("dose", "tablet", "antibiotic", "paracetamol", "ibuprofen", "prescription"), "a pharmacist or the leaflet in the box"),
    (("battery", "charger", "router", "app", "software", "phone"), "the maker's support page"),
    (("mortgage", "overdraft", "pension", "tax", "benefit", "allowance"), "the official page, gov.uk or your bank"),
    (("lease", "landlord", "deposit", "tenancy"), "your contract or the council's housing team"),
    (("passport", "visa", "embassy", "renewal"), "the passport office's own site"),
    (("weed", "soil", "compost", "prune", "seedling", "plant"), "the RHS site or the plant's own label"),
    (("puppy", "kitten", "vet", "dog", "cat"), "your vet"),
    (("stitch", "sew", "hem", "zip", "fabric", "garment"), "the care label or a tailor"),
)

A_MOVE_WORDS = frozenset("""
    prick cut score slash stab turn stir cover uncover leave put add check wash rinse soak scrub use try
    rest shake season salt test taste wait keep freeze defrost empty clean wipe change replace
    trim peel chop slice mix whisk knead roll fill drain squeeze press
    bleed flush prime seal grease oil sand paint varnish glue screw tighten loosen unplug plug
    switch reset restart reboot charge update install download back defrost refrigerate reheat
    tin jar bottle label marinate brine gut bone stuff ice chill cool warm heat preheat blind
    line flour dust glaze baste carve prove rise fold beat cream sieve sift blend mash grate zest
    juice deseed core hull soak de-ice descale unblock plunge rod hoover vacuum mop dust sweep
    water feed prune repot stake tie mulch mow scarify aerate
""".split())

WHETHER_ASKS = (
    re.compile(r"\b(?:do|did)\s+i\s+(?:need|have|got)\s+(?:to\s+)?(?P<rest>[^?!]+)", re.I),
    re.compile(r"\bshould\s+i\s+(?:be\s+|just\s+|still\s+)?(?P<rest>[^?!]+)", re.I),
    re.compile(r"\bam\s+i\s+(?:meant|supposed)\s+(?:to\s+)?(?P<rest>[^?!]+)", re.I),
    re.compile(r"\bcan\s+i\s+(?:just|still|safely|even)?\s*(?P<rest>[^?!]+)", re.I),
    re.compile(r"\bis\s+it\s+(?:ok|okay|safe|alright|fine)\s+to\s+(?P<rest>[^?!]+)", re.I),
)


METHOD_ASKS = (
    re.compile(r"\b(?:will|would|does|do|did|is|are|can|could)\s+(?P<rest>[^?!]{3,40}?)\s+"
               r"(?:work|works|help|helps|do\s+anything|do\s+it|do\s+the\s+job|"
               r"(?:be\s+)?enough|(?:be\s+)?any\s+good|be\s+ok\b|be\s+okay|"
               r"be\s+worth\s+(?:it|doing))\b[^?!]*", re.I),
)
NOT_A_METHOD = frozenset("""
    it that this they those these there he she i we you one ones
""".split())

A_QUALITY = frozenset("""
    work works worked working better best help helps helped worth enough good fine okay ok
    safe still anymore actually really even than
""".split())


STILL_ASKS = re.compile(
    r"^(?:(?:and|but|so|or)\s+)?"
    r"(?P<aux>can|could|may|should|would)\s+(?P<who>i|we)\s+still\s+(?P<rest>[a-z].*)$", re.I)


def _whether_to(clean):
    for shape in WHETHER_ASKS:
        found = shape.search(clean)
        if not found:
            continue
        rest = " ".join(found.group("rest").split()).strip(" .,")
        words_of_it = rest.split()
        if not words_of_it or len(words_of_it) > 5:
            continue
        if words_of_it[0] not in A_MOVE_WORDS:
            continue
        return "whether to " + rest
    for shape in METHOD_ASKS:
        found = shape.search(clean)
        if not found:
            continue
        rest = " ".join(found.group("rest").split()).strip(" .,")
        words_of_it = rest.split()
        if not words_of_it or len(words_of_it) > 5:
            continue
        if words_of_it[0] in NOT_A_METHOD:
            continue
        return "whether to use " + rest
    found = STILL_ASKS.match(clean)
    if found:
        return ("whether " + found.group("who").lower() + " " + found.group("aux").lower()
                + " still " + " ".join(found.group("rest").split()).strip(" .,"))
    return ""


def _a_stem(word):
    word = str(word or "").lower()
    for suffix in ("ing", "ings", "ed", "es", "s"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 4:
            word = word[: -len(suffix)]
            break
    if word.endswith("e") and len(word) > 4:
        word = word[:-1]
    return word


NOT_A_SUBJECT = frozenset("""
    first thing things one ones rest bit part way ways sort kind lot next still even actually
    really everything anything something nothing else another
""".split())


def _the_chat_is_still_on(said, memory):
    words = set(re.findall(r"[a-z']+", str(said or "").lower()))
    words |= {word for word in _the_keys_of(said, memory) if len(word) > 2}
    words = {word for word in words
             if len(word) > 2 and word not in topics.STOPWORDS and word not in NOT_A_SUBJECT}
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return False
    last = turns[-1]
    for side in ("bot", "user"):
        here = {word for word in re.findall(r"[a-z']+", str(last.get(side) or "").lower())
                if len(word) > 2 and word not in topics.STOPWORDS
                and word not in NOT_A_SUBJECT}
        if words & here:
            return True
    return False


def _where_the_rest_is(said, memory, turn, ask=""):
    card_words = " ".join(re.findall(r"[a-z']+", str(said or "").lower()))
    card_words = (card_words + " " + " ".join(sorted(_the_keys_of(said, memory)))).strip()
    for needles, place in WHERE_TO_LOOK_WORDS:
        if any(re.search(r"\b" + word + r"\b", card_words) for word in needles):
            return place
    try:
        card_read = understand(str((turn or {}).get("user") or "")) or {}
        card_topic = str(card_read.get("topic") or "")
    except Exception:
        card_topic = ""
    if ask:
        try:
            ask_topic = str((understand(ask) or {}).get("topic") or "")
        except Exception:
            ask_topic = ""
        if card_topic and ask_topic and card_topic != ask_topic:
            return WHERE_TO_LOOK_DEFAULT
    return WHERE_TO_LOOK.get(card_topic, WHERE_TO_LOOK_DEFAULT)


def what_it_knows(text, memory):
    if not isinstance(memory, dict):
        return None
    clean = " ".join(str(text or "").lower().split()).strip(" ?!.")
    if not clean:
        return None
    whether = _whether_to(clean)
    if not whether:
        return None
    asked = [word for word in topics.words(" ".join(whether.split()[2:]))
             if len(word) > 2 and not word.isdigit() and word not in topics.STOPWORDS
             and word not in ASK and word not in ASK_VERB and word not in TIME
             and word not in FILLER and word not in SELF and word not in PART_STAND_INS]
    if not asked:
        return None
    seen_a_card = False
    gap = ""
    for back, turn in enumerate(reversed((memory.get("turns") or [])[-LOOK_BACK:]), 1):
        if not isinstance(turn, dict) or turn.get("module") != "answers":
            continue
        said = str(turn.get("bot") or "").strip()
        if not said or HEDGE.search(said) or said.rstrip().endswith("?"):
            continue
        if len(said) < 50:
            continue
        if set(asked) & _the_keys_of(said, memory):
            continue
        on_the_card = {_a_stem(word) for word in re.findall(r"[a-z']+", said.lower())}
        named = [word for word in asked if _a_stem(word) in on_the_card]
        missing = [word for word in asked
                   if _a_stem(word) not in on_the_card and word not in A_QUALITY]
        if named and not missing:
            for sentence in _sentences(said):
                sentence = sentence.strip().rstrip(" ;")
                if len(sentence.split()) < 4 or sentence.lower().endswith("?"):
                    continue
                if {_a_stem(word) for word in asked} & {
                        _a_stem(word) for word in re.findall(r"[a-z']+", sentence.lower())}:
                    head = sentence.split(":")[0] if ":" in sentence else sentence
                    if len(head.split()) < 4:
                        head = sentence
                    return head[:1].upper() + head[1:] + ("" if head[-1:] in ".!?\"" else ".")
            continue
        seen_a_card = True
        first_card = back <= 1 or not any(
            isinstance(t, dict) and t.get("module") == "answers"
            for t in (memory.get("turns") or [])[-back + 1:])
        if back > 1 and not _the_chat_is_still_on(said, memory):
            continue
        if (back > 1 and not first_card
                and not _about_the_same_thing(str(turn.get("user") or ""), said, memory)):
            continue
        move_words = [w for w in whether.split()[2:] if w not in PART_STAND_INS]
        on_the_card = {_a_stem(word) for word in re.findall(r"[a-z']+", said.lower())}
        if not move_words[1:]:
            continue
        part = ""
        lead = ""
        for sentence in _sentences(said):
            sentence = sentence.strip().rstrip(" ;")
            if len(sentence.split()) < 4 or sentence.lower().endswith("?"):
                if not lead and sentence and not sentence.lower().endswith("?") \
                        and len(sentence.split()) >= 2 and not NOT_ALONE.match(sentence):
                    lead = sentence
                continue
            if _already_repeated(sentence, memory):
                continue
            if {_a_stem(word) for word in asked} & {
                    _a_stem(word) for word in re.findall(r"[a-z']+", sentence.lower())}:
                return None
            part = sentence
            break
        look = _where_the_rest_is(said, memory, turn, ask=clean)
        if not look:
            return None
        if not part:
            gap = ("On " + whether + ", " + look + " will know more than I can - nothing I have"
                   " covers it.")
            continue
        head = part[:1].upper() + part[1:] + ("" if part[-1:] in ".!?\"" else ".")
        if lead:
            head = lead[:1].upper() + lead[1:] + " " + head
        if len(clean) % 2:
            return head + " On " + whether + ", " + look + " will know more than I can."
        return head + " That is what I can tell you; on " + whether + ", " + look + " will say."
    return gap or None


GAVE_ASKS = re.compile(
    r"\bwhat(?:'s|s|\s+(?:was|were|is|are))\s+(?:my|our|the)\b"
    r"|\bwhat\s+did\s+(?:i|we)\s+(?:say|tell)\b"
    r"|\bhow\s+(?:long|much|many|often|soon)\b"
    r"|\bwhat\s+was\s+it\s+(?:i|we)\b"
    r"|\bwhat(?:'s|s|\s+is|\s+are|\s+do|\s+does|\s+did)\s+(?:i|we|my|our)\s+"
    r"(?:(?:current|exact|actual)\s+)?"
    r"(?:earn|earns|earning|make|makes|paid|pay|pays|wage|wages|salary|salaries|income)\b", re.I)
ASK_FRAME = FIGURE_WORDS | frozenset("""
    said say says saying tell told telling mention mentioned remember remembers remember forgot
    recall earlier before after since again exactly actually probably guess think know my our
    the a an i we you it its thing things one ones number figure what whats which was were is are did
    do does have has had got left until till by about story now been
""".split())
A_FIGURE = re.compile(
    r"(?P<money>£\s?\d[\d,]*(?:\.\d+)?(?:\s?(?:k|grand|thousand|m)\b)?"
    r"|\b(?<![\d.])\d[\d,]*(?:\.\d+)?\s?(?:grand|k|quid|pounds?|dollars?|euros?|bucks)\b)"
    r"|(?P<time>\b(?<![\d.])\d[\d,]*(?:\.\d+)?\s*"
    r"(?:seconds?|secs?|minutes?|mins?|hours?|hrs?|days?|weeks?|wks?|months?|years?|nights?)\b"
    r"|\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s+"
    r"(?:seconds?|minutes?|hours?|days?|weeks?|months?|years?|nights?)\b"
    r"|\b(?:about\s+|around\s+|nearly\s+|over\s+|under\s+)?(?:a|an)\s+"
    r"(?:second|minute|hour|day|week|month|year|night)\b"
    r"|\b(?:a\s+)?(?:couple\s+of|few|couple)\s+"
    r"(?:seconds?|minutes?|hours?|days?|weeks?|months?|years?|nights?)\b"
    r"|\bhalf\s+an?\s+(?:hour|day|week|month)\b)"
    r"|(?P<share>\b(?<![\d.])\d[\d,]*(?:\.\d+)?\s?(?:%|per\s?cent\b|percent\b))"
    r"|(?P<count>\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"(?<![\d.])\d[\d,]*(?:\.\d+)?)\s+[a-z][a-z-]{2,}\b)"
    r"|(?P<amount>\b(?<![\d.])\d[\d,]{2,}\b)", re.I)
GAVE_LOOK_BACK = 8
PAY_FAMILY = frozenset("""earn earning earned pay paid pays payslip wage salary income make making
made takehome""".split())
A_PAY_WORD = re.compile(
    r"\b(?:earn|earns|earning|earnings|pay|pays|paid|wage|wages|salary|salaries|income|"
    r"make|makes|making|made)\b", re.I)
A_PAY_VERB_AT_THE_END = re.compile(r"\b(?:make|makes|earn|earns|paid|pay)\s*[.?!]*\s*$", re.I)
A_TAKE_HOME = re.compile(r"\btak(?:e|es|en|ing)\s+home\b", re.I)
A_IM_ON_A_FIGURE = re.compile(
    r"\b(?:i'?m|i am|we'?re|we are)\s+on\s+(?:about\s+|roughly\s+|around\s+)?"
    r"[\u00a3$£]?\s*\d", re.I)
A_PAY_JUDGEMENT = re.compile(
    r"\b(?:like|worth|enough|fair|reasonable|normal|average|typical|good|bad|ok|okay|"
    r"competitive)\b", re.I)
PAY_WHEN_WORDS = frozenset("""current currently presently now moment latest today exact exactly
    actual precisely roughly""".split())
A_MEASURE_WORD = frozenset("""
    day days night nights week weeks weekend weekends month months year years hour hours minute
    minutes morning mornings afternoon afternoons evening evenings time times while""".split())
A_DOING_WORD = frozenset("""going away off there gone staying travelled traveled travelling
    traveling returning back doing""".split())


FIGURE_NOUNS = frozenset("""target amount total figure count number budget price cost age date
    sum score""".split())
GOAL_NOUNS = frozenset("target goal aim objective ambition".split())
A_GOAL_LINE = re.compile(
    r"\b(?:save|saving|saved|need|needs|needed|want|wants|wanted|aim|aiming|goal|target|"
    r"objective|ambition|trying|try|plan|planning|afford)\b", re.I)
A_RATE_LINE = re.compile(
    r"\b\d[\d,.]*\s*(?:a|an|per|each|every)\s+"
    r"(?:day|week|month|year|fortnight)\b"
    r"|\b(?:a|per|each|every)\s+(?:day|week|month|year|fortnight)\b", re.I)
A_QUESTION = re.compile(
    r"\W*(?:how|what|which|when|where|who|why|do|did|does|can|could|should|would|will|shall|"
    r"is|are|was|were|have|has)\b", re.I)


A_WERE_ASKS = re.compile(
    r"\A\s*were\s+(?:i|you|we|they|he|she|it|there|any|all|none|not|this|these|those|either)\b",
    re.I)


def the_plain_line(line):
    text = str(line or "")
    if A_WERE_ASKS.match(text) or not re.match(r"\A\s*were\s+\w", text, re.I):
        return text
    return re.sub(r"\A(\s*)were\b", r"\1we are", text, count=1, flags=re.I)


A_RATE_OF_TIME = re.compile(
    r"(?:\d|\u00a3|\$|\u20ac)\s*$"
    r"|\b(?:once|twice|thrice|times|per|each|every|a|an)\s*$", re.I)
A_SCHEDULED_AFTER = re.compile(r"\s*(?:before|after|past|prior\s+to)\b", re.I)
A_HAS_THE_LENGTH = re.compile(r"\b(?:have|has|had|got|there's|there\s+are|there\s+is)\b", re.I)


NOT_A_FIGURE_ASK = re.compile(
    r"\b(?:called|named|call|spell|spelt|means?|stand\s+for)\b"
    r"|\btoo\s+(?:much|many)\b"
    r"|\benough\b|\bsafe\b|\bhealthy\b|\brecommend\b"
    r"|\b(?:is|are|was|were)\s+how\s+(?:many|much)\b"
    r"|\bhow\s+do\s+i\b"
    r"|\bhow\s+much\s+(?:have|has|did)\s+(?:i|we|they)\b"
    r"(?!\s+(?:say|said|tell|told|mention|mentioned))"
    r"|\b(?:in total|altogether|all together|so far)\b",
    re.I)
A_PLAN_ASK = re.compile(r"\b(?:should|can|could|shall)\s+(?:i|we)\b", re.I)
A_THE_PLAN_ASK = re.compile(
    r"\bwhat(?:'s|s|\s+is|\s+are|\s+was|\s+were)?\s+(?:the|a|our|my)\s+plan\b"
    r"|\bwhat\s+(?:do|does|should)\s+(?:i|we)\s+do\s+(?:first|next)\b", re.I)
A_THING_NAMED_AFTER_THE_CUE = re.compile(
    r"\b(?:did|do|does|was|were|am|are)\s+(?:i|we)\s+"
    r"(?:say|said|tell|told|think|want|wanted|need|needed|do|does|did)?\s*"
    r"(?:the|a|an|my|our|his|her|their|your)\s+[a-z]", re.I)
A_BARE_AMOUNT_ASK = re.compile(
    r"\bhow\s+much\s+(?:was|is|were|are)\s+(?:it|that|this|they|those|these)"
    r"\s*(?:again|now|then)?\s*[.?!]*\s*\Z"
    r"|\bhow\s+much\s+(?:did|do|does)\s+(?:i|we)\s+(?:say|need|want|have|owe|pay|spend|agree)"
    r"\s*(?:again|now|then|already|so\s+far|in\s+total|altogether|for\s+it)?\s*[.?!]*\s*\Z"
    r"|\bremind\s+me\s+how\s+much\b", re.I)
A_BARE_DURATION_ASK = re.compile(
    r"\bdid\s+i\s+(?:say|want|choose|pick)\b"
    r"|\bhow\s+long\s+(?:am|are|was|were)\s+(?:i|we)\s+"
    r"(?:going|away|out|there|staying|off)\b"
    r"|\bhow\s+long\s+have\s+i\s+had\b|\bhave\s+i\s+had\b"
    r"|\bhow\s+long\s+(?:has|have)\s+(?:it|that|this)\s+been\b"
    r"|\bhow\s+long\s+(?:was|is)\s+(?:it|that)\b", re.I)
A_HOW_LONG_ITS_BEEN = re.compile(
    r"\bhow\s+long\s+(?:has|have|had)\s+(?:[\w']+\s+){1,5}been\s+"
    r"(?:like\s+(?:this|that)|going\s+on|that\s+way|this\s+way|now|so\s+far)\b", re.I)
_OWNS_THE_THING = re.compile(r"\b(?:my|our|his|her|their|the)\b", re.I)


def how_long_its_been(text):
    found = A_HOW_LONG_ITS_BEEN.search(" ".join(str(text or "").lower().split()))
    return bool(found and _OWNS_THE_THING.search(found.group(0)))
A_LINE_THAT_ASKS = re.compile(
    r"\A(?:\W*(?:and|but|so|ok|okay|also|then|well|now|hmm|oh|yeah|yes|right|actually|sorry|"
    r"plus|just)\b[\s,]*)*" + A_QUESTION.pattern, re.I)
A_CORRECTION = re.compile(
    r"^[\s,.\-]*(?:(?:oh|ok|okay|and|but|so|well|sorry|no|nope|actually|wait|oops|correction|"
    r"my mistake|it'?s)\b[\s,;:.-]*){1,3}"
    r"|^[\s,.\-]*(?:make\s+(?:it|that)|i\s+mean|we\s+mean|scratch\s+that|i\s+meant|"
    r"we\s+meant)\b", re.I)
A_MARKER_AT_THE_END = re.compile(r"\s+(?:actually|really|honestly)\s*[.!?]*\s*$", re.I)

def _a_line_that_corrects(line):
    said = str(line or "")
    if A_CORRECTION.search(said):
        return True
    found = A_MARKER_AT_THE_END.search(said)
    if found is None:
        return False
    head = said[:found.start()].strip()
    if not head or len(head.split()) > 8:
        return False
    return not facts.extract(head)

A_NUMBER_WORD = re.compile(
    r"\b(?:\d[\d,]*(?:\.\d+)?|one|two|three|four|five|six|seven|eight|nine|ten|eleven|"
    r"twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|"
    r"forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand)\b", re.I)
JOINERS = frozenset("""a an the and or but so of to in on at for with from by as then that this
    is are was were it them us you""".split())
FIGURE_TAIL = JOINERS | frozenset("""because cos coz cuz cause since""".split())

A_ONE_MORE = re.compile(r"\b(?:more|extra|other|others|fewer|less)\b", re.I)
A_GAIN = re.compile(
    r"\b(?:one|two|three|four|\d+|another)\s+(?:more|extra|other)\b"
    r"|\banother\s+(?:one|guest|person|adult|kid|child|friend|mate|of)\b"
    r"|\bplus\s+(?:one|two|three|\d+)\b|\bone\s+of\s+(?:my|our)\b", re.I)
A_GROUP_WORD = re.compile(r"\b(?:us|we|them|they|people|guests?|party)\b", re.I)
A_LOSS = re.compile(
    r"\b(?:died|passed away|put (?:him|her|it|them) down|gave\b[^.?!]{0,20}\baway"
    r"|rehomed|sold|stolen|went missing|ran away|eaten|no longer|not any ?more)\b"
    r"|\bone\s+of\s+(?:them|those|these|the)\b|\bgave\s+one\b|\bone\s+(?:away|off|back)\b",
    re.I)


_A_AGE = r"(?:\d[\d,]*(?:\.\d+)?|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)"
A_LIST_OF_AGES = re.compile(
    r"\b(?:aged?|ages)\s*" + _A_AGE + r"\b\s*(?:and|&|,)\s*" + _A_AGE + r"\b"
    r"|\b" + _A_AGE + r"\b\s*(?:and|&|,)\s*" + _A_AGE
    + r"\b\s*(?:years?|yrs?)(?:\s+old)?\b",
    re.I)


def _a_list_of_ages(line):
    return bool(A_LIST_OF_AGES.search(str(line or "")))


def _something_gone(lines, at, words):
    for later in lines[at + 1:]:
        if not later:
            continue
        if A_GAIN.search(later) and A_GROUP_WORD.search(later):
            return True
        if not A_LOSS.search(later):
            continue
        said = topics.keywords(later)
        if any(_the_same_word(word, other) for word in words for other in said):
            return True
        if "one" in A_LOSS.search(later).group(0).lower():
            return True
    return False


COUNT_ASK = re.compile(r"\bhow\s+many\s+([a-z'&-]+(?:\s+[a-z'&-]+){0,3})", re.I)
PERIOD_WORD = frozenset("""hour hours day days week weeks fortnight fortnights month months
    year years night nights morning mornings evening evenings weekend weekends christmas""".split())
A_RATE_IN_THE_FIGURE = re.compile(
    r"\b(?:once|twice|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d+)\s+times?\b"
    r"|\bevery\s+(?:\w+\s+)?(?:hour|day|week|fortnight|month|year|morning|evening|night|weekend)\b",
    re.I)


THE_SAME_NUMBER = {
    "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7",
    "eight": "8", "nine": "9", "ten": "10", "eleven": "11", "twelve": "12", "fifteen": "15",
    "twenty": "20", "thirty": "30", "forty": "40", "fifty": "50", "sixty": "60",
    "seventy": "70", "eighty": "80", "ninety": "90", "hundred": "100", "thousand": "1000",
}
A_PLURAL_ONLY_NOUN = frozenset("""people children men women feet teeth""".split())


def _the_ask_gave_that_figure(number, clean):
    number = str(number or "").strip().lower()
    if not number:
        return False
    first = number.split()[0]
    looked = {first, THE_SAME_NUMBER.get(first, first)}
    for other in A_NUMBER_WORD.findall(clean):
        if other == first or THE_SAME_NUMBER.get(other, other) in looked:
            return True
        if other[:1].isalpha() and first[:1].isalpha() and _the_same_word(first, other):
            return True
    return False


def _a_count_of_one_with_a_plural(number, noun):
    if str(number).strip().lower() not in ("1", "one", "a", "single"):
        return False
    word = (noun.split() or [""])[-1].lower()
    if not word:
        return False
    return word in A_PLURAL_ONLY_NOUN or word.endswith("s")


def _the_thing_counted(clean, said):
    match = COUNT_ASK.search(clean)
    if not match:
        return ""
    phrase = match.group(1).split()
    words = [word for word in phrase
             if word not in topics.STOPWORDS and word not in ASK_FRAME
             and word not in FIGURE_NOUNS]
    if not words:
        return ""
    tail = said.split()[-1].lower()
    for one, other in zip(phrase, phrase[1:]):
        if other in words and _the_same_word(one, tail):
            return one + " " + other
    for word in words:
        if _the_same_word(word, tail):
            return word
    return words[-1]


def _figures_in(line):
    text = str(line or "")
    if not text or "?" in text or A_QUESTION.match(text):
        return []
    out = []
    for match in A_FIGURE.finditer(text):
        if match.group("time") and A_RATE_OF_TIME.search(text[:match.start()]):
            continue
        if (match.group("time") and A_SCHEDULED_AFTER.match(text[match.end():])
                and not A_HAS_THE_LENGTH.search(text[:match.start()])):
            continue
        said = " ".join(match.group(0).split()).rstrip(" ,.;:")
        if not said:
            continue
        if match.group("count") and A_ONE_MORE.match(" ".join(said.split()[1:])):
            continue
        try:
            whose, _who = facts.subject(text, match.start())
        except Exception:
            whose = ""
        if whose == "other":
            continue
        counted = match.group("count") is not None
        kind = "time" if match.group("time") else "amount"
        if match.group("share"):
            digits = re.match(r"\s*([\d][\d,]*(?:\.\d+)?)", match.group(0))
            number = digits.group(1) if digits else said
            out.append((kind, number + " per cent", number, False))
            continue
        if counted and said.lower().endswith(" per"):
            said = said[:-4].rstrip(" ,.;:")
        words = said.split()
        while len(words) > 1 and words[-1].lower() in FIGURE_TAIL:
            words.pop()
        said = re.split(r"(?<!\d),|,(?!\d)", " ".join(words))[0]
        said = said.rstrip(" ,.;:")
        number = (said.split()[0] if counted else said).rstrip(" ,.;:")
        if not number:
            continue
        out.append((kind, said, number, counted))
    return out


_MONEY_PAID_FOR = re.compile(
    r"\b(?:paid|pay|pays|spent|spend|cost|costs|charged|gave|give|offered|quoted|put|set)\b"
    r"[^.?!]{0,25}?[\u00a3$\u20ac]?\s?\d[\d.,]*[^.?!]{0,25}?\b(?:for|on|towards)\b", re.I)
_AN_AMOUNT_WANTED = re.compile(
    r"\bhow\s+(?:much|many)\b|\bcost\b|\bcosts\b|\bprice\b|\bpaid\b|\bpay\b"
    r"|\bspent\b|\bspend\b|\bbudget\b|\bfee\b|\btotal\b|\bworth\b", re.I)


def _money_paid_for_a_thing(clean, line):
    if _AN_AMOUNT_WANTED.search(clean):
        return False
    return bool(_MONEY_PAID_FOR.search(line))


def _one_figure(found, kind):
    if not found:
        return ()
    if kind:
        found = [one for one in found if one[0] == kind]
    elif len({one[0] for one in found}) > 1:
        return ()
    return found[0] if found else ()


def _a_bare_count(figure):
    words = str(figure or "").split()
    return len(words) == 1 and bool(A_NUMBER_WORD.fullmatch(words[0]))


def _the_same_word(one, other):
    first, second = topics.stem(one), topics.stem(other)
    if first == second:
        return True
    if topics.forms(first) & topics.forms(second):
        return True
    for shorter, longer in ((first, second), (second, first)):
        if longer.endswith("room") and longer[:-4] == shorter:
            return True
    if first in PAY_FAMILY and second in PAY_FAMILY:
        return True
    return (len(first) >= 4 and len(second) >= 4
            and (first.startswith(second) or second.startswith(first)))


def _the_corrected(lines, at, kind, found):
    for later in lines[at + 1:]:
        if not later or not _a_line_that_corrects(later) or A_LINE_THAT_ASKS.search(later):
            continue
        got = _one_figure(_figures_in(later), kind)
        if got:
            found = got
        elif A_NUMBER_WORD.search(later) and kind != "time":
            return ()
    return found


A_TOLD_BACK = re.compile(
    r"\b(?:did\s+i\s+(?:say|tell|mention)|what\s+did\s+i\s+(?:say|tell)"
    r"|what\s+was\s+it\s+i\s+(?:said|told)|how\s+(?:long|many|much)\s+did\s+i\s+(?:say|tell))\b",
    re.I)
NOT_A_THING_ASKED = frozenset((
    "sorry", "apologise", "apologize", "going", "told", "tell", "said", "say", "mention",
    "remember", "again", "asked", "ask"))


def _the_length_they_mean(clean, lines, spoken=()):
    wanted = [word for word in topics.keywords(clean)
              if word not in ASK_FRAME and word not in NOT_A_THING_ASKED]
    if wanted and spoken:
        theirs = [other for line in lines for other in topics.keywords(line)]
        heard = [other for line in spoken for other in topics.keywords(line)]
        new = [word for word in wanted
               if not any(_the_same_word(word, other) for other in theirs)]
        if new and all(any(_the_same_word(word, other) for other in heard) for word in new):
            wanted = []
    named, anywhere = [], []
    for back, line in enumerate(lines):
        if A_LINE_THAT_ASKS.search(line):
            continue
        figures = [one for one in _figures_in(line) if one[0] == "time"]
        if not figures:
            continue
        anywhere.append((back, figures))
        words = topics.keywords(line)
        if any(_the_same_word(word, other) for word in wanted for other in words):
            named.append((back, figures))
    for pool in ((named,) if wanted else (named, anywhere)):
        if not pool:
            continue
        distinct = {one[1].lower() for _back, figures in pool for one in figures}
        if len(distinct) == 1:
            back, figures = pool[-1]
            later = _the_corrected(lines, back, "time", figures[-1])
            return (later or figures[-1])[1]
        if A_CORRECTION.search(lines[pool[-1][0]]):
            return pool[-1][1][-1][1]
    return ""


def _the_figure_of_a_goal(lines, kind, wanted=()):
    for at, line in enumerate(lines):
        if not line or A_LINE_THAT_ASKS.search(line) or not A_GOAL_LINE.search(line):
            continue
        if A_RATE_LINE.search(line):
            continue
        words = topics.keywords(line)
        narrowing = [word for word in wanted if word not in GOAL_NOUNS]
        if not all(any(_the_same_word(word, other) for other in words) for word in narrowing):
            continue
        found = _one_figure(_figures_in(line), kind)
        if not found and kind is None:
            found = _one_figure(_figures_in(line), "amount")
        if found:
            return _the_corrected(lines, at, kind, found)
    return ()

def _the_figure_counts_the_thing(text, figure):
    thing = history.the_thing_they_named(text)
    if not thing:
        return True
    named = set(topics.content(thing))
    return bool(named & set(topics.content(str(figure or ""))))


A_NARROWING_ONLY = re.compile(
    r"""^(?:(?:ok|okay|and|or|also|but|then|so|just|only|maybe|actually)[\s,]+)*
        (?:
            (?:the|those|these|any|some|other|both|all)(?:\s+[a-z']+){0,3}\s+(?:one|ones)
          | (?:one|ones)
          | [a-z']+\s+(?:one|ones)
          | (?:something|anything|everything)\s+[a-z']+
          | (?:not|no)\s+(?:too|very|that|so|more|as)\s+[a-z']+
          | (?:a\s+bit\s+)?(?:cheaper|closer|nearer|bigger|smaller|longer|shorter|quicker|faster|
                easier|simpler|warmer|colder|quieter|lighter|nicer|better|worse)\b
          | (?:since|before|after|from|until|till|by|around|near|in|on|at)\s+[\w' ]{1,24}
        )
        (?:\s+[a-z']+)*
        \s*[.!]?$""", re.I | re.X)

A_NARROWING_WORDS = 7

def a_narrowing_and_its_line(line, memory):
    said = " ".join(str(line or "").split())
    if not said or "?" in said or len(said.split()) > A_NARROWING_WORDS:
        return None
    if not A_NARROWING_ONLY.match(said):
        return None
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return None
    lines = [" ".join(str(turn.get("user") or "").split()) for turn in turns
             if isinstance(turn, dict)]
    places = [at for at, text in enumerate(lines) if text == said]
    if not places or not places[-1]:
        return None
    before = lines[places[-1] - 1]
    if (not before or "?" in before or len(before.split()) < 2
            or not topics.content(before) or A_NARROWING_ONLY.match(before)):
        return None
    return before, said

def _the_turn_that_names_it(text, memory):
    row = history.the_earlier_turn(memory, text)
    line = " ".join(str((row or {}).get("user") or "").split()).rstrip(" .!?")
    if not line:
        return None
    pair = a_narrowing_and_its_line(line, memory)
    if pair:
        before, after = pair
        return pick(["You said: \"" + before + "\" \u2014 then \"" + after + "\".",
                     "Your own words were: \"" + before + "\", then \"" + after + "\".",
                     "That was: \"" + before + "\" \u2014 then \"" + after + "\"."], memory)
    return pick(["You said: \"" + line + "\"",
                 "Your own words were: \"" + line + "\"",
                 "That was: \"" + line + "\""], memory)


def the_figure_they_gave(text, memory):
    if not isinstance(memory, dict):
        return None
    clean = " ".join(str(text or "").lower().split())
    if not clean or len(clean.split()) > 16 or not GAVE_ASKS.search(clean):
        return None
    if NOT_A_FIGURE_ASK.search(clean):
        return None
    counting = COUNT_ASK.search(clean)
    if counting:
        counted = counts.answer(clean, memory)
        if counted:
            return counted
        if any(word in counts.THEIRS for word in counting.group(1).split()):
            return None
    wanted = [word for word in topics.keywords(clean) if word not in ASK_FRAME]
    if A_PAY_WORD.search(clean):
        wanted = [word for word in wanted if word not in PAY_WHEN_WORDS]
    if not wanted and A_PAY_WORD.search(clean) and A_PAY_VERB_AT_THE_END.search(clean):
        wanted = ["pay"]
    if len(wanted) > 4:
        return None
    goal_named = any(word in GOAL_NOUNS for word in wanted)
    kind = None
    for name in ("often", "time", "heat", "amount"):
        for one_name, ask, _figure in FIGURE_ASKS:
            if one_name == name and ask.search(clean):
                kind = name
                break
        if kind:
            break
    if kind in (None, "amount", "heat") and (A_PLAN_ASK.search(clean)
                                             or A_THE_PLAN_ASK.search(clean)):
        return None
    all_lines = [the_plain_line(str(turn.get("user") or "")) for turn in (memory.get("turns") or [])
                 if isinstance(turn, dict)]
    lines = all_lines[-GAVE_LOOK_BACK:]
    spoken = [str(turn.get("bot") or "") for turn in (memory.get("turns") or [])
              if isinstance(turn, dict)][-GAVE_LOOK_BACK:]
    if kind == "time" and A_TOLD_BACK.search(clean):
        said = _the_length_they_mean(clean, lines, spoken)
        if said:
            if not _the_figure_counts_the_thing(clean, said):
                return _the_turn_that_names_it(text, memory)
            return pick(["You said " + said + ".",
                         said[:1].upper() + said[1:] + " \u2014 that's what you told me."],
                        memory)
    if goal_named:
        found = _the_figure_of_a_goal(all_lines, kind, wanted)
        if found:
            figure = found[1]
            return pick(["You said " + figure + ".",
                         figure[:1].upper() + figure[1:] + " \u2014 that's what you told me."],
                        memory)
    if wanted:
        said = [other for line in lines for other in topics.keywords(line)]
        said += ["takehome" for line in lines if A_TAKE_HOME.search(line)]
        said += ["pay" for line in lines if A_IM_ON_A_FIGURE.search(line)]
        kept = [word for word in wanted
                if any(_the_same_word(word, other) for other in said)]
        named = [word for word in wanted
                 if word not in A_MEASURE_WORD and word not in A_DOING_WORD]
        if named and not any(word in kept for word in named):
            return None
        if A_PAY_WORD.search(clean) and (A_PAY_JUDGEMENT.search(clean)
                                         or len(kept) < len(wanted)):
            return None
        if not A_THING_NAMED_AFTER_THE_CUE.search(clean):
            wanted = kept
    if _the_store_keeps_this_figure(clean, memory):
        return None
    if not wanted:
        bare = (A_BARE_AMOUNT_ASK.search(clean) if kind == "amount"
                else A_BARE_DURATION_ASK.search(clean) if kind == "time" else None)
        if not bare:
            return None
        found = [(back, one[1]) for back, line in enumerate(lines)
                 if not A_LINE_THAT_ASKS.search(line)
                 for one in _figures_in(line) if one[0] == kind]
        distinct = {one.lower() for _back, one in found}
        if len(distinct) != 1:
            corrected = [one for back, one in found if A_CORRECTION.search(lines[back])]
            if not corrected or found[-1][1] != corrected[-1]:
                return None
            figure = corrected[-1]
        else:
            figure = found[0][1]
        if not _the_figure_counts_the_thing(clean, figure):
            return _the_turn_that_names_it(text, memory)
        return pick(["You said " + figure + ".",
                     figure[:1].upper() + figure[1:] + " \u2014 that's what you told me."],
                    memory)
    best = None
    for back in range(len(lines) - 1, -1, -1):
        line = lines[back]
        if not line or A_LINE_THAT_ASKS.search(line):
            continue
        said = topics.keywords(line)
        if A_TAKE_HOME.search(line):
            said = said + ["takehome"]
        if A_IM_ON_A_FIGURE.search(line):
            said = said + ["pay"]
        core = [word for word in wanted if word not in FIGURE_NOUNS] or wanted
        if not all(any(_the_same_word(word, other) for other in said) for word in core):
            continue
        shared = [word for word in wanted
                  if any(_the_same_word(word, other) for other in said)]
        figures = _figures_in(line)
        found = _one_figure(figures, kind)
        if not found:
            continue
        beside = _the_figure_beside_the_thing(figures, core)
        if beside:
            found = beside
        if COUNT_ASK.search(clean) and _a_list_of_ages(line):
            continue
        if _money_paid_for_a_thing(clean, line):
            continue
        found = _the_corrected(lines, back, kind, found)
        if not found:
            continue
        many = _every_figure_the_ask_names(wanted, line, kind)
        last = (found[1].split() or [""])[-1]
        if _something_gone(lines, back, [word for word in said if word in shared] + [last]):
            continue
        score = (len(shared), back)
        if best is None or score > best[0]:
            best = (score, found, shared, many)
    if best is None:
        return None
    _score, (kind_of, said, number, counted), shared, many = best
    if many:
        return pick(["You said " + many + ".",
                     many[:1].upper() + many[1:] + " \u2014 that's what you told me."], memory)
    noun = _the_thing_counted(clean, said) if counted else ""
    if (counted and noun and noun.split()[-1].lower() in PERIOD_WORD
            and A_RATE_IN_THE_FIGURE.search(said)):
        return None
    if noun and number.lower() in ("1", "one") and noun.endswith("s") and not noun.endswith("ss"):
        noun = noun[:-1]
    figure = (number + " " + noun).strip() if noun else said
    if _the_ask_gave_that_figure(number, clean):
        return None
    if noun and _a_count_of_one_with_a_plural(number, noun):
        return None
    if not _the_figure_counts_the_thing(clean, figure):
        return _the_turn_that_names_it(text, memory)
    if _a_bare_count(figure):
        return pick(["You said " + figure + ".", figure + ", as you said."], memory)
    return pick(["You said " + figure + ".",
                 figure[:1].upper() + figure[1:] + " \u2014 that's what you told me."], memory)

A_FIGURE_WORD = re.compile(
    r"\d|\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen|twenty"
    r"|thirty|forty|fifty|sixty|ninety|hundred|thousand)\b", re.I)


def _the_store_keeps_this_figure(clean, memory):
    if not isinstance(memory, dict):
        return False
    asked = set(topics.keywords(clean))
    if not asked:
        return False
    for entry in reversed(list(memory.get("facts_log") or [])):
        if not isinstance(entry, dict):
            continue
        value = " ".join(str(entry.get("value") or "").split())
        if not value or not A_FIGURE_WORD.search(value):
            continue
        key_words = topics.keywords(str(entry.get("key") or "").replace("_", " "))
        if not key_words:
            continue
        if not any(_the_same_word(word, other) for word in key_words for other in asked):
            continue
        said_on = str(entry.get("text") or "")
        if said_on and A_LINE_THAT_ASKS.search(said_on):
            continue
        return True
    return False


A_RECALL_CUE = recall.LOOKS_BACK


A_POINTS_BACK_HARD = re.compile(
    r"\b(?:again|remind\w*|remember|recall|earlier|same\s+(?:again|one))\b"
    r"|\b(?:you|u)\s+(?:said|told)\b|\btold\s+me\b"
    r"|\bwhat(?:'s|s|\s+is|\s+are|\s+was|\s+were)?\s+(?:my|our)\b"
    r"|\bwhat\s+did\s+(?:i|we)\s+(?:say|tell)\b"
    r"|\b(?:am|are|did|do|does|was|were|have|has|had)\s+(?:i|we)\b", re.I)


def _the_figure_beside_the_thing(figures, words):
    for figure in figures:
        beside = topics.keywords(figure[1])
        if any(_the_same_word(word, other) for word in words for other in beside):
            return figure
    return None


def _every_figure_the_ask_names(wanted, line, kind):
    named = [word for word in wanted if word not in ASK_FRAME and word not in FIGURE_NOUNS]
    if len(named) < 2:
        return ""
    figures = [one for one in _figures_in(line) if not kind or one[0] == kind]
    if len(figures) < 2:
        return ""
    taken = []
    for word in named:
        for figure in figures:
            if figure in taken:
                continue
            if any(_the_same_word(word, other) for other in topics.keywords(figure[1])):
                taken.append(figure)
                break
    if len(taken) < 2:
        return ""
    parts = [figure[1] for figure in taken]
    return ", ".join(parts[:-1]) + " and " + parts[-1]


def asked_back(text, memory):
    if not isinstance(text, str) or not isinstance(memory, dict):
        return None
    if not recall.looks_back(text):
        return None
    if not A_POINTS_BACK_HARD.search(text) and recall.the_earlier_turn(text, memory) is None:
        return None
    figure = the_figure_they_gave(text, memory)
    if figure:
        return figure
    try:
        from . import counts as _counts
        said = _counts.answer(text, memory)
    except Exception:
        return None
    return said or None


def carries_the_figure(figure, reply):
    said = str(reply or "")
    numbers = re.findall(r"\d[\d,]*", str(figure or ""))
    if numbers:
        for number in numbers:
            if not re.search(r"(?<![\d,.])" + re.escape(number) + r"(?!\d)", said):
                return False
        return True
    words = [word for word in topics.keywords(figure) if not word.isdigit()]
    low = said.lower()
    return bool(words) and all(word in low for word in words)


CHANGED_IT = re.compile(
    r"\b(?:actually|instead|changed|change of plan|moved it|moved to|now it'?s|now we'?re|"
    r"no longer|swapped|postponed|cancell?ed|put it back|make it|makes it|we'?ve moved)\b", re.I)


def _the_same_words(one, other):
    def bare(line):
        return " ".join(re.sub(r"[^a-z0-9]+", " ", str(line or "").lower()).split())
    return bare(one) == bare(other) and len(bare(one).split()) >= 4


def _shortened(said):
    said = " ".join(str(said or "").split())
    if len(said) <= 320:
        return said
    kept = ""
    for part in _sentences(said):
        if kept and len(kept) + len(part) > 320:
            break
        kept = (kept + " " + part).strip()
    return kept or said


def _the_answer_again(said, memory):
    framed = topics.said_again(said, memory)
    if framed:
        return framed
    return topics.REPEAT[0].format(reply=_shortened(said))


def the_same_question_again(text, memory):
    if not isinstance(memory, dict):
        return None
    turns = memory.get("turns")
    if not isinstance(turns, list) or len(turns) < 3:
        return None
    clean = str(text or "").strip()
    if len(clean.split()) < 4:
        return None
    for back, turn in enumerate(reversed(turns[:-2])):
        if not isinstance(turn, dict):
            continue
        if not _the_same_words(clean, turn.get("user")):
            continue
        said = str(turn.get("bot") or "").strip()
        if not said or len(said) < 40:
            continue
        if HEDGE.search(said) or said.rstrip().endswith("?"):
            continue
        index = len(turns) - 2 - back
        between = [str((t or {}).get("user") or "") for t in turns[index + 1:-1]
                   if isinstance(t, dict)]
        if any(CHANGED_IT.search(line) for line in between):
            return None
        return _the_answer_again(said, memory)
    return None
