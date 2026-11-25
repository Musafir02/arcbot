import re

_SEEN = (r"(?:cares?|cared|listens?|listened|understands?|understood|notices?|noticed|"
         r"checks? (?:in|on me)|invites?|invited|includes?|included|sees? me|"
         r"wants? me|likes? me|loves? me|stands? up for me|is (?:there|around) for me|"
         r"are (?:there|around) for me|is on my side|are on my side|has time for me|"
         r"knows? (?:my name|me|i exist)|"
         r"have time for me|talks? to me|spoke to me|speaks to me|texts? me|rings? me|calls? me)")
_NOT_SEEN = (r"(?:invisible|unseen|unheard|overlooked|ignored|left out|an afterthought|"
             r"a spare part|like furniture|like a ghost|like a nobody|like i am not there|"
             r"like i'?m not there|like i do not exist|like i don'?t exist)")
OTHER = re.compile(r"\b(?:he|she|they|him|her|them|his|their|my (?:mum|mom|mam|dad|boss|son|"
                   r"daughter|partner|husband|wife|friend|sister|brother|colleague|manager|"
                   r"neighbour|neighbor|carer))\b")
NOT_ME = re.compile(r"\b(?:the (?:planet|climate|environment|government|club|team|company|"
                    r"shop|bins|bin|road|park|beach|library|bus|train)|them|it all|"
                    r"about (?:the|this|that)\s+(?:company|job|place|team|club))\b")
PROFESSIONAL = re.compile(
    r"\b(?:doctor|gp|surgery|consultant|nurse|midwife|health visitor|dentist|optician|"
    r"teacher|head ?teacher|tutor|lecturer|social worker|council|landlord|letting agent|"
    r"housing officer|jobcentre|dwp|bank|insurer)\b")
RISK = re.compile(
    r"\b(?:nobody|no ?one)\s+would\b"
    r"|\bif i (?:wasn'?t|was not|weren'?t|were not|am not|was |were )?(?:here|gone)\b"
    r"|\bif i died\b|\bbetter off (?:dead|without me)\b|\bkill myself\b"
    r"|\bend (?:it all|my life)\b|\bno reason to (?:live|go on)\b|\bnot be here any ?more\b")
DENIED = re.compile(
    r"\b(?:im|i['\u2019]?m|i\s+(?:feel|felt|am|get|end up))\s+(?:not|never|hardly|barely)\s+"
    r"(?:like\s+)?" + _NOT_SEEN + r"\b"
    r"|\b(?:nobody|no ?one|no-one|none of (?:my|them|the lot))\b(?:\s+\w+){0,3}\s+"
    r"(?:not|never|does?nt|do not|didnt|isnt|is not|wont|will not)\b")
BARE_VERB = re.compile(
    r"\b(?:nobody|no ?one|no-one|not one person|none of (?:my|them|the lot))"
    r"(?:\s+\w+){0,4}\s+"
    r"(?:(?:cares?|cared|listens?|listened|understands?|understood|notices?|noticed)"
    r"|(?:checks?|checked) (?:in|up))\b"
    r"(?P<tail>[^.!?,]{0,40})")
THE_PERSON = re.compile(
    r"^\s*(?:$"
    r"|(?:me|us)\b"
    r"|(?:in|up|on|with)\s+(?:me|us)\b"
    r"|(?:about|to|for|of|at|with)\s+(?:me|us)\b"
    r"|(?:about|to|for|of)\s+(?:how|what|whether|if|anything|nothing|whatever|any\s+of\s+it)"
    r"\s+(?:i|we)\b"
    r"|(?:how|whether|if)\s+(?:i|we)\b"
    r"|(?:in|up)\s+(?:on|with)\s+(?:me|us)\b"
    r"|(?:anymore|any ?more|at all|either|ever)\b"
    r"|(?:in|up)?\s*$)")
IGNORED_BY = re.compile(
    r"\b(?:ignored|overlooked|left out|unseen|unheard|not noticed)\s+by\s+"
    r"(?:the|a|an|my|our|his|her|their)\s+(\w+)")
PEOPLE = frozenset((
    "mum", "mom", "mam", "mother", "dad", "father", "parents", "family", "friends", "friend",
    "mates", "mate", "people", "everyone", "everybody", "anyone", "anybody", "someone",
    "somebody", "colleagues", "colleague", "coworkers", "neighbours", "neighbors", "kids",
    "children", "son", "daughter", "partner", "husband", "wife", "boyfriend", "girlfriend",
    "brother", "sister", "siblings", "group", "others", "crowd", "team", "class", "work",
    "housemates", "flatmates", "school", "them", "him", "her",
))
ME = re.compile(
    r"\b(?:nobody|no ?one|no-one|not one person|none of (?:my|them|the lot))"
    r"(?:\s+\w+){0,4}\s+" + _SEEN + r"\b"
    r"|\b(?:nobody|no ?one|no-one)\s+(?:cares?|cared)\b(?=\s*(?:[.!?,]|$))"
    r"|\b(?:nobody|no ?one|no-one)(?:\s+\w+){0,2}\s+(?:asks?|asked|notices?|noticed)\s+"
    r"(?:me\s+|us\s+)?(?:how|whether|if)\s+(?:i|we)\b"
    r"|\b(?:nobody|no ?one|no-one)(?:\s+\w+){0,4}\s+(?:asks?|asked)\s+(?:about|after)\s+me\b"
    r"|\b(?:nobody|no ?one|no-one)(?:\s+\w+){0,4}\s+bothers?\s+(?:with|about)\s+me\b"
    r"|\b(?:i\s+(?:feel|felt|am|get|end up)|im|i['\u2019]m)\b(?:\s+\w+){0,2}\s+(?:like\s+)?"
    + _NOT_SEEN + r"\b"
    r"|\b(?:feel|feels|felt|feeling)\s+(?:like\s+)?" + _NOT_SEEN + r"\b")
NAMED_PEOPLE = (
    r"(?:my|our)\s+(?:best\s+|old\s+|oldest\s+|closest\s+|closer\s+|own\s+|new\s+|"
    r"eldest\s+|older\s+|younger\s+|little\s+|big\s+)?(?:friends?|mates?|family|mum|mom|"
    r"mam|mother|dad|father|parents|"
    r"sister|brother|siblings|husband|wife|partner|boyfriend|girlfriend|kids|children|"
    r"son|daughter|flatmates?|housemates?|colleagues?|coworkers?|workmates?|neighbours?|"
    r"neighbors?|relatives|cousins?|in-?laws)"
    r"|the\s+(?:girls|boys|lads|lasses|others|kids|team|group|people|family|mums|parents)"
    r"|everyone|everybody")
NAMED_REGARD = (
    r"(?:likes?|loves?|wants?|cares?(?:\s+about)?|notices?|needs?|listens?\s+to|"
    r"bothers?\s+with|invites?|includes?|misses?|respects?|trusts?|fancies|talks?\s+to|"
    r"texts?|rings?|calls?)")
NAMED_OVER = re.compile(r"\b(?:want|love|need|miss|fancy)\s+me\s+(?:back|any\s?more)\b")
NAMED_TOLD = re.compile(r"\b(?:likes?|loves?|wants?|needs?|asks?)\s+(?:me|us)\s+to\s+\w+")
NAMED = re.compile(
    r"\b(?:{people})\b(?:\s+\w+){{0,2}}\s+"
    r"(?:dont|don'?t|doesnt|doesn'?t|didnt|didn'?t|never|wont|won'?t|do not|does not|"
    r"did not|will not)\s+(?:\w+\s+){{0,2}}{regard}\s+(?:me|us)\b".format(
        people=NAMED_PEOPLE, regard=NAMED_REGARD))
LINES = (
    "That is a lonely place to be, and being surrounded by people does not fix it. Who is one "
    "person who does see you?",
    "I hear you. Talking and getting nothing back wears a person down. How long has it felt "
    "like this?",
    "Not being noticed by the people near you is its own kind of hard. Where does it bite most "
    "- home, work, or with friends?",
    "That would get to anyone, and it is not about being easy to overlook. Is there one person "
    "you could say this to?",
)


def reads(clean):
    text = " ".join(str(clean or "").lower().split())
    if not text or RISK.search(text):
        return False
    named = (bool(NAMED.search(text)) and not NAMED_OVER.search(text)
             and not NAMED_TOLD.search(text))
    if not named and not ME.search(text):
        return False
    if DENIED.search(text):
        return False
    if named:
        return not PROFESSIONAL.search(text)
    if NOT_ME.search(text) or OTHER.search(text) or PROFESSIONAL.search(text):
        return False
    bare = BARE_VERB.search(text)
    if bare and not THE_PERSON.match(bare.group("tail")):
        return False
    by = IGNORED_BY.search(text)
    if by and by.group(1) not in PEOPLE:
        return False
    return True
