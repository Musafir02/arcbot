
import re

PRIORITY = -997

A_PERSON_AFTER_THE_NAME = frozenset("""
    brother sister mum mom mam dad father mother son daughter wife husband partner friend mate
    cousin uncle aunt nephew niece boss colleague workmate neighbour neighbor stepson stepdaughter
    flatmate roommate lodger lad girl bloke fella boyfriend girlfriend fiance fiancee
""".split())

NOT_DONE = re.compile(
    r"\b(?:havent|hasnt|hadnt|ha(?:ve|s|d)\s+not|didnt|did\s+not|not\s+(?:yet\s+)?(?:replied|"
    r"heard|fixed|paid|sent|done|come|turned\s+up)|no\s+(?:reply|response|answer|word)\b|"
    r"still\s+(?:waiting|no|nothing)|nothing\s+(?:back|yet|since|at\s+all)|ignoring|ignored|"
    r"wont|won't|refuse[sd]?|too\s+long|weeks\s+now|months\s+now|"
    r"and\s+nothing\b|heard\s+nothing|nothing\s+(?:ever\s+)?came\s+back|"
    r"never\s+(?:did|bothered|rang|replied|came|got\s+back|gave|sent|turned\s+up)|"
    r"never\s+(?:heard|came)\s+back|"
    r"no\s+one\s+(?:(?:has|had)\s+)?(?:got|gotten|come)\s+back|nobody\s+(?:(?:has|had)\s+)?"
    r"(?:got|gotten|come)\s+back|has\s+not\s+come\s+back|have\s+not\s+come\s+back|"
    r"(?:nobody|no\s+one)\s+(?:\w+\s+){0,2}(?:rang|rung|phoned|called|replied|answered|bothered))")

HOW_TO_CHASE = re.compile(
    r"\b(?:chase|chasing|escalate|escalation|ombudsman|complain|complaint|"
    r"follow\s+(?:it\s+)?up|how\s+long\s+(?:should|do|before|until|to\s+wait|till)|"
    r"who\s+(?:do\s+i|should\s+i|can\s+i)\s+(?:ask|ring|call|contact|chase|escalate)|"
    r"what\s+(?:can|do|should)\s+i\s+do\s+(?:about|now)|take\s+(?:it|this)\s+further)\b")

ORGANISATIONS = (
    (("council tax",), "the council tax",
     "the account number on the bill"),
    (("council", "local authority", "town hall"), "the council",
     "the reference on their letter"),
    (("housing association", "housing office", "housing trust"), "the housing association",
     "their repair or complaint reference"),
    (("landlord", "letting agent", "landlady"), "the landlord",
     "the date you reported it and your photos"),
    (("dwp", "jobcentre", "job centre", "universal credit", "benefits office"), "the DWP",
     "the reference on the decision letter"),
    (("hmrc", "tax office", "inland revenue"), "HMRC",
     "your taxpayer reference and the tax year"),
    (("gp", "doctor", "surgery", "health centre", "dentist"), "the surgery",
     "the practice manager's name and the date you first asked"),
    (("hospital", "nhs trust", "clinic"), "the hospital",
     "your appointment or referral reference"),
    (("energy supplier", "electricity", "gas company", "water company", "water board"),
     "the supplier", "your account number and the date of the bill"),
    (("bank", "building society"), "the bank",
     "the complaint reference they gave you"),
    (("employer", "payroll", "hr"), "your employer",
     "your payslip dates and the hours you were short"),
    (("school", "head teacher", "headteacher", "academy trust"), "the school",
     "the date you raised it and their letter"),
    (("university", "college", "student finance"), "the university",
     "your student number and the decision reference"),
    (("dvla", "passport office", "home office", "ukvi"), "the office",
     "the application reference on your receipt"),
    (("parcel", "delivery", "courier", "postage", "the post", "my order", "the order"),
     "the seller", "the order number and the delivery date they gave you"),
)

THE_SHAPE = (
    "Have {reference} in front of you, and put the ask in writing once: what has not happened, "
    "when you first raised it, and the day you want an answer by. {body}'s complaints page names "
    "the timescale and the next stage, usually an ombudsman after eight weeks, and that page is "
    "the part I cannot see.",
    "First get {reference} together, then write once, with what has not happened, "
    "the date you first raised it and the day you need to hear by. {body}'s own complaints page "
    "has the timescale and the escalation route, and what it says for your case is the part I "
    "cannot see.",
    "Start with {reference}, then write once: what has not happened, when you first raised it, and "
    "the day you need to hear by. {body}'s complaints page says how long they take and where it "
    "goes next, and that and your letter are what I cannot see from here.",
)


RAISED = re.compile(
    r"\b(?:complain(?:ed|ing|t)?|letters?|form|emails?|emailed|wrote|written|write|applied|"
    r"application|claim(?:ed|s)?|asked|rang|phoned|called|contacted|chased|reported|"
    r"requested|sent|posted|appealed|emailed\s+them|in\s+touch|heard\s+from\s+them|"
    r"repairs?|refunds?|payments?|booking|appointment|orders?|delivery|deposits?|quote|"
    r"invoices?|reimburs\w*)")

THE_SHAPE_UNNAMED = (
    "Write once with the reference they gave you, what has not happened, the date you first raised "
    "it and the day you need to hear by, and keep a copy. Past that day a complaint goes to an "
    "ombudsman, usually after eight weeks, and their own complaints page has the timescale - the "
    "part I cannot see from here.",
    "The letter only needs the reference, what has not happened, the date you first asked and the "
    "day you want an answer by. That copy is what makes the next step easy: their complaints page "
    "names the timescale and who takes it on after it, and I cannot see that page from here.",
    "Put it in writing once, with the reference, the dates and the day you need to hear by. "
    "Complaints usually go on to an ombudsman after eight weeks if nothing comes back, and the "
    "page that says how long they allow for this case is the one I cannot see.",
)


def _the_shape_unnamed(memory, lowered):
    from ..compose import fallback
    return fallback._choose(THE_SHAPE_UNNAMED, memory, lowered)


IVE_TRIED = re.compile(
    r"\b(?:i(?:ve|\s+have)\s+(?:rung|rang|called|phoned|emailed|written|been\s+in|been\s+down|"
    r"asked|chased|tried)|(?:rung|rang|called|phoned|emailed)\s+(?:them|him|her|the\s+\w+)|"
    r"no\s+one\s+(?:answers|picks\s+up|rings\s+back)|keeps?\s+passing\s+me\s+(?:round|around))")

IVE_TRIED_LEAD = (
    "A call leaves nothing they have to answer, so the step that works now is one line in writing.",
    "Phoning again will get the same answer; what counts is the ask in writing.",
    "That is the point to stop ringing and put it in writing, because a call is not a record.",
)


BARE_CONTINUATION = re.compile(
    r"^(?:so|ok|okay|and|but|right|well)?\s*(?:what\s+now|what\s+next|now\s+what|"
    r"what\s+do\s+i\s+do(?:\s+now)?|where\s+do\s+i\s+start|how\s+do\s+i\s+start)\s*[?.!]*$")

THE_TIMESCALE_ASK = re.compile(
    r"\bhow\s+long\b|\bhow\s+many\s+(?:weeks|days|months|working\s+days)\b|"
    r"\bhow\s+soon\b|\bwhen\s+should\s+i\s+(?:chase|escalate|complain|write)\b|"
    r"\bwait\s+(?:before|until)\b|\bhow\s+much\s+longer\b")

THE_TIMESCALE = (
    "Eight weeks is the usual marker: until then {body} works to its own published timescale, and "
    "after it a complaint can go to the ombudsman. Put the day you need an answer by in the "
    "letter, keep the copy, and the date you wrote down is what makes it their deadline.",
    "Most schemes give {body} eight weeks to answer before a complaint can be escalated to an "
    "ombudsman, and its own page has the shorter figure it works to day to day. Your letter is "
    "what starts the clock, so give a date and keep a copy of it.",
)


THE_NEXT_STEP = (
    "Then it is two short paragraphs: what has not happened, the date you first raised it and the "
    "day you want an answer by, sent to the address on their letter with {reference} in it so "
    "there is a copy. If the date passes or the reply is a no, {body}'s complaints page names the "
    "next stage, which is usually an ombudsman after eight weeks.",
    "Put {reference} at the top, say in two or three lines what has not happened and when you "
    "first asked, and ask for an answer by a named day. Keep the copy: {body}'s own page has the "
    "timescale, and the letter it sends back names who takes it on if they miss it.",
    "Write it once, with {reference}, the date you first raised it and the day you need to hear "
    "by, and keep a copy. {body} publishes how long it should take and where a complaint goes "
    "next after that, and the date you put in the letter is what makes it their deadline.",
)


THE_NEXT_STEP_UNNAMED = (
    "Then write it once: the reference they gave you, what has not happened, the date you first "
    "raised it and the day you need to hear by, and keep a copy of it. Past that day a complaint "
    "usually goes on to an ombudsman after eight weeks, and their own page has the timescale for "
    "your case - the part I cannot see.",
    "One short letter: the reference, what has not happened, the date you first asked and the day "
    "you want an answer by, with a copy kept. Their complaints page says how long they allow and "
    "who takes it on after that, and your copy is what proves the date you gave them.",
)


A_PERSON_THEIRS = (
    r"(?:best\s+|old\s+|oldest\s+|closest\s+|own\s+|little\s+|big\s+|eldest\s+|younger\s+|"
    r"school\s+|uni\s+|work\s+|childhood\s+)*"
    r"(?:friends?|mates?|brothers?|sisters?|mum|mom|mam|mother|dad|father|sons?|daughters?|"
    r"husbands?|wifes?|wives|partners?|boyfriends?|girlfriends?|cousins?|uncle|aunt|nephews?|"
    r"nieces?|flatmates?|housemates?|roommates?|colleagues?|workmates?|neighbours?|neighbors?|"
    r"ex|ex-?(?:wife|husband|partner|boyfriend|girlfriend))")
A_REPLY_VERB = (
    r"(?:text(?:s|ed|ing)?|messag(?:e|es|ed|ing)|call(?:s|ed|ing)?|ring(?:s|ing)?|rang|rung|"
    r"repl(?:y|ies|ied|ying)|answer(?:s|ed|ing)?|respond(?:s|ed|ing)?|pick(?:s|ed|ing)?\s+up|"
    r"ignor(?:e|es|ed|ing)|open(?:s|ed|ing)?|writ(?:e|es|ten|ing)?|wrote|"
    r"(?:be|been)\s+in\s+touch|"
    r"(?:come|came|get|gets|getting|got)\s+back)")
A_NEGATIVE = (
    r"(?:hasnt|havent|hadnt|has\s+not|have\s+not|didnt|did\s+not|doesnt|does\s+not|isnt|"
    r"isn't|is\s+not|wasnt|wasn't|was\s+not|never|wont|won't|refuses?\s+to)")
A_PERSON_OWES_A_REPLY = re.compile(
    r"\b(?:my|our)\s+(?:\w+\s+){0,1}" + A_PERSON_THEIRS +
    r"\b[^.?!]{0,40}?\b" + A_NEGATIVE + r"\s+(?:\w+\s+){0,2}" + A_REPLY_VERB +
    r"\b(?:\s+(?:me|us|back)){0,2}", re.I)
THE_PRONOUN = (r"(?:(?:he|she|they)(?:s|'s|re|'re|ve|'ve)?)")

A_PRONOUN_OWES_A_REPLY = re.compile(
    r"^\W*(?:(?:so|and|but|then|ok|okay|well)\s+)*" + THE_PRONOUN + r"\b[^.?!]{0,30}?\b"
    + r"(?:" + A_NEGATIVE + r"|\bnot)\s+(?:\w+\s+){0,2}" + A_REPLY_VERB +
    r"\b(?:\s+(?:me|us|back)){0,2}", re.I)
A_PRONOUN_DID_THE_SILENT_THING = re.compile(
    r"^\W*(?:(?:so|and|but|then|ok|okay|well)\s+)*" + THE_PRONOUN + r"\b[^.?!]{0,30}?\b"
    r"(?:ignor(?:ed|es)|ghost(?:ed|s)|blank(?:ed|s)\s+me|left\s+me\s+on\s+read|"
    r"gave\s+me\s+the\s+silent\s+treatment)\b", re.I)

ANSWERING_SOMETHING_ELSE = re.compile(
    r"\b(?:the\s+)?(?:door|doorbell|buzzer|intercom|gate)\b", re.I)

A_PERSON_DID_THE_SILENT_THING = re.compile(
    r"\b(?:my|our)\s+(?:\w+\s+){0,1}" + A_PERSON_THEIRS +
    r"\b[^.?!]{0,30}?\b(?:ignor(?:ed|es)|ghost(?:ed|s)|blank(?:ed|s)\s+me|"
    r"left\s+me\s+on\s+read|gave\s+me\s+the\s+silent\s+treatment)\b", re.I)

THE_WAIT_FOR_A_PERSON = (
    "No word back, and the waiting is the worst of it. One plain message - \"no rush, just "
    "checking you're ok\" - beats three follow-ups, and it is easy to answer, which matters more "
    "than saying it perfectly.",
    "A silence like that does the talking on its own, so it is worth one clear message rather than "
    "guessing: say you would like to hear from them and that there is no pressure, then leave the "
    "ball with them. A first nudge reads as care and a third reads as a chase.",
    "Waiting on somebody to answer is its own kind of tired. Send one message that is easy to "
    "answer - no list of complaints, no \"we need to talk\" - and then let a day or two pass "
    "before you read anything into it: people go quiet for reasons that have nothing to do with "
    "you.",
)


def _the_person_before(memory):
    said = [str(turn.get("user") or "") for turn in (memory.get("turns") or [])
            if isinstance(turn, dict)]
    for line in said[-3:]:
        if re.search(r"\b(?:my|our)\s+" + A_PERSON_THEIRS + r"\b", line, re.I):
            return True
    return False


def _the_wait_for_a_person(memory, lowered):
    if A_PERSON_OWES_A_REPLY.search(lowered):
        said = A_PERSON_OWES_A_REPLY.search(lowered)
    elif A_PERSON_DID_THE_SILENT_THING.search(lowered):
        said = A_PERSON_DID_THE_SILENT_THING.search(lowered)
    elif A_PRONOUN_DID_THE_SILENT_THING.search(lowered) and _the_person_before(memory):
        said = A_PRONOUN_DID_THE_SILENT_THING.search(lowered)
    elif A_PRONOUN_OWES_A_REPLY.search(lowered) and _the_person_before(memory):
        said = A_PRONOUN_OWES_A_REPLY.search(lowered)
    else:
        return None
    if ANSWERING_SOMETHING_ELSE.search(lowered):
        return None
    from ..compose import fallback
    return fallback._choose(THE_WAIT_FOR_A_PERSON, memory, lowered)


def _was_an_unnamed_chase(memory, current):
    said = [str(turn.get("user") or "") for turn in (memory.get("turns") or [])
            if isinstance(turn, dict)]
    said = [line for line in said if line.strip() and line.strip().lower() != current]
    if not said:
        return False
    lowered = " ".join(said[-1].lower().split())
    return _the_body(lowered, _words(lowered)) is None and not _names_its_own_person(lowered) \
        and bool(RAISED.search(lowered) and NOT_DONE.search(lowered))


def _words(text):
    return set(re.findall(r"[a-z']+", str(text or "").lower()))


def _the_body(lowered, words):
    if A_PERSON_WHO_WORKS_THERE.search(lowered):
        return None
    for triggers, said, reference in ORGANISATIONS:
        for trigger in triggers:
            if " " in trigger:
                if trigger in lowered:
                    return said, reference
            elif trigger in words:
                owner = _the_person_it_belongs_to(lowered, trigger)
                if owner:
                    continue
                return said, reference
    return None


A_PERSON_WHO_WORKS_THERE = re.compile(
    r"\b(?:my|our)\s+(?:\w+\s+){0,1}" + A_PERSON_THEIRS +
    r"\b[^.?!]{0,25}?\b(?:works?|working|worked|is\s+employed|has\s+a\s+job|got\s+a\s+job|"
    r"does\s+a\s+job)\s+(?:for|at|in|with)\b", re.I)

A_PERSON_NOT_A_BODY = re.compile(
    r"\b(?:brother|sister|mum|mom|mam|dad|father|mother|son|daughter|wife|husband|partner|"
    r"friend|mate|cousin|uncle|aunt|nephew|niece|boss|colleague|neighbour|neighbor|stepson|"
    r"stepdaughter|flatmate|roommate|landlady|lad)\b")


def _names_its_own_person(lowered):
    return bool(A_PERSON_NOT_A_BODY.search(lowered))


def _the_person_it_belongs_to(lowered, trigger):
    found = re.search(r"\b%s\s+(?:(\w+)\s+)?(\w+)" % re.escape(trigger), lowered)
    if not found:
        return None
    for after in found.groups():
        if after and after in A_PERSON_AFTER_THE_NAME:
            return after
    return None


def _the_body_before(memory, current):
    said = [str(turn.get("user") or "") for turn in (memory.get("turns") or [])
            if isinstance(turn, dict)]
    said = [line for line in said if line.strip() and line.strip().lower() != current]
    for line in said[::-1]:
        lowered = " ".join(line.lower().split())
        body = _the_body(lowered, _words(lowered))
        if body is not None:
            return body
    return None


def respond(text, memory):
    lowered = " ".join(str(text or "").lower().split())
    if not lowered:
        return None
    if not isinstance(memory, dict):
        memory = {}
    body = _the_body(lowered, _words(lowered))
    if body is not None:
        if not (NOT_DONE.search(lowered) or HOW_TO_CHASE.search(lowered)):
            return None
        return _the_shape(body, memory, lowered)
    if THE_TIMESCALE_ASK.search(lowered) and not BARE_CONTINUATION.match(lowered):
        before = _the_body_before(memory, lowered)
        if before is not None:
            return _the_timescale(before, memory, lowered)
    if BARE_CONTINUATION.match(lowered):
        before = _the_body_before(memory, lowered)
        if before is not None:
            return _the_next_step(before, memory, lowered)
        if _was_an_unnamed_chase(memory, lowered):
            return _the_next_step_unnamed(memory, lowered)
        return None
    if IVE_TRIED.search(lowered):
        before = _the_body_before(memory, lowered)
        if before is not None:
            from ..compose import fallback
            lead = fallback._choose(IVE_TRIED_LEAD, memory, lowered)
            return "%s %s" % (lead, _the_shape(before, memory, lowered))
    person_wait = _the_wait_for_a_person(memory, lowered)
    if person_wait is not None:
        return person_wait
    if RAISED.search(lowered) and NOT_DONE.search(lowered) and not _names_its_own_person(lowered):
        return _the_shape_unnamed(memory, lowered)
    return None


def _the_timescale(body, memory, lowered):
    the_body, _reference = body
    from ..compose import fallback
    said = fallback._choose(THE_TIMESCALE, memory, lowered).replace("{body}", the_body)
    said = said[0].upper() + said[1:]
    return re.sub(r"(?<=[.!?] )([a-z])", lambda hit: hit.group(1).upper(), said)


def _the_next_step(body, memory, lowered):
    the_body, reference = body
    from ..compose import fallback
    said = fallback._choose(THE_NEXT_STEP, memory, lowered)
    said = said.replace("{reference}", reference).replace("{body}", the_body)
    said = said[0].upper() + said[1:]
    return re.sub(r"(?<=[.!?] )([a-z])", lambda hit: hit.group(1).upper(), said)


def _the_next_step_unnamed(memory, lowered):
    from ..compose import fallback
    said = fallback._choose(THE_NEXT_STEP_UNNAMED, memory, lowered)
    said = said[0].upper() + said[1:]
    return re.sub(r"(?<=[.!?] )([a-z])", lambda hit: hit.group(1).upper(), said)


def _the_shape(body, memory, lowered):
    the_body, reference = body
    from ..compose import fallback
    shape = fallback._choose(THE_SHAPE, memory, lowered)
    said = shape.replace("{reference}", reference).replace("{body}", the_body)
    said = said[0].upper() + said[1:]
    said = re.sub(r"(?<=[.!?] )([a-z])", lambda hit: hit.group(1).upper(), said)
    return said
