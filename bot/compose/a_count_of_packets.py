import re

COUNT = (r"(?:two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d{1,3}|"
         r"a\s+couple\s+of|a\s+few|several|a\s+handful\s+of)")
CONTAINER = (r"(?:packets?|packs?|boxes|box|bottles?|blisters?|strips?|sleeves?|sachets?|"
             r"handfuls?)")
DRUG = (r"(?:pills|tablets|paracetamol|ibuprofen|painkillers|analgesics|meds|medicines?|"
        r"sleeping\s+pills|antidepressants|tranquill?i[sz]ers?|insulin|codeine|co[\s-]?codamol|"
        r"codamol|tramadol|morphine|diazepam|cough\s+medicine|painkillers?)")
VERB = (r"(?:swallowed|swallowing|drank|drunk|eaten|ate|took|taken|downed|inhaled|popped|necked|"
        r"finished|used|washed\s+down|swilled|gulped|gave|given|handed)")

PACKETS = (COUNT + r"\s+" + CONTAINER + r"\s+of\s+[^.?!]{0,15}\b" + DRUG + r"\b")

TAKEN = re.compile(r"\b" + VERB + r"\b[^.?!]{0,25}\b" + PACKETS)

NO_VERB = re.compile(r"\b" + PACKETS +
                     r"[^.?!]{0,25}\b(?:feel|felt|feeling|sick|ill|dizzy|drowsy|sleepy|vomit\w*|"
                     r"throwing\s+up|shak\w*|blurry|off\s+my\s+face|can'?t\s+stay\s+awake|"
                     r"sleeping\s+all\s+day|swallow\w*|and\s+then\s+i|and\s+now\s+i)\b")

AN_ANIMAL = (r"(?:dogs?|pupp(?:y|ies)|cats?|kittens?|rabbits?|bunn(?:y|ies)|hamsters?|budgies?|"
             r"birds?|parrots?|horses?|pon(?:y|ies)|guinea\s+pigs?|gerbils?|ferrets?|tortoises?|"
             r"animals?|pets?)")
AN_ANIMAL_TOOK = re.compile(r"\b" + AN_ANIMAL + r"\b[^.?!]{0,25}\b" + VERB + r"\b")

PACKET_WORDS_BEFORE = re.compile(r"\b(?:buy|buys|buying|bought|shop|shopping|order|ordered|"
                                 r"prescription|prescribed|pharmacy|chemist|doctor|gp|nurse|"
                                 r"getting|pick\s+up|picked\s+up|stock|stocked\s+up|spare|"
                                 r"first\s+aid)\b[^.?!]{0,30}" + PACKETS)
PACKET_WORDS_ON = re.compile(r"\b" + PACKETS +
                             r"[^.?!]{0,25}\b(?:for\s+(?:the|a|my)\s+(?:trip|holiday|weekend|"
                             r"flight|journey|kids)|on\s+holiday|on\s+business|to\s+take\s+away|"
                             r"away\s+with\s+me|in\s+my\s+(?:bag|pocket|suitcase|handbag|purse)|"
                             r"in\s+the\s+(?:cupboard|drawer|cabinet|glovebox)|at\s+home|"
                             r"left\s+over|spare|abroad)\b")
STOCK_PLACE = re.compile(r"\b(?:in|inside|kept\s+in|keep\s+in|keeps\s+in|have|has|got|carry|"
                         r"carrying|stash)\b[^.?!]{0,20}\b(?:cupboard|drawer|cabinet|shelf|"
                         r"shelves|bag|pocket|purse|glovebox)\b")


def is_a_dose(text):
    line = " ".join((text or "").lower().split())
    if not line:
        return False
    if AN_ANIMAL_TOOK.search(line):
        return False
    if (PACKET_WORDS_BEFORE.search(line) or PACKET_WORDS_ON.search(line)
            or STOCK_PLACE.search(line)):
        return False
    return bool(TAKEN.search(line) or NO_VERB.search(line))
