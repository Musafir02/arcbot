import argparse
import importlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from bot.bulk import match
from bot.modules import bulk_dispatch


def read_jsonl(path):
    rows = []
    if not os.path.isfile(path):
        return rows
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                continue
    return rows


def sample(rows, limit):
    if limit == 0:
        return []
    if limit < 0 or len(rows) <= limit:
        return rows
    step = len(rows) / float(limit)
    return [rows[min(len(rows) - 1, int(index * step))] for index in range(limit)]


def silent(module, reply):
    return module in (None, "greeting") or reply in ("Hello!", "")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--false-limit", type=int, default=50)
    args = parser.parse_args()
    holdout = read_jsonl(os.path.join(ROOT, "bot", "bulk", "holdout.jsonl"))
    false_rows = read_jsonl(os.path.join(ROOT, "bot", "bulk", "false.jsonl"))
    if not holdout:
        print("holdout missing")
        return 1
    holdout = sample(holdout, args.limit)
    false_rows = sample(false_rows, args.false_limit)

    original = bulk_dispatch.respond
    bulk_dispatch.respond = lambda text, memory: None
    import bot.runtime as runtime
    runtime = importlib.reload(runtime)
    baseline = []
    for index, row in enumerate(holdout, 1):
        found = runtime.turn(row.get("q", ""), {})
        baseline.append((found.get("module"), found.get("reply")))
        if index % 20 == 0:
            print("baseline {}/{}".format(index, len(holdout)), flush=True)

    bulk_dispatch.respond = original
    runtime = importlib.reload(runtime)
    full = []
    for index, row in enumerate(holdout, 1):
        found = runtime.turn(row.get("q", ""), {})
        full.append((found.get("module"), found.get("reply")))
        if index % 20 == 0:
            print("full {}/{}".format(index, len(holdout)), flush=True)

    answered_before = 0
    answered_after = 0
    bulk_answered = 0
    bulk_correct = 0
    wins = 0
    per_category = {}
    for row, before, after in zip(holdout, baseline, full):
        query = row.get("q", "")
        domain = row.get("domain")
        category = domain.split("/")[0] if isinstance(domain, str) else "?"
        stats = per_category.setdefault(category, {"n": 0, "silent": 0, "fired": 0,
                                                    "correct": 0, "win": 0})
        stats["n"] += 1
        before_ok = not silent(before[0], before[1])
        after_ok = not silent(after[0], after[1])
        answered_before += before_ok
        answered_after += after_ok
        meta = match.match_with_meta(query)
        in_bulk = after[0] == "bulk_dispatch" and meta is not None
        bulk_answered += in_bulk
        stats["fired"] += in_bulk
        if not before_ok:
            stats["silent"] += 1
        if in_bulk:
            predicted = "/".join(meta[1].split(".")[:2])
            if predicted == domain:
                bulk_correct += 1
                stats["correct"] += 1
                if not before_ok:
                    wins += 1
                    stats["win"] += 1

    total = len(holdout)
    end_false = 0
    for index, row in enumerate(false_rows, 1):
        found = runtime.turn(row.get("q", ""), {})
        if not silent(found.get("module"), found.get("reply")):
            end_false += 1
        if index % 20 == 0:
            print("false {}/{}".format(index, len(false_rows)), flush=True)

    print("sample_holdout={} sample_false={}".format(total, len(false_rows)))
    print("answered_before={} ({:.3f})".format(answered_before, answered_before / total))
    print("answered_after={} ({:.3f})".format(answered_after, answered_after / total))
    print("bulk_answered={} ({:.3f})".format(bulk_answered, bulk_answered / total))
    print("bulk_correct={} ({:.3f})".format(bulk_correct, bulk_correct / total))
    print("coverage_win={} ({:.3f})".format(wins, wins / total))
    print("end_to_end_false_positive={} ({:.3f})".format(
        end_false, end_false / len(false_rows) if false_rows else 0.0))
    print("category | n | baseline_silent | bulk_fired | bulk_correct | coverage_win")
    for category in sorted(per_category):
        stats = per_category[category]
        print("{} | {} | {} | {} | {} | {}".format(
            category, stats["n"], stats["silent"], stats["fired"],
            stats["correct"], stats["win"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
