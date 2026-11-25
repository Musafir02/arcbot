import argparse
import ctypes
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from bot.bulk import match, loader

BUILD_BUDGET = 45.0
MATCH_BUDGET = 0.030
RSS_BUDGET = 700.0
TOP1_GATE = 0.90
FALSE_GATE = 0.05


def rss_mb():
    if os.name == "nt":
        import ctypes.wintypes

        class Counters(ctypes.Structure):
            _fields_ = [
                ("cb", ctypes.wintypes.DWORD),
                ("PageFaultCount", ctypes.wintypes.DWORD),
                ("PeakWorkingSetSize", ctypes.c_size_t),
                ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                ("PagefileUsage", ctypes.c_size_t),
                ("PeakPagefileUsage", ctypes.c_size_t),
            ]
        counters = Counters()
        counters.cb = ctypes.sizeof(counters)
        try:
            psapi = ctypes.WinDLL("psapi")
            kernel = ctypes.WinDLL("kernel32")
            kernel.GetCurrentProcess.restype = ctypes.wintypes.HANDLE
            reader = psapi.GetProcessMemoryInfo
            reader.argtypes = [ctypes.wintypes.HANDLE, ctypes.POINTER(Counters),
                               ctypes.wintypes.DWORD]
            reader.restype = ctypes.wintypes.BOOL
            if reader(kernel.GetCurrentProcess(), ctypes.byref(counters), counters.cb):
                return counters.WorkingSetSize / (1024.0 * 1024.0)
        except Exception:
            pass
    try:
        with open("/proc/self/status", "r", encoding="ascii") as handle:
            for line in handle:
                if line.startswith("VmRSS:"):
                    return float(line.split()[1]) / 1024.0
    except Exception:
        pass
    return 0.0


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


def sample_queries(limit=500):
    found = []
    for module_id, module in loader.iter_modules():
        if module is None:
            continue
        for patterns, answer in getattr(module, "ITEMS", ()):
            for pattern in patterns:
                found.append(pattern)
                if len(found) >= limit:
                    return found
    return found


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gate", action="store_true")
    parser.add_argument("--queries", type=int, default=500)
    parser.add_argument("--holdout", default=os.path.join("bot", "bulk", "holdout.jsonl"))
    parser.add_argument("--false", default=os.path.join("bot", "bulk", "false.jsonl"))
    args = parser.parse_args()
    match.reset()
    before = rss_mb()
    start = time.perf_counter()
    index = match.index()
    build = time.perf_counter() - start
    after = rss_mb()
    stats = match.stats()
    print(f"build={build:.3f}s rss_before={before:.1f}MB rss_after={after:.1f}MB")
    print(f"modules={stats['modules']} patterns={stats['patterns']} answers={stats['answers']} "
          f"tokens={stats['tokens']} skipped={stats['skipped']} bad={stats['bad_patterns']}")
    holdout = read_jsonl(os.path.join(ROOT, args.holdout))
    false_rows = read_jsonl(os.path.join(ROOT, args.false))
    if index is None:
        print("index is empty")
        if args.gate:
            return 1
        return 0
    probes = [row.get("q") for row in holdout if isinstance(row.get("q"), str)]
    if not probes:
        probes = sample_queries(args.queries)
    times = []
    for query in probes[:args.queries]:
        start = time.perf_counter()
        match.match_with_meta(query)
        times.append(time.perf_counter() - start)
    if times:
        times.sort()
        avg = sum(times) / len(times)
        p95 = times[min(len(times) - 1, int(len(times) * 0.95))]
        print(f"match_queries={len(times)} avg={avg * 1000:.2f}ms "
              f"p95={p95 * 1000:.2f}ms max={times[-1] * 1000:.2f}ms")
    else:
        avg = 0.0
        print("match_queries=0")
    top1 = None
    if holdout:
        right = 0
        for row in holdout:
            query = row.get("q")
            domain = row.get("domain")
            found = match.match_with_meta(query)
            if not found or not isinstance(domain, str):
                continue
            parts = found[1].split(".")
            predicted = "/".join(parts[:2])
            if predicted == domain:
                right += 1
        top1 = right / len(holdout)
        print(f"holdout={len(holdout)} top1={top1:.3f}")
    else:
        print("holdout missing")
    false_rate = None
    if false_rows:
        hits = 0
        for row in false_rows:
            if match.match(row.get("q", "")):
                hits += 1
        false_rate = hits / len(false_rows)
        print(f"false_set={len(false_rows)} false_positive={false_rate:.3f}")
    else:
        print("false set missing")
    problems = []
    if build > BUILD_BUDGET:
        problems.append(f"build {build:.3f}s over {BUILD_BUDGET:.1f}s")
    if times and avg > MATCH_BUDGET:
        problems.append(f"average match {avg * 1000:.2f}ms over {MATCH_BUDGET * 1000:.0f}ms")
    if after > RSS_BUDGET:
        problems.append(f"rss {after:.1f}MB over {RSS_BUDGET:.0f}MB")
    if top1 is not None and top1 < TOP1_GATE:
        problems.append(f"top1 {top1:.3f} under {TOP1_GATE:.2f}")
    if false_rate is not None and false_rate > FALSE_GATE:
        problems.append(f"false positive {false_rate:.3f} over {FALSE_GATE:.2f}")
    if problems:
        for line in problems:
            print("FAIL", line)
        if args.gate:
            return 1
        print("budgets not met")
        return 0
    print("budgets ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
