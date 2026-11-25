import re

from ..memory import holds as earlier

A_WAIT_ASK = re.compile(
    r"\b(?:when|whenabouts|how\s+long|how\s+soon|what\s+day|by\s+when)\b[^?.!]{0,30}?"
    r"\b(?:get(?:s|ting)?\s+here|arriv\w*|turn(?:s|ing)?\s+up|show(?:s|ing)?\s+up|"
    r"come(?:s|ing)?(?:\s+round)?|be\s+(?:here|done|ready|fixed|back|sorted|delivered|"
    r"repaired|installed|finished|in\s+stock|on\s+sale)|have\s+\w+|hear(?:d)?(?:\s+back)?|"
    r"let\s+(?:me|us)\s+know|get\s+back\s+to\s+(?:me|us)|tell\s+(?:me|us)|"
    r"waiting?)\b"
    r"|\bwill\s+(?:it|that|this|they)\s+(?:still\s+)?(?:have\s+\w+|"
    r"be\s+(?:fixed|done|ready|back|delivered|here|sorted|repaired|finished|installed|"
    r"on\s+sale|in\s+stock|available|open)|come|arrive|turn\s+up|show\s+up|get\s+here)\b"
    r"[^?.!]{0,30}?\b(?:by|before|in\s+time|next|this\s+(?:week|month|weekend)|then|friday|"
    r"monday|tuesday|wednesday|thursday|saturday|sunday|tomorrow|the\s+weekend)\b"
    r"|\bwill\s+(?:they|it)\s+still\s+have\s+(?:it|them|any|one)\b"
    r"|\bis\s+it\s+worth\s+waiting\b"
    r"|\b(?:is|has)\s+there\s+(?:a|any)\s+(?:date|day|delivery\s+date|deadline)\b"
    r"|\bany\s+(?:date|word\s+(?:yet|on\s+when)|news\s+(?:yet|on\s+when))\b"
    r"|\b(?:any|no)\s+idea\s+(?:of\s+)?(?:when|how\s+long|what\s+day)\b"
    r"|\bdate\s+(?:yet|in\s+sight|at\s+all)\b"
    r"|\bshould\s+(?:i|we)\s+wait\b")
A_WAIT_LENGTH = re.compile(r"\b(?:wait|hold off|hold on)\b|\bfor\s+(?:the\s+)?(?:sales?|payday|"
                           r"christmas|black\s+friday|january|next\s+(?:week|month))\b")

ORDER_WORDS = re.compile(
    r"\b(?:ordered|order|ordering|parcel|package|delivery|deliver|delivered|dispatch|"
    r"dispatched|courier|tracking|arriving|on\s+its\s+way|coming\s+(?:on|by|next|tomorrow)|"
    r"bought|purchased|refund|returns?|sent\s+(?:it\s+)?back)\b")
REPAIR_WORDS = re.compile(
    r"\b(?:broken|broke|not\s+working|stopped\s+working|repair|repairing|fixed|fixing|"
    r"engineer|technician|repairman|plumber|electrician|boiler|fuse|spare\s+part|part\s+order|"
    r"quote|callout|call\s+out|warranty|leak\w*|drip\w*|flood\w*|fault\w*|cracked|"
    r"smashed|packed\s+up|on\s+the\s+blink|won'?t\s+(?:start|work|drain|spin|heat|turn\s+on)|"
    r"stopped\s+(?:working|turning|spinning|heating))\b")
BOOKING_WORDS = re.compile(
    r"\b(?:booked|booking|appointment|mot|service\s+slot|viewing|quote\s+visit|haircut|"
    r"reservation|table\s+booked|van\s+hire|court|lesson)\b")
REPLY_WORDS = re.compile(
    r"\b(?:cv|application|applied|applying|interview|recruiter|agency|hiring|hear\s+back|"
    r"heard\s+back|reply|replied|emailed|phoned|rang|rang\s+them|left\s+a\s+message|"
    r"waiting\s+to\s+hear|offer\s+letter|references?|landlord|letting|estate\s+agent|"
    r"boss|manager|council|DWP|benefits?)\b")
OFFER_WORDS = re.compile(
    r"\b(?:sale|sales|discount|reduced|offer|deal|in\s+stock|out\s+of\s+stock|cheaper|"
    r"price|prices|bargain|coat|jacket|sofa|tv|laptop|phone|bike|pram|furniture|present|"
    r"gift|looking\s+at|thinking\s+of\s+buying|want\s+to\s+buy|going\s+to\s+buy)\b")

NOT_OURS = re.compile(
    r"\b(?:hospital|doctor|gp|nurse|surgery|clinic|a&e|ambulance|diagnos\w*|cancer|tumour|"
    r"tumor|chemo|operation|surgery|infection|pregnan\w*|baby|babies|miscarriage|funeral|"
    r"died|dead|death|dying|grief|bereave\w*|vet|vets|the\s+dog|the\s+cat|my\s+dog|my\s+cat)\b")

THE_ASK = ("how long do i have to wait", "how long will it be", "how long does it take",
           "will it be ready by then", "when will it be done")

NOTHING_HELD = (
    "A date like that is nearly always written down somewhere - a confirmation, an order page, a "
    "letter, an email - and that is where to look first: it carries a reference, the date they "
    "gave you, and what they promised. Then one short chase, quoting the reference and asking for "
    "a day rather than \"soon\", is what moves it. What is it you are waiting to hear about?",
    "Whichever date it is, three things settle it: find the paper or page with the reference on "
    "it, read what it actually promises, and ask the one who gave it to you for a day in writing. "
    "A date in writing is what you can hold them to if it slips. Tell me which wait this is and I "
    "will take it apart with you.",
)

WAITING_FOR_AN_ORDER = (
    "When it lands is the shop's to say, mine to help you plan around. The date they gave you is "
    "on the confirmation email or the order page, and it moves when they dispatch it; the quickest "
    "settling of it is a message to them with the order number, asking whether the date still "
    "holds and what happens if it slips.",
    "Delivery dates are the shop's, not mine - and they are usually on the confirmation email, "
    "which also carries a tracking link once it ships. Ring or message them with the order number "
    "and ask them to confirm the day in writing; that gives you something to point at if it moves.",
    "The shop holds that date, and the tracking link is the closest thing to it you have: it "
    "usually says what is happening today and when they expect to deliver. Ask them with the "
    "order number for a day rather than a window - a day you can plan a morning around.",
)

WAITING_FOR_A_REPAIR = (
    "Whether it is done by then is the repairer's call, not mine - what you can pin down is the "
    "part that decides it: whether they have the part, and whether they can give you a slot "
    "rather than a day. Ring them with the job reference and ask for both, and ask what happens "
    "to the price if the part is late.",
    "That date belongs to whoever is doing the work, and what decides it is usually a part or a "
    "second visit. Ask them straight: is the part in, is the job booked in, and what would make "
    "it slip - then you know whether to plan around it or chase it.",
    "Nobody can promise you the day from here, and a repairer can: they know the part and the "
    "diary. Ask them for the date in writing and what happens if the part is late, and keep the "
    "quote handy - a repair that slips is the moment a quote gets re-quoted.",
)

WAITING_FOR_A_REPLY = (
    "When they come back to you is theirs to decide, and what you can do is make it easy to say "
    "yes: one short chase, naming the date you applied and asking when they expect to decide. If "
    "there is a date in their own advert or letter, that is the one to hold them to.",
    "Nobody can promise you their answer, and the polite version of chasing is the thing that "
    "moves it: ring or email once, say what you sent and when, and ask for a date rather than an "
    "answer. A week to ten days is the usual ask; after that a second note is reasonable.",
    "That one is theirs to give, not mine - and it is worth asking them what their timeline is "
    "rather than whether they have decided. One chase, with the date you applied and the "
    "reference, is enough; if a decision date was written down anywhere, that is what to quote.",
)

WAITING_FOR_A_BOOKING = (
    "The place holds that date, and their own booking is the record of it: the time on the "
    "confirmation text or email is what they will go by. Ring them with the booking name and ask "
    "how long the slot really takes - the appointment time is usually the start of it, not the "
    "whole of it.",
    "How long it takes is theirs to say, and it varies with what they find on the day. The "
    "confirmation will have the start time; ring and ask how long to allow and whether you should "
    "bring anything, and you will not be guessing on the morning.",
)

WAITING_FOR_AN_OFFER = (
    "Whether it is still on offer next week is the shop's call - nobody outside it knows when a "
    "sale ends, and the date is usually on the page under the price or the small print. If it is "
    "a thing you want, ask them before the day: a shop can often hold a price for a day or tell "
    "you the day it ends.",
    "Sale dates are the shop's, and the page usually says when it finishes - look under the price "
    "for an end date, and ring the branch if it does not. Nobody can promise stock either: a "
    "popular size goes before the sale ends, so the thing worth asking is whether they will hold "
    "one, not whether the discount lasts.",
    "That one is the shop's to answer: the price page normally carries the end date, and a phone "
    "call to the branch settles the rest - whether it is in stock in your size and whether they "
    "will put one by. A discount you cannot get in your size is no discount at all.",
)

WAITING_A_DECISION = (
    "Waiting is a real choice here, and the trade is easy to say: sales come round on set dates "
    "and prices do drop, but the thing you want can go out of stock first, and a wait on something "
    "you need now costs more than the discount saves. The shop's page carries the date a sale "
    "ends; what only you can answer is how much the wait is worth to you.",
    "That is your call, and the parts of it are knowable: when sales usually land, whether the "
    "thing is likely to be in stock at the end of one, and what it costs you to go without in the "
    "meantime. If it is something you need this week, the wait has already lost; if it is a treat, "
    "a month is cheap. The shop's own page will tell you the date, and I can help you weigh it.",
)


def asks_for_a_date(clean, repaired=None):
    for line in (clean, repaired):
        if line and A_WAIT_ASK.search(line):
            return True
    return False


def _the_thread(clean, memory):
    said = [str(clean or "")]
    said.extend(earlier.lines(memory)[-4:])
    return " ".join(said).lower()


def _the_kind(clean, thread):
    if re.search(r"\b(?:should\s+(?:i|we)\s+wait|is\s+it\s+worth\s+waiting|wait\s+(?:for|till|"
                 r"until)\s+the\s+(?:sales?|payday|christmas|black\s+friday))\b", clean or ""):
        return "decision"
    for kind, words in (("repair", REPAIR_WORDS), ("order", ORDER_WORDS),
                        ("booking", BOOKING_WORDS), ("reply", REPLY_WORDS),
                        ("offer", OFFER_WORDS)):
        if words.search(thread):
            return kind
    return None


def for_the_ask(clean, repaired, memory):
    if not asks_for_a_date(clean, repaired):
        return None
    thread = _the_thread(clean, memory)
    if NOT_OURS.search(thread):
        return None
    kind = _the_kind(clean, thread)
    if kind == "decision":
        return WAITING_A_DECISION
    if kind == "repair":
        return WAITING_FOR_A_REPAIR
    if kind == "order":
        return WAITING_FOR_AN_ORDER
    if kind == "booking":
        return WAITING_FOR_A_BOOKING
    if kind == "reply":
        return WAITING_FOR_A_REPLY
    if kind == "offer":
        return WAITING_FOR_AN_OFFER
    return NOTHING_HELD


POOLS = (WAITING_FOR_AN_ORDER, WAITING_FOR_A_REPAIR, WAITING_FOR_A_BOOKING,
         WAITING_FOR_A_REPLY, WAITING_FOR_AN_OFFER, WAITING_A_DECISION, NOTHING_HELD)
