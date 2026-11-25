import re

from ..compose import pick
from . import again, repeat
from . import topics
from . import quotes as quoted

OPENERS = (r"^(?:(?:and|so|but|ok|okay|well|right|sorry|wait|basically|hmm|um|er|uh|ah|oh|yeah|"
           r"then|no|nope|again|hold\s+on|alright)\b[\s,]+)*"
           r"(?:(?:i\s*(?:'m|m)\s*)?not\s+sure(?:\s+(?:what|that|if))?[\s,]+|"
           r"i\s+don(?:'t|t)\s+(?:get|understand|follow)\b[\s,]*(?:it|that|this)?[\s,]*|"
           r"(?:i\s+)?did(?:n'?t|nt)\s+(?:catch|follow)(?:\s+(?:that|you))?[\s,]+|"
           r"not\s+following[\s,]+|you\s+lost\s+me[\s,]+)*")

MEAN = re.compile(r"^\s*" + OPENERS +
                  r"(?:"
                  r"(?:what|wot|wat|wut|whut)\s+(?:(?:do|did|d)\s+)?(?:you|u|ya)\s+mean"
                  r"(?:\s+(?:by\s+(?:that|it|this)|exactly|though|then))?|"
                  r"(?:whatcha|watcha|whaddya|whadya|whatdya)\s+mean"
                  r"(?:\s+by\s+(?:that|it|this))?|"
                  r"how\s+(?:do|did)\s+(?:you|u|ya)\s+mean"
                  r"(?:\s+(?:by\s+(?:that|it|this)|exactly))?|"
                  r"what(?:'s|s)?\s+(?:(?:does|do|is)\s+)?(?:that|it|this)\s+"
                  r"(?:(?:actually|really|exactly|precisely|even|then)\s+)?"
                  r"(?:supposed\s+to\s+)?mean"
                  r"(?:\s+(?:then|though|exactly|precisely))?"
                  r"(?:\s+by\s+(?:that|it|this))?"
                  r"(?:\s+for\s+(?:me|us|him|her|them|my\s+case|my\s+situation|"
                  r"(?:my|our)\s+[\w'\u2019-]+(?:\s+[\w'\u2019-]+)?))?"
                  r"(?:\s+about\s+(?:my|our|the|this|that)\s+[\w'\u2019-]+"
                  r"(?:\s+[\w'\u2019-]+){0,2})?"
                  r"(?:\s+in\s+(?:practice|reality|real\s+terms))?"
                  r"(?:\s+(?:then|though|exactly|precisely))?|"
                  r"meaning\s+what|explain\s+(?:what\s+)?(?:you|u)\s+mean|"
                  r"wdym|mean\s+what\s+exactly|"
                  r"(?:what(?:'s|s)?|what\s+is)\s+(?:the\s+)?meaning\s+of\s+(?:that|it|this)|"
                  r"(?:the\s+)?meaning\s+of\s+(?:that|it|this)|and\s+that\s+means\?|"
                  r"what\s+is\s+meant\s+by\s+(?:that|it|this)|whats?\s+the\s+meaning|"
                  r"(?:that|it|this)\s+means\s+what"
                  r"(?:\s+(?:exactly|then|though|precisely))?|"
                  r"what\s+(?:you|u|ya)\s+mean|what\s+(?:that|it|this)\s+means?"
                  r"(?:\s+(?:exactly|then|though|precisely))?"
                  r")"
                  r"(?:,\s*(?:then|though|exactly|precisely|really|actually)\b)?"
                  r"\s*[?.!]*\s*$", re.I)

ASKS_SOMETHING = re.compile(
    r",\s*(?:is|are|was|were|am|does|do|did|will|would|can|could|should|shall|has|have)\s+"
    r"[\w'\u2019-]+(?:\s+[\w'\u2019-]+){0,6}\s*[?.!]*\s*$", re.I)

REPEAT = re.compile(r"^\s*(?:and\s+|so\s+|but\s+|ok\s+|okay\s+|well\s+|right\s+|sorry\s+|er+\s+|um+\s+)*"
                    r"(?:"
                    r"(?:can|could|would)\s+you\s+(?:please\s+)?"
                    r"(?:say|repeat|explain|rephrase|clarify)(?:\s+(?:that|it))?(?:\s+again)?"
                    r"(?:\s+please)?|"
                    r"(?:say|repeat)\s+(?:that|it)\s+again|"
                    r"explain(?:\s+that)?|explain\s+again|meaning|"
                    r"(?:i\s+)?(?:(?:still|really|just|honestly|actually|literally)\s+)?"
                    r"(?:do\s*n[o']?t|dont|does\s*n[o']?t|did\s*n[o']?t|didnt)\s+"
                    r"(?:(?:really|still|quite|honestly|fully)\s+|at\s+all\s+)?"
                    r"(?:understand|follow|get\s+it|catch\s+that|"
                    r"(?:get|see|follow)\s+what\s+you(?:'re|\s+are)?\s+(?:saying|on\s+about|mean))"
                    r"(?:\s+(?:it|that|this|at\s+all|one\s+bit|any\s+of\s+it|"
                    r"what\s+you\s+mean|a\s+word\s+of\s+it|the\s+last\s+bit))?|"
                    r"(?:i'?m|im)\s+not\s+(?:following|with\s+you)|"
                    r"(?:i'?m|im)\s+(?:still\s+|a\s+bit\s+|totally\s+|completely\s+)?"
                    r"(?:confused|lost)|"
                    r"(?:you\s+)?(?:have\s+)?lost\s+me(?:\s+(?:there|completely|entirely))?|"
                    r"(?:that|this)\s+is\s+confusing|"
                    r"(?:that'?s|thats)\s+confusing|"
                    r"(?:what|pardon|eh|huh)\?*|"
                    r"sorry\s*,?\s*(?:what|pardon|eh|huh)?\s*\?+|"
                    r"sorry\s*,?\s*(?:what|pardon|eh|huh)\s*[?.!]*|"
                    r"(?:say|explain|put)\s+it\s+in\s+(?:plain\s+)?english(?:\s+please)?|"
                    r"what(?:'s|s|\s+is)?\s+(?:that|this|it)\s+in\s+(?:plain\s+)?english|"
                    r"in\s+(?:plain\s+)?english(?:\s+please)?|english\s+please|"
                    r"come\s+again|say\s+what"
                    r")\s*[?.!]*\s*$", re.I)

REPEAT_LEADS = (
    "I said: {said}",
    "Same again: {said}",
    "Let me put it plainer: {said}",
)

LEADS = (
    "I mean this: {said}",
    "Just this: {said}",
    "What I meant: {said}",
)

PERSONAL = re.compile(r"\bfor\s+(?:me|us|him|her|them|my\s+case|my\s+situation|"
                      r"(?:my|our)\s+[\w'\u2019-]+)\b|"
                      r"\bin\s+(?:practice|reality|real\s+terms)\b", re.I)

FOR_MINE = re.compile(r"\bfor\s+(?:my|our)\s+"
                      r"(?!case\b|situation\b|own\b|end\b|side\b|part\b)"
                      r"([\w'\u2019-]+(?:\s+[\w'\u2019-]+)?)\s*[?.!]*\s*$",
                      re.I)
PERSONAL_LEADS = (
    "For you, that means: {said}",
    "In your case: {said}",
)

FOLLOW_UP_WORDS = frozenset("""what whats which that this it thats those them they
    mean means meaning meant you u ya your i im sorry ok okay so then and but well just really
    actually exactly precisely simply plain plainer please can could would will do does did is
    are was were there here have has had
    put putting say saying said tell telling explained explaining explain
    break down again another other way words wording sense terms term practice reality real life
    english jargon
    technical simpler simple clearly five like of in on about to for me us him her huh pardon
    people normal someone folk most""".split())
PUT_IT_PLAINER = frozenset("""mean means meaning meant explain explained explaining
    tell telling another sense terms term practice reality english jargon technical plain words
    plainer simpler simple simply clearly break""".split())
NOT_LETTERS = re.compile(r"[^a-z'\s]")
TELLS = re.compile(r"\b(?:that|this|it|those|these)\b[^.?!]{0,20}\btell", re.I)
WHAT_YOU_ARE = re.compile(r"\b(?:what|who)\s+(?:are|r)\s+(?:you|u|ya)\b|\bwhat do you do\b", re.I)
ASKING_ABOUT_DOING = frozenset("""do does did done work works took take takes costing cost
    last lasts hurt hurts help helps happen happens matter matters""".split())


def _asked_plainly(clean):
    said = str(clean or "").lower().replace("\u2019", "'").strip(" ?.!,")
    if NOT_LETTERS.search(said):
        return False
    words = re.findall(r"[a-z']+", said)
    if not words or len(words) > 9:
        return False
    if not set(words) <= FOLLOW_UP_WORDS:
        return False
    if not set(words) & PUT_IT_PLAINER:
        return False
    if ("tell" in words or "telling" in words) and not TELLS.search(said):
        return False
    if WHAT_YOU_ARE.search(said):
        return False
    if words[-1] in ASKING_ABOUT_DOING:
        return False
    return True
ABOUT_MINE = re.compile(r"\babout\s+(?:my|our|the|this|that)\s+"
                        r"([\w'\u2019-]+(?:\s+[\w'\u2019-]+){0,2})\s*[?.!]*\s*$", re.I)
SOMEONE_ELSE = re.compile(r"\bfor\s+(him|her|them)\b", re.I)
SOMEONE_LEADS = "For {who}, that means: {said}"
_PERSONAL_HEADS = tuple(lead.split("{")[0] for lead in PERSONAL_LEADS) + ("For him, that means: ",
                                                                         "For her, that means: ",
                                                                         "For them, that means: ")


def _personal(said):
    return (said or "").strip().startswith(_PERSONAL_HEADS)


def _their_subject(said):
    found = FOR_MINE.search(said or "")
    return " ".join(found.group(1).lower().split()) if found else ""


def _on_the_table(noun, memory):
    head = (noun or "").split()
    head = head[0] if head else ""
    if not head or not isinstance(memory, dict):
        return False
    said = ""
    for turn in (memory.get("turns") or [])[-2:]:
        if isinstance(turn, dict):
            said += " %s %s" % (turn.get("user") or "", turn.get("bot") or "")
    return bool(re.search(r"\b%s" % re.escape(head), said.lower()))


def _under_the_lead(said):
    text = (said or "").strip()
    for head in sorted(_HERE, key=len, reverse=True):
        if text.lower().startswith(head.lower()):
            return text[len(head):].strip()
    return _carried(text)

SENTENCE = re.compile(r"(?<=[.!?])\s+")
RECEIPT = re.compile(
    r"^\s*(?:sure\s*[-\u2014]\s*)?(?:noted\b|got it\b|so far i know\b|"
    r"thanks for telling me\b|i hear you\b|i'?m listening\b|say more\b|tell me more\b|"
    r"that sounds\b|i'?ll keep that\b|good to know\b|nothing (?:to do|i can add)\b|"
    r"i'?m here if\b|(?:i\s+)?haven'?t put anything about it into words|"
    r"nothing of mine to go back over|is there anything you'?d like\b|"
    r"you'?re (?:noted|on the list)\b)"
    r"|[\u2014-]\s*(?:noted|good to know|got it|i'?ll remember that|i'?ve got that)\b[.!]*\s*$",
    re.I)

NOTHING_WRITTEN = (
    "I haven't put anything about it into words yet - give me a bit more and I'll start from "
    "there.",
    "Nothing of mine to go back over yet. Tell me a little more and I'll take it from the top.",
    "I hadn't answered anything yet, so there's nothing of mine to put straighter - tell me what "
    "you were after and I'll take it on.",
    "Nothing of mine to explain yet: I said how that landed and stopped there. Say what you were "
    "asking and I'll have a proper go at it.",
    "That was me saying how it lands, not an answer. Ask me again and I'll take it on.",
)

NO_ANSWER_OF_MINE = (
    "I didn't have an answer there, so there's nothing of mine to explain - it just didn't know. "
    "Say a bit more about it and I'll have a proper go.",
    "Nothing of mine to go over: I didn't know that one. Tell me more and I'll try again.",
)

SAID_TWICE = (
    "I've put that twice now, so the words in it are probably the problem - tell me which bit and "
    "I'll unpack that one.",
    "That is the second time I've said it that way. Which word in it is the trouble?",
)

CLAUSE = re.compile(r":\s+|\s+-\s+|;\s+|,\s+so\s+|,\s+and\s+|,\s+but\s+|,\s+which\s+", re.I)
MOST = 150
LEAST = 30
ANSWERED = 20
LOOK_BACK = 3
LOOK_BACK_FAR = 7


def _sentences(said):
    return quoted.sentences(said, SENTENCE)


DEFINES = re.compile(
    r"\bmeans?\b|\bis when\b|\bis what\b|\bis where\b|\bin other words\b|\brefers to\b|"
    r"\bstands for\b|\bwhich means\b|\bthat is what\b", re.I)


def _gist(sentence):
    sentence = (sentence or "").strip()
    cut = None
    after_a_colon = False
    for match in CLAUSE.finditer(sentence):
        if match.start() >= LEAST:
            cut = match.start()
            after_a_colon = match.group(0).startswith(":")
            break
    if cut is not None:
        explained = sentence[cut:].lstrip(":;- ").strip()
        if after_a_colon and len(explained) >= LEAST and DEFINES.search(explained):
            sentence = explained[:1].upper() + explained[1:]
        else:
            sentence = sentence[:cut]
    sentence = sentence.strip().rstrip(",;:- ")
    if len(sentence) > MOST:
        sentence = sentence[:MOST].rsplit(" ", 1)[0].rstrip(",;:- ")
    if sentence and sentence[-1] not in ".!?":
        sentence += "."
    return sentence


NOT_TO_REPEAT = frozenset(("safety", "loss", "grief"))

CONDOLENCE = re.compile(
    r"^\s*(?:(?:oh|ah)\s*,?\s+|(?:i'?m|i\s+am)\s+(?:so\s+|really\s+|very\s+)?)*sorry\b|^\s*"
    r"(?:oh\s+no|ugh|that'?s\s+(?:rough|hard|awful|a\s+lot\s+to\s+carry)|that\s+is\s+rough|"
    r"what\s+a\s+shame|how\s+awful|that\s+sounds\s+(?:rough|tough|hard|awful|horrible))\s*[,:.\u2014-]",
    re.I)


def _answers(memory, back=LOOK_BACK):
    out = []
    for turn in reversed((memory.get("turns") or [])[-back:]):
        if not isinstance(turn, dict):
            break
        said = str(turn.get("bot") or "").strip()
        if not said:
            continue
        if str(turn.get("module") or "") in NOT_TO_REPEAT:
            break
        out.append((said, str(turn.get("user") or "").strip()))
    return out


def _thick_enough(said, asked):
    words = [w for w in topics.words(said) if w not in topics.STOPWORDS and len(w) > 2]
    if len(words) >= 5:
        return True
    theirs = {w for w in topics.words(asked) if w not in topics.STOPWORDS and len(w) > 2}
    return bool(theirs.intersection(words))


_HERE = tuple(lead.split("{")[0] for lead in LEADS + REPEAT_LEADS + PERSONAL_LEADS)


def _framed(said):
    return repeat.framed(said) or (said or "").strip().startswith(_HERE)


def _a_figure(said):
    return bool(re.search(r"\d", str(said or "")))


def _a_question(sentence):
    return str(sentence or "").strip().endswith("?")


def _worth_handing_over(said, sentence, asked):
    if not (_thick_enough(said, asked) or _a_figure(said)):
        return False
    return _a_figure(said) or _a_question(sentence) or _thick_enough(sentence, asked)


def _cite(said, sentence, asked="", memory=None):
    if repeat.HEDGE.search(said):
        return None
    if CONDOLENCE.match(said):
        said = _after_the_condolence(said)
        if not said:
            return None
        if sentence and sentence not in said:
            sentence = _meant(said, said.rstrip().endswith("?"))
    if len(sentence) < ANSWERED and not _a_figure(said) and not _thick_enough(said, asked):
        return None
    if RECEIPT.search(said) or RECEIPT.search(sentence):
        return None
    if _framed(said):
        return None
    if said in ((memory or {}).get("repeated") or []):
        return None
    if not _worth_handing_over(said, sentence, asked):
        return None
    return _gist(sentence)


def _meant(said, asked_what_it_meant=False):
    parts = _sentences(said)
    if not parts:
        return ""
    if said.rstrip().endswith("?") and (asked_what_it_meant or len(parts) == 1):
        return parts[-1]
    first = ""
    for sentence in parts:
        if not repeat.HEDGE.search(sentence) and len(sentence) >= ANSWERED:
            first = sentence
            break
    if not first:
        return parts[0]
    if not DEFINES.search(first):
        for sentence in parts:
            if sentence == first or repeat.HEDGE.search(sentence):
                continue
            if len(sentence) >= ANSWERED and DEFINES.search(sentence):
                return sentence
    return first


CONDOLENCE_SENTENCE = re.compile(
    r"^\s*(?:(?:oh|ah)\s*,?\s+|(?:i'?m|i\s+am)\s+(?:so\s+|really\s+|very\s+)?)*sorry[^.!?]*[.!?]"
    r"|^\s*(?:oh\s+no|ugh|that'?s\s+(?:rough|hard|awful|a\s+lot\s+to\s+carry)|that\s+is\s+"
    r"rough|what\s+a\s+shame|how\s+awful|that\s+sounds\s+(?:rough|tough|hard|awful|horrible))"
    r"[^.!?]*[.!?]",
    re.I)


def _after_the_condolence(said):
    cut = CONDOLENCE_SENTENCE.match(said or "")
    if not cut:
        return ""
    rest = " ".join((said or "")[cut.end():].split())
    return rest


def _same_bit(one, other):
    one = (one or "").strip().rstrip(".?! ").lower()
    other = (other or "").strip().rstrip(".?! ").lower()
    for lead in LEADS + REPEAT_LEADS:
        head = lead.split("{")[0].lower()
        if other.startswith(head):
            other = other[len(head):].strip()
    if not one or not other:
        return False
    short, long = (one, other) if len(one) <= len(other) else (other, one)
    return long.startswith(short) or short in long


def _already(cited, said_since):
    return any(_same_bit(cited, line) for line in said_since)


def _carried(said):
    return again.unframed(said) or ""


def _applied_to_the_person(clean, said, asked, memory, what_it_meant):
    if not (what_it_meant and PERSONAL.search(clean)):
        return None
    carried = _under_the_lead(said)
    if not carried or _personal(said):
        return None
    noun = _their_subject(clean)
    if noun and not _on_the_table(noun, memory):
        return None
    cited = _cite(carried, _meant(carried, what_it_meant), asked, memory) or carried
    if not cited:
        return None
    someone = SOMEONE_ELSE.search(clean)
    if someone:
        lead = SOMEONE_LEADS.format(who=someone.group(1).lower(), said=cited)
    else:
        lead = pick(PERSONAL_LEADS, memory, clean).format(said=cited)
    return repeat.handed_back(memory, lead)


def answer_for(text, memory):
    if not isinstance(memory, dict):
        return None
    clean = ((memory.get("understood") or {}).get("clean") or text or "").strip()
    repaired = ((memory.get("understood") or {}).get("plain") or "").strip()
    if repaired and repaired != clean and not (MEAN.match(clean) or REPEAT.match(clean)):
        if MEAN.match(repaired) or REPEAT.match(repaired):
            clean = repaired
    if MEAN.match(clean) and ASKS_SOMETHING.search(clean):
        return None
    if MEAN.match(clean):
        leads = LEADS
        what_it_meant = True
        if _their_subject(clean) and not _on_the_table(_their_subject(clean), memory):
            return None
        about = ABOUT_MINE.search(clean)
        if about and not _on_the_table(about.group(1), memory):
            return None
    elif REPEAT.match(clean):
        leads = REPEAT_LEADS
        what_it_meant = False
    elif _asked_plainly(clean):
        leads = REPEAT_LEADS
        what_it_meant = False
    else:
        return None
    said_since = []
    lines = []
    applied_once = False
    for back in (LOOK_BACK, LOOK_BACK_FAR):
        for said, asked in _answers(memory, back):
            if said in said_since:
                continue
            if not applied_once and (what_it_meant and PERSONAL.search(clean)
                                     and _personal(said)):
                applied_once = True
            if not applied_once:
                applied = _applied_to_the_person(clean, said, asked, memory, what_it_meant)
                if applied:
                    return applied
            carried = _carried(said)
            if carried:
                cited = _cite(carried, _meant(carried, what_it_meant), asked, memory)
                if cited and not _already(cited, said_since):
                    return pick(leads, memory, clean).format(said=cited)
                said_since.append(said)
                lines.append((said, asked))
                continue
            cited = _cite(said, _meant(said, what_it_meant), asked, memory)
            if cited and not _already(cited, said_since):
                return pick(leads, memory, clean).format(said=cited)
            said_since.append(said)
            lines.append((said, asked))
    if lines and _framed(lines[0][0]):
        carried = _under_the_lead(lines[0][0])
        noun = _their_subject(clean)
        if (what_it_meant and carried and PERSONAL.search(clean)
                and (not noun or _on_the_table(noun, memory))
                and not _personal(lines[0][0])):
            applied = _applied_to_the_person(clean, lines[0][0], lines[0][1], memory,
                                            what_it_meant)
            if applied:
                return applied
        return repeat.handed_back(memory, pick(SAID_TWICE, memory, clean))
    if lines and CONDOLENCE.match(lines[0][0]):
        return repeat.handed_back(memory, pick(NOTHING_WRITTEN, memory, clean))
    if lines and repeat.HEDGE.search(lines[0][0]):
        return repeat.handed_back(memory, pick(NO_ANSWER_OF_MINE, memory, clean))
    if lines and (RECEIPT.search(lines[0][0])
                  or (not _a_figure(lines[0][0])
                      and (not _thick_enough(lines[0][0], lines[0][1])
                           or len(_meant(lines[0][0])) < ANSWERED))):
        return repeat.handed_back(memory, pick(NOTHING_WRITTEN, memory, clean))
    return None


def reads_it(text):
    clean = " ".join(str(text or "").lower().split())
    return bool(MEAN.match(clean) or REPEAT.match(clean) or _asked_plainly(clean))
