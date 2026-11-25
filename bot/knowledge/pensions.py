import re

from .lookup import a_thing_has_stopped, entry

ANSWERS = ("money",)


def _state_pension(memory, understood):
    text = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    record = ("Your record is on gov.uk under \"check your National Insurance record\": it lists "
              "each year and whether it counts, and gaps can often be filled by paying voluntary "
              "contributions.")
    asks_record = bool(re.search(r"\brecord\b|\bcheck\b.*\b(?:national insurance|\bni\b)", text))
    when = ("The state pension starts at 66 now, and at 67 for anyone reaching that age from 2028, "
            "with 68 to come later, so check your own date on gov.uk. It is not automatic: a letter "
            "should come about two months before, and if it does not, claim it on gov.uk or by "
            "phone.")
    years = ("The full new state pension is about £230 a week, £11,500 a year, in 2025-26, on 35 "
             "qualifying years of National Insurance; each year short pays about a thirtieth less, "
             "and you need at least 10 years to get anything at all.")
    counted = re.search(r"\b\d+\s*years?\b|\bhow many years\b|"
                        r"\byears? of (?:national insurance|ni)\b|\bqualifying\b", text)
    asks_when = re.search(r"\bwhen\b|how old|what age|\bdate\b|\bretir(?:e|ing|ement)\b", text)
    asks_amount = re.search(r"\bhow much\b|\bamount\b|\bper week\b|\ba week\b", text)
    if asks_record and not asks_when:
        reply = record + " " + years + " " + when
    elif (asks_amount or counted) and not asks_when:
        reply = years + " " + when
    else:
        reply = when + " " + years
    if re.search(r"\bretir(?:e|ing|ement)\b|\bstop(?:ping)?\s+work", text):
        reply += (" Stopping work and claiming it are two different things, so retiring early is a "
                  "question about your own money rather than about the pension.")
    return reply


ENTRIES = [
    entry("state-pension",
          (("state pension", "pension age", "retirement age", "national insurance record",
            "national insurance years", "ni years", "ni record", "pension forecast",
            "qualifying years", "my state pension", "stop work", "stopping work",
            "years of national insurance", "national insurance contributions",
            "ni contributions", "years of ni", "national insurance so far",
            "until i retire", "until i can retire", "until retirement",
            "how long until i retire", "years until i retire",
            "stop working", "stopping working"),
           ("when", "how old", "what age", "how much", "how long", "how many years",
            "do i get", "qualify", "check",
            "forecast", "how many", "get", "am i", "will i", "can i", "should i", "want",
            "what happens", "what")),
          _state_pension,
          avoid=("workplace", "opt out", "opting out", "contribution", "contribute",
                 "contributing", "pay in", "put in", "paying in", "auto enrolment",
                 "auto-enrolment", "scheme", "should i pay", "join", "put it in", "or save",
                 "save it", "pension or", "put away", "invest", "worth", "debt", "pay off",
                 "pay it off", "save or", "overdraft", "loan", "tax free", "tax-free",
                 "lump sum", "25%", "take my pension", "take it early", "take my pot", "pot",
                 "draw down", "drawdown", "private pension", "personal pension", "sipp",
                 "how can i retire", "how do i retire", "how can i retire early",
                 "retire early", "retiring early"),
          guard=lambda understood: not a_thing_has_stopped(understood)),
]
