import re

from . import fallback, fallback_data
from ..memory import ack


BEEN_ON_A_STRETCH = re.compile(
    r"\b(?:ive|i've|i\u2019ve|i have|i had|weve|we've|we\u2019ve|we have|i)\s+been\b"
    r"(?P<doing>[a-z' ]{3,60}?)"
    r"(?P<when>\ball (?:day|night|morning|afternoon|evening|week|weekend|month|year|shift|term)\b"
    r"|\b(?:most of the|the whole|the entire)\s+(?:day|morning|afternoon|evening|week|weekend)\b"
    r"|\bfor (?:ages|ever|hours|days|weeks|months|years|minutes|a while|half an hour"
    r"|(?:a|an|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|"
    r"forty|fifteen|\d+)\s*"
    r"(?:hour|hours|minute|minutes|day|days|week|weeks|month|months|year|years))\b"
    r"|\b(?:ever since|since (?:this |last |the )?(?:morning|afternoon|evening|night|week|"
    r"weekend|month|year|monday|tuesday|wednesday|thursday|friday|saturday|sunday|january|february|"
    r"march|april|may|june|july|august|september|october|november|december|christmas|easter|"
    r"yesterday|noon|midnight|half (?:past )?(?:one|two|three|four|five|six|seven|eight|nine|ten|"
    r"eleven|twelve)|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"\d+(?::\d+)?\s*(?:am|pm)?))\b"
    r"|\b(?:hours|days|weeks|months|years|ages)\s+now\b\s*)",
    re.I)
POINTER_STRETCH = (
    "at this", "on this", "at it", "on it", "at that", "on that", "at these", "on these",
    "with this", "with it", "the thing")
SPENT_ON_A_STRETCH = re.compile(
    r"\b(?:ive|i've|i\u2019ve|i have|i|weve|we've|we\u2019ve|we have|we)\s+(?:spent|wasted)\b"
    r"(?P<doing>[a-z' ]{0,40}?)\s*"
    r"(?P<when>\ball (?:day|night|morning|afternoon|evening|weekend|week)\b"
    r"|\b(?:most of the|the whole|the entire)\s+(?:day|morning|afternoon|evening|weekend|week)\b"
    r"|\bfor (?:ages|hours|days|weeks|months|years)\b"
    r"|\b(?:hours|days|weeks|months|years)\s+now\b)",
    re.I)
TAKEN_A_STRETCH = re.compile(
    r"\b(?:this|that|it)(?:'s|s|\u2019s|\s+has|\s+had)\s+taken\s+(?:me|us)\s+"
    r"(?P<when>\ball (?:day|night|morning|afternoon|evening|weekend|week)\b"
    r"|\b(?:most of the|the whole|the entire)\s+(?:day|morning|afternoon|evening|weekend|week)\b"
    r"|\bfor (?:ages|hours|days|weeks|months|years)\b"
    r"|\b(?:hours|days|weeks|months|years)\s+now\b)",
    re.I)
VISITING_STRETCH = (
    "at the hospital", "in hospital", "at hospital", "in the hospital", "at a&e", "in a&e",
    "at the a&e", "in the a&e", "at the clinic", "at the doctors", "at the doctor's",
    "at the surgery", "at the care home", "at the hospice", "at the nursing home",
    "at the vets", "at the vet")
STRETCH_IS_FINISHED = (
    "finished", "finished it", "done it", "all done", "got it done", "sorted it", "sorted now",
    "got there", "finally done", "managed it", "got it finished", "its done", "it's done")
QUEUE_STRETCH = (
    "queueing", "queuing", "queued", "in a queue", "sat here", "standing here", "sat in the car",
    "waiting for the bus", "waiting for a bus", "waiting for the train", "waiting for a taxi",
    "waiting at the tip", "at the tip", "at the dump", "recycling centre")
WITH_THEIR_OWN = (
    "with my mum", "with my mom", "with my mother", "with my dad", "with my father",
    "with my nan", "with my gran", "with my grandma", "with my grandad", "with my granny",
    "with my son", "with my daughter", "with my kids", "with my child", "with my husband",
    "with my wife", "with my partner", "with my sister", "with my brother", "with my friend",
    "with my mate", "at my mum's", "at my mom's", "at my dad's", "at my nan's")
WAITING_AFTER_THE_STRETCH = (
    "waiting", "waited", "on hold", "in a queue", "queueing", "queuing", "on the phone")
VIGIL = re.compile(
    r"\bwait(?:ing|ed)?\s+(?:for|on|by|at|with)\b[^.]{0,24}?\b(?:die|dying|death|pass|"
    r"passing|go|wake|wake up|come round|come back|pull through|make it|breathe|survive)\b"
    r"|\b(?:by|at|beside)\s+(?:his|her|their|my (?:mum|mom|dad|nan|gran|son|daughter|wife|"
    r"husband|partner|sister|brother|friend)'?s?)\s+(?:bed|bedside)\b"
    r"|\b(?:his|her|their)\s+bedside\b")
NOT_A_SPENT_JOB = (
    "to get here", "to get there", "to drive", "to come", "to travel", "to walk", "the bus",
    "the train", "the traffic", "at work", "at the office", "in work", "at school", "at college",
    "at uni", "on a course")
WAITING_STRETCH = (
    "waiting", "waited", "chasing", "chased", "chase", "ringing", "phoning", "phoned",
    "calling", "emailing", "emailed", "messaging", "queuing", "queueing", "queued",
    "hounding", "pestering", "chasing it", "on hold", "on the phone", "in a queue",
    "on a waiting list", "on a waiting list", "back and forth", "trying to get through",
    "trying to speak", "trying to cancel", "hunting", "searching", "applying",
    "job hunting")
CARING_STRETCH = (
    "looking after", "caring for", "sitting with", "nursing", "minding",
    "cleaning up after", "running after", "running round after", "feeding", "settling",
    "carrying")
UP_WITH_A_PERSON = re.compile(
    r"\bup with\s+(?:my|her|his|their|our|the|a)\s+\w+|\bup with\s+(?:him|her|them|"
    r"mum|dad|nan|gran|the kids|someone)\b", re.I)
EFFORT_STRETCH = (
    "painting", "decorating", "wallpapering", "tiling", "plastering", "sanding",
    "stripping", "cleaning", "tidying", "sorting", "clearing",
    "hoovering", "vacuuming", "scrubbing", "washing", "ironing",
    "dusting", "unloading", "loading", "packing", "unpacking", "moving", "digging",
    "weeding", "mowing", "pruning", "building", "fixing", "mending", "repairing",
    "renovating", "assembling", "filing", "shredding", "decluttering", "boxing",
    "shifting", "polishing", "hanging", "hammering")
NOT_A_STRETCH_JOB = (
    "feeling", "felt", "low", "flat", "tired", "exhausted", "knackered", "shattered",
    "sleeping", "slept", "waking", "hurting", "aching", "sore", "sick", "puking",
    "vomiting", "throwing up", "bleeding", "coughing", "sneezing", "crying", "shaking",
    "dizzy", "worried", "anxious", "stressing", "stressed", "panicking", "missing",
    "thinking", "going over", "dreaming", "eating", "drinking", "smoking", "scratching",
    "itching", "out of breath", "breathless", "sweating", "on my feet", "in bed",
    "off work", "off sick", "off ill", "signed off", "on the sick")
WAITING_STRETCH_SAID_BACK = (
    "{When} - that is a long time to be kept waiting. Has anyone given you an answer yet?",
    "{When} and still no answer - who is left to try?",
    "{When} chasing the same thing. Has it moved at all?",
    "{When} and it is all waiting on other people. Is there a name you can ask for?",
)
EFFORT_STRETCH_SAID_BACK = (
    "{When} - that is a lot of it on one job. How close is it to done?",
    "{When} and still at it - what is left of it?",
    "{When} - jobs like that always take longer than they look. What is left?",
    "{When} at the same thing - is the end in sight?",
)
CARING_STRETCH_SAID_BACK = (
    "{When} - that is a lot of looking after someone, on your own. Does anyone give you a break?",
    "{When} being needed and nothing else. Who is looking after you in it?",
    "{When} of somebody else's week taking yours. Have you got any help with it?",
)
QUEUE_STRETCH_SAID_BACK = (
    "{When} in a queue - did it move at all?",
    "{When} of it and no sign of it moving. Is there another way round it, or is this the only one?",
    "{When} of it with nothing to show for it. How much more of it is there?",
)
VISITING_STRETCH_SAID_BACK = (
    "{When} in that place - those are mostly waiting about, whichever end of it you are on. "
    "How is it looking?",
    "{When}, and it is all waiting. How are things there?",
    "{When} of it. Nobody plans a day like that - how is it going?",
)
VISITING_SOMEBODY_SAID_BACK = (
    "{When} sitting with somebody. That is a long day for you as well - is anyone spelling you?",
    "{When} and no let up - how are they doing, and how are you doing with it?",
    "{When} of it. Is there anyone sitting with them so you can get a break?",
)
SOMEBODY_ELSE_IN_IT = (
    "with my mum", "with my mom", "with my mother", "with my dad", "with my father",
    "with my nan", "with my gran", "with my grandma", "with my grandad", "with my granny",
    "with my son", "with my daughter", "with my kids", "with my child", "with my husband",
    "with my wife", "with my partner", "with my sister", "with my brother", "with my friend",
    "with my mate", "to see my mum", "to see my mom", "to see my dad", "to see my nan",
    "to see my gran", "to see my son", "to see my daughter", "to see my wife",
    "to see my husband", "to see my partner", "to see my sister", "to see my brother",
    "to see my friend", "visiting my", "at my mum's", "at my mom's", "at my dad's",
    "at my nan's", "my mum is in", "my dad is in", "my nan is in", "my son is in",
    "my daughter is in", "my wife is in", "my husband is in", "my sister is in",
    "my brother is in", "my friend is in", "hes in hospital", "shes in hospital",
    "theyre in hospital", "with him", "with her", "with them")
WAITING_ON_THEIR_OWN = (
    "my mum", "my mom", "my dad", "my nan", "my gran", "my son", "my daughter", "my kids",
    "my husband", "my wife", "my partner", "my sister", "my brother", "my friend", "my mate",
    "my lad", "my girl", "the kids")
WAITING_FOR_A_PERSON = re.compile(r"\b(?:for|on)\s+(?:him|her|them)\s+(?:to|about)\b", re.I)
WAITING_ON_THEIR_OWN_SAID_BACK = (
    "{When} waiting on somebody of your own. Have they been in touch at all?",
    "{When} of it, and no word. Is this how they usually are?",
    "{When} waiting on them. That is a long time to be kept hanging about.",
)
WAITING_TO_TALK = (
    "to talk to someone", "to talk to somebody", "to talk to anyone", "for someone to talk to",
    "for somebody to talk to", "to have someone to talk to", "to have somebody to talk to",
    "to speak to someone", "to speak to somebody", "someone to talk to", "somebody to talk to")
TALKING_TO_A_PLACE = re.compile(
    r"\b(?:talk to|speak to|get through to|get hold of)\s+(?:someone|somebody|a person)\s+"
    r"(?:at|from|in)\b", re.I)
TALKING_STRETCH_SAID_BACK = (
    "{When} with nobody to talk to. That is a long stretch to carry on your own - what have you "
    "been doing with it?",
    "{When} of it, and no company. What is the day like where you are?",
    "{When} waiting for someone to talk to - well, you have my attention now. What is on your "
    "mind?",
)
STRETCH_STARTS_UPPER = frozenset((
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
    "january", "february", "march", "april", "may", "june", "july", "august", "september",
    "october", "november", "december", "christmas", "easter"))


def _the_stretch_said_back(phrase):
    words = [w for w in " ".join(phrase.split()).strip(" .,!?;:").split() if w]
    if words[:1] in (["for"], ["since"], ["all"], ["most"], ["the"]) and len(words) > 1:
        lead, rest = words[0], words[1:]
        words = [lead] + [w.capitalize() if w.lower() in STRETCH_STARTS_UPPER else w
                          for w in rest]
    if not words:
        return ""
    said = " ".join(words)
    return said[:1].upper() + said[1:]


def _names_one_of(doing, phrases):
    words = doing.split()
    return any((" " in phrase and phrase in doing) or phrase in words for phrase in phrases)


def _the_shape(doing, said, after):
    if _names_one_of(doing, NOT_A_STRETCH_JOB):
        return None
    if _names_one_of(doing, CARING_STRETCH) or UP_WITH_A_PERSON.search(said):
        return "caring"
    if _names_one_of(doing, QUEUE_STRETCH) or _names_one_of(said, QUEUE_STRETCH):
        return "queueing"
    if _names_one_of(doing, WAITING_STRETCH):
        if _names_one_of(said, WAITING_TO_TALK) and not TALKING_TO_A_PLACE.search(said):
            return "talking"
        if (_names_one_of(doing, WAITING_ON_THEIR_OWN) or _names_one_of(after, WAITING_ON_THEIR_OWN)
                or WAITING_FOR_A_PERSON.search(said)):
            return "waiting_on_their_own"
        return "waiting"
    if _names_one_of(said, VISITING_STRETCH) or _names_one_of(said, WITH_THEIR_OWN):
        return "visiting"
    if _names_one_of(doing, EFFORT_STRETCH):
        return "effort"
    if doing and _names_one_of(doing, POINTER_STRETCH):
        return "effort"
    if _names_one_of(after, WAITING_AFTER_THE_STRETCH) or \
            _names_one_of(said, WAITING_AFTER_THE_STRETCH):
        return "queueing" if _names_one_of(said, QUEUE_STRETCH) else "waiting"
    return None


def reads_as_a_long_stretch(clean):
    said = " ".join((clean or "").lower().split())
    if not said or "?" in said:
        return None
    for pattern, spent in ((BEEN_ON_A_STRETCH, False), (SPENT_ON_A_STRETCH, True)):
        for met in pattern.finditer(said):
            doing = (met.group("doing") or "").strip(" ,.;:")
            if len(doing.split()) > 8 or " and " in doing:
                continue
            when = _the_stretch_said_back(met.group("when"))
            if not when:
                continue
            if _names_one_of(said, NOT_A_STRETCH_JOB) or VIGIL.search(said):
                continue
            if _names_one_of(said, STRETCH_IS_FINISHED):
                continue
            if spent and _names_one_of(said, NOT_A_SPENT_JOB):
                continue
            shape = _the_shape(doing, said, said[met.end():])
            if shape or spent:
                return (shape or "effort", when)
    for met in TAKEN_A_STRETCH.finditer(said):
        when = _the_stretch_said_back(met.group("when"))
        if not when:
            continue
        if _names_one_of(said, NOT_A_STRETCH_JOB) or _names_one_of(said, NOT_A_SPENT_JOB):
            continue
        if _names_one_of(said, STRETCH_IS_FINISHED):
            continue
        return ("effort", when)
    return None


def the_stretch_pool(shape, when, said=""):
    if shape == "visiting":
        shape = ("visiting_somebody" if _names_one_of(said, SOMEBODY_ELSE_IN_IT)
                 else "visiting")
    pool = {"waiting": WAITING_STRETCH_SAID_BACK, "effort": EFFORT_STRETCH_SAID_BACK,
            "caring": CARING_STRETCH_SAID_BACK, "queueing": QUEUE_STRETCH_SAID_BACK,
            "visiting": VISITING_STRETCH_SAID_BACK,
            "visiting_somebody": VISITING_SOMEBODY_SAID_BACK,
            "waiting_on_their_own": WAITING_ON_THEIR_OWN_SAID_BACK,
            "talking": TALKING_STRETCH_SAID_BACK}.get(shape, ())
    return tuple(line.replace("{When}", when) for line in pool)


def _only_a_placeholder(text, said):
    said = " ".join(str(said or "").split())
    if not said:
        return True
    if said in fallback.NEUTRAL or fallback._is_a_hedge(said) or ack.reads_as_a_receipt(said):
        return True
    if said in fallback_data.A_SMALL_DAY or said in fallback_data.A_DAY_ASKED_PLAIN:
        return True
    mine = set(re.findall(r"[a-z']+", str(text or "").lower()))
    theirs = set(re.findall(r"[a-z']+", said.lower()))
    if len(mine) < 2:
        return False
    shared = mine & theirs
    return len(shared) >= 3 and len(shared) / len(mine) >= 0.6


def the_stretch_said_back(text, memory, said):
    if not _only_a_placeholder(text, said):
        return ""
    stretch = reads_as_a_long_stretch(text)
    if not stretch:
        return ""
    clean = " ".join(str(text or "").lower().split())
    return fallback._choose(the_stretch_pool(stretch[0], stretch[1], clean),
                            memory, clean) or ""
