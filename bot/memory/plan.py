import copy
import re

from ..compose import pick
from . import repeat

CARRY_ON = re.compile(
    r"^(?:(?:ok|okay|right|so|yeah|yes|alright|and|then|well|ah)\s+)*"
    r"(?:and\s+then|then\s+what|what\s+next|what\s+now|next|and\s+after\s+that|after\s+that|"
    r"and\s+next|go\s+on|carry\s+on|keep\s+going)\s*[.?!]*$", re.I)

FIRST_LEADS = (
    "Start with this: {step}.",
    "Begin here: {step}.",
    "The thing to do first: {step}.",
    "Do this bit first: {step}.",
)

AMOUNTS_LEADS = (
    "First up: {step}.",
    "Begin with the mix: {step}.",
    "Start with what goes in: {step}.",
)

_OPENS_ON_THE_INSTRUCTION = re.compile(
    r"^(?:start(?:\s+(?:with|by|off))?|begin(?:\s+(?:with|by))?|first(?:ly)?|to\s+start|"
    r"the\s+first\s+thing)\b(?:[,:]|\s)", re.I)

_COUNTS = {2: "I make it two steps.", 3: "I make it three steps.",
           4: "I make it four steps.", 5: "I make it five steps."}

LEADS = (
    "Next: {step}.",
    "Then: {step}.",
    "The next bit: {step}.",
    "Once that is done: {step}.",
    "The step after that: {step}.",
)

DONE = (
    "There is nothing after that bit that I can pick out. The last of it is: {step}. Where have "
    "you got to?",
    "That is the last step I can pick out of it: {step}. Say where you are and I'll help with the "
    "rest.",
    "I have nothing more to hand you after: {step}. Tell me which bit you are on.",
)

FINISHED = (
    "That is every step I can pick out of it - nothing left of what I can hand you. Tell me how it "
    "went.",
    "There is nothing after that I can pick out. Say what happened and we will go from there.",
    "Nothing more I can pull out of that answer. How did it go?",
)

NOT_A_JOB = ("loss", "grief", "safety")

WHILE_IT_LASTS = 3

_NOT_THE_THING = {"take", "have", "with", "that", "this", "what", "when", "them", "they", "your",
                  "from", "into", "just", "like", "some", "then", "than", "also", "once", "done",
                  "make", "over", "will", "back", "again", "away", "each", "every", "about",
                  "after", "before", "under", "while", "there", "here", "been", "being"}


_HAD_A_GO = re.compile(r"\b(?:tried|trying|already|gave it|had a go|no luck|used)\b", re.I)


def _the_thing_named(text):
    return {word for word in re.findall(r"[a-z']+", str(text or "").lower())
            if len(word) > 3 and word not in _NOT_THE_THING}


def _tried(step, memory):
    mine = _the_thing_named(step)
    if not mine:
        return False
    for turn in (memory.get("turns") or [])[-3:]:
        if not isinstance(turn, dict):
            continue
        line = str(turn.get("user") or "")
        if not _HAD_A_GO.search(line):
            continue
        if mine & _the_thing_named(line):
            return True
    return False


def the_last_answer(memory):
    for turn in reversed((memory or {}).get("turns") or []):
        if isinstance(turn, dict) and turn.get("bot"):
            return str(turn["bot"])
    return ""


def the_answer_in_hand(memory):
    plan = (memory or {}).get("steps") if isinstance(memory, dict) else None
    if not isinstance(plan, dict):
        return ""
    answer = str(plan.get("answer") or "").strip()
    if not answer:
        return ""
    last = " ".join(the_last_answer(memory).split()).strip()
    if not last:
        return ""
    if last == " ".join(str(plan.get("said") or "").split()).strip():
        return answer
    return answer if _our_own_line(last, plan) else ""


def _module_of_last(memory):
    for turn in reversed((memory or {}).get("turns") or []):
        if isinstance(turn, dict) and turn.get("bot"):
            return str(turn.get("module") or "")
    return ""


def _last_user(memory):
    for turn in reversed((memory or {}).get("turns") or []):
        if isinstance(turn, dict) and turn.get("user"):
            return str(turn["user"])
    return ""


def _a_cut_at_a_colon(step):
    head, sep, tail = step.partition(": ")
    if sep and len(tail.split()) < 5:
        return head.strip()
    return step


def steps_of(answer):
    steps = [step for step in (_a_cut_at_a_colon(step) for step in repeat._the_steps(answer))
             if step]
    steps = _the_amounts_first(answer, steps)
    if len(steps) < 2:
        return []
    return steps


AMOUNTS = re.compile(r"\b\d+(?:\.\d+)?\s*(?:g|kg|ml|l|oz|lb|tsp|tbsp|teaspoons?|tablespoons?)\b",
                     re.I)


def _the_amounts_first(answer, steps):
    first = repeat.SENTENCE.split(str(answer or "").strip())[0].strip()
    if not first or len(AMOUNTS.findall(first)) < 2:
        return steps
    if not re.search(r"\b[a-z]{3,}ed\b", first.lower()):
        return steps
    if steps and steps[0].lower()[:40] in first.lower():
        return steps
    return [first.rstrip(".")] + list(steps)


def _words(text):
    return {word for word in re.findall(r"[a-z']+", str(text or "").lower()) if len(word) > 3}


def _stems(text):
    return {word[:5] for word in re.findall(r"[a-z']{4,}", str(text or "").lower())}


def _the_same_job(answer, plan):
    said = _words(answer)
    if not said:
        return False
    for step in plan.get("steps") or []:
        if _words(step) & said:
            return True
    return False


def _the_same_topic(memory, plan):
    here = _stems(_last_user(memory)) | _stems(the_last_answer(memory))
    if not here:
        return False
    about = set()
    for step in plan.get("steps") or []:
        about |= _stems(step)
    topic = plan.get("topic")
    about |= _stems(topic.get("text") if isinstance(topic, dict) else "")
    return bool(here & about)


def _said_in(answer, plan):
    said = _words(answer)
    if not said:
        return 0
    reached = 0
    for at, step in enumerate(plan.get("steps") or []):
        if _words(step) & said:
            reached = at + 1
    return reached


def _our_own_line(answer, plan):
    said = " ".join(str(answer or "").split()).strip()
    if not said:
        return False
    for step in plan.get("steps") or []:
        flat = " ".join(step.split())
        if flat and flat.lower() in said.lower():
            return True
    return False


def _plan_for(memory):
    answer = the_last_answer(memory)
    plan = memory.get("steps") if isinstance(memory, dict) else None
    if isinstance(plan, dict) and plan.get("steps"):
        if plan.get("answer") == answer or plan.get("said") == answer:
            return plan
        if _our_own_line(answer, plan):
            plan["answer"] = answer
            plan["at"] = max(plan.get("at") or 0, _said_in(answer, plan))
            return plan
        turns = len((memory or {}).get("turns") or [])
        fresh = steps_of(answer)
        if (not fresh or fresh == plan.get("steps")) \
                and turns - (plan.get("turn") or 0) < WHILE_IT_LASTS \
                and (_the_same_topic(memory, plan) or _the_same_job(answer, plan)):
            plan["answer"] = answer
            plan["at"] = max(plan.get("at") or 0, _said_in(answer, plan))
            return plan
    if _module_of_last(memory) in NOT_A_JOB:
        return None
    steps = steps_of(answer)
    if not steps:
        return None
    return {"answer": answer, "steps": steps, "at": 0,
            "turn": len((memory or {}).get("turns") or []),
            "topic": copy.deepcopy(memory.get("topic")) if isinstance(memory.get("topic"), dict)
            else None}


def carry_on(text, memory):
    line = str(text or "").strip()
    if not line or not isinstance(memory, dict):
        return None
    if not CARRY_ON.match(line):
        return None
    plan = _plan_for(memory)
    if plan is None:
        return None
    here = len(memory.get("turns") or [])
    if plan.get("at_turn") == here and plan.get("said"):
        return plan["said"]
    steps = plan["steps"]
    at = plan.get("at") or 0
    while at < len(steps) and _tried(steps[at], memory):
        at += 1
    if at >= len(steps):
        last = steps[-1]
        if plan.get("done"):
            said = pick(FINISHED, memory, line)
        else:
            said = pick(DONE, memory, line).format(
                step=last[0].lower() + last[1:])
        _record(memory, plan.get("answer") or "", steps, at, said)
        memory["steps"]["done"] = True
        return said
    step = steps[at]
    if _OPENS_ON_THE_INSTRUCTION.match(step):
        said = step[0].upper() + step[1:]
        if not said.endswith((".", "!", "?")):
            said += "."
    elif at == 0:
        leads = AMOUNTS_LEADS if AMOUNTS.match(step) else FIRST_LEADS
        said = pick(leads, memory, line).format(step=step[0].upper() + step[1:])
    else:
        said = LEADS[(at - 1) % len(LEADS)].format(step=step[0].upper() + step[1:])
    if at == 0 and len(steps) in _COUNTS:
        said = f"{said} {_COUNTS[len(steps)]}"
    _record(memory, plan.get("answer") or "", steps, at + 1, said)
    return said


def _record(memory, answer, steps, at, said=""):
    turn = len(memory.get("turns") or [])
    before = memory.get("steps") if isinstance(memory.get("steps"), dict) else {}
    same = before.get("steps") == steps
    topic = memory.get("topic")
    memory["steps"] = {"answer": answer,
                      "steps": steps, "at": at, "turn": turn, "at_turn": turn, "said": said,
                      "done": bool(before.get("done")) and same,
                      "topic": before.get("topic") if same and before.get("topic")
                      else (copy.deepcopy(topic) if isinstance(topic, dict) else None)}
