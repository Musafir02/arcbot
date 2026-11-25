import re

from ..compose import pick

_LEAD = (
    r"^\s*(?:(?:oh|aw+|ah|ha+|hi|hey|tbh|honestly|ok|okay|well|and|but|so|yeah|anyway|"
    r"still|currently|right now|not much|nm|just|im|i'm|iam|i am)[,\s]+)*"
)
_TAIL = (
    r"(?:\s+(?:today|tonight|now|at the moment|right now|lately|this morning|this afternoon|"
    r"this evening|lol|ha+|haha|tbh|honestly))*"
)
_END = r"\s*(?:[.!]+|lol|ha+|haha|tbh|honestly)*\s*$"

_WAITING = re.compile(
    _LEAD + r"(?:"
    r"wait(?:ing)? (?:at|for|in|on) \w+(?: \w+){0,3}"
    r"|wait(?:ing)? in (?:a|the) (?:queue|line|waiting room)"
    r"|in (?:a|the) (?:queue|line|waiting room)(?: (?:at|for) \w+(?: \w+){0,3})?"
    r"|queu(?:e|ing) (?:at|for) \w+(?: \w+){0,2}"
    r"|on hold(?: with \w+(?: \w+)?)?"
    r")" + _TAIL + _END, re.I)

_MOVING = re.compile(
    _LEAD + r"(?:"
    r"on (?:the|a|my) (?:bus|train|tube|tram|coach|ferry|plane|flight|boat)"
    r"|on (?:the|a) (?:bus|train|tube|tram) (?:home|in|back|to \w+(?: \w+)?)"
    r"|on my way (?:home|in|back|there|to \w+(?: \w+)?)"
    r")" + _TAIL + _END, re.I)

_IN_THE_CAR = re.compile(
    _LEAD + r"(?:in (?:the|my) car|driving(?: (?:home|back|up|down|to \w+(?: \w+)?))?"
    r"|on the motorway(?: to \w+(?: \w+)?)?|stuck in traffic)"
    + _TAIL + _END, re.I)

_SLOW = re.compile(
    _LEAD + r"(?:"
    r"hav(?:e|ing) (?:a|an) (?:lazy|quiet|slow|cosy|couch|pyjama|relaxing|easy|chill) "
    r"(?:one|day|morning|afternoon|evening|night|sunday|weekend)"
    r"|(?:it'?s|its)(?: been)?(?: a)?(?: (?:really|very|proper|nice|lovely))? "
    r"(?:lazy|quiet|slow|cosy|relaxing|easy) (?:one|day|morning|afternoon|evening|sunday)"
    r"|(?:lazy|quiet|slow|chilled) day(?: (?:today|here|at work|so far))?"
    r"|nothing much (?:on|planned|doing)(?: (?:today|here|planned))?"
    r"|not much (?:on|planned)(?: (?:today|here))?"
    r"|nothing on (?:today|this afternoon|this morning)"
    r"|(?:took|taking|having) (?:the|a|my) day off(?: work)?(?: today)?"
    r")" + _TAIL + _END, re.I)

_IN_BED = re.compile(
    _LEAD + r"(?:"
    r"(?:still |back |lying |sat |sitting |laying )?in bed"
    r"|(?:lying|laying|sat|sitting) in bed"
    r"|back to bed"
    r")" + _TAIL + _END, re.I)

_SOFA = re.compile(
    _LEAD + r"(?:"
    r"(?:lying|sat|sitting|slouched|curled up) on the (?:sofa|settee|couch)"
    r"|curled up (?:with a book|in front of the tv)"
    r"|having (?:a|another) (?:cup of tea|brew|cuppa|coffee)"
    r"|chill(?:ing|in)(?: out)?(?: (?:now|at home))?"
    r"|taking it easy"
    r")" + _TAIL + _END, re.I)

_ON_A_BREAK = re.compile(
    _LEAD + r"(?:"
    r"on (?:my|a|the) (?:lunch|dinner|tea|coffee) ?(?:break|hour)"
    r"|on (?:my|a) break"
    r"|taking (?:a|my) (?:lunch )?break"
    r")" + _TAIL + _END, re.I)

_AT_WORK = re.compile(
    _LEAD + r"(?:"
    r"(?:at|back at) (?:work|the office)|in (?:the )?office|at (?:my|the) desk"
    r"|on (?:shift|shifts|nights|days|the clock)|working"
    r")" + _TAIL + _END, re.I)


_AT_THE_GYM = re.compile(
    _LEAD + r"(?:"
    r"(?:at|in) the gym|working out|lifting|lifting weights|on the treadmill"
    r"|doing (?:a|my) (?:workout|session|class)"
    r")" + _TAIL + _END, re.I)

_AT_A_DOCTOR = re.compile(
    _LEAD + r"(?:"
    r"(?:at|in|outside) (?:the |a )?(?:hospital|a&e|ae|casualty|clinic|surgery|doctors|"
    r"doctor's|gp|dentist|orthodontist|pharmacy|chemist|walk in centre)"
    r"|at the doctors waiting"
    r")" + _TAIL + _END, re.I)

_AT_A_PLACE = re.compile(
    _LEAD + r"(?:"
    r"(?:at|over at|down at|round at|up at|outside|near) (?:the |a |my |our |me )?[a-z][\w'&]*(?: [a-z][\w'&]*){0,2}"
    r"|at home"
    r")" + _TAIL + _END, re.I)
_NOT_A_PLACE = re.compile(
    r"\b(?:limit|limits|loss|a loss|breaking point|end of my tether|wits end|wit's end|fault|"
    r"risk|peace|war|odds|best|worst|least|most|first|last|standstill|stretch|push|glance|"
    r"crossroads|disadvantage|loggerheads|pains|ease|large|hand|that age|my age|this|that|it|"
    r"stage|point|end|end of my rope|loose end|again|once|twice|"
    r"funeral|wake|christening)\b", re.I)

WAITING_REPLIES = (
    "Queues are the worst of it. This is as good a way to spend one as any.",
    "Nothing to do but wait, then. What are you waiting on?",
    "That kind of wait always runs longer than they tell you. Hope it moves.",
    "Hope it goes quickly. I'm here if you want company while it does.",
)
MOVING_REPLIES = (
    "A journey is a good place for a chat. What's on your mind?",
    "Nothing like a ride for thinking things through. Ask away.",
    "Journeys are mostly waiting with a view. Where are you off to?",
    "Mind how you go - I'll be here when you get there.",
)
IN_THE_CAR_REPLIES = (
    "Eyes on the road - I'll be here when you stop.",
    "No reading and driving. Park up and I'll answer anything you like.",
    "I'll keep. Get where you're going first, then ask me whatever it is.",
)
SLOW_REPLIES = (
    "Then take it slow. That is what those days are for.",
    "A lazy day with nothing in it is a good day. Enjoy it.",
    "A slow one can be a good one. What would make it better?",
    "Quiet days are underrated. I'm here if you want something to fill it.",
)
IN_BED_REPLIES = (
    "No rush to get up. What is the rest of the day looking like?",
    "Enjoy the duvet. Anything on your mind?",
    "A warm bed and nowhere to be. Fair enough.",
    "Five more minutes is always the right answer. I'm here when you're up.",
)
SOFA_REPLIES = (
    "That sounds like the right place to be. I'm here when you want something.",
    "Nothing wrong with taking it easy. Ask away if something comes up.",
    "Comfortable, then. Anything you want a hand with while you're there?",
    "A slow afternoon done properly. What are you thinking about?",
)
BREAK_REPLIES = (
    "Break earned. What are you doing with it?",
    "Enjoy it \u2014 half an hour goes faster than you think.",
    "A proper break, then. Anything you want a second opinion on?",
)
AT_WORK_REPLIES = (
    "Work can wait for this. What is it?",
    "Right, you're on the clock. What do you need?",
    "Go on \u2014 I'll keep it short.",
)
AT_THE_GYM_REPLIES = (
    "Good stuff. Cardio or the weights?",
    "Nice. What are you working on today?",
    "Go on then \u2014 what do you need between sets?",
    "Better than sitting down. What's the question?",
)
AT_A_DOCTOR_REPLIES = (
    "Waiting rooms are the worst of it. What do you need while you're there?",
    "That's a long morning whatever it's for. How long have you been there?",
    "Hope it goes quickly. What's on your mind?",
    "Hospital or not, I'm here. What do you need?",
)
AT_A_PLACE_REPLIES = (
    "What are you up to there?",
    "Noted \u2014 what do you need while you're there?",
    "Right you are. Anything you want a second opinion on?",
    "I'll let you get on. What's on your mind?",
)


_HEAVY = re.compile(
    r"\b(?:died|dying|death|funeral|passed away|kill myself|killing myself|suicide|suicidal|"
    r"end it all|take my own life|hurt myself|hurting myself|self harm|self-harm|cut myself|"
    r"overdose|miscarriage|stillborn|terminal|beat me|beats me|hit me|hits me|hurts me|"
    r"hurting me|threatened me|abused? me|assaulted|not safe|scared of|afraid of|"
    r"can'?t stop crying|can not stop crying|crying|in tears|so upset|upset about|devastated|"
    r"heartbroken|at the end of my tether)\b", re.I)


A_STRETCH_OF_TIME = re.compile(
    r"\b(?:all|every|each|most|whole) (?:day|days|week|weeks|night|nights|morning|evening|"
    r"time|summer|winter|year)|these days|most days|all the time|\d+ (?:days|weeks|hours) a week\b",
    re.I)

A_DAY_TO_COME = re.compile(
    r"\b(?:tomorrow|next (?:week|month|year|monday|tuesday|wednesday|thursday|friday|"
    r"saturday|sunday)|on (?:monday|tuesday|wednesday|thursday|friday|saturday|sunday))\b",
    re.I)


def _the_chat_is_heavy(memory):
    turns = (memory or {}).get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return False
    earlier = [turn for turn in turns if isinstance(turn, dict)
               and str(turn.get("user", "")).strip()]
    for turn in earlier[-2:]:
        if _HEAVY.search(" ".join(str(turn["user"]).split())):
            return True
    return False


def reply(text, memory):
    clean = " ".join(str(text or "").replace("\u2019", "'").split())
    if not clean or len(clean.split()) > 9:
        return None
    if _the_chat_is_heavy(memory):
        return None
    if A_STRETCH_OF_TIME.search(clean) or A_DAY_TO_COME.search(clean):
        return None
    seed = str(text or "")
    if _ON_A_BREAK.match(clean):
        return pick(BREAK_REPLIES, memory, seed_text=seed)
    if _WAITING.match(clean):
        return pick(WAITING_REPLIES, memory, seed_text=seed)
    if _IN_THE_CAR.match(clean):
        return pick(IN_THE_CAR_REPLIES, memory, seed_text=seed)
    if _MOVING.match(clean):
        return pick(MOVING_REPLIES, memory, seed_text=seed)
    if _IN_BED.match(clean):
        return pick(IN_BED_REPLIES, memory, seed_text=seed)
    if _SOFA.match(clean):
        return pick(SOFA_REPLIES, memory, seed_text=seed)
    if _SLOW.match(clean):
        return pick(SLOW_REPLIES, memory, seed_text=seed)
    if _AT_WORK.match(clean):
        return pick(AT_WORK_REPLIES, memory, seed_text=seed)
    if _AT_THE_GYM.match(clean):
        return pick(AT_THE_GYM_REPLIES, memory, seed_text=seed)
    if _AT_A_DOCTOR.match(clean):
        return pick(AT_A_DOCTOR_REPLIES, memory, seed_text=seed)
    if _AT_A_PLACE.match(clean) and not _NOT_A_PLACE.search(clean):
        return pick(AT_A_PLACE_REPLIES, memory, seed_text=seed)
    return None
