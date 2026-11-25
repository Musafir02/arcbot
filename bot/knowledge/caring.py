import re

from .lookup import entry

ANSWERS = ("money", "health", "family-and-parenting")

_ASKING = ("how", "what", "whats", "who", "which", "can i", "could i", "do i", "does", "is",
           "are", "should i", "much", "many", "claim", "claiming", "apply", "applying",
           "qualify", "qualifies", "eligible", "entitled", "worth", "explain", "mean",
           "means", "about", "tell", "long", "pay", "paid", "start", "receive", "receiving")

_NOT_THE_JOB = ("job", "jobs", "work at", "work in", "working at", "working in", "career",
                "volunteer", "volunteering", "salary", "interview", "nurse do", "nurses do",
                "training to be", "study to be")

_A_KEPT_ANIMAL = (r"(?:dogs?|puppies|puppy|pups?|cats?|kittens?|rabbits?|guinea pigs?|hamsters?|"
                  r"fish|goldfish|fish tank|tropical fish)")
_AN_ANIMAL_CARED_FOR = re.compile(
    r"\b(?:caring for|care for|caring of|looking after|look after|i care for|i look after)\s+"
    r"(?:my|our|the|a|an|his|her|their|two|three|both|elderly|old|sick|poor|new|little|baby|"
    r"big)?\s*(?:\w+\s+){0,1}?" + _A_KEPT_ANIMAL + r"\b")
_AN_ANIMAL_WEARS_ME_OUT = re.compile(
    r"\b(?:my|our|the)\s+(?:\w+\s+){0,1}?" + _A_KEPT_ANIMAL +
    r"\s+(?:is|are|has|have|keeps?|takes|took)\b")


def _an_animal_is_the_one_cared_for(reading):
    said = " ".join(str((reading or {}).get(key) or "") for key in ("clean", "text", "plain"))
    said = " " + re.sub(r"[^a-z0-9' ]+", " ", said.lower()) + " "
    if _AN_ANIMAL_CARED_FOR.search(said) or _AN_ANIMAL_WEARS_ME_OUT.search(said):
        return False
    return True


_THE_LOAD = ("cope", "coping", "cope with", "cant cope", "cannot cope", "not coping",
             "how do i cope", "how do i keep going", "keep going", "exhausted", "knackered",
             "worn out", "wearing me out", "wears me out", "burnt out", "burned out",
             "burnout", "burn out", "overwhelmed", "struggling", "struggling to cope",
             "no time for myself", "no life", "no life of my own", "on my own with it",
             "all on me", "it never stops", "never get a break", "no help", "help me",
             "tiring", "so tiring", "draining", "is a lot", "a lot of work", "hard work",
             "is hard", "hard going", "knackering", "shattered", "worn down", "getting to me",
             "help for carers", "support for carers", "look after myself",
             "run ragged", "dont know how much longer")

_THE_CARER = ("carer", "carers", "carer burnout", "carer stress", "unpaid carer",
              "full time carer", "i am a carer", "im a carer", "being a carer",
              "caring for my", "care for my", "caring for a", "care of my")


ENTRIES = [
    entry("respite-care", (("respite", "respite care", "respite break",
                           "short break from caring", "a break from caring"), _ASKING),
          "Respite care is a break for the person doing the caring, and it comes in small "
          "pieces: a few hours a week at a day centre, somebody sitting with them so you can go "
          "out, or a week in a care home so you can have a holiday. Arrange it before you are "
          "desperate, because the good places have a waiting list. The council can arrange it "
          "after a carer's assessment and means-tests the person you care for, not you; hospices "
          "and charities often have free day places and short stays; and the GP or district "
          "nurse knows what exists locally, which is usually more than the council website says.",
          ask=_ASKING, avoid=_NOT_THE_JOB,
          explain=True, bias=1),
    entry("hospice", (("hospice", "hospices", "hospice care"), _ASKING),
          "A hospice is for controlling pain and symptoms and for supporting the person doing "
          "the caring - it is not a place people are sent only to die. Most of what they do is "
          "day services, help at home and short stays, and people are usually referred months "
          "before the end, which is the whole point: it is easier to sort pain out early than in "
          "a crisis. The care is free (charity and NHS funded) and needs a referral from the GP, "
          "district nurse or hospital team, so ask for one; you can also ring the hospice and "
          "ask what they have, because they answer that question all day.",
          ask=_ASKING, avoid=_NOT_THE_JOB + ("how does the hospice work",),
          explain=True, bias=1),
    entry("palliative-care", (("palliative care", "palliative", "end of life care",
                              "palliative care team"), _ASKING),
          "Palliative care is treatment that controls symptoms and keeps somebody comfortable "
          "when a cure is not the aim - and it can run for years alongside treatment for the "
          "illness, so it does not mean care has been given up on. It is about pain, "
          "breathlessness, sickness, sleep and worry, it happens wherever the person is (at "
          "home, in a hospice, in hospital or in a care home), and the GP or specialist nurse "
          "can refer. Asking for it early is the thing that makes the last months better rather "
          "than the last weeks.",
          ask=_ASKING, avoid=_NOT_THE_JOB,
          explain=True, bias=1),
    entry("carer-burnout",
          (_THE_CARER, _THE_LOAD),
          "The first thing to ask for is a carer's assessment from your council: it is free, it "
          "is about you rather than the person you care for, and it can pay for someone to sit "
          "with them so you get a few hours back each week. Then tell your GP that you are "
          "caring - it goes on your notes, it counts for your own health, and it changes what "
          "they offer you. Ring Carers UK on 0808 808 7777 once, because they know the local "
          "schemes and the grants better than any website does, and ask your employer about "
          "flexible hours and unpaid carer's leave, which is now a day-one right. Book the break "
          "before you need it: a few hours a week arranged in advance is the difference between "
          "coping and going under, and taking it is not a failure.",
          ask=_THE_LOAD,
          guard=_an_animal_is_the_one_cared_for,
          avoid=_NOT_THE_JOB + (
                                "carer allowance", "carers allowance", "carer's allowance",
                                "allowance", "allowances", "benefit", "benefits", "pip",
                                "universal credit", "tax credit", "bus pass", "pass",
                                "travel", "blue badge", "badge", "motability", "money",
                                "paid", "pay", "claim", "claiming", "qualify",
                                "assessment", "how much", "how many hours"),
          bias=1, report=True),
]

_CARERS_PAY = ("carer's allowance", "carers allowance", "carer allowance", "carers allowance",
               "carer's credit", "carers credit", "carer credit",
               "paid for caring", "paid to care", "pay for caring", "money for caring",
               "paid for looking after", "paid to look after",
               "get paid for caring", "get paid to care", "get paid for looking after",
               "get paid to look after", "get paid as a carer", "paid as a carer",
               "get paid to be a carer", "paid for being a carer",
               "carer's allowance rate", "carers allowance amount")

_CARERS_ASSESSMENT = ("carer's assessment", "carers assessment", "carer assessment",
                      "assessment as a carer", "carer's needs assessment",
                      "carers needs assessment", "support as a carer", "help as a carer",
                      "help for carers", "support for carers", "carer support",
                      "what help can i get as a carer")

_NOT_THE_CARERS_MONEY = _NOT_THE_JOB + ("childminder", "childminders", "childminding",
                                        "babysit", "babysitting", "nanny", "fostering",
                                        "foster", "adoption", "nursery", "au pair",
                                        "care worker", "care assistant", "support worker",
                                        "care home job", "agency work")

def _the_care_is_for_a_grown_up(understood):
    line = str(understood.get("clean") or understood.get("text") or "").lower()
    if not re.search(r"\b(?:kid|kids|child|children|childminding|toddler|toddlers|"
                     r"babies|baby)\b", line):
        return True
    return bool(re.search(r"\bcarers?'?\s*(?:allowance|credit)\b|\bcaring\b|\bcarer\b", line))


ENTRIES += [
    entry("carers-allowance", (_CARERS_PAY, _ASKING),
          "Carer's Allowance is about £83 a week for caring 35 hours or more for someone who "
          "gets PIP daily living, Attendance Allowance or DLA middle or higher care. You must be "
          "16 or over, not in full-time education, and earning under about £200 a week after "
          "tax. Claim on gov.uk and date it from the day you started, because it backdates three "
          "months; earn too much and Carer's Credit keeps your NI record going instead.",
          ask=_ASKING, avoid=_NOT_THE_CARERS_MONEY, guard=_the_care_is_for_a_grown_up,
          explain=True, bias=1),
    entry("carers-assessment", (_CARERS_ASSESSMENT, _ASKING),
          "Ask the council's adult social care team for a carer's assessment. It is free, it is "
          "about your needs and not theirs, and you can ask without telling them. It takes about "
          "an hour, at home or on the phone, and it can bring respite hours, a direct payment "
          "you spend yourself, training and a number to ring in the worst moments. Say \"I would "
          "like a carer's assessment\" and get what they agree in writing.",
          ask=_ASKING, avoid=_NOT_THE_CARERS_MONEY + ("bus pass", "freedom pass", "travel pass",
                                                      "blue badge", "companion", "motability",
                                                      "disabled person"),
          explain=True, bias=1),
]

_LOOKED_AFTER_ME = ("cares for me", "care for me", "caring for me", "cared for me",
                    "cared for by", "looks after me", "look after me", "looking after me",
                    "looked after me", "looked after by")
_MY_FAMILY_CARER = ("son", "sons", "daughter", "daughters", "husband", "wife", "partner",
                    "mum", "mother", "dad", "father", "sister", "brother", "grandson",
                    "granddaughter", "grandchild", "niece", "nephew", "children", "kids",
                    "family", "friend", "friends", "neighbour", "neighbours", "aunt", "uncle",
                    "cousin", "relatives", "carer", "carers")
_NOT_THIS_ROW = _NOT_THE_JOB + ("allowance", "allowances", "credit", "benefit", "benefits",
                                "claim", "claiming", "qualify", "qualifies", "entitled",
                                "pip", "attendance", "cope", "coping", "cant cope",
                                "cannot cope", "exhausted", "burnt out", "burned out",
                                "struggling", "overwhelmed", "tiring", "worn out", "no life",
                                "respite", "assessment", "a break", "how do i get help")

ENTRIES += [
    entry("my-family-cares-for-me", (_LOOKED_AFTER_ME, _MY_FAMILY_CARER),
          "Two things are worth starting this week, because neither is sent automatically. "
          "Whoever looks after you for 35 hours a week or more can claim Carer's Allowance, "
          "about \u00a383 a week, and it keeps their National Insurance record going too. There is "
          "money for you as well: Attendance Allowance if you are over pension age, PIP if you "
          "are younger, neither of them means-tested, and both unlock more on other benefits. "
          "Then ask the council for a carer's assessment - it is free, it is about their needs, "
          "and it can pay for someone to sit with you so they get an evening back.",
          avoid=_NOT_THIS_ROW, bias=1),
]
