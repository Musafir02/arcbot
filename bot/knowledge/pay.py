
from .lookup import entry



_GROSS_WORDS = ("gross", "gross pay", "gross salary", "gross income", "gross wage",
                "gross wages", "gross earnings", "before tax", "pre tax", "pre-tax", "pretax",
                "before deductions", "before its taxed", "before it is taxed")
_QUOTED_PAY_WORDS = ("salary", "salaries", "wage", "wages", "pay", "income", "earnings",
                     "pay packet", "the offer", "the advert", "the job advert", "the money",
                     "20k", "25k", "30k", "35k", "40k", "45k", "50k", "60k", "20,000", "25,000",
                     "30,000", "35,000", "40,000", "50,000")
_NET_WORDS = ("net", "net pay", "net salary", "net income", "net wage", "net wages",
              "net earnings", "net of tax", "net of tax pay", "after tax", "after-tax",
              "after deductions", "take home", "take-home", "takehome", "take home pay",
              "take-home pay", "takehome pay", "what lands in the bank", "in my hand",
              "in my pocket")
_PAY_WORDS = ("pay", "paid", "salary", "salaries", "wage", "wages", "income", "earnings",
              "pay packet", "paypacket", "payslip", "pay slip", "monthly pay", "weekly pay",
              "hourly pay", "my gross", "my net", "the gross", "the net", "a gross", "a net",
              "take home", "take-home", "takehome")
_GROSS_AND_NET_COMPARED = ("difference", "different", "vs", "versus", "or", "between",
                           "compare", "compared", "which is", "same", "higher", "bigger",
                           "more than", "less than")
_GROSS_AND_NET_INCLUDES = ("include", "includes", "included", "quoted", "advertised", "advert",
                           "offer", "offered", "the number on the advert", "the figure")

_GROSS_AND_NET_THREE = (
    "Gross is what you earned before anything is taken, net (or take-home) is what lands in the "
    "bank, and the difference is income tax, National Insurance and any pension you pay in. A pay "
    "figure is always quoted gross unless it says take-home, so a job advertised at £30,000 is "
    "about £2,000 a month in your hand on a standard code, and less if you pay into a pension. "
    "Check the tax code against your HMRC coding notice (1257L is the standard one): a wrong code "
    "is the usual reason a wage comes out short.")
_GROSS_AND_NET_GROSS = (
    "Gross is your pay before anything is taken out of it: the number in the job advert, on the "
    "contract and at the top of the payslip, before income tax, National Insurance and pension. "
    "What actually lands in your bank is net, or take-home, and the gap between them is those "
    "deductions - about a fifth of it on an ordinary wage. So a salary quoted at £30,000 is gross "
    "unless it says take-home.")
_GROSS_AND_NET_NET = (
    "Net, or take-home, is what lands in your bank after income tax, National Insurance and any "
    "pension have come off. Gross is the number before those - the one in the advert and on the "
    "contract - so the two differ by the deductions on the payslip. If the net figure is less than "
    "you expected, check the tax code first: a wrong one is the commonest reason.")
_GROSS_AND_NET_INCLUDES_REPLY = (
    "No: a quoted salary or wage is gross, before tax, unless the advert or the offer says "
    "take-home. So £30,000 a year is about £2,000 a month after income tax and National Insurance "
    "on a standard code, and less if you pay into a pension. Ask for the figure in writing and "
    "check whether a pension is included, because that changes what you actually get.")


def _about_pay(understood):
    text = " %s " % " ".join(str((understood or {}).get("clean")
                                 or (understood or {}).get("text") or "").lower().split())
    says_gross = any(" %s " % word in text for word in _GROSS_WORDS)
    says_net = any(" %s " % word in text for word in _NET_WORDS)
    if any(ch.isdigit() for ch in text) and not any(
            " %s " % word in text for word in ("include", "includes", "included", "include tax",
                                               "includes tax", "tax included", "before or after",
                                               "after or before")):
        return False
    if says_gross and says_net:
        return True
    if says_gross or says_net:
        return any(" %s " % word in text for word in _PAY_WORDS) or any(
            " %s " % word in text for word in ("tax", "taxed"))
    if not any(" %s " % word in text for word in _QUOTED_PAY_WORDS):
        return False
    if not any(" %s " % word in text for word in ("tax", "taxed")):
        return False
    return any(" %s " % word in text for word in ("include", "includes", "included", "taxed",
                                                  "before", "after", "quoted", "advertised"))


def _gross_or_net(memory, understood):
    text = " %s " % " ".join(str((understood or {}).get("clean")
                                 or (understood or {}).get("text") or "").lower().split())
    says_gross = any(" %s " % word in text for word in ("gross", "gross pay", "gross salary",
                                                        "gross income", "before tax", "pre tax",
                                                        "pre-tax", "pretax"))
    says_net = any(" %s " % word in text for word in ("net", "net pay", "net income", "after tax",
                                                      "take home", "take-home", "takehome",
                                                      "take home pay", "net of tax"))
    if says_gross and says_net:
        return _GROSS_AND_NET_THREE
    if (" before or after " in text or " after or before " in text
            or " gross or net " in text or " net or gross " in text):
        return _GROSS_AND_NET_THREE
    if any(" %s " % word in text for word in _GROSS_AND_NET_COMPARED) and says_gross:
        return _GROSS_AND_NET_THREE
    if any(" %s " % word in text for word in _GROSS_AND_NET_INCLUDES):
        return _GROSS_AND_NET_INCLUDES_REPLY
    if says_net:
        return _GROSS_AND_NET_NET
    if says_gross:
        return _GROSS_AND_NET_GROSS
    return _GROSS_AND_NET_THREE


ENTRIES = [
    entry("gross-and-net",
          (_GROSS_WORDS + _NET_WORDS + _QUOTED_PAY_WORDS,
           _PAY_WORDS + ("what is", "whats", "what does", "mean", "means", "meaning",
                         "difference", "different", "vs", "versus", "or", "between",
                         "include", "includes", "included", "quoted", "advertised", "advert",
                         "salary", "offer", "compare", "compared", "explain", "which",
                         "is", "are", "was", "does", "do", "did",
                         "include tax", "includes tax", "tax included", "tax on it")),
          _gross_or_net,
          bias=2,
          guard=_about_pay,
          avoid=("misconduct", "negligence", "grossly", "grossed out", "gross me out",
                 "gross out", "disgusting", "net worth", "net weight", "gross weight",
                 "drained weight", "net zero", "safety net", "fishing", "netball", "net profit",
                 "net margin", "net asset", "turnover", "butterfly net", "tennis net",
                 "keep net", "net curtains", "moss", "internet", "netflix",
                 "income tax", "tax code", "tax return", "tax year", "national insurance",
                 "salary sacrifice", "how much tax", "tax on", "tax bracket", "tax bill",
                 "self assessment", "underpaid", "overpaid", "emergency tax", "average salary",
                 "average wage", "median", "minimum wage", "living wage", "payslip",
                 "a week", "a month", "an hour", "a day", "per week", "per month", "per hour",
                 "what is that a week", "what is that a month")),

    entry("paye-taken-from-pay",
          (("paye", "paye tax", "pay as you earn"),
           ("come out", "comes out", "comes off", "taken off", "taken out", "taken from",
            "taken from my pay", "deducted", "deducted from", "deduction", "deductions",
            "out of my pay", "off my pay", "out of my wages", "off my wages", "from my pay",
            "out of my salary", "off my salary", "on my payslip", "stop", "stops", "stopped",
            "pay paye", "paid paye", "do i pay", "am i paying", "paye taken")),
          "Yes: PAYE is the income tax your employer takes out of your pay before it reaches "
          "you, worked out from your tax code each payday and shown on the payslip, so the "
          "number you are paid is already after it. National Insurance comes off the same way, "
          "and a pension or a student loan is listed as its own line. Compare the code on your "
          "payslip with your HMRC coding notice (1257L is the standard one): a wrong code is the "
          "usual reason PAYE takes too much.",
          avoid=("tax code", "wrong", "too much", "too high", "overpaid", "underpaid", "refund",
                 "rebate", "emergency tax", "tax return", "self assessment", "how much tax",
                 "national insurance", "p60", "p45", "self employed", "cis", "what is paye",
                 "what does paye", "mean", "explain"),
          bias=1),

    entry("student-loan-taken-from-pay",
          (("student loan", "student loans", "student debt", "student loan repayment",
            "student loan repayments"),
           ("come out", "comes out", "comes off", "taken off", "taken out", "deducted",
            "deduction", "deductions", "out of my pay", "off my pay", "out of my wages",
            "off my wages", "from my pay", "out of my salary", "off my salary", "on my payslip",
            "stop", "stops", "stopped", "pay student loan", "paid student loan",
            "do i pay", "am i paying")),
          "Yes: a student loan comes off your pay like tax, through PAYE, once you earn over the "
          "threshold for your plan - on plan 5 that is 9% of what you earn above about £25,000 a "
          "year (£2,082 a month), shown as its own line on the payslip. Only the part above the "
          "threshold counts, so a low month takes nothing, and it stops by itself when the loan "
          "is paid off. If the figure looks wrong, ask payroll for the plan they have you on: "
          "the wrong plan is the usual cause.",
          avoid=("how much", "how much is", "pay off", "pay it back", "pay back",
                 "repay early", "overpay", "overpayment",
                 "worth", "settle", "write off", "written off", "forgiven", "cancel", "plan 1",
                 "plan 2", "plan 4", "threshold", "what is a student loan", "interest rate"),
          bias=1),
]

ANSWERS = ("money",)
