import re

from . import pick

A_COURT_THING = re.compile(
    r"\bcourt\b|\bsummons\b|\btribunal\b|\bhearing\s+(?:date|on|for)\b|"
    r"\bmagistrates?\b|\bsmall\s+claims\b|\bbailiffs?\b|\bsolicitors?\s+letter\b")
A_GAME_COURT = re.compile(
    r"\b(?:tennis|squash|badminton|basketball|netball|volleyball|football|padel|pickleball|"
    r"handball|five-a-side|bowls)\s+courts?\b|\b(?:food|courtyard|shopping|outlet)\s+courts?\b")
A_LOCAL_RULE = re.compile(
    r"\b(?:council|local\s+authority|parking|pavement|kerb|driveway|bins?|bin\s+day|"
    r"fly\s*tipping|noise\s+nuisance|planning\s+permission|permission\s+for|shed|fence|"
    r"conservatory|loft|extension|licen[cs]e|permit|bus\s+lane|allotment|dog\s+warden|hedge|"
    r"garden|chickens?|hens?|"
    r"bees?|hive|bonfire|barbeque|barbecue)\b")
LAW_ASKED = re.compile(
    r"\b(?:is|isnt|is\s+not|was|wasnt)\s+(?:it|that|this)\s+(?:actually\s+|really\s+|even\s+)?"
    r"(?:legal|illegal|lawful|unlawful|against\s+the\s+law|allowed|a\s+crime)\b"
    r"|\bam\s+i\s+(?:legally\s+)?allowed\s+to\b"
    r"|\bdo\s+i\s+have\s+to\s+(?:by\s+law|legally)\b"
    r"|\bcan\s+(?:i|they|he|she|you|we)\s+be\s+fined\b"
    r"|\bwill\s+(?:i|they|he|she|we)\s+get\s+(?:done|fined|prosecuted|points|a\s+fine)\b"
    r"|\bwhats?\s+the\s+law\s+(?:on|about|say)\b"
    r"|\bdoes\s+the\s+law\s+say\b"
    r"|\bwhat\s+does\s+the\s+law\s+say\b"
    r"|\bis\s+there\s+a\s+law\s+(?:against|on|about)\b")
NOT_A_RULE_ASK = re.compile(
    r"\b(?:tablets?|pills?|painkillers?|paracetamol|ibuprofen|antibiotics?|insulin|medicines?|"
    r"dose|dosage|prescription|symptoms?|bleeding|pregnant|pregnancy|baby|babies|child|kids?|"
    r"sick|ill|hurt|pain|doctor|gp|nurse|hospital)\b")
A_FOLLOW_UP = re.compile(
    r"\b(?:will|would|can|could|do|does|did)\s+(?:they|it|he|she|the\s+council|the\s+court)\b"
    r"|\bwhat\s+(?:happens|happened|now|next)\b|\bhow\s+long\b|\bwhat\s+do\s+i\s+do\b"
    r"|\bam\s+i\s+(?:in\s+trouble|stuck|liable)\b")

UNKNOWN_THE_LAW = (
    "There is an answer in law to that, and it turns on the exact situation rather than the "
    "general idea - which is the part I would get wrong. gov.uk has the wording in plain English, "
    "and Citizens Advice will read it against your own case for free.",
    "The general rule is written down, but where it lands depends on your side of it, and that is "
    "exactly the bit I would only be guessing at. gov.uk has the wording, and Citizens Advice is "
    "free and will apply it to your situation.",
    "I can tell you where this one is kept rather than what it says: law like this is published in "
    "full, and a summary from me could be wrong on a detail that matters. It is on gov.uk in plain "
    "words, and Citizens Advice will answer the same question about your own case free of charge.",
)
UNKNOWN_A_LOCAL_RULE = (
    "Rules like this are set by your council rather than nationally, so two roads can answer "
    "differently - which is why I would only be guessing at yours. Their own site has the exact "
    "wording and any charge, and their phone line settles it in a minute.",
    "This one is your council's to set and enforce, and it changes from place to place. Their "
    "site has it in writing, and Citizens Advice is free if the page is a maze, which it often is.",
    "The council writes this one, so theirs is the only wording that counts - and it varies by "
    "street, so a general answer would be no use to you. It is on their site with the details; "
    "ringing them is quicker than reading, and the number is on the page.",
)
UNKNOWN_A_COURT_THING = (
    "The letter is the thing that matters here: it names the date and the office that can answer "
    "for it, and that office is quicker than the paperwork looks. Ring it with the reference to "
    "hand, sooner rather than later - and Citizens Advice will read the letter with you first, free.",
    "Whoever sent it knows what happens next and by when, and nothing I say changes a date that is "
    "already set. Ring the office named on the letter with the reference to hand; Citizens Advice "
    "will go through the wording with you first at no cost.",
    "A court's next step is on the paperwork rather than in a general answer, and the office that "
    "sent it can tell you where you stand. The reference on the letter is what gets you through - "
    "and Citizens Advice will read it with you for free if the wording is unclear.",
)


def _said(text):
    return " ".join(str(text or "").lower().split())


def _a_court_of_law(said):
    if not A_COURT_THING.search(said or ""):
        return False
    return not (A_GAME_COURT.search(said or "") and not LAW_ASKED.search(said or ""))


def _the_thread_said(memory, pattern, look_back=2):
    turns = [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)]
    return any(pattern.search(_said(turn.get("user"))) for turn in turns[-look_back:])


def _a_court_of_law_in_the_thread(memory, look_back=2):
    turns = [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)]
    return any(_a_court_of_law(_said(turn.get("user"))) for turn in turns[-look_back:])


PERMISSION_ASKED = re.compile(
    r"\b(?:can|could|may)\s+(?:i|we|you|they|he|she)\b"
    r"|\b(?:do|does|did)\s+(?:i|we|you|they|he|she)\s+(?:need|have\s+to|require|apply)\b"
    r"|\b(?:i|we|they|he|she)\s+(?:need|needs|have\s+to|has\s+to|required|requires)\b"
    r"|\bam\s+i\s+(?:allowed|supposed)\b"
    r"|\bis\s+it\s+(?:allowed|legal|illegal|against\s+the\s+law)\b"
    r"|\bwhat\s+(?:are|is)\s+the\s+rules?\b"
    r"|\b(?:rules?|regulations?|bylaws?|by-laws?|permission|permit|licen[cs]e)\b")
WHO_OWNS_IT = re.compile(
    r"\b(?:council|local\s+authority|town\s+hall|court|tribunal|planning|enforcement|"
    r"warden|inspector|officer)\b")
A_PENALTY = re.compile(
    r"\b(?:fines?|fined|penalt(?:y|ies)|prosecut\w*|summons|points|asbos?|"
    r"notice|tribunal|evict\w*|bailiffs?)\b")


def _said_a_local_rule_recently(memory, look_back=2):
    turns = [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)]
    return any(A_LOCAL_RULE.search(_said(turn.get("user"))) for turn in turns[-look_back:])


def _a_rule_ask_in_the_thread(memory, look_back=2):
    turns = [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)]
    for turn in turns[-look_back:]:
        earlier = _said(turn.get("user"))
        if not earlier or NOT_A_RULE_ASK.search(earlier):
            continue
        if LAW_ASKED.search(earlier) or WHO_OWNS_IT.search(earlier):
            return True
        if A_LOCAL_RULE.search(earlier) and PERMISSION_ASKED.search(earlier):
            return True
    return False


def pool_for(text, memory=None):
    said = _said(text)
    if not said or NOT_A_RULE_ASK.search(said):
        return None
    if _a_court_of_law(said) or _a_court_of_law_in_the_thread(memory):
        return UNKNOWN_A_COURT_THING
    if LAW_ASKED.search(said):
        if A_LOCAL_RULE.search(said):
            return UNKNOWN_A_LOCAL_RULE
        return UNKNOWN_THE_LAW
    if A_FOLLOW_UP.search(said) and _said_a_local_rule_recently(memory):
        if A_PENALTY.search(said) or _a_rule_ask_in_the_thread(memory):
            return UNKNOWN_A_LOCAL_RULE
    return None


def answer_for(text, memory=None):
    said = _said(text)
    pool = pool_for(said, memory)
    if not pool:
        return None
    return pick(pool, memory if isinstance(memory, dict) else {}, said)
