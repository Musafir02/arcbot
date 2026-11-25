import copy
import importlib
import pkgutil

from . import modules

ARBITER = "arbiter"
FALLBACK = "Hello!"


def load_modules():
    loaded = []
    for entry in pkgutil.iter_modules(modules.__path__):
        try:
            module = importlib.import_module(f"{modules.__name__}.{entry.name}")
        except Exception:
            continue
        priority = getattr(module, "PRIORITY", 0)
        if isinstance(priority, bool) or not isinstance(priority, (int, float)):
            priority = 0
        loaded.append((priority, entry.name, module))
    loaded.sort(key=lambda item: (-item[0], item[1]))
    return [(name, priority, module) for priority, name, module in loaded]


def _hooks(name):
    return [(module_name, priority, getattr(module, name)) for module_name, priority, module in _MODULES
            if callable(getattr(module, name, None))]


_MODULES = load_modules()
_OBSERVERS = _hooks("observe")
_HANDLERS = _hooks("respond")
_AFTER = _hooks("after")
_ARBITER = next((getattr(module, "choose", None) for name, _, module in _MODULES if name == ARBITER), None)


def _copy(memory):
    try:
        return {key: value if key == "turns" else copy.deepcopy(value) for key, value in memory.items()}
    except Exception:
        return memory


def _choose(text, memory, candidates):
    if _ARBITER is None or len(candidates) < 2:
        return 0
    views = [dict(c) for c in candidates]
    try:
        picked = _ARBITER(text, memory, views)
    except Exception:
        return 0
    if isinstance(picked, int) and not isinstance(picked, bool) and 0 <= picked < len(views):
        return picked
    if isinstance(picked, dict):
        for i, view in enumerate(views):
            if view is picked or view["module"] == picked.get("module"):
                return i
    return 0


def turn(text, memory):
    for _, _, observe in _OBSERVERS:
        try:
            observe(text, memory)
        except Exception:
            continue
    candidates, copies = [], []
    for name, priority, respond in _HANDLERS:
        mine = _copy(memory)
        try:
            answer = respond(text, mine)
        except Exception:
            continue
        if isinstance(answer, str) and answer.strip():
            candidates.append({"module": name, "priority": priority, "reply": answer})
            copies.append(mine)
    if candidates:
        index = _choose(text, memory, candidates)
        reply, module = candidates[index]["reply"], candidates[index]["module"]
        if copies[index] is not memory:
            memory.clear()
            memory.update(copies[index])
    else:
        reply, module = FALLBACK, None
    for _, _, after in _AFTER:
        try:
            after(text, reply, memory)
        except Exception:
            continue
    turns = memory.get("turns")
    if not isinstance(turns, list):
        turns = memory["turns"] = []
    turns.append({"user": text, "bot": reply, "module": module})
    return {"reply": reply, "module": module, "candidates": candidates}


def reply(text, memory):
    return turn(text, memory)["reply"]
