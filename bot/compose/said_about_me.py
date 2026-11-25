import re

from . import pick

_A_CLOSE_PERSON = (r"(?:mum|mom|mam|mammy|mother|dad|father|daddy|stepmum|stepmom|stepdad|"
                   r"stepfather|stepmother|parent|nan|nana|gran|granny|grandma|grandad|"
                   r"grandpa|grandmother|grandfather|sister|brother|sis|bro|son|daughter|"
                   r"child|kid|teenager|teacher|tutor|head\s+teacher|boss|manager|"
                   r"colleague|friend|mate|neighbour|neighbor|uncle|aunt|auntie|"
                   r"mother[\s-]in[\s-]law|father[\s-]in[\s-]law|in[\s-]laws|cousin)")
CLOSE_PERSON = _A_CLOSE_PERSON + r"(?:s|es)?"
_SUBJECT = (r"(?:(?:my|our)\s+" + CLOSE_PERSON + r"|(?:he|she|they))")
_SAYING = (r"(?:say|says|said|saying|tell|tells|told|telling|think|thinks|thought|reckon|"
           r"reckons|moan|moans|moaned|complain|complains|complained|goes|went)"
           r"(?:\s+(?:me|that|how))?")
_A_STATE = (r"(?!fine\b|ok\b|okay\b|alright\b|all\s+right\b|good\b|great\b|grand\b|"
            r"tired\b|busy\b|hungry\b|sleepy\b|bored\b|sad\b|happy\b|upset\b|angry\b|"
            r"cross\b|late\b|early\b|right\b|wrong\b)")
_GETTING = (r"(?:getting|putting\s+on|gone)\s+(?:a\s+bit\s+|so\s+|really\s+|too\s+)?"
            r"(?:fat|big|heavy|chubby|large|weight|old|older|slow|slower|forgetful|lazy|"
            r"picky|soft|naughty|moody|grumpy|difficult)")
_VERDICT = (r"(?:i(?:'?m|\s+am|\s+aint|m)\s+" + _GETTING
            + r"|i(?:'?m|\s+am|\s+aint|m)\s+"
            r"(?:not\s+|so\s+|too\s+|just\s+|always\s+|really\s+)?"
            r"(?:a\s+|an\s+|the\s+)?" + _A_STATE + r"[a-z']+)")
_BEFORE_SAYING = (r"(?:\s+(?:keeps?|kept|always|constantly|regularly|just|still|also|now|"
                  r"honestly|literally|basically|straight|even))*(?:\s+is|\s+was)?\s*")
_AFTER_SAYING = r"\s+(?:(?:me|that|to\s+me|straight|honestly|basically|again|either)\s+){0,2}"
_ACT = (r"(?:i\s+(?:dont|don't|do\s+not|never|always|keep|can'?t|cannot|wont|won'?t|"
        r"made|make|mess|screw))")
REPORTED_LABEL = re.compile(
    r"\b" + _SUBJECT + r"\b" + _BEFORE_SAYING + r"\b" + _SAYING + _AFTER_SAYING
    + _VERDICT + r"[a-z']*", re.I)
REPORTED_ACT = re.compile(
    r"\b" + _SUBJECT + r"\b" + _BEFORE_SAYING + r"\b" + _SAYING + _AFTER_SAYING + _ACT, re.I)
REPORTED = REPORTED_LABEL

_DANGER = re.compile(
    r"\b(?:hit|hits|hitting|hurt|hurts|hurting|punch|punched|kick|kicked|slap|slapped|push|"
    r"pushed|pushing|throw|threw|thrown|strangle|strangled|choke|choked|choking|threat|"
    r"threatens|threatened|threatening|scared|scary|frightened|afraid|terrified|fear|"
    r"unsafe|not\s+safe|safety|lock|locked|locks|police|arrest|bruise|bruises|bleeding|"
    r"kill|kills|killing|dead|die|suicide|self[\s-]harm|starve|starving|withhold|"
    r"control|controlling|controls|track|tracks|tracking|monitor|monitors|isolate|"
    r"money|phone|passport|keys|drink|drunk|drugs|scream|screams|screaming|shout|shouts|"
    r"shouting|yell|yells|yelling|swear|swears|swearing|silent\s+treatment|ignores\s+me)\b", re.I)

_PARTNER = re.compile(
    r"\b(?:my|our)\s+(?:husband|wife|partner|boyfriend|girlfriend|fiance|fiancee|"
    r"ex|ex[\s-]?(?:husband|wife|partner|boyfriend|girlfriend)|hubby|carer|"
    r"step[\s-]?dad|step[\s-]?mum|step[\s-]?father|step[\s-]?mother)\b", re.I)

_GRANDPARENT = re.compile(r"\b(?:nan|nana|gran|granny|grandma|grandad|grandpa|grandmother|"
                          r"grandfather)s?\b", re.I)
_PARENT = re.compile(r"\b(?:mum|mom|mam|mammy|mother|dad|father|daddy|stepmum|stepmom|"
                     r"stepdad|stepfather|stepmother|parent)s?\b", re.I)
_SIBLING = re.compile(r"\b(?:sister|brother|sis|bro)s?\b", re.I)
_WORK = re.compile(r"\b(?:boss|manager|colleague)s?\b", re.I)
_SCHOOL = re.compile(r"\b(?:teacher|tutor|head\s+teacher|lecturer|form\s+tutor)s?\b", re.I)

_PARENT_LINES = (
    "That is a hard thing to hear from your mum or dad, and it says more about the day they are "
    "having than about you. Is this how they usually talk, or is it new?",
    "It lands hardest from a parent, whoever else says the same thing. What did they want you to "
    "be doing differently?",
    "Parents say the thing that will sting without meaning to. Has it been like this a while, or "
    "did something happen today?",
)
_GRANDPARENT_LINES = (
    "That is the kind of thing a nan says and then worries about. How did it land - did it come "
    "out of the blue, or is it a theme?",
    "Grandparents talk about weight in a way their own generation did, and it still stings coming "
    "from someone who is supposed to be on your side. What did you say back?",
)
_SIBLING_LINES = (
    "Brothers and sisters know exactly where to aim. Is this how they always talk to you, or "
    "has something changed?",
    "That is a sibling's line if ever there was one. Do they mean it, or is it the way they talk "
    "when they are in a mood?",
)
_WORK_LINES = (
    "That is a rough thing to hear where you are trying to do a job. Was it a fair point about the "
    "work, or was it a dig?",
    "Being told you are not up to it at work is a heavy thing to carry home. Has it come up more "
    "than once?",
    "A comment like that is easier to carry when you know what it was about. What was the job they "
    "were talking about?",
)
_SCHOOL_LINES = (
    "Being marked down by a teacher lands differently from being told it at home. Is it this "
    "subject, or all of it?",
    "A teacher saying that is usually about one piece of work, not about the whole person. What "
    "was it about?",
    "That is the kind of comment that sticks, and it says as much about their marking as about "
    "you. Has it been said more than once?",
)
_ACCUSED_LINES = (
    "That sounds like an old argument wearing a new coat. What makes her say it?",
    "Being told you do not care, when you clearly do, is a maddening thing to hear. What set it "
    "off?",
    "It is worth asking her straight what she means by it. What would she want you to do "
    "differently?",
    "That is a charge, not a small thing. How long has it been going on?",
)
_GENERIC_LINES = (
    "That is a rough thing to be told. What did they want you to do differently?",
    "Somebody saying that to you says more about them than about you. How did it land - did you "
    "believe it?",
    "That is a hard thing to hear, whichever way round it was meant. What do you think is behind "
    "it?",
)


_REPORTING = re.compile(
    r"\b(?:he|she|they|him|her|them|" + CLOSE_PERSON.replace("(?:", "(?:", 1) + r")\b"
    r"[^.?!]{0,25}?\b(?:say|says|said|saying|tell|tells|told|telling|think|thinks|thought|"
    r"reckon|reckons|reckoned|goes|went|call|calls|called|calling|moan|moans|complain|complains)"
    r"\b[^.?!]{0,20}?\b(?:i(?:'?m|\s+am)|im)\b", re.I)


def reads_as_somebody_elses_words(text):
    said = " ".join(str(text or "").split())
    return bool(said) and bool(_REPORTING.search(said))


def _kind(text):
    said = " ".join(str(text or "").split())
    if not said or "?" in said:
        return ""
    if _DANGER.search(said) or _PARTNER.search(said):
        return ""
    if REPORTED_LABEL.search(said):
        return "label"
    if REPORTED_ACT.search(said):
        return "act"
    return ""


def reads_as_reported_judgement(text):
    return bool(_kind(text))


_A_HABIT = re.compile(
    r"\b(?:every\s+time|every\s+(?:day|visit|week|night|time)|all\s+the\s+time|always|"
    r"constantly|whenever|each\s+time|again\s+and\s+again|keeps?\s+(?:doing|saying|going)|"
    r"again\s+today|it\s+happens|she\s+does\s+it|he\s+does\s+it|they\s+do\s+it)\b", re.I)
_HABIT_LINES = (
    "Then it is a pattern, not a comment, and a fresh answer each time is what keeps it going. "
    "Pick one sentence and use the same one every time, said calmly and early: \"I have heard "
    "you, and I am not going to argue about it today.\"",
    "If it comes up again and again, say once at the start that you are not going over it this "
    "time, and then do not take the bait. Naming it before it lands takes the teeth out of it.",
    "A remark that comes every time needs a conversation at a calm moment rather than in the "
    "moment it happens. What would you want to say to her when nothing is going on?",
)


def _user_lines(memory, how_many=3):
    turns = (memory or {}).get("turns") if isinstance(memory, dict) else None
    if not turns:
        return []
    out = []
    for turn in turns[-how_many * 2:]:
        if not isinstance(turn, dict):
            continue
        line = str(turn.get("user") or "")
        if not out or out[-1] != line:
            out.append(line)
    return out[-how_many:]


def _on_the_thread(memory):
    lines = _user_lines(memory)
    if not lines:
        return False
    if reads_as_reported_judgement(lines[-1]):
        return True
    return (len(lines) > 1 and bool(_A_HABIT.search(lines[-1]))
            and reads_as_reported_judgement(lines[-2]))


def answer_followup(text, memory=None):
    said = " ".join(str(text or "").split())
    if not said or "?" in said or len(said.split()) > 12:
        return ""
    if _DANGER.search(said) or not _A_HABIT.search(said):
        return ""
    if not _on_the_thread(memory):
        return ""
    return pick(_HABIT_LINES, memory if isinstance(memory, dict) else {}, said)


_SELF_ADDRESSED = re.compile(
    r"\b(?:yourself|how\s+you\s+feel|feel\s+about\s+yourself|you\s+feel\s+like|"
    r"youd\s+be\s+on\s+a\s+friend|harder\s+on\s+yourself)\b", re.I)


def speaks_to_a_self_judgement(reply):
    said = " ".join(str(reply or "").split())
    return bool(said) and bool(_SELF_ADDRESSED.search(said))


def answer_for(text, memory=None):
    if not reads_as_reported_judgement(text):
        return ""
    said = " ".join(str(text or "").split())
    if _kind(said) == "act":
        return pick(_ACCUSED_LINES, memory if isinstance(memory, dict) else {}, said)
    if _SCHOOL.search(said):
        pool = _SCHOOL_LINES
    elif _WORK.search(said):
        pool = _WORK_LINES
    elif _SIBLING.search(said):
        pool = _SIBLING_LINES
    elif _GRANDPARENT.search(said):
        pool = _GRANDPARENT_LINES
    elif _PARENT.search(said):
        pool = _PARENT_LINES
    else:
        pool = _GENERIC_LINES
    return pick(pool, memory if isinstance(memory, dict) else {}, said)
