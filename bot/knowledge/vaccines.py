import re

from .health import PETS, _the_line
from .lookup import entry

ANSWERS = ("health",)

VACCINE_BOOSTER_ANSWER = (
    "The covid and flu boosters are offered each autumn to anyone 65 or over, pregnant, in a care "
    "home, or living with a condition like asthma, diabetes or a weak immune system, plus carers "
    "and health staff; the invitation comes to you, and failing that a pharmacy or the NHS app "
    "will book it. They are yearly because protection fades, and outside those groups a pharmacy "
    "gives the flu jab for about £15 to £20.")

TETANUS_JAB_ANSWER = (
    "You need a tetanus booster if it is more than 5 years since your last one and the wound was "
    "dirty - soil, a bite, a deep puncture or a burn - while a clean small cut within 10 years is "
    "usually fine. A pharmacist, a minor injuries unit or A&E can give it the same day, so ask "
    "today rather than waiting. Get a deep or heavily bleeding wound looked at straight away, not "
    "just for the jab.")


MEASLES_JAB_ANSWER = (
    "Measles is covered by the MMR, which is two doses: the first at about 1 year old and the "
    "second at 3 years and 4 months, and two doses is what counts as protected. An adult born "
    "after 1970 who never had two doses, or cannot remember, can have the MMR free at a GP "
    "surgery - and anyone born before 1970 is usually immune from having had measles itself. "
    "One dose gives about 90 per cent protection and two gives about 99.")

SHINGLES_JAB_ANSWER = (
    "The shingles vaccine is offered on the NHS when you turn 65 and again at 70, and it is two "
    "doses given two months apart. If you have already had shingles you can still have it, "
    "because it lowers the chance of it coming back, and younger adults with a weakened immune "
    "system are offered it too - ask the GP if you are not sure whether you have had it.")

PNEUMONIA_JAB_ANSWER = (
    "The pneumonia jab (pneumococcal) is a one-off rather than a yearly one, offered at 65 and to "
    "anyone with asthma, diabetes, heart, kidney or liver disease, or no spleen. If you have had "
    "it you do not need it again, and the GP record will say - the yearly autumn jab you are "
    "thinking of is the flu one, which is a different vaccine.")

JAB_SAFETY_ANSWER = (
    "A sore arm, tiredness and a mild fever for a day or two are the ordinary after-effects, and "
    "serious reactions are rare - a severe allergic reaction is about one in a million doses, "
    "which is why you wait 15 minutes afterwards. The flu jab cannot give you flu because it is "
    "not a live virus, while the MMR and the children's nasal flu spray are live but weakened and "
    "are not given in pregnancy or to someone whose immune system is badly weakened. Mention any "
    "reaction you have had before when you book, and the pharmacist or GP will say whether it is "
    "a reason to skip one.")

PREGNANCY_JAB_ANSWER = (
    "The flu and covid jabs are offered in pregnancy at any stage, because both illnesses are "
    "harder on you and the baby then, and the whooping cough jab is offered from about 16 weeks "
    "and again in each pregnancy. Say you are pregnant when you book, at the GP, the pharmacy or "
    "the maternity team, and they will give you the one for your stage.")


_AN_APPOINTMENT_DAY = re.compile(
    r"\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday|tomorrow|tonight|next week|"
    r"next month|this week|this afternoon|this morning|booked|booking|appointment|appointments|"
    r"rescheduled|rebooked|cancelled|canceled|yesterday|already had|already been|just had)\b")


def _it_is_not_an_appointment_already(understood):
    if str((understood or {}).get("kind") or "") == "question":
        return True
    return not _AN_APPOINTMENT_DAY.search(_the_line(understood))


def _the_vaccine_row_is_the_answer(understood):
    return (_it_is_not_an_appointment_already(understood)
            and _not_the_flu_on_its_own(understood)
            and _the_booster_is_the_jab(understood))


_A_JAB_WORD = re.compile(
    r"\b(covid|flu|jab|jabs|jabbed|jabbing|vaccine|vaccines|vaccinate|vaccinated|vaccination|"
    r"vaccinations|immunisation|immunization|immunised|immunized|inoculation|tetanus|lockjaw|"
    r"booster shot|booster jab|pregnan\w*|expecting|whooping cough|shingles|pneumonia)\b")


def _the_booster_is_the_jab(understood):
    if _A_JAB_WORD.search(_the_line(understood)):
        return True
    lean = (understood or {}).get("leans_on") or {}
    if not str(lean.get("text") or "").strip():
        return True
    said = " ".join([str(lean.get("text") or ""), str(lean.get("subject") or ""),
                     " ".join(str(word) for word in lean.get("words") or ())]).lower()
    return bool(_A_JAB_WORD.search(said))


def _not_the_flu_on_its_own(understood):
    line = _the_line(understood)
    if "flu" in line and not any(word in line for word in ("pregnan", "expecting", "booster",
                                                          "jabbed", "booster jab")):
        return False
    return True


_JAB_BY_DISEASE = (
    (("measles", "mumps", "rubella", "mmr"), MEASLES_JAB_ANSWER),
    (("shingles",), SHINGLES_JAB_ANSWER),
    (("pneumonia", "pneumococcal"), PNEUMONIA_JAB_ANSWER),
)

_ASKING_IF_IT_IS_SAFE = re.compile(
    r"\b(?:\w+\s+){0,4}safe\b|\bany (?:risk|risks|danger)\b|\bside effects?\b|"
    r"\bdangerous\b|\bharmful\b|\bbad for (?:me|you)\b")


def _vaccine_booster_answer(memory, understood):
    line = _the_line(understood)
    if any(word in line for word in ("pregnan", "expecting", "due in", "weeks gone")):
        return PREGNANCY_JAB_ANSWER
    if _ASKING_IF_IT_IS_SAFE.search(line):
        return JAB_SAFETY_ANSWER
    for words, answer in _JAB_BY_DISEASE:
        if any(word in line for word in words):
            return answer
    if "tetanus" in line or "lockjaw" in line:
        return TETANUS_JAB_ANSWER
    return VACCINE_BOOSTER_ANSWER


ENTRIES = []

ENTRIES.append(entry(
    "vaccine-booster",
    (("booster", "booster jab", "booster shot", "booster dose", "booster vaccine", "top up jab",
      "covid booster", "covid jab", "covid vaccine", "covid vaccination", "covid shot",
      "jab", "jabs", "jabbed", "vaccine", "vaccines", "vaccination", "vaccinations",
      "immunisation", "immunization", "tetanus", "tetanus jab", "tetanus shot",
      "flu booster",
      "measles", "mumps", "rubella", "mmr", "shingles", "shingles jab", "pneumonia",
      "pneumococcal"),
     ("need", "needed", "should", "when", "due", "overdue", "get", "got", "have", "had",
      "worth", "how often", "again", "another", "next", "am i", "do i", "can i", "is it",
      "time", "book", "where", "free", "pay", "top up", "safe", "ok", "fine")),
    _vaccine_booster_answer,
    avoid=("seat", "car seat", "booster seat", "child seat", "isofix", "cushion", "trolley",
           "backless", "high backed", "high-backed", "rear facing", "rear-facing", "135",
           "height", "booster cushion",
           "pushchair", "high chair", "car", "cars", "van", "driving", "travel", "flight",
           "plane", "holiday",
           "wifi", "wi fi", "wireless", "router", "internet", "broadband", "signal", "reception",
           "mobile signal", "tv", "telly", "aerial", "speaker", "amp", "hifi", "punch", "punching",
           "boxing", "sparring",
           "after the", "after my", "paracetamol", "ibuprofen", "alcohol", "drink",
           "yellow fever", "typhoid", "hepatitis", "rabies", "dengue", "malaria",
           "travel vaccine", "travel jab", "travel clinic",
           "sore", "ache", "hurts", "hurting", "swollen", "side effect", "side effects",
           "arm", "shoulder",
           "baby", "babies", "toddler", "newborn", "child", "children", "kid", "kids",
           "my son", "my daughter", "my boy", "my girl", "school", "nursery", "puppy", "kitten",
           "hamster", "rabbit", "parrot") + PETS,
    guard=_the_vaccine_row_is_the_answer))
