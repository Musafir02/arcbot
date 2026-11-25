import re

from ..understanding import lexicon
from .lookup import entry


CHILD_WORK_WORDS = ("work", "works", "working", "job", "jobs", "employed", "employment",
                    "earn", "earns", "earning", "paid", "pay")

CHILD_WORK_CHILD = ("13 year old", "14 year old", "15 year old", "16 year old",
                    "at 13", "at 14", "at 15", "at 16",
                    "aged 13", "aged 14", "aged 15", "aged 16",
                    "age 13", "age 14", "age 15", "age 16",
                    "13 years", "14 years", "15 years", "16 years",
                    "13", "14", "15", "16",
                    "year old", "years old", "child", "children", "kid", "kids",
                    "teenager", "teenagers", "teenage", "son", "daughter", "school leaving age",
                    "school leaver", "school leavers", "under 16", "under 18", "gcse",
                    "what age", "how old", "old enough", "whats the youngest", "youngest")

CHILD_WORK_ASK = ("how many hours", "hours a week", "how old", "what age", "age", "youngest",
                  "what jobs",
                  "which jobs", "can i", "can my", "can a", "can an", "can you", "should i let",
                  "latest", "how late",
                  "allowed", "legal", "law", "rules", "permit", "minimum wage", "how much",
                  "pay", "get a job", "get one", "start work", "start a job",
                  "wants a job", "wants to work", "wants one", "is asking", "keeps asking")

CHILD_WORK_ABROAD = re.compile(r"\b(?:abroad|overseas|foreign country|another country|"
                               r"in (?:australia|america|the usa|the us|canada|new zealand|"
                               r"spain|france|germany|italy|ireland|dubai|europe|japan|china)|"
                               r"america|australia)\b")

CHILD_WORK_GET = re.compile(r"\b(?:how do i (?:get|find|apply)|where (?:can|do) i (?:find|get|look)|"
                            r"how can i (?:get|find)|job hunt|job hunting|applications?|apply)\b")

CHILD_WORK_PUB = re.compile(r"\b(?:pub|pubs|bar|bars|bar work|behind the bar|barman|barmaid|"
                            r"off licence|off-licence|betting shop|bookmaker)\b")

CHILD_WORK_OLDER = re.compile(r"\b(?:17|18|seventeen|eighteen)\s*(?:year old|years old)\b|"
                              r"\b(?:17|18) year old\b")

CHILD_WORK_HOLIDAY = re.compile(r"\b(?:school holidays?|holidays?|summer|half term|"
                                r"christmas break|easter break)\b")

CHILD_WORK_HOURS_ASK = re.compile(r"\b(?:how many hours|hours|week|weekly|how long|"
                                  r"how late|what time)\b")

CHILD_WORK_TIME_ASK = re.compile(r"\b(?:until|till|til|how late|how early|what time|latest|"
                                 r"finish|finishes|night|nights|evening|evenings)\b")

CHILD_WORK_TOO_YOUNG = re.compile(r"\b(?:6|7|8|9|10|11|12|six|seven|eight|nine|ten|eleven|"
                                  r"twelve)\s*(?:year[- ]old|years old)\b")
CHILD_WORK_JOBS_ASK = re.compile(r"\b(?:what|which)\s+(?:kind of\s+)?(?:jobs?|work)\b|"
                                 r"\bjobs?\s+(?:can|could|are|is|for)\b|"
                                 r"\bwhat\s+can\s+(?:a|my|they|he|she)\s+\w*\s*(?:year old\s+)?do\b")
CHILD_WORK_PAY_ASK = re.compile(r"\b(?:pay|pays|paid|wage|wages|earn|earns|earning|money|"
                                r"how much|minimum wage|rate|rates|salary)\b")
CHILD_WORK_PERMIT_ASK = re.compile(r"\b(?:permit|permission|licen[cs]e|allowed to work|"
                                   r"do they need|do i need|paperwork|register)\b")
CHILD_WORK_AGE_ASK = re.compile(r"\b(?:age|how old|old enough|old do you have to be|"
                                r"too young|youngest|when can|start)\b")

CHILD_WORK_HOURS = (
    "Twelve hours a week is the cap in term time, at 13 and 14 and again at 15 and 16. The rest "
    "of it moves with age: two hours on a school day either way, five hours on a Saturday at 13 "
    "and 14 and eight at 15 and 16, and 25 hours a week in the school holidays at 13 and 14 and "
    "35 at 15 and 16. Nothing before 7am or after 7pm, nothing during school hours, a break after "
    "four hours, and two weeks off a year. Once school has finished at 16 the young-worker limit "
    "of 8 hours a day and 40 a week takes over.")

CHILD_WORK_OLDER_REPLY = (
    "At 17 the school rules stop and the young-worker ones start: no more than 8 hours a day or "
    "40 hours a week while under 18, a 30-minute break after four and a half hours, and no work "
    "between 10pm and 6am unless the job is one of the exceptions, such as a hospital, a bakery or "
    "a hotel. A written risk assessment is required for anyone under 18.")

CHILD_WORK_HOLIDAY_REPLY = (
    "In the school holidays the cap is 25 hours a week at 13 and 14 and 35 at 15 and 16, against "
    "12 hours a week in term time. The 7am to 7pm limit still holds, the two-week break off work "
    "each year still applies, and a 16 year old who has left school comes under the 8-hour day and "
    "40-hour week instead.")

CHILD_WORK_JOBS = (
    "Shops, cafes and restaurants, hairdressing, an office, cleaning, garden or farm work, and a "
    "paper round are what a council normally allows at 13 or 14. Not under 16: a factory, a "
    "building site, a pub or a betting shop, anything with machinery or heavy lifting, or anything "
    "that keeps them standing for hours.")

CHILD_WORK_TIME = (
    "Not before 7am or after 7pm on any day, and never during school hours - 7pm is the latest "
    "finish at any age under 16, Saturday included. On top of that the weekly cap is 12 hours in "
    "term time, with 5 hours on a Saturday at 13 and 14 and 8 at 15 and 16, and 2 hours on a "
    "school day.")

CHILD_WORK_TOO_YOUNG_REPLY = (
    "No part-time work before 13 in most of the UK. A few things are allowed younger - sport, "
    "modelling, acting and a paper round - and those need a licence from the council. From 13 the "
    "usual jobs are a paper round, a shop or a cafe, capped at 12 hours a week in term time and 2 "
    "hours on a school day, with a free work permit from the council.")

CHILD_WORK_AGE = (
    "Thirteen is the youngest that part-time work is allowed in most of the UK, and 14 is when "
    "employers actually take people on. Under 16 the job also needs a free work permit from the "
    "local council, and the hours are capped at 12 a week in term time.")

CHILD_WORK_PAY = (
    "There is no minimum wage under 16, so the rate is whatever is agreed: fix it and the hours "
    "before the first shift, and get the pay day in writing. At 16 and 17 the lower 16-17 rate "
    "applies, and the national insurance number can be applied for three months before the "
    "sixteenth birthday.")

CHILD_WORK_ABROAD_REPLY = (
    "Every country sets its own age and hours, so check that country's government page rather "
    "than the UK's: most set 14 or 15 as the youngest for part-time work, cap the hours in school "
    "weeks, and require the employer to register the job. A working-holiday or student visa has "
    "its own age and hour limits on top.")

CHILD_WORK_PUB_REPLY = (
    "At 16 they can work in a pub, but not behind the bar: taking orders, clearing tables and "
    "washing up are fine, and serving alcohol is only with a meal and where the licence allows it. "
    "Under 16 there is no pub work at all - and the same list rules out a factory, a building site, "
    "a betting shop and anything with machinery.")

CHILD_WORK_PERMIT = (
    "Under 16 the job needs a work permit from the local council: it is free, it names the "
    "employer and the hours, and the employer usually starts it, though a parent can ask the "
    "council's child employment officer directly. Working without one is the employer's problem, "
    "not the child's.")


def _child_work(memory, understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if CHILD_WORK_GET.search(said):
        return None
    if CHILD_WORK_PUB.search(said):
        return CHILD_WORK_PUB_REPLY
    if CHILD_WORK_OLDER.search(said):
        return CHILD_WORK_OLDER_REPLY
    if CHILD_WORK_ABROAD.search(said):
        return CHILD_WORK_ABROAD_REPLY
    if CHILD_WORK_TOO_YOUNG.search(said):
        return CHILD_WORK_TOO_YOUNG_REPLY
    if CHILD_WORK_PERMIT_ASK.search(said):
        return CHILD_WORK_PERMIT
    if CHILD_WORK_JOBS_ASK.search(said):
        return CHILD_WORK_JOBS
    if CHILD_WORK_PAY_ASK.search(said):
        return CHILD_WORK_PAY
    if CHILD_WORK_HOLIDAY.search(said):
        return CHILD_WORK_HOLIDAY_REPLY
    if CHILD_WORK_TIME_ASK.search(said):
        return CHILD_WORK_TIME
    if CHILD_WORK_HOURS_ASK.search(said):
        return CHILD_WORK_HOURS
    return CHILD_WORK_AGE


CHILD_WORK_NOT_AN_AGE = re.compile(r"\b1[3-6]\s?(?:hours?|hrs?|days?|weeks?|months?|minutes?|"
                                   r"mins?|stone|kg|kilos?|kilos|kgs?|lbs?|pounds|miles?|mph|cm|"
                                   r"litres?|liters?|degrees?)\b")


def _a_number_is_an_age(understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    return not CHILD_WORK_NOT_AN_AGE.search(said)


ANSWERS = ("work",)

ENTRIES = [
    entry(
    "a-child-with-a-job",
    (CHILD_WORK_WORDS, CHILD_WORK_CHILD),
    _child_work,
    ask=CHILD_WORK_ASK,
    avoid=("my job", "my work", "i work", "i am a", "i'm a", "career", "careers", "salary",
           "promotion", "boss", "manager", "colleague", "colleagues", "interview", "cv",
           "resign", "quit", "redundant", "redundancy", "sacked", "apprentice",
           "apprenticeship", "visa", "adapter", "adaptor", "plug", "sockets", "charger",
           "volunteer", "volunteering", "workout", "work out", "works for", "how does it work"),
    guard=_a_number_is_an_age,
    bias=2)
]
