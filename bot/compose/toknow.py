import re

from . import pick

A_WHAT_TO_KNOW_ASKED = re.compile(
    r"\b(?:anything|something|everything|nothing|what)"
    r"(?:\s+else)?\s+(?:that\s+)?(?:i|we|you)\s+(?:should|ought to|need to|have to|must)\s+know\b"
    r"|\b(?:is|are) there (?:anything|something|much)\b[^?.!]{0,25}\b(?:i|we)\s+know\b"
    r"|\bwhat\s+(?:should|do|would)\s+(?:i|we)\s+know\b", re.I)

A_THING_YOU_AGREE_TO = re.compile(
    r"\b(?:job|jobs|role|position|post|offer|contract|permanent|probation|shift|rota|hours|pay|"
    r"salary|apprenticeship|placement|course|uni|university|college|degree|tenancy|lease|landlord|"
    r"flat|house|mortgage|rent|deposit|move|mover|buying|purchase|loan|credit|insurance|policy|"
    r"car|van|bike|warranty|gym|membership|subscription|phone contract|broadband|nursery|"
    r"childcare|school place|deal|signing|sign|agreement|terms)\b", re.I)

BEFORE_YOU_AGREE = (
    "The things people are glad they checked are the money after the first month, what it commits "
    "you to, and how you get out of it - and all three are written down somewhere before you agree "
    "to anything. Which of those is the one you are unsure about?",
    "It is nearly always the small print that decides it: what it costs over time, what you can "
    "and cannot do, and the notice you have to give. Do you have the paperwork in front of you?",
    "Ask what happens if it goes wrong, because that is the part nobody mentions until it has. "
    "What is the thing you would be agreeing to?",
)

WHAT_TO_KNOW_FIRST = (
    "Tell me the part you want to get right about {thing} and I will tell you what I know. The "
    "general rule is that what you want from it and the one limit you cannot move decide "
    "everything else, and the details sit on the official page for it. Which part is it?",
    "What I can be useful on is the part you are unsure about, rather than a list: say which bit "
    "of {thing} you are weighing and I will take it from there. What is worrying you?",
)

WHAT_THE_BOT_CAN_SAY_ABOUT_IT = ("what do you know about {}", "is {} worth it", "tell me about {}")

A_PRONOUN_NOT_A_THING = re.compile(
    r"^(?:it|this|that|them|those|these|him|her|me|us|you|one|ones|things|stuff)\b", re.I)
THE_WORDS_THAT_END_THE_THING = re.compile(
    r"\b(?:before|after|when|if|so|and|but|because|or|for|with|to|in|on|at|from)\b", re.I)
A_FEW_WORDS_OF_THING = 5


def _the_thing_asked_about(clean):
    match = re.search(r"\bknow\b[^?.!]{0,10}?\babout\b\s*([^?.!]{1,60})", clean, re.I)
    if not match:
        match = re.search(r"\babout\b\s*([^?.!]{1,60})\b(?:before|first)\b", clean, re.I)
    if not match:
        return ""
    thing = match.group(1).strip(" ?.!,")
    cut = THE_WORDS_THAT_END_THE_THING.search(thing)
    if cut:
        thing = thing[:cut.start()].strip(" ?.!,")
    if not thing or A_PRONOUN_NOT_A_THING.match(thing):
        return ""
    if len(thing.split()) > A_FEW_WORDS_OF_THING:
        return ""
    return thing


def _a_card_about(thing):
    try:
        from ..modules import answers
    except Exception:
        return ""
    for frame in WHAT_THE_BOT_CAN_SAY_ABOUT_IT:
        try:
            said = answers.respond(frame.format(thing), {})
        except Exception:
            said = None
        if said:
            return said
    return ""


def ask_about_what_to_look_out_for(clean, memory=None):
    said = " ".join((clean or "").lower().split())
    if not said or not A_WHAT_TO_KNOW_ASKED.search(said):
        return None
    if A_THING_YOU_AGREE_TO.search(said):
        return pick(BEFORE_YOU_AGREE, memory, said) or ""
    asked_about = _the_thing_asked_about(said)
    if not asked_about:
        return ""
    card = _a_card_about(asked_about)
    if card:
        return card
    shaped = pick(WHAT_TO_KNOW_FIRST, memory, said)
    if shaped:
        return shaped.replace("{thing}", asked_about)
    return ""
