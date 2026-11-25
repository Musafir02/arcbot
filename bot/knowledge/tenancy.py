import re

from .lookup import entry

_NOT_A_RENT_RAISE = re.compile(
    r"\brais(?:e|ed|es|ing)\s+(?:a|an|the|my|our|your|their|any|some)?\s*"
    r"(?:complaints?|concerns?|issues?|problems?|matters?|questions?|grievances?|objections?|"
    r"disputes?|alarms?|glass|glasses|toast|voices?|prices?|funds?|money|children|kids|"
    r"awareness|profile|hell)\b",
    re.IGNORECASE)

_A_TENANCY = re.compile(
    r"\b(?:landlords?|landlad(?:y|ies)|letting agents?|letting agency|lettings agency"
    r"|tenants?|tenancy|tenancies|housing association|council house)\b",
    re.IGNORECASE)


def _said(understood):
    if isinstance(understood, str):
        return understood.lower()
    reading = understood or {}
    return str(reading.get("clean") or reading.get("text") or "").lower()


def _a_raise_with_an_object(understood):
    return bool(_NOT_A_RENT_RAISE.search(_said(understood)))


def _a_tenancy_and_not_a_manager(understood):
    return bool(_A_TENANCY.search(_said(understood)))


def _fence(modules, row_id, when):
    for module in modules:
        for row in getattr(module, "ENTRIES", ()) or ():
            if row.id == row_id and getattr(row, "guard", None) is None:
                row.guard = lambda understood, when=when: not when(understood)


from . import money, work

_fence((money,), "rent-rise", _a_raise_with_an_object)
_fence((work,), "raise-with-boss", _a_tenancy_and_not_a_manager)


ENTRIES = [
    entry("landlord-complaint",
          (("landlord", "landlords", "landlady", "landladies", "letting agent",
            "letting agents", "letting agency", "lettings agent", "housing association",
            "my tenancy", "the tenancy", "my letting agent"),
           ("complain", "complains", "complained", "complaining", "complaint", "complaints",
            "formal complaint", "raise a complaint", "put in a complaint", "make a complaint",
            "made a complaint", "log a complaint", "report", "reported", "redress", "ombudsman",
            "deadlock", "not happy with", "unhappy with", "dispute", "issue", "issues",
            "concern", "concerns", "problem", "problems", "matter", "matters", "grievance")),
          "Put it in writing to the landlord - a dated email or letter, what happened, what you "
          "want done and a deadline of 14 days - and keep a copy, because every later step asks "
          "for it. If a letting agent runs the flat, the agent has to belong to a free redress "
          "scheme (the Property Redress Scheme or The Property Ombudsman), and a complaint can go "
          "there after eight weeks, or sooner if the agent deadlocks it. A hazard - damp, no "
          "heating, a broken boiler, a fire risk - is your council's housing team, who can inspect "
          "and order the work, and the deposit scheme holding your deposit sorts out a deposit "
          "argument. Shelter or Citizens Advice will read the letter before you send it, free.",
          ask=("landlord", "landlady", "agent", "tenancy", "tenants", "tenant", "flat",
               "complain", "complaint", "redress", "ombudsman"),
          avoid=("fix", "fixed", "fixing", "repair", "repairs", "broken", "boiler", "heating",
                 "hot water", "damp", "mould", "mold", "deposit", "deposits", "selling", "sell",
                 "sale", "sold", "evict", "evicted", "eviction", "section 21", "section 8",
                 "notice to quit", "kick me out", "throw me out", "arrears", "behind on rent",
                 "rent increase", "raise the rent", "raised the rent", "put the rent up",
                 "eviction notice"),
          bias=1),
]

ANSWERS = ("home-and-diy",)
