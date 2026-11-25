import json
import os
import types

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")


def data_root():
    return DATA


def module_id(path, root=None):
    base = root or DATA
    rel = os.path.relpath(path, base)
    return os.path.splitext(rel)[0].replace(os.sep, ".")


def iter_paths(root=None):
    base = root or DATA
    if not os.path.isdir(base):
        return
    for folder, dirs, files in os.walk(base):
        dirs[:] = sorted(name for name in dirs
                         if name != "__pycache__" and not name.startswith("."))
        for name in sorted(files):
            if not name.endswith(".py"):
                continue
            if name.startswith("_"):
                continue
            yield os.path.join(folder, name)


def load_file(path):
    with open(path, "r", encoding="utf-8") as handle:
        source = handle.read()
    namespace = {}
    exec(compile(source, path, "exec"), namespace)
    namespace.pop("__builtins__", None)
    return types.SimpleNamespace(**namespace)


def iter_modules(root=None):
    base = root or DATA
    for path in iter_paths(base):
        try:
            module = load_file(path)
        except Exception:
            yield module_id(path, base), None
            continue
        yield module_id(path, base), module


def manifest(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception:
        return None
