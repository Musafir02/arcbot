import re

from ..compose import pick

A_HARD_PAST = re.compile(
    r"\b(?:alcoholic|alcoholics|drinker|drinkers|addict(?:s|ed|ion)?|overdos(?:e|ed)|rehab|"
    r"prison|jail|divorce[ds]?|custody|abusive|abuser|widow|widowed|widower|estrang\w*|"
    r"homeless|bankrupt\w*|gambling|dementia|stillborn|stillbirth|miscarriage|miscarried|"
    r"car crash|in a crash|had a crash|bad crash|fatal crash|"
    r"marriage ended|marriage broke|relationship ended|walked out|left us)\b")

A_THE_PAST = re.compile(
    r"\b(?:was|were|had been|used to|grew up|growing up|as a kid|when i was|went to|"
    r"walked out|ended|ago|for a bit|for a while|for years|back then|in the end|at the time|"
    r"last (?:year|summer|winter|decade)|years back|after that)\b")
A_NEWS_ARRIVING = re.compile(
    r"\b(?:getting|going through|just told|just said|just heard|asked for|wants|wanting|"
    r"is leaving|has asked|separating|divorcing|this morning|tonight|right now|at the moment|"
    r"today)\b")

A_CLOSING_WORD = r"(?:fine|okay|ok|good|better|clean|dry|sober|sorted|happy|healthy|stable|" \
                  r"working|employed|a job|job|a house|a flat|a home|back on my feet|" \
                  r"still friends|still together|paid off|all paid)"
A_CLOSED = re.compile(
    r"\b" + A_CLOSING_WORD + r"\b[^.!?]{0,24}?\b(?:now|since|these days|any ?more)\b"
    r"|\b(?:now|since|these days)\b[^.!?]{0,24}?\b" + A_CLOSING_WORD + r"\b"
    r"|\b(?:dry|clean|sober|straight|off it)\b[^.!?]{0,16}?\b\d+\s*(?:years?|months?|decades?)\b"
    r"|\b(?:never looked back|put it behind me|put that behind me|moved on from it|"
    r"turned (?:it|things|my life) around|came out the other side|over it now|past it now|"
    r"in a better place|still friends|no longer)\b")

A_OWNED = frozenset("""
    my our his her their your mum mums mum's dad dads dad's mother father brother sister son
    daughter husband wife partner ex nan gran granny grandma grandad grandpa uncle aunt cousin
    parents family stepdad stepmum
""".split())
A_BETWEEN = frozenset("""
    i we ive weve been was were am had have has got did do done went never once really badly
    eventually finally long time terrible bad hard worst back then ago after before so that
    this it there with from at to a an the in into through out on off for of and but also both
    years year months weeks days month week twice again now still just
""".split())
A_SUBJECT = frozenset(("i", "we", "ive", "weve"))

A_LOSS = re.compile(
    r"\b(?:died|dies|dying|death|dead|passed away|funeral|buried|miscarriage|miscarried|"
    r"stillborn|stillbirth|widow|widows|widowed|widower|bereaved|bereavement)\b")


A_HARD_PAST_SAID = (
    "That is a heavy thing to have lived with. Say more about it if you want to.",
    "That is not a small thing to carry. I'm listening if you want to say more.",
    "That one leaves a mark. Go on if you want to.",
    "That is a lot to have been through. Tell me as much or as little as you like.",
)

PRIORITY = -980


def _hangs_on_the_person(clean, at):
    before = re.findall(r"[a-z']+", clean[:at])[-6:]
    for word in before[-4:]:
        if word in A_OWNED or (word.endswith("'s") and word[:-2] in A_OWNED):
            return True
    low = [word.replace("'", "") for word in before]
    seen = [i for i, word in enumerate(low) if word in A_SUBJECT]
    if seen:
        return all(word in A_BETWEEN for word in low[seen[-1] + 1:])
    return False


def _the_hard_thing(text, memory=None):
    clean = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    if not clean or "?" in clean:
        return ""
    understood = (memory or {}).get("understood") or {}
    if isinstance(understood, dict) and str(understood.get("kind") or "") == "question":
        return ""
    if not A_HARD_PAST.search(clean):
        return ""
    if not any(_hangs_on_the_person(clean, found.start())
               for found in A_HARD_PAST.finditer(clean)):
        return ""
    if A_NEWS_ARRIVING.search(clean) or not A_THE_PAST.search(clean):
        return ""
    if A_LOSS.search(clean):
        return ""
    if A_CLOSED.search(clean):
        return ""
    return clean


def takes_as_it_comes(text, memory):
    try:
        return bool(_the_hard_thing(text, memory))
    except Exception:
        return False


def respond(text, memory):
    try:
        clean = _the_hard_thing(text, memory)
        if not clean:
            return None
        return pick(A_HARD_PAST_SAID, memory, clean)
    except Exception:
        return None
