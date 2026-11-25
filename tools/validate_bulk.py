import argparse
import ast
import io
import os
import re
import sys
import tokenize

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from bot.bulk import loader
from bot.bulk.text import normalise, tokens

LABELS = frozenset("""
cars conditions cooking cooking-and-food creative entertainment everyday-help
family-and-parenting fitness food-and-drink friends-and-relationships
garden-and-plants garden-tools geography-and-travel health health-and-fitness
history home-and-diy kept-animals kits-and-claims language-and-writing
maths-and-numbers meat-in-a-card money nature-and-weather nursing opinions pets
safety school-and-study science shopping sleep small-talk sport technology
travel work
""".split())

BANNED = (
    "as an ai", "language model", "i think", "i believe", "in my opinion",
    "lorem ipsum", "todo", "tbd", "fixme", "placeholder", "your answer here",
    "http://", "https://", "www.", "pybot", "chatgpt", "claude", "gemini", "openai",
)

AMERICAN = (
    "color", "favorite", "realize", "organize", "center", "liter", "apartment",
    "vacation", "cookie", "fries", "eggplant", "cilantro", "mom", "math", "gray",
    "aluminum", "defense", "traveling", "canceled",
)

BAD_ANSWER_CHARS = set("*#`[]{}<>")
BAD_PATTERN_WORDS = frozenset(("question", "pattern", "placeholder", "example", "test",
                               "todo", "tbd", "fixme", "lorem"))
WORD = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")
SENTENCE = re.compile(r"(?<=[.!?])\s+")


def _ascii(text):
    return all(ord(char) < 128 for char in str(text))


def _sentences(answer):
    return [part for part in SENTENCE.split(str(answer).strip()) if part.strip()]


def _shares_subject(pattern, topic):
    if not topic:
        return True
    found = tokens(pattern)
    for mine in found:
        for theirs in topic:
            if mine == theirs:
                return True
            short, long = sorted((mine, theirs), key=len)
            if len(short) >= 3 and long.startswith(short) and len(long) - len(short) <= 2:
                return True
    return False


def _check_answer(answer, errors, warnings, where):
    if not isinstance(answer, str):
        errors.append(f"{where}: answer is not a string")
        return False
    if not answer.strip():
        errors.append(f"{where}: answer is empty")
        return False
    if not _ascii(answer):
        errors.append(f"{where}: answer has non-ASCII characters")
    if "\n" in answer or "\t" in answer or "\r" in answer:
        errors.append(f"{where}: answer has a newline or tab")
    if len(answer) < 80 or len(answer) > 500:
        errors.append(f"{where}: answer length {len(answer)} is outside 80-500")
    count = len(_sentences(answer))
    if count < 1 or count > 3:
        errors.append(f"{where}: answer has {count} sentences, expected 1-3")
    low = answer.lower()
    for phrase in BANNED:
        if phrase in low:
            errors.append(f"{where}: answer contains banned phrase '{phrase}'")
    for char in BAD_ANSWER_CHARS:
        if char in answer:
            errors.append(f"{where}: answer contains forbidden character '{char}'")
    if re.search(r"\b(?:www\.|https?://)\S+", low):
        errors.append(f"{where}: answer contains a URL")
    for word in AMERICAN:
        if re.search(r"\b" + re.escape(word) + r"\b", low):
            errors.append(f"{where}: answer uses American spelling '{word}'")
    if not answer.rstrip().endswith((".", "!", "?")):
        warnings.append(f"{where}: answer has no closing punctuation")
    return True


def _check_pattern(pattern, errors, where, topic):
    if not isinstance(pattern, str):
        errors.append(f"{where}: pattern is not a string")
        return None
    if not pattern:
        errors.append(f"{where}: pattern is empty")
        return None
    if not _ascii(pattern):
        errors.append(f"{where}: pattern has non-ASCII characters")
    if pattern != pattern.strip():
        errors.append(f"{where}: pattern has leading or trailing whitespace")
    if "  " in pattern or "\n" in pattern or "\t" in pattern or "\r" in pattern:
        errors.append(f"{where}: pattern has repeated whitespace or a newline")
    if pattern != pattern.lower():
        errors.append(f"{where}: pattern is not lowercase")
    if pattern.rstrip().endswith(("?", "!", ".")):
        errors.append(f"{where}: pattern ends with punctuation")
    length = len(pattern)
    if length < 12 or length > 110:
        errors.append(f"{where}: pattern length {length} is outside 12-110")
    words = pattern.split()
    if len(words) < 3 or len(words) > 16:
        errors.append(f"{where}: pattern has {len(words)} words, expected 3-16")
    if not re.search(r"[a-z]", pattern):
        errors.append(f"{where}: pattern has no letters")
    for word in BAD_PATTERN_WORDS:
        if re.search(r"\b" + re.escape(word) + r"\b", pattern):
            errors.append(f"{where}: pattern contains filler word '{word}'")
    topic_tokens = tokens(topic)
    if not _shares_subject(pattern, topic_tokens):
        errors.append(f"{where}: pattern does not name the topic")
    return normalise(pattern)


def _source_errors(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            source = handle.read()
    except Exception as error:
        return [f"cannot read file ({error})"]
    try:
        tree = ast.parse(source, filename=path)
    except SyntaxError as error:
        return [f"cannot parse file ({error})"]
    errors = []
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            errors.append("module body must contain only assignments")
            break
    try:
        for token in tokenize.generate_tokens(io.StringIO(source).readline):
            if token.type == tokenize.COMMENT:
                errors.append("file contains a comment")
                break
    except Exception:
        pass
    return errors


def _file_errors(path, category, domain, module_id):
    errors, warnings = [], []
    for line in _source_errors(path):
        errors.append(f"{module_id}: {line}")
    try:
        module = loader.load_file(path)
    except Exception as error:
        errors.append(f"{module_id}: cannot load file ({error})")
        return errors, warnings, 0, 0, []
    if getattr(module, "MODULE", None) != module_id:
        errors.append(f"{module_id}: MODULE is {getattr(module, 'MODULE', None)!r}")
    if getattr(module, "CATEGORY", None) != category:
        errors.append(f"{module_id}: CATEGORY is {getattr(module, 'CATEGORY', None)!r}")
    if getattr(module, "DOMAIN", None) != domain:
        errors.append(f"{module_id}: DOMAIN is {getattr(module, 'DOMAIN', None)!r}")
    topic = getattr(module, "TOPIC", None)
    if not isinstance(topic, str) or not topic.strip():
        errors.append(f"{module_id}: TOPIC is missing")
        topic = ""
    elif not _ascii(topic) or len(topic) > 80 or "\n" in topic:
        errors.append(f"{module_id}: TOPIC is not valid ASCII under 80 characters")
    priority = getattr(module, "PRIORITY", None)
    if isinstance(priority, bool) or not isinstance(priority, int) or priority != 5000:
        errors.append(f"{module_id}: PRIORITY must be the integer 5000")
    answers = getattr(module, "ANSWERS", None)
    if not isinstance(answers, (tuple, list)) or len(answers) != 1:
        errors.append(f"{module_id}: ANSWERS must be a one-item tuple")
    elif answers[0] not in LABELS:
        errors.append(f"{module_id}: ANSWERS label {answers[0]!r} is not a known topic")
    items = getattr(module, "ITEMS", None)
    if not isinstance(items, (tuple, list)) or len(items) != 10:
        errors.append(f"{module_id}: ITEMS must contain exactly 10 items")
        return errors, warnings, 0, 0, []
    if not isinstance(items, tuple):
        warnings.append(f"{module_id}: ITEMS should be a tuple")
    pattern_total, answer_total = 0, 0
    seen_patterns, seen_answers = {}, set()
    normalised = []
    for item_index, item in enumerate(items):
        where = f"{module_id} item {item_index + 1}"
        if not isinstance(item, (tuple, list)) or len(item) != 2:
            errors.append(f"{where}: item must be a (patterns, answer) pair")
            continue
        patterns, answer = item
        if not isinstance(patterns, (tuple, list)) or len(patterns) != 10:
            errors.append(f"{where}: patterns must contain exactly 10 entries")
            continue
        if not isinstance(patterns, tuple):
            warnings.append(f"{where}: patterns should be a tuple")
        if _check_answer(answer, errors, warnings, where):
            answer_total += 1
            if answer in seen_answers:
                errors.append(f"{where}: answer is repeated within the module")
            seen_answers.add(answer)
        for pattern_index, pattern in enumerate(patterns):
            found = _check_pattern(pattern, errors, f"{where} pattern {pattern_index + 1}", topic)
            if found is None:
                continue
            pattern_total += 1
            if found in seen_patterns:
                errors.append(f"{where} pattern {pattern_index + 1}: duplicates pattern "
                              f"{seen_patterns[found]}")
            else:
                seen_patterns[found] = pattern_index + 1
            normalised.append((found, module_id))
    if pattern_total != 100:
        errors.append(f"{module_id}: found {pattern_total} usable patterns, expected 100")
    if answer_total != 10:
        errors.append(f"{module_id}: found {answer_total} usable answers, expected 10")
    return errors, warnings, pattern_total, answer_total, normalised


def _domain_dirs(base):
    found = []
    if not os.path.isdir(base):
        return found
    for category in sorted(os.listdir(base)):
        category_path = os.path.join(base, category)
        if not os.path.isdir(category_path) or category.startswith((".", "_")):
            continue
        for domain in sorted(os.listdir(category_path)):
            domain_path = os.path.join(category_path, domain)
            if not os.path.isdir(domain_path) or domain.startswith((".", "_")):
                continue
            found.append((category, domain, domain_path))
    return found


def _module_files(path):
    return sorted(name for name in os.listdir(path)
                  if name.endswith(".py") and not name.startswith("_"))


def _check_manifest(category, domain, path, files, errors):
    expected = {name[:-3] for name in files}
    manifest_path = os.path.join(path, "_domain.json")
    if not os.path.isfile(manifest_path):
        errors.append(f"{category}/{domain}: _domain.json is missing")
        return
    data = loader.manifest(manifest_path)
    if not isinstance(data, dict):
        errors.append(f"{category}/{domain}: _domain.json is not valid JSON")
        return
    if data.get("category") != category or data.get("domain") != domain:
        errors.append(f"{category}/{domain}: _domain.json category or domain does not match")
    if not isinstance(data.get("title"), str) or not data["title"].strip():
        errors.append(f"{category}/{domain}: _domain.json title is missing")
    modules = data.get("modules")
    if not isinstance(modules, list) or len(modules) != 50:
        errors.append(f"{category}/{domain}: _domain.json must list exactly 50 modules")
        return
    listed = []
    for entry in modules:
        if not isinstance(entry, dict):
            errors.append(f"{category}/{domain}: _domain.json has a non-object entry")
            continue
        name = entry.get("file")
        title = entry.get("title")
        if not isinstance(name, str) or not name:
            errors.append(f"{category}/{domain}: _domain.json has an entry without a file")
            continue
        if name.endswith(".py"):
            errors.append(f"{category}/{domain}: _domain.json file {name!r} includes .py")
            name = name[:-3]
        if not isinstance(title, str) or not title.strip():
            errors.append(f"{category}/{domain}: _domain.json entry {name!r} has no title")
        listed.append(name)
    if len(set(listed)) != len(listed):
        errors.append(f"{category}/{domain}: _domain.json lists a file twice")
    missing = sorted(set(listed) - expected)
    extra = sorted(expected - set(listed))
    if missing:
        errors.append(f"{category}/{domain}: _domain.json lists missing files {missing[:5]}")
    if extra:
        errors.append(f"{category}/{domain}: domain has unlisted files {extra[:5]}")


def _check_domain(category, domain, path, complete, duplicate_map):
    errors, warnings = [], []
    files = _module_files(path)
    module_ids = []
    patterns, answers = 0, 0
    normalised = []
    for name in files:
        file_path = os.path.join(path, name)
        module_id = f"{category}.{domain}.{name[:-3]}"
        module_ids.append(module_id)
        found_errors, found_warnings, found_patterns, found_answers, used = _file_errors(
            file_path, category, domain, module_id)
        errors.extend(found_errors)
        warnings.extend(found_warnings)
        patterns += found_patterns
        answers += found_answers
        normalised.extend(used)
    if complete:
        if len(files) != 50:
            errors.append(f"{category}/{domain}: has {len(files)} module files, expected 50")
        if not os.path.isfile(os.path.join(path, "__init__.py")):
            errors.append(f"{category}/{domain}: __init__.py is missing")
        category_path = os.path.dirname(path)
        if not os.path.isfile(os.path.join(category_path, "__init__.py")):
            errors.append(f"{category}: __init__.py is missing")
        _check_manifest(category, domain, path, files, errors)
    if duplicate_map is not None:
        for pattern, module_id in normalised:
            seen = duplicate_map.get(pattern)
            if seen is not None and seen != module_id:
                errors.append(f"{module_id}: pattern duplicates {seen}: {pattern}")
            else:
                duplicate_map[pattern] = module_id
    return errors, warnings, len(files), patterns, answers


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--complete", action="store_true")
    parser.add_argument("--duplicates", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--max-errors", type=int, default=200)
    args = parser.parse_args()
    base = loader.data_root()
    if not (args.domain or args.all or args.complete):
        parser.error("choose --domain, --all, or --complete")
    if args.complete:
        args.all = True
    targets = []
    if args.domain:
        parts = args.domain.replace("\\", "/").strip("/").split("/")
        if len(parts) != 2:
            parser.error("--domain must look like category/domain")
        category, domain = parts
        path = os.path.join(base, category, domain)
        if not os.path.isdir(path):
            print(f"missing domain: {category}/{domain}")
            return 1
        targets.append((category, domain, path))
    if args.all:
        targets = _domain_dirs(base)
        if not targets:
            print("no domains found")
            return 1
    duplicate_map = {} if args.duplicates else None
    errors, warnings = [], []
    files = patterns = answers = 0
    for category, domain, path in targets:
        found_errors, found_warnings, found_files, found_patterns, found_answers = _check_domain(
            category, domain, path, args.all, duplicate_map)
        errors.extend(found_errors)
        warnings.extend(found_warnings)
        files += found_files
        patterns += found_patterns
        answers += found_answers
    if args.complete:
        if len(targets) != 200:
            errors.append(f"found {len(targets)} domains, expected 200")
        if files != 10000:
            errors.append(f"found {files} module files, expected 10000")
        if answers != 100000:
            errors.append(f"found {answers} answers, expected 100000")
        if patterns != 1000000:
            errors.append(f"found {patterns} patterns, expected 1000000")
    print(f"domains={len(targets)} files={files} patterns={patterns} answers={answers}")
    print(f"errors={len(errors)} warnings={len(warnings)}")
    for line in errors[:args.max_errors]:
        print("ERROR", line)
    if len(errors) > args.max_errors:
        print(f"ERROR ... {len(errors) - args.max_errors} more")
    for line in warnings[:20]:
        print("WARN", line)
    if len(warnings) > 20:
        print(f"WARN ... {len(warnings) - 20} more")
    if args.strict and warnings:
        return 1
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
