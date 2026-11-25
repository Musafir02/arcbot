import re

from . import pick as compose_pick

INVITED = re.compile(
    r"\b(?:do|would|will|can)\s+you\s+(?:want|fancy|feel\s+like|be\s+up\s+for|come|join)\b"
    r"|\b(?:do|would|will)\s+you\s+(?:like\s+to\s+)?(?:come|join)\b"
    r"|\bfancy\b|\bup\s+for\b|\bwanna\b|\bshall\s+we\b|\bwe\s+could\b"
    r"|\bwant\s+to\s+(?:go|get|grab|have|see|watch|come|join)\b"
    r"|\bcare\s+to\s+(?:come|join)\b")
INVITED_AT_THE_START = re.compile(r"^(?:fancy|wanna|up\s+for|shall\s+we|we\s+could|want\s+to)\b")
NOT_THEIRS = re.compile(r"^(?:i|we|he|she|they|my|our|her|his|their)\b")
NOT_WANTED = re.compile(
    r"\b(?:know|knew|learn|ask|asked|tell|say|hear|check|explain|guess|help|try)\b"
    r"|\b(?:see|check|find\s+out)\s+if\b|\bwhether\b|\bhow\s+to\b")
NOT_AN_INVITE = re.compile(
    r"\b(?:anything|something|a\s+hand|a\s+lift|a\s+receipt|a\s+piece|me\s+come|"
    r"her|him|them|die|dying|kill)\b"
    r"|\b(?:want|like|need|fancy)\s+(?:me|us)\s+to\b")

PRESENCE = re.compile(
    r"\b(?:can|could|would|will)\s+(?:you|u)\s+(?:please\s+|possibly\s+)?"
    r"(?:come|pop|stop|drop|visit|join|meet|attend|be)\b"
    r"|\bare\s+(?:you|u)\s+(?:coming|free|around|about)\b"
    r"|\b(?:do|would|will)\s+(?:you|u)\s+(?:be\s+)?(?:coming|there|around)\b"
    r"|\b(?:you|u)\s+(?:coming|joining\s+(?:me|us))\b"
    r"|\bwhy\s+don'?t\s+(?:you|u)\s+(?:come|join)\b"
    r"|\b(?:come|join)\s+(?:me|us)\s+(?:for|to)\b")
NOT_PRESENCE = re.compile(
    r"\bcome\s+(?:up|back|across|down\s+to|off)\b"
    r"|\b(?:be|being)\s+there\s+for\s+(?:me|us|him|her|them)\b"
    r"|\bmeet\s+(?:the|a|an|my|your|our)\b"
    r"|\b(?:be|is|are|was)\s+(?:there|around)\s+(?:when|if|to\s+(?:help|talk|listen))\b")
ASKING_IF_IM_HERE = re.compile(
    r"^(?:hi|hey|hello|ok|okay|so|right|and|thanks|ta|sorry|please)?\s*"
    r"(?:are\s+(?:you|u)|you|r\s+u)\s+(?:there|here|about|around)\s*[?.!]*$")

TOGETHER_AT = (
    ("drink", re.compile(
        r"\b(?:coffee|cuppa|brew|pint|beer|wine|drink|juice|tea\s+out|pub|bar|cafe|"
        r"coffee\s+shop)\b")),
    ("meal", re.compile(
        r"\b(?:lunch|dinner|brunch|breakfast|takeaway|take\s+away|curry|pizza|chinese|indian|"
        r"bite|meal|restaurant|nando'?s|kebab)\b")),
    ("walk", re.compile(
        r"\b(?:walk|stroll|hike|wander|run|jog|cycle|bike\s+ride|swim|gym|park\s+run)\b")),
    ("screen", re.compile(
        r"\b(?:film|movie|show|play|gig|concert|match|telly|cinema|theatre|festival)\b")),
    ("shopping", re.compile(
        r"\b(?:shopping|shops|market|city\s+centre|high\s+street|boot\s+sale)\b")),
    ("out", re.compile(
        r"\b(?:day\s+out|weekend\s+away|trip|beach|countryside|seaside|coast|museum|"
        r"stately\s+home|picnic)\b")),
    ("do", re.compile(
        r"\b(?:party|bbq|barbecue|barbeque|wedding|birthday|christening|housewarming|"
        r"house-warming|quiz|karaoke|reunion|funeral|wake|service|graduation|"
        r"engagement|anniversary|get-together|get\s+together|celebration|naming\s+ceremony)\b"
        r"|\b(?:a|the|this|that|my|his|her|their|big|fancy|work|office|leaving|christmas|"
        r"charity|fundraising|retirement|birthday)\s+do\b")),
)
TOGETHER_REPLIES = {
    "drink": (
        "I can't come along, but that sounds like a good idea. Where do you go for it?",
        "Wish I could join you. Somewhere near you, or the place you always go?",
    ),
    "meal": (
        "I can't make it, but that sounds good. Is it a treat, or an ordinary weeknight?",
        "Wish I could be there. Somewhere new, or the place you always end up in?",
    ),
    "walk": (
        "I can't come with you, but that sounds like a good idea. Is there a route you like, or "
        "somewhere new to try?",
        "Wish I could join you. It clears the head more than people expect - where do you go?",
    ),
    "screen": (
        "I can't come along, but that is a good shout. What is on?",
        "Wish I could be there. Something you have been meaning to see, or picking on the night?",
    ),
    "shopping": (
        "I can't come along, but that sounds like a good afternoon. Is it a browse, or are you "
        "after something in particular?",
        "Wish I could be there. Do you know what you want, or will it find you?",
    ),
    "out": (
        "I can't come along, but that sounds like a good day out. Where are you thinking?",
        "Wish I could be there. Have you been before, or would it be the first time?",
    ),
    "do": (
        "I can't be there - I'm words on a screen - but it sounds a good do. What do you need "
        "help with for it: what to take, what to wear, or what to say to the host?",
        "No legs on this end, so I can't make it, sorry. Tell me how many are going and what you've "
        "got to sort out, and I'll do the planning side of it.",
    ),
}

PRESENCE_REPLIES = (
    "I can't be there in person - nothing here leaves the chat - but tell me the plan and I'll do "
    "the useful half: what to take, what to cook, how to get there.",
    "No body on this end, so coming along isn't mine, sorry. Say what the day looks like and I'll "
    "help with the bits that are words - the list, the timing, what to say.",
    "I'd be there if I could. I'm not, so let me help from here: how many are coming, and what have "
    "you got left to sort?",
)


def _the_invitation(clean):
    text = " ".join(str(clean or "").lower().split())
    if not text or ASKING_IF_IM_HERE.match(text):
        return None
    present = bool(PRESENCE.search(text)) and not NOT_PRESENCE.search(text)
    if not present and not INVITED.search(text):
        return None
    if not INVITED_AT_THE_START.match(text) and NOT_THEIRS.match(text):
        return None
    if not present and (NOT_WANTED.search(text) or NOT_AN_INVITE.search(text)):
        return None
    if present and NOT_AN_INVITE.search(text):
        return None
    for kind, pattern in TOGETHER_AT:
        if pattern.search(text):
            return TOGETHER_REPLIES[kind]
    if present:
        return PRESENCE_REPLIES
    return None


def reply_for(text, memory):
    clean = " ".join(str(text or "").lower().split())
    pool = _the_invitation(clean)
    if not pool:
        return None
    return compose_pick(pool, memory, clean)
