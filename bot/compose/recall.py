
import re

from . import pick

TAILS = (
    "How are you feeling about it?",
    "Is there anything you need before it?",
    "What do you want to have ready for it?",
)

LONG_PLAN = 78

PLAN_WORDS = frozenset("""a an the of to on in at for with and or but my your our their his her
its it you i we they he she be been being am is are was were will would can could shall should
may might must going go gone away back off up down out over about around next last this that
these those coming week weeks month months year years day days night nights tomorrow today
tonight soon again still just also too very really quite nearly almost more most less""".split())


GRIEF_PLAN = re.compile(
    r"\b(?:funeral|funerals|wake|burial|cremation|crematorium|memorial|mourners?|"
    r"viewing|interment|graveside|obsequies|death|deaths|died|dying|passing|passed away|"
    r"grave|remembrance)\b", re.I)


def _is_a_death(said):
    return bool(GRIEF_PLAN.search(said))


def _said_on_the_last_turn(said, memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return False
    last = turns[-1] if isinstance(turns[-1], dict) else {}
    bot = str(last.get("bot") or "").strip()
    return bool(bot) and (bot == said or bot.startswith(said + " "))


def _names_a_thing(said):
    return any(word.isalpha() and word.lower() not in PLAN_WORDS
               for word in said.strip(" .").split()[1:])


def with_a_tail(said, memory):
    said = str(said or "").strip()
    if not said or len(said) > LONG_PLAN or said.count(".") > 1:
        return said
    if not _names_a_thing(said) or _is_a_death(said):
        return said
    if _said_on_the_last_turn(said, memory):
        return said
    return said + " " + pick(list(TAILS), memory, said)
