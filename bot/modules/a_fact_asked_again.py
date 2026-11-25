
import re

from ..memory import when as when_store

PRIORITY = 7050

AGAIN = re.compile(r"\bagain\b", re.I)
AN_ASK = re.compile(r"\b(?:what|whats|what's|when|which|where|who|how much|how many)\b", re.I)
NOT_A_RECALL = re.compile(r"\b(?:should|shall|ought|best|better|tips?|advice|recommend\w*|"
                          r"worth|cheapest|easiest|normal|usually|ok|okay|fine|bad|safe|"
                          r"possible|allowed|do i need to|can i|could i|is it)\b", re.I)

A_TIME = re.compile(r"\bwhen\b|\bwhat (?:day|date|time)\b", re.I)
A_THING_TO_AVOID = re.compile(r"(?:keep\w* (?:away|off)|stay\w* (?:away|off)|avoid\w*|allerg\w*|"
                              r"cant have|can'?t have|not allowed|off limits|cant eat|can'?t eat)",
                              re.I)
A_TARGET = re.compile(r"\b(?:target|goal|aim|trying to get to|trying to reach|hoping to get to|"
                      r"hoping for|working towards|saving for)\b", re.I)

A_DATE = (
    re.compile(r"\b(?:the\s+)?\d{1,2}(?:st|nd|rd|th)\s+(?:of\s+)?(?:jan|feb|mar|apr|may|jun|jul|"
               r"aug|sep|oct|nov|dec)[a-z]*\b", re.I),
    re.compile(r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{1,2}"
               r"(?:st|nd|rd|th)?\b", re.I),
    re.compile(r"\bnext\s+(?:week|month|year|weekend|monday|tuesday|wednesday|thursday|friday|"
               r"saturday|sunday)\b", re.I),
    re.compile(r"\b(?:the\s+)?\d{1,2}(?:st|nd|rd|th)\b", re.I),
    re.compile(r"\b(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", re.I),
    re.compile(r"\b(?:january|february|march|april|may|june|july|august|september|october|"
               r"november|december)\b", re.I),
)


def _the_plans(memory):
    user = (memory or {}).get("user") or {}
    plans = [plan for plan in (user.get("plans") or []) if isinstance(plan, str) and plan.strip()]
    latest = user.get("plan")
    if isinstance(latest, str) and latest.strip() and latest not in plans:
        plans.append(latest)
    return [" ".join(plan.split()) for plan in plans]


def _the_allergies(memory):
    out = []
    for one in (memory or {}).get("others") or []:
        if not isinstance(one, dict):
            continue
        who = str(one.get("who") or "").strip()
        for what in one.get("allergies") or []:
            what = str(what or "").strip()
            if what:
                out.append((who, what))
    return out


def _the_date_in(plan):
    for pattern in A_DATE:
        match = pattern.search(plan)
        if match:
            return " ".join(match.group(0).split())
    return None


def _the_time_asked_again(text, memory):
    try:
        if when_store.when_answer(text, memory):
            return None
    except Exception:
        return None
    dated = [date for date in (_the_date_in(plan) for plan in _the_plans(memory)) if date]
    if len(dated) != 1:
        return None
    return "You said " + dated[0] + "."


def _the_thing_to_avoid_asked_again(text, memory):
    allergies = _the_allergies(memory)
    if not allergies:
        return None
    who, what = allergies[-1]
    if who:
        return what.capitalize() + " - your " + who + " is allergic to them."
    return what.capitalize() + "."


PLAN_OPENS = ("i want to ", "i wanna ", "i'm trying to ", "im trying to ", "i am trying to ",
              "i'm hoping to ", "im hoping to ", "i am hoping to ", "i hope to ", "to ")
THE_WORD_ASKED = (("goal", "goal"), ("aim", "aim"), ("target", "target"), ("plan", "plan"))


def _the_noun_asked(text):
    low = " ".join(text.lower().split())
    for word, noun in THE_WORD_ASKED:
        if re.search(r"\b" + word + r"s?\b", low):
            return noun
    return "plan"


def _a_name(plan):
    first = plan.split()[0] if plan.split() else ""
    return bool(re.search(r"\b(?:vauxhall|ford|toyota|nissan|bmw|audi|honda|ikea|argos|"
                          r"january|february|march|april|may|june|july|august|september|october|"
                          r"november|december|monday|tuesday|wednesday|thursday|friday|saturday|"
                          r"sunday)\b", first, re.I)) and first[:1].isupper()


def _the_target_asked_again(text, memory):
    plans = _the_plans(memory)
    if not plans:
        return None
    plan = plans[-1]
    low = plan.lower()
    for opener in PLAN_OPENS:
        if low.startswith(opener):
            plan = plan[len(opener):]
            break
    noun = _the_noun_asked(text)
    if plan[:1].isupper() and not plan[:2].isupper() and not _a_name(plan):
        plan = plan[0].lower() + plan[1:]
    return "You said your " + noun + " is to " + plan.rstrip(".!?") + "."


def respond(text, memory):
    if not isinstance(text, str) or not isinstance(memory, dict):
        return None
    low = " ".join(text.lower().split())
    if not AGAIN.search(low) or not AN_ASK.search(low) or NOT_A_RECALL.search(low):
        return None
    if A_TIME.search(low):
        return _the_time_asked_again(text, memory)
    if A_THING_TO_AVOID.search(low):
        return _the_thing_to_avoid_asked_again(text, memory)
    if A_TARGET.search(low):
        return _the_target_asked_again(text, memory)
    return None
