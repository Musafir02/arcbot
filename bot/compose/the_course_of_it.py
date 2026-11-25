
import re

HEAVY = frozenset("""
feel feeling feelings felt sad sadness sadder grief grieving heartbroken broken heartsick lonely
loneliness alone guilt guilty ashamed shame anxious anxiety anxiousness depressed depression
panic unhappy happy happiness normal myself missing miss loss empty hopeless worthless numb
crying cry tears raw hurting hurts hurt heavy
""".split())

BODY = frozenset("""
rash cough cold flu virus infection temperature fever spot spots itch itching lump bruise ache
aches pain painful headache migraine tooth teeth gum gums back knee hip shoulder neck ankle wrist
sickness nausea dizzy dizziness diarrhoea constipation blister burn cut wound swelling stiff
stiffness allergy allergic symptoms symptom period periods pregnant pregnancy
""".split())

MED = frozenset("""
meds medication medicine medicines tablets tablet pill pills dose dosage antibiotic antibiotics
antidepressant antidepressants sertraline citalopram prozac prescription prescribed treatment
chemotherapy withdrawal
""".split())

RECOVERY = frozenset("""
section caesarean cesarean csection surgery operation op ops operation hospital hospitalised
hospitalized recovery recovering recovered convalescing stitches stitch physio physiotherapy
chemo radiotherapy transplant bypass hysterectomy appendectomy appendix labour labor delivery
birth births fall falls fracture fractured fractures sprain sprains
discharge ward icu catheter cast plaster
""".split())

THING = frozenset("""
boiler car engine tyre tyres mot wifi internet broadband router phone laptop computer printer
oven washing machine dishwasher fridge freezer heating radiator leak tap roof gutter damp mould
noise neighbour neighbors traffic rain weather winter summer sale offer subscription contract
mortgage rent landlord job shift rota school term exam
""".split())

COURSE = re.compile(
    r"\b(?:"
    r"get(?:ting)?\s+back\s+to\s+normal"
    r"|get(?:ting)?\s+(?:easier|any\s+easier|better|any\s+better)"
    r"|feel(?:ing)?\s+(?:like\s+myself|normal|better|happy|ok|okay|fine|human)\s+again"
    r"|be\s+(?:happy|ok|okay|normal|fine|myself)\s+again"
    r"|go(?:es|ing)?\s+away|went\s+away|gone\s+away|ever\s+go\b"
    r"|get(?:ting)?\s+over\s+(?:it|this|that|him|her|them|everything)"
    r"|feel\s+like\s+this"
    r"|(?:this|it|that)\s+(?:be\s+)?forever"
    r"|(?:this|it|that)\s+(?:ever\s+)?(?:last|lasts|lasted)\b"
    r"|(?:ever\s+)?(?:going\s+to\s+)?(?:stop|end|ease|eases|settle|settles|pass|passes|lift|lifts)"
    r"|(?:always\s+|forever\s+|still\s+)?(?:going\s+to\s+)?be\s+like\s+this"
    r"|be\s+over"
    r")\b",
    re.I,
)

ASKS = re.compile(
    r"^\s*(?:so\s+|but\s+|and\s+)?(?:when|does|do|will|would|is|are|am|can|could|how\s+long)\b",
    re.I,
)

CARD_IN_THE_CHAT = "the card in the chat"

NO_SUBJECT = "no subject yet"

IT_IS_HOW_IT_FEELS = frozenset("""
easier better cope coping manage managing deal dealing normal myself fine alright happy ok okay
heal healing recover recovering recoverd over through move moving onwards forward bearable
""".split())

NOTHING_NAMED = (
    "It depends what it is: a cough, a bad patch of sleep and a row at work all run on their own "
    "clock. Tell me the thing and I will say what usually happens with it.",
    "Nobody can say how long that lasts without knowing what it is. Which is it - something with "
    "your body, someone at home, or a job?",
    "How long that goes on for comes from what it is, and I do not know yet. Say what it refers to "
    "and I will tell you what usually happens.",
)

LASTS = re.compile(r"\bhow\s+long\s+(?:does|do|will|did|would)\b.*\b(?:last|take|go\s+on)\b", re.I)

DISTRESS = frozenset("""
cut cuts cutting cut myself self harmed harm harming suicide suicidal kill myself overdose
overdosed overdosing sectioned blades blade scars scarred burning starving starved purging
relapsed relapse
""".split())

ORDINARY = frozenset("""
baby babies newborn newborns teething toddler toddlers nappy nappies formula feeding breastfed
sleepless knackered tired exhausted shifts shift rota rotas nights overtime commute gym diet
running marathon training weight old age ageing aging birthday birthdays
""".split())

CARE = frozenset("""
lost lose losing died death dead funeral buried miscarriage miscarried separating separated
separation divorce divorced redundant redundancy sacked breakup broke broken cancer tumour
diagnosis diagnosed hospital hospice chemo stillbirth
""".split())

CARE_PROSE = (
    "I'm sorry - that's a heavy thing to be carrying. There is no date for it and I would be "
    "making one up, but it does come in patches rather than one long slope: a bearable hour, then "
    "a day that feels like the start again, and the bearable stretches get longer first. What "
    "helps early on is company and a shape to the day - someone who will sit with you, and one "
    "thing you do at the same time each day. Cruse takes calls from anyone who has lost someone, "
    "and your GP will see you about it too.",
    "That is a lot to hold, and I'm sorry. Nobody can tell you when it will feel lighter, and a "
    "guess would not help you. What tends to happen is that the good stretches come first, before "
    "the bad days get shorter, so a bad afternoon after a decent week is not a step back. Keep one "
    "fixed thing in the week and let people do things for you rather than asking; if it is grief, "
    "Cruse's line is there for exactly this, and your GP is the other door.",
)

PROSE = (
    "Nobody can put a date on that, and I would be making it up if I did. It tends to lift in "
    "patches before it lifts properly - an ordinary afternoon, then a day that feels like the "
    "start again - and a bad day after a good week is not you going backwards. Two things that "
    "help meanwhile: one fixed thing in the week you would turn up to anyway, and one person who "
    "hears the honest version. If it is still spoiling your sleep or your appetite after a few "
    "weeks, that is worth saying to a GP.",
    "It does ease for most people, but not on a timetable, so any date would be a guess. The bad "
    "days usually get further apart before they get shorter, which is worth knowing on a day that "
    "feels like week one again. Until then: keep one routine you do not have to think about, get "
    "outside most days, and tell one person how it actually is. If there is nobody to tell, your "
    "GP is the place to start, and so is a group of people who have been through the same thing.",
    "I can't tell you when, and anyone who can is guessing. What I can say is that it comes in "
    "patches rather than a steady line, and the patches get shorter - the stretch between bad days "
    "widens first. What moves it along is usually other people and a bit of structure rather than "
    "a lot of thinking: a walk with someone, a class, a fixed Sunday call. Your GP is the right "
    "next stop if it is your mood as much as the loss.",
)


CARD_PROSE = (
    "Nobody can put a date on that one, sorry - it answers to time rather than to anything I can "
    "look up. What shifts it is the everyday bit: {bit}. If it has not moved after a couple of "
    "weeks, that is the point to ask someone who can see the whole picture.",
    "I can't tell you when, and a guess would not help. The part that does the work is the "
    "everyday bit: {bit}. See where it is in a couple of weeks.",
    "There is no date for that, sorry. What moves it is what the first answer said: {bit}. If it "
    "is no different in a couple of weeks, that is when to ask someone who knows the case.",
)

CARD_PROSE_UNTIMED = (
    "There is no date for that one, and I would be making one up. What the answer was pointing at "
    "is still where to put the effort: {bit}. Has it moved at all since?",
    "Nobody can say when, sorry, and a made-up deadline would not help you. What the first answer "
    "said is the part to go on: {bit}. How long has it been going on?",
    "I can't put a time on it. The part that does the work is what was already said: {bit}. What "
    "has changed since it started?",
)

EASES = (
    "It gets easier for most people, and how long that takes varies - a couple of months is not "
    "unusual. What the answer said is the part that does the work: {bit}. Does it feel any "
    "different from the first week?",
    "It usually eases before it stops, and the easing is rarely in a straight line. Keep the thing "
    "the card named up: {bit}. Has it got any easier yet?",
    "That usually does get easier with time, though not evenly. The bit worth keeping up is what "
    "was said: {bit}. Has it eased at all yet?",
)


DOES_IT = frozenset("""
treat keep put believe water ask give use take call try make add move leave stop ring check measure
tell say write get go see book buy cut clean feed walk watch brush cover tie hold run set turn
start begin finish test watch wrap
""".split())

KEEP_UP = (
    "There is no date for that, sorry. What is worth keeping up in the meantime: {bit}. If it has "
    "not changed in a couple of weeks, that is the point to look at one thing and change it.",
    "I can't say when it will stop, and nobody could. The bit that does the work is the everyday "
    "one: {bit}. Give that a couple of weeks before you judge it.",
    "No date on that one, sorry. Keep the everyday bit up - {bit} - and watch for it moving over "
    "the next couple of weeks.",
)

KEEP_UP_UNTIMED = (
    "There is no date for that, sorry. The everyday bit is the part that does the work: {bit}. "
    "Keep that going and see what changes.",
    "I can't say when it stops, and nobody could. What is worth doing in the meantime: {bit}. "
    "What has changed so far?",
    "No date on that one, sorry. Keep the everyday bit up - {bit} - and watch for the first sign "
    "of it moving.",
)

STILL_STANDS = (
    "No date on that one, sorry. What the first answer said still stands: {bit}. If it is no "
    "different in a couple of weeks, that is the point to change one thing.",
    "I can't put a date on it. The facts have not moved since the first answer: {bit}. Give it a "
    "couple of weeks before you judge it.",
    "Nobody can say when, sorry. What the first answer said holds: {bit}. If nothing has changed "
    "in a couple of weeks, that is the moment to look at one thing.",
)

STILL_STANDS_UNTIMED = (
    "There is no date for that, and I would not invent one. What the first answer said is where "
    "to start: {bit}. Has it moved at all since?",
    "I can't say when, sorry. The part to go on is this: {bit}. How long has it been like this?",
    "Nobody can promise when, and a guess would not help. What the first answer said still "
    "stands: {bit}. What has changed since?",
)

TIME_IN_THE_CARD = re.compile(
    r"\b(?:hours?|days?|nights?|weeks?|months?|fortnight|how\s+long|heals?|clears?|settles?|"
    r"eases?|improves?|by\s+the\s+end)\b",
    re.I,
)

EASING = re.compile(r"\b(?:easier|better|improv\w*|bearable|less\s+often)\b", re.I)


def _words(text):
    return set(re.findall(r"[a-z']+", text.lower()))


def _same_as_the_last_answer(written, memory):
    seen = 0
    for turn in reversed((memory or {}).get("turns") or []):
        if not isinstance(turn, dict):
            continue
        said = str(turn.get("bot") or "").strip()
        if not said:
            continue
        if said[:60] == written[:60]:
            return True
        seen += 1
        if seen >= 3:
            break
    return False


ACK_LEAD = re.compile(
    r"^\s*(?:got\s+it|noted|right|okay|ok|thanks\s+for\s+telling\s+me|fair\s+enough|no\s+problem|"
    r"understood|sure|cheers)\b[^.!?]{0,40}?[.:;,\u2014\u2013-]\s*",
    re.I,
)


def _an_answer_worth_quoting(said):
    content = ACK_LEAD.sub("", str(said or "")).strip()
    return len(re.findall(r"[A-Za-z']+", content)) >= 5


def _the_card_in_the_chat(memory):
    turns = [((memory or {}).get("topic") or {}).get("text") or ""]
    for turn in reversed((memory or {}).get("turns") or []):
        if isinstance(turn, dict):
            turns.append(str(turn.get("user") or ""))
    try:
        from ..understanding import understand
        from ..knowledge import lookup
    except Exception:
        return ""
    before = (memory or {}).get("understood") or {}
    for line in turns:
        line = (line or "").strip()
        if not line:
            continue
        try:
            reply = getattr(lookup.find(understand(line, {"understood": before})), "reply", "")
        except Exception:
            continue
        if isinstance(reply, str) and reply.strip():
            written = reply.strip()
            return written, "said" if _same_as_the_last_answer(written, memory) else "card"
    try:
        from . import fallback
    except Exception:
        fallback = None
    for turn in reversed((memory or {}).get("turns") or []):
        if not isinstance(turn, dict):
            continue
        said = str(turn.get("bot") or "").strip()
        if said.endswith("?") or not _an_answer_worth_quoting(said):
            continue
        if fallback is not None and (fallback._is_a_hedge(said)
                                     or fallback._is_an_ask_which_bit(said)):
            continue
        opening = said[:60].lower()
        if "?" in opening or ":" in opening or "tell me" in opening or "say what" in opening:
            continue
        return said, "said"
    return "", ""


FIRST_BIT = re.compile(r"(?<=[.;:])\s+|\s+[\u2014\u2013]\s+")


def _the_first_bit(card, limit=150, skip_openers=False):
    said = str(card or "").strip()
    if not said:
        return ""
    first = FIRST_BIT.split(said, maxsplit=1)[0].strip()
    if skip_openers and len(first) < 30:
        rest = FIRST_BIT.split(said, maxsplit=1)
        if len(rest) > 1 and rest[1].strip():
            first = FIRST_BIT.split(rest[1].strip(), maxsplit=1)[0].strip()
    first = first.rstrip(" .;:")
    if len(first) > limit:
        cut = first[:limit]
        comma = cut.rfind(", ")
        first = cut[:comma] if comma > 40 else cut
        first = first.rstrip(" ,;:-")
    return first


def _leans_on(memory):
    understood = (memory or {}).get("understood") or {}
    lean = understood.get("leans_on") or {}
    return " ".join(lean.get("words") or ())


def _recent(memory, line=""):
    turns = (memory or {}).get("turns") or []
    said = []
    for turn in turns[-4:]:
        if not isinstance(turn, dict):
            continue
        text = str(turn.get("user") or "").strip().lower()
        if text and text != (line or "").strip().lower():
            said.append(text)
    return " ".join(said)


WISH_TO_DIE = re.compile(
    r"\b(?:want|wanna|wanting)\s+(?:to\s+)?die\b|\bkill\s+myself\b|\bend\s+it\s+all\b|"
    r"\bno\s+(?:point|reason)\s+(?:in\s+)?(?:living|going\s+on|carrying\s+on)\b|"
    r"\bbetter\s+off\s+dead\b|\bdon'?t\s+want\s+to\s+be\s+here\b",
    re.I)

AN_AGE = re.compile(r"\b(?:i'?m|im|i\s+am|turn(?:ing|ed)?|about|nearly|almost)\s+"
                    r"(?:to\s+be\s+)?(?:[1-9]\d)\b", re.I)


def reads(text, memory=None):
    line = (text or "").strip()
    if not line or len(line.split()) > 14:
        return None
    words = _words(line)
    if words & MED or words & BODY or words & THING or words & RECOVERY:
        return None
    match = COURSE.search(line)
    lasts = LASTS.search(line)
    if not match and not lasts:
        return None
    if not (ASKS.search(line) or line.endswith("?")):
        return None
    lean = _words(_leans_on(memory)) | _words(_recent(memory, line))
    if (words | lean) & DISTRESS or WISH_TO_DIE.search(line + " " + _recent(memory, line)):
        return None
    if not (words & HEAVY):
        card, source = _the_card_in_the_chat(memory)
        if card:
            return CARD_IN_THE_CHAT + ":" + source
        asks_about_a_feeling = bool(words & IT_IS_HOW_IT_FEELS)
        about_a_hard_time = bool(lean & HEAVY) or bool(lean & {"died", "death", "funeral", "loss"})
        like_this = bool(match) and "like this" in match.group(0).lower()
        nothing_named = len(_recent(memory, line).split()) < 3
        if (nothing_named and not asks_about_a_feeling and not about_a_hard_time and not like_this
                and not re.search(r"\bhow\s+long\b|\bhow\s+much\b|\bwhat\s+time\b",
                                  line.lower())):
            return NO_SUBJECT
    like_this = bool(match) and "like this" in match.group(0).lower()
    heavy = (like_this or bool(words & HEAVY) or bool(words & {"easier"})
             or bool(lean & HEAVY))
    if not heavy:
        return None
    ordinary = bool((words | lean) & ORDINARY) or bool(AN_AGE.search(line + " " + _recent(memory, line)))
    if ordinary and not ((words | lean) & CARE):
        return None
    if (lean & RECOVERY) and not (lean & CARE):
        return None
    understood = (memory or {}).get("understood") or {}
    if understood.get("body") or understood.get("about_bot"):
        return None
    return (match.group(0) if match else lasts.group(0)).strip().lower()


def reply_for(text, memory=None):
    asked = reads(text, memory)
    if not asked:
        return None
    if asked == NO_SUBJECT:
        said = (text or "").strip()
        pick = (sum(ord(c) for c in said) + 5 * len(said)) % len(NOTHING_NAMED)
        return NOTHING_NAMED[pick]
    if asked.startswith(CARD_IN_THE_CHAT):
        whole, source = _the_card_in_the_chat(memory)
        card = _the_first_bit(whole, skip_openers=(source == "said"))
        if not card:
            return None
        said = (text or "") + "|" + card
        pick = (sum(ord(c) for c in said) + 7 * len(said)) % 3
        timed = bool(TIME_IN_THE_CARD.search(whole))
        if EASING.search(text or ""):
            return EASES[pick].format(bit=card)
        if source == "card":
            return (CARD_PROSE if timed else CARD_PROSE_UNTIMED)[pick].format(bit=card)
        first = re.findall(r"[a-z']+", card.lower())
        if first and first[0] in DOES_IT:
            return (KEEP_UP if timed else KEEP_UP_UNTIMED)[pick].format(bit=card)
        return (STILL_STANDS if timed else STILL_STANDS_UNTIMED)[pick].format(bit=card)
    said = (text or "") + "|" + _leans_on(memory)
    pick = (sum(ord(c) for c in said) + 7 * len(said)) % len(PROSE)
    lean = _words(_leans_on(memory))
    if (_words(text) | lean) & CARE:
        return CARE_PROSE[pick % len(CARE_PROSE)]
    return PROSE[pick]
