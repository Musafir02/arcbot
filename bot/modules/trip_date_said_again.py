
import re

from ..memory import facts as extract
from ..memory import trips
from . import memory_store

PRIORITY = 6900


A_DATE_SAID_NOW = re.compile(
    r"^\W*(?:(?:ok|okay|right|well|so|and|no|nope|sorry|actually|oops|wait|ah|oh|hmm)"
    r"[,.]?\s+){0,4}"
    r"(?:(?:it'?s|its|it\s+is|that'?s|thats)\s+)?"
    + extract.A_DATE_VALUE +
    r"\s+now\b", re.I)
A_MARKER_SAID = re.compile(r"\b(?:no|nope|sorry|actually|oops|wait|ah|oh|hmm)\b", re.I)


def _a_date_said_now(text):
    line = str(text or "")
    if "?" in line:
        return ""
    found = A_DATE_SAID_NOW.search(line)
    if found is None:
        return ""
    if not A_MARKER_SAID.search(line[:found.start(1)]):
        return ""
    for group in found.groups():
        if group and extract._a_date(group):
            return extract._tidy(group)
    return ""


def _the_first_clause(text):
    head = str(text or "").split(",")[0].strip()
    return head if len(head.split()) >= 2 else ""


def _the_trip_it_moves(memory):
    plan = memory_store._stated_plan(memory) or memory_store.user(memory).get("plan")
    if not isinstance(plan, str) or not plan.strip():
        return None
    trip = trips._the_trip_so_far(memory)
    if not trip:
        return None
    on_record = " ".join(str(trip.get("plan") or "").lower().split())
    if not on_record:
        return None
    if on_record == " ".join(plan.lower().split()):
        return plan
    said_before = [" ".join(str(one or "").lower().split())
                   for one in memory_store.user(memory).get("plans") or []]
    if on_record in said_before:
        return trip.get("plan")
    return None


def _the_month_taken_back(memory):
    trip = trips._the_trip_so_far(memory) or {}
    month = " ".join(str(trip.get("month") or "").lower().split())
    if not month:
        return None
    for said in memory_store.user(memory).get("plans") or []:
        if month in " ".join(str(said or "").lower().split()):
            return month
    return None


def _a_dated_fact_beside_it(memory):
    for other in memory.get("others") or []:
        if not isinstance(other, dict):
            continue
        if any(other.get(key) for key in ("birthday", "appointment", "when", "date")):
            return True
    return False


def observe(text, memory):
    if not isinstance(memory, dict):
        return
    moved = (extract.a_trip_date_put_right(text)
             or extract.a_trip_date_put_right(_the_first_clause(text))
             or _a_date_said_now(text))
    if not moved:
        return
    if not _the_trip_it_moves(memory):
        return
    taken_back = _the_month_taken_back(memory) if _a_dated_fact_beside_it(memory) else None
    memory_store._apply_correction(memory, {"to": moved, "from": taken_back}, text)
