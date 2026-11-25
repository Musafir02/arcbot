import re

from .entertainment import BOOK_MOODS, FILM_MOODS, GRAVE
from .lookup import entry

ANSWERS = ("entertainment", "creative")

PICKS = {"film": FILM_MOODS, "book": BOOK_MOODS}
MEDIUM_WORDS = {
    "film": ("film", "films", "movie", "movies", "watch", "watching", "netflix", "telly",
             "tv", "series", "cinema"),
    "book": ("book", "books", "read", "reading", "novel", "novels", "author", "audiobook"),
}
_TITLED = re.compile(r"\*([^*\n]{2,60})\*")
_MOOD_LEAD = re.compile(r"^for (?:a|an|the)[^:\n]{0,40}:\s*", re.I)
MOOD_NEAR = {
    "funny": ("light", "uplifting", "twist"),
    "light": ("uplifting", "funny", "short"),
    "uplifting": ("light", "funny", "romance"),
    "sad": ("romance", "think", "uplifting"),
    "think": ("twist", "true", "gripping"),
    "gripping": ("twist", "think", "true"),
    "twist": ("gripping", "think", "true"),
    "true": ("think", "gripping", "uplifting"),
    "short": ("light", "funny", "romance"),
    "romance": ("uplifting", "sad", "light"),
    "scary": ("think", "gripping", "twist"),
}
PICK_ORDER = ("light", "uplifting", "funny", "think", "gripping", "twist", "true", "short",
              "romance", "scary", "sad")
SERIES_SIDE = frozenset("""series sitcom episodes episode netflix iplayer prime tv telly channel
streaming broadcast""".split())


def _titles_in(text):
    return [one.strip() for one in _TITLED.findall(str(text or ""))]


def _medium_of(text):
    found = set(re.findall(r"[a-z']+", str(text or "").lower()))
    for medium, cues in MEDIUM_WORDS.items():
        if found & set(cues):
            return medium
    return None


def _the_line(understood, memory):
    if isinstance(understood, dict):
        for key in ("text", "clean", "line"):
            if isinstance(understood.get(key), str) and understood[key].strip():
                return understood[key]
    turns = [one for one in (memory.get("turns") or []) if isinstance(one, dict)]
    return str((turns[-1].get("user") if turns else "") or "")


def _pick_in_play(memory, understood=None):
    turns = [one for one in (memory.get("turns") or []) if isinstance(one, dict)]
    replies = [str(one.get("bot") or "") for one in turns if one.get("bot")]
    if not replies:
        return None, set()
    last = replies[-1]
    if len(_titles_in(last)) < 2:
        return None, set()
    named = {title.lower() for reply in replies for title in _titles_in(reply)}
    here = _the_line(understood, memory)
    medium = _medium_of(here) or _medium_of(last)
    return medium, named


def _moods_named(text, table):
    words = set(re.findall(r"[a-z']+", str(text or "").lower()))
    return [mood for mood in table if mood in words]


def _other_pick(memory, understood):
    medium, named = _pick_in_play(memory, understood)
    if not medium:
        return None
    turns = [one for one in (memory.get("turns") or []) if isinstance(one, dict)]
    asked = _the_line(understood, memory)
    if set(re.findall(r"[a-z']+", asked.lower())) & SERIES_SIDE:
        return None
    table = PICKS[medium]
    before = [str(one.get("user") or "") for one in turns[:-1]]
    order = []
    for part in (asked, before[-1] if before else "", " ".join(before)):
        for mood in _moods_named(part, table):
            if mood in order:
                continue
            order.append(mood)
            order += [near for near in MOOD_NEAR.get(mood, ()) if near in table]
    order += [mood for mood in PICK_ORDER if mood in table]
    order += [mood for mood in table]
    seen_moods = set()
    listed = {title.lower() for title in named}
    for mood in order:
        if mood in seen_moods:
            continue
        seen_moods.add(mood)
        sentence = table[mood]
        titles = _titles_in(sentence)
        if not titles:
            continue
        if any(title.lower() in listed for title in titles):
            continue
        return "Something different then: " + _MOOD_LEAD.sub("", sentence)
    return None


ENTRIES = [
    entry("another-pick",
          (("any other film", "any other films", "any other movie", "any other movies",
            "any other book", "any other books", "any other series",
            "another film", "another movie", "another book",
            "something else to watch", "anything else to watch", "something to watch after",
            "one more film", "one more book"),
           ("film", "films", "movie", "movies", "book", "books", "series", "watch", "read")),
          _other_pick, ask=("other", "another", "else", "more", "after", "next"),
          avoid=GRAVE + ("instead of", "rather than", "how do i", "how can i", "cancel",
                         "stop", "delete", "hide", "cheaper", "free", "where can i")),
]
