import argparse
import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from bot import runtime

QUERIES = [
    "who are you?",
    "what is the capital of france?",
    "how long should i boil an egg?",
    "why is my cake sinking in the middle?",
    "can i freeze cooked rice?",
    "how do i stop my cat scratching the sofa?",
    "what tyre pressure do i need for a long drive?",
    "how often should i water a snake plant?",
    "how do i remove a red wine stain?",
    "how much does a boiler service cost?",
    "how do i get rid of slugs in the garden?",
    "what should i pack for a week in iceland?",
    "my laptop battery drains fast, what can i do?",
    "how do i whiten my teeth at home?",
    "how long does it take to learn spanish?",
    "can i use olive oil instead of butter in brownies?",
    "why does my bread come out dense?",
    "how do i fix a dripping tap?",
    "what should i do if my dog eats chocolate?",
    "how do i improve my credit score?",
    "what is the best time to visit japan?",
    "how do i change a tyre?",
    "what is a good beginner guitar?",
    "how many hours of sleep do i need?",
    "how do i clean a washing machine?",
    "what is the best way to save money?",
    "how do i write a cv?",
    "how do i treat a sore throat?",
    "what should i do in a power cut?",
    "how do i cook rice without it going sticky?",
]


def run(query):
    random.seed(0)
    return runtime.turn(query, {})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--baseline", default=os.path.join("tools", "baseline.json"))
    args = parser.parse_args()
    path = os.path.join(ROOT, args.baseline)
    if args.write:
        rows = []
        for query in QUERIES:
            found = run(query)
            rows.append({"q": query, "reply": found["reply"], "module": found["module"]})
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(rows, handle, indent=2, ensure_ascii=True)
            handle.write("\n")
        print(f"wrote {len(rows)} rows to {path}")
        return 0
    if not os.path.isfile(path):
        print(f"missing baseline: {path}")
        return 1
    with open(path, "r", encoding="utf-8") as handle:
        rows = json.load(handle)
    bad = 0
    for row in rows:
        found = run(row["q"])
        if found["reply"] != row["reply"]:
            bad += 1
            print(f"MISMATCH {row['q']}")
            print(f"  expected {row['reply']!r}")
            print(f"  actual   {found['reply']!r}")
    print(f"checked={len(rows)} mismatches={bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
