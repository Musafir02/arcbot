import re

from . import pick


def _bare(text):
    said = str(text or "").lower().replace("\u2019", "'").replace("'", "")
    return " ".join(re.sub(r"[^a-z0-9 ]+", " ", said).split())


THROAT = (r"(?:(?:ok|okay|right|so|hi|hello|hey|oi|and|oh|ah|er|um|umm|hmm|quick|just|also|"
          r"sorry|now|then|again)\s+)*")
ASKED = re.compile(
    r"^" + THROAT +
    r"(?:(?:can|could|would|will|might)\s+(?:you|u|ya)\b"
    r"|(?:please|pls|kindly)\b"
    r"|i\s+(?:want|need|would\s+like|would\s+love)\s+(?:you|u)\s+to\b)")
FOR_ME = re.compile(r"\b(?:for me|for us|on my behalf)\b")
FLAT = re.compile(
    r"^" + THROAT +
    r"(?:set|start|put|add|note|jot|print|scan|send|text|email|forward|upload|download|attach|"
    r"sign|fill|read|translate|record|play|pause|skip|cue|turn|switch|stick|keep|write|type)\b")
POINTS_HERE = re.compile(
    r"\b(?:it|this|that|these|those)\b|\bfor me\b"
    r"|\b(?:my|the)\s+(?:calendar|diary|planner|timer|notes?|alarm|phone|minutes|transcript|"
    r"report|letter|essay|forms?|pages?|list|draft|script)\b")
COMPOSE = re.compile(
    r"\b(?:draft|compose|word|reword|put\s+together)\b"
    r"|\bwrite\s+(?:\w+\s+){0,2}(?:text|message|email|letter|note|reply|card|email)\b"
    r"|\bnotes?\s+(?:for|to)\s")
JOBS = (
    ("timer", re.compile(r"\b(?:timer|countdown|stopwatch|alarm)\b")),
    ("diary", re.compile(r"\b(?:calendar|diary|planner)\b")),
    ("note", re.compile(r"\b(?:note\s+(?:that|it|this)|jot\s+(?:that|it|this)\s+down|"
                        r"write\s+(?:it|this|that)\s+down|make\s+a\s+note|"
                        r"keep\s+a\s+note|type\s+up\s+(?:my|the|this|these|those)\s+"
                        r"(?:notes?|minutes|transcript))\b")),
    ("send", re.compile(r"\b(?:send|sending|forward|post|share|print|scan|upload|download|"
                        r"attach|sign|fill\s+in|(?:text|email|message)\s+(?!to\b)|"
                        r"write\s+(?:it|this|that)\s+up|"
                        r"type\s+(?:it|this|that|these|those)\s+up|type\s+up\s+"
                        r"(?:my|the|this|that|these|those|your)\b)\b")),
    ("play", re.compile(
        r"\b(?:play|playing|pause|unpause|skip|stop|start|cue|turn|switch|stick|put\s+on)"
        r"\b(?:\s+\w+){0,3}?\s+"
        r"(?:music|song|songs|playlist|track|album|radio|telly|tv|video|podcast|episode|record)\b"
        r"|\b(?:telly|tv|radio|music|volume|sound)\s+(?:up|down|on|off|louder|quieter)\b")),
    ("read", re.compile(r"\b(?:read\s+(?:it|this|that|them)\s+(?:out|aloud|to\s+me|for\s+me)|"
                        r"read\s+(?:my|the|this|these|those)\s+(?:emails?|messages?|letter|page|"
                        r"screen|file|document|text)\b|read\s+(?:it\s+)?out\s+loud|translate|"
                        r"summari[sz]e|proofread)\b")),
)
TO_ME = re.compile(r"\b(?:send|text|email|message|post|share|read|write|print)\s+(?:me|us)\b")
LOOKUP = re.compile(
    r"\b(?:(?:google|search)\s+(?:it|that|this|something)\b|"
    r"look\s+(?:it|that|this|something)\s+up\b|look\s+up\s+(?:the|a|an|some|my)\b|"
    r"check\s+(?:it|that|this)\s+(?:online|up)\b|"
    r"read\s+(?:me\s+)?(?:the|today'?s|this\s+morning'?s)\s+"
    r"(?:news|headlines|papers?|weather|scores?|forecast)\b)")
A_HOW_TO_TAIL = re.compile(
    r"\b(?:how\s+to|how\s+do|how\s+can|what|why|when|where|which|who|if|whether)\b")
NOT_FOR_HELP = re.compile(
    r"\b(?:send|get|call|fetch|find)\s+(?:help|someone|somebody|anyone|anybody|the\s+police|"
    r"an?\s+ambulance|a\s+doctor|medical)\b|\b(?:send|get|call|fetch|ring)\s+for\b")
OWN_PLAN = re.compile(
    r"\b(?:in the morning|tomorrow|tonight|later on|next week|when i get (?:home|back)|"
    r"before i forget|after (?:work|lunch|tea))\b")
NOT_A_JOB = re.compile(
    r"^(?:how\b|whats\b|what\s+(?:is|are|should)\b|where\b|when\b|why\b|who\b|which\b|"
    r"(?:can|could|would|will)\s+(?:you|u)\s+(?:tell|show|explain|teach|help|suggest|recommend|"
    r"advise|remind|check|look|find|search|google|see|hear|watch|open|remember|know|think|"
    r"guess|say|give|list|make|do|work|count|spell)\b)")

JOBS_UNAVAILABLE = {
    "timer": (
        "Set that on the phone's timer - nothing on this end can ring or buzz, so the phone is "
        "the one to trust. What's it timing?",
        "I can't set a timer, no - no hands and nothing that buzzes. Your phone's clock app will, "
        "and tell me what it's for and I'll help you with the rest of it.",
    ),
    "diary": (
        "That has to go in your calendar rather than mine - I can't put anything in there. Tell "
        "me the date and what it's for, and I'll help you work out what has to happen before it.",
        "Nothing I can add to a diary from this end, sorry. Say when it is and I'll help you plan "
        "backwards from it.",
    ),
    "note": (
        "I can't keep a note past this chat, sorry. Say the line here and I'll help you get it "
        "short and plain, so it is worth saving the moment you copy it out.",
        "I can't save a note anywhere you'd see it later, sorry. Say it here and I'll hold it "
        "while we talk; copy it into your notes app before you go.",
    ),
    "send": (
        "I can't send, print or attach anything - I'm words in this chat, with nothing to post "
        "from. Paste the text here and I'll get the wording right, ready for you to send.",
        "That needs hands I haven't got, sorry. The words I can do: give me the message and I'll "
        "tidy it, shorten it or say it better.",
    ),
    "play": (
        "I can't play anything - there is no speaker on this end, only words. Put the radio or "
        "the telly on, and tell me what you're in the mood for and I'll suggest something.",
        "Nothing here to play it on, sorry. Say what kind of thing you fancy and I'll help you "
        "pick, then it's the remote or your own speaker that does the rest.",
    ),
    "read": (
        "The page is on your side of the chat, not mine - paste the bit you want and I'll read "
        "it, shorten it, or put it in other words.",
        "I can't see the file or the screen, sorry. Copy the words into the chat and I'll take it "
        "from there.",
        "No inbox on this end, sorry - nothing arrives here. Your mail app has it open in a tap, "
        "and paste me the message you want to answer and I'll help you word the reply.",
    ),
}


def reads(text):
    line = _bare(text)
    if not line or len(line.split()) > 18:
        return None
    if TO_ME.search(line) or COMPOSE.search(line) or NOT_FOR_HELP.search(line):
        return None
    asked = bool(ASKED.match(line)) or bool(FOR_ME.search(line))
    if asked and LOOKUP.search(line) and not A_HOW_TO_TAIL.search(line):
        return "lookup"
    if NOT_A_JOB.match(line):
        return None
    flat = bool(FLAT.match(line))
    if not asked and not flat:
        return None
    for kind, shape in JOBS:
        if not shape.search(line):
            continue
        if flat and not asked and (kind in ("send", "note") or OWN_PLAN.search(line)):
            if not POINTS_HERE.search(line) or OWN_PLAN.search(line):
                return None
        return kind
    return None


def writes_the_words(text):
    return reads(text) in ("send", "note", "read", "play")


MAIL = re.compile(r"\b(?:e-?mails?|inbox|mailbox|mail|messages?)\b")


def reply_for(text, memory):
    kind = reads(text)
    if not kind:
        return None
    if kind == "lookup":
        from . import fallback
        return pick(fallback.ABOUT_SELF["online"], memory, _bare(text))
    pool = JOBS_UNAVAILABLE[kind]
    if kind == "read":
        pool = (pool[2],) if MAIL.search(_bare(text)) else pool[:2]
    return pick(pool, memory, _bare(text))
