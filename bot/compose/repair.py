import re

PEOPLE = (r"(?:mum|mom|mam|mother|dad|father|son|daughter|child|kid|kids|baby|partner|husband|"
          r"wife|boyfriend|girlfriend|fiance|fiancee|ex|sister|brother|nan|nana|gran|granny|"
          r"grandma|grandad|grandpa|aunt|uncle|cousin|stepmum|stepdad|stepson|stepdaughter|"
          r"mother in law|father in law|in laws|friend|friends|mate|best friend|bestie|"
          r"flatmate|housemate|neighbour|neighbor|boss|manager|colleague|coworker|team|staff)")
WHO = (r"(?:(?:my|his|her|their|our|the)\s+%s|him|her|them|someone|somebody)" % PEOPLE)
_BETWEEN = r"(?:(?:have|had|ve|d|just|really|actually|totally|completely|already|also|then|" \
           r"kind of|sort of|so|still|again|keep|keeps|kept|always|often|usually|sometimes|" \
           r"constantly|managed to|went and)\s+){0,4}"

_THE_THING_THEY_WERE_IN = (
    r"(?:%s)?(?:play|concert|recital|match|game|show|performance|assembly|sports day|"
    r"parents evening|parents' evening|nativity|graduation|prize giving|prizegiving|first day|"
    r"open day|appointment)\b"
    % r"(?:school|first|big|little|football|netball|swimming|music|dance|"
      r"christmas|xmas|summer|end of term|leavers?)\s+")

DEEDS = (
    ("let down", re.compile(
        r"(?:\bi\s+%s|\b(?:about|for|after|of)\s+%s)(?:let|lets|letting)\s+%s\s+down\b"
        % (_BETWEEN, _BETWEEN, WHO))),
    ("lied", re.compile(r"\bi\s+%s(?:lied|lie|lying|lies)\b[^.!?]{0,20}?\bto\s+%s\b"
                        % (_BETWEEN, WHO))),
    ("lied", re.compile(r"\bi\s+%s(?:told|tell|have told|ve told)\s+(?:%s\s+)?(?:a\s+)?lie\b"
                        % (_BETWEEN, WHO))),
    ("forgot a date", re.compile(
        r"\bi\s+(?:(?:keep|always|completely|totally|just|nearly|almost|went and|went)\s+){0,3}"
        r"(?:forgot|forget|forgetting|forgotten)\b[^.!?]{0,40}?"
        r"\b(?:birthday|anniversary)\b")),
    ("forgot a date", re.compile(
        r"\bi\s+%s(?:missed|miss)\s+(?:%s'?s?\s+)?(?:birthday|anniversary)\b"
        % (_BETWEEN, WHO))),
    ("lost my temper", re.compile(r"\bi\s+%s(?:lost|lose|losing|have lost|ve lost)\s+my\s+temper\b"
                                  % _BETWEEN)),
    ("upset them", re.compile(
        r"\bi\s+%s(?:upset|hurt|offended|insulted|embarrassed|annoyed|disappointed|angered)\s+%s\b"
        % (_BETWEEN, WHO))),
    ("upset them", re.compile(r"\bi\s+%s(?:hurt|upset|offended|annoyed)\s+%s'?s?\s+feelings\b"
                              % (_BETWEEN, WHO))),
    ("was unkind to them", re.compile(
        r"\bi\s+%s(?:was|been|am|have been|ve been|were)\s+(?:a bit |a little |really |very |"
        r"so |quite |pretty |just |being |really being |so being )*"
        r"(?:rude|horrible|mean|cruel|unkind|nasty|sharp|short|unfair|dismissive|snappy|"
        r"off|offhand|harsh|awful|dreadful|terrible|disrespectful|cheeky|abrupt)\s+"
        r"(?:to|with|towards|toward)\s+%s\b" % (_BETWEEN, WHO))),
    ("shouted at them", re.compile(
        r"\bi\s+%s(?:shouted|yelled|screamed|snapped|swore|sworn)\s+"
        r"(?:at|with)\s+%s\b" % (_BETWEEN, WHO))),
    ("said the wrong thing", re.compile(
        r"\bi\s+(?:%s)?(?:said|say|saying|told|tell|telling)\s+(?:the wrong thing|the wrong "
        r"words|something\s+(?:stupid|awful|daft|silly|dumb|mean|horrible|wrong|embarrassing|"
        r"terrible|harsh|unkind))\b" % _BETWEEN)),
    ("said the wrong thing", re.compile(
        r"\bi\s+(?:%s)?(?:said|told)\b[^.!?]{0,40}\b(?:was|were|is) (?:awful|horrible|stupid|"
        r"mean|rude|unkind|dreadful|terrible|nasty|rubbish|disgusting|pathetic)\b" % _BETWEEN)),
    ("missed their thing", re.compile(
        r"\bi\s+%s(?:missed|miss)\s+(?:(?:%s)'?s?\s+|(?:my|his|her|their|our)\s+)%s"
        % (_BETWEEN, WHO, _THE_THING_THEY_WERE_IN))),
    ("broke a promise", re.compile(
        r"\bi\s+%s(?:broke|broken|break|breaks|have broken|ve broken)\s+(?:a\s+|my\s+|the\s+)?"
        r"promise\b" % _BETWEEN)),
    ("cancelled on them", re.compile(
        r"\bi\s+%s(?:stood|stand|standing)\s+%s\s+up\b" % (_BETWEEN, WHO))),
    ("cancelled on them", re.compile(
        r"\bi\s+%s(?:cancelled|canceled|cancel|cancelling|canceling)\s+(?:on\s+)?%s\b"
        % (_BETWEEN, WHO))),
    ("ignored them", re.compile(
        r"\bi\s+%s(?:ignored|ignore|ignoring|blanked|blank)\s+%s\b" % (_BETWEEN, WHO))),
    ("ignored them", re.compile(
        r"\bi\s+%s(?:ignored|ignore|ignoring|blanked|blank)\s+%s'?s?\s+"
        r"(?:calls?|texts?|messages?|emails?|letters?|invites?)\b" % (_BETWEEN, WHO))),
    ("made them cry", re.compile(
        r"\bi\s+%s(?:made|make|making|have made|ve made)\s+%s\s+"
        r"(?:cry|cried|crying|sad|miserable|upset|tearful)\b" % (_BETWEEN, WHO))),
)

_LAPSE_VERBS = (
    r"(?:call(?:ed|ing)?|ring|rang|rung|ringing|text(?:ed|ing)?|messag(?:e|ed|ing)|"
    r"repl(?:y|ied|ying)|writ(?:e|ing|ten)|visit(?:ed|ing)?|wish(?:ed|ing)?|send|sent|sending)")
LAPSES = (
    ("left it too long", re.compile(
        r"\bi\s+%s(?:forgot|forget|forgetting|have forgotten|ve forgotten)\s+to\s+"
        r"%s\b[^.!?]{0,30}?%s" % (_BETWEEN, _LAPSE_VERBS, WHO))),
    ("left it too long", re.compile(
        r"\bi\s+%s(?:didnt|didn'?t|did not|never|havent|haven'?t|have not|hadnt|hadn'?t|"
        r"had not|hasnt|hasn'?t|has not)\s+%s"
        r"(?:\s+to)?\s+%s'?s?\b" % (_BETWEEN, _LAPSE_VERBS, WHO))),
    ("left it too long", re.compile(
        r"\bi\s+%s(?:havent|haven'?t|have not|hadnt|hadn'?t|had not)\s+"
        r"(?:seen|saw|visited|been\s+to\s+see)\s+%s\s+in\b"
        % (_BETWEEN, WHO))),
    ("left it too long", re.compile(
        r"\bi\s+%s(?:didnt|didn'?t|did not|never)\s+(?:get|got|buy|bought|send|sent)\s+%s\s+"
        r"(?:anything|nothing|a\s+(?:present|gift|card))" % (_BETWEEN, WHO))),
)


NOT_A_DEED = re.compile(
    r"\b(?:let|letting)\s+(?:my|her|his|their|your)\s+hair\s+down\b|"
    r"\bi (?:hurt|upset|pulled|broke|twisted|strained|cut|burnt|burned|dislocated|sprained)\s+"
    r"my\s+(?:back|knee|ankle|shoulder|arm|leg|foot|feet|hand|finger|wrist|neck|head|hip|"
    r"stomach|toe|ribs?|thumb|elbow|eye|teeth|tooth|ear|throat|chest|spine|hamstring|"
    r"calves|calf|shin|jaw|skin|appetite|weight|sleep|hair)\b|"
    r"\bi (?:lost|lose|losing)\s+my\s+(?:keys|phone|wallet|purse|job|way|mind|"
    r"trainers|glasses|vape|earbuds?)\b|"
    r"\bi (?:am|m|feel|felt|been)\s+(?:so |really |very |a bit )?"
    r"(?:lost|stuck|short of|out of)\b|"
    r"\bi (?:never|don'?t|didnt|didn'?t|hardly ever|rarely)\s+(?:let|lied|lie|forget|lose|lost|"
    r"shout|yell|snap|swear|cancel|ignore|blank)\b")
NOBODY_TO_REPAIR = re.compile(
    r"\b(?:didnt|didn'?t|did not|never)\s+(?:get|got|win|won|pass|passed|make|made)\b|"
    r"\b(?:got|been) (?:fired|sacked|dumped|rejected|turned down)\b|"
    r"\bthere'?s no fixing\b|\bit'?s too late\b")


PHYSICAL_HARM = re.compile(
    r"\b(?:hit|hits|hitting|punch|punched|slap|slapped|push|pushed|shove|shoved|shook|shake|"
    r"shaking|kick|kicked|throw|threw|thumped|strangle|strangled|bit|biting|dragged|grabbed)\b|"
    r"\b(?:hurt|hurting|injured|burned|burnt|bruised)\s+(?:my|her|his|their|our)\s+"
    r"(?:baby|child|kid|kids|son|daughter|wife|husband|partner|girlfriend|boyfriend|mum|mom|dad|"
    r"mother|father|sister|brother)\b(?!'?s?\s+feelings)")


PET_OR_PROFESSIONAL = re.compile(
    r"\b(?:to|with|at)\s+(?:my|our|the|a)\s+(?:dog|cat|puppy|kitten|horse|pony|rabbit|"
    r"hamster|guinea pig|budgie|parrot|pet|fish|bird|chickens?|sheep|cow|goat|lamb|doctor|gp|"
    r"nurse|consultant|surgeon|midwife|health visitor|dentist|orthodontist|physio(?:therapist)?|"
    r"pharmacist|optician|vet|solicitor|accountant|landlord|letting agent|bank)\b")


DEEDS_WITH_A_CARD = frozenset({"lost my temper", "shouted at them", "forgot a date",
                               "cancelled on them"})


_REGRET_FIRST = re.compile(r"^\s*(?:(?:honestly|god|tbh|ugh|so|ok|okay)\s+)*i\s+"
                           r"(?:just\s+|really\s+|deeply\s+|so\s+|still\s+)*regret\w*\b")

_FEELING_FIRST = re.compile(
    r"^\s*(?:(?:honestly|god|tbh|ugh|sometimes|now|ok|okay|so)\s+)*"
    r"i\s+(?:just\s+|really\s+|still\s+|properly\s+|honestly\s+)*"
    r"(?:feel|felt|feels)\b"
    r"[^.?!]{0,40}?\b(?:that|about|for|because|when|after|of|at|like)\b\s*"
    r"(?:i|i'?ve|im|i'?m|me|my|not|letting|cancelling|missing|going|being|doing)\b")

THE_FEELING_NAMED = ("Guilt like that is doing its job if it moves on: ")
THE_FEELING_NAMED_DATED = ("Guilt about a date does not make it right, so put it right: ")


_GRIEF = re.compile(
    r"\b(?:died|dies|dying|death|deaths|passed away|passed on|funeral|burial|cremation|"
    r"grief|grieving|bereav\w*|widow|widower|widowed|estate|the will|his will|her will)\b")


_A_BABY = re.compile(r"\b(?:baby|babies|newborn|newborns|infant|infants)\b")


def deed_of(clean):
    if isinstance(clean, dict):
        clean = clean.get("clean") or clean.get("text") or ""
    text = " ".join(str(clean or "").lower().replace("\u2019", "'").split())
    if not text:
        return None
    if PET_OR_PROFESSIONAL.search(text) or PHYSICAL_HARM.search(text):
        return None
    if _GRIEF.search(text):
        return None
    if _A_BABY.search(text):
        return None
    if _REGRET_FIRST.search(text):
        return None
    for deed, pattern in LAPSES:
        if pattern.search(text):
            return deed
    if NOT_A_DEED.search(text) or NOBODY_TO_REPAIR.search(text):
        return None
    for deed, pattern in DEEDS:
        if pattern.search(text):
            return deed
    return None


def owns_the_deed(line):
    return deed_of(line) is not None


_AMENDS = (
    r"\b(?:make|making)\s+(?:[\w']+\s+){0,6}up\s+to\s+%s\b|"
    r"\b(?:make|making|made)\s+(?:it\s+)?up\s+to\s+%s\b|"
    r"\bmake\s+(?:it\s+)?up\s+with\s+%s\b|"
    r"\bmake\s+(?:some\s+)?amends\b|"
    r"\bput\s+(?:it|things)\s+right\s+(?:with|to)\s+%s\b")
AMENDS = re.compile(_AMENDS % (WHO, WHO, WHO, WHO))


def with_the_feeling_named(reply, clean):
    if not reply:
        return reply
    text = " ".join(str(clean or "").lower().replace("\u2019", "'").split())
    if not _FEELING_FIRST.search(text):
        return reply
    lead = THE_FEELING_NAMED_DATED if deed_of(text) == "forgot a date" else THE_FEELING_NAMED
    return lead + reply[0].lower() + reply[1:]


def line_of(reading):
    if isinstance(reading, str):
        return reading
    if not isinstance(reading, dict):
        return ""
    for key in ("clean", "text"):
        value = reading.get(key)
        if isinstance(value, str) and value:
            return value
    return " ".join(word for word in (reading.get("words") or ()) if isinstance(word, str))


def amends_to(clean):
    if isinstance(clean, dict):
        clean = clean.get("clean") or clean.get("text") or ""
    text = " ".join(str(clean or "").lower().replace("\u2019", "'").split())
    if not text or not AMENDS.search(text):
        return False
    return not (PET_OR_PROFESSIONAL.search(text) or PHYSICAL_HARM.search(text))


ASKS_FOR_THE_WORDS = re.compile(
    r"\bwhat (?:do|should|shall|can|could) i (?:actually |really )?(?:say|tell)\b|"
    r"\bhow (?:do|should) i (?:say it|word it|put it|phrase it)\b|"
    r"\bwhat (?:would|should) i say\b|\bwhat do i say to\b|\bhow do i tell (?:her|him|them)\b|"
    r"\bi (?:just |really )?dont know what to say\b")

ASKS_WHAT_TO_DO = re.compile(
    r"\bwhat (?:do|should|shall|can|could) i do\b|\bhow (?:do|can|should) i (?:fix|make|put|"
    r"smooth|sort)\b|\bhow do i (?:fix it|make it right|make up for it)\b|"
    r"\bwhere do i start\b|\bwhat now\b|\bwhats the next step\b|\bany advice\b|"
    r"\bwhat would you do\b|\bhow do i say sorry\b|\bhow do i apologise\b")


def a_repair_is_open(memory):
    if not isinstance(memory, dict):
        return False
    told = [str(turn.get("user") or "").lower() for turn in (memory.get("turns") or [])
            if isinstance(turn, dict)]
    for said in reversed(told[-3:]):
        said = " ".join(said.split())
        if not said:
            continue
        if owns_the_deed(said) or amends_to(said):
            return True
        if len(said.split()) > 9 or not (ASKS_FOR_THE_WORDS.search(said)
                                         or ASKS_WHAT_TO_DO.search(said)):
            return False
    return False
