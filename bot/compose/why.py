import re

from . import pick
from ..memory import again, another

BARE_WHY = re.compile(
    r"^(?:(?:but|and|so|ok|okay|yeah|no|well|right)\s+)*"
    r"(?:"
    r"(?:why|y|how come)"
    r"(?:\s+(?:not|tho|though|so|then|is that|is it|was that|does it|do they|did it|did they|"
    r"would it|wouldnt it|should i|shouldnt i)(?:\s+(?:tho|though|then))?)?"
    r"(?:\s+(?:did|does|do|is|was|were|would|will|should)\s+"
    r"(?:that|it|this|they|those|these)"
    r"(?:\s+(?:happen|happened|happening|keep happening|keeps happening|work|works|not work|"
    r"never work|be|matter|help|go|goes|go wrong|goes wrong|come|do that|do it))?)?"
    r"|how come\s+(?:that|it|this)(?:\s+(?:happens?|happened|went wrong|goes wrong|keeps "
    r"happening))?"
    r"|what(?:'?s|\s+is|\s+was|\s+(?:could|might|would|can|may)\s+be)\s+causing\s+"
    r"(?:that|it|this)"
    r"|what(?:'?s|\s+is|\s+was)\s+(?:going wrong|wrong|the (?:problem|issue|matter))"
    r"|what\s+(?:am|are|was|were)\s+(?:i|we)\s+(?:doing\s+wrong|missing|getting\s+wrong)"
    r"|what\s+did\s+(?:i|we)\s+do\s+wrong"
    r")"
    r"[\s?!.,]*$",
    re.IGNORECASE)

CAUSING_IT = re.compile(
    r"what(?:'?s|\s+is|\s+was|\s+(?:could|might|would|can|may)\s+be)\s+causing\s+"
    r"(?:that|it|this)\b",
    re.IGNORECASE)

WRONG = re.compile(
    r"\bwhat(?:'?s|\s+is|\s+was)?\s*(?:am\s+i\s+)?(?:going\s+wrong|wrong|"
    r"doing\s+wrong|getting\s+wrong|missing|the\s+(?:problem|issue|matter))\b"
    r"|\bwhat\s+did\s+(?:i|we)\s+do\s+wrong\b",
    re.IGNORECASE)

LIFE = re.compile(
    r"\b(?:my (?:job|work|boss|career|business|kids?|children|son|daughter|mum|mom|dad|husband|"
    r"wife|partner|boyfriend|girlfriend|friend|sister|brother|family|marriage|relationship|"
    r"life|money|salary|wages|benefits|rent|interview|exam|degree|course)|"
    r"job|jobs|jobless|unemployed|redundant|sacked|fired|divorce|divorced|breakup|broke up|"
    r"shouting|shout at|arguing|argued|argument|falling out|fell out|not talking to me|"
    r"grieving|funeral|depressed|anxious|lonely|ashamed|guilty)\b",
    re.IGNORECASE)


def _named_as_a_sentence(last, reason):

    want = " ".join(str(reason or "").lower().split()).strip(" .,;:")
    if not want:
        return False
    for sentence in re.split(r"(?<=[.!?])\s+", str((last or {}).get("bot") or "")):
        found = NAMED_CAUSE.search(sentence)
        if not found:
            continue
        clause = " ".join(found.group(1).lower().split()).strip(" .,;:")
        if clause != want:
            continue
        return True
    return False


def _reads_a_fault(last):
    said = " ".join(str((last or {}).get("bot") or "").lower().split())
    them = " ".join(str((last or {}).get("user") or "").lower().split())
    if LIFE.search(them):
        return False
    return bool(said)


WHY_NOT = re.compile(r"\bnot\b", re.IGNORECASE)

THEIR_DECISION = re.compile(
    r"\b(?:he|she|they|him|her|them|his|their|"
    r"my (?:boss|manager|landlord|landlady|wife|husband|partner|boyfriend|girlfriend|ex|mum|mom|"
    r"mam|dad|father|mother|son|daughter|child|kid|friend|mate|neighbour|neighbor|colleague|"
    r"council|company|employer|school|teacher|gp|doctor|nurse|worker|agent|insurer)\b|"
    r"the (?:council|company|school|landlord|manager|boss|insurer|bank|hospital|surgery)\b)",
    re.IGNORECASE)
SAID_NO = re.compile(
    r"\b(?:said|says|saying|told|tells|refused|refuses|refusing|won'?t|wont|will not|"
    r"can'?t|cant|cannot|denied|rejected|decided|decides|reckons|thinks|banned|stopped|"
    r"turned (?:me|it|us) down|not allowed|no chance)\b",
    re.IGNORECASE)


def _about_someone_elses_decision(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return False
    for last in reversed(turns[-3:]):
        if not isinstance(last, dict):
            continue
        said = str(last.get("user") or "")
        if not said:
            continue
        low = " ".join(said.lower().split())
        if THEIR_DECISION.search(low) and SAID_NO.search(low):
            return True
    return False

THEIR_SUGGESTION = re.compile(
    r"\A(?:you (?:could|should|might|may|can) (?:try|just|also)|try|maybe try|have you tried"
    r"|why don'?t you|what about|how about|consider)\b"
    r"|\b(?:you (?:could|should|might) (?:try|also try)|have you tried)\b", re.IGNORECASE)
SUGGESTED_VERBS = frozenset((
    "try", "cut", "stop", "quit", "feed", "turn", "bleed", "top", "add", "start", "use", "take",
    "buy", "get", "give", "keep", "put", "run", "walk", "drink", "eat", "avoid", "ask", "go",
    "see", "check", "swap", "replace", "wash", "clean", "sort", "leave", "make", "do",
))


def _the_suggestion_was_theirs(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return False
    for last in reversed(turns[-3:]):
        if not isinstance(last, dict):
            continue
        said = str(last.get("user") or "")
        if not said:
            continue
        low = " ".join(said.lower().split())
        if THEIR_SUGGESTION.search(low):
            return True
        words = low.strip(" .,!?:;").split()
        if words and words[0].strip(".,!?:;") in SUGGESTED_VERBS:
            return True
    return False


ANSWERED = frozenset(("answers", "chat"))
SUBSTANCE = 8
HEDGED = re.compile(
    r"\b(?:search|searching|beyond what i know|don'?t know enough|not something i can see|"
    r"rather not guess|no way of knowing)\b",
    re.IGNORECASE)

WHY_ANSWERED = (
    "I'd be guessing at the reason - the cause is not something I can see from here. Which part "
    "of that do you want the why for?",
    "I don't know why, and I'd rather say so than invent one. What happens just before it goes "
    "wrong?",
    "Honestly the why is the bit I can't tell from this side. Tell me which part you mean and I "
    "will help you work it out.",
)

WHY_BODY = (
    "Honestly, I can't tell you why from here - I'd be guessing. What sets it off?",
    "I don't know the reason, and I'd rather say so than invent one. When did you first notice it?",
    "The why is the part I can't see from what you've told me. What is it like at its worst?",
    "No idea why, honestly. Does it happen at a particular time, or after anything in particular?",
)

CAUSE = re.compile(
    r"\b(?:because|since|that'?s why|which is why|that is why|is why|comes? from|caus(?:e|es|ed) by|"
    r"means that|so that|the reason (?:is|was)|scatters?|keeps? \w+ (?:from|off|out)|"
    r"stops? [^.]{0,28}?\b(?:forming|coming|happening|going|building|getting|spreading)|"
    r"is down to|which (?:makes|means|is why)|that'?s what (?:makes|keeps|stops|drives|turns)|"
    r"is what (?:drives|turns|causes|makes|keeps|stops)|"
    r"(?:has|have|had|got) (?:too (?:little|much)|not enough)|"
    r"(?:is|are) (?:almost |nearly |usually |normally |often |mostly )+(?:always )?\w|"
    r"live?s? in |breaks? (?:the |it |them )?\w+ into |"
    r"\b(?:sinks?|go(?:es)?|turns?|comes?|happens?|fails?|breaks?|stops?|sticks?|cracks?|"
    r"curdl(?:e|es)|collapses?|dries?|burns?|smells?|tastes?|looks?)\b"
    r"[^.;:]{0,40}?\bwhen\b|"
    r"\b(?:is|are|was|were)\s+[^.;:]{0,40}?\b\w+(?:ed|en)\b[^.;:]{0,20}?\b(?:by|from)\b)",
    re.IGNORECASE)
STEP_VERBS = (
    r"(?:ventilate|open|keep|use|take|leave|put|run|wipe|wash|give|avoid|let|get|ask|"
    r"check|try|swap|cover|move|hold|store|cook|drink|eat|sit|add|lower|raise|turn|clean|buy|"
    r"restrict|limit|reduce|cut|change|switch|replace|bin|tip|throw|sort|fit|hire|book|"
    r"pick|start|stop|do|make|go|wear|ring|call|fill|write|read|set|work|stay|carry|"
    r"delete|update|download|install|uninstall|restart|reboot|reinstall|clear|free|"
    r"close|move|rotate|treat|rinse|hoover|vacuum|dust|air|dry|iron|seal|label)")
SO_ADVICE = re.compile(r",? ?so (?=" + STEP_VERBS + r"\b)", re.IGNORECASE)
DOSE = re.compile(
    r"\b(?:once|twice|three times|four times|daily|weekly|nightly|every (?:day|week|night|morning)|"
    r"a (?:day|week|night|month)|per (?:day|week|month)|\d+ ?(?:times|minutes|hours|glasses|"
    r"litres|grams|g|mg|mg|ml|degrees|sessions))\b",
    re.IGNORECASE)
AND_STEP = re.compile(r",? ?and (?=(?!air\b)" + STEP_VERBS + r"\b)", re.IGNORECASE)
AND_ADVICE = re.compile(r",? ?(?:and|but) (?:it|they|that|this|you|then|if)\b", re.IGNORECASE)
NEGATIVE = re.compile(r"\b(?:never|don'?t|do not|avoid|no need to|there'?s no need)\b",
                      re.IGNORECASE)
CONDITIONAL = re.compile(r"\b(?:if|unless|once|when|before|after|until)\b", re.IGNORECASE)
CONDITIONAL_SENTENCE = re.compile(
    r"^(?:if|unless|once|whenever|when|before|after|until|in case)\b", re.IGNORECASE)
INSTRUCTION = re.compile(
    r"\b(?:never|don'?t|do not|keep|call|ring|take|ask|check|make sure|you should|if you|try to|"
    r"avoid|be careful|watch|use|put|put it|store|leave it|cover it|fit|swap|replace)\b",
    re.IGNORECASE)
PARTS = (": ", " - ", "; ")
SO_REASON = re.compile(
    r"\bso\s+(?:the|it|they|you|your|that|this|air|water|heat|warmth)\b",
    re.IGNORECASE)
LEADING_MARKER = re.compile(r"^(?:since|as|so)\s+(?=\w)", re.IGNORECASE)
CLAIM_BEFORE_COLON = re.compile(r"^[^:]{4,}?\b(?:is|are|was|were)\b[^:]*:\s*(?P<why>[^:]{12,})$",
                               re.IGNORECASE)
CLAIM_SUBJECT = re.compile(r"^\s*(?:here|there|this|these|those|what|below|following)\b",
                           re.IGNORECASE)
IMPERATIVE = re.compile(
    r"^(?:soak|add|mix|stir|do|use|put|take|keep|leave|cover|store|check|try|avoid|don'?t|never|"
    r"give|wipe|wash|open|close|turn|set|ring|call|ask|make|let|get|go|run|start|stop|fill|"
    r"brush|floss|drink|eat|sit|stand|sleep|walk|stretch|reduce|cut|change|swap|replace|clean|"
    r"remove|apply|spread|heat|cook|boil|bake|roast|freeze|thaw|rest|massage|wear|hang|bin|"
    r"throw|unplug|label|write|book|hire|buy|sell|learn|practise|practice|repeat|look|watch|"
    r"listen|say|tell|note|remember|think|pick|choose|plan|sort|fit|trim|prune|water|feed|"
    r"move|top|blot|rinse|scrape|vacuum|spray|chop|slice|simmer|grill|season|serve|"
    r"cool|chill|drain|pat|press|squeeze|peel|whisk|steam|blanch|defrost|shake|dust|sweep|mop|"
    r"scour|polish|iron|sand|prime|seal|charge|reboot|restart|reset|update|empty|plug|tighten|"
    r"loosen|screw|glue|nail|drill|measure|mark|taste|knead|fold|roll|save|delete)\b",
    re.IGNORECASE)
THE_FIX = re.compile(
    r"\b(?:is|was|are|'s) the (?:fix|answer|thing to do|way to do it)\b|\bfix next time\b|"
    r"\bthe fix (?:is|for|next time)\b|\bis how you (?:do|fix|stop|get)\b|"
    r"\bwhat (?:you do|to do) (?:next time|instead|now)\b",
    re.IGNORECASE)
NAMED_CAUSE = re.compile(r"\b(?:the\s+)?(?:cause|reason)\s+(?:is|was)\s+(.+)", re.IGNORECASE)
EXPLAINS = re.compile(
    r"\b(?:because|since|so\s+(?:air|the|it|they|you)|"
    r"so\s+\w+(?:\s+\w+){0,4}\s+(?:are|is|was|were)\b|"
    r"when\b[^.!?]*\b(?:are|is|was|were)\b|"
    r"which\s+(?:makes|means|traps|tightens|widens)|"
    r"making\b|heats?\s+(?:\w+ )?(?:up\b|the\b|it\b|them\b|your\b|a\b)|"
    r"expands?|traps?|tightens?|wide(?:ns?|ned|ning)?|"
    r"carries|evaporat(?:es|ed|ing)|scatters?|tell(?:s|ing)?\b[^.!?]*\bto\b|"
    r"seems?\s+to)\b",
    re.IGNORECASE)
DANGLING = re.compile(
    r"^(?:(?:but|and|so|though)\s+)?(?:if\s+)?"
    r"(?:it|they|he|she|that|this|these|those)\b"
    r"|^(?:then|also|which|the same)\b",
    re.IGNORECASE)
RESULT_NUMBER = re.compile(r",\s*so\b[^.!?]*\d", re.IGNORECASE)
CHANGE = re.compile(
    r"\b(?:sinks?|sank|rises?|rose|drops?|dropped|collapses?|collapsed|sags?|sagged|cracks?|"
    r"cracked|splits?|curdles?|curdled|separates?|separated|goes|went|gets|got|turns?|turned|"
    r"becomes?|became|sticks?|stuck|burns?|burnt|dries?|dried|toughens?|toughened|shrinks?|"
    r"shrank|smells?|smelt|tastes?|tasted|wrinkles?|wrinkled|tears?|tore|melts?|melted|sets?|"
    r"yellows?|yellowed|browns?|browned|wilts?|wilted|droops?|drooped|leaks?|leaked|clogs?|"
    r"clogged|overcooks?|overcooked|undercooks?|undercooked|overbakes?|overbaked|underbakes?|"
    r"underbaked|overmixes?|overmixed)\b",
    re.IGNORECASE)
WHEN_CAUSE = re.compile(r"\b(?:when|whenever)\b", re.IGNORECASE)
SO_FROM_HERE = re.compile(r",?\s+so\s+|;\s*", re.IGNORECASE)
WHY_NAMED = (
    "That's what is behind it: {c}",
    "It comes down to this: {c}",
    "{c} - that's the reason.",
)
KEEP_CAPITAL = frozenset((
    "i", "i'm", "i'd", "i've", "i'll", "monday", "tuesday", "wednesday", "thursday", "friday",
    "saturday", "sunday", "january", "february", "march", "april", "may", "june", "july",
    "august", "september", "october", "november", "december", "britain", "british", "england",
    "english", "london", "scotland", "wales", "ireland", "america", "american", "europe",
    "christmas", "easter", "god",
))


def _in_frame(frame, clause):
    word = clause.split(" ", 1)[0].strip("\"'(*[")
    keep = word.lower().strip(".,!?:;") in KEEP_CAPITAL or word[1:2].isupper()
    if frame.startswith("{c}"):
        return frame.replace("{c}", clause)
    if keep or not clause:
        return frame.replace("{c}", clause)
    return frame.replace("{c}", clause[:1].lower() + clause[1:])
WHY_NAMED_BECAUSE = (
    "Because {c}",
    "That's because {c}",
    "{c} - that's the reason.",
)

WHY_NAMED_SELF = (
    "The cause is {c}",
    "The reason is {c}",
)
WHY_FRONT = frozenset(
    front for front in (frame.split("{")[0].strip().rstrip(":").strip().lower()
                        for frame in WHY_NAMED + WHY_NAMED_BECAUSE + WHY_NAMED_SELF)
                if front)
WHY_END = "- that's the reason"


def is_a_reason_line(text):
    line = str(text or "").strip().lower().replace("\u2019", "'")
    if not line:
        return False
    if line.rstrip(" .").endswith(WHY_END):
        return True
    return any(line.startswith(front) for front in WHY_FRONT)

WHY_AGAIN = (
    "Because all I have is what you've told me, and the cause isn't in it - one more detail and I "
    "might see it.",
    "I still can't see the cause from here: it isn't in what you've told me. What does it do just "
    "before it goes wrong?",
    "The reason is still the part I can't reach from this side. When it goes wrong, what has just "
    "happened?",
)

WRONG_ANSWERED = (
    "I can't see what is going wrong from here, and I'd rather say so than invent a cause. Does "
    "it go wrong the same way every time?",
    "Nothing you've told me points at the cause, so I'd be guessing. Which part goes wrong - the "
    "start, the middle, or the end?",
    "I can't see what is wrong from here, and guessing would not help you. Talk me through what "
    "happens and I'll tell you what I can see in it.",
)

WRONG_NOT_A_FAULT = (
    "I can't see a reason in what you've told me, and I'd rather say that than invent one. What "
    "happened just before it?",
    "Nothing you've told me points at a cause, and I won't guess at one. Talk me through what "
    "happened and I'll tell you what I can see in it.",
    "I don't know why, honestly. Tell me a bit more about how it came about and I'll say what I "
    "can see.",
)

WHY_NOT_ANSWERED = (
    "I can't speak for anyone else's reasons - only for what you can do about it. What was said "
    "when you raised it?",
    "Fair question, and I have no way of knowing what is behind it. What is their side of it?",
    "I can't tell why not from here. What is stopping it, as far as you can see?",
)

WHY_NOT_ITS_OWN = (
    "No reason it has to be that way - it is the version that works for most people, not a rule. "
    "What is it about it that does not sit right?",
    "Only because it tends to be the one that works. If it does not suit you, say so and we will "
    "find another way.",
    "There is nothing wrong with the other way if it suits you. What are you weighing up?",
    "Mostly because it works for most people, not because it is the only way. What would you "
    "rather do?",
)


def _said_the_reason_cannot_be_seen(memory):
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns or not isinstance(turns[-1], dict):
        return False
    said = str(turns[-1].get("bot") or "")
    return (said in WHY_ANSWERED or said in WHY_BODY or said in WRONG_ANSWERED
            or said in WHY_METHOD or said in WRONG_NOT_A_FAULT)


THINKS_BACK = re.compile(
    r"^\W*(?:(?:but|and|so|ok|okay|yeah|no|well|right)\s+)*"
    r"(?:why|y)\s+(?:do|did|would)\s+(?:you|u)\s+(?:think|thinking)\s+(?:that|so|this|it)"
    r"(?:\s+(?:then|though|tho))?[\s?!.,]*$",
    re.IGNORECASE)


def _is_bare_why(clean):
    return bool(BARE_WHY.match((clean or "").strip()))


def _last_turn(memory):
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns:
        return {}
    skipped_a_nod = False
    for last in reversed(turns[-3:]):
        if not isinstance(last, dict):
            return {}
        said = last.get("bot")
        if isinstance(said, str) and _answered_nothing(said):
            skipped_a_nod = True
            continue
        if last.get("module") in ANSWERED:
            if not isinstance(said, str) or len(said.split()) < SUBSTANCE:
                return {}
            if skipped_a_nod:
                reason = _reason_in(last)
                if not reason or THE_REASON_POINTS_AT_THE_ADVICE.match(reason):
                    return {}
            return last
        if last.get("module") == "greeting" and isinstance(said, str) and HEDGED.search(said):
            continue
        return {}
    return {}


A_NOD_OPENS = re.compile(
    r"^(?:alright|all\s+right|ok|okay|sure|got\s+it|noted|right|of\s+course|no\s+problem|"
    r"lovely|great|good|glad|happy|sorry|thanks|thank\s+you|fair\s+enough|makes\s+sense|"
    r"understood|will\s+do|cool|nice)\b", re.I)
A_NOD_IS_SHORT = 12
THE_REASON_POINTS_AT_THE_ADVICE = re.compile(r"^(?:because\s+|since\s+)?(?:that|this)\b", re.I)


def _answered_nothing(said):
    said = (said or "").strip()
    if not said or len(said.split()) > A_NOD_IS_SHORT:
        return False
    if IMPERATIVE.match(said) or INSTRUCTION.search(said) or CAUSE.search(said):
        return False
    if EXPLAINS.search(said) or NAMED_CAUSE.search(said):
        return False
    return bool(A_NOD_OPENS.match(said))


FIRST_SENTENCES = 2


WHY_METHOD = (
    "Those steps are the how-to; the reason under them is the part I'd be guessing at. Tell me "
    "what happens and I'll say what I can see.",
    "Everything I gave you there is what to do, not why it happens - that half isn't in what I "
    "have. What is it doing when it goes wrong?",
    "The method is what I can stand behind. The cause is the bit I can't see from here, so tell me "
    "what it does and I'll work it back from that.",
)


def _gave_a_method(last):
    said = str(last.get("bot") or "")
    if not said:
        return False
    if CAUSE.search(said) or EXPLAINS.search(said) or NAMED_CAUSE.search(said):
        return False
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", said) if s.strip()]
    steps = [s for s in sentences if IMPERATIVE.match(s) or INSTRUCTION.search(s)]
    return bool(steps) and len(steps) * 2 >= len(sentences)


def _a_cause_named_outright(last):
    said = str(last.get("bot") or "")
    for sentence in re.split(r"(?<=[.!?])\s+", said)[:FIRST_SENTENCES]:
        text = sentence.strip()
        if IMPERATIVE.match(text):
            continue
        named = NAMED_CAUSE.search(text)
        if named and not THE_FIX.search(text):
            cause = named.group(1).strip().rstrip(".,;:")
            if len(cause.split()) >= 2:
                return cause
        thing = A_THING_NAMED_BEFORE_A_COLON.match(text)
        if thing:
            return "the " + thing.group("thing").strip()
    return ""


def _reason_in(last, strict=False):
    said = str(last.get("bot") or "")
    reason = _a_reason_in(said, strict=strict)
    if reason and _inside_a_quotation(said, reason):
        return _a_reason_in(_without_examples(said), strict=strict)
    return reason


EXAMPLE_IN_QUOTES = re.compile('"[^"]{4,}"|\u201c[^\u201d]{4,}\u201d')


def _without_examples(said):
    return EXAMPLE_IN_QUOTES.sub(" ", str(said or ""))


def _inside_a_quotation(said, clause):
    said = str(said or "")
    at = said.find(clause)
    if at <= 0:
        return False
    before = said[:at]
    marks = before.count('"') + before.count("\u201c") + before.count("\u201d")
    return marks % 2 == 1


def _a_reason_in(said, strict=False):
    whole = re.split(r"(?<=[.!?])\s+", said)
    sentences = whole[:FIRST_SENTENCES]
    for sentence in sentences:
        text = sentence.strip()
        if IMPERATIVE.match(text):
            continue
        named = (A_THING_NAMED_BEFORE_A_COLON.match(text)
                 or A_THING_NAMED_BEFORE_A_COLON.match(A_LEAD_IN.sub("", text)))
        if named:
            return "the " + named.group("thing").strip()
        short = SHORT_OF_A_CAUSE.match(text)
        if short:
            cause = " ".join(short.group("cause").split()).rstrip(".,;:")
            if len(cause.split()) >= 2:
                return cause
    for sentence in whole:
        found = NAMED_CAUSE.search(sentence)
        if (not found or INSTRUCTION.search(sentence) or RESULT_NUMBER.search(sentence)
                or THE_FIX.search(sentence)):
            continue
        clause = found.group(1).strip().rstrip(".,;:")
        if len(clause.split()) >= 2:
            return clause
    for sentence in sentences:
        named = WHAT_IT_TAKES.search(sentence)
        if named and not IMPERATIVE.match(sentence.strip()):
            clause = named.group(1).strip().rstrip(".,;:")
            if len(clause.split()) >= 3:
                return clause
    passes = (False,) if strict else (False, True)
    for instruction_ok in passes:
        for number, sentence in enumerate(sentences):
            if RESULT_NUMBER.search(sentence):
                continue
            if number and DANGLING.match(sentence.strip()):
                continue
            if number and not instruction_ok and INSTRUCTION.search(sentence):
                continue
            if CONDITIONAL_SENTENCE.match(sentence.strip()):
                continue
            trigger = _trigger_in(sentence)
            if (trigger and not THE_FIX.search(trigger)
                    and not (number and INSTRUCTION.search(sentence))):
                return trigger
            if (not CAUSE.search(sentence) and not CLAIM_BEFORE_COLON.match(sentence.strip())
                    and EXPLAINS.search(sentence) and not IMPERATIVE.match(sentence)
                    and not THE_FIX.search(sentence)
                    and not CONDITIONAL_SENTENCE.match(sentence.strip())
                    and not DOSE.search(sentence)
                    and not _is_the_answer_itself(said, sentence)):
                clause = sentence.strip().rstrip(".,;:")
                if len(clause.split()) >= 3:
                    return clause
            if CONDITIONAL_SENTENCE.match(sentence.strip()):
                continue
            parts = [sentence]
            for mark in PARTS:
                parts = [piece for part in parts for piece in part.split(mark)]
            for part in parts:
                clause = _cause_clause(part, number, instruction_ok)
                if clause and not THE_FIX.search(clause):
                    if strict and _carries_the_fix(sentence, clause):
                        return sentence.strip().rstrip(".,;:")
                    return clause
                trigger = _trigger_in(part)
                if (trigger and not THE_FIX.search(trigger)
                        and not (number and INSTRUCTION.search(part))):
                    return trigger
    named_class = _named_by_definition(said)
    if named_class:
        return named_class
    return _the_class_it_belongs_to(said)


WHAT_IT_TAKES = re.compile(
    r"^(?P<thing>[^.;:]{4,}?\b(?:is|are)\s+what\b[^,.;]{0,40}?(?:needs?|wants?|feeds?|"
    r"thrives? on|likes?|goes? for)\b[^,.;]*)[,.;]?\s+so\b", re.I)


A_THING_NAMED_BEFORE_A_COLON = re.compile(
    r"\A(?:it|that|this)\s+(?:is|was|isn'?t|wasn'?t)\s+"
    r"(?:almost\s+always\s+|nearly\s+always\s+|usually\s+|often\s+|just\s+)?"
    r"(?:the|a|an|your|too\s+much|not\s+enough|too\s+little)\s+(?P<thing>[a-z][^:,.;!?]{1,40}?)"
    r"(?:,\s*(?:not|rather\s+than)\s+(?:the\s+|a\s+|your\s+)?[a-z][^:,.;!?]{1,25})?"
    r"\s*:\s*\S",
    re.IGNORECASE)

A_LEAD_IN = re.compile(
    r"\A(?:(?:nine|eight|seven|six|five|four|three|two)\s+times\s+(?:in|out\s+of)\s+"
    r"(?:ten|twenty|a\s+hundred|\d+)|most\s+of\s+the\s+time|more\s+often\s+than\s+not"
    r"|usually|nearly\s+always|almost\s+always|in\s+my\s+experience|as\s+a\s+rule"
    r"|nine\s+times\s+out\s+of\s+ten)\s+",
    re.IGNORECASE)

SHORT_OF_A_CAUSE = re.compile(
    r"\A(?!(?:it|that|this|there|which)\b)[^.;:]{3,60}?\s+(?:is|are|was|were)\s+"
    r"(?:usually\s+|nearly\s+always\s+|almost\s+always\s+|often\s+|probably\s+|just\s+)?"
    r"(?P<cause>(?:short\s+of|low\s+on|lacking|too\s+much|too\s+little|not\s+enough)\b"
    r"[^.;:]{1,60})",
    re.IGNORECASE)
AFTER_THE_MARK = re.compile(r"^\s*(?::| - |; )\s*(?P<rest>.+)$")


def _is_the_answer_itself(said, sentence):
    whole = _words(said)
    part = _words(sentence)
    if not whole or not part:
        return False
    return len(part) >= max(3, int(len(whole) * 0.9))


def _words(text):
    return [word for word in re.split(r"[^a-z0-9']+", str(text or "").lower()) if word]


def _carries_the_fix(sentence, clause):
    rest = sentence.strip()
    if not rest.startswith(clause):
        return False
    found = AFTER_THE_MARK.match(rest[len(clause):])
    return bool(found and IMPERATIVE.match(found.group("rest").strip()))


def _trigger_in(part):
    text = str(part or "").strip()
    if not text or IMPERATIVE.match(text) or CONDITIONAL.match(text) or NEGATIVE.search(text):
        return ""
    for match in WHEN_CAUSE.finditer(text):
        head = text[:match.start()].strip()
        if len(head.split()) < 2 or not CHANGE.search(head):
            continue
        clause = SO_FROM_HERE.split(text[match.start():])[0]
        clause = clause.split(": ")[0]
        clause = (head + " " + clause).strip().rstrip(".,;:").strip()
        clause = _cut_long(clause)
        if len(clause.split()) < 4:
            continue
        return clause
    return ""



def _cause_clause(part, number, instruction_ok):
    found = CAUSE.search(part)
    if not found:
        found = SO_REASON.search(part)
    if not found:
        return ""
    if number and INSTRUCTION.search(part):
        return ""
    if not instruction_ok and IMPERATIVE.match(part.strip()):
        return ""
    if found.group(0).lower() in ("because", "since"):
        prefix = part[:part.lower().find(found.group(0).lower())]
        if NEGATIVE.search(prefix) or CONDITIONAL.search(prefix):
            return ""
    from_the_marker = (found.group(0).lower() in ("because", "since")
                       or found.re is SO_REASON)
    clause = (part[part.lower().find(found.group(0).lower()):]
              if from_the_marker else part)
    clause = SO_ADVICE.split(clause)[0]
    clause = AND_STEP.split(clause)[0]
    clause = AND_ADVICE.split(clause)[0]
    clause = LEADING_MARKER.sub("because ", clause.strip(), count=1)
    clause = clause.strip().rstrip(".,;:").strip()
    clause = _cut_long(clause)
    if len(clause.split()) < 3:
        return ""
    if not clause.lower().startswith(("because ", "since ")) and IMPERATIVE.match(clause):
        return ""
    return clause


A_GENERAL_CLAIM = re.compile(
    r"\A(?:most|almost\s+all|nearly\s+all|in\s+most\s+cases|the\s+majority\s+of|mostly)\s+"
    r"(?P<subject>[^.;:,]{2,60}?)\s+(?:is|are|was|were)\s+(?P<what>[^.;:]{2,140})",
    re.IGNORECASE)
ENDS_THE_CLASS = re.compile(r"(?::|,| - | and | so | which | but | worse )", re.IGNORECASE)
SAYS_WHAT_IT_DOES = re.compile(
    r"\b(?:want|wants|need|needs|live|lives|take|takes|last|lasts|go|goes|come|comes|get|gets|"
    r"settle|settles|heal|heals|die|dies|cost|costs|help|helps|work|works|hold|holds|keep|keeps|"
    r"put|puts|eat|eats|do|does|say|says|give|gives|pay|pays|rise|rises|fall|falls|start|starts|"
    r"finish|finishes|run|runs|turn|turns|sit|sits|charge|charges|cover|covers|include|includes|"
    r"pass|passes|count|counts|matter|matters|mean|means|stay|stays|carry|carries)\b",
    re.IGNORECASE)
A_PLACEHOLDER = frozenset(("it", "this", "that", "them", "they", "one", "so", "true", "fine",
                           "ok", "okay", "normal", "harmless", "nothing", "none", "air", "you",
                           "me", "us"))


def _the_class_it_belongs_to(said):
    first = re.split(r"(?<=[.!?])\s+", str(said or "").strip())[0].strip()
    if IMPERATIVE.match(first) or CONDITIONAL_SENTENCE.match(first):
        return ""
    found = A_GENERAL_CLAIM.match(first)
    if not found:
        return ""
    claim = ENDS_THE_CLASS.split(found.group("what"), 1)[0].strip().rstrip(".,;:")
    if len(claim.split()) < 1 or len(claim.split()) > 14:
        return ""
    if SAYS_WHAT_IT_DOES.search(claim) or re.search(r"\d", claim):
        return ""
    if claim.lower() in A_PLACEHOLDER or THE_FIX.search(claim):
        return ""
    if INSTRUCTION.search(claim) or DOSE.search(claim):
        return ""
    subject = found.group("subject").strip()
    lead = first[:found.start("what")].strip()
    return "{} {}".format(lead or "Most " + subject, claim)


def _named_by_definition(said):
    for sentence in re.split(r"(?<=[.!?])\s+", str(said or ""))[:1]:
        found = CLAIM_BEFORE_COLON.match(sentence.strip())
        if not found or CLAIM_SUBJECT.match(sentence) or IMPERATIVE.match(sentence.strip()):
            continue
        why = found.group("why").strip().rstrip(".,;:")
        if why[:1] in "\"'\u2018\u201c" or IMPERATIVE.match(why) or INSTRUCTION.match(why):
            continue
        why = SO_ADVICE.split(why)[0].strip().rstrip(".,;:")
        why = _cut_long(why)
        if len(why.split()) < 4:
            continue
        return "because " + why[0].lower() + why[1:]
    return ""


def _cut_long(clause):
    words = clause.split()
    if len(words) <= 24:
        return clause
    head = " ".join(words[:24])
    at = max(head.rfind(", "), head.rfind(" - "))
    if at < len(head) // 3:
        return ""
    return head[:at]


ANSWER_LONG = 18


ACT_NOW = re.compile(
    r"\b(?:999|911|112|a&e|a and e|ambulance|paramedic|unconscious|"
    r"not breathing|can'?t breathe|scald\w*|never open|still hot|poison\w*|gas leak|on fire|"
    r"stop driving|pull over|don'?t wait|do not wait|stay on the line)\b",
    re.IGNORECASE)
ACT_NOW_SOON = re.compile(
    r"\b(?:111|same[- ]day|straight away|right away|immediately|today)\b",
    re.IGNORECASE)
CONDITIONAL = re.compile(r"\b(?:if|unless|should|in case|any time)\b", re.IGNORECASE)
SENTENCE = re.compile(r"[^.?!;]+[.?!;]?")


def _an_answer_to_act_on(last):
    said = str(last.get("bot") or "")
    if not said:
        return False
    if ACT_NOW.search(said):
        return True
    for sentence in SENTENCE.findall(said):
        if ACT_NOW_SOON.search(sentence) and not CONDITIONAL.search(sentence):
            return True
    return False


SAID_AGAIN = re.compile(
    r"^(?!so\s+what\b)"
    r"(?:(?:sorry|ok|okay|er|erm|um|eh|and|so|but|wait|no|yes)[\s,]+)*"
    r"(?:"
    r"what|wat|wot|wut|huh|pardon"
    r"|what\s+did\s+(?:you|u)\s+say"
    r"|what\s+(?:was|is)\s+that"
    r"|say\s+(?:that|it)\s+again|say\s+again|come\s+again|run\s+that\s+by\s+me\s+again"
    r")"
    r"(?:\s+(?:sorry|please|mate|then|now))?[\s?!.,]*$",
    re.IGNORECASE)
AGAIN_SHORTER = (
    "In short: {short}",
    "Shorter: {short}",
    "The short of it: {short}",
    "The gist of it: {short}",
)
REPEAT_LEADS = tuple(str(frame).split("{short}")[0] for frame in AGAIN_SHORTER)
CLAUSE_END = re.compile(r":\s+|;\s+")
_A_SAVE_LEAST = 5
_A_CLAUSE_LEAST = 6
_A_LONG_SENTENCE = 25
_A_STRIDE = 3
AGAIN_WORDS = 40
NO_CUT = re.compile(
    r"\b(?:gp|doctor|nurse|pharmacist|chemist|dentist|physio\w*|midwife|health visitor|"
    r"111|999|a&e|hospital|ambulance|paramedic)\b"
    r"|\b(?:get|have)\s+it\s+(?:checked|looked at|seen)\b"
    r"|\bworth\s+(?:getting|having)\s+.{0,30}?(?:checked|looked at)\b", re.IGNORECASE)
END_OF_SENTENCE = re.compile(r"(?<=[.!?])\s+")


OPENS_ON_CARE = re.compile(
    r"^(?:ok|okay|right|well|oh|ah|aw|ugh|sorry)?[\s,\u2014-]*"
    r"(?:i'?m (?:really |so )?sorry|sorry|that (?:is|was) (?:a rough|rough|tough|hard|a lot)|"
    r"no wonder|that sounds|lousy|horrible|awful|poor you|rough one)\b", re.IGNORECASE)


def _first_sentence(said):
    said = " ".join(str(said or "").split())
    if not said:
        return ""
    parts = [part.strip() for part in END_OF_SENTENCE.split(said) if part.strip()]
    if len(parts) < 2:
        return ""
    return parts[0].rstrip(",;:- ")


def _a_shorter_way(said):
    said = " ".join(str(said or "").split())
    if not said:
        return ""
    lead = _past_a_lead_in(said)
    first = _first_sentence(lead)
    if first:
        doing = _the_doing_of(first)
        if doing:
            return doing
        clause = _a_clause_of(first)
        if len(first.split()) > _A_LONG_SENTENCE:
            if clause and len(clause.split()) * _A_STRIDE <= len(first.split()):
                return clause
            if lead != " ".join(said.split()):
                return _end_a_sentence(first)
            return ""
        elif clause and len(clause.split()) * 2 >= len(first.split()):
            return clause
        if len(first.split()) <= AGAIN_WORDS:
            return _end_a_sentence(first)
        return clause
    return _a_clause_of(_past_a_lead_in(said))


def _past_a_lead_in(said):
    parts = [part.strip() for part in END_OF_SENTENCE.split(said) if part.strip()]
    if len(parts) < 2:
        return said
    if len(parts[0].split()) >= _A_CLAUSE_LEAST + 2:
        return said
    return said[len(parts[0]):].strip()


def _end_a_sentence(text):
    text = (text or "").strip().rstrip(",;:- ")
    if not text:
        return ""
    return text if text[-1] in ".!?" else text + "."


def _a_clause_of(sentence):
    sentence = (sentence or "").strip()
    for match in CLAUSE_END.finditer(sentence):
        cut = sentence[:match.start()].strip().rstrip(",;:-\u2014 ")
        if len(cut.split()) < _A_CLAUSE_LEAST + 2:
            continue
        if not _brackets_closed(cut):
            continue
        if not _carries_a_verb(cut) or _leans_back(cut):
            continue
        if _points_at_what_follows(cut):
            continue
        return _end_a_sentence(cut)
    return ""


def _the_doing_of(sentence):
    sentence = (sentence or "").strip()
    for match in CLAUSE_END.finditer(sentence):
        cut = sentence[:match.start()].strip().rstrip(",;:-\u2014 ")
        if len(cut.split()) < _A_CLAUSE_LEAST + 2:
            continue
        if not _brackets_closed(cut):
            continue
        if _points_at_what_follows(cut):
            continue
        return _end_a_sentence(_the_half_that_does_it(cut, sentence[match.end():]))
    return ""


_A_DOING = re.compile(
    r"\b(?:turn|switch|take|keep|put|use|try|check|give|add|buy|swap|replace|clean|wash|rinse|"
    r"leave|stand|wrap|store|feed|water|encourage|bleed|call|ask|book|avoid|stop|start|run|set|"
    r"hold|move|cover|cut|open|close|repeat|ring|email|text|pick|press|fill|mix|stir|boil|blot|"
    r"pour|write|say|tell|offer|lower|heat|defrost|freeze|lock|shut|prick|scrub|soak|scrape|"
    r"wipe|sweep|vacuum|iron|sand|seal|tape|glue|screw|drill|tie|hang|fold|chop|slice|drain|"
    r"compare|measure|weigh|test|log|track|budget|plan|read|learn|practise|split|share|anchor|"
    r"aim|ask|check|brush|clear|empty|refill|label|freeze|work|go|look|listen|watch|wait|sit|"
    r"step|point|answer|name|note|mark|count|sort|tidy|eat|drink|cook|bake|grill|roast|serve|"
    r"pack|carry|lift|bend|stretch|breathe|rest|get|give|help|do|redo|rub|polish|dry|spray|"
    r"apply|dab|swab|wax|shampoo|polish)\b",
    re.IGNORECASE)
_A_DOING_WINDOW = 3
_A_FIGURE = re.compile(
    r"\d|\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|"
    r"forty|fifty|half|quarter|once|twice|per ?cent)\b", re.IGNORECASE)


_A_LEAD_IN = frozenset("""on for in with at to from after before if when once and then also""".split())


def _opens_a_doing(half):
    words = re.findall(r"[a-z']+", str(half or "").lower())
    if not words:
        return False
    if _A_DOING.fullmatch(words[0]):
        return True
    if words[0] in _A_LEAD_IN:
        return any(_A_DOING.fullmatch(word) for word in words[1:_A_DOING_WINDOW + 2])
    return False


_SAYS_HOW = re.compile(
    r"\b(?:is|are|was|were|has|have|had|does|do|will|would|can|could|wants?|needs?|keeps?|"
    r"stops?|strips?|holds?|works?|matters?|helps?|makes?|means?|costs?|takes?|gets?|gives?|"
    r"comes?|stays?|lasts?)\b", re.IGNORECASE)


def _says_how_it_works(half):
    first = re.split(r"[,;]", str(half or ""))[0]
    return bool(_SAYS_HOW.search(first) or _VERB_SHAPE.search(first))


_ANNOUNCES = re.compile(
    r"\b(?:it|them|these|those|this|that)\b(?:\s+[\w'-]+){0,2}\s+(?:order|list|steps?|way|shape)\b",
    re.IGNORECASE)


def _announces_the_list(half):
    return bool(_ANNOUNCES.search(half or ""))


_NEEDS_A_SUBJECT = re.compile(
    r"^(?:he|she|it|they|them|this|that|these|those|his|her|their|its|itself|themselves)\b", re.I)
_A_PARTICIPLE = frozenset("""laid launched built made given taken held written born grown founded
opened designed painted published signed set sold bought won lost sent kept left put begun""".split())


def _needs_its_subject(after):
    words = str(after or "").split()
    if not words:
        return True
    if _NEEDS_A_SUBJECT.match(words[0]):
        return True
    first = re.sub(r"[^a-z]", "", words[0].lower())
    return first in _A_PARTICIPLE and first not in ("set", "left", "put", "lost")


_VERB_SHAPE = re.compile(r"\b\w{4,}(?:ed|ing)\b", re.I)
_A_VERB = frozenset("""is are was were be been am has have had do does did can could will would
should must might may need needs want wants take takes give gives make makes keep keeps leave
leaves put puts get gets add adds use uses turn turns go goes come comes cost costs last lasts
help helps hold holds cut cuts run runs set sets let lets seem seems feel feels work works mean
means change changes choose chooses find finds show shows matter matters depend depends ring
rings wash washes clean cleans""".split())
_A_CAUSE_OPENS = re.compile(
    r"^(?:nearly|usually|mostly|often|almost|probably|generally|mainly|sometimes|always|never|"
    r"rarely|hardly)\b", re.I)


def _carries_a_verb(half):
    text = str(half or "")
    if not text.strip():
        return False
    if _A_DOING.search(text) or _VERB_SHAPE.search(text):
        return True
    if any(word in _A_VERB for word in re.findall(r"[a-z']+", text.lower())):
        return True
    if _A_FIGURE.search(text):
        return True
    return bool(_A_CAUSE_OPENS.match(text))


_LEANS_BACK = re.compile(
    r"\b(?:them|these|those|both|each|either|neither|the rest|all of (?:the|them)|the others?|"
    r"any of (?:the|them)|that end|this end|this order|these steps|the ones|"
    r"as follows)\b", re.I)


_LEANS_BACK_WINDOW = 6


def _leans_back(half):
    return bool(_LEANS_BACK.search(" ".join(str(half or "").split()[:_LEANS_BACK_WINDOW])))


_EXPLAINS = re.compile(r"^(?:a|an|the|most|some|many|much|which|because|so|that|this)\b", re.I)


_A_REASON_LEAST = 12


def _the_reason(after):
    after = str(after or "")
    if len(after.split()) > _A_REASON_LEAST or "," in after or ";" in after:
        return False
    return _carries_a_verb(after)


_OPENS_ON_A_FIGURE = re.compile(r"^\s*(?:[£$\u20ac]\s*\d|\d)")


def _opens_on_a_figure(after):
    return bool(_OPENS_ON_A_FIGURE.match(str(after or "")))


_A_CATEGORY = re.compile(
    r"\b(?:it|them|these|those|things|stuff|bits|ones|kinds|sorts|lots)\b"
    r"|\b(?:need|needs|want|wants|have|has|how|what|where|when|who)\s+to\W*$",
    re.I)


def _names_no_particular(before):
    return bool(_A_CATEGORY.search(before or ""))


def _the_half_that_does_it(before, after):
    before = (before or "").strip()
    after = (after or "").strip().rstrip(",;:- ")
    if len(after.split()) < _A_CLAUSE_LEAST // 2:
        return ""
    if not _carries_a_verb(after) or _leans_back(after):
        return ""
    if _needs_its_subject(after):
        return ""
    if _opens_a_doing(before) and not _announces_the_list(before):
        if _opens_a_doing(after):
            if len(after.split()) >= len(before.split()):
                return after[:1].upper() + after[1:]
            return ""
        if _the_reason(after) or _opens_on_a_figure(after):
            return ""
        if _A_FIGURE.search(before) and not _opens_on_a_figure(after):
            return ""
        if not _names_no_particular(before):
            return ""
        if _says_how_it_works(after):
            return ""
        return after[:1].upper() + after[1:]
    if _opens_a_doing(after):
        if _A_FIGURE.search(before) and not _opens_on_a_figure(before) and not _names_no_particular(before):
            return ""
        return after[:1].upper() + after[1:]
    if _EXPLAINS.match(after):
        if _A_FIGURE.search(before) and not _opens_on_a_figure(after):
            return ""
        if not _names_no_particular(before):
            return ""
        if _the_reason(after):
            return ""
        if _carries_a_verb(before):
            return after[:1].upper() + after[1:]
        return ""
    if not _A_FIGURE.search(before) and _A_FIGURE.search(after):
        return after[:1].upper() + after[1:]
    return ""


_POINTS_FORWARD = re.compile(r"\b(?:it|them|these|those)\W*$", re.IGNORECASE)
_POINTS_FORWARD_ANY = re.compile(
    r"\bthe (?:most|best|worst|biggest|main|first|last|rest)\W*$", re.IGNORECASE)
_POINTS_FORWARD_LEAST = 10


def _points_at_what_follows(cut):
    cut = (cut or "").strip()
    if _POINTS_FORWARD_ANY.search(cut):
        return True
    return bool(_POINTS_FORWARD.search(cut)) and len(cut.split()) < _POINTS_FORWARD_LEAST


def _brackets_closed(text):
    text = text or ""
    return (text.count("(") == text.count(")") and text.count("[") == text.count("]"))


def _the_route_is_in_it(said):
    return bool(NO_CUT.search(str(said or "")))


def said_again(clean, memory):
    if not SAID_AGAIN.match(clean):
        return None
    if _an_answer_to_act_on(_last_turn(memory)):
        return None
    short = _not_shortened(_said_above(memory))
    if not short:
        return None
    return pick(AGAIN_SHORTER, memory, clean).replace("{short}", short)


def is_the_answer_shorter(reply, last):
    text = str(reply or "").strip()
    short = ""
    for lead in REPEAT_LEADS:
        if text.startswith(lead):
            short = text[len(lead):]
            break
    if not short:
        return False
    words = re.findall(r"[a-z0-9']+", short.lower())
    previous = re.findall(r"[a-z0-9']+", str(last or "").lower())
    if len(words) < 3 or len(previous) < len(words) + 4:
        return False
    size = len(words)
    return any(previous[start:start + size] == words
               for start in range(0, len(previous) - size + 1))


def _said_above(memory):
    last = _last_turn(memory)
    return _unframed(str(last.get("bot") or ""))


def _unframed(reply):
    reply = str(reply or "")
    for lead in REPEAT_LEADS:
        if reply.startswith(lead) and reply[len(lead):].strip():
            return reply[len(lead):].strip()
    found = another.FRAME.match(reply)
    if found and reply[found.end():].strip():
        return reply[found.end():].strip()
    return again.unframed(reply) or reply


def _not_shortened(said):
    said = str(said or "")
    if len(said.split()) < ANSWER_LONG:
        return ""
    if CARE_ANSWER.search(said) or OPENS_ON_CARE.match(_first_sentence(said) or said):
        return ""
    if _the_route_is_in_it(said):
        return ""
    short = _a_shorter_way(said)
    echo = _first_sentence(_past_a_lead_in(said)) or said
    doing = _end_a_sentence(_the_doing_of(echo))
    if doing and short == doing:
        echo = said
    saved = len(echo.split()) - len(short.split()) if short else 0
    if _past_a_lead_in(said) == " ".join(str(said or "").split()) and \
            saved < max(_A_SAVE_LEAST, len(echo.split()) // 4):
        return ""
    return short


def takes_as_it_comes(text, memory):
    clean = " ".join(str(text or "").lower().split())
    if SAID_AGAIN.match(clean):
        if _an_answer_to_act_on(_last_turn(memory)):
            return False
        if not _not_shortened(_said_above(memory)):
            return False
        return True
    if not _is_bare_why(clean):
        return False
    last = _last_turn(memory)
    if _an_answer_to_act_on(last):
        return False
    if _said_the_reason_cannot_be_seen(memory):
        return True
    return len(str(last.get("bot") or "").split()) >= ANSWER_LONG


WHY_YOU_SAID_IT = re.compile(
    r"^(?:(?:but|and|so|ok|okay|yeah|no|well|right)\s+)*"
    r"(?:"
    r"(?:why|y|how come)\s+(?:(?:do|did|would|will|are|were)\s+)?(?:you|u)\s+"
    r"(?:say|saying|said|tell me|told me|reckon|claim)"
    r"|what\s+makes\s+(?:you|u)\s+say"
    r"|why\s+(?:do\s+you\s+|would\s+you\s+)?think"
    r")\s+(?:that|this|so|it|those|these)"
    r"(?:\s+is)?(?:\s+(?:then|though|tho))?[\s?!.,]*$",
    re.IGNORECASE)
THE_BOT_DESCRIBED_ITSELF = re.compile(
    r"\b(?:a program|a chatbot|a bot|not a person|no feelings|nothing in me|just rules|"
    r"written rules|rules someone wrote|rules doing their job|no mind behind|behind the "
    r"curtain|nothing to report on my side|no inner)\b",
    re.IGNORECASE)
CARE_ANSWER = re.compile(
    r"\b(?:i'?m (?:really |so )?sorry|so sorry|sorry to hear|sorry about|a real loss|"
    r"be gentle with yourself|no words needed|you did the right thing|i'?m here for you|"
    r"here if you want|nothing you have to say|how are you (?:holding up|doing))\b",
    re.IGNORECASE)
WHY_CARE = (
    "Nothing behind it: you told me something hard, and I meant it.",
    "No reason beyond what you said - I'm sorry, and I still mean it.",
    "There's nothing to work out in it: you said something hard, and that was enough for me to "
    "be sorry about it.",
)
WHY_THE_BOT = (
    "Because there is nothing in here to feel it with: I'm rules someone wrote for ordinary "
    "questions, and the words come from those rather than from anything I have lived.",
    "Because that is all I am made of - written rules. Nothing in me feels something first and "
    "reports it after, so there is no inner reason behind the line.",
    "Because there is no machinery for it in here, which is the whole of the answer: I pick the "
    "words from what is written into me and from what you have told me here.",
)
ABOUT_THE_BOT_LINE = re.compile(
    r"^\W*(?:(?:so|ok|okay|and|but|well|right|hey|hi)\s+)*"
    r"(?:(?:are|do|did|does|can|could|would|will|have|has|were|is)\s+(?:you|u|ya)\b"
    r"|(?:you|u)\s+(?:are|re)\b"
    r"|tell me about yourself\b|what are you\b|who are you\b|what do you do\b)",
    re.IGNORECASE)


def asks_about_the_last_answer(clean):
    return bool(WHY_YOU_SAID_IT.match((clean or "").strip()))


def respond_to_a_saying_ask(clean, memory, understood=None, body=False):
    if THINKS_BACK.match((clean or "").strip()):
        if not _the_turn_above(memory).get("bot"):
            return None
        return respond(clean, memory, understood, body=body)
    if not asks_about_the_last_answer(clean):
        return None
    said = str(_the_turn_above(memory).get("user") or "")
    if ABOUT_THE_BOT_LINE.match(said):
        return pick(WHY_THE_BOT, memory, clean)
    above = str(_the_turn_above(memory).get("bot") or "")
    if CARE_ANSWER.search(above):
        return pick(WHY_CARE, memory, clean)
    if THE_BOT_DESCRIBED_ITSELF.search(above):
        return pick(WHY_THE_BOT, memory, clean)
    last = _last_turn(memory)
    if not last:
        return None
    if not _reason_in(last):
        from ..memory import topics
        return topics.said_again(str(_the_turn_above(memory).get("bot") or ""), memory)
    return respond("why", memory, understood, body=body)


def _the_turn_above(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return {}
    last = turns[-1]
    return last if isinstance(last, dict) else {}


def respond(clean, memory, understood=None, body=False):
    again = said_again(clean, memory)
    if again:
        return again
    thinks_back = bool(THINKS_BACK.match((clean or "").strip()))
    if not (_is_bare_why(clean) or thinks_back):
        return None
    last = _last_turn(memory)
    if not last:
        if THE_BOT_DESCRIBED_ITSELF.search(str(_the_turn_above(memory).get("bot") or "")):
            return pick(WHY_THE_BOT, memory, clean)
        if _said_the_reason_cannot_be_seen(memory):
            return pick(WHY_AGAIN, memory, clean)
        return None
    act_now = _an_answer_to_act_on(last)
    whole_thing = bool(WRONG.search(clean) or CAUSING_IT.search(clean))
    if WHY_NOT.search(clean):
        reason = "" if act_now else _a_cause_named_outright(last)
        if not reason:
            if _about_someone_elses_decision(memory):
                return pick(WHY_NOT_ANSWERED, memory, clean)
            if _the_suggestion_was_theirs(memory):
                return pick(WHY_NOT_ITS_OWN, memory, clean)
            return pick(WHY_NOT_ANSWERED, memory, clean)
    else:
        reason = "" if act_now else _reason_in(last, strict=whole_thing)
    if reason:
        said = reason[len("because "):] if reason.lower().startswith("because ") else reason
        if _named_as_a_sentence(last, said):
            pool = WHY_NAMED_SELF
        else:
            pool = WHY_NAMED_BECAUSE if said is not reason else WHY_NAMED
        reply = _in_frame(pick(pool, memory, clean), said)
        reply = reply if reply.endswith((".", "!", "?")) else reply + "."
        reply = reply[0].upper() + reply[1:]
        return reply
    if thinks_back and not act_now:
        from ..memory import topics
        handed_back = topics.said_again(str(_the_turn_above(memory).get("bot") or ""), memory)
        if handed_back:
            return handed_back
    if body:
        return pick(WHY_BODY, memory, clean)
    if not act_now and whole_thing and _gave_a_method(last) and _reads_a_fault(last):
        return pick(WHY_METHOD, memory, clean)
    if whole_thing:
        pool = WRONG_ANSWERED if _reads_a_fault(last) else WRONG_NOT_A_FAULT
        return pick(pool, memory, clean)
    return pick(WHY_ANSWERED, memory, clean)
