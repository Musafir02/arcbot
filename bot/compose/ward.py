import re

PERSON = re.compile(
    r"(?<![a-z])(?:he|she|they|him|her|them|his|their)(?![a-z])"
    r"|(?<![a-z])(?:my|our|his|her|their)\s+(?:mum|mom|mother|dad|father|son|daughter|child|kid|"
    r"wife|husband|partner|brother|sister|gran|granny|grandma|grandad|grandpa|nana|nan|aunt|"
    r"uncle|cousin|friend|mate|neighbour|neighbor|baby|boy|girl|lad|boss|colleague)(?![a-z])",
    re.I)
SELF = re.compile(r"(?<![a-z])(?:i|me|my|mine|myself)(?![a-z])", re.I)
PLACE = re.compile(
    r"(?<![a-z])(?:hospital|ward|hospice|care home|nursing home|residential home|clinic|"
    r"infirmary|a&e|theatre|theatres)(?![a-z])", re.I)
STAFF = re.compile(
    r"(?<![a-z])(?:consultant|doctor|nurse|midwife|anaesthetist|anesthetist|surgeon|registrar|"
    r"duty nurse)(?![a-z])", re.I)
DETAIL = re.compile(
    r"(?<![a-z])(?:operation|surgery|op|procedure|scan|x-ray|xray|mri|ct scan|ultrasound|"
    r"results|test results|notes|chart|discharge|discharged|visitors|visiting|"
    r"visiting hours)(?![a-z])", re.I)
ASK = re.compile(
    r"(?<![a-z])(?:how long|how soon|how many days|when|what time|what ward|what room|"
    r"what unit|what bed|what hospital|which|where|has (?:she|he|they)|have they|"
    r"is (?:she|he|they)|are they|will (?:she|he|they)|can i|can we|could i|am i allowed|"
    r"are we allowed|did they)(?![a-z])", re.I)
SOMETHING_WRONG = re.compile(
    r"(?<![a-z])(?:pain|painful|hurts?|hurting|aching|aches?|sore|swollen|swelling|bleeding|bled|"
    r"fever|temperature|rash|infection|infected|vomit|vomiting|dizzy|breathless|bruise|wound|"
    r"symptom|diagnos\w*)(?![a-z])", re.I)
A_PET = re.compile(
    r"(?<![a-z])(?:vet|vets|veterinary|puppy|kitten|rabbit|hamster|guinea|budgie|parrot|"
    r"dog|cat|horse|pony)(?![a-z])", re.I)
HOME_AGAIN = re.compile(
    r"(?<![a-z])(?:"
    r"is (?:now )?home|are (?:now )?home|was home|were home|got home|back home|"
    r"came home|has come home|had come home|"
    r"left (?:the )?hospital|came out of (?:the )?hospital|got out of (?:the )?hospital|"
    r"out of (?:the )?hospital now|"
    r"(?<!come )(?<!coming )(?<!comes )(?<!get )(?<!getting )(?<!go )(?<!going )(?<!going to )"
    r"home from (?:the )?hospital|"
    r"(?:has|have|had) been discharged|was discharged|is discharged"
    r")(?![a-z])", re.I)
A_STAY_IN_THE_LINE = re.compile(
    r"(?<![a-z])(?:in for|in there|in here|still in|be in|is (?:she|he|they) in|are they in|"
    r"staying|stay overnight|staying overnight|can i stay|"
    r"out of (?:there|hospital)|discharg\w*|visitors?|visiting|room|bed|bay|ward|"
    r"(?:coming|came|come) home|(?:going|went) home|get home|getting home|back on (?:her|his|their) feet)"
    r"(?![a-z])", re.I)
THE_BOT = re.compile(r"(?<![a-z])(?:you|your|yours|yourself)(?![a-z])", re.I)

THE_WARD_KNOWS = (
    "Nobody here can see {whose} notes, so the ward is the way to find out: ring and ask for the "
    "nurse looking after {whom}, and put the question as you put it to me.",
    "That sits in {whose} notes, and nothing here can read them. Ring the ward and ask for the "
    "nurse on duty - they will tell you what is happening and what happens next.",
    "Only the people looking after {whom} can say. Ring the ward, say who you are and who you are "
    "asking about, and ask them straight.",
    "I can't see {whose} chart from here. Ring the ward and ask for the nurse looking after "
    "{whom}: they have the notes in front of them and they answer this all day.",
    "The answer is in {whose} notes, so it has to come from the ward. Ring them, ask for the "
    "nurse on duty, and say what you need to know - they can look it up while you are on the "
    "phone.",
)
WHOSE = {"her": "her", "him": "his", "them": "their", "you": "your"}


def _whom(said):
    if re.search(r"(?<![a-z])she(?![a-z])", said, re.I):
        return "her"
    if re.search(r"(?<![a-z])he(?![a-z])", said, re.I):
        return "him"
    if not PERSON.search(said):
        return "you"
    return "them"


def _the_place_before(memory):
    if not isinstance(memory, dict):
        return ""
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    return " ".join(str(turn.get("user") or "").lower() for turn in turns[-3:])


def answer_for(text, memory=None):
    said = " ".join(str(text or "").lower().split())
    if len(said.split()) < 3 or THE_BOT.search(said):
        return None
    room = " ".join((said, _the_place_before(memory)))
    if A_PET.search(room) or SOMETHING_WRONG.search(room) or HOME_AGAIN.search(room):
        return None
    if not (PLACE.search(room) or STAFF.search(room) or DETAIL.search(room)):
        return None
    if not (PLACE.search(said) or STAFF.search(said) or DETAIL.search(said)) \
            and not A_STAY_IN_THE_LINE.search(said):
        return None
    if not (PERSON.search(said) or (SELF.search(said) and PLACE.search(room))):
        return None
    if not ASK.search(said):
        return None
    whom = _whom(said)
    seed = len((memory or {}).get("turns") or []) * 31 + len(said)
    return THE_WARD_KNOWS[seed % len(THE_WARD_KNOWS)].format(whose=WHOSE[whom], whom=whom)
