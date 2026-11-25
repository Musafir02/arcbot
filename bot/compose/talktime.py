import re

from . import fallback

_DAY = (r"(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday|today|tomorrow|tonight|"
        r"christmas|the weekend)")
_PART = (r"(?:morning|afternoon|evening|night|daytime|lunchtime|teatime|"
         r"after work|after tea|after dinner|after lunch|after school|after the kids are in bed)")
_A_MARKER = (
    r"(?:(?:this |next |on |by )(?:" + _DAY + r")"
    r"|(?:" + _DAY + r")(?:\s+(?:" + _PART + r"))?"
    r"|(?:this |in the |in |during the |tomorrow )(?:" + _PART + r")"
    r"|(?:" + _PART + r")"
    r"|later(?:\s+on)?|in a (?:bit|minute|while|mo)|in the week|during the week|"
    r"sometime|some time|any time|at some point|at some stage|whenever|"
    r"next week|this week|next month|this month"
    r"|at\s+\d{1,2}(?:[.:]\d{2})?\s*(?:am|pm|a\.m\.|p\.m\.|o'?clock)?"
    r"|at\s+(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|noon|midday|"
    r"midnight|teatime|lunchtime|half\s+\w+|quarter\s+\w+)"
    r"|in\s+(?:a|one|two|three|half\s+an?|an?|\d{1,3})\s+(?:hour|hours|hr|hrs|minute|minutes|"
    r"min|mins)"
    r"|when you(?:'re| are) free|when you have time|when you get a chance|when you can)"
)
THE_TIME = r"(?:" + _A_MARKER + r"(?:\s+" + _A_MARKER + r"){0,2})"
A_COURTESY = r"(?:\s+(?:please|thanks|thank you|ta))?"

A_COMPANY_ASK = re.compile(
    r"^(?:hi|hiya|hey|hello|so|ok|okay|and|but|just|right)?[,!. ]*"
    r"(?:(?:can|could|will|would|do)\s+(?:you|u)\s+(?:please\s+)?)?"
    r"(?:(?:keep|stay)\s+me\s+company|stay\s+with\s+me)"
    r"(?:" + A_COURTESY + r"|\s+(?:" + THE_TIME + r")" + A_COURTESY + r")?\s*[?.!]*$")
A_TALK_AT_A_TIME_ASK = re.compile(
    r"^(?:hi|hiya|hey|hello|so|ok|okay|and|but|just|right|um|er)?[,!. ]*"
    r"(?:(?:can|could|shall|should|would|will)\s+(?:we|you|u|i)\s+(?:please\s+)?"
    r"(?:talk|chat|speak|catch up|have a word|have a chat|have a talk)"
    r"(?:\s+(?:to|with)\s+(?:you|u|me))?"
    r"|i\s+(?:want|need|would like|wanna|have)\s+to\s+(?:talk|chat|speak)\s+to\s+(?:you|u))"
    r"\s+"
    + THE_TIME + A_COURTESY +
    r"\s*[?.!]*$")
A_TALK_AT_A_TIME_HARM = re.compile(
    r"\b(?:kill myself|end it|end my life|suicid|self harm|hurt myself|overdose|\bdie\b|"
    r"\bdying\b|dead|funeral|died|cancer|hospital|ambulance|999|911)\b")

A_TALK_AT_A_TIME = (
    "I can't hold a time or remind you - no diary and no clock on this end. The chat doesn't mind "
    "when you come back, so start now or whenever suits: what's it about?",
    "Nothing here books a slot or rings you, so a time is the one thing I can't keep. What I can do "
    "is talk it through now and pick it up again when you come back. What did you want to say?",
    "There's no diary on this end, so I can't promise to be there at a set time - but nothing here "
    "closes either, so the thread keeps its place. What's on your mind?",
    "I can't put anything in a diary or set a reminder, and I would rather say that than nod along. "
    "What I can do is start now and keep the thread for whenever you come back. What's up?",
    "No clock here, so any hour is all the same to me, and the conversation stays where we leave "
    "it. What did you want to talk about?",
    "I can't save a slot or bring it up again, sorry - but the chat is here at any hour of the day "
    "and keeps its place. What's going on?",
)


def answer_for(text, memory=None):
    said = memory if isinstance(memory, dict) else {}
    clean = " ".join(str(text or "").lower().split())
    if not clean:
        return None
    if not (A_TALK_AT_A_TIME_ASK.match(clean) or A_COMPANY_ASK.match(clean)):
        return None
    if A_TALK_AT_A_TIME_HARM.search(clean):
        return None
    return fallback._choose(A_TALK_AT_A_TIME, said, clean)
