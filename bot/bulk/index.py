import heapq
import math
from array import array

from . import loader
from .text import pattern_tokens, tokens

MAX_CANDIDATES = 12000
STAGE1_KEEP = 400
MIN_PAT_COV = 0.70
MIN_Q_COV = 0.50
MIN_IDF_COV = 0.55
MIN_SCORE = 0.68
HIGH_SCORE = 0.88
MIN_GAP = 0.04


class Index:

    __slots__ = ("modules", "answers", "answer_of", "module_of", "item_of", "offsets",
                 "pattern_tokens", "postings", "token_ids", "df", "idf",
                 "pattern_count", "skipped", "bad_patterns", "max_idf")

    def __init__(self, modules, answers, answer_of, module_of, item_of, offsets, pattern_tokens,
                 postings, token_ids, df, idf, skipped, bad_patterns):
        self.modules = modules
        self.answers = answers
        self.answer_of = answer_of
        self.module_of = module_of
        self.item_of = item_of
        self.offsets = offsets
        self.pattern_tokens = pattern_tokens
        self.postings = postings
        self.token_ids = token_ids
        self.df = df
        self.idf = idf
        self.pattern_count = len(offsets) - 1
        self.skipped = skipped
        self.bad_patterns = bad_patterns
        self.max_idf = max(idf) if idf else 1.0

    def stats(self):
        return {
            "modules": len(self.modules),
            "patterns": self.pattern_count,
            "answers": len(self.answers),
            "skipped": self.skipped,
            "bad_patterns": self.bad_patterns,
            "tokens": len(self.token_ids),
        }

    def match(self, text):
        found = self.match_with_meta(text)
        return found[0] if found else None

    def match_with_meta(self, text):
        try:
            return self._match(text)
        except Exception:
            return None

    def _match(self, text):
        if self.pattern_count == 0:
            return None
        query = tokens(text)
        if len(query) < 2:
            return None
        ordered = []
        seen = set()
        for token in query:
            if token in seen:
                continue
            seen.add(token)
            ordered.append(token)
        known = []
        total_idf = 0.0
        for token in ordered:
            token_id = self.token_ids.get(token)
            if token_id is None:
                total_idf += self.max_idf
                continue
            known.append(token_id)
            total_idf += self.idf[token_id]
        if len(known) < 2 or total_idf <= 0.0:
            return None
        query_len = len(ordered)
        query_set = set(known)
        query_seq = [token_id for token_id in (self.token_ids.get(token) for token in ordered)
                     if token_id is not None]
        query_pairs = set(zip(query_seq, query_seq[1:]))
        lists = sorted(((len(self.postings[token_id]), token_id) for token_id in known))
        candidates = self._candidates(lists)
        if not candidates:
            return None
        offsets = self.offsets
        pattern_tokens = self.pattern_tokens
        idf = self.idf
        scored = []
        for pattern in candidates:
            start = offsets[pattern]
            end = offsets[pattern + 1]
            length = end - start
            if length < 2:
                continue
            matched = set()
            for at in range(start, end):
                token_id = pattern_tokens[at]
                if token_id in query_set:
                    matched.add(token_id)
            inter = len(matched)
            pat_cov = inter / length
            if pat_cov < MIN_PAT_COV:
                continue
            q_cov = inter / query_len
            if q_cov < MIN_Q_COV:
                continue
            idf_cov = sum(idf[token_id] for token_id in matched) / total_idf
            if idf_cov < MIN_IDF_COV:
                continue
            pre = 0.55 * pat_cov + 0.25 * q_cov + 0.20 * idf_cov
            scored.append((pre, pattern, pat_cov, length, q_cov, idf_cov))
        if not scored:
            return None
        top = heapq.nlargest(STAGE1_KEEP, scored, key=lambda row: (row[0], row[3]))
        final = []
        for pre, pattern, pat_cov, length, q_cov, idf_cov in top:
            start = offsets[pattern]
            end = offsets[pattern + 1]
            pairs = 0
            for at in range(start, end - 1):
                if (pattern_tokens[at], pattern_tokens[at + 1]) in query_pairs:
                    pairs += 1
            adj = pairs / max(1, length - 1)
            score = 0.40 * pat_cov + 0.20 * q_cov + 0.15 * adj + 0.25 * idf_cov
            if score < MIN_SCORE:
                continue
            module = self.modules[self.module_of[pattern]][0]
            final.append((score, length, module, pattern))
        if not final:
            return None
        final.sort(key=lambda row: (-row[0], -row[1], row[2]))
        best = final[0]
        if best[0] < HIGH_SCORE and len(final) > 1 and best[0] - final[1][0] < MIN_GAP:
            return None
        pattern = best[3]
        return (self.answers[self.answer_of[pattern]], self.modules[self.module_of[pattern]][0],
                self.item_of[pattern], round(best[0], 4))

    def _candidates(self, lists):
        if not lists:
            return set()
        first_len, first_id = lists[0]
        if first_len > MAX_CANDIDATES:
            found = set(self.postings[first_id])
            for length, token_id in lists[1:]:
                found.intersection_update(self.postings[token_id])
                if len(found) <= MAX_CANDIDATES:
                    break
            if len(found) > MAX_CANDIDATES:
                return set()
            return found
        found = set(self.postings[first_id])
        for length, token_id in lists[1:]:
            if len(found) >= MAX_CANDIDATES:
                break
            if len(found) + len(self.postings[token_id]) > MAX_CANDIDATES:
                break
            found.update(self.postings[token_id])
        return found


def _valid_module(module, module_id):
    try:
        if getattr(module, "MODULE", None) != module_id:
            return False
        items = getattr(module, "ITEMS", None)
        if not isinstance(items, (tuple, list)) or len(items) != 10:
            return False
        for item in items:
            if not isinstance(item, (tuple, list)) or len(item) != 2:
                return False
            patterns, answer = item
            if not isinstance(patterns, (tuple, list)) or len(patterns) != 10:
                return False
            if not isinstance(answer, str) or not answer.strip():
                return False
        return True
    except Exception:
        return False


def build(root=None):
    base = root or loader.data_root()
    modules = []
    answers = []
    answer_of = []
    module_of = []
    item_of = []
    offsets = [0]
    flat = []
    postings = []
    token_ids = {}
    skipped = 0
    bad_patterns = 0
    pattern_count = 0
    ids_get = token_ids.get
    postings_append = postings.append
    flat_append = flat.append
    for module_id, module in loader.iter_modules(base):
        if module is None or not _valid_module(module, module_id):
            skipped += 1
            continue
        module_index = len(modules)
        modules.append((module_id, getattr(module, "ANSWERS", ()),
                        getattr(module, "PRIORITY", 0)))
        for item_index, item in enumerate(module.ITEMS):
            patterns, answer = item
            answer_index = len(answers)
            answers.append(answer)
            for pattern in patterns:
                found = pattern_tokens(pattern)
                if len(found) < 2:
                    bad_patterns += 1
                    continue
                found = tuple(dict.fromkeys(found))
                pattern_index = pattern_count
                pattern_count += 1
                for token in found:
                    token_id = ids_get(token)
                    if token_id is None:
                        token_id = len(postings)
                        token_ids[token] = token_id
                        postings_append([])
                    postings[token_id].append(pattern_index)
                    flat_append(token_id)
                offsets.append(len(flat))
                answer_of.append(answer_index)
                module_of.append(module_index)
                item_of.append(item_index)
    count = len(offsets) - 1
    df = [len(found) for found in postings]
    idf = [math.log((count + 1.0) / (seen + 1.0)) + 1.0 for seen in df]
    return Index(modules, answers, array("I", answer_of), array("I", module_of),
                 array("I", item_of), array("I", offsets), array("I", flat),
                 [array("I", found) for found in postings], token_ids, df, idf,
                 skipped, bad_patterns)
