import random
import re

from ..compose import pick

from . import last_bot, recent

_LEAD = r"^(?:(?:ok|okay|fine|right|well|so|then|hmm|ha)[, ]+)*"
_PICK_ASK = re.compile(
    _LEAD +
    r"(?:"
    r"(?:you|u|yous)[ ]?(?:pick|choose|decide|select|choose one|pick one|decide for me)"
    r"|(?:you|u) (?:can )?(?:pick|choose|decide)(?: (?:one|it|for me|the (?:one|rest|\w+)))?"
    r"|your (?:call|choice|pick|decision)"
    r"|(?:i'?ll |i will |i'?d )?let you (?:pick|choose|decide)(?: (?:one|it|for me|this time))?"
    r"|(?:can|could|will|would) you (?:pick|choose|decide)(?: (?:one|it|for me))?"
    r"|up to you|over to you|you tell me|you know best|surprise me"
    r"|(?:i )?(?:don'?t|do not) mind[, ]+you (?:pick|choose|decide)"
    r"|(?:either|any|whatever)(?: one| of (?:them|those|these))?(?: is| are)? (?:fine|good|ok|okay)"
    r"(?:[, ]+(?:you|u) (?:pick|choose|decide))?"
    r"|(?:you|u) (?:pick|choose|decide)(?:[, ]+(?:i )?(?:don'?t|do not) mind)?"
    r")"
    r"(?: (?:then|please|thanks|for me|between (?:them|those|these|the two)))?"
    r"[.?!]*$", re.I)

_CLAUSE = re.compile(
    r"\b(?:i|i'll|i'd|you|you'll|we|they|tell me|let me|if|but|because|which|whichever|whatever|"
    r"search|google|not sure|don'?t know)\b", re.I)

_TAIL_STRIP = re.compile(r"[\s.;:,]+$")
_STEP = re.compile(r"\b(?:with|then|until|after|before|for \d|at \d|under|onto|over|into|"
                   r"using|while|once)\b", re.I)
_NOT_A_THING = re.compile(r"\b(?:so|are|is|was|were|works|tastes|means|are)\b|^-", re.I)


def _clean_option(piece):
    piece = piece.strip(" \t*_-\u2014")
    piece = re.sub(r"^(?:or|and|either|then|else)\s+", "", piece, flags=re.I)
    piece = _TAIL_STRIP.sub("", piece)
    words = piece.split()
    if not piece or len(words) > 11 or len(piece) > 70:
        return ""
    if _CLAUSE.search(piece):
        return ""
    if piece[-1:] in "?!:" or piece.endswith("..."):
        return ""
    return piece


def _from_italics(text):
    found = re.findall(r"\*([^*\n]{2,40})\*(?: ([^,;.\n]{1,30}))?", text)
    options = []
    for title, tail in found:
        title = _clean_option(title)
        if not title:
            continue
        tail = "" if _CLAUSE.search(tail or "") else (tail or "")
        options.append(_clean_option((title + " " + tail).strip()) or title)
    return options


def _segment(text):
    body = text
    for sep in (":", " \u2014 ", " - "):
        head, found, tail = body.rpartition(sep)
        if found and len(tail.split()) >= 2:
            return tail
    return body


def _from_list(text):
    body = _segment(text)
    body = re.split(r"\.\s+[A-Z]", body)[0]

    def things(pieces, steps=False):
        out = []
        for piece in pieces:
            if _NOT_A_THING.search(piece) or (steps and _STEP.search(piece)):
                continue
            option = _clean_option(piece)
            if option:
                out.append(option)
        return out

    if " or " in body.lower() or ";" in body:
        pieces = [p for p in re.split(r";", body) if p.strip()]
        options = things(pieces)
        if len(options) < 2:
            options = things([p for p in re.split(r",\s+|\s+or\s+|\s+and\s+", body) if p.strip()])
        if len(options) >= 2:
            return options
    comma = [o for o in things([p for p in re.split(r",\s+", body) if p.strip()], steps=True)
             if len(o.split()) <= 8]
    return comma if len(comma) >= 3 else []


def _from_labels(text):
    labels = []
    for label in re.findall(r"(?:^|[.;]\s+)([A-Za-z][^:.;\n]{2,30}):", text):
        option = _clean_option(label)
        if option:
            labels.append(option)
    seen, unique = set(), []
    for label in labels:
        if label.lower() not in seen:
            seen.add(label.lower())
            unique.append(label)
    return unique


def _from_question(text):
    if not text.rstrip().endswith("?") or " or " not in text.lower():
        return []
    body, again = re.subn(r"^\W*(?:so |then )?(?:would you rather|would you prefer|shall we|"
                          r"do you want|do you fancy|which would you rather|are you (?:thinking|"
                          r"leaning)|how about|which one)\s+", "", text.strip(), flags=re.I)
    if not again:
        return []
    body = body.rstrip("?")
    return [_clean_option(p) for p in re.split(r"\s+or\s+", body) if _clean_option(p)]


def options_in(reply):
    if not reply:
        return []
    text = " ".join(str(reply).split())
    for reader in (_from_italics, _from_labels, _from_question, _from_list):
        options = reader(text)
        seen, unique = set(), []
        for option in options:
            key = option.lower()
            if key not in seen:
                seen.add(key)
                unique.append(option)
        if len(unique) >= 2:
            return unique
    return []


def asks_for_a_pick(text):
    low = " ".join(str(text or "").lower().split())
    return bool(_PICK_ASK.match(low))


PICKS = (
    "My pick: {option}.",
    "I'd say {option}.",
    "If it were me: {option}.",
    "{option} \u2014 that's the one I'd choose.",
)


_ASKED = re.compile(r"^(?:\W*(?:what|which|who|when|where|why|how|any|anyone|anything|can|could|"
                    r"should|would|do|does|did|is|are|shall|give me|tell me|suggest|recommend)\b"
                    r"|.*\?\s*$)", re.I)


def _from_user_line(memory):
    turns = recent(memory, 1)
    line = " ".join(str((turns[-1].get("user") if turns else "") or "").lower().split())
    if " or " not in line:
        return []
    body = re.sub(r"^\W*(?:(?:so|ok|okay|but)[, ]+)?(?:should|could|do|would|shall|can|will)\s+"
                  r"(?:i|we)\s+|^\W*(?:is it better to|which is better,?|what about|"
                  r"is it worth)\s+", "", line.rstrip("?"))
    options = []
    for piece in re.split(r"\s+or\s+", body):
        option = _clean_option(piece)
        if option and len(option.split()) <= 5:
            options.append(option)
    if len(options) < 2:
        return []
    first = {o.split()[0] for o in options}
    if len(first) == 1 and all(len(o.split()) > 1 for o in options):
        rest = [" ".join(o.split()[1:]) for o in options]
        if all(r[:1].isalpha() for r in rest):
            options = rest
    if len(options[0].split()) > 1 and re.match(r"(?:a|an|the)\b", options[1]):
        options = [" ".join(o.split()[1:]) if len(o.split()) > 1 else o for o in options]
    return options


def _asked_for_help(memory, n=4):
    for turn in reversed(recent(memory, n)):
        line = " ".join(str(turn.get("user") or "").split())
        if line and _ASKED.match(line):
            return True
    return False


_BARE_HAND_BACK = re.compile(
    r"^(?:(?:ok|okay|fine|right|well|so|then|and|hmm|ha)[, ]+)*"
    r"(?:"
    r"(?:i\s)?(?:don'?t|do not|dont) mind(?: (?:really|either|much|at all|tbh))?"
    r"|(?:i'?m|im) (?:easy|not bothered|not fussed)(?: (?:either|really|tbh))?"
    r"|(?:either|any|anything)(?: one| of (?:them|those|these))?"
    r"(?: ?(?:is|are)? ?(?:fine|good|ok|okay|works))?"
    r"|(?:any|either) of (?:them|those|these)"
    r"|whatever (?:you|u) (?:think|reckon|say|like)"
    r")"
    r"[.?!]*$", re.I)

_PICK_SAID = (
    re.compile(r"^(?:my pick:|if it were me:|i'?d say|i'?d go with|i would go with) *(.+?)[.!]*$", re.I),
    re.compile(r"^(.+?)\s+\u2014\s+that's the one i'?d choose[.!]*$", re.I),
)
_INSIST_LEAD = r"then it is|my pick is still|same pick:|i'?ll decide then:|go with"
_INSIST_SAID = re.compile(r"^(?:%s) *(.+?)[.!](?:\s|$)" % _INSIST_LEAD, re.I)
_INSIST_WRAP = re.compile(r"^(?:%s) *(.+?)[.!]*$" % _INSIST_LEAD, re.I)

INSISTED = (
    "Then it is {option}. You can blame me if it is wrong.",
    "My pick is still {option}.",
    "Same pick: {option}.",
    "I'll decide then: {option}.",
    "Go with {option}. Someone has to choose, so I have.",
    "Then it is {option}. There is nothing else to weigh up.",
)
BY_A_RULE = (
    "Then take the cheapest one that fits the time you have, and sort the details as you go.",
    "Go with the one you would be annoyed to lose. The rest is noise.",
    "Pick the first one you liked the sound of. That instinct is usually right.",
    "Then choose the one that leaves you the most time. The rest sorts itself out.",
)


def _peeled(option):
    option = option.strip(" *_\u2014,.;:")
    for _ in range(3):
        match = _INSIST_WRAP.match(option)
        if not match:
            break
        option = match.group(1).strip(" *_\u2014,.;:")
    return option


_A_MEASURE = re.compile(
    r"\b(?:\d+(?:\.\d+)?\s*(?:cal|calories|kcal|g|kg|mg|ml|l|gram|grams|kilo|kilos|litre|litres"
    r"|min|mins|minutes|hour|hours|degrees?|percent|%)|per\s+\d)", re.I)


def _readable(options):
    keep = []
    for option in options:
        text = str(option).strip()
        if not text or len(text.split()) > 6 or _A_MEASURE.search(text):
            continue
        keep.append(option)
    return keep


def _already_picked(memory, back=3):
    for turn in reversed(recent(memory, back)):
        said = " ".join(str(turn.get("bot") or "").split())
        if not said or said.endswith("?"):
            continue
        for pattern in (_INSIST_SAID,) + _PICK_SAID:
            match = pattern.match(said)
            if not match:
                continue
            option = _peeled(match.group(1))
            if option and len(option.split()) <= 8 and "?" not in option:
                return option
    return None


def reply_for(text, memory):
    asked = asks_for_a_pick(text)
    shrug = False if asked else bool(
        _BARE_HAND_BACK.match(" ".join(str(text or "").lower().split())))
    if not (asked or shrug):
        return None
    turns = memory.get("turns") or []
    picked = _already_picked(memory)
    options = _readable(options_in(last_bot(memory)))
    if len(options) < 2:
        options = _readable(_from_user_line(memory))
    if len(options) >= 2:
        short = [o for o in options if len(o.split()) <= 8]
        options = short or options
        chosen = random.Random(len(turns)).choice(options)
        line = random.Random(len(turns) + 7).randrange(len(PICKS))
        said = PICKS[line].format(option=chosen)
        return said[:1].upper() + said[1:]
    if picked:
        return pick(INSISTED, memory, seed_text=text).format(option=picked)
    if _asked_for_help(memory):
        return pick(BY_A_RULE, memory, seed_text=text)
    return None


DECIDING_ASK = re.compile(
    r"^(?:(?:ok|okay|fine|right|well|so|then|and|but|hmm|ah)[, ]+)*"
    r"(?:(?:what|which)(?:\s+(?:one|thing|of them))?\s+(?:did|do|have|had)\s+(?:i|we)\s+"
    r"(?:decide|decided|settle|settled|pick|picked|choose|chose|go for|go with|"
    r"end up with|end up getting|come down to|land on|get|got|buy|bought)"
    r"|(?:so\s+)?what\s+(?:am|are)\s+(?:i|we)\s+(?:getting|having|going for|picking|"
    r"ending up with|settling on))"
    r"\b[^?.!]{0,24}[?.!]*$", re.I)

STRONG_CHANGE = re.compile(
    r"\b(?:actually|instead|on second thoughts?|changed my mind|then again|make it|"
    r"i(?:'| a)?ve decided|i decided|we decided|we(?:'| a)?ve decided|decided on|"
    r"settled on|settling on|i(?:'| a)?ve settled|we(?:'| a)?ve settled)\b", re.I)

WEAK_CHANGE = re.compile(
    r"\b(?:go with|going with|go for|going for|went with|went for|end up with|ended up with|"
    r"land on|landed on|opt for|opted for|pick|picked|picks|choose|chose|chosen)\b", re.I)

CHANGED_IT = re.compile(STRONG_CHANGE.pattern + "|" + WEAK_CHANGE.pattern, re.I)

CUE = frozenset("""no nope ok okay so then well and but lets let fine right actually instead
    hmm ah yes yeah""".split())

SECOND_FRAME = re.compile(
    r"^\W*(?:(?:make (?:it|that)|go (?:with|for)|going (?:with|for)|decided on|settled on|"
    r"settling on|(?:i|we)(?:'ve|'a)?ve?\s+(?:decided|settled)(?:\s+(?:on|to))?|"
    r"lets|let us|to (?:get|go|buy|have)|just|then|so|ok|okay|instead|actually)\b[\s,]*)+",
    re.I)

NOT_AT_THE_START = frozenset("""up out off on down back in into onto over around through about
    at by from with without for to of after before since until away along across""".split())

DEFINITE = frozenset("the this that these those my our your his her their".split())

TRAIL = frozenset("""instead actually really probably maybe i think though anyway honestly then
    now please thanks for with to on in at about of and but so also too both""".split())

CORRECTION = re.compile(
    r"^\W*(?:its|it's|it is|theyre|they're|they are|theres|there's|thats|that's|"
    r"hes|he's|shes|she's|im|i'm|i am|we're|we are)\b", re.I)

A_CHOICE = re.compile(
    r"\b(?:thinking (?:of|about)|consider(?:ing)?|deciding|decided between|chose between|"
    r"choosing between|torn between|looking at|can'?t decide|undecided|options?|"
    r"should i (?:get|go|buy|have|pick|choose)|which (?:one|would)|instead of|whether)\b",
    re.I)

BARE_CHANGE = frozenset(("actually", "rather"))

DETERMINERS = frozenset("a an the my our your his her their this that".split())

NO_THEN_THING = re.compile(r"^\W*(?:no|nope)\b[\s,!]+", re.I)

CORRECTION_OPENER = re.compile(r"^\W*(?:(?:actually|oh|sorry|ok|okay|well|right|wait)\s+[,.]?\s*)*"
                               r"(?:no|nope)\b[\s,.!-]+", re.I)
NO_CONTINUES = frozenset("longer more way thanks thank such bother idea need chance matter doubt".split())

VERBISH = frozenset("""
like likes liked love loved hate hated want wanted need needed think thought know knew
said say says tell told do did does done be been being is are was were will would can
could should might have has had get got go went feel felt seems seem sound sounds work works
""".split())

NOT_THE_THING = frozenset("""
a an the my our your his her their this that these those it its it's them they he she hes shes
one ones you your yours i im ive we us there here
to get getting have having buy buying go going for with on about at in
of and or but so then now instead actually really probably maybe i think we
something anything nothing else more better different
""".split())

SETTLED = (
    "{thing} \u2014 that's the one you settled on.",
    "You settled on {thing}.",
    "The one you landed on was {thing}.",
    "{thing}, as far as this chat goes.",
)


def _the_thing_in(line):
    weak = False
    said = STRONG_CHANGE.search(line)
    if said is None:
        said = WEAK_CHANGE.search(line)
        weak = said is not None
    if said is None:
        said = NO_THEN_THING.match(line)
        if not said or len(line[said.end():].split()) > 3:
            return ""
    elif weak and not _hands_the_choice_over(line[:said.start()]):
        return ""
    tail = line[said.end():]
    for _ in range(2):
        opened = CORRECTION_OPENER.match(tail)
        rest = tail[opened.end():] if opened else ""
        if not rest.strip() or rest.split()[0].lower().strip(",.!?") in NO_CONTINUES:
            break
        tail = rest
    for _ in range(3):
        frame = SECOND_FRAME.match(tail)
        if not frame:
            break
        tail = tail[frame.end():]
    if CORRECTION.match(tail):
        return ""
    words_after = [w.strip(",.!?;:'\"()") for w in tail.split()]
    kept = []
    lead = ""
    for word in words_after:
        if not word:
            continue
        if word.lower() in DETERMINERS and not kept:
            lead = word.lower()
            continue
        if word.lower() in NOT_THE_THING and not kept:
            continue
        if kept and word.lower() in TRAIL:
            break
        kept.append(word)
        if len(kept) == 3:
            break
    if not kept and said.group(0).lower() == "instead":
        return _the_thing_in(line[:said.start()])
    if not kept or kept[0].lower() in VERBISH:
        return ""
    if kept[0].lower() in NOT_AT_THE_START:
        return ""
    if weak and lead not in DEFINITE:
        return ""
    return " ".join(([lead] if lead else []) + kept)


def _hands_the_choice_over(before):
    words_ = [w for w in re.findall(r"[A-Za-z']+", before or "")]
    if not words_:
        return True
    return len(words_) <= 2 and all(word.lower() in CUE for word in words_)


def settled_on(memory):
    for turn in reversed(recent(memory, 3)):
        line = " ".join(str(turn.get("user") or "").split())
        if not line:
            continue
        thing = _the_thing_in(line)
        if not thing:
            continue
        if _bare_change(line) and not _a_choice_in_hand(memory, line):
            continue
        return thing
    return ""


def _bare_change(line):
    text = str(line or "")
    for match in STRONG_CHANGE.finditer(text):
        if match.group(0).strip().lower() not in BARE_CHANGE:
            return ""
    first = STRONG_CHANGE.search(text)
    return first.group(0).strip().lower() if first else ""


def _a_choice_in_hand(memory, this):
    for turn in reversed(recent(memory, 8)):
        line = " ".join(str(turn.get("user") or "").split())
        if not line or line == this:
            continue
        if A_CHOICE.search(line) or " or " in line.lower():
            return True
    return False


def the_decision(text, memory):
    line = " ".join(str(text or "").split())
    if not DECIDING_ASK.match(line):
        return None
    thing = settled_on(memory)
    if not thing:
        return None
    said = _a_way_of_saying_it(thing, memory)
    return said[:1].upper() + said[1:]


def _a_way_of_saying_it(thing, memory):
    last = " ".join(str(last_bot(memory) or "").split()).lower()
    frames = [frame for frame in SETTLED if frame.format(thing=thing).lower() != last]
    frames = frames or list(SETTLED)
    return random.Random(len(memory.get("turns") or [])).choice(frames).format(thing=thing)


def offered(memory, n=1):
    out = []
    for turn in recent(memory, n):
        out.extend(options_in(turn.get("bot") or ""))
    return out
