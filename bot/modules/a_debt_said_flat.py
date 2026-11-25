import re

from ..compose import pick

PRIORITY = -500

_A_RATE = re.compile(r"\b(\d{1,2}(?:\.\d{1,2})?)\s*(?:%|per\s?cent|percent)")
_A_BORROWING = re.compile(
    r"\b(?:credit\s+card|store\s+card|storecard|credit\s+cards|payday\s+loan|overdraft|"
    r"debt|debts|catalogue|klarna|bnpl|buy\s+now\s+pay\s+later|a\s+loan|my\s+loan|the\s+loan|"
    r"loan|loans|card|cards)\b"
    r"|\b(?:my|the|on\s+the|our|me)\s+(?:visa|mastercard|amex|american\s+express)\b"
    r"|\b(?:visa|mastercard)\s+card\b")
_A_JOINED = re.compile(r"^(?:and|but|so|also|then|plus|or|what\s+about|how\s+about|"
                       r"same|still|anyway)\b")
_A_BALANCE = re.compile(r"£\s?\d[\d,]*|\b\d[\d,]{2,7}\s?(?:pounds|quid|grand|k\b)?"
                        r"|\b\d+\s?(?:grand|k\b)")
_A_DEBT_DONE = re.compile(
    r"\b(?:paid\s+off|paid\s+up|paying\s+off|cleared|clearing|settled|rid\s+of|getting\s+rid|"
    r"sorted\s+out|over\s+with|done\s+with)\b"
    r"|\b(?:paid|pay|paying|settled)\b[^.?!]{0,20}\b(?:off|up)\b")
_A_NOT_THIS_DEBT = re.compile(
    r"\bstudent\s+(?:loan|loans|debt|debts|finance|loan\s+company)\b|\bplan\s+[1245]\b"
    r"|\bmaintenance\s+loan\b|\bmortgage\b|\bmortgages\b")
_A_PAYMENT = re.compile(r"\b\d[\d,]{1,7}\s?(?:pounds|quid|grand|k)?\s*(?:a|per|each)\s*"
                        r"(?:month|week|year|fortnight)\b")
_A_DEBT_NAMED = re.compile(
    r"\b(?:credit\s+cards?|store\s*cards?|storecards?|overdraft|catalogue|klarna|bnpl|"
    r"pay\s?day\s+loans?|buy\s+now\s+pay\s+later|a\s+loan|my\s+loan|the\s+loan|loans|"
    r"debts?)\b|\b(?:my|the|our|on\s+the|me)\s+(?:visa|mastercard|amex|american\s+express)\b"
    r"|\b(?:visa|mastercard)\s+card\b")
_A_GREETING_CARD = re.compile(
    r"\b(?:birthday|christmas|xmas|thank[- ]?you|sympathy|get[- ]well|anniversary|leaving"
    r"|wedding|new\s+baby|congratulations|farewell)\s+cards?\b"
    r"|\bcards?\s+(?:for|from|to)\s+(?!my\s+card|the\s+card|pay)\w+"
    r"|\b(?:bought|buy|buying|sent|send|sending|gave|give|giving|made|making|got|getting|"
    r"picked\s+up|picking\s+up)\b(?:\s+(?!on\b|off\b)\w+){0,3}\s+"
    r"(?:a|an|the|some)\s+cards?\b")

_A_HAVE = re.compile(r"\b(?:got|have|has|owe|owes|ive|weve|theyve|there'?s)\b")
_A_THINKING = re.compile(r"\b(?:spend|spending|spent|overspend|stop|again|keep|"
                         r"shouldn'?t|worried|scared|hate|stuck|struggling)\b")
_A_ASK = re.compile(
    r"^(?:should|shall|can|could|would|do|does|did|is|are|was|were|what|how|which|when|where|"
    r"who|why|worth|better|best)\b")

A_DEBT_RATE = (
    "That is an expensive rate: {rate}% a year is more than most savings accounts pay, so spare "
    "money does more going off the balance than into a saver. Roughly what is on it?",
    "{rate}% is dear money, more than most savers pay you, so clearing it first beats saving "
    "alongside it. How much is left on it?",
    "At {rate}% that is costing you every month it sits there, and it is more than most savings "
    "pay, so the balance comes first. How much is on it?",
)

A_DEBT_BALANCE = (
    "A balance like that is usually the first thing to clear: it costs more than most saving "
    "pays, so spare money is better off going to it than to a saver. Can you pay more than the "
    "minimum?",
    "That is the one to aim spare money at, since borrowing costs more than a saver pays you. "
    "What is the rate on it, and is it the only one?",
    "It is usually the first thing to clear, ahead of saving: what goes on the balance saves you "
    "more than the same money earns in a saver. Is it just the one balance?",
)

A_DEBT_CHEAP = (
    "At {rate}% that is cheap borrowing, so it is not the one to panic about; what matters is "
    "whether the rate is fixed or runs out, because a cheap rate that jumps is where these get "
    "away from people. Do you know when it ends?",
    "{rate}% is a low rate, so it is not costing you much; the thing to check is how long it "
    "lasts and what it becomes afterwards, which the terms you were given will say. Is it fixed "
    "for a set time?",
)


A_DEBT_STORE = (
    "Store cards and catalogues are usually the dearest borrowing in the shop: the rate is on the "
    "statement, and it is often twice what a credit card charges. How much is on it?",
    "Catalogue and store card rates are the ones worth checking first, because they are sold at "
    "the till rather than compared. What is the rate, and how much is left on it?",
)

A_DEBT_BNPL = (
    "Buy now pay later is free until the date it is not: what catches people is the deadline "
    "passing and the fee that lands with it. When is the payment due?",
    "The thing that matters with buy now pay later is the date the interest-free bit ends, and "
    "whether the repayments come out on time. Which one is it, and when?",
)

A_DEBT_NO_FIGURE = (
    "The rate is the figure that decides what to do about a borrowing - it is on the statement or "
    "the agreement - and after that what is left on it. Do you know either?",
    "What to do about borrowing turns on two things: what it costs a year, and how much is left on "
    "it. The rate is usually the one printed on the statement. Which have you got?",
)

A_BORROWING_WORDS = re.compile(
    r"\b(?:store\s*cards?|storecards?|catalogue)\b|\b(?:bnpl|klarna|buy\s+now\s+pay\s+later)\b")


def observe(text, memory):
    return None


def respond(text, memory):
    if not isinstance(text, str):
        return None
    clean = " ".join(text.lower().split())
    if not clean or "?" in clean:
        return None
    if not _A_BORROWING.search(clean):
        return None
    if _A_DEBT_DONE.search(clean):
        return None
    if _A_ASK.match(clean) and not _A_RATE.search(clean):
        return None
    if _A_JOINED.match(clean):
        return None
    if _A_NOT_THIS_DEBT.search(clean):
        return None
    if _A_GREETING_CARD.search(clean):
        return None
    rate = _A_RATE.search(clean)
    if rate:
        percent = rate.group(1)
        try:
            value = float(percent)
        except ValueError:
            return None
        if value >= 8.0:
            return pick(A_DEBT_RATE, memory, clean).format(rate=percent)
        return pick(A_DEBT_CHEAP, memory, clean).format(rate=percent)
    if _A_BALANCE.search(clean):
        if _A_PAYMENT.search(clean):
            return None
        return pick(A_DEBT_BALANCE, memory, clean)
    if _A_DEBT_NAMED.search(clean) and _A_HAVE.search(clean) and not _A_THINKING.search(clean):
        kind = A_BORROWING_WORDS.search(clean)
        if kind and kind.group(0).startswith(("bnpl", "klarna", "buy")):
            return pick(A_DEBT_BNPL, memory, clean)
        if kind:
            return pick(A_DEBT_STORE, memory, clean)
        return pick(A_DEBT_NO_FIGURE, memory, clean)
    return None
