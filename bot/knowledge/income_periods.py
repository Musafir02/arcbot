import re

from .lookup import entry
from .money import _MONEY, _clause_about, _income_tax_and_ni, _per_month, _salary_in


def _living_not_a_bill(text):
    for name in ("cost of living", "costs of living", "living costs", "living cost"):
        text = text.replace(name, "living")
    return text


ANSWERS = ("money",)

_LIVING = ("enough to live on", "enough to live", "enough to get by", "enough to survive",
           "to live on my own", "to live alone", "to live in london", "to live on your own",
           "enough money to live", "money to live on", "cost of living", "living costs",
           "afford to live", "live on", "live off", "survive on", "get by on",
           "need to live", "left to live on")
_COPING = ("enough", "get by", "manage", "survive", "cope", "cover", "afford",
           "live off", "stretch to", "left over")
_ENOUGH_TO_LIVE = _LIVING + _COPING
_A_MONTH_OF_IT = ("a month", "per month", "each month", "monthly", "a week", "per week",
                  "each week", "weekly", "a year", "per year", "each year", "yearly", "annual",
                  "salary", "wage", "wages", "income", "take home",
                  "on my own", "on your own", "by myself", "by yourself", "living alone",
                  "live alone")
_ASKS_WHAT_IS_NEEDED = ("how much does a single person need", "how much does someone need",
                        "how much do i need", "how much money do i need",
                        "how much money does it take", "what do i need to live",
                        "how much does it cost")
_A_SUM_A_MONTH = _A_MONTH_OF_IT + _ASKS_WHAT_IS_NEEDED
_EARN_ENOUGH = ("need to earn", "earn to live", "earn enough", "salary do i need",
                "salary would i need", "wage do i need", "how much do i need to earn",
                "what do i need to earn")
_LONDON = re.compile(r"\blondon\b|zone [12]|inner city", re.I)


def _the_gross_for(net_a_month):
    gross = int(net_a_month * 12)
    for _ in range(40):
        tax, ni = _income_tax_and_ni(gross)
        if (gross - tax - ni) / 12.0 >= net_a_month:
            return int(-(-gross // 100) * 100)
        gross += 100
    return gross


def _a_months_costs(london):
    if london:
        return ("In London the same month is roughly £2,000, nearly all of it rent: a one-bed is "
                "£1,300 to £1,900 there before the bills.")
    return ("Outside London one adult needs roughly £1,200 a month: rent £600 to £900, council tax "
            "about £180, energy about £145, food £150 to £200, and about £100 for broadband, phone "
            "and travel.")


_A_FIGURE = re.compile(_MONEY, re.I)


def _a_month_of_life(understood):
    reading = understood if isinstance(understood, dict) else {}
    text = " " + str(reading.get("clean") or reading.get("text") or "").lower() + " "
    if _A_FIGURE.search(text):
        if any(phrase in text for phrase in _LIVING):
            return True
        topic = str(reading.get("topic") or "")
        return any(word in text for word in _COPING) and topic in ("", "money")
    if any(ask in text for ask in _ASKS_WHAT_IS_NEEDED) or _earn_asked(text):
        return any(phrase in text for phrase in _LIVING) or \
            any(word in text for word in _COPING)
    return False


def _earn_asked(text):
    return any(phrase in text for phrase in _EARN_ENOUGH) or bool(
        re.search(r"\b(salary|wage)\b.{0,20}\b(need|needed|require[sd]?)\b", text))


def _enough_to_live_on(memory, understood):
    reading = understood or {}
    text = " " + str(reading.get("clean") or reading.get("text") or "").lower() + " "
    london = bool(_LONDON.search(text))
    monthly, lead = 0, ""
    if re.search(r"a year|per year|each year|yearly|annual", text):
        salary = _salary_in(text)
        if salary and salary >= 5000:
            tax, ni = _income_tax_and_ni(salary)
            monthly = int(round((salary - tax - ni) / 12.0))
            lead = ("On £{:,} a year you take home about £{:,} a month. "
                    .format(salary, monthly))
    if not monthly:
        monthly = _per_month(_living_not_a_bill(text))
    tight, enough = (1750, 2100) if london else (1050, 1300)
    where = "in London" if london else "outside London"
    if _earn_asked(text):
        return ("You need roughly £%s a year before tax to live on your own %s - about £%s a "
                "month after tax. " % (format(_the_gross_for(enough), ","), where,
                                       format(enough, ","))
                + _a_months_costs(london) + " Both move, so check this year's band and the "
                "price cap.")
    if not monthly:
        return (_a_months_costs(london) + " Tell me the figure you have in mind and I will say "
                "whether it covers the month.")
    if monthly >= enough:
        verdict = ("£%s a month is enough %s, with room to save."
                   % (format(monthly, ","), where))
    elif monthly >= tight:
        verdict = ("£%s a month is enough %s only with a cheap rent - there is little left at the "
                   "end of the month." % (format(monthly, ","), where))
    else:
        verdict = ("£%s a month leaves you about £%s short of what one adult needs %s."
                   % (format(monthly, ","), format(enough - monthly, ","), where))
    return (lead + verdict + " " + _a_months_costs(london)
            + " Both move, so check this year's band and the price cap.")


ENTRIES = []


ENTRIES.append(entry(
    "enough-to-live-on",
    (_ENOUGH_TO_LIVE, _A_SUM_A_MONTH),
    _enough_to_live_on,
    bias=2,
    guard=_a_month_of_life,
    avoid=("deposit", "saved", "savings goal", "mortgage", "buy a flat", "buy a house",
           "for food", "on food", "food shop", "for petrol", "on petrol", "universal credit",
           "benefit", "benefits", "carer", "carers", "pension", "abroad", "dog", "dogs", "cat",
           "cats", "pet", "pets", "plants", "my partner", "my husband", "my wife", "my son",
           "my daughter", "family of", "two of us", "kids", "children",
           "rent", "deposit", "council tax", "energy bill", "gas bill", "electric bill"),
    ask=("enough", "much", "how do i", "can i", "could i", "will i", "do i", "is it", "would i",
         "need", "get by", "afford", "only", "just", "survive", "manage", "cover")))

_A_PERIOD_IN_A_SUM = re.compile(
    _MONEY + r"\s*(?:a|an|per|each|every|/)\s*"
    r"(week|weekly|fortnight|fortnightly|month|monthly|year|yearly|annually|annual)", re.I)
_PERIODS_IN_A_YEAR = {"week": 52.0, "weekly": 52.0, "fortnight": 26.0, "fortnightly": 26.0,
              "month": 12.0, "monthly": 12.0, "year": 1.0, "yearly": 1.0,
              "annual": 1.0, "annually": 1.0}
_ANOTHER_PERIOD = re.compile(
    r"\b(?:a|an|per|each|every|over|in|for|of|the)\s*"
    r"(week|fortnight|month|year)\b|\b(yearly|annually|annual|monthly|weekly)\b", re.I)
_EVERYDAY_PERIOD = {"yearly": "year", "annually": "year", "annual": "year",
                    "monthly": "month", "weekly": "week"}
_SAID_AGAIN = {"year": "a year", "month": "a month", "week": "a week",
               "fortnight": "a fortnight"}


def _per_period(text):
    match = _A_PERIOD_IN_A_SUM.search(text)
    if not match:
        return None
    amount = float(match.group(1).replace(",", ""))
    if match.group(2):
        amount *= 1000
    own = match.group(3).lower()
    own = _EVERYDAY_PERIOD.get(own, own)
    for other in _ANOTHER_PERIOD.finditer(text):
        if other.start() < match.end() and other.end() > match.start():
            continue
        wanted = (other.group(1) or other.group(2) or "").lower()
        wanted = _EVERYDAY_PERIOD.get(wanted, wanted)
        if wanted in ("week", "fortnight", "month", "year") and wanted != own:
            return amount, own, wanted
    return None


_ASKS_FOR_THE_FIGURE = ("how much", "how many", "whats", "what's", "what is", "what does",
                        "what would", "what will", "comes to", "come to", "convert", "worth",
                        "equivalent", "in a year", "in a month", "in a week", "over a year",
                        "over a month", "a year in total", "a year altogether")


def _two_periods_named(understood):
    text = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    return bool(_per_period(text))


def _a_sum_in_another_period(memory, understood):
    reading = understood or {}
    text = str(reading.get("clean") or reading.get("text") or "").lower()
    if any(word in text for word in ("keep", "records", "receipts", "payslips", "statements",
                                     "tax return", "how long", "how many years")):
        return None
    found = _per_period(text)
    if not found:
        return None
    if not any(ask in text for ask in _ASKS_FOR_THE_FIGURE):
        return None
    amount, own, wanted = found
    annual = amount * _PERIODS_IN_A_YEAR[own]
    value = annual / _PERIODS_IN_A_YEAR[wanted]
    said = "£{:,} {} is £{:,} {}.".format(
        int(round(amount)), _SAID_AGAIN[own], int(round(value)), _SAID_AGAIN[wanted])
    clause = _clause_about(text, 0, len(text))
    if any(word in clause for word in ("earn", "earns", "salary", "wage", "wages", "paid",
                                       "pay", "job")):
        tax, ni = _income_tax_and_ni(int(round(annual)))
        left = annual - tax - ni
        said += (" After tax and National Insurance that is about £{:,} a month, or £{:,} a "
                 "year.".format(int(round(left / 12)), int(round(left))))
    return said


ENTRIES.append(entry(
    "a-sum-in-another-period",
    (("a month", "a week", "a fortnight", "a month", "per month", "monthly", "each month",
      "weekly", "every week", "each week", "a month"),
     ("a year", "yearly", "a yr", "per year", "annually", "annual", "over a year", "in a year",
      "a month", "monthly", "per month", "a week", "weekly", "per week")),
    _a_sum_in_another_period,
    guard=_two_periods_named,
    avoid=("spare", "save", "saving", "savings", "put by", "put aside", "put away", "set aside",
           "rent", "landlord", "deposit", "mortgage", "afford", "budget", "cheapest",
           "how long", "records", "receipts",
           "after tax", "take home", "take-home", "net pay", "tax"),
    bias=2))
