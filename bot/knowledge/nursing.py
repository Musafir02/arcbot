import re

from bot.knowledge.lookup import entry
from bot.knowledge.study import CAREER_SUBJECTS, _career_subjects

ENTRIES = []

_POINT_WORDS = ("points", "ucas points", "ucas", "entry points", "tariff points", "tariff",
                "how many points", "points do i need", "points needed", "points for")

_CAREER_NAMES = tuple(name for names, _ in CAREER_SUBJECTS for name in names)

ENTRIES.append(entry(
    "career-entry-points",
    (_CAREER_NAMES, _POINT_WORDS),
    _career_subjects,
    avoid=("licence", "license", "driving", "driver", "penalty", "speeding", "ban", "banned",
           "insurance", "f1", "formula 1", "formula one", "grand prix", "motogp", "lap", "laps",
           "try", "tries", "goal", "goals", "touchdown", "conversion", "rugby", "football",
           "soccer", "cricket", "netball", "basketball", "hockey", "tennis", "match", "game",
           "games", "score", "scored", "scoring", "season", "team", "teams", "loyalty",
           "reward", "rewards", "reward card", "nectar", "clubcard", "club card", "store card",
           "voucher", "vouchers", "coffee", "free coffee", "free drink", "supermarket", "shop",
           "shopping", "air miles", "my card", "dehumidifier", "point of"),
    bias=6))
