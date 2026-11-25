
import re

PICK = "pick"
OPTIONS = "options"
AMOUNT = "amount"
TIME = "time"
STEPS = "steps"
YESNO = "yesno"
VAGUE = "vague"
RECALL = "recall"
PAPERWORK = "paperwork"
REASON = "reason"
ADVICE = "advice"

PICK_LINES = (
    "I can't pick for you, but two questions settle most choices like this: which one you would "
    "still choose in a year, and which is cheaper to undo if it turns out wrong. Which way are "
    "you leaning?",
    "There is no right answer I can point you at. What every pick like this comes down to is what "
    "you will use most, and whether the cheaper one is good enough for that. What are you down to "
    "choosing between?",
    "Two ways to choose: the one that is best at the main thing, or the one that is decent at "
    "everything. Most people regret the second. What would it have to be good at?",
)
PICK_LINES_NAMED = tuple(line for line in PICK_LINES if "choosing between" not in line)

OPTIONS_LINES = (
    "I have no list to hand you, and I would rather not invent one. What makes a shortlist worth "
    "anything is that the choices are actually different: one cheap, one that lasts, one that is "
    "least effort. Which of those three are you after?",
    "Nothing in front of me to suggest from. Tell me the two or three things that are fixed - "
    "where, when, how much - and I can say what sort of option fits them. Which is the one that "
    "cannot move?",
    "I can't give you a list without making it up. The useful question is what you would say no to: "
    "once that is settled there are usually only two or three options left. What is a no?",
)

AMOUNT_LINES = (
    "I haven't got a figure for that, and guessing one would be worse than none. A number like this "
    "is worked out from two or three others rather than looked up - give me those and I will do the "
    "sums with you. What have you got to go on?",
    "That is arithmetic more than a fact. Tell me the size of it, how many there are, and what it is "
    "per one, and I will work the total out with the steps shown so you can check them. Which of "
    "those do you have?",
    "No number from me without the figures it comes from - that is what stops it being a guess. "
    "What numbers do you already have?",
)

TIME_LINES = (
    "I don't know the size of the job, so any time I gave you would be a guess. Most things like "
    "this are minutes for the small version and a day or more for the big one, and which one you "
    "have is the whole question. How big is it?",
    "That depends on what somebody finds once they start, which is why nobody will give you a firm "
    "number before they look. Ask for the usual time and add half again. Who is doing it?",
    "No honest number from me without knowing the size and who does it. If it is the simple "
    "version it is quick; if anything has to be taken out first it is not. What has to happen?",
)

YESNO_LINES = (
    "I can't say yes or no to that honestly. The test I would use is the worst that happens if it "
    "goes wrong, and how easily you could undo it. If both are small, it is worth a try - how bad "
    "is the worst case?",
    "That is yours to weigh, and I don't have the details to weigh it for you. It comes down to "
    "what you would lose, how likely that is, and whether you could put it back. What would you "
    "lose at worst?",
    "No verdict from me on this one - I would be guessing. Say what would make you change your "
    "mind, and if nothing would, that is your answer already. What would change it?",
)

REASON_LINES = (
    "I don't know this one well enough to say why, and a made-up reason is worse than none. Cases "
    "like it usually have two or three causes, and the way to tell which is yours is what else "
    "happens at the same moment. What else have you noticed?",
    "No cause I could name honestly. The reliable way to find one is to change a single thing at a "
    "time and see whether it goes away - two changes at once tells you nothing. What have you "
    "tried?",
    "I would be guessing at the reason. Whatever it is, it will have a before and after: what was "
    "different the first time it happened?",
)

ADVICE_LINES = (
    "I can't tell you what to do here - I haven't got the details, and it is yours to decide. "
    "Which is the option you keep coming back to? I will argue the other side properly.",
    "No advice worth the name from me on this. The question that usually settles it is the one you "
    "would regret not asking. Which is it?",
    "I don't know enough to say what is right. Put it into one sentence - the choice, and what it "
    "costs - and I will help you look at it from the outside. What is the choice?",
)


VAGUE_LINES = (
    "Give me a little more and I'll answer that part properly - what are you after?",
    "Happy to keep going - which part do you want next?",
    "That one is too open for me to answer well, and a guess would waste your time. Which bit "
    "matters most?",
    "One more line and I'll have something useful for you. What are you after now?",
)
_A_VAGUE = re.compile(
    r"^(?:and|so|ok|okay|right|well|hmm|um)?\s*,?\s*(?:now\s+what|what\s+now|now)\b[\s?!.]*$"
    r"|^what should i (?:think about|be doing(?: now)?|do next|do first)\b[\s?!.]*$"
    r"|^what do i do now\b[\s?!.]*$")

_WHAT_TO_DO_WITH = re.compile(r"\bwhat (?:should|shall|do|would|can|will) (?:i|we) (?:do|use|put)\b"
                               r"[^?.!]{0,20}?\b(?:with|about)\b")
_A_WHAT_WAS_IT = re.compile(
    r"^\s*(?:and\s+|so\s+)?(?:what|which)\s+(?:was|is|were|are)?\s*(?:the\s+)?(?:year|one|name|number|date"
    r"|day|time|age|colour|color"
    r"|brand|make|model|price|word|thing)\b"
    r"|\bwhat\b[^?.!]{0,24}?\b(?:did|do) (?:i|we) (?:say|tell|mention)\b"
    r"|\bremind me\b|\bwhat did (?:i|we|he|she|they|you) (?:say|tell|decide|choose|pick)\b"
    r"|\b(?:what|which)\b[^?.!]{0,30}?\bagain\b")
_A_THEY_SAID_SO = re.compile(r"\b(?:i|we)\s+(?:say|said|say\s+it|told\s+you|mention|mentioned)\b"
                             r"|\bagain\b|\bremind\s+me\b")
_A_FREQUENCY = re.compile(r"\bhow (?:many|often)\b[^?.!]{0,24}?\b(?:days|nights|times|weeks|months|"
                          r"years)\b[^?.!]{0,12}?\b(?:a|per|each)\b")
_AN_ASK_AT_THE_FRONT = re.compile(r"^(?:ok\s+|okay\s+|and\s+|so\s+|but\s+|also\s+)?(?:which|what|"
                                  r"should|shall|would|could|can|do|did|is|are|am|i|we|im|i'm|were|"
                                  r"we're|cant|can't|help|how|any|got)\b")
_WHICH_I_NEED = re.compile(r"\bwhich\b[^?.!]{0,24}?\b(?:do|would|will|should|shall)\s+(?:i|we)\s+"
                           r"(?:need|use|get for|ask for|call)\b")

RECALL_LINES = (
    "That is one for between us rather than a search - say it once more and I will answer from "
    "what you tell me. What was it?",
    "I would rather have it from you than guess: say it again and I will hold on to it. Which one "
    "was it?",
    "Say it once more and I will keep it this time, then answer straight from that. What was it?",
)

PAPERWORK_LINES = (
    "That one is on the paperwork, not out where I can see it - the renewal date sits near the "
    "policy number on the letter or in your account online. What does it say?",
    "The date is in their hands rather than mine: it is on the notice they last sent you, beside "
    "the reference number. Have you still got it?",
    "I can't see your own documents, so the date is on the letter or in the app under the plan. "
    "What date does it give?",
)
_LINES = {
    PICK: PICK_LINES,
    OPTIONS: OPTIONS_LINES,
    AMOUNT: AMOUNT_LINES,
    TIME: TIME_LINES,
    YESNO: YESNO_LINES,
    VAGUE: VAGUE_LINES,
    RECALL: RECALL_LINES,
    PAPERWORK: PAPERWORK_LINES,
    REASON: REASON_LINES,
    ADVICE: ADVICE_LINES,
}

_HEAVY = re.compile(
    r"\b(?:died|dying|death|funeral|cancer|hospice|hospital|miscarr\w*|suicide|kill myself|"
    r"abuse|assault|overdose|relapse|diagnos\w*|terminal)\b")


_TWO_THINGS = re.compile(r"(\w[\w'-]*)\W{0,2}\s+or\s+\W{0,2}(\w[\w'-]*)")
_NOT_AN_OPTION = frozenset("""i we you he she it they me us them him her my our your their this that
these those there then so if and but not no yes is are was were do does did can could will would
should shall may might have has had get got go going put take make""".split())


def _the_two_things_are_on_the_table(understood, memory):
    said = [str(understood.get("clean") or understood.get("text") or "")]
    for turn in (memory.get("turns") or [])[-4:]:
        if isinstance(turn, dict):
            said.append(str(turn.get("user") or ""))
            said.append(str(turn.get("bot") or ""))
    for text in said:
        for left, right in _TWO_THINGS.findall(text.lower()):
            if left not in _NOT_AN_OPTION and right not in _NOT_AN_OPTION:
                return True
    return False


_HOW_MANY = re.compile(r"^(?:and\s+|so\s+|but\s+)?how\s+(?:many|much)\s+(?:\w+\s+){0,2}?(\w{3,})")
_NOT_THE_THING = frozenset("""more time long often far big much many old new good bad early late
soon quick long worth often""".split())


def _the_figures_are_in_the_thread(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    for turn in turns[-2:]:
        for source in (str(turn.get("user") or ""), str(turn.get("bot") or "")):
            if re.search(r"\d", source):
                return True
    return False


def _the_bot_just_said_a_lot(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    for turn in reversed(turns[-2:]):
        bot = str(turn.get("bot") or "")
        if len(bot.split()) >= 25:
            return True
    return False


def _a_count_of_the_thing_just_named(clean, memory):
    match = _HOW_MANY.match(str(clean or "").lower().strip())
    if not match:
        return False
    word = match.group(1)
    if word in _NOT_THE_THING:
        return False
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-4:]
    if not turns:
        return False
    for turn in reversed(turns):
        for source in (str(turn.get("bot") or ""), str(turn.get("user") or "")):
            if re.search(r"(?<![a-z])" + re.escape(word.rstrip("s")) + r"[a-z]{0,2}(?![a-z])",
                         source.lower()):
                return True
    return False


_A_TIME_WORD = re.compile(r"\b(?:how\s+far\s+ahead|how\s+soon|how\s+long|how\s+quick|"
                          r"when\s+should|what\s+time)\b")
_A_FACT_ABOUT_TIME = re.compile(
    r"\bwhen (?:does|do|did|will) (?:the|it|they|this|that|a|my|his|her|your)\b"
    r"|\bwhen (?:does|do|did|will)\s+(?!i\b|we\b|you\b)\w"
    r"|\bwhen (?:does|do) it\b"
    r"|\bwhat time (?:does|do|is|are|will)\b"
    r"|\bhow far (?:ahead|in advance)\b"
    r"|\bhow long (?:before|in advance)\b"
    r"|\b(?:should|do|can) i (?:need to )?book\b")
_A_STORED_COUNT = re.compile(
    r"\bhow many (?:episodes|seasons|chapter|chapters|pages|tracks|songs|albums|volumes|parts|"
    r"instalments|films|series|books|tablets|doses|rounds)\b"
    r"|\bhow many \w+ (?:are|were) there\b")
_A_FIT_STATE = re.compile(
    r"\b(?:ok|okay|alright|all\s+right|fine|safe|sound|sound\s+enough|still\s+good|still\s+ok|still\s+fine|"
    r"gone\s+off|gone\s+bad|in\s+date|off|spoiled|spoilt|edible|contaminated|damaged|broken|worn|leaking)\b")
_A_POINTS_AT_A_THING = re.compile(r"\b(?:it|that|this|those|these|they|them|the|mine|ours)\b")
_A_VERDICT_WORD = re.compile(
    r"\b(?:worth|enough|too\s+many|too\s+much|better|worse|help|helps|work|works|risk|safe|"
    r"okay|ok|fine|point|bother|afford|matter|matters)\b")
_A_DECISION = re.compile(r"\b(?:should\s+(?:i|we)|shall\s+(?:i|we)|is\s+it\s+worth|worth\s+it|"
                         r"worth|do\s+you\s+think|would\s+(?:i|we)|am\s+i\s+better|enough|"
                         r"too\s+much|too\s+many|better\s+off|bother|afford|for\s+that"
                         r"|(?:would|will|does|do|did|could|can)\s+(?:a|an|another|one|two|the)"
                         r"\b[^?.!]{0,25}?\b(?:help|be\s+(?:better|good|worth))\b)")
_A_WHOSE_THING = re.compile(r"\b(?:my|our|mine|his|her|their)\b")
_A_DATE_ON_IT = re.compile(r"\b(?:when|what\s+date)\b[^?.!]{0,30}?\b(?:run\s+out|runs\s+out|expire|"
                           r"expires|renew|renews|renewal|end|ends|due|"
                           r"give\s+notice|notice\s+period)\b|\b(?:when|what\s+date)\b"
                           r"[^?.!]{0,24}?\b(?:do|should)\s+(?:i|we)\s+(?:need\s+to\s+)?renew\b")
_THEIR_THINGS = re.compile(r"\b(?:polic(?:y|ies)|insurance|contract|warranty|guarantee|mot|lease|"
                           r"tenancy|licence|license|passport|membership|subscription|pass|"
                           r"agreement|cover|plan|booking|reservation|permit|filing|return)\b")
_AN_ENOUGH_ASK = re.compile(r"\b(?:is|are|will|would|do|does|did)\b[^?.!]{0,15}?\benough\b")
_A_PICK_ASK = re.compile(r"^(?:ok\s+|and\s+|so\s+)?(?:what|which)\s+(?:should|shall|do|would|can)"
                         r"\s+(?:i|we)\s+(?:go\s+for|pick|choose|get|buy|start\s+with|have)\b")
_A_STRAIGHT_YESNO = re.compile(r"^(?:ok\s+|and\s+|so\s+)?(?:should|shall|do|does|did|would|will"
                               r"|is|are|can|could)\s+(?:i|we|it|that|this)\b")
_A_WORK_OUT = re.compile(r"\bhow (?:do|does|would|can|could|shall) (?:i|we)\b[^?.!]{0,30}?"
                         r"\b(?:work|figure|sort)\s+out\b"
                         r"|\bhow (?:do|would|can|could) (?:i|we) (?:know|tell|estimate|budget)\b"
                         r"[^?.!]{0,30}?\b(?:much|many|cost|costs|afford|price|budget|total)\b")
_ON_PAPER = re.compile(r"\b(?:polic(?:y|ies)|renewal|insurance|contract|agreement|licence|license|"
                       r"passport|warrant(?:y|ies)|booking|ticket|statement|invoice|receipt|"
                       r"letter|form|certificate|account|mortgage|tenancy|lease|quote|"
                       r"registration|mot|v5c)\b")
_BARE_ASK = re.compile(r"^(?:ok\s+|and\s+|so\s+)?(?:what|which|where|whats|what's)\s+"
                       r"(?:should|shall|do|can|could|would)\s+(?:i|we)\s+"
                       r"(?:visit|see|do|go|eat|drink|get|buy|put|pick|choose|start|try|book)\b")

_LEANS_ON_THE_THREAD = re.compile(
    r"^(?:and\s+|so\s+|but\s+|ok\s+)?(?:does|do|did|is|are|was|were|will|would|can|could|"
    r"should)\s+(?:that|this|it|they|those|these)\b")


def _on_paper(line, memory):
    said = [str(line or "")]
    for turn in (memory.get("turns") or [])[-4:]:
        if isinstance(turn, dict):
            said += [str(turn.get("user") or ""), str(turn.get("bot") or "")]
    return any(_ON_PAPER.search(text.lower()) for text in said if text)


def _the_thing_is_theirs(memory):
    if not isinstance(memory, dict):
        return False
    for turn in (memory.get("turns") or [])[-3:]:
        if not isinstance(turn, dict):
            continue
        said = str(turn.get("user") or "").lower()
        if _A_WHOSE_THING.search(said) and _THEIR_THINGS.search(said):
            return True
    return False


def _the_thread_is_heavy(memory):
    for turn in (memory.get("turns") or [])[-3:]:
        if not isinstance(turn, dict):
            continue
        if _HEAVY.search(str(turn.get("user") or "").lower()):
            return True
    return False


def the_shape_without_the_fact(understood, memory=None):
    if not isinstance(understood, dict):
        return None
    want = understood.get("wants")
    line = str(understood.get("clean") or understood.get("text") or "").lower()
    if want == STEPS and _A_PICK_ASK.match(line.strip()):
        want = PICK
    if want == STEPS and _A_WORK_OUT.search(line):
        want = AMOUNT
    elif want == STEPS and _A_STRAIGHT_YESNO.match(line.strip()):
        want = YESNO
    if want == AMOUNT and _A_TIME_WORD.search(line):
        want = TIME
    if _A_DATE_ON_IT.search(line) and (_A_WHOSE_THING.search(line) or _the_thing_is_theirs(memory)):
        want = PAPERWORK
    if want in (AMOUNT, TIME) and _A_FREQUENCY.search(line):
        return None
    if (want in (PICK, OPTIONS) and not _AN_ASK_AT_THE_FRONT.match(line.strip())
            and not _TWO_THINGS.search(line)):
        return None
    elif want in (TIME, AMOUNT) and _A_FACT_ABOUT_TIME.search(line):
        return None
    if want == AMOUNT and _A_STORED_COUNT.search(line):
        return None
    _turns = memory.get("turns") if isinstance(memory, dict) else None
    if _A_WHAT_WAS_IT.search(line) and _A_THEY_SAID_SO.search(line) and not _turns:
        want = RECALL
    elif _A_WHAT_WAS_IT.search(line) and _turns:
        return None
    if _A_VAGUE.match(line.strip()):
        want = VAGUE
    if want in (PICK, OPTIONS) and _WHICH_I_NEED.search(line):
        return None
    if want in (PICK, OPTIONS) and _WHAT_TO_DO_WITH.search(line):
        return None
    if want not in _LINES:
        return None
    if _the_thread_is_heavy(memory or {}):
        return None
    if memory and memory.get("turns"):
        if want != YESNO and _LEANS_ON_THE_THREAD.match(line.strip()):
            return None
        if want in (PICK, STEPS, OPTIONS) and _BARE_ASK.match(line.strip()) \
                and _the_bot_just_said_a_lot(memory):
            return None
    if want == YESNO and _AN_ENOUGH_ASK.search(line):
        want, pool = AMOUNT, _LINES[AMOUNT]
        return pool
    if want == YESNO and _A_FIT_STATE.search(line) and _A_POINTS_AT_A_THING.search(line):
        return None
    if want == YESNO and _LEANS_ON_THE_THREAD.match(line.strip()) \
            and not _A_VERDICT_WORD.search(line):
        return None
    if want == YESNO and not _A_DECISION.search(line) \
            and not (memory and memory.get("turns")):
        return None
    if want in (AMOUNT, TIME) and _on_paper(line, memory or {}):
        return None
    if want in (AMOUNT, TIME) and _the_figures_are_in_the_thread(memory or {}):
        return None
    pool = _LINES.get(want)
    if want == PICK and _the_two_things_are_on_the_table(understood, memory or {}):
        pool = PICK_LINES_NAMED
    if _a_count_of_the_thing_just_named(understood.get("clean") or understood.get("text"),
                                        memory or {}):
        return None
    return pool

_A_HEADS = 40


def _a_placeholder(reply, fallback):
    said = " ".join(str(reply or "").lower().split())
    if not said:
        return False
    if fallback._in_a_pool(reply, (fallback.NEUTRAL,)):
        return True
    return said[:_A_HEADS] in [line.lower()[:_A_HEADS] for line in fallback.UNKNOWN]


def _a_thread_with_a_person_in_trouble(fallback, memory):
    for reader in ("_in_a_care_thread", "_in_a_loss_thread", "_in_a_crisis_thread",
                   "_thread_is_about_the_body"):
        try:
            if getattr(fallback, reader)(memory):
                return True
        except Exception:
            continue
    return False


def answer_for(text, memory, reply):
    from . import fallback

    if not isinstance(memory, dict):
        return None
    understood = memory.get("understood")
    if not isinstance(understood, dict):
        return None
    if not _a_placeholder(reply, fallback):
        return None
    pool = the_shape_without_the_fact(understood, memory)
    if pool is None:
        return None
    if _a_thread_with_a_person_in_trouble(fallback, memory):
        return None
    clean = understood.get("clean") or " ".join(str(text or "").lower().split())
    return fallback._choose(pool, memory, clean)
