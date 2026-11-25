import importlib
import pkgutil

_INTERNAL = {"lookup", "units", "cooking_entries", "keeping_cooked", "crisis_replies",
             "home_craft", "quantity", "cooking_more", "bake_faults", "family_more",
             "cooking_tables"}

TOPIC_ALIASES = {
    "home": "home-and-diy",
    "travel": "geography-and-travel",
    "nature": "nature-and-weather",
    "garden": "garden-and-plants",
    "food": "food-and-drink",
    "food_and_drink": "food-and-drink",
    "maths": "maths-and-numbers",
    "school": "school-and-study",
    "language": "language-and-writing",
}

_cache = {}


def domains():
    cached = _cache.get("domains")
    if cached is not None:
        return cached
    found = {}
    for item in pkgutil.iter_modules(__path__):
        if item.name in _INTERNAL:
            continue
        try:
            found[item.name] = importlib.import_module(f"{__name__}.{item.name}")
        except Exception:
            continue
    _cache["domains"] = found
    return found


def by_topic(found=None):
    remembered = found is None
    cached = _cache.get("by_topic") if remembered else None
    if cached is not None:
        return cached
    if remembered:
        found = domains()
    out = {}
    for name, module in found.items():
        declared = getattr(module, "ANSWERS", ())
        if isinstance(declared, str):
            declared = (declared,)
        try:
            declared = [str(item).strip().lower() for item in declared if str(item).strip()]
        except TypeError:
            declared = []
        if not declared:
            flat = str(name).strip().lower().replace("_", "-")
            declared = [TOPIC_ALIASES.get(flat, flat)]
        out[str(name)] = tuple(sorted(topic for topic in declared if topic))
    if remembered:
        _cache["by_topic"] = out
    return out


def topics(found=None):
    answered = set()
    for declared in by_topic(found).values():
        answered.update(declared)
    answered.discard("")
    return tuple(sorted(answered))


def _with_one_more_test(guard, extra):
    if guard is None:
        return extra

    def guard_and_extra(understood):
        return bool(guard(understood)) and bool(extra(understood))
    return guard_and_extra


def entries():
    if "all" not in _cache:
        found = []
        for name, module in sorted(domains().items()):
            stands_aside = getattr(module, "STANDS_ASIDE", None)
            guard_folds = getattr(module, "GUARD_FOLDS", None) or {}
            for item in getattr(module, "ENTRIES", ()) or ():
                try:
                    item.domain = name
                    if stands_aside is not None and getattr(item, "guard", None) is None:
                        item.guard = stands_aside
                    extra = guard_folds.get(getattr(item, "id", ""))
                    if extra is not None:
                        item.guard = _with_one_more_test(item.guard, extra)
                except AttributeError:
                    pass
                found.append(item)
        _cache["all"] = found
    return _cache["all"]
