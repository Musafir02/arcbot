import re

A_STRONG_STATE = re.compile(
    r"\b(?:drunk|drunken|pissed(?!\s+off)|plastered|bladdered|trolleyed|mullered|mangled|"
    r"sozzled|paralytic|off\s+(?:my|his|her|their|our)\s+(?:face|head|tits)|"
    r"on\s+the\s+lash|bender|"
    r"(?:a\s+)?few\s+too\s+many|one\s+too\s+many|too\s+much\s+(?:to\s+drink|wine|beer|lager|booze)|"
    r"too\s+much\s+last\s+night|heavy\s+night|big\s+night)\b", re.I)
A_WEAK_STATE = re.compile(
    r"\b(?:wasted|smashed|steaming|tipsy|boozy|lash|binge|bendered|drank|"
    r"hammered|leathered|wrecked|half\s+cut|"
    r"been\s+drinking|was\s+drinking|were\s+drinking)\b", re.I)
A_TIME_THAT_HAS_GONE = re.compile(
    r"\b(?:last\s+night|last\s+evening|yesterday|the\s+night\s+before|all\s+night|overnight|"
    r"this\s+morning|woke\s+up|till\s+\d|til\s+\d|until\s+\d|"
    r"(?:fri|satur|sun)day\s+night|at\s+the\s+weekend|night\s+out|"
    r"at\s+the\s+(?:party|pub|club|do|wedding|works\s+do|leaving\s+do)|at\s+a\s+party|"
    r"on\s+a\s+night\s+out)\b", re.I)
A_HANGOVER = re.compile(r"\b(?:hung\s?over|hangover|hanging|woke\s+up\s+rough|"
                        r"rough\s+as\s+a\s+badger)\b", re.I)
A_MORNING = re.compile(r"\b(?:this\s+morning|today|now|after\s+last\s+night)\b", re.I)
A_CONSEQUENCE = re.compile(
    r"\b(?:said|saying|told|texted|messaged|rang|rung|called|drove|drive|drove\s+home|hit|"
    r"shouted|argued|arguing|kissed|cheated|spent|ruined|broke|broke\s+up|fell|fall|"
    r"lost\s+my|got\s+in\s+a\s+fight|fight)\b", re.I)
A_STILL_TO_COME = re.compile(
    r"\b(?:tonight|tomorrow|next\s+(?:week|weekend|month|year)|going\s+to|gonna|"
    r"this\s+weekend|on\s+friday|on\s+saturday)\b", re.I)
SOMEONE_ELSE = re.compile(
    r"\b(?:hes|shes|theyre)\b|"
    r"\b(?:my|our|his|her|their|he|she|they|we|us)\s+(?:\w+\s+){0,2}?"
    r"(?:was|were|got|gets|get|is|are|had|has|keeps?|been)\b", re.I)
AN_EMERGENCY = re.compile(
    r"\b(?:ambulance|999|911|111|hospital|a\s?&?\s?e\b|passed\s+out|passing\s+out|"
    r"blacked\s+out|blackout|can'?t\s+wake|not\s+breathing|stopped\s+breathing|"
    r"alcohol\s+poisoning|overdose|overdosed|choking|seizure|collapsed|unconscious)\b", re.I)
A_QUESTION_ABOUT_IT = re.compile(
    r"\b(?:should|shall|could|how\s+do|how\s+can|how\s+to|what\s+should|any\s+tips|advice|"
    r"stop\s+drinking|give\s+up|cut\s+down|cutting\s+down|quitting|quitting|help)\b", re.I)

A_MORNING_AFTER = (
    "Ha - how is your head today?",
    "Water, something plain to eat and an early night is most of the cure. How is today going?",
    "That is a long night. Are you feeling it today, or did you get away with it?",
    "How are you this morning? A pint of water, food and time, in that order.",
    "How bad is it - banging head, or just tired and skint?",
    "That sounds like one of those nights. Are you able to take it easy today?",
    "Right. How are you feeling now?",
)


def reads_as_a_morning_after(clean):
    if not clean:
        return False
    if AN_EMERGENCY.search(clean) or A_QUESTION_ABOUT_IT.search(clean):
        return False
    if A_CONSEQUENCE.search(clean):
        return False
    gone = A_TIME_THAT_HAS_GONE.search(clean)
    strong = A_STRONG_STATE.search(clean)
    weak = A_WEAK_STATE.search(clean) if gone else None
    hangover = A_HANGOVER.search(clean) if A_MORNING.search(clean) else None
    said = strong or weak or hangover
    if not said:
        return False
    if SOMEONE_ELSE.search(clean[:said.start()]):
        return False
    if not gone and A_STILL_TO_COME.search(clean):
        return False
    return True
