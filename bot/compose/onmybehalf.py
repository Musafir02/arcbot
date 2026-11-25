import re

from . import fallback_data, pick

_FLAT = (fallback_data.NEUTRAL, fallback_data.A_THING_SEEN_TO, fallback_data.A_THING_DONE,
         fallback_data.A_SMALL_DAY)

_ASKING_BACK = re.compile(
    r"^\s*(?:(?:please|pls|plz|just|ok|okay|now|and|also|so|then|hi|hey)\s+)*"
    r"(?:(?:can|could|would|will)\s+(?:you|u)\s+(?:please\s+|just\s+|kindly\s+|also\s+)*"
    r"|(?:i\s+(?:want|need|would\s+like)\s+you\s+to\s+))?")

_A_SEARCH = re.compile(
    r"^\s*(?:(?:please|pls|plz|just|ok|okay|now|and|also|so|then)\s+)*"
    r"(?:(?:can|could|would|will)\s+(?:you|u)\s+(?:please\s+|just\s+|kindly\s+|also\s+)*)?"
    r"(?:search|look\s+(?:it\s+)?up|look\s+for|google|browse|compare|check\s+(?:the\s+)?"
    r"(?:price|prices|times|flights|trains|availability))\b")

_A_SPEND = re.compile(
    r"^\s*(?:(?:please|pls|plz|just|ok|okay|now|and|also|so|then)\s+)*"
    r"(?:(?:can|could|would|will)\s+(?:you|u)\s+(?:please\s+|just\s+|kindly\s+|also\s+)*)?"
    r"(?:book|reserve|order|buy|purchase|pay|top\s+up|renew|cancel|check\s+(?:me\s+)?in|"
    r"get\s+me\s+(?:a\s+)?(?:ticket|table|seat|room))\b")

_A_MESSAGE_OUT = re.compile(
    r"^\s*(?:(?:please|pls|plz|just|ok|okay|now|and|also|so|then)\s+)*"
    r"(?:(?:can|could|would|will)\s+(?:you|u)\s+(?:please\s+|just\s+|kindly\s+|also\s+)*)?"
    r"(?:send|email|text|forward|share|print|post|mail|message)\b")

_A_LIST = re.compile(
    r"^\s*(?:(?:please|pls|plz|just|ok|okay|now|and|also|so|then)\s+)*"
    r"(?:(?:can|could|would|will)\s+(?:you|u)\s+(?:please\s+|just\s+|kindly\s+|also\s+)*)?"
    r"(?:save|keep|store|note|jot|add|put|write\s+(?:it|this|that)\s+down|"
    r"make\s+a\s+note|set\s+(?:a|an)\s+(?:reminder|alarm)|"
    r"remind\s+(?:me|us)\s+to|remember\s+(?:that|to))\b")

_THEIR_ERRAND = re.compile(
    r"\b(?:me|my|mine|our|ours|us|for\s+me|for\s+us|this|that|these|those|it|them|"
    r"(?:the|a|an)\s+\w+)\b")

_KEEP_OUT = re.compile(
    r"\b(?:how\s+(?:do|can|should|would|to)\b|what\s+should|should\s+i|shall\s+i|"
    r"is\s+it\s+worth|worth\s+it|do\s+you\s+think|"
    r"i\s+(?:have\s+|already\s+)?(?:booked|ordered|bought|paid|sent|saved|added)|"
    r"i\s+(?:did|tried)|my\s+(?:mum|dad|son|daughter|friend|husband|wife|partner|boss|carer|"
    r"neighbour|brother|sister|nan|gran|grandad|child)\s+(?:has|have|wants|asked|said)|"
    r"ambulance|999|911|112|A&E|a\s*&\s*e|doctor|gp|surgery|nurse|pharmacist|chemist|"
    r"hospital|pain|rash|lump|bleeding|blood|breath|chest|dose|medicine|tablet|"
    r"an\s+email\s+(?:from|about)|a\s+(?:text|letter|email)\s+(?:from|about)|"
    r"send\s+my\s+(?:love|regards|wishes|thanks|best)|love\s+to\b|"
    r"(?:give|send)\s+(?:them|him|her)\s+my\b)")

A_NO_SEARCH = (
    "Nothing here can search the web - no browser on this side. Say what matters most about "
    "{what} and I'll help you work out what to compare; the site or app itself has the rest.",
    "I can't look anything up live, sorry. Tell me what you need to know about {what} and I'll "
    "say what to look for and what to ignore; whoever sells it has today's version.",
    "No search from here - I only know what is in my own head, and none of it changes today. Name "
    "the details that matter about {what} and I'll narrow it down before you open the site.",
)

A_NO_SPEND = (
    "I can't book, order or pay for anything - no account, no card, no hands. Do it in their app "
    "or on their site, and tell me the price first: I'll say whether it looks fair and what to "
    "check before you pay.",
    "Nothing on my side can hold a booking or take money. Read their cancellation line before you "
    "click buy - it is the one part of this that costs you later - and say what you are buying "
    "and I'll say what to watch.",
    "That one needs your account, not me: I can't reach a basket or a booking form. Tell me what "
    "it costs and what it covers, and I'll help you work out whether the dearer one earns its "
    "money.",
)

A_NO_SEND = (
    "I can't send or print anything - nothing leaves this chat. I'll get {what} right here "
    "instead, in full; copying it across is the one press on your side.",
    "No email, no text, no printer on my side, sorry. What I can do is get {what} exactly right "
    "here; pasting it over is the last step, and it is yours.",
    "Nothing here can post or send. I'll write {what} out so it is ready to go - the copy and the "
    "send are the two presses on your end.",
)

A_NO_LIST = (
    "Nothing here keeps a list between chats - every chat starts fresh, so what you put here does "
    "not come back tomorrow. Write it where you'll see it (your phone's notes, a paper by the "
    "door) and tell me the items: I'll help you sort them.",
    "I can't save anything, sorry - there is nowhere on my side for it to live. Say the items out "
    "loud here and I'll help you order and trim the list; then keep it in your own notes.",
    "No memory of a list once we stop talking. Give me the lot and I'll group them by where they "
    "are in the shop; your notes app is the thing that will still have it tomorrow.",
)


_THE_VERB_AND_THEN = re.compile(
    r"^\s*(?:(?:please|pls|plz|just|ok|okay|now|and|also|so|then)\s+)*"
    r"(?:(?:can|could|would|will)\s+(?:you|u)\s+(?:please\s+|just\s+|kindly\s+|also\s+)*)?"
    r"(?:search|look\s+(?:it\s+)?up|look\s+for|google|browse|compare|check|"
    r"send|email|text|forward|share|print|post|mail|message|"
    r"book|reserve|order|buy|purchase|pay|top\s+up|renew|cancel|"
    r"save|keep|store|note|jot|add|put|write\s+(?:it|this|that)\s+down)\b\s*", re.I)
_A_LEADING_PREPOSITION = re.compile(r"^\s*(?:for|about|on|at|into|up|out|down|to)\b\s*", re.I)
_THE_ADDRESSEE = re.compile(r"^\s*(?:me|us)\b\s*", re.I)
_THE_TAIL_OF_THE_ASK = re.compile(
    r"\s+(?:for\s+(?:me|us)|to\s+(?:me|us)|please|pls|now|asap|online|thanks|ta|cheers|"
    r"out|up|down|here)\s*[.!?]*$", re.I)
_A_MERE_PRONOUN = frozenset(("it", "that", "this", "them", "those", "these", "one", "things"))

_MINE = re.compile(r"\b(my|our|mine|ours)\b", re.IGNORECASE)
_YOURS = {"my": "your", "our": "your", "mine": "yours", "ours": "yours"}


def _facing_them(phrase):
    return _MINE.sub(lambda found: _YOURS[found.group(1).lower()], phrase)


def _what_was_asked_for(clean):
    after = _THE_VERB_AND_THEN.sub("", clean or "", count=1)
    after = _THE_ADDRESSEE.sub("", after or "", count=1)
    for _ in range(4):
        before = after
        after = _A_LEADING_PREPOSITION.sub("", after, count=1).strip()
        after = _THE_TAIL_OF_THE_ASK.sub("", after).strip(" .!?,")
        if after == before:
            break
    words = [w for w in after.split() if w]
    if not words or len(words) > 8 or (len(words) == 1 and words[0] in _A_MERE_PRONOUN):
        return "it"
    return " ".join(words)


def _is_a_flat_read(reply):
    return any(reply in pool for pool in _FLAT)


def _is_a_hedge(reply):
    from . import fallback
    from ..memory import store_lines
    if fallback.is_a_hedge(reply):
        return True
    return any(reply in pool for pool in (store_lines.POINTS_BACK_NOTHING,
                                         store_lines.POINTING_WORD_NOTHING))


def _about_an_errand(clean):
    if len(clean.split()) > 14:
        return None
    a_search = bool(_A_SEARCH.search(clean))
    if not a_search and not _THEIR_ERRAND.search(clean):
        return None
    if _KEEP_OUT.search(clean):
        return None
    if a_search:
        return A_NO_SEARCH
    if _A_SPEND.search(clean):
        return A_NO_SPEND
    if _A_MESSAGE_OUT.search(clean):
        return A_NO_SEND
    if _A_LIST.search(clean):
        return A_NO_LIST
    return None


def answer_for(text, memory, reply):
    if not reply:
        return None
    clean = " ".join((text or "").lower().split())
    if not clean:
        return None
    pool = _about_an_errand(clean)
    if not pool:
        return None
    if not _is_a_flat_read(reply) and not (pool is A_NO_SEARCH and _is_a_hedge(reply)):
        return None
    return pick(pool, memory, text).format(what=_facing_them(_what_was_asked_for(clean)))
