import re

from ..understanding.kinds import a_stop_ask
from . import fallback, verdict

ON_SCREEN_LINES = (
    "That is in the answer above: {said}",
    "Same answer: {said}",
    "It is in what I said above: {said}",
)

STANDS_BY_LINES = (
    "I'd go by what I said: {said}",
    "I still stand by this: {said}",
    "Same answer, and it holds: {said}",
)

ON_SCREEN_ASK = re.compile(
    r"^(?:so|and|but|ok|okay|then|also)?\s*,?\s*(?:what|how|which|where|when|who|why|should|"
    r"shall|can|could|do|does|did|is|are|will|would|any)\b", re.I)

A_THING_NAMED_IN_FRONT = re.compile(
    r"^(?:so|and|but|ok|okay|then|also)?\s*,?\s*what about\b", re.I)

A_STEP_IN_IT = re.compile(
    r"\b(?:check|clean|clear|call|ring|ask|take|put|add|set|switch|turn|leave|keep|try|use|"
    r"replace|restart|update|move|fix|buy|get|book|look|make|run|wash|start|plug|test|wipe|"
    r"pull|open|close|soak|water|cut|pick|apply|scrub|hoover|vacuum|cover|store|wrap|rinse|"
    r"push|carry|plough|plow|soldier)\b",
    re.I)
NOT_TO_HAND_BACK = re.compile(
    r"^(?:hope\b|good luck|let me know|take care|all the best|sorry\b|i'm sorry|im sorry|"
    r"i don't know|i dont know|i'm not sure|im not sure|i can't|i cant|i would|i'd)", re.I)
ASKS_WHAT_TO_DO = re.compile(
    r"\b(?:what (?:should|do|can) i do|what do i do|how do i|how can i|should i|do i need to|"
    r"does that mean|will that|is that enough|is it enough|how much|how long|how often)\b", re.I)
POINTS_BACK = re.compile(
    r"\b(?:it|its|it's|that|this|they|them)\b"
    r"|\b(?:about|with) (?:the|my|our|his|her|their)\b", re.I)
NAMES_NOTHING_OF_ITS_OWN = frozenset((
    "look", "expect", "watch", "take", "bring", "wear", "say", "ask", "try", "buy", "get",
    "need", "want", "now", "next", "first", "else", "then", "there", "anything", "something",
    "work", "works",
    "actually", "really", "truly", "genuinely", "seriously", "even", "ever", "honestly",
    "help", "helps", "helping", "true", "right", "correct", "wrong", "case", "sure",
))
ASKS_RATHER_THAN_NAMES = frozenset("""
mean means meant stop stops started start keep keeps keeping give gives need needs
help helps try tries use uses used work works working do does doing done happen happening
happens enough better worse best long much many often soon cost costs price way time point
anyway else instead still just really actually suppose supposed about around
off out up down over back away on in through along ahead
""".split())
THE_THINGS_IT_COULD_BE_ABOUT = frozenset("""
smell smells smelly noise noisy sound sounds leak leaks leaking damp mould mold mildew stain
stains colour color taste tastes itch itchy ache aches pain pains mess dirty dirt rust rusty
water wet burning squeak squeaks rattle rattles bang banging drip dripping dust
""".split())
WHO_TO_TALK_TO = re.compile(
    r"\b(?:who can i (?:talk|speak|ring|call)|who should i (?:talk|speak|ring|call)|"
    r"who do i (?:talk|speak|ring|call)|where can i get help|who can help me)\b", re.I)
A_HELP_IN_IT = re.compile(
    r"\b(?:crisis line|helpline|hotline|samaritans|116 ?123|988|999|111|911|emergency number|"
    r"a and e|a&e|gp|doctor|nurse|midwife|health visitor|pharmacist|social worker|"
    r"ring|call|phone)\b", re.I)
A_BUY_ASK = re.compile(
    r"\b(?:do i need to buy|need to buy|anything to buy|what do i need to buy|what to buy|"
    r"will it cost|how much (?:is|does|will)|is it (?:cheap|expensive)|worth buying)\b", re.I)
A_PURCHASE_IN_IT = re.compile(
    r"\b(?:buy|buys|buying|bought|cost|costs|price|prices|pound|pounds|dollar|dollars|"
    r"cheap|cheaper|expensive|order|shop|store|supermarket|pharmacy|chemist|can of|a tube of|"
    r"a bottle of|a packet of|a box of)\b", re.I)
A_LEAD_IN = re.compile(r"^(?:so|then|and|but|also|now|first|next),?\s+", re.I)
QUOTED = re.compile(r"[\"\u201c\u201d][^\"\u201c\u201d]{2,}[\"\u201c\u201d]")
A_DECISION_ASK = re.compile(r"\b(?:should|shall|ought)\s+i\b|\bis it worth\b|\bdo i need\b",
                            re.I)
LONG_SENTENCE = 52


A_WORD_THAT_ONLY_JOINS = frozenset("""
because cause cos since whether though although while during before after until unless
not dont doesnt didnt cant cannot wont isnt arent wasnt werent havent hasnt couldnt wouldnt
shouldnt am are was were been being have has had having do does did doing can could would
should will shall may might must
""".split())


_DOUBLED = "bdgmnprtl"


def _stem(word):
    for ending in ("ing", "ed", "es", "s"):
        if len(word) - len(ending) >= 4 and word.endswith(ending):
            word = word[:-len(ending)]
            break
    if (len(word) >= 4 and word[-1] == word[-2] and word[-1] in _DOUBLED):
        word = word[:-1]
    return word


def _the_same_word(word, said):
    if word in said or word.rstrip("s") in said or word + "s" in said:
        return True
    if _stem(word) in _stems(said):
        return True
    return bool(len(word) >= 5 and any(len(other) >= 5 and word[:5] == other[:5]
                                      for other in said))


def _stems(words):
    return set(_stem(word) for word in words)


EFFORT_WORDS = frozenset("""push pushes pushing carry carrying keep keeping continue continuing
on through harder ahead along""".split())


def _names_something_new(mine, said, in_the_chat):
    last = mine[-1] if mine else ""
    for word in mine:
        if _the_same_word(word, said):
            continue
        if word in ASKS_RATHER_THAN_NAMES or word in EFFORT_WORDS:
            continue
        if word in THE_THINGS_IT_COULD_BE_ABOUT and _the_same_word(word, in_the_chat):
            continue
        if word != last and A_STEP_IN_IT.search(word):
            continue
        return True
    return False


def _the_words_in_the_chat(memory, answer):
    words = set(fallback._flat_words(answer))
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    for turn in turns[-2:]:
        words |= set(fallback._flat_words(str(turn.get("user") or "")))
    return words


def _the_answer_to_hand_back(memory):
    from ..memory import history

    return history.the_answer_on_screen(memory)


def _the_answer_is_a_card(memory):
    from ..memory import history

    return history.the_answer_is_a_card(memory)


CLAUSE_AFTER_A_COLON = re.compile(r":\s+(.+)$")


A_LONG_SENTENCE_SPLIT = re.compile(r":\s+|;\s+")


def _the_parts(sentence):
    if len(sentence.split()) <= LONG_SENTENCE:
        return [sentence]
    parts = [one.strip() for one in A_LONG_SENTENCE_SPLIT.split(sentence) if one.strip()]
    if len(parts) < 2:
        return [sentence]
    return [parts[0]] + [one[0].upper() + one[1:] for one in parts[1:]]


def _the_sentence_to_hand_back(sentence, mine, said):
    tail = CLAUSE_AFTER_A_COLON.search(sentence)
    if tail:
        clause = tail.group(1).strip()
        in_the_clause = any(_the_same_word(word, set(fallback._flat_words(clause)))
                            for word in mine)
        if (len(clause.split()) >= 6
                and (in_the_clause
                     or sum(1 for word in mine if _the_same_word(word, said)) == 0)):
            sentence = clause[0].upper() + clause[1:]
    return sentence


A_GO_ON_ASK = re.compile(
    r"\b(?:push(?:\s+(?:on|through|harder))?|carry\s+on|keep\s+(?:going|on|at\s+it|it\s+up)|"
    r"continuing|continue|go\s+on|going\s+on|crack\s+on)\b", re.I)
A_LIMIT_IN_IT = re.compile(
    r"\bas\s+far\s+as\b|\bfor\s+as\s+long\s+as\b|\bno\s+more\s+than\b|\bnot\s+(?:much\s+)?past\b|"
    r"\b(?:un)?til\s+(?:it|you|they|things|the\s+(?:pain|soreness|swelling|bleeding))\s*"
    r"(?:eases|eased|is\s+(?:better|easier|still|comfortable)|stops|settles|calms|feels|can|are\s+able|hurts|gets\s+worse)?\b|"
    r"\bwhile\s+(?:it|you|the|they)\b|\bshort\s+of\b|\bup\s+to\b|"
    r"\bstops?\s+(?:if|when|as\s+soon|before|at)\b|\bease[sd]?\s+off\b|\bback(?:s|ed)?\s+off\b|"
    r"\bfor\s+(?:a|the\s+first|one|two|three)\s+(?:week|fortnight|day|while|few)\b|"
    r"\bfor\s+a\s+while\b|\bin\s+short\s+bursts\b|\blittle\s+and\s+often\b|"
    r"\bno\s+more\s+of\s+than\b|\bwhen\s+it\s+(?:starts|hurts|gets\s+hard|feels)\b", re.I)
ASKS_WHAT_DECIDES = re.compile(
    r"\b(?:tell|say|let)\s+me\s+(?:what|how|which|whether|if|more)\b|"
    r"\bwhat\s+(?:it|they|you)\s+(?:did|does|looks?\s+like|smells?\s+like|tastes?\s+like)\b", re.I)
def the_answer_on_screen(text, memory):
    try:
        clean = " ".join(str(text or "").lower().split())
        if not clean or not ON_SCREEN_ASK.match(clean):
            return ""
        if A_THING_NAMED_IN_FRONT.match(clean):
            return ""
        if len(clean.split()) > 8:
            return ""
        if fallback._hedged_recently(memory):
            return ""
        answer = " ".join(str(_the_answer_to_hand_back(memory) or "").split())
        if not answer:
            return ""
        sentences = [one.strip() for one in re.split(r"(?<=[.!?])\s+", answer) if one.strip()]
        mine = [word for word in fallback.content_words(clean)
                if word not in A_WORD_THAT_ONLY_JOINS]
        said = set(fallback._flat_words(answer))
        asks_who_to_talk_to = bool(WHO_TO_TALK_TO.search(clean)) and _the_answer_is_a_card(memory)
        if (not asks_who_to_talk_to
                and not all(word in NAMES_NOTHING_OF_ITS_OWN for word in mine)
                and _names_something_new(mine, said, _the_words_in_the_chat(memory, answer))):
            return ""
        best, best_score, first_step, opening = "", 0, "", ""
        steps = []
        for sentence in sentences:
            if len(sentence.split()) < 5 or sentence.endswith("?"):
                continue
            if NOT_TO_HAND_BACK.match(sentence):
                continue
            if QUOTED.search(sentence):
                continue
            if any(punt in sentence.lower() for punt in fallback.PUNT):
                continue
            step = bool(A_STEP_IN_IT.search(sentence))
            if step:
                steps.append(sentence)
                if not first_step:
                    first_step = sentence
            if not opening:
                opening = sentence
            for piece in _the_parts(sentence):
                if len(piece.split()) > LONG_SENTENCE:
                    continue
                words = set(fallback._flat_words(piece))
                score = sum(1 for word in mine if _the_same_word(word, words))
                if score and score > best_score:
                    best, best_score = piece, score
        if (not best and first_step and ASKS_WHAT_TO_DO.search(clean)
                and POINTS_BACK.search(clean)):
            best = first_step
        says_it_again = False
        if asks_who_to_talk_to and not best:
            for sentence in sentences:
                if A_HELP_IN_IT.search(sentence) and not NOT_TO_HAND_BACK.match(sentence):
                    best = sentence
                    break
        if not best and opening and asks_who_to_talk_to:
            best, says_it_again = opening, True
        if not best and mine and all(word in NAMES_NOTHING_OF_ITS_OWN for word in mine):
            best, says_it_again = opening, True
        if not best and A_GO_ON_ASK.search(clean):
            best = next((one for one in steps
                         if A_LIMIT_IN_IT.search(one) or ASKS_WHAT_DECIDES.search(one)), "")
        if not best:
            return ""
        if A_DECISION_ASK.search(clean) and not A_STEP_IN_IT.search(best):
            return ""
        if A_BUY_ASK.search(clean) and not A_PURCHASE_IN_IT.search(best):
            return ""
        already = " ".join(fallback._flat_words(best))
        turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
        source = -1
        for place, turn in enumerate(turns):
            if str(turn.get("bot") or "") == answer:
                source = place
        for turn in turns[source + 1:]:
            if already and already in " ".join(fallback._flat_words(str(turn.get("bot") or ""))):
                return ""
        if not says_it_again:
            best = _the_sentence_to_hand_back(best, mine, said)
        first_said = " ".join(fallback._flat_words(answer))
        if (not says_it_again
                and first_said.startswith(" ".join(fallback._flat_words(best))[:60])):
            return ""
        given = A_LEAD_IN.sub("", best)
        if given and given != best:
            best = given[0].upper() + given[1:]
        if a_stop_ask(clean):
            frames = STANDS_BY_LINES
        else:
            frames = (ON_SCREEN_LINES[:1] if says_it_again else ON_SCREEN_LINES)
        reply = fallback._choose(frames, memory, clean).replace("{said}", best)
        flat = " ".join(fallback._flat_words(reply))
        recent = {" ".join(fallback._flat_words(str(t.get("bot") or "")))
                  for t in (memory.get("turns") or [])[-3:] if isinstance(t, dict)}
        if flat in recent:
            return ""
        return reply
    except Exception:
        return ""





_ABOUT_THE_CONVERSATION = re.compile(
    r"\b(?:hello again|hi again|you again|here again)\b"
    r"|\bwhere (?:were we|we (?:were|left off|got to)|did we (?:get to|get))\b"
    r"|\bwhat were we (?:saying|doing|on about)\b"
    r"|\bcarry on where\b|\bpick (?:it |things |up )?where\b"
    r"|\bas (?:i|we) (?:said|mentioned)\b|\blike i (?:said|mentioned|told you)\b"
    r"|\b(?:what|that) i (?:said|told you)\b"
    r"|\byou (?:said|mentioned|told me) (?:earlier|before|last time|a moment ago|just now)\b"
    r"|\byou said\s*:"
    r"|\bsince we last spoke\b|\bsame as before\b|(?<!not )\bthe last time\b|\blast time you\b"
    r"|\bearlier you\b", re.I)


def earlier_turn(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    return bool(isinstance(turns, list) and turns)


def talks_about_the_conversation(reply):
    unquoted = re.sub(r"[\"“][^\"”]*[\"”]", " ", str(reply or ""))
    return bool(_ABOUT_THE_CONVERSATION.search(unquoted))
