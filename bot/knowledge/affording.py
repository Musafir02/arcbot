import re

from .lookup import entry

ANSWERS = ("friends-and-relationships", "money", "family-and-parenting")

_NO_MONEY = (
    "cant afford", "can't afford", "cannot afford", "couldnt afford", "couldn't afford",
    "cant go", "can't go", "cant come", "can't come", "too expensive for me",
    "too expensive for us", "thats too expensive", "that's too expensive",
    "expensive things", "expensive stuff", "priced out", "money is tight", "moneys tight",
    "money's tight", "no money for", "cant stretch to", "can't stretch to",
)

_THE_OCCASION = (
    "holiday", "holidays", "trip", "trips", "weekend away", "long weekend", "city break",
    "stag", "stag do", "stags", "hen", "hen do", "hens",
    "birthday dinner", "birthday meal", "birthday drinks", "birthday do", "birthday party",
    "dinner", "meal", "night out", "party", "parties", "bridesmaid", "best man", "godparent",
    "to come", "to go", "come along", "be there", "my share", "my half", "the share",
    "my ticket", "the ticket", "inviting me", "invited me", "invites me", "invitation",
)

_A_PERSON_OR_AN_INVITATION = re.compile(
    r"\b(?:friend|friends|mate|mates|pal|pals|mum|mam|mom|mother|dad|father|sister|brother|"
    r"sibling|cousin|colleague|workmate|family|she|he|they|her|him|them|"
    r"invit(?:e|es|ed|ing|ation|ations)|asking me|asked me|keep asking|"
    r"to come|to go|come along|be there|my share|my half)\b", re.IGNORECASE)

_PLANNING = re.compile(
    r"\b(?:planning|guest list|how much should|how much do i|budget(?:ing)? for|"
    r"cheapest|cheap|save for|saving for|my own wedding|our wedding|we are getting married|"
    r"afford a holiday|afford a trip|afford a wedding)\b", re.IGNORECASE)


def _an_invitation_is_what_they_cannot_afford(understood):
    reading = understood or {}
    words = " ".join(str(one) for one in (reading.get("words") or ()))
    text = str(reading.get("clean") or reading.get("text") or "") or words
    if not _A_PERSON_OR_AN_INVITATION.search(text):
        return False
    return not _PLANNING.search(text)


ENTRIES = [
    entry("an-invitation-you-cannot-afford",
          (_NO_MONEY, _THE_OCCASION),
          "Say it early, to the person who asked you, and keep it about the money rather than "
          "about them: 'I'd love to be there, and I can't do the whole thing this year.' Offer "
          "the part you can do - the meal, the one night, a smaller gift - and name a number if "
          "you have one. Don't invent a reason and don't leave it to the week before: one "
          "honest no, said kindly, is much easier to hear than a yes you cannot afford.",
          bias=2,
          guard=_an_invitation_is_what_they_cannot_afford,
          avoid=("wedding", "weddings", "bride", "groom", "bridesmaid", "best man",
                 "godparent",
                 "present", "presents", "gift", "gifts", "secret santa", "christmas", "xmas",
                 "rent", "mortgage", "bill", "bills", "energy", "electric", "gas", "council tax",
                 "insurance", "car", "van", "petrol", "fuel", "childcare", "nursery",
                 "school trip", "uniform", "food", "shopping", "dental", "dentist", "glasses")),
]
