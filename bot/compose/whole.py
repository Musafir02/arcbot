import re

_LAST_CLAUSE = re.compile(
    r"(?:^|[,;:]\s+|[.!?][\"'\u201d]?\s+)((?:and\s+)?(?:if|unless|in\s+case)\b[^,;:]*)$", re.I)

_CONTINUES = re.compile(
    r"^['\"\u201d]?(?:or|and|but|which|who|whom|whose|that|so|then|yet|plus|as|if|unless)\b", re.I)

_MOST_AFTER = 90


def a_whole_cut(text, most):
    whole = str(text or "").strip()
    if len(whole) <= most:
        return whole
    cut = max(whole.rfind(", ", 0, most), whole.rfind("; ", 0, most))
    if cut < 80:
        cut = whole.rfind(" ", 0, most)
    cut = max(cut, 80)
    kept = whole[:cut].strip(" ,;:-")
    dropped = whole[cut:].strip(" ,;:-")
    hanging = _LAST_CLAUSE.search(kept)
    if not hanging or not dropped or _CONTINUES.match(dropped):
        return kept
    after = re.search(r"[,;]\s", whole[cut + 2:])
    end = cut + 2 + after.start() if after else len(whole)
    doing = whole[cut:end]
    if end - cut <= _MOST_AFTER and "'" not in doing and '"' not in doing:
        return whole[:end].strip(" ,;:-")
    return kept[:hanging.start(1)].strip(" ,;:-")
