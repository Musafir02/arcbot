import re

from ..compose import fallback, findout, routes

SEARCH_ONLY = re.compile(
    r"\b(?:beats searching|a search (?:should|will)|quick search|searching for it will|"
    r"quickest route to a straight answer|would rather not guess|beyond what i know|"
    r"not sure about that one)\b", re.I)

A_YES_OR_NO_ASK = re.compile(
    r"\b(?:is there|are there|do they have|does (?:it|this|that|the [a-z]+) have|have they got)\b")
LIVE_ONLY = re.compile(
    r"(timetables? and listings|change by the hour|that is live|live, sorry|today's included|"
    r"the current one, today)", re.I)
INCLUDED_ASK = re.compile(
    r"\b(?:includes?|included|in with|comes? with|part of the price|on top|extra)\b", re.I)
A_FIGURE_REPLY = re.compile(
    r"(?:comes from a quote or a listing|no list price|price the same description|"
    r"ask two firms to price|compare what each one leaves out)", re.I)
MONEY_WORDS = re.compile(
    r"\b(?:rate|rates|charge|charges|price|prices|pricing|cost|costs|fee|fees|tariff|per hour|"
    r"per day|per night)\b", re.I)

QUESTION_FILLER = frozenset("""
a an the is are was were be been being am do does did have has had having there here it this
that these those they them their theirs i me my mine we us our you your yours he him his she
her hers who whom whose what which when where why how much many long far often any some all
and or but if then than so not no yes can could will would should may might must shall to of
in on at for with from by about into over under up down out off again more most very just
only also too own same other another such per each every both either neither nor as like
get got gets getting go going goes went come comes came coming take takes took taken taking
one ones thing things still yet ever never always really quite rather bit lot
""".split())


OLD_ONE_VERBS = frozenset("""keep keeping kept take taking taken away rid getting get gets
throw throwing leave leaving want wants wanted happen happens happened dispose disposal""".split())


def _content(text, skip=()):
    return {w for w in re.findall(r"[a-z]+", (text or "").lower())
            if len(w) > 2 and w not in QUESTION_FILLER and w not in skip}


PRIORITY = -999


def _would_be_said(text, memory):
    try:
        from . import greeting
        said = greeting.respond(text, memory)
    except Exception:
        said = None
    if not said:
        said = fallback.reply_for(text, memory)
    return said or ""


def _answers_the_ask(route, clean, said):
    if not said:
        return True
    if route is routes.A_PLACE_HAS and A_YES_OR_NO_ASK.search(clean):
        if MONEY_WORDS.search(said) or LIVE_ONLY.search(said):
            return False
        return bool(_content(said) & _content(clean))
    if route is routes.THE_OLD_ONE_POOL:
        return bool(_content(said) & _content(clean, OLD_ONE_VERBS))
    if route is routes.INCLUDED and INCLUDED_ASK.search(clean) and A_FIGURE_REPLY.search(said):
        return False
    return True


def respond(text, memory):
    understood = memory.get("understood") or {}
    clean = fallback._matchable(fallback._plain(understood.get("clean") or text))
    if findout.reads_as_busy(clean):
        return None
    route = routes.options(clean)
    if not route:
        return None
    said = _would_be_said(text, memory)
    if fallback._is_a_hedge(said) or SEARCH_ONLY.search(said or ""):
        return fallback._choose(route, memory, fallback._matchable(text))
    if route is routes.INCLUDED and INCLUDED_ASK.search(clean) \
            and A_FIGURE_REPLY.search(said or ""):
        return fallback._choose(route, memory, fallback._matchable(text))
    if not _answers_the_ask(route, clean, said or ""):
        return fallback._choose(route, memory, fallback._matchable(text))
    return None
