import re

RETURNING = re.compile(
    r"\b(?:it|that|this|they|the (?:same )?(?:problem|trouble|issue|fault|leak|smell|noise|"
    r"pain|spot|mould|damp|drip|mark|stain|rash|ache|cough|itch|swelling|spots|noises|pains|"
    r"leaks|smells|rashes|aches|coughs|itches)s?)\s+"
    r"(?:(?:'s|is|was|has|had|have|came|comes|come|keeps coming|kept coming|keep coming)\s+)"
    r"(?:\w+\s+){0,2}back\b"
    r"|\b(?:its|it's|they're|theyre)\s+back\b"
    r"|\b(?:it|that|this)\s+has\s+(?:come|came)\s+back\b"
    r"|\bback again\b")
AGAIN = re.compile(
    r"\b(?:it|its|it's|that|thats|that's|they|theyre|they're|this|"
    r"the (?:same )?(?:problem|trouble|issue|fault|leak|smell|noise|pain|ache|rash|drip|mould|"
    r"damp|blockage|spots?|pains?|noises?|leaks?|spots?))\s+"
    r"(?:has |have |had |is |was |keeps? |kept |just |only |still |all |already |again )*"
    r"(?:dropped|drop|drops|dropping|started|starting|starts|happened|happens|happening|"
    r"come back|came back|comes back|come|came|gone|gone off|returned|return|done it|does it|"
    r"doing it|played up|plays up|playing up|acting up|acts up|acted up|flared up|flares up|"
    r"flaring up|stopped working|broken|broke|failed|fails|failing|blocking|blocked|"
    r"back|no better|not better|not clearing|not cleared|just as bad|as bad|worse|better)\b",
    re.I)
RECURRING = re.compile(r"\b(?:again|still|no better|not better|worse than before|"
                       r"just as bad|as bad as before)\b", re.I)
SELF_EVIDENT = re.compile(
    r"\b(?:returned|return|came back|come back|coming back|keeps? coming|kept coming|"
    r"keeps? (?:dropping|failing|blocking|breaking|playing up|acting up|flaring up)|"
    r"flared up|flaring up|back again)\b", re.I)
ASKING = re.compile(
    r"^(?:will|would|does|do|did|is|are|was|were|can|could|should|why|when|how|what|where|who|"
    r"shall)\b")

NEXT_STEP = re.compile(
    r"\b(?:if|when|once)\s+(?:it|that|this|they|things)\s+"
    r"(?:keeps?|still|comes? back|come back|returns?|happens? again|does it again|doesn'?t|"
    r"does not|hasn'?t|has not|has been|have been|lasts?|persists?|keeps up|won'?t|"
    r"will not|is no better|isn'?t better|isn'?t clearing|is not clearing|gets worse)", re.I)
SENTENCE = re.compile(r"(?<=[.!?])\s+")

NOT_AN_ANSWER = ("safety", "urgent", "grief", "loss")

CONDITIONAL_ASK = re.compile(
    r"^(?:and|but|so|then)?\s*(?:what\s+)?if\s+"
    r"(?:it|that|this|they|theyre|it's|things|the\s+\w+)\s+"
    r"(?:does\s?n[o']?t|does not|did\s?n[o']?t|did not|is\s?n[o']?t|is not|has\s?n[o']?t|"
    r"has not|have\s?n[o']?t|gets?|stays?|keeps?|lasts?|still|stops?|eases?|"
    r"no better|not better|not clearing)\b", re.I)


def reads_as_returning(text):
    line = " ".join(str(text or "").lower().split())
    if not line or len(line.split()) > 16:
        return False
    if ASKING.match(line):
        return False
    if RETURNING.search(line):
        return True
    return bool(AGAIN.search(line) and (RECURRING.search(line) or SELF_EVIDENT.search(line)))


def _the_turn_before(memory):
    turns = [turn for turn in (memory or {}).get("turns") or [] if isinstance(turn, dict)]
    return turns[-1] if turns else None


def _the_answer_before(memory, keep=4):
    turns = [turn for turn in (memory or {}).get("turns") or [] if isinstance(turn, dict)]
    for turn in reversed(turns[-keep:]):
        if str(turn.get("module") or "") in NOT_AN_ANSWER:
            return None
        if the_next_step(turn.get("bot")):
            return turn
    return None


LEADING_CONDITION = re.compile(
    r"^(?:if|when|once)\s[^,.;:]{0,80},\s*(?=[A-Za-z])", re.I)
CONTINUES = ("or", "and", "keeps", "keep", "kept", "comes", "come", "still", "lasts", "persists",
             "gets", "goes", "happens", "does", "hasn't", "has not", "isn't", "is not", "won't",
             "will not", "stops", "swells", "spreads", "bleeds", "hurts", "wakes")


def the_next_step(reply):
    for sentence in SENTENCE.split(str(reply or "").strip()):
        sentence = sentence.strip()
        if not sentence or not NEXT_STEP.search(sentence):
            continue
        bare = LEADING_CONDITION.sub("", sentence)
        if bare and bare != sentence and len(bare.split()) >= 4 \
                and bare.split()[0].lower().strip(",.;:") not in CONTINUES:
            return bare[:1].upper() + bare[1:]
        if sentence.lower().startswith(("if ", "when ", "once ")):
            continue
        return sentence
    return None


RECURRENCE = re.compile(
    r"\b(?:again|still)\b\s*(?:(?:today|tonight|this morning|this afternoon|this evening|"
    r"this week|already|now|too|though)\b\s*)*(?:[.!]*$|of\b)", re.I)
REMIND_ME = re.compile(r"\b(?:remind|refresh my memory|what (?:was|is|were|did))\b", re.I)
AN_ASK = re.compile(
    r"^(?:how|what|when|where|which|who|why|can|could|should|shall|will|would|may|might|"
    r"do|does|did|is|are|am|was|were|have|has|any|is there|are there)\b", re.I)


def says_it_happened_again(text):
    said = " ".join(str(text or "").lower().split())
    if not said or REMIND_ME.search(said) or AN_ASK.match(said):
        return False
    if reads_as_returning(said):
        return True
    return bool(RECURRENCE.search(said))


def reads_as_a_conditional(text):
    said = " ".join(str(text or "").lower().split())
    return bool(CONDITIONAL_ASK.match(said))


def pool_for(text, memory):
    conditional = reads_as_a_conditional(text)
    if not reads_as_returning(text) and not conditional:
        return None
    before = _the_answer_before(memory)
    if not before:
        return None
    said = str(before.get("bot") or "")
    step = the_next_step(said)
    if not step:
        return None
    if " ".join(step.lower().split()) == " ".join(said.lower().split()):
        return None
    if conditional:
        around = " ".join(said.replace(step, " ").split())
        if len(around.split()) <= 8:
            return None
    return step


def the_whole_of_it(text, memory):
    if not reads_as_returning(text):
        return None
    before = _the_answer_before(memory)
    said = str((before or {}).get("bot") or "")
    return said if the_next_step(said) else None
