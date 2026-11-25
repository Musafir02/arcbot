import re

from . import pick

THEIRS = frozenset("""
wedding funeral wake christening baptism party celebration anniversary birthday
scan appointment interview exam test operation surgery treatment chemo chemotherapy
radiotherapy biopsy results procedure checkup consultation diagnosis meeting
presentation review appraisal shift holiday honeymoon trip flight journey drive
move date match game concert gig show play film meal dinner lunch breakfast roast
takeaway restaurant hotel kids children child family mum mom dad mother father parent wife
husband partner son daughter sister brother baby toddler grandparents gran grandma
grandad nana dog cat puppy kitten pet rabbit hamster work job business shop team
house home flat garden
allotment course term lesson class school nursery weekend week day night morning
evening church ceremony service birth viewing rehearsal training practice football
rugby
""".split())

NOT_AN_EVENT = frozenset(("fault", "idea", "point", "question", "turn", "problem", "favour"))

HEAVY = frozenset("""
funeral wake scan operation surgery treatment chemo chemotherapy radiotherapy biopsy
results procedure checkup diagnosis
""".split())

HOW = re.compile(
    r"^(?:(?:so|and|ok|okay|well|oh|but|right)[,\s]+)?"
    r"how(?:\s+(?:was|were|is|are|did|does)|'s|s)\s+"
    r"(?:(?P<whose>my|our|his|her|their|the)\s+)?"
    r"(?P<thing>[a-z][a-z' -]{0,30}?)"
    r"(?:\s+(?:go|went|going|doing|then|today|yesterday|tonight|last night|this week))*"
    r"\s*\??$", re.I)
FELT = re.compile(
    r"^(?:(?:so|and|ok|okay|well|oh|but|right)[,\s]+)?"
    r"(?:was|were)\s+(?:it|that|this)\s+"
    r"(?:(?:really|actually|very|too|that|so|pretty)\s+)?"
    r"(?P<word>bad|good|nice|hard|tough|rough|scary|easy|awful|ok|okay|alright|fine|fun|"
    r"horrible|dreadful|painful|tiring|stressful|busy|long|slow|worrying|grim|lovely|great|sunny|warm|cold|wet|windy|hot)"
    r"\s*(?:for\s+(?:you|her|him|them))?\s*[?!.]*$", re.I)

THE_BOT = re.compile(r"(?<![a-z])(?:you|your|yours|yourself|u|ur)(?![a-z])", re.I)
PAST = (
    "You'll have to tell me - I only get what you type. How did it go?",
    "I wasn't there, so you're the one who knows. How did it go?",
    "Nothing of it reached me here, so tell me: how did it go?",
    "You tell me - how did it go? I only get what you type.",
)
STILL_PLURAL = (
    "You'll have to tell me - I only get what you type. How are they doing?",
    "I'm not there for any of it, so you're the one who knows. How are they?",
    "Nothing of that reaches me here. So how are they?",
)
STILL_SINGLE = (
    "You'll have to tell me - I only get what you type. How is it going?",
    "I'm not there for any of it, so you're the one who knows. How is it going?",
    "Nothing of that reaches me here. So how is it going?",
)
CAREFUL = (
    "I only know what you tell me. I hope it went as well as it could - how are you doing now?",
    "Nothing of that reaches me, so I only have what you say. How did it go?",
    "I hope it went as well as it could. Tell me how you are doing with it.",
)
MORE_THAN_ONE = frozenset("""
children kids twins people parents grandparents mumanddad results tests scans appointments
""".split())
SINGULAR_ENDS_IN_S = frozenset("""
business class christmas maths news series gas address boss
""".split())


def a_kind_of_theirs(head):
    if head in THEIRS:
        return True
    for suffix in ("s", "es"):
        if head.endswith(suffix) and head[:-len(suffix)] in THEIRS:
            return True
    return False


def more_than_one(head):
    if head in MORE_THAN_ONE:
        return True
    return head.endswith("s") and head not in SINGULAR_ENDS_IN_S


def _head(thing):
    return thing.split()[-1].strip("'") if thing.split() else ""


def answer_for(text, memory=None):
    line = " ".join((text or "").lower().split()).rstrip(" .!,;:")
    if not line or THE_BOT.search(line):
        return None
    match = HOW.match(line)
    if not match:
        felt = FELT.match(line)
        if felt:
            return pick(list(PAST), memory or {}, line)
        return None
    thing = (match.group("thing") or "").strip()
    whose = (match.group("whose") or "").lower()
    head = _head(thing)
    if not head or head in NOT_AN_EVENT:
        return None
    if whose not in ("my", "our", "his", "her", "their") and not a_kind_of_theirs(head):
        return None
    if head in HEAVY:
        pool = CAREFUL
    elif re.match(r"^(?:(?:so|and|ok|okay|well|oh|but|right)[,\s]+)?"
                  r"how(?:'s|s| is| are)\b", line):
        pool = STILL_PLURAL if more_than_one(head) else STILL_SINGLE
    else:
        pool = PAST
    return pick(list(pool), memory or {}, line)

LEAD = (r"(?:(?:oh|ah|well|actually|honestly|yeah|yep|no|ha|hmm|so|and|but|ok|okay|"
        r"thankfully|happily)[,\s]+)*")
COMPARE = (r"(?:better|worse|easier|harder|nicer|quicker|slower|cheaper|quieter|rougher|"
           r"smoother|calmer|lighter|heavier|longer|shorter|funnier|duller)")
SOFT = r"(?:much|far|a lot|loads|a bit|bit|slightly|definitely|way|even|so much)?\s*"
COPULA = r"(?:(?:it|that|this)(?:'s|s| is| was| went| turned out| feels)?\s+)?"
MINE = r"(?:i|we)"
HOPED = (r"(?:expected|thought|hoped|feared|imagined|dreaded|anticipated|planned|"
         r"was expecting|were expecting|was hoping|were hoping)")
THAN = (r"than\s+(?:" + MINE + r"\s+(?:" + HOPED + r")|last\s+time|yesterday|before|"
        r"the\s+last\s+one|the\s+other\s+one|the\s+first\s+(?:one|time)|the\s+usual|usual|"
        r"(?:the\s+)?(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday|weekend|"
        r"christmas|last\s+year|last\s+week|last\s+month))\b")
COMPARED = re.compile("^" + LEAD + COPULA + SOFT + r"(?P<word>" + COMPARE + r")\s*" + THAN,
                      re.I)
NOT_AS = re.compile("^" + LEAD + COPULA + r"not\s+(?:as|so)\s+"
                    r"(?P<word>good|bad|nice|easy|hard|busy|expensive|cheap|scary|painful)\s+"
                    r"as\s+" + MINE + r"\s+(?:" + HOPED + r")", re.I)
AS_EXPECTED = re.compile("^" + LEAD + r"(?:(?:about|roughly|pretty|more\s+or\s+less)\s+)?"
                         r"(?:as|what)\s+" + MINE + r"\s+expected\b", re.I)
EXPECTED_BARE = re.compile(
    "^" + LEAD + r"(?:(?:pretty|much|about|roughly|more\s+or\s+less)\s+|pretty\s+much\s+)*"
    r"as\s+expected\b", re.I)
WHICH_WAS_THE_AIM = re.compile(
    r"^(?P<what>[a-z][a-z' -]{1,24}?),?\s+which\s+(?:is|was)\s+(?:just\s+)?"
    r"what\s+" + MINE + r"\s+(?:wanted|needed|hoped\s+for|(?:was|were)\s+after)\b", re.I)
NOTHING_WENT_WRONG = re.compile(
    r"\b(?:broke|broken|failed|died|stopped|leaked|flooded|crashed|caught\s+fire|went\s+wrong|"
    r"lost|cancelled|ruined)\b", re.I)
STANDS_ALONE = frozenset("""
it that this not much far way so even still definitely bit slightly honestly actually
well oh ah yeah yep no about roughly pretty as what
""".split())
COMPARE_WORD = re.compile("^(?:" + COMPARE + ")$", re.I)
LEAD_STRIP = re.compile("^" + LEAD)

BETTER = (
    "Good - better than you expected is the best way round for it to go.",
    "That's a nice surprise. What made the difference?",
    "Pleased to hear it. What was better about it than you thought?",
)
WORSE = (
    "Sorry - that's a let-down when you had hoped for more.",
    "Ah, I'm sorry. What was off about it?",
    "That's a shame. Do you know what changed?",
)
RELIEF = (
    "That's a relief, then. What was it actually like?",
    "Good - the dread is usually worse than the thing itself.",
    "Pleased it was not the ordeal you had braced for.",
)
NO_SURPRISES = (
    "No surprises then. Is there anything you would do differently next time?",
    "Fair enough - it did what you expected of it.",
    "So it went the way you thought it would. Nothing to fix.",
)
WANTED_IT = (
    "Good - {0} is exactly what you were after.",
    "That's the good kind of {0}. Pleased it landed that way.",
    "{0} was the point of it, so that counts as a good one.",
)
LOW = frozenset("worse harder rougher busier heavier longer slower duller".split())
NOT_SO_BAD = frozenset("bad hard busy expensive scary painful".split())


def _opens_on_the_comparison(line):
    rest = LEAD_STRIP.sub("", line)
    first = rest.split()[0] if rest.split() else ""
    return first in STANDS_ALONE or bool(COMPARE_WORD.match(first))


def the_answer_they_gave(text, memory=None):
    line = " ".join((text or "").lower().split()).rstrip(" .!,;:")
    if not line or "?" in line or THE_BOT.search(line):
        return None
    if len(line.split()) > 9:
        return None
    aim = WHICH_WAS_THE_AIM.match(line)
    if aim:
        what = aim.group("what").strip()
        for lead in ("it was ", "it is ", "that was ", "this was "):
            if what.startswith(lead):
                what = what[len(lead):]
        if not what or NOTHING_WENT_WRONG.search(what) or len(what.split()) > 3:
            return None
        return pick([line.format(what) for line in WANTED_IT], memory or {}, line)
    if not _opens_on_the_comparison(line):
        return None
    match = COMPARED.search(line)
    not_as = NOT_AS.search(line)
    if match:
        pool = WORSE if match.group("word").lower() in LOW else BETTER
    elif not_as:
        pool = RELIEF if not_as.group("word").lower() in NOT_SO_BAD else WORSE
    elif AS_EXPECTED.search(line) or EXPECTED_BARE.search(line):
        pool = NO_SURPRISES
    else:
        return None
    return pick(list(pool), memory or {}, line)
