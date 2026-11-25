import re

from ..compose import fallback
from . import greeting

PRIORITY = -500

JUDGE_PEOPLE_ASK = re.compile(
    r"\b(?:will|would|do|did|are|r|can|could)\s+(?:you|u)\s+"
    r"(?:just\s+|really\s+|actually\s+|even\s+|ever\s+|not\s+)?judg\w*\s+"
    r"(?:(?:a|the|other)\s+)?"
    r"(?:people|person|persons|someone|somebody|anyone|anybody|folk|folks|others|them|him|her)"
    r"\b"
    r"|\b(?:dont|do not|never)\s+judg\w*\s+"
    r"(?:(?:a|the|other)\s+)?(?:people|anyone|anybody|someone|somebody|person|folk|folks)\b",
    re.I)

JUDGE_A_THING_NOT_PEOPLE = re.compile(
    r"\bjudg\w*\s+(?:the|this|that|it|my|his|its)\b"
    r"|\bjudg\w*\s+(?:a|an)\s+(?!person\b|people\b|human\b|child\b|kid\b|man\b|woman\b"
    r"|guy\b|girl\b|boy\b|teen\w*\b)\w+",
    re.I)
JUDGE_BY_A_STANDARD = re.compile(r"\bjudg(?:ing|ed)\s+(?:by|on|from)\b", re.I)

JUDGE_SOMEONE_ELSE = re.compile(
    r"\b(?:everyone|everybody|people|they|them|someone|somebody|nobody|no one|parents|friends|"
    r"family|colleagues|strangers|relatives|neighbours)\b(?:\s+\w+){0,3}\s+judg\w*"
    r"|\b(?:my|his|her|their|our|your)\s+(?:\w+\s+){0,2}judg\w*"
    r"|\b(?:she|he|they|it|shell|hell|theyll|theyd|shed|shes|hes)\b(?:\s+\w+){0,3}\s+judg\w*"
    r"|\b(?:the|a|my|his|her|our|their|your)\s+(?:\w+\s+){0,2}to\s+judg\w*\s+(?:me|us)\b",
    re.I)

PEOPLE_LINES = (
    "I try not to. Nobody gets a verdict off me - what people tell me stays here. What's on your "
    "mind?",
    "No. I've no interest in scoring people - say whatever you came to say.",
    "I don't, no. Whatever you tell me I take as it comes, so where are we starting?",
)

EMPTY_HEADS = (
    "got it", "noted:", "thanks for telling me", "i'm listening", "i am listening",
    "that's your call", "that sounds like a lot", "sorry, i don't know", "i don't know enough",
)


def _says_nothing(said):
    said = str(said or "")
    if not said:
        return True
    if fallback._is_a_hedge(said):
        return True
    return said.lower().startswith(EMPTY_HEADS)


def _the_composer_says_nothing(text, memory):
    for reply in (greeting.respond(text, memory), fallback.reply_for(text, memory)):
        if reply and not _says_nothing(reply):
            return False
    return True


def reads_it(text):
    said = " ".join(str(text or "").lower().split())
    if not said:
        return False
    if not JUDGE_PEOPLE_ASK.search(said):
        return False
    return not (JUDGE_A_THING_NOT_PEOPLE.search(said) or JUDGE_BY_A_STANDARD.search(said)
                or JUDGE_SOMEONE_ELSE.search(said))


def respond(text, memory):
    if not reads_it(text):
        return None
    if not _the_composer_says_nothing(text, memory):
        return None
    turns = (memory or {}).get("turns") or []
    last = str(turns[-1].get("bot") or "") if turns else ""
    start = sum(ord(ch) for ch in " ".join(str(text or "").lower().split()))
    for step in range(len(PEOPLE_LINES)):
        line = PEOPLE_LINES[(start + step) % len(PEOPLE_LINES)]
        if not last or line[:24] not in last:
            return line
    return PEOPLE_LINES[start % len(PEOPLE_LINES)]
