import random
import re

from . import fallback

THE_ILL_POOLS = (fallback.UNKNOWN_HOW_IT_GOES_FOR_SOMEONE
                 + fallback.UNKNOWN_HOW_LONG_IN_HOSPITAL)

A_BREAK_UP = re.compile(
    r"\b(?:broke|broken|splitting|split|breaking)\s+up\b|\bdivorce\w*\b|\bseparation\b"
    r"|\bseparated\b|\bwalked\s+out\b|\bleft\s+(?:me|him|her|them)\b|\bsplit\b")


def _thread_said(memory, line):
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)][-3:]
    said = [str(turn.get("user") or "") for turn in turns]
    said += [str(turn.get("bot") or "") for turn in turns[-1:]]
    said.append(str(line or ""))
    return " ".join(said).lower()


def answer_for(text, reply, memory):
    if not isinstance(memory, dict) or reply not in THE_ILL_POOLS:
        return None
    said = _thread_said(memory, text)
    if not A_BREAK_UP.search(said):
        return None
    if not fallback.A_HARD_TIME.search(said):
        return None
    without_the_split = A_BREAK_UP.sub(" ", said)
    if fallback.A_MEDICAL_THREAD.search(without_the_split):
        return None
    if fallback.AN_ILLNESS.search(without_the_split):
        return None
    pool = fallback.UNKNOWN_HOW_IT_GOES_FOR_A_HARD_TIME
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    last = str(turns[-1].get("bot") or "") if turns else ""
    fresh = [line for line in pool if line != last] or list(pool)
    seed = len(turns) * 7919 + sum(ord(c) for c in str(text or "").lower())
    return random.Random(seed).choice(fresh)
