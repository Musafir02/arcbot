import re

from .fallback import (_choose, _grief_thread, _in_a_loss_thread, _in_a_pool, _the_line_before,
                       in_a_safety_thread)

ROLE_WITH_SOMEBODY_ABOVE = (
    r"(?:boss|manager|line\s+manager|team\s+lead|team\s+leader|team\s+manager|supervisor|"
    r"shift\s+lead|foreman|colleague|co-?worker|teacher|head\s?teacher|tutor|lecturer|"
    r"landlord|landlady|letting\s+agent|social\s+worker|social\s+services|housing\s+officer|"
    r"housing\s+association|jobcentre|council|school|nursery|college|university|"
    r"gp\s+surgery|doctors\s+surgery|surgery|practice|hr|payroll|recruiter|agency)")
A_COMPLAINT_WORD = re.compile(
    r"\b(?:never|not|no|wont|won'?t|doesnt|doesn'?t|didnt|didn'?t|ignores?|ignored|forgets?|"
    r"forgot|losing|loses|lost|lies|lying|lied|shouts?|shouted|yell\w*|blames?|blamed|"
    r"criticis\w*|undermin\w*|gaslight\w*|cancel\w*|clos\w*|chang\w*|changes|moves?|moved|"
    r"goalposts|overrules?|shuts? me down|snaps? at me|rolls? (?:his|her|their) eyes|leaves? me out|"
    r"rules|last minute|wrong|unfair|credit|favourites?|piling|pile|micromanag\w*|hiding|"
    r"refuses?|refused|picks on|picked on|talks over|talked over|belittles?|belittled|"
    r"mess(?:ed)? up|muck\w*|stops? me|stopped me|keeps me|kept me|delay\w*|chase\w*|"
    r"impossible|nightmare|stress\w*|awful|horrible|useless|lazy|rude|bully\w*|unprofessional)\b",
    re.I)
KEEPS_DOING_IT = re.compile(
    r"\b(?:keeps?|always|never|constantly|every\s+(?:single\s+)?(?:time|week|day|shift|month|"
    r"term)|again\s+and\s+again|over\s+and\s+over|all\s+the\s+time|ignores?|ignored|"
    r"picks?\s+on\s+me|undermines?\s+me|talks?\s+over\s+me|belittles?\s+me|gaslights?)\b",
    re.I)
A_PERSON_WHO_KEEPS = re.compile(
    r"\b(?:(?:my|our|his|her|their|the)\s+(?:new\s+|old\s+|current\s+|ex\s+)?)?"
    + ROLE_WITH_SOMEBODY_ABOVE + r"\b", re.I)
A_WARM_MEMORY = re.compile(
    r"\b(?:always|used\s+to)\s+(?:said|told|taught|gave|made\s+me|let\s+me|wanted|encouraged)\b"
    r"|\b(?:was|were)\s+(?:great|lovely|kind|good|brilliant|fair|helpful)\b", re.I)
A_BRUSH_OFF = re.compile(
    r"\b(?:says?\s+(?:that\s+)?(?:its|it'?s|thats|that'?s)\s+(?:just\s+)?(?:how|the\s+way)\b"
    r"|says?\s+(?:that\s+)?(?:its|it'?s|thats|that'?s)\s+life\b"
    r"|shrugs?\s+(?:it\s+off|it|and)\b"
    r"|says?\s+(?:to\s+)?(?:just\s+)?(?:get\s+on\s+with\s+it|put\s+up\s+with\s+it)"
    r"|says?\s+(?:everyone|everybody|we\s+all)\b[^.?!]{0,40}?(?:put[s]?\s+up\s+with|has\s+to)"
    r"|keeps?\s+saying\s+(?:we'?ll\s+see|next\s+(?:month|week|year)|soon|in\s+a\s+(?:bit|minute|while))"
    r"|won'?t\s+even\s+(?:say|answer|reply|discuss))\b", re.I)
THE_BRUSH_OFF_REPLIES = (
    "That is a brush-off rather than an answer. Nothing to look up here, but the move that works "
    "is a short email: say what they said, what you want changed, and ask for a reply by a date. "
    "If the date passes, that email is what you take one rung above them, or to ACAS if it is a "
    "workplace.",
    "When the answer is that is just how it is, ask once more in writing - what you want changed "
    "and by when - and keep the reply. That email is what the next rung reads: ACAS for a "
    "workplace, or the complaints procedure every school, council and surgery has to follow.",
    "Nothing to look up here, but do not leave it spoken: put the request in writing with a date "
    "on it and keep a copy. If {role} will not answer that, the next step is one rung above them, "
    "and after that the ombudsman, which is free to use and is where a case finally gets looked "
    "at.",
    "There is a shape to these answers and it is worth naming: ask for the reason in writing, "
    "once, with the date you want it by. A recorded refusal is something you can challenge, and "
    "the complaints procedure is the route - it has to end somewhere, usually with the ombudsman.",
)
PERSON_WHO_KEEPS_REPLIES = (
    "Nothing in that to look up, but the step is the same as for any pattern like this: put it in "
    "writing once - the date, what happened, what you want - and keep a copy. If it does not come "
    "back in a week, it goes one rung above {role}, and ACAS gives free advice on the wording if "
    "it is a workplace.",
    "When it happens again and again the wording decides it: dates, what you asked for, what "
    "happened next. Send that once to {role} and ask for an answer by a date. If it does not come, "
    "ask for the written complaints or grievance procedure and follow the step it names.",
    "Keep a short record - the date, what happened, what you asked for. A record is what makes "
    "{role} have to answer, and it is what the next rung reads. Every school, council and GP "
    "surgery has a complaints procedure with named steps, and asking for a copy is the first one.",
    "That is a pattern rather than one bad day, so put it in writing rather than say it again: "
    "what you want changed, with dates. Nothing to look up here, but the complaints procedure is "
    "where this goes next - ask for a copy of it and follow the step it names.",
)


ROLE_SAID_BACK = {"hr": "HR", "gp surgery": "the surgery", "doctors surgery": "the surgery",
                  "surgery": "the surgery", "school": "the school", "nursery": "the nursery",
                  "council": "the council", "university": "the university",
                  "college": "the college", "jobcentre": "the jobcentre"}


THEIR = {"my": "your", "our": "your", "his": "their", "her": "their", "their": "their"}


def _the_role_said_back(found):
    role = " ".join(str(found or "").split()).lower()
    if role in ROLE_SAID_BACK:
        return ROLE_SAID_BACK[role]
    if role.startswith(("the ", "a ")):
        return role
    first, _, rest = role.partition(" ")
    if first in THEIR and rest:
        return THEIR[first] + " " + rest
    if first in ("your", "their", "the", "a"):
        return role
    return "the " + role


A_BODY_LINE = re.compile(
    r"\b(?:knife|gun|knives|weapon|throat|strangl\w*|chok\w*|punch\w*|beat (?:me|him|her)|"
    r"hit (?:me|him|her|my)|hits? me|hurt(?:ing)? me|hurts? me|threaten\w*|threats?|"
    r"kill me|kill(?:ed)? (?:him|her|them)|bruis\w*|abus\w*|assault\w*|rape\w*|"
    r"black eye|broken (?:arm|nose|ribs?))\b", re.I)


def _a_body_line_above(memory):
    if not isinstance(memory, dict):
        return False
    said = [str(turn.get("user") or "") for turn in (memory.get("turns") or [])
            if isinstance(turn, dict)]
    return any(A_BODY_LINE.search(" ".join(line.lower().split())) for line in said[-2:])


def _a_person_who_keeps(clean, repaired, memory):
    said = " ".join(str(clean or "").split())
    if not said:
        return None
    role = None
    for line in (said, " ".join(str(repaired or "").split())):
        match = A_PERSON_WHO_KEEPS.search(line)
        if not match:
            continue
        after = line[match.end():match.end() + 70]
        brush = A_BRUSH_OFF.search(after)
        if (brush or (KEEPS_DOING_IT.search(after) and A_COMPLAINT_WORD.search(line))) \
                and not A_WARM_MEMORY.search(line):
            role = _the_role_said_back(line[match.start():match.end()])
            pool = THE_BRUSH_OFF_REPLIES if brush else PERSON_WHO_KEEPS_REPLIES
            break
    if not role:
        return None
    if (in_a_safety_thread(memory) or _grief_thread(memory) or _in_a_loss_thread(memory)
            or _a_body_line_above(memory)):
        return None
    says = str(_the_line_before(memory) or "")
    if says and _in_a_pool(says, (PERSON_WHO_KEEPS_REPLIES, THE_BRUSH_OFF_REPLIES)):
        return None
    return _choose([line.format(role=role, Role=role[0].upper() + role[1:])
                    for line in pool], memory, clean)


def reply_for(clean, repaired, memory):
    return _a_person_who_keeps(clean, repaired, memory)
