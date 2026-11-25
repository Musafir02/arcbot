import re

from . import pick

BARE_DOUBT = re.compile(
    r"^(?:and |so |but |ok |okay |oh |right |hmm )*"
    r"(?:(?:is|was|are|were|does|do|did) (?:that|this|it)(?: all)?"
    r"(?: (?:really|actually|very|too|that|so))?"
    r"(?: (?:bad|normal|serious|dangerous|ok|okay|fine|safe|good|alright|"
    r"a lot|too much|too often|too many|enough|much of a problem|a problem|"
    r"something to worry about|anything to worry about))"
    r"|(?:should|do|ought) i (?:be )?(?:worried|worry|worrying|bothered)"
    r"|am i (?:ok|okay|alright|all right|normal|right))"
    r"(?: then| though| honestly| here)?$")

QUANTITY_ASK = re.compile(r"\b(?:enough|a lot|too much|too many|too often)\b")

CALL_MADE = (
    r"(?:get (?:it|that|them|yourself) (?:checked|looked at|seen)|get (?:an|a) "
    r"(?:appointment|referral)|see (?:a|your|the) (?:gp|doctor|nurse|dentist|optician|physio)|"
    r"ring (?:999|911|112|111|your gp|the gp|the surgery)|call (?:999|911|112|111)|"
    r"go to (?:a&e|the hospital|a walk-in|minor injuries)|book (?:an appointment|a gp)|"
    r"photograph it|have it looked at)")
CARE_NAMED = re.compile(r"(?:^|[.!?]\s+)(?:then |also |first )?" + CALL_MADE, re.I)

SOMEBODY_TOLD_THEM = re.compile(
    r"\b(?:gp|doctor|doctors|pharmacist|chemist|nurse|practice|surgery|dentist|optician|"
    r"physio|physiotherapist|midwife|health visitor|consultant|vet|vets|111|a&e|hospital|"
    r"walk-in|paramedic|ambulance)\b", re.I)
TOLD = re.compile(
    r"\b(?:said|says|say|told|tells|tell|advised|advises|wants|wanted|reckons|thinks|"
    r"suggested|recommended|sent me|referred|booked|making me|making me go|insisted)\b", re.I)

CARE_LINES = (
    "Yes - worth getting seen rather than waiting on.",
    "Yes, get it seen. Asking is not fussing.",
    "Yes - that is a call worth making, not an overreaction.",
)

NOT_READ_BACK = frozenset(("safety", "urgent", "grief", "loss"))


def _last_bot(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return "", ""
    for turn in reversed(turns):
        if not isinstance(turn, dict):
            continue
        text = str(turn.get("bot") or "")
        if text:
            return text, str(turn.get("module") or "")
    return "", ""


def reads_as_a_doubt(clean):
    flat = re.sub(r"[^a-z0-9 ]+", " ", str(clean or "").lower())
    flat = re.sub(r"\s+", " ", flat).strip()
    return bool(flat) and BARE_DOUBT.match(flat) is not None


def _the_line_behind(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return ""
    for turn in reversed(turns):
        if not isinstance(turn, dict):
            continue
        if str(turn.get("bot") or ""):
            return str(turn.get("user") or "").lower()
    return ""


def reply_for(clean, memory):
    if not reads_as_a_doubt(clean):
        return None
    if QUANTITY_ASK.search(str(clean or "").lower()):
        return None
    said, module = _last_bot(memory)
    if not said or module in NOT_READ_BACK:
        return None
    if not CARE_NAMED.search(said):
        return None
    behind = _the_line_behind(memory)
    if not (SOMEBODY_TOLD_THEM.search(behind) and TOLD.search(behind)):
        return None
    return pick(CARE_LINES, memory, clean)
