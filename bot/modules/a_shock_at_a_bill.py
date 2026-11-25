import re


PRIORITY = 1000

A_BODY_ENDING = re.compile(
    r"\b(?:nearly|almost|bloody\s+near|like\s+to\s+have)\s+"
    r"(?:died|fell\s+over|fainted|passed\s+out|choked|keeled\s+over|collapsed)\b"
    r"|\b(?:had|having)\s+a\s+heart\s+attack\b|\bmy\s+heart\s+(?:stopped|sank)\b"
    r"|\bcould(?:n'?t| not)\s+(?:breathe|get\s+my\s+breath|catch\s+my\s+breath)\b"
    r"|\bmy\s+(?:jaw|eyes|heart)\s+(?:dropped|fell|nearly\s+dropped)\b"
    r"|\b(?:was|were)\s+(?:gasping|choking)\b|\bchoked\b|\bgasped\b"
    r"|\bnearly\s+(?:cried|wept)\b"
    r"|\bwent\s+(?:white|pale)\b|\bmy\s+knees\s+(?:went|gave)\b", re.I)
A_SHOCK_AT_A_PAGE = re.compile(
    r"\btook\s+my\s+breath\s+away\b|\bmy\s+(?:jaw|heart)\s+(?:dropped|fell|sank)\b"
    r"|\bwent\s+(?:white|pale)\b|\bmy\s+knees\s+(?:went|gave)\b", re.I)
A_DOCUMENT = re.compile(
    r"\b(?:bill|bills|statement|statements|invoice|invoices|invoiced)\b", re.I)
_NOT_YET = re.compile(
    r"\b(?:hasn'?t|hasnt|haven'?t|havent|hadn'?t|hadnt|didn'?t|didnt|never|no)\b"
    r"[^.!?]{0,30}\b(?:arrived|come|came|turned\s+up|showed\s+up)\b"
    r"|\bno\s+(?:bill|statement|invoice)\s+(?:yet|at\s+all)\b"
    r"|\b(?:not|never)\s+(?:had|received|got)\s+(?:it|a\s+(?:bill|statement|invoice))\s+yet\b"
    r"|\bstill\s+waiting\b", re.I)


A_PAGE_VERB = re.compile(
    r"\b(?:saw|seen|opening|opened|read|reading|looked\s+at|looking\s+at|looked\s+through|"
    r"checked|checking|got|get|received|receiving|landed|arrived|through\s+the\s+door)\b", re.I)
_ONLY_THE_PAGE = re.compile(
    r"^(?:i|we)?\s*(?:have\s+|had\s+|just\s+|only\s+just\s+|finally\s+|today\s+|"
    r"this\s+morning\s+|yesterday\s+)*"
    r"(?:saw|seen|opened|opening|read|reading|got|get|received|checked|looked\s+at)\s+"
    r"(?:the|my|this|our|that|a)\s+"
    r"(?:bill|bills|statement|statements|invoice|invoices)\b"
    r"(?:\s+(?:today|yesterday|this\s+morning|last\s+night|again|now))?[.!]*$", re.I)


def _a_complaint_added_after_the_ending(text):
    line = " ".join((text or "").lower().split())
    said = A_BODY_ENDING.search(line)
    if not said:
        return False
    tail = line[said.end():]
    after = set(re.findall(r"[a-z']+", tail))
    if after & (_A_SYMPTOM | _ALSO_A_COMPLAINT):
        return True
    if _A_WENT_OUT_COLD.search(tail):
        return True
    return bool(after & _A_BODY_WORD) and bool(_A_STATE_OF_A_BODY.search(tail))


_ALSO_A_COMPLAINT = frozenset((
    "numb", "numbness", "weak", "weakness", "shaky", "shaking", "lightheaded", "sweating",
    "faint", "fainting", "dizzy", "dizziness", "breathless", "breathlessness",
))

_A_WENT_OUT_COLD = re.compile(r"\b(?:blacked out|blackout|blacked|passed out|out cold|unconscious|"
                              r"keeled over|collapsed|fainted|fainting fits?)\b")
_A_STATE_OF_A_BODY = re.compile(
    r"\b(?:hurt|hurts|hurting|sore|soreness|tight|tightness|numb|numbness|ache|aches|aching|throb|"
    r"throbbing|swollen|swelling|bleeding|stiff|stiffness|weak|weakness|shaky|shaking|still|worse|"
    r"pounding|squeezing|burning|itchy|itching|watering|gone|goes|went)\b")

try:
    from ..compose.fallback_data import BODY_PARTS as _A_BODY_WORD
    from ..compose.fallback_data import SYMPTOM_WORDS as _A_SYMPTOM
except Exception:
    _A_BODY_WORD = frozenset((
        "arm", "back", "chest", "ear", "eye", "eyes", "foot", "hand", "head", "hip", "jaw",
        "knee", "leg", "neck", "shoulder", "skin", "stomach", "teeth", "throat", "toe", "wrist",
    ))
    _A_SYMPTOM = frozenset((
        "ache", "aches", "bleed", "bleeding", "bruise", "confused", "cough", "dizzy", "fever",
        "headache", "hurt", "hurting", "hurts", "nausea", "nauseous", "pain", "painful", "rash",
        "sick", "sore", "swollen", "temperature", "tired", "vomit", "vomiting", "wheezing",
    ))


def _the_page_in_hand(line):
    return bool(_ONLY_THE_PAGE.match(line) and not _NOT_YET.search(line))


def _the_ending_and_the_page(text):
    line = " ".join((text or "").split())
    if not line:
        return False
    if _the_page_in_hand(line):
        return True
    if _NOT_YET.search(line) and A_DOCUMENT.search(line) and A_BODY_ENDING.search(line):
        return True
    page = A_SHOCK_AT_A_PAGE.search(line)
    if page:
        return bool(A_DOCUMENT.search(line))
    said = A_BODY_ENDING.search(line)
    if not said:
        return False
    after = A_DOCUMENT.search(line, said.end())
    if after:
        return True
    document = A_DOCUMENT.search(line)
    if not document:
        return False
    before = line[:document.start()]
    return bool(A_PAGE_VERB.search(before[-24:]))


_BILL_LINES = (
    "A bill is worth checking before you pay it: the dates it covers, what it says you are being "
    "charged for, and the reference. Ask for the breakdown in writing, and if it is wrong say so "
    "in writing before the date on it, keeping a copy. What is it for, and how much?",
    "Before paying a bill you did not expect, check the dates it covers, what it is charging for "
    "and the reference. Ask for the breakdown in writing, and answer in writing before the date "
    "on it, keeping a copy. What is it charging you for?",
)
_WITHOUT_A_FIGURE = (
    "That is worth checking before you pay it: the dates it covers, what it says you are being "
    "charged for, and the reference. Ask for the breakdown in writing, and if it is wrong say so "
    "in writing before the date on it, keeping a copy. What is the reference on it?",
    "Before you pay it, check the dates it covers, what it says you are charged for and the "
    "reference. Ask for the breakdown in writing and keep a copy of everything. Does it say what "
    "period it covers?",
)
_BEFORE_IT_COMES = (
    "When it comes, the three things to find are the date they want an answer by, what it says you "
    "are charged for and the reference. Ask them to confirm when it was sent and to which address, "
    "and note who you spoke to and when.",
    "While you wait, it is worth confirming they have your right address, and noting "
    "the date and the name of whoever you speak to. When it lands, the reply-by date, what it "
    "charges for and the reference are the things to check first.",
)
_A_FIGURE = re.compile(
    r"(?:\u00a3\s*\d|\b\d+(?:[.,]\d+)?\s*(?:pounds?|quid|p|per\s?cent|%)\b"
    r"|\b(?:for|of|cost(?:s|ing)?|paid|owe[sd]?|totall?ing)\s+\u00a3?\d+)", re.I)


def _pick(lines, memory):
    try:
        last = str(((memory or {}).get("turns") or [{}])[-1].get("bot") or "")
    except (AttributeError, IndexError, TypeError):
        last = ""
    for line in lines:
        if line != last:
            return line
    return lines[0]


_A_ACCOUNT_WORD = frozenset("""
account annual quarterly monthly bank bill card charge council credit debit electricity electric
energy gas insurance internet loan metered metering meter mobile mortgage phone rent service
sewerage student supply tax tv utility water
""".split())

_A_WORD_ABOUT_ANY_BILL = frozenset("""
a an the my our your their his her its this that these those some any no
big small huge massive enormous enormous giant tiny little
new old latest last first second third final whole same other another next
unexpected surprise shocking ridiculous stupid bloody damn awful terrible
monthly quarterly annual weekly daily
""".split())


A_BILL_WITH_ITS_OWN_CARD = ("council tax",)


_A_WORD_BEFORE_A_KIND = frozenset("""
i me my we us our you your he him his she her it its they them their
saw see seen seeing read reading reads open opened opening opens got get gets getting
receive received receiving arriving arrived arrive came come comes coming
paid pay paying sent send sends sending took take taken
in on at for from with about of to and but or when after before then now today
the first second last final
""".split())


_A_SOMEBODY_ELSE = re.compile(
    r"\b(?:my|his|her|their|our)\s+(?:mum|mom|mammy|dad|father|mother|son|daughter|"
    r"wife|husband|partner|boyfriend|girlfriend|nan|nana|gran|granny|grandma|granddad|"
    r"grandad|grandpa|grandmother|grandfather|brother|sister|uncle|aunt|cousin|friend|"
    r"kid|kids|child|baby|boy|girl|dog|cat|neighbour|neighbor)\b"
    r"|\b(?:he|she|they|him|her|them)\b")


def _the_ending_is_somebody_elses(text):
    line = " ".join((text or "").lower().split())
    said = A_BODY_ENDING.search(line)
    if not said:
        return False
    return bool(_A_SOMEBODY_ELSE.search(line[:said.start()]))


def _a_kind_word_in_front_of_the_page(text):
    line = " ".join((text or "").lower().split())
    for document in A_DOCUMENT.finditer(line):
        before = re.findall(r"[a-z']+", line[max(0, document.start() - 40):document.start()])
        for word in reversed(before):
            if word in _A_WORD_ABOUT_ANY_BILL:
                continue
            if word in _A_WORD_BEFORE_A_KIND or word in _A_ACCOUNT_WORD:
                return ""
            return word
    return ""


def _a_bill_of_another_kind(text):
    low = " ".join((text or "").lower().split())
    return bool(_a_kind_word_in_front_of_the_page(text)) or any(
        kind in low for kind in A_BILL_WITH_ITS_OWN_CARD)


A_MONEY_PROBLEM = re.compile(
    r"\b(?:charged\s+(?:me\s+)?twice|double\s+charged|charged\s+me\s+double|duplicate|"
    r"overcharged|over\s*charged|cant\s+pay|can'?t\s+pay|cant\s+afford|can'?t\s+afford|"
    r"cannot\s+pay|cannot\s+afford|owe|owes|owed|arrears|in\s+arrears|payment\s+plan|"
    r"instal+ments?|wrong|too\s+much|discount|rebate|refund|benefit|hardship|"
    r"meter\s+read|reading|estimated)\b", re.I)


def TAKES_AS_IT_COMES(text, memory=None):
    if not _the_ending_and_the_page(text):
        return False
    if _a_complaint_added_after_the_ending(text):
        return False
    if _the_ending_is_somebody_elses(text):
        return False
    if _a_money_problem_in_the_line(text, memory):
        return False
    return not _a_bill_of_another_kind(text)


def _ask_for_what_is_missing(memory, text):
    line = " ".join((text or "").split())
    if _NOT_YET.search(line):
        return _pick(_BEFORE_IT_COMES, memory)
    said_the_figure = bool(_A_FIGURE.search(line))
    lines = _WITHOUT_A_FIGURE if said_the_figure else _BILL_LINES
    return _pick(lines, memory)


A_MONEY_IN_THE_ANSWER = re.compile(
    r"\b(?:pay|pays|paid|payment|payments|overdraft|refund|refunds|duplicate|charge|charges|"
    r"charged|owe|owes|arrears|debit|instal+ments?|bill|bills|council|band|discount|discounts|"
    r"rebate|tariff|standing\s+charge|meter|account|bank|money|rent)\b", re.I)


def _a_money_problem_in_the_line(text, memory=None):
    if not A_MONEY_PROBLEM.search(" ".join(str(text or "").lower().split())):
        return False
    try:
        from . import answers as _answers
        reply = _answers.respond(text, memory if isinstance(memory, dict) else {})
    except Exception:
        return False
    return bool(reply) and bool(A_MONEY_IN_THE_ANSWER.search(reply))


def respond(text, memory=None):
    if not _the_ending_and_the_page(text):
        return None
    if _a_complaint_added_after_the_ending(text):
        return None
    if _the_ending_is_somebody_elses(text):
        return None
    if _a_money_problem_in_the_line(text, memory):
        return None
    if _a_bill_of_another_kind(text):
        return None
    try:
        return _ask_for_what_is_missing(memory or {}, text)
    except Exception:
        return None
