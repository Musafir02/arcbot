from .index import build

_INDEX = None


def index():
    global _INDEX
    if _INDEX is None:
        try:
            _INDEX = build()
        except Exception:
            _INDEX = False
    return _INDEX or None


def match_with_meta(text):
    found = index()
    if found is None:
        return None
    return found.match_with_meta(text)


def match(text):
    found = match_with_meta(text)
    return found[0] if found else None


def stats():
    found = index()
    if found is None:
        return {"modules": 0, "patterns": 0, "answers": 0, "skipped": 0,
                "bad_patterns": 0, "tokens": 0}
    return found.stats()


def reset():
    global _INDEX
    _INDEX = None
