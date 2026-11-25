import re

from ..compose import loss, negated, pick, trouble
from ..compose.badnews import reads_as_bad_news, reads_for_a_pet, reads_like_a_symptom
from ..compose.goodnews import reads_as_good_news, reads_as_settled, worry_on_the_table
from ..understanding import understand as understanding
from ..understanding.kinds import SHIFT_EARLY, SHIFT_LATE, VERBISH
from ..understanding.topics import NUMBER_WORDS
from ..understanding.normalize import (LEFT_OFF_CONTRACTION, LEADERS,
                                       opens_without_subject,
                                       without_a_leading_exclamation)
from . import last_user, there_is_a_chat
from . import opening
from . import you as say_it_back
from . import facts, hours as hours_after, named, narrow, not_a_trip, taste, topics
from . import stuck as stuck_line
from .facts import DAYS, MONTHS, a_limit_on_the_plan
from .relations import _person_from_pronoun, _pronoun_fits
from .store_lines import CHILD, PERSON_GROUP

FACTS = ("name", "age", "job", "city", "places", "allergies", "pets", "people", "budget", "diet",
         "plan", "done", "others", "relations", "condition", "tastes", "birthday", "weight",
         "height")

EXPLAIN_TAIL = (
    "{Thing}. That explains it \u2014 no wonder it sits on you. What would take some weight off?",
    "{Thing}. That is a lot to carry on top of how you feel. What would help most?",
    "{Thing} \u2014 so that is the part behind it. What has been hardest about it?",
)
HAVE_THING = re.compile(
    r"\b(?:i|we)(?:['\u2019]?ve)?\s+(?:have(?:\s+got)?|got|own|keep|just got|"
    r"recently got|already got|just bought|bought)\b"
    r"(?:\s+(?:already|just|only|still|now|also))?\s+"
    r"(?:(?:a|an|one|two|three|four|five|six|seven|eight|nine|ten|another|some|no|few"
    r"|couple|my|our|his|her|their)\s+)?([a-z][a-z'-]{2,20})\b", re.I)
NOT_A_THING = frozenset("""
    feeling idea question clue hurt look go try rest break problem issue theory plan reason hope
    dream nightmare laugh cry shower think thought memory chance sense guess moment minute while
    day week month year option choice say part lot bit time life job appointment check
    read call text email message right headache pain ache cough cold temperature fever migraine
    bug flu to no not nothing none much more less enough already got
""".split())

AN_AIM = re.compile(
    r"^\s*(?:(?:ok|okay|so|well|right|and|but|yeah|hi|hey)[,\s]+)*"
    r"(?:(?:i'?m|i am|im|i|we'?re|we are|we)\s+(?:really |still |just |also |now )?"
    r"(?:trying|hoping|aiming|planning|working|wanting|looking)\b[^.!?]{0,40}?\b(?:to|on|at)\b"
    r"|\bi want to (?!talk|say|tell|ask|know|feel|die|disappear|give up)\b"
    r"|\bi(?:'?m| am|m) on a (?:diet|plan|course|programme)\b)",
    re.I)
A_FEELING_ABOUT_IT = re.compile(
    r"\b(?:"
    r"feel\s+(?:like\s+)?(?:giving|awful|terrible|rubbish|horrible|dreadful|hopeless|useless|"
    r"a\s+failure|like\s+a\s+failure|low|down|bad|shit|stupid|fat|ugly|impossible|sick)"
    r"|dont\s+feel\s+like|don'?t\s+feel\s+like|not\s+feeling\s+it"
    r"|feelings?|felt\s+(?:like|awful|terrible|low|down)|it\s+feels\s+impossible"
    r"|giv(?:e|ing|en)\s+up|gave\s+up|going\s+to\s+quit"
    r"|struggl\w*"
    r"|can'?t\s+(?:do\s+it|keep|cope|face|take\s+it|manage)|cannot\s+(?:do|keep|cope)"
    r"|hopeless|worthless|useless|pointless|miserable|ashamed|guilty|hate\s+my\s+body"
    r"|fail\w*"
    r"|fed\s+up|sick\s+of|had\s+enough|tired\s+of\s+it"
    r"|exhausted|knackered|worn\s+out|burnt?\s+out"
    r"|embarrass\w*|depress\w*|anxious|anxiety|stressed|tearful|crying"
    r"|no\s+motivation|losing\s+(?:heart|motivation)|disheartened|demoralis\w*|demoraliz\w*"
    r"|not\s+going\s+well|going\s+badly"
    r"|worried|scared|afraid"
    r")\b",
    re.I)

SOMEONE_GOOD = re.compile(
    r"\b(?:prize|award|medal|trophy|cup|distinction|honours|top of the class|head boy|head girl"
    r"|scholarship|won|wins|winning|came first|passed|passing|graduated|graduates|degree"
    r"|a[\s*'-]?stars?\b(?![\s-]*(?:wars|trek|gazer|gazing|sign|bucks|fish|city|chart))"
    r"|a\*s?|straight 9s|all 9s|all 8s|grade 9|grade 8|top grades"
    r"|got into|got engaged|engaged|married|expecting|gave birth|had a baby|new baby"
    r"|promoted|promotion|new job|retired|retiring|all clear|out of hospital"
    r"|new puppy|new kitten|new dog|new cat|new rabbit|new hamster|new foal)\b", re.I)
SOMEONE_TAIL = (
    "{Thing} \u2014 that's lovely news.",
    "{Thing}. That's a good bit of news to hear.",
    "{Thing} \u2014 you must be pleased for them.",
    "{Thing}. That's worth a bit of a fuss.",
)
SOMEONE_COMING = re.compile(
    r"\b(?:my|our)\s+(?:mum|mom|mam|mother|dad|father|son|daughter|sister|brother|wife|husband"
    r"|partner|aunt|uncle|gran|granny|grandma|grandad|grandpa|nan|cousin|niece|nephew|mate|mates"
    r"|friends?|in[- ]?laws?|parents|family|folks|brother|sister-in-law|brother-in-law)\b"
    r"[^.;!?]{0,18}?\b(?:is|are|was|were)\s+(?:already\s+|just\s+|now\s+|still\s+|all\s+)?"
    r"(?:coming|visiting|staying|stopping|arriving|due\s+to\s+(?:arrive|come|visit|stay))\b"
    r"|\b(?:i'?m|im|i am|we'?re|we are)\s+(?:off\s+|going\s+)?(?:up|down|over|back)?\s*"
    r"(?:to\s+see|visiting|staying\s+with|stopping\s+with)\s+(?:my|our)\s+"
    r"(?:mum|mom|mam|mother|dad|father|son|daughter|sister|brother|wife|husband|partner|aunt"
    r"|uncle|gran|granny|grandma|grandad|grandpa|nan|cousin|niece|nephew|mate|friends?|parents"
    r"|family|folks)\b", re.I)
NOT_A_VISIT = re.compile(
    r"\b(?:pick(?:ing)?\s+(?:me|us)\s+up|drop(?:ping)?\s+(?:me|us)\s+off|collect(?:ing)?\s+"
    r"(?:me|us)|to\s+(?:have\s+a\s+look|check|fix|repair|help|clean|deliver|install|service)\b)",
    re.I)
VISIT_TAIL = (
    "{Thing} \u2014 that's something to look forward to.",
    "{Thing}. Nice \u2014 a proper visit.",
    "{Thing} \u2014 enjoy it.",
    "{Thing}. Good \u2014 that's a proper bit of the week.",
)

SOMEONE_MILESTONE = re.compile(
    r"\b(?:birthday|anniversary)\b[^.;!?]{0,24}?\b(?:next|this|on|is)\s+"
    r"(?:week|month|weekend|today|tomorrow|saturday|sunday|monday|tuesday|wednesday|thursday|friday)\b"
    r"|\bturns?\s+\d{1,3}\b"
    r"|\b(?:forty|fifty|sixty|seventy|eighty|ninety)\b"
    r"|\b\d{2,3}(?:th|st|nd|rd)?\b[^.;!?]{0,24}?\b(?:next|this|on|in)\s+(?:week|month|weekend|"
    r"saturday|sunday|monday|tuesday|wednesday|thursday|friday)\b"
    r"|\b(?:next|this)\s+(?:week|month|weekend)\b[^.;!?]{0,20}?\b\d{2,3}\b",
    re.I)
SOMEONE_MILESTONE_TAIL = (
    "{Thing} \u2014 that's a big one.",
    "{Thing}. Are you doing anything for it?",
    "{Thing} \u2014 a round one deserves a fuss.",
    "{Thing}. That's coming round fast.",
)

A_SECOND_PERSON = re.compile(
    r"^\s*(?:and|also|plus|or|what\s+about|how\s+about)\b[\s,]*"
    r"(?:my|our|your)\s+(?P<who>[a-z][a-z '-]{1,24}?)\s*(?:'s|s)?\s*[.!?]*\s*$", re.I)
A_BIRTHDAY_TOLD = re.compile(r"\b(?:birthday|bday|dob|date of birth)\b", re.I)
A_PLAN_VERB = re.compile(r"\b(?:is|are|was|were)\s+(?P<verb>[a-z]+ing)\b", re.I)
A_DATE_TOLD = re.compile(
    r"\b(?:" + "|".join(MONTHS) + r"|" + "|".join(DAYS) + r"|"
    r"\d{1,2}(?:st|nd|rd|th)\b|next\s+(?:week|month|weekend)|this\s+(?:week|month|weekend))",
    re.I)


def _a_relation(word):
    said = " ".join(str(word or "").lower().split()).strip(" .,;:!?'")
    for candidate in (said, said[:-1] if said.endswith("s") else "", said.replace(" ", "")):
        if candidate in facts.RELATIONS:
            return candidate
    return ""


def _the_pronoun(relation):
    if relation in facts.HE:
        return "he"
    if relation in facts.SHE:
        return "she"
    return ""


def _the_ages_held(memory):
    from . import others as the_others
    held = {}
    for entry in (the_others(memory) or []):
        if isinstance(entry, dict) and entry.get("age") is not None:
            held[str(entry.get("who") or "").lower()] = entry.get("age")
    return held


def _people_in_chat(memory):
    if not isinstance(memory, dict):
        return False
    user = memory.get("user") or {}
    if isinstance(user, dict) and (user.get("people") or user.get("kids")):
        return True
    from . import others as the_others
    if the_others(memory):
        return True
    for turn in (memory.get("turns") or [])[-4:]:
        said = str((turn or {}).get("user") or "").lower() if isinstance(turn, dict) else ""
        if any(re.search(r"\bmy\s+" + re.escape(one) + r"\b", said) for one in facts.RELATIONS):
            return True
    return False


def a_person_named_alone(text, memory):
    if not isinstance(text, str):
        return ""
    only = named.the_one_asked_about(text) or " ".join(text.split())
    match = A_PERSON_ALONE.match(" ".join(only.split()))
    if not match:
        return ""
    said = " ".join(match.group("what").lower().split()).strip(" .,;:!?'")
    said = WHICH_ONE.sub("", said)
    ours = match.group("det").lower() in ("my", "our")
    word = said[:-1] if said.endswith("s") and said[:-1] in facts.RELATIONS else said
    several = said.endswith("s") and said[:-1] in facts.RELATIONS
    place = A_POSITION.get(" ".join(match.group("what").lower().split()))
    if place:
        if place in A_POSITION_MAYBE_A_THING and not _people_in_chat(memory):
            return ""
        pool = A_POSITION_LINES.get(place) or A_PERSON_ALONE_LINES
        who = ("Your " if ours else "The ") + place
        return (pick(pool, memory, said).replace("{Who}", who)
                    .replace("{they}", "they").replace("{them}", "them").replace("{do}", "do"))
    group = A_GROUP_ALONE.get(said) or (said[:-1] + "s" if several else "")
    if group:
        who = ("Your " if ours else "The ") + group
        return pick(A_GROUP_ALONE_LINES, memory, said).format(Who=who)
    relation = _a_relation(word)
    if not relation:
        return ""
    return _the_question_about(relation, said, ours, memory)


def _the_question_about(relation, said, ours, memory, name=""):
    pronoun = _the_pronoun(relation)
    they, them = (pronoun, "him" if pronoun == "he" else "her") if pronoun else ("they", "them")
    who = name or (("Your " if ours else "The ") + relation)
    known = relation in _the_ages_held(memory)
    pool = A_KNOWN_AGE_LINES if known else A_PERSON_ALONE_LINES
    line = pick(pool, memory, said)
    return (line.replace("{Who}", who).replace("{they}", they).replace("{them}", them)
                .replace("{do}", "does" if they in ("he", "she") else "do"))


A_POINTED_AT = re.compile(r"^(?:him|her|them|they|that one|this one|those two|the two of them|"
                          r"both of them|the pair of them)$")


def a_person_pointed_at(text, memory):
    if not isinstance(text, str):
        return ""
    only = named.the_one_asked_about(text)
    if not only or not A_POINTED_AT.match(" ".join(only.lower().split())):
        return ""
    word = only.lower().strip()
    if word not in ("him", "her", "them", "they", "that one", "this one") \
            and _how_many_people(memory) < 2:
        return ""
    if word not in ("him", "her", "them", "they", "that one", "this one"):
        all_named = _the_people_pointed_at(memory)
        if len(all_named) >= 2:
            who = " and ".join(all_named[:2])
            pool = A_TWO_ALONE_LINES if all(_an_age_held(memory, one) for one in all_named[:2]) \
                else A_GROUP_ALONE_LINES
            return pick(pool, memory, who).format(Who=who)
    person = _the_person_pointed_at(word, memory)
    if not person:
        return ""
    relation, name = person
    return _the_question_about(relation, relation, True, memory, name)


def _how_many_people(memory):
    from . import others as the_others
    return sum(1 for entry in (the_others(memory) or [])
               if isinstance(entry, dict) and str(entry.get("who") or "").lower() in facts.RELATIONS)


def _the_people_pointed_at(memory):
    from . import others as the_others
    names = []
    for entry in the_others(memory) or []:
        if not isinstance(entry, dict):
            continue
        if str(entry.get("who") or "").lower() not in facts.RELATIONS:
            continue
        name = str(entry.get("name") or "").strip()
        if not name or not name[:1].isalpha():
            continue
        name = name[0].upper() + name[1:]
        if name not in names:
            names.append(name)
    return names


def _an_age_held(memory, name):
    from . import others as the_others
    for entry in the_others(memory) or []:
        if not isinstance(entry, dict):
            continue
        held = str(entry.get("name") or "").strip().lower()
        if held == name.strip().lower() and entry.get("age"):
            return True
    return False


def _the_person_pointed_at(word, memory):
    from . import others as the_others
    wanted = {"him": facts.HE, "her": facts.SHE}.get(word)
    people = [entry for entry in (the_others(memory) or []) if isinstance(entry, dict)]
    for entry in reversed(people):
        relation = str(entry.get("who") or "").strip().lower()
        if relation not in facts.RELATIONS:
            continue
        if wanted is not None and relation not in wanted:
            continue
        name = str(entry.get("name") or "").strip()
        if name and name[:1].isalpha():
            name = name[0].upper() + name[1:]
        return relation, name
    return None


def a_second_person(text, memory):
    if not isinstance(text, str):
        return ""
    match = A_SECOND_PERSON.match(" ".join(text.split()))
    if not match:
        return ""
    who = _a_relation(match.group("who"))
    if not who:
        return ""
    before = " ".join(str(last_user(memory) or "").lower().split())
    if not before:
        return ""
    first = next((one for one in facts.RELATIONS if re.search(r"\bmy\s+" + re.escape(one) + r"", before)), "")
    if not first or first == who:
        return ""
    if not (A_BIRTHDAY_TOLD.search(before) or A_DATE_TOLD.search(before)):
        return ""
    said = "your " + who
    if A_BIRTHDAY_TOLD.search(before):
        return "And " + said + "'s birthday \u2014 when is that?"
    verb = A_PLAN_VERB.search(before)
    pronoun = _the_pronoun(who)
    if verb and pronoun:
        return "And " + said + " \u2014 when's " + pronoun + " " + verb.group("verb").lower() + "?"
    return "And " + said + " \u2014 when is that?"


A_PERSON_ALONE = re.compile(
    r"^\s*(?:(?:and|also|plus|or|what\s+about|how\s+about|same\s+for|and\s+same\s+for|"
    r"same\s+as|and\s+so\s+does|and\s+so\s+is)\b[\s,]*)?"
    r"(?P<det>my|our|the|a|an)\s+(?P<what>[a-z][a-z '-]{1,24}?)\s*[.!]*\s*$", re.I)
WHICH_ONE = re.compile(r"^(?:other|second|third|first|eldest|oldest|youngest|little|big|"
                       r"older|younger|new|baby|step|half|adopted|foster)\s+")
A_GROUP_ALONE = {"kids": "children", "children": "children", "childs": "children",
                 "twins": "twins", "boys": "boys", "girls": "girls", "sons": "sons",
                 "daughters": "daughters", "parents": "parents", "brothers": "brothers",
                 "sisters": "sisters", "grandkids": "grandchildren",
                 "grandchildren": "grandchildren", "grandparents": "grandparents"}
A_POSITION = {
    "youngest": "youngest", "youngest one": "youngest", "eldest": "eldest",
    "eldest one": "eldest", "oldest": "oldest", "oldest one": "oldest",
    "middle one": "middle one", "middle": "middle one", "second one": "second one",
    "third one": "third one", "little one": "little one", "littlest": "little one",
    "small one": "little one", "other one": "other one", "baby": "baby",
    "new baby": "baby", "little baby": "baby", "other half": "other half", "half": "other half",
    "partner": "other half",
}
A_POSITION_MAYBE_A_THING = frozenset(("other one", "second one", "third one", "middle one"))
A_POSITION_LINES = {
    "baby": ("{Who} \u2014 how many months?",
             "{Who} \u2014 boy or girl, and how old?",
             "{Who} \u2014 tell me about {them}."),
    "other half": ("{Who} \u2014 how long have you two been together?",
                   "{Who}. What {do} {they} do?",
                   "{Who} \u2014 tell me about {them}."),
}
A_PERSON_ALONE_LINES = (
    "{Who} \u2014 how old is {they}?",
    "{Who}. What {do} {they} get up to?",
    "{Who} \u2014 tell me a bit about {them}.",
)
A_KNOWN_AGE_LINES = (
    "{Who} \u2014 what is {they} into at the moment?",
    "{Who}. How is {they} getting on?",
)
A_TWO_ALONE_LINES = (
    "{Who} \u2014 what are they into at the moment?",
    "{Who}. How are they getting on?",
)
A_GROUP_ALONE_LINES = (
    "{Who} \u2014 how old are they?",
    "{Who}. How are they getting on?",
    "{Who} \u2014 tell me about them.",
)

FRAMES = (
    "{Thing} \u2014 noted.",
    "Got it \u2014 {thing}.",
    "{Thing}, good to know.",
    "Noted: {thing}.",
    "{Thing} \u2014 I'll remember that.",
    "{Thing}, right \u2014 I've got that.",
)

STILL_TO_DO = re.compile(
    r"\b(?:still\s+(?:have|got)|have\s+got|i\s+ve\s+still\s+got)\s+"
    r"((?:the|my|our|a|an|his|her|their|this|that)\s+[a-z' ]{2,28}?)\s+to\s+"
    r"(?:sort|do|deal|get|finish|pay|arrange|handle|see|take|cover|make|run|write|clean|buy|"
    r"order|collect|ring|book|fix|wash|iron|pack|post|send|sign|check|tidy|move|email|print|"
    r"return|visit|walk|feed|look)\b",
    re.I)
NOT_ONE_THING = re.compile(r"\b(?:and|but|so|because|that|if|when|which)\b", re.I)
THE_LIMIT_GOES_FIRST = (
    "Then {thing} first, and the rest can wait.",
    "Then do {thing} first and let the rest wait.",
    "Then take {thing} first \u2014 the rest can wait until it is done.",
    "Fair enough: {thing} first, and the rest of the list waits.",
)


_A_PLAN_WAS_GIVEN = re.compile(
    r"\b(?:one thing|only that|pick|first|start with|begin with|next step|smallest)\b", re.I)


def _the_last_reply_gave_a_plan(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    said = ""
    for turn in reversed(turns or []):
        if isinstance(turn, dict) and str(turn.get("bot") or "").strip():
            said = " ".join(str(turn["bot"]).lower().split())
            break
    if not said:
        return False
    if re.search(r"\d", said) or ":" in said:
        return True
    if _A_PLAN_WAS_GIVEN.search(said):
        return True
    return stuck_line._the_answer_gave_a_step(memory)


def _a_limit_on_the_plan(read, memory):
    if not _the_last_reply_gave_a_plan(memory):
        return None
    found = STILL_TO_DO.search(read)
    if not found:
        return None
    thing = " ".join(found.group(1).split()).strip(" .,!?:;")
    words = thing.split()
    if not 1 <= len(words) <= 4 or NOT_ONE_THING.search(thing):
        return None
    pool = tuple(line.format(thing=thing) for line in THE_LIMIT_GOES_FIRST)
    return pick(pool, memory, read)


DAY_SOON = re.compile(
    r"\b(?:tonight|tomorrow|this (?:afternoon|evening)|"
    r"(?:on |next |this )?(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)|"
    r"(?:next |this |at the |the )weekend|next week|"
    r"(?:on|by|before|until|till) the \d{1,2}(?:st|nd|rd|th)\b"
    r"|\b\d{1,2}(?:st|nd|rd|th) of (?:january|february|march|april|may|june|july|august"
    r"|september|october|november|december)"
    r"|\b(?:is|due|falls?|lands?) (?:on )?the \d{1,2}(?:st|nd|rd|th)\b)", re.I)
DAY_BEEN_AND_GONE = re.compile(
    r"\b(?:saw|met|went|was|were|had|took|tried|left|rang|called|kicked|started|finished|ended"
    r"|moved|got married|felt|ate|slept|woke|bought|sold|made|said|told|came|did|hurt|cried"
    r"|stopped|began|broke|forgot|lost|won|worked|texted|visited|arrived|landed|been"
    r"|this morning|yesterday|last (?:night|week|month|year|weekend|sunday|monday|tuesday"
    r"|wednesday|thursday|friday|saturday)|since (?:six|seven|three|four|five|eight|nine|ten"
    r"|eleven|twelve|two|one|half)|was in|used to|every (?:day|morning|night|week|weekend"
    r"|month|tuesday|monday|sunday|friday|saturday)|usually|always|normally|like the \d+)\b",
    re.I)
A_DOING = re.compile(
    r"\b(?:is|are|am|was|were|be|been|being|have|has|had|got|gets|get|go|goes|going|gone|come"
    r"|comes|coming|came|see|sees|seeing|visit|visits|visiting|fly|flies|flying|meet|meets"
    r"|meeting|start|starts|starting|work|works|working|need|needs|want|wants|wanted|due|take"
    r"|takes|taking|leave|leaves|leaving|arrive|arrives|arriving|stay|stays|staying|play|plays"
    r"|shut|shuts|open|opens|starts|turning|turns|have to|has to|going in|going back|back|off"
    r"|away|free|busy"
    r"|dentist|vets?|doctor|gp|hospital|scan|appointment|haircut|interview|meeting|flight"
    r"|train|bus|viewing|pickup|shift|party|match|wedding|birthday|exam|test|lesson"
    r"|class|club|football|rugby|school|concert|payday|pay day|rent|bill|deadline|review"
    r"|christening|funeral|service|checkup|check-up|surgery|midwife|health visitor)\b", re.I)
A_FIGURE = re.compile(r"\b\d{3,}\b")
A_DOING_TURNED_DOWN = re.compile(
    r"\b(?:dont|don'?t|do not|doesnt|doesn'?t|didnt|didn'?t|wont|won'?t|wouldnt|wouldn'?t|"
    r"cant|can'?t|cannot|not|never|no longer|no way)\s+(?:\w+\s+){0,2}?"
    r"(?:want|wants|wanted|need|needs|fancy|go|goes|going|have|has|having|do|doing|"
    r"come|comes|coming|came|stay|staying|work|working|eat|eating|drink|drinking|see|seeing|"
    r"happen|happening)\b")


DAY_JUST_A_STATE = re.compile(
    r"\b(?:worse|better|pale|ill|sick|poorly|off (?:it|his|her|their) food|not himself"
    r"|not herself|up till|up until|much going on|busy|quiet|lovely|nice|awful|horrible)\b",
    re.I)
DAY_FAR = re.compile(
    r"\b(?:in|of|next|this|by)\s+(?:january|february|march|april|may|june|july|august|september"
    r"|october|november|december)\b|\bin (?:the )?(?:spring|summer|autumn|winter)\b"
    r"|\bnext (?:month|year)\b|\blater (?:this|in the) (?:year|month)\b", re.I)
A_DAY_ASKED = re.compile(r"\?|^(?:what|when|how|why|where|who|can|could|should|do|does|did|is|"
                         r"are|will|would|shall)\b", re.I)
NOT_A_DAY_TO_LOOK_FORWARD_TO = re.compile(
    r"\b(?:inquest|post[- ]mortem|autopsy|coroner|funeral|cremation|burial|bury|"
    r"reading of the will|probate|hearing|tribunal|court|custody|bailiffs?|eviction|"
    r"wake\b(?!\s*(?:up|at|early))|"
    r"creditors?|bankrupt(?:cy)?|insolven(?:cy|t)|debt (?:meeting|hearing)|"
    r"repossession|disciplinary|operation|surgery|biopsy|hospice|chemotherapy|radiotherapy|"
    r"diagnosis|results|care assessment)\b", re.I)
SOON_TAIL = (
    "{Thing}. Not long now, then.",
    "{Thing} \u2014 that is soon, then.",
    "{Thing}. Not far off now.",
    "{Thing} \u2014 coming round quickly, then.",
)
FAR_TAIL = (
    "{Thing} \u2014 plenty of time to sort the rest.",
    "{Thing}. That is one to look forward to.",
    "{Thing} \u2014 nice to have something in the diary.",
    "{Thing}. Plenty of time, anyway.",
)
SORRY_TAIL = (
    "{Thing}. That is a lot to have coming.",
    "{Thing} \u2014 I hope it goes as well as it can.",
    "{Thing}. That is a hard one to have ahead of you.",
    "{Thing} \u2014 no wonder it is on your mind.",
)


def _a_day_coming(clean):
    said = clean or ""
    if A_DAY_ASKED.search(said) or DAY_BEEN_AND_GONE.search(said):
        return None
    if DAY_JUST_A_STATE.search(said) or A_FIGURE.search(said):
        return None
    if A_DOING_TURNED_DOWN.search(said):
        return None
    if not A_DOING.search(said):
        return None
    if NOT_A_DAY_TO_LOOK_FORWARD_TO.search(said):
        return SORRY_TAIL
    if DAY_FAR.search(said):
        return FAR_TAIL
    if DAY_SOON.search(said):
        return SOON_TAIL
    return None


    coming = _a_day_coming(clean)
    if coming:
        return coming

_SAID_BACK = tuple(
    (frame.split("{", 1)[0].strip().lower(), frame.rsplit("}", 1)[-1].strip().lower())
    for frame in FRAMES
)


_SENTENCE = re.compile(r"(?<=[.!?])\s+")
_SPACED_DASH = re.compile(r"\s+(?:\u2014|\u2013|-)\s+")


def reads_as_a_receipt(text):
    said = " ".join(str(text or "").lower().split())
    if not said:
        return False
    readings = (said, _SPACED_DASH.sub(", ", said))
    for reading in readings:
        if _one_frame(reading):
            return True
    for reading in readings:
        first = _SENTENCE.split(reading)[0]
        if first != reading and _one_frame(first):
            return True
    return False


def _one_frame(said):
    for front, back in _SAID_BACK:
        if front and not said.startswith(front):
            continue
        if back and not said.endswith(back):
            continue
        middle = said[len(front):len(said) - len(back)].strip(" \u2014-.:,;")
        if middle:
            return True
    return False
WORK_FRAMES = (
    "{Thing} \u2014 what do you do there?",
    "{Thing}. How long have you been there?",
    "{Thing} \u2014 is it a good place to work?",
    "{Thing}. What's a normal day like?",
)
WORK_PLACE = frozenset(("at", "in", "for"))

HABIT_TAIL = (
    "{Thing} \u2014 that's a proper routine.",
    "{Thing}. That's a habit now.",
    "{Thing} \u2014 keep that up and it'll stick.",
)
GOING_TAIL = (
    "{Thing} \u2014 how's it going?",
    "{Thing}, how long have you been at it?",
    "{Thing} \u2014 how are you finding it?",
)
TRIP_TAIL = (
    "{Thing} \u2014 have you been before?",
    "{Thing}. How long are you going for?",
    "{Thing} \u2014 that's something to look forward to.",
    "{Thing}. What do you want to do while you're there?",
)
OCCASION_TAIL = (
    "{Thing} \u2014 are you looking forward to it?",
    "{Thing}. That'll come round fast.",
    "{Thing} \u2014 that's something to look forward to.",
)
PET_TAIL_ONE = (
    "{Thing} \u2014 how long has it been with you?",
    "{Thing}. What's it like to live with?",
    "{Thing} \u2014 is it good company?",
)
PET_TAIL_MANY = (
    "{Thing} \u2014 do they get on?",
    "{Thing}. Who's in charge?",
    "{Thing} \u2014 how long have they been with you?",
)
OCCASION_FLAT_TAIL = (
    "{Thing}. That's a way off yet \u2014 and you can always leave early.",
    "{Thing} \u2014 the run-up is usually worse than the day itself.",
    "{Thing}. Not everything on the calendar has to be a highlight.",
)
DIARY_WORDS = (
    "dentist", "dental", "doctor", "doctors", "gp", "optician", "opticians", "clinic",
    "hospital", "scan", "x-?ray", "check\\s?-?up", "appointment", "interview", "viewing",
    "survey", "mot", "service", "haircut", "hairdresser", "barber", "physio",
    "physiotherapy", "chiropractor", "osteopath", "hygienist", "podiatrist", "midwife",
    "health visitor", "counselling", "vet", "blood test", "bloods", "jabs?", "injection",
    "hearing", "tribunal", "parents evening", "parents' evening", "sports day", "nativity",
    "recital")
DIARY_THING = re.compile(r"\b(?:" + "|".join(DIARY_WORDS) + r")\b", re.I)
DIARY_TIME = re.compile(
    r"\b\d{1,2}(?:[:.]\d{2})?\s*(?:am|pm|o'?clock)\b|\b(?:at|from|by)\s+\d{1,2}\b"
    r"|\b(?:morning|afternoon|evening|noon|midday|lunchtime|first thing)\b", re.I)
DIARY_TAIL = (
    "{Thing} \u2014 what time are you in?",
    "{Thing}. What time is it?",
    "{Thing} \u2014 is it first thing or later?",
)
DIARY_TIME_TAIL = (
    "{Thing} \u2014 is it far from you?",
    "{Thing}. Do you know where it is?",
    "{Thing} \u2014 somewhere you've been before?",
)
MEETING_TAIL = (
    "{Thing} \u2014 where are you meeting?",
    "{Thing}. Who else is going?",
    "{Thing} \u2014 what's the occasion?",
)
MEETING_TIME_TAIL = (
    "{Thing} \u2014 what time are you meeting?",
    "{Thing}. What time does it start?",
)
COMING_TO_STAY = re.compile(
    r"\b(?:coming|comes|visiting|staying|arriving|flying over|driving down|over for)\b", re.I)
VISIT_TAIL_ONE = (
    "{Thing} \u2014 how long is {who} staying?",
    "{Thing}. Is {who} staying long?",
    "{Thing} \u2014 how long has {who} got with you?",
)
VISIT_TAIL_MANY = (
    "{Thing} \u2014 how long are they staying?",
    "{Thing}. Are they staying long?",
    "{Thing} \u2014 have they got long with you?",
)
PLURAL_KIN = frozenset("""
    parents brothers sisters grandparents grandkids grandchildren children kids twins folks
    family relatives friends mates lads boys girls in laws in-laws
    """.split())
A_COMING_WORD = re.compile(
    r"\b(?:is|are|was|were|coming|comes|come|visiting|visits|visit|staying|stays|arriving|"
    r"arrives|flying|driving|stopping|stops)\b")


def _more_than_one_coming(said, start, word):
    if word in PLURAL_KIN:
        return True
    if word.endswith("s") and word[:-1] in facts.RELATIONS and word not in facts.RELATIONS:
        return bool(re.search(r"\b(?:are|were|were both|are both)\b", said))
    rest = said[start:]
    cut = A_COMING_WORD.search(rest)
    if cut:
        rest = rest[:cut.start()]
    if re.search(r"\band (?:i|me|we|us)\b", rest):
        return False
    return bool(re.search(r"\band\b|&", rest))
OCCASIONS = frozenset((
    "wedding", "weddings", "party", "parties", "birthday", "birthdays", "anniversary",
    "hen", "stag", "festival", "festivals", "concert", "gig", "gigs", "reunion",
    "graduation", "christening", "baptism", "barbecue", "bbq", "housewarming", "prom",
    "shower"))
SHOWER = frozenset(("baby", "bridal", "wedding", "naming"))
PLACES_WITH_THE = frozenset((
    "algarve", "cotswolds", "lakes", "highlands", "alps", "pyrenees", "cairngorms",
    "wight", "isle", "new forest", "peak district", "lake district", "states", "dales",
    "broads", "fens"))
THING_BEFORE = frozenset(("a", "an", "the", "my", "your", "his", "her", "our", "their"))
PAST_PLAN = frozenset("went was were been came returned back".split())
TRIP_VERB = re.compile(
    r"\b(?:going|gonna|off|flying|fly|flies|flew|driving|heading|travelling|traveling|sailing|"
    r"holiday|land|lands|landed|landing|arriv\w+|touch(?:es)? down|getting in|got in|get in)\b",
    re.I)
DESTINATION = re.compile(r"\b(?:to|off to|into)\s+(?:the\s+|a\s+|an\s+)?([a-z][a-z'\u2019-]*)",
                         re.I)
ARRIVE_VERB = re.compile(
    r"\b(?:land|lands|landed|landing|arriv\w+|touch(?:es)? down|fly|flies|flew|getting in|"
    r"got in|get in)\b", re.I)
DESTINATION_ARRIVAL = re.compile(
    r"\b(?:in|at|into)\s+(?:the\s+|a\s+|an\s+)?([a-z][a-z'\u2019-]*)", re.I)
NOT_A_TRIP = frozenset("""
    bed sleep work school college uni university gym doctor doctors dentist hospital shops shop
    town meeting interview court loo toilet hairdresser optician vet nursery see visit watch pick
    collect drop get take it that this them there here him her us me you

    appointment appointments scan scans checkup check-up clinic physio physiotherapy chiropractor
    midwife blood test tests xray x-ray hearing hearings trial trials court courts tribunal prison prisons
    jail jails cell custody remand probation solicitor lawyer

    funeral funerals burial cremation wake wakes

    be being been
    tesco asda sainsbury sainsburys morrisons lidl aldi coop co-op iceland waitrose supermarket
    office bank post
    """.split())
DATE_AHEAD = re.compile(
    r"\b(?:next|this|tomorrow|tonight|weekend|"
    r"in (?:january|february|march|april|may|june|july|august|september|october|november|"
    r"december|spring|summer|autumn|winter)|"
    r"on (?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)|"
    r"for (?:a|an|one|two|three|four|five|six|seven|eight|\d+) (?:(?:more|whole|extra) )?"
    r"(?:day|night|week|fortnight|month)s?)\b", re.I)
DREADED_OCCASION = re.compile(
    r"\b(?:hate|hates|hated|dread|dreads|dreading|dreaded|can'?t face|cant face|"
    r"not looking forward|dont want to go|don'?t want to go|dont fancy|don'?t fancy|"
    r"cant be bothered|can'?t be bothered|a drag|boring|obligated)\b", re.I)

HOW_LONG_ALREADY = re.compile(
    r"\bfor (?:a|an|one|two|three|four|five|six|seven|eight|\d+)\s*"
    r"(?:day|night|week|fortnight|month|weekend)s?\b|\bfor the weekend\b|\bfor a few days\b",
    re.I)


def reads_as_a_trip(clean):
    if not isinstance(clean, str) or not clean.strip():
        return None
    flat = " ".join(clean.lower().split())
    if not DATE_AHEAD.search(flat) or OBLIGED.search(flat):
        return None
    if set(re.findall(r"[a-z']+", flat)) & PAST_PLAN:
        return None
    if flat.startswith(("my ", "her ", "his ", "their ", "she ", "he ")):
        return None
    if not TRIP_VERB.search(flat):
        return None
    destination = DESTINATION.search(flat)
    if not destination and ARRIVE_VERB.search(flat):
        destination = DESTINATION_ARRIVAL.search(flat)
    if not destination or destination.group(1) in NOT_A_TRIP:
        return None
    after_to = re.findall(r"[a-z'’]+", flat[destination.start():])[1:5]
    if not_a_trip.not_a_destination(after_to, after_to[0] if after_to else ""):
        return None
    if set(after_to) & NOT_A_TRIP:
        return None
    if set(after_to) & OCCASIONS:
        if "shower" in after_to and not set(after_to) & SHOWER:
            return None
        return "occasion_flat" if DREADED_OCCASION.search(flat) else "occasion"
    head = after_to[0] if after_to else ""
    if head in THING_BEFORE or head.endswith(("'s", "’s", "s'")):
        named = after_to[1] if len(after_to) > 1 else ""
        two_word = " ".join(after_to[1:3])
        if not (head == "the" and (named in PLACES_WITH_THE or two_word in PLACES_WITH_THE)):
            return None
    if not head:
        return None
    return "trip"

HABIT = re.compile(
    r"\b(?:every (?:day|week|month|morning|evening|afternoon|weekend|other day)|"
    r"every (?:mon|tues|wednes|thurs|fri|satur|sun)day|"
    r"each (?:day|week|morning)|most days|most weeks|twice a (?:day|week|month)|"
    r"once a (?:day|week|month)|on (?:a|an) (?:monday|tuesday|wednesday|thursday|friday|"
    r"saturday|sunday))\b", re.I)
GOING = re.compile(r"\b(?:i(?:'ve| have) (?:been |just )?started|i(?:'ve| have) (?:taken up|got into|signed up)|i(?:'m| am) (?:trying|getting|"
                   r"working|building|writing|learning|practising|practicing)|i(?:'ve| have) been|"
                   r"started (?:again|back)|back (?:into|at) it)\b", re.I)
OBLIGED = re.compile(r"\b(?:have to|has to|had to|must|got to|gotta|need to|needs to|keeps|"
                     r"kept|constantly|always|every time|end up|ends up)\b", re.I)
FEELING = re.compile(
    r"\b(?:cry|cries|cried|crying|tears|sob\w*|weep\w*|panic\w*|anxious|anxiety|depress\w*|"
    r"numb|shak\w*|nightmares?|insomnia|miserable|upset|self[- ]harm\w*|hurt(?:ing)? myself|"
    r"feel(?:s|ing)? (?:low|down|awful|rubbish|empty|worthless)|"
    r"shout\w* at|yell\w* at|scream\w* at|swear\w* at|hit(?:s|ting)? (?:my|the|him|her|them)|"
    r"sick|sickness|vomit\w*|throwing up|threw up|throw up|nausea|nauseous|diarr\w*|"
    r"migraine\w*|angry|furious|rage|lash(?:ing)? out)\b", re.I)
GOING_BAD = re.compile(r"\b(?:badly|not|never|can'?t|cant|won'?t|wont|too much|too many|"
                       r"stop|stopped|give up|gave up|fail\w*|struggl\w*|hard|tough|"
                       r"shattered|exhausted|knackered|late|behind|broke)\b", re.I)

BUDGET_FRAMES = (
    "{Thing} \u2014 I'll keep any suggestions inside it: fixed bills and food first, then savings.",
    "{Thing}, then \u2014 I'll stick to that: fixed bills and food first, then a set amount to "
    "savings.",
    "{Thing} \u2014 noted, and I'll work within it: fixed bills and food first, then savings on "
    "payday.",
)
PERIOD = re.compile(r"\b(?:(?:a|an|per|each|every)\s+(?:day|week|fortnight|month|year)\b"
                    r"|weekly|monthly|fortnightly|yearly|annually|a month|in a month|"
                    r"a week|in a week)\b", re.I)
A_SPAN_OF_TIME = re.compile(
    r"\bfor\s+(?:the\s+(?:rest\s+of\s+)?(?:week|fortnight|month|year|day)\b"
    r"|this\s+(?:week|month|year)\b|next\s+(?:week|month|year)\b"
    r"|last\s+(?:week|month|year)\b|the\s+rest\b"
    r"|a\s+(?:week|fortnight|month|year|day)\b|an?\s+hour\b)", re.I)
FOR_A_THING = re.compile(r"\b(?:\d[\d,.]*|a few|a couple of|about)\s*(?:pounds?|quid|euros?|"
                         r"dollars?)?\s*(?:budget\s+)?for\s+(?:a|an|the|my|our|some|new)\b"
                         r"|\bbudget\s+for\s+(?:a|an|the|my|our|some|new)\b", re.I)
BUYING = re.compile(r"\b(?:buy|buys|buying|present|presents|gift|gifts|"
                    r"shopping for|looking for a|looking for some|looking for new|"
                    r"should i get|shall i get|which one|get (?:my|him|her|them|myself)|"
                    r"spend on|worth getting|what to get|need (?:a|some|new|another)\b|"
                    r"getting (?:a|an|one|some|new)\b(?!\s*(?:lot|bit|break|rest|handle|hold|"
                    r"sense|grip|kick|chance|look|few|couple|little|better|worse|"
                    r"grief|telling|hearing|going|ready))|after (?:a|an|some)\b(?!\s*(?:lot|bit|"
                    r"advice|help|idea|good|thought|while|time|break|rest|sense|point))|"
                    r"want (?:a|an|some|one|to get|to buy)\b(?!\s*(?:lot|bit|break|rest|handle|"
                    r"hold|sense|grip|kick|chance|look|few|couple|little))|"
                    r"planning (?:a|an|some|my|our)\b|moving (?:into|in|to|out|house|home)\b|"
                    r"redec\w+|renovat\w+|refurbish\w*)", re.I)
MONEY = re.compile(r"\b(?:money|loan|loans|pension|pensions|mortgage|mortgages|credit card|"
                   r"credit cards|overdraft|debt|debts|savings|insurance|benefits|"
                   r"universal credit|job|jobs|salary|wage|wages|tax|budget|budgets|plan|"
                   r"planner|finances?|rent|bills?|groceries)\b", re.I)

SPENDING_FRAMES = (
    "{Thing} \u2014 I'll keep what I suggest inside it.",
    "{Thing} \u2014 good, and everything I suggest will be within it.",
    "{Thing} \u2014 noted, and I'll stay under that with what I recommend.",
)
FOOD_FRAMES = (
    "{Thing} \u2014 I'll keep that in mind when I suggest food.",
    "{Thing}, good to know \u2014 I'll plan around it.",
    "{Thing} \u2014 noted, and I won't suggest anything that goes against it.",
)

DRINK_FRAMES = (
    "{Thing} \u2014 I'll keep that in mind for anything I suggest.",
    "{Thing}, good to know \u2014 I'll plan around it.",
    "{Thing} \u2014 noted, and I won't suggest a drink that goes against it.",
)
CONDITION_FOOD = {"coeliac": "gluten", "celiac": "gluten", "gluten intolerant": "gluten",
                  "lactose intolerant": "dairy"}
CONDITION_FRAMES = (
    "{Thing} \u2014 noted, and I'll keep {food} out of anything I suggest.",
    "{Thing}, good to know \u2014 I'll plan around the {food}.",
    "{Thing} \u2014 right, so nothing with {food} in it.",
)
OTHER_LIMIT_FRAMES = (
    "{Thing} \u2014 I'll keep that in mind for anything I suggest.",
    "{Thing}, good to know \u2014 I'll work around it.",
    "{Thing} \u2014 right, so that is off the table for them.",
)

LIMIT_FRAMES = {
    "move": (
        "{Thing} \u2014 so anything I suggest stays short and flat, with somewhere to sit.",
        "{Thing}, then. Nothing I put to you needs hours on your feet.",
        "{Thing} \u2014 noted, and I'll keep the days gentle and close to a seat.",
    ),
    "money": (
        "{Thing} \u2014 so I'll keep what I suggest to what costs nothing.",
        "{Thing}, then. Nothing that needs paying up front.",
        "{Thing} \u2014 noted, and nothing pricey in anything I put to you.",
    ),
    "move_stay": (
        "{Thing} \u2014 so it is the downstairs room or a bed moved down, a chair in the shower "
        "rather than a step over the bath, and the outings one at a time.",
        "{Thing}, then \u2014 book the bed that needs no stairs and keep the week's outings short "
        "and near a seat.",
    ),
    "other": (
        "{Thing} \u2014 noted, and I'll keep anything I suggest inside it.",
        "{Thing}, then \u2014 I'll plan around it and keep what I suggest inside it.",
    ),
}

A_STAY_PLAN = re.compile(
    r"\b(?:coming|comeing|come|comes|staying|stays|stay|stopping|to stay|visiting|visit)\b"
    r"|\b(?:we|i)(?:'re| are| am)?\s+having\s+(?:people|family|guests|my|her|his)\b", re.I)
A_TRIP_PLAN = re.compile(
    r"\b(?:going to|off to|heading to|away to|flying to|driving to|trip to|holiday|weekend away|"
    r"going away|staying near|in (?:june|july|august|september|october|november|december|"
    r"january|february|march|april|may))\b", re.I)
A_STAY_PERSON = re.compile(
    r"\b(?:mum|mam|mom|mother|dad|father|parents|gran|grandma|grandad|granny|nana|nan|"
    r"grandpa|grandparents|sister|brother|aunt|uncle|cousin|in laws|in-laws|mother in law|"
    r"father in law|friend|friends|guest|guests|visitors|family)\b", re.I)


def _the_plan_in_hand(memory, clean=""):
    lines = []
    if isinstance(clean, str) and clean.strip():
        lines.append(clean)
    if isinstance(memory, dict):
        for turn in reversed((memory.get("turns") or [])[-PLAN_TURNS:]):
            said = turn.get("user") if isinstance(turn, dict) else None
            if isinstance(said, str) and said.strip():
                lines.append(" ".join(said.split()))
    for said in lines:
        if A_STAY_PLAN.search(said) and A_STAY_PERSON.search(said):
            return "stay"
    for said in lines:
        if A_TRIP_PLAN.search(said) and not a_limit_on_the_plan(said):
            return "trip"
    return None


_LIMIT_ONLY = frozenset(("people", "relations", "other", "others", "relation", "detail"))

_OPENS_WITH_AN_ASK = re.compile(
    r"^\s*(?:what|which|how|where|when|who|why|should|shall|can|could|would|will|do|does|"
    r"did|is|are|was|were|any|anyone|anything|tell me|give me|suggest|recommend)\b", re.I)

LIKES_FRAMES = (
    "{Thing} \u2014 what is it you like about it?",
    "{Thing} \u2014 what is it about it that gets you?",
    "{Thing}. Good to know \u2014 what do you like best about it?",
    "{Thing} \u2014 that goes in the keep pile. I'll remember it.",
)
A_LIKE_OF_ONE_THING = re.compile(r"^(?!(?:.*\b(?:and|but|because|so|though|although|when|if|"
                                 r"which|that)\b)).{2,40}$", re.I)


A_LIKE_ECHO = re.compile(
    r"^(?:you|we)\s+(?:really\s+|absolutely\s+|just\s+|still\s+|also\s+|do\s+|both\s+)?"
    r"(?:love|like|adore|enjoy|prefer)\s+(?P<thing>[^,;]+)$", re.I)
A_LIKE_WITH_TWO_HALVES = re.compile(
    r"\b(?:and|but|because|so|though|although|when|if|which|that|than|too)\b", re.I)
A_PERSON_LIKED = re.compile(
    r"\b(?:girl|boy|man|woman|guy|bloke|lad|lass|person|someone|somebody|people|they|them|him|her"
    r"|his|hers|theirs)\b", re.I)


def _a_like_of_one_thing(clean, memory=None):
    echo = _echo(clean, memory)
    match = A_LIKE_ECHO.match(echo or "")
    if not match:
        return False
    thing = match.group("thing")
    if A_LIKE_WITH_TWO_HALVES.search(thing) or A_PERSON_LIKED.search(thing):
        return False
    return not any(re.search(r"\b" + re.escape(word) + r"\b", thing, re.I)
                   for word in (facts.RELATIONS or ()))


def _only_a_liking(found):
    rest = {key for key, value in (found or {}).items()
            if value and key not in ("tastes", "pets") and not key.endswith("_frame")}
    return bool((found or {}).get("tastes")) and not rest


def a_liked_thing(found):
    for entry in (found or {}).get("tastes") or []:
        if not isinstance(entry, dict) or str(entry.get("how") or "") != "yes":
            continue
        thing = " ".join(str(entry.get("thing") or "").split()).strip(" ,.:;!?")
        if (thing and "{" not in thing and "}" not in thing
                and len(thing.split()) <= 4 and A_LIKE_OF_ONE_THING.match(thing)):
            return thing
    return ""


_AN_ABILITY = re.compile(
    r"\b(?:can'?t|cannot|can not|isn'?t able to|is not able to|not able to|only manage)\s+"
    r"(?:walk|climb|manage|stand|sit)\b"
    r"|\b(?:can'?t|cannot|can not|isn'?t able to|is not able to|not able to|only manage)\s+"
    r"(?:do|manage|get\s+up|get\s+up\s+and\s+down|get\s+up\s+the|use|cope\s+with)\s+"
    r"(?:the\s+|a\s+|any\s+)?(?:more\s+)?(?:stairs?|steps?|hills?|walks?|walking|"
    r"climbing|standing)\b", re.I)

PLAN_TURNS = 3


def a_limit_reply(text, memory=None):
    if not isinstance(text, str):
        return None
    clean = " ".join(text.split())
    if not clean or "?" in clean:
        return None
    if _OPENS_WITH_AN_ASK.match(clean):
        return None
    family = a_limit_on_the_plan(clean)
    if family is None:
        return None
    if not _AN_ABILITY.search(clean) and not _a_plan_on_the_table(memory, clean):
        return None
    found = _learned(text, memory)
    if found and not set(found) <= _LIMIT_ONLY:
        return None
    return _a_limit_reply(clean, family, memory)


WANTS_IT = re.compile(
    r"\b(?:i|we)\s+(?:want|wanna|need|'?d like|'?d rather|would like|would rather)\s+to\b", re.I)


def _a_plan_on_the_table(memory, clean=""):
    if isinstance(clean, str) and WANTS_IT.search(clean):
        return True
    if not isinstance(memory, dict):
        return False
    seen = 0
    for turn in reversed(memory.get("turns") or []):
        said = turn.get("user") if isinstance(turn, dict) else None
        if not isinstance(said, str) or not said.strip():
            continue
        seen += 1
        if seen > PLAN_TURNS:
            return False
        if facts.PLAN.search(said) and not facts.a_limit_on_the_plan(said):
            return True
        if (facts.extract(said) or {}).get("plan"):
            return True
    return False


SAID_BACK_WORDS = 7

LIMIT_AFTER_THE_LINE = {
    "move": (
        "So anything I suggest stays short and flat, with somewhere to sit.",
        "Then nothing I put to you needs hours on your feet, and there is a seat at the end of it.",
    ),
    "money": (
        "So I'll keep what I suggest to what costs nothing.",
        "Then nothing I put to you needs paying up front.",
    ),
    "move_stay": (
        "Then it is the downstairs room or a bed moved down, a chair in the shower rather than a "
        "step over the bath, and the outings one at a time.",
        "Then book the bed that needs no stairs, and keep the week's outings short and near a seat.",
    ),
}


def _a_limit_reply(clean, family, memory):
    body = _echo(clean) or clean
    if family == "move" and _the_plan_in_hand(memory, clean) == "stay":
        family = "move_stay"
    if len(body.split()) > SAID_BACK_WORDS:
        after = LIMIT_AFTER_THE_LINE.get(family)
        if after:
            return _pick_ending(after, memory)
    frames = LIMIT_FRAMES.get(family) or LIMIT_FRAMES["other"]
    return _pick_ending(frames, memory, thing=body, Thing=body[:1].upper() + body[1:])


def a_limit_for_the_plan(text, memory=None):
    if not isinstance(text, str):
        return None
    clean = " ".join(text.split())
    if not clean or "?" in clean or _OPENS_WITH_AN_ASK.match(clean):
        return None
    family = a_limit_on_the_plan(clean)
    if family is None:
        return None
    if not there_is_a_chat(memory):
        return None
    if _the_plan_in_hand(memory) != "stay":
        return None
    return _a_limit_reply(clean, family, memory)

UP_CLOSED = (r"(?!\s+(?:the|a|an|it|this|that|these|those|my|his|her|their|your|our|"
             r"into|over|between)\b)")
LEFT_CLOSED = (r"(?=\s*(?:[,.!?;]|$|\b(?:for|after|last|in|on|at|with|when|because|so|and|"
               r"since|about|yesterday|today|tonight)\b))")

SEPARATION = re.compile(
    r"\b(?:left me|leaving me)" + LEFT_CLOSED + r"|"
    r"\b(?:walked out on|dumped me|cheated on me)\b|"
    r"\b(?:broke up|split up)" + UP_CLOSED + r"|"
    r"\bdivorce\w*\b|"
    r"\b(?:he|she|they|my (?:wife|husband|partner|boyfriend|girlfriend|ex))\b[^.!?]{0,16}"
    r"\bmoved out\b|\b(?:we|my \w+ and i) separated\b")

HEAVY_TURNS = 3

_NOT_A_BODY_PART = (r"(?<!\b(?:my|his|her|their|your|our)\s)(?<!\b(?:the|a)\s)"
                    r"(?<!\b(?:knee|back|leg|legs|arm|arms|head|shoulder|shoulders|neck|foot|"
                    r"feet|hip|hand|hands|stomach|tooth|teeth|ear|ears|eye|eyes|chest|ankle|"
                    r"wrist|joint|joints|muscle|muscles)\s)")
_BULLIED = re.compile(
    r"\b(?:bull(?:y|ies|ied|ying))\b|\bpick(?:s|ed|ing)?\s+on\b|\bpicked\s+on\b|"
    r"\bpicks\s+on\b|\bmean\s+to\s+(?:me|him|her|them|us|my\b)|"
    r"\bpicked\s+on\s+(?:me|him|her|them|us)\b", re.I)
HURTS_A_PERSON = re.compile(
    r"\b(?:he|she|they|my\s+\w+|his\s+\w+|her\s+\w+|the\s+\w+)\s+"
    r"(?:(?:hit|hits|hit(?:ting)?|punch\w*|kick\w*|shov\w*|"
    r"slap\w*|smack\w*|threaten\w*)\s+"
    r"(?:me|him|her|them|us|the\s+(?:kids|children|baby|little\s+one))\b"
    r"|(?:beat|beats|beating)\s+"
    r"(?:me|him|her|them|us|the\s+(?:kids|children|baby|little\s+one))\b"
    r"(?!\s*(?:at|in|on)\s+(?:the\s+|a\s+|his\s+|her\s+|their\s+)?[a-z]))"
    r"|\b(?:shout|shouts|shouting|swear|swears|swearing|yell|yells|yelling)\s+"
    r"(?:at|at)\s+(?:me|him|her|them|us|the\s+(?:kids|children|baby|little\s+one))\b"
    r"|\b(?:is|are|was|were|being)\s+horrible\s+to\s+(?:me|him|her|them|us)\b"
    r"|\b(?:he|she|they|my\s+\w+|his\s+\w+|her\s+\w+)\s+(?:was|is|were|are|"
    r"has\s+been|had\s+been|got)\s+violent\b"
    r"|\b(?:violent|violence)\s+(?:to|towards|with|at)\s+(?:me|him|her|them|us)\b"
    r"|\b(?:was|were|am|is|being|been)\s+harass\w*\s+(?:at|on|in)\b", re.I)
A_NAME_WAS_VIOLENT = re.compile(
    r"^\s*(?!(?:the|a|an|it|there|this|that|these|those|my|his|her|their|your|our|we|i|you|he|"
    r"she|they)\b)[a-z][a-z'\u2019-]*\s+"
    r"(?:was|is|were|are|has\s+been|had\s+been|got)\s+violent\b", re.I)


def reads_as_cruelty(said):
    text = " ".join(str(said or "").split())
    if not text:
        return False
    if _BULLIED.search(text) or A_NAME_WAS_VIOLENT.search(text):
        return True
    return bool(HURTS_A_PERSON.search(text))

HEAVY_FRAMES = (
    "{Thing} \u2014 I'm sorry it's all coming at once.",
    "Got it \u2014 {thing}. That's a hard week.",
    "{Thing}. I'm sorry there's so much on your plate.",
)
STILL_FRAMES = (
    "{Thing} \u2014 got it. And I'm sorry it's a hard time.",
    "{Thing}. Noted \u2014 and I'm sorry you're having a hard week.",
    "{Thing} \u2014 I've got that. Still sorry for what you're going through.",
)

LEAD_IN = ("hi", "hiya", "hello", "hey", "so", "well", "oh", "and", "also", "ok", "okay", "right",
           "because", "cos", "coz", "cause", "cuz", "because of", "cos of",
           "yeah", "yes", "actually", "anyway", "btw", "by the way", "just so you know",
           "quick one", "sorry", "haha", "lol", "oh and", "for the record",
           "one thing", "that reminds me", "thanks", "thank you", "cheers", "ta", "cool",
           "sorry one more thing", "one more thing", "one last thing", "last thing",
           "nice", "great", "yep", "yup", "mmm", "haha",
           "to be honest", "to be fair", "if im honest", "if i am honest", "if im being honest",
           "honestly", "tbh", "to tell the truth", "truth be told", "not going to lie",
           "not gonna lie", "ngl", "i wont lie", "i have to say", "i must admit",
           "i will say", "ill be honest", "to be truthful")
WANTS_ANSWER = re.compile(r"\b(?:what|which|how|where|whereabouts|when|who|why|whats|hows|"
                           r"whos|wheres)\b", re.I)
GREETING = re.compile(r"^\s*(?:hi|hiya|hello|hey|morning|good morning|evening|yo|howdy)\b", re.I)
DEATH_WORDS = re.compile(r"\b(?:die|died|dies|dying|death|dead|kill|killed|suicide)\b", re.I)
ON_NIGHTS = re.compile(
    r"\b(?:(?:i|we)\s+(?:work|works|do|does|am on|are on|am doing|are doing|'m on|'re on)\s+"
    r"(?:the\s+)?night(?:s|\s+shift(?:s)?)?\b"
    r"|night shifts?\b|\bon nights\b|\bnights this week\b)", re.I)
EARLY_RISE = re.compile(
    r"\b(?:i|we)\s+(?:get up|get|start|leave|wake up|am up|are up|have to be up|'m up)"
    r"\s+(?:at|by|for)\s+(?:\d{1,2}(?:[:.]\d{2})?\s*(?:am|pm)?|four|five|six|seven|"
    r"half (?:four|five|six))\b", re.I)
LATE_FINISH = re.compile(
    r"\b(?:i|we)\s+(?:finish|finishes|get home|am back|'m back)\s+(?:at|around|about|by)\s+"
    r"(?:\d{1,2}(?:[:.]\d{2})?\s*(?:am|pm)?|nine|ten|eleven|twelve|half (?:nine|ten|eleven))\b",
    re.I)
LONG_SHIFT = re.compile(
    r"\b(?:\d{1,2}|twelve|ten|eleven)\s*[- ]?hour (?:shift|shifts|days?)\b"
    r"|\blong (?:days|shifts)\b|\bwork(?:ing)? long hours\b", re.I)
SHIFTS_ALL_OVER = re.compile(
    r"\b(?:my|our|the)\s+(?:shifts?|rota|hours)\s+(?:is|are|change|changes|move|moves|rotate|rotates|"
    r"all over|all over the place|everywhere|different|random|mad)\b"
    r"|\bshifts? (?:all over|all over the place|everywhere)\b"
    r"|\bwork(?:ing)? two jobs\b|\bsecond job\b", re.I)
WORK_FROM_HOME = re.compile(r"\bwork(?:ing)? from home\b|\bwork from home\b|\bwfh\b", re.I)
NIGHT_TAIL = (
    "Nights turn the week upside down. The sleep in the day is never quite the same as the sleep "
    "at night, and that is the part people underrate.",
    "Nights, then. It is a different world at three in the morning, and not many people see it.",
    "Nights are hard on the body clock. Whatever makes the sleep after a shift work is worth "
    "protecting.",
)
EARLY_TAIL = (
    "That is an early start. The night before is where those mornings are won or lost.",
    "Up at that hour, the whole day is done by lunchtime. It is the evening that has to be "
    "guarded.",
    "That is a hard hour to be up, and it gets easier once the going to bed moves with it.",
)
LATE_TAIL = (
    "Finishing that late means the evening has gone by the time you are out. The wind-down is the "
    "bit worth protecting.",
    "That is a long day by the time you are home. The last hour of it is the one to keep for "
    "yourself.",
    "Home at that hour, the day turns into the next one. Best to have the food and the quiet "
    "already waiting.",
)
LONG_TAIL = (
    "Those are long days. Whatever you do for yourself has to be small enough to happen when you "
    "are wrecked.",
    "Long shifts like that leave nothing of the day. The food and the sleep are the parts that "
    "actually matter.",
    "That is a lot of hours. The days off are not a bonus, they are the half of the week that "
    "makes the rest work.",
)
SPREAD_TAIL = (
    "Shifts that move make the week hard to plan. The few fixed things - sleep, one day off, a "
    "meal at a set time - are what hold it together.",
    "A rota like that means no two weeks are the same. Worth putting the things you care about "
    "in before the rota comes out, not after.",
    "That kind of week is hard to build anything on. Whatever is regular in it is doing a lot of "
    "the work.",
)
HOME_TAIL = (
    "Working from home, the day has no edges unless you put them in. A walk at the end of it "
    "stands in for the commute.",
    "That suits a lot of people and it eats a lot of people. The bit that helps is stopping at a "
    "time rather than when the work runs out.",
    "Home all day, the work and the rest end up in the same room. A door you can shut, or a walk "
    "out of it, does more than any system.",
)
AN_ASK = re.compile(
    r"^(?:(?:and|so|but|ok|okay|well|also|plus)\s+)*(?:should|shall|can|could|do|does|did|is|are|"
    r"was|were|will|would|may|might|am|have|has|any|what|whats|which|how|hows|where|wheres|"
    r"whereabouts|when|who|whos|why)\b", re.I)


def reads_as_an_ask(line):
    return "?" in line or bool(AN_ASK.match(str(line or "").strip()))


NOT_THE_HOURS = re.compile(
    r"\b(?:cant sleep|can'?t sleep|not sleeping|insomnia|exhaust\w*|knackered|shattered|"
    r"burn(?:t|ed) out|depress\w*|anxi\w*|panic|stress\w*|fed up|sick of|had enough|"
    r"hate|hates|quit|quitting|resign\w*|sacked|fired|redundant|laid off|losing my job|lost my job|"
    r"overtime|pay|paid|wage|wages|money|salary|boss|manager|colleague|interview|contract|"
    r"holiday|annual leave|tips|advice|how do i|how can i|what should|should i|help me|"
    r"pregnant|baby|kids?|child|school run|uni|college|course|exam)\b", re.I)

WHEN_DETAIL = re.compile(
    r"^(?:and |oh |also |so |but )?"
    r"(?:(?:its|it's|it is|thats|that's|that is|were|we're|i'm|im)\s+(?:(?:on|in)\s+)?"
    r"|(?:on|in)\s+|and\s+)"
    r"(?P<when>"
    r"tomorrow|tonight|today"
    r"|this (?:weekend|week|morning|evening|afternoon)"
    r"|next (?:week|month|weekend|year)"
    r"|monday|tuesday|wednesday|thursday|friday|saturday|sunday"
    r"|(?:\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten)"
    r"\s+(?:days?|weeks?|months?)"
    r"|a (?:few|couple of) (?:days|weeks)"
    r"|a couple of (?:days|weeks)"
    r")"
    r"(?:\s+(?:away|left|to go))?\s*[.!]*$", re.I)
WHEN_TODAY = re.compile(r"\b(?:today|tonight|this (?:morning|afternoon|evening))\b", re.I)
WHEN_TOMORROW = re.compile(r"\btomorrow\b", re.I)
WHEN_DAYS = re.compile(
    r"\b(?:this (?:week|weekend)|monday|tuesday|wednesday|thursday|friday|saturday|sunday"
    r"|a few days|a couple of days)\b", re.I)
COUNTED = re.compile(r"\b(\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten)"
                     r"\s+(days?|weeks?|months?)\b", re.I)
COUNT = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
         "eight": 8, "nine": 9, "ten": 10}


def _shape_of(when):
    if WHEN_TODAY.search(when):
        return "today"
    if WHEN_TOMORROW.search(when):
        return "tomorrow"
    found = COUNTED.search(when)
    if found:
        number = COUNT.get(found.group(1).lower(), found.group(1))
        unit = found.group(2).lower()
        if unit.startswith("month"):
            return "room"
        if int(number) <= (5 if unit.startswith("day") else 1):
            return "days"
        return "room"
    if WHEN_DAYS.search(when):
        return "days"
    return "room"


WHEN_TODAY_TAIL = (
    "{When}, so the first of it happens now: a small thing done today beats a better one that "
    "waits for a quiet hour.",
    "There is no day left to work up to it in. {When} is the day, so start at the first step.",
    "{When} is already here, which makes the part of it you were saving for later today's job.",
)
WHEN_TOMORROW_TAIL = (
    "Tomorrow, so today is the working day: the first step now beats a good plan for the morning.",
    "That leaves today for it. Do the part you would least like to be doing at the last minute.",
    "Tomorrow, then. Whatever in that needs two sittings has to have the first of them today.",
)
WHEN_DAYS_TAIL = (
    "{When} is one step a day rather than all of it at once: pick the first step and give it "
    "today.",
    "{When}, so count the days and put a step in each one. The last day is for checking, not "
    "starting.",
    "{When} only fits the whole of it if each day carries a bit of it: start today, not on "
    "the last one.",
)
WHEN_ROOMY_TAIL = (
    "{When} is enough time if you spread it: one small bit a week, and the last week only "
    "checking.",
    "{When} gives you room to do it properly. Start with the part you would least like to get "
    "wrong.",
)
TIME_WORD = (r"(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
             r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)")
CLOCK_DETAIL = re.compile(
    r"^(?:and |oh |also |so |but )?"
    r"(?:(?:its|it's|it is|thats|that's|that is|were|we're|the\s+[a-z'-]+\s+is)\s+)?"
    r"(?:at\s+|for\s+)?"
    r"(?P<when>"
    r"\d{1,2}[:.]\d{2}\s*(?:am|pm|a\.m\.|p\.m\.)?"
    r"|\d{1,2}\s*(?:am|pm|a\.m\.|p\.m\.)"
    r"|\d{1,2}\s*o'?\s?clock"
    r"|(?:half|quarter)\s+(?:(?:past|to)\s+)?" + TIME_WORD +
    r"|(?:five|ten|twenty|twenty[- ]five)\s+to\s+" + TIME_WORD +
    r"|" + TIME_WORD + r"\s+(?:o'?\s?clock|am|pm|a\.m\.|p\.m\.|thirty|fifteen|"
    r"forty[- ]five)"
    r"|\d{1,2}\s+(?:thirty|fifteen|forty[- ]five))"
    r"\s*[.!]*$", re.I)
CLOCK_AT = re.compile(
    r"^(?:and |oh |also |so |but )?"
    r"(?:(?:its|it's|it is|thats|that's|that is|the\s+[a-z'-]+\s+is)\s+)?"
    r"(?:at|for)\s+"
    r"(?P<when>(?:\d{1,2}[:.]\d{2}|\d{1,2}|" + TIME_WORD + r")(?:\s*(?:am|pm))?)"
    r"\s*[.!]*$", re.I)
CLOCK_MORNING_TAIL = (
    "{At} on the day, so be there twenty minutes early and the nerves have somewhere to sit while "
    "you wait.",
    "{At}, so the day is built around it, and the bit that wants you sharp belongs before you "
    "set off rather than after.",
    "{At}, so there is enough of the morning to get ready without rushing it, which is usually the "
    "part that decides how it goes.",
)
CLOCK_AFTER_TAIL = (
    "{At}, so the morning is free for the part that needs you sharp, and nothing else has to fit "
    "round it.",
    "{At} on the day: get the other jobs done in the morning so you go into it with nothing else "
    "on your mind.",
    "{At}, so the morning is where the part that wants a steady head goes, and the afternoon is "
    "clear for it.",
)
CLOCK_EVENT = re.compile(
    r"\b(?:dentist|dental|optician|hygienist|doctor|gp|surgery|vet|clinic|hospital|"
    r"hearing|interview|appointment|scan|exam|test|checkup|check-up|consultant|physio|"
    r"physiotherapy|podiatrist|chiropodist|midwife|blood\s+test|presentation)\b", re.I)
CLOCK_FLAT = re.compile(
    r"\b(?:meeting|viewing|shift|class|lesson|lecture|rehearsal|assessment|haircut|tattoo|"
    r"collection|pickup|lunch|dinner|breakfast|drinks|supper)\b", re.I)
CLOCK_FLAT_TAIL = (
    "{At}, then, and the rest of the day arranges itself round it rather than the other way round.",
    "{At} on the day, so what comes before it is short and what comes after it is free.",
    "{At}, so the day is built round it and nothing else has to be squeezed in before it.",
)
CLOCK_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
               "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
               "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
               "nineteen": 19, "twenty": 20}


def _clock_shape(when):
    said = str(when or "").lower()
    found = re.search(r"\d{1,2}|[a-z]+", said)
    if not found:
        return "morning"
    token = found.group(0)
    hour = CLOCK_WORDS.get(token) if not token.isdigit() else int(token)
    if hour is None:
        return "morning"
    if "pm" in said or "p.m" in said:
        return "after"
    if "am" in said or "a.m" in said:
        return "morning"
    if hour <= 3:
        return "after"
    return "morning" if hour < 12 else "after"
STEP_OPENS = re.compile(
    r"^\s*(?:first|firstly|start|begin|own|book|name|skip|put|blot|pour|turn|take|check|keep|let|"
    r"leave|get|add|cut|fill|soak|wash|rinse|call|ask|write|print|plan|split|break|set|read|look|"
    r"watch|listen|tell|say|try|do|go|sit|spend|give|use|make|run|buy|pick|wear|choose|cook|boil|"
    r"roast|fry|steam|bake|rest|chill|freeze|store|measure|weigh|clean|wipe|scrape|open|hold|walk|"
    r"drive|move|cover|line|grease|trim|water|feed|brush|email|text|ring|phone|budget|save|"
    r"avoid)\b", re.I)


def _tells_them_what_to_do(said):
    opening = re.split(r"(?<=[.!?])\s+", str(said or "").strip(), maxsplit=1)[0]
    return bool(STEP_OPENS.match(opening.strip()))


WOULD_HAVE_BEEN = re.compile(r"\bwould(?:\s*have|'ve)?\s+(?:\w+\s+){0,2}been\b", re.I)
BODY = re.compile(
    r"\b(?:pain\w*|ache\w*|aching|hurts?|hurting|illness|poorly|unwell|fever\w*|"
    r"rash\w*|swell\w*|swollen|infec\w*|antibiotic\w*|blood\w*|"
    r"choked?|choking|swallow\w*|dizz\w*|nausea\w*|vomit\w*|diarrhoea|migraine\w*|"
    r"sore|cramp\w*|symptom\w*|injur\w*|wound\w*|fractur\w*|"
    r"surger\w*|operation|a&e|111|999|seiz\w*|sezure|breathless\w*|x-ray|xray)\b", re.I)
BODY_STATE_WORDS = frozenset("""faint faintish fainting woozy dizzy giddy groggy wobbly shaky
clammy sweaty queezy queasy nauseous nauseated bilious sickly bunged sniffly sniffles sniffing
croaky hoarse congested sneezing lightheaded
pale pallid ashen grey gray greyish grayish mottled blotchy spotty puffy bloated flushed
feverish shivery tender husky snotty""".split())
BODY_STATE_PHRASES = frozenset(("light headed", "bilious", "bunged up", "blocked up"))
BODY_STATE_TAIL = frozenset("""today tonight now still again though honestly already here
actually really so very absolutely bloody thanks up and""".split())


def _a_bare_state(clean):
    words = [w.strip(".,!?;:") for w in clean.replace("-", " ").split()]
    words = [w for w in words if w]
    if words[:1] in (["im"], ["i'm"], ["iam"]):
        words = words[1:]
    elif words[:2] == ["i", "am"]:
        words = words[2:]
    else:
        return False
    if not words:
        return False
    if " ".join(words) in BODY_STATE_PHRASES:
        return True
    return (any(w in BODY_STATE_WORDS for w in words)
            and all(w in BODY_STATE_WORDS or w in BODY_STATE_TAIL for w in words))


BLEED = re.compile(r"\bbleed\w*\b(?![^.!?]{0,12}\b(?:dry|radiator|boiler|pipe\w*)\b)", re.I)
SELF_INTRO = re.compile(r"^\s*(?:i(?:'m| am)|im|my name(?:'s| is))\s+[A-Z][a-z'\u2019-]+\b")
MEET_GREET = re.compile(
    r"^\s*(?:(?:nice|good|great|pleased|lovely|glad|happy|grand)\s+to\s+"
    r"(?:meet|see|hear\s+from)\s+(?:you|u|ya)\b"
    r"|(?:good|great|lovely|nice)\s+to\s+have\s+you\b"
    r"|how\s+(?:are|r)\s+(?:you|u|ya)\b"
    r"|how(?:'s|s|\s+is)\s+(?:it\s+going|things|tricks|you\s+doing|your\s+day)\b"
    r"|how\s+do\s+you\s+do\b"
    r"|long\s+time\s+no\s+see\b)", re.I)
SUBJECT = (r"(?:i|i'm|im|i've|i'd|we|we're|my|our|mine|she|she's|he|he's|it|it's|they|"
           r"they're|his|her|its|their)")
STOP = re.compile(r"\s*(?:,\s|;|\.\s|$|\b(?:because|so|but)\b|\b(?:and|then)\b\s+(?="
                  + SUBJECT + r"\b))\s*", re.I)
WORD = re.compile(r"[A-Za-z0-9'\u2019-]+")
POLITE = re.compile(r"[,\s]+(?:thanks|thank you|cheers|ta|please|thx)\s*$", re.I)
from .filler import TAIL_OFF, without_filler
STATE = re.compile(
    r"\b(?:is|are|am|im|'s|'re|'m|was|were|has|have|had|'ve|ive|can|will|'ll|need|needs|want|wants|"
    r"live|lives|work|works|study|studies|love|loves|like|likes|prefer|prefers|go|goes|going|"
    r"off to|plan|plans|planning|train|training|learn|learning|move|moving|fly|flying|getting|"
    r"got|adopted|allergic|spend|save|saving)\b", re.I)
TROUBLE = re.compile(
    r"\b(?:being|bullied|bullies|bully|teas\w+|never|always|keeps|kept|refuses|refused|"
    r"stopped|stops|quit|hates?|hated|hit|hits|shout\w*|yell\w*|scream\w*|argu\w*|row|"
    r"won'?t|doesn'?t|didn'?t|isn'?t|can'?t|cannot|failed|failing|behind|ignores?|ignored|"
    r"blames?|blamed|lost|losing|dead against|just want|just need|driving me|drives me|"
    r"doing my head in|fed up|sick of|had enough|tether|drives? me mad)\b", re.I)
_EMPTY = frozenset("""a an the and or but if so then this that these those it its it's i i'm im me my
we we're us our you your he she they them his her their is are was were be been being am 's 're
of to in on at for with from about as not no do does did have has had will would can could just
really very too also still now""".split())
_FEELING_WORDS = (
    r"worried|frightened|scared|terrified|afraid|fear\w*|dread\w*|anxious|panic\w*|"
    r"overreacting|upset|angry|annoyed|sad|lonely|guilty|embarrassed|ashamed|stressed|"
    r"exhausted|knackered|weary|miserable|cry|cried|crying|tears?|sob\w*|moan\w*|whinge\w*|"
    r"whine|rant\w*|vent\w*")
A_FEELING = re.compile(r"\b(?:" + _FEELING_WORDS + r")\b", re.I)
GOOD_MOOD = re.compile(
    r"\b(?:in (?:a|an) (?:very )?(?:good|great|fine) mood|good mood|great mood|feeling good|"
    r"feel good|feeling great|feel great|cheerful|cheery|in good spirits)\b", re.I)
A_EVENT = re.compile(
    r"\b(?:job|promotion|baby|exam|test|interview|offer|house|flat|course|degree|wedding|"
    r"engagement|engaged|pregnant|expecting|won|passed|accepted|hired|booked|sold|bought|"
    r"holiday|graduated|qualified|retired)\b", re.I)
A_CLEAR = re.compile(
    r"\b(?:all clear|(?:came|come|comes) back clear|(?:scan|results?|tests?) (?:was|is|were|are) "
    r"clear|given? the all clear)\b", re.I)


A_RESULT = re.compile(
    r"\b(?:i|we|he|she|they|my \w+|our \w+)\s+(?:(?:just|finally|only|also|now)\s+)?"
    r"(?:got|gotten|finished|finishes|started|starts|passed|passes|won|wins|landed|booked|"
    r"sold|bought|completed|handed in|graduated|qualified|retired)\b"
    r"|\b(?:went|gone) (?:well|great|brilliant|fine)\b"
    r"|\bout of (?:the )?hospital\b|\bhome from (?:the )?hospital\b", re.I)
A_MOVED = re.compile(r"\b(?:moved|moving|move) (?:in|into|to|house|out|abroad|back|country)\b",
                     re.I)


def has_news(text):
    text = text or ""
    return bool(A_EVENT.search(text) or A_CLEAR.search(text) or A_RESULT.search(text)
                or A_MOVED.search(text))


COMPLAINT = re.compile(
    r"\bhad a (?:go|dig|pop) at\b|\b(?:gave|given|handed) me a (?:ticket|fine|bollocking)\b|"
    r"\b(?:got|get|gets|getting|received) (?:a |an |the |my )?(?:parking |speeding |"
    r"fixed penalty )?(?:ticket|penalty|caution|warning|bollocking)\b|"
    r"\b(?:got|get|gets|getting|received|gave me) (?:a |an |the )?fine\b"
    r"(?!\s+(?:view|views|day|time|weather|meal|bit|line|mess|idea|point|thing|way|year))|"
    r"\b(?:parking|speeding) ticket\b|\bclamped\b|\b(?:a|the) telling off\b|"
    r"\btold (?:me )?off\b|\ba bollocking\b", re.I)
_NOT_A_DETAIL = re.compile(
    r"\b(?:bye|goodnight|good night|catch (?:you|up)|speak (?:later|soon)|talk later|see you|"
    r"night then|anyway|back to|as i said|like i said|nothing much|not much|"
    r"can'?t complain|same old|same as ever|not a lot|how about you|you\?|"
    r"fair enough|sounds good|(?:i'?ll|i will|ill) (?:try|give) (?:that|it)|will do|no worries|"
    r"nice one|same to you|not bad|all good|"
    r"want(?:ed)? to (?:say|ask|tell)|how (?:do|should) i put it|\bmeant\b|\bsoz\b|"
    r"\bi (?:said|told you|mentioned|already|just said)\b|\bas i said\b|\blike i said\b|"
    + COMPLAINT.pattern +
    r"|" + _FEELING_WORDS + r")\b", re.I)
_SAID_YES_NO = re.compile(r"^(?:no|nope|nah|yes|yeah|yep)\b(?=[,.!]|\s+(?:please|thanks|thank you|"
                          r"mate|then)\b|$)", re.I)
_ANSWER_OPENER = re.compile(r"^(?:ok|okay|course|right)\b[ ,]", re.I)
_ASKS_MIDWAY = re.compile(r"\b(?:is|are|was|were|do|does|did|can|could|should|would|will|shall|"
                          r"have|has)\s+(?:it|that|this|they|i|we|you|he|she)\b", re.I)
_ASKED_FOR = re.compile(r"^(?:any|anything|something|someone|somewhere|nowhere|nothing)\b", re.I)
DIGIT = re.compile(r"\d")
_FAULT = re.compile(
    r"\b(?:leak\w*|drip\w*|blocked|clogged|jammed|stuck|won'?t start|won'?t turn on|"
    r"stopped working|not working|isn'?t working|broken|broke|bang(?:s|ing)?|rattl\w*|noisy|"
    r"grind\w*|screech\w*|whin\w*|error code|flashing|blinking|rust\w*|damp|mould\w*)\b",
    re.I)
_NOT_A_DETAIL_SUBJECT = re.compile(
    r"\b(?:funeral|grief|passed away|passed on|death|died|widow|hospital|diagnos\w*|"
    r"lost (?:the|our|a) (?:baby|pregnancy)|miscarriage|stillborn|"
    r"cancer|chemo|depress\w*|anxiety|breakup|broke up|divorce)\b", re.I)
FRAGMENT = 30
WITH_SLASH = re.compile(r"\bw/\s*", re.I)
DURATION_UNITS = frozenset("""week weeks day days month months year years hour hours
fortnight fortnights minute minutes min mins""".split())
TWO_TO = re.compile(r"\b(?:going|go|goes|went|off|back|fly|flying|drive|driving|walk|walking|"
                    r"head|heading|move|moving|travel|travelling|coming|come|be|been)\s+2\b"
                    r"(?!\s*(?:%s)\b)" % "|".join(sorted(DURATION_UNITS)), re.I)
TWO_PLACE = re.compile(r"\b2\s+(?=(?:the|a|an|my|our|his|her|their|its|work|bed|school|town|"
                       r"uni|university|college|church|hospital|town)\b)", re.I)
TWO_VERB = re.compile(r"\b2\s+(?=(?:go|get|come|see|do|be|make|take|put|give|tell|say|try|book|buy|"
                      r"ask|call|send|pay|sort|check|fix|start|stop|leave|stay|eat|drink|sleep|run|"
                      r"walk|drive|catch|meet|pick|order|cook|clean|wash|pack|post|ring|text|email|"
                      r"look|find|keep|learn|help|join|move|remember|finish|read|get)\b)", re.I)

SPEAK = {"im": "i'm", "ive": "i've", "i'd": "i'd", "id": "i'd", "ill": "i'll",
         "dont": "don't", "didnt": "didn't", "doesnt": "doesn't", "cant": "can't", "wont": "won't", "isnt": "isn't",
         "wasnt": "wasn't", "werent": "weren't", "arent": "aren't", "havent": "haven't",
         "hasnt": "hasn't", "couldnt": "couldn't", "wouldnt": "wouldn't", "shouldnt": "shouldn't",
         "thats": "that's", "its": "it's", "youre": "you're", "weve": "we've", "theres": "there's",
         "hes": "he's", "shes": "she's", "theyre": "they're", "youve": "you've"}
ITS_OWNS_AFTER = frozenset("""
    on in at to from of for with by into onto near under over behind inside outside off about
    got gets gotten get had has have having sold sell sells bought buy buys changed change changes
    lost lose loses moved move moves took take takes taken gave give gives made make makes used
    use uses keeps keep kept needs need needed left leaves
    replaced replaced fitted fixed cleaned painted washed dropped scratched licked wore worn cut put
    set parked serviced insured registered broke eaten bit hit
    """.split())


SHORT = {"yrs": "years", "yr": "year", "mth": "month", "mths": "months", "wk": "week",
         "wks": "weeks", "u": "you", "ur": "your", "r": "are", "n": "and",
         "tho": "though", "coz": "because", "cuz": "because", "b4": "before",
         "abt": "about", "tmrw": "tomorrow", "2moro": "tomorrow", "nite": "night",
         "pls": "please", "thx": "thanks", "luv": "love", "ya": "you", "yer": "your",
         "goin": "going", "doin": "doing", "havin": "having", "nuthin": "nothing",
         "somthing": "something", "w": "with", "2": "two",
         "gonna": "going to", "wanna": "want to"}
YES_AFTER = frozenset("""i im ive id ill it its that thats the we they you he she my our
    no yes dont didnt doesnt cant could is was there here what how why when where who ok okay
    just so but and can do does did nah yep yeah.""".split())
CLAUSES = 2
MOST = 90


def _repaired(clean, memory):
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if not isinstance(understood, dict):
        return clean
    if understood.get("clean") != clean.lower():
        return clean
    return understood.get("plain") or clean


CORRECTED_WITH_UNIT = (
    "{Value} {unit}, then.",
    "Got it \u2014 {value} {unit}.",
    "{Value} {unit}, got it.",
)

CORRECTED_ALONE = (
    "{Value}, then.",
    "Got it \u2014 {value}.",
    "{Value}, got it.",
)
VALUE_UNIT_WORDS = frozenset("""km k mile miles kilo kilos kg kgs g gram grams stone stones lb
    lbs foot feet ft inch inches cm m metre metres meter meters yard yards
    liter litre liters litres ml pint pints hour hours
    hr hrs minute minutes min mins day days week weeks wk month months year years time
    pound pounds quid dollar dollars euro euros
    morning evening night weekend cup cups spoon spoons egg eggs""".split())
VALUE_UNIT_GLUED = re.compile(r"^\d[\d,]*(?:\.\d+)?([a-z]{1,5})$", re.I)
A_MEASURE = {
    "km": "distance", "k": "distance", "mile": "distance", "miles": "distance",
    "m": "distance", "metre": "distance", "metres": "distance", "meter": "distance",
    "meters": "distance", "foot": "distance", "feet": "distance", "ft": "distance",
    "inch": "distance", "inches": "distance", "cm": "distance", "yard": "distance",
    "yards": "distance",
    "kilo": "weight", "kilos": "weight", "kg": "weight", "kgs": "weight", "g": "weight",
    "gram": "weight", "grams": "weight", "stone": "weight", "stones": "weight",
    "lb": "weight", "lbs": "weight", "pound": "money", "pounds": "money",
    "quid": "money", "dollar": "money", "dollars": "money", "euro": "money",
    "euros": "money",
    "hour": "time", "hours": "time", "hr": "time", "hrs": "time", "minute": "time",
    "minutes": "time", "min": "time", "mins": "time", "week": "time", "weeks": "time",
    "wk": "time", "month": "time", "months": "time", "year": "time", "years": "time",
    "day": "time", "days": "time", "morning": "time", "evening": "time",
    "night": "time", "weekend": "time", "time": "time", "times": "time", "per": "time",
    "a": "time", "an": "time", "every": "time",
    "litre": "volume", "litres": "volume", "liter": "volume", "liters": "volume",
    "ml": "volume", "pint": "volume", "pints": "volume", "cup": "volume",
    "cups": "volume", "spoon": "volume", "spoons": "volume",
    "egg": "count", "eggs": "count",
}


WHOLE_FREQUENCY = frozenset("""once twice thrice daily nightly weekly fortnightly monthly
    quarterly yearly annually hourly""".split())


def _the_values_measures(value):
    found = set()
    for word in str(value or "").split():
        if word.strip(".,!?;:'\u2019").lower() in WHOLE_FREQUENCY:
            found.add("time")
        word = word.strip(".,!?;:'\u2019").lower()
        glued = VALUE_UNIT_GLUED.match(word)
        if glued:
            word = glued.group(1).lower()
        if word in VALUE_UNIT_WORDS:
            found.add(A_MEASURE.get(word, word))
    return found


def _the_units_measure(unit):
    found = set()
    for word in str(unit or "").split():
        measure = A_MEASURE.get(word.strip(".,!?;:'\u2019").lower())
        if measure:
            found.add(measure)
    return found


def _the_unit_is_said_twice(value, unit):
    here = _the_values_measures(value)
    there = _the_units_measure(unit)
    if here and there:
        return bool(here & there)
    return False


PUT_RIGHT_LEAD = (
    ("i", "got", "it", "wrong"), ("got", "it", "wrong"), ("i", "made", "a", "mistake"),
    ("i", "was", "wrong"), ("my", "mistake"), ("silly", "me"), ("i", "mean"), ("i", "meant"),
    ("hang", "on"), ("hold", "on"), ("correction",), ("actually",), ("sorry",), ("wait",),
    ("nope",), ("nah",), ("no",), ("its",), ("it's"),

)
PUT_RIGHT_TAIL = (
    ("i", "got", "it", "wrong"), ("got", "it", "wrong"), ("i", "made", "a", "mistake"),
    ("i", "was", "wrong"), ("my", "mistake"), ("silly", "me"), ("i", "mean"), ("i", "think"),
    ("thanks",), ("sorry",), ("actually",), ("then",), ("right",), ("though",),
)


def _without_a_frame(words, phrases, back=False):
    words = list(words)
    took = False
    while words:
        for phrase in phrases:
            end = words[-len(phrase):] if back else words[:len(phrase)]
            said = tuple(word.lower().strip(".,!?;:'\u2019") for word in end)
            if said == phrase:
                words = words[:-len(phrase)] if back else words[len(phrase):]
                took = True
                break
        else:
            break
    return words, took


def _without_a_not(words):
    if len(words) >= 3 and words[-2].lower().strip(".,!?") == "not" \
            and re.search(r"\d", words[-1]):
        return words[:-2], True
    return list(words), False


def _the_bare_value(clean):
    words = [word for word in re.split(r"[\s,]+", (clean or "").strip(" .!?")) if word]
    if not words:
        return ""
    words, led = _without_a_frame(words, PUT_RIGHT_LEAD)
    words, _ = _without_a_not(words)
    words, tailed = _without_a_frame(words, PUT_RIGHT_TAIL, back=True)
    if not (led or tailed):
        return ""
    if not words or len(words) > 4:
        return ""
    return " ".join(words).strip(" .,!?")


def value_put_right(clean, memory):
    match = MAKE_A_VALUE.match(clean or "")
    bare = ""
    if not match:
        bare = _the_bare_value(clean or "")
        if not bare:
            return ""
    if not _the_line_before(memory):
        return ""
    value = " ".join((match.group("value") if match else bare).split()).strip(" .")
    if not value or len(value.split()) > 4:
        return ""
    words = [word.lower().strip(".,!?'\u2019") for word in value.split()]
    if bare:
        if not (re.search(r"\d", value)
                or all(word in VALUE_WORDS or word in WHOLE_FREQUENCY for word in words)):
            return ""
    elif not (re.search(r"\d", value) or all(word in VALUE_WORDS or word in DAYS
                                              or word in MONTHS or word in WHOLE_FREQUENCY
                                              for word in words)):
        return ""
    unit = _the_unit_before(memory)
    if not unit:
        return ""
    unit = _without_a_unit_already_in_the_value(value, unit)
    if _the_unit_is_said_twice(value, unit):
        return pick(CORRECTED_ALONE, memory, seed_text=clean).format(
            value=value, Value=value[:1].upper() + value[1:])
    return pick(CORRECTED_WITH_UNIT, memory, seed_text=clean).format(
        value=value, Value=value[:1].upper() + value[1:], unit=unit)


def _without_a_unit_already_in_the_value(value, unit):
    unit_words = str(unit or "").split()
    value_words = str(value or "").split()
    if len(unit_words) < 2 or not value_words:
        return unit
    last = value_words[-1].strip(".,!?;:'\u2019").lower()
    if last == unit_words[0].strip(".,!?;:'\u2019").lower():
        return " ".join(unit_words[1:])
    return unit


def _the_line_before(memory):
    if not isinstance(memory, dict):
        return ""
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns:
        return ""
    last = turns[-1]
    said = last.get("user") if isinstance(last, dict) else None
    return said if isinstance(said, str) else ""


def _the_unit_before(memory):
    said = _the_line_before(memory)
    if not said.strip():
        return ""
    words = [word.strip(".,!?;:") for word in said.split() if word.strip(".,!?;:")]
    for index, word in enumerate(words[:-1]):
        figure = word.lower()
        if figure in ("a", "an", "the"):
            continue
        if not (re.search(r"\d", figure) or figure in VALUE_WORDS or figure in DAYS
                or figure in MONTHS):
            continue
        tail = []
        for following in words[index + 1:index + 4]:
            if following.lower() in UNITS_AFTER and len(tail) < 3:
                tail.append(following.lower())
                continue
            break
        if tail:
            return " ".join(tail)
    return ""


GIVEN_AWAY = re.compile(
    r"\b(?:had|have|has|got)\s+to\s+give\b[^.!?]{0,30}?\b(?:away|up|back|to)\b|"
    r"\b(?:had|have|has|got)\s+to\s+(?:rehome|surrender|get rid of)\b|"
    r"\b(?:had|have|has|got)\s+to\s+let\b[^.!?]{0,20}?\b(?:go|away)\b|"
    r"\b(?:gave|given|giving)\b[^.!?]{0,30}?\b(?:away|up)\b|"
    r"\b(?:couldn'?t|could not|can'?t|cannot)\s+keep\b|"
    r"\bsurrendered\b|\bhanded (?:him|her|them|it) (?:over|back)\b", re.I)
GIVEN_ANIMAL = re.compile(
    r"\b(dogs?|puppy|pup|puppies|cats?|kitten|kittens|rabbits?|hamsters?|guinea pigs?|parrots?|"
    r"budgie|birds?|horses?|pony|snakes?|lizards?|rats?|ferrets?|tortoises?|pets?)\b", re.I)
NOT_THEIRS = re.compile(
    r"\b(?:my|his|her|their|our)\s+(?:mum|mom|mam|dad|father|mother|sister|brother|son|"
    r"daughter|nan|gran|granny|aunt|uncle|friend|mate|neighbou?r|colleague|boss|partner|wife|"
    r"husband|cousin)\b", re.I)
GIVEN_AWAY_REPLIES = (
    "That's a hard thing to do, and I doubt giving up a {animal} was an easy call.",
    "Giving up a {animal} is usually a last resort, so I doubt you came to it lightly.",
    "I'm sorry \u2014 giving up a {animal} is one of the harder decisions there is.",
    "That can't have been easy. You did right by the {animal}, whatever the reasons.",
)


def _the_animal_given_away(text, memory=None):
    found = GIVEN_ANIMAL.search(text)
    if found:
        kind = found.group(1).lower()
        return kind[:-1] if kind.endswith("s") and not kind.endswith("ss") else kind
    gone = memory.get("denial") if isinstance(memory, dict) else None
    records = gone.get("pets") if isinstance(gone, dict) else None
    said = text.lower()
    for record in records or []:
        if not isinstance(record, dict):
            continue
        name = str(record.get("name") or "").strip().lower()
        if name and re.search(r"\b" + re.escape(name) + r"\b", said):
            kind = str(record.get("animal") or "pet").lower()
            return kind[:-1] if kind.endswith("s") and not kind.endswith("ss") else kind
    return ""


def pet_given_away(text, memory=None):
    if not isinstance(text, str):
        return None
    clean = " ".join(text.split())
    if not clean or not GIVEN_AWAY.search(clean):
        return None
    if NOT_THEIRS.search(clean) and not re.match(r"\s*(?:i|we)\b", clean, re.I):
        return None
    kind = _the_animal_given_away(clean, memory)
    if not kind:
        return None
    return pick(GIVEN_AWAY_REPLIES, memory if isinstance(memory, dict) else {},
                seed_text=clean).format(animal=kind)


OFFERS_A_CHAT = re.compile(
    r"^\W*(?:ok|okay|so|well|hi|hey|and)?[,\s]*"
    r"(?:i\s+|we\s+)?(?:just|only|really|actually\s)?\s*"
    r"(?:wanted|want|fancied|feel like|felt like)\s+"
    r"(?:a\s+|to\s+|some\s+)?(?:chat|talk|natter|chinwag)\b"
    r"(?:\s+(?:really|honestly|today|tonight|for a bit|for a while|a bit|with someone|"
    r"to someone|to somebody|with somebody|i suppose|i guess|thats all|that'?s all|"
    r"more than anything|you know|i think|if thats ok|if that'?s ok))*"
    r"[\s.!?]*$"
    r"|^\W*(?:ok|okay|so|well)?[,\s]*(?:i\s+)?(?:just\s+)?(?:wanted|want|fancied)\s+"
    r"(?:someone|somebody)\s+to\s+(?:talk|chat)\s+(?:to|with)?"
    r"(?:\s+(?:really|honestly|today|tonight|a bit|i suppose|i guess))*[\s.!?]*$"
    r"|^\W*(?:i\s+)?thought\s+(?:i'?d|i would)\s+(?:say|pop)\s+(?:hi|hello|in)\b"
    r"(?:\s+(?:really|honestly|today|tonight|i suppose|before i go))*[\s.!?]*$",
    re.I)
CHAT_OFFER_REPLY = (
    "Anytime \u2014 what's on your mind?",
    "I'm here. Anything you want to talk about, big or small?",
    "Good, I've got time. What's been going on?",
    "Any time. What shall we talk about?",
    "Nice \u2014 I'm all yours. What's up?",
)


def _offers_a_chat(clean, memory=None):
    if not OFFERS_A_CHAT.match(clean or ""):
        return None
    for turn in (memory.get("turns") or [])[-3:] if isinstance(memory, dict) else []:
        said = str((turn or {}).get("user") or "").lower() if isinstance(turn, dict) else ""
        if said and (reads_as_bad_news(said) or loss.reads_as_loss(said)):
            return None
    return pick(CHAT_OFFER_REPLY, memory)


A_DATE_ALONE = re.compile(
    r"^(?:(?:ok|okay|so|and|well|oh|hmm|yeah|yes|no)\s*[,\s]\s*)*"
    r"(?:(?:it'?s|its|it is|that'?s|thats|that is|we'?re|we are|the date is|the day is)"
    r"\s+)?(?:in|on|for|by|at the end of|early|late)?\s*"
    r"(?P<when>january|february|march|april|may|june|july|august|september|october|november"
    r"|december|next\s+week|next\s+month|next\s+year|this\s+weekend|the\s+weekend"
    r"|tomorrow|tonight|the\s+\d{1,2}(?:st|nd|rd|th)|\d{1,2}(?:st|nd|rd|th)"
    r"|monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
    r"\s*(?:i think|i reckon|i believe|this year|next year|at the latest|i'?m sure)?"
    r"\s*[.!]*$", re.I)
A_MONTH_ALONE = re.compile(
    r"^(?:january|february|march|april|may|june|july|august|september|october|november"
    r"|december|monday|tuesday|wednesday|thursday|friday|saturday|sunday)$", re.I)
A_WEEKDAY = re.compile(r"^(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)$", re.I)
A_DATE_ON_A_PLAN = (
    "{Thing} \u2014 plenty of time to sort the rest.",
    "{Thing}. That's something to look forward to.",
    "{Thing} \u2014 what's left to sort?",
    "{Thing}. Good to have the date down.",
)
A_DAY_ON_A_PLAN = (
    "{Thing} \u2014 that is soon, then.",
    "{Thing}. Not long now.",
    "{Thing} \u2014 that comes round quickly.",
)
A_WORRIED_ABOUT_IT = re.compile(
    r"\b(?:nervous|worried|worry|worrying|dreading|dread|scared|afraid|anxious|panic|hate|"
    r"stress(?:ed|ful)?|not looking forward|can'?t face)\b", re.I)
A_DATE_ON_A_HARD_PLAN = (
    "{Thing} \u2014 no wonder it is on your mind.",
    "{Thing}. The run-up is usually worse than the day itself.",
    "{Thing} \u2014 that is a lot to have coming.",
)
A_DAY_ON_A_HARD_PLAN = (
    "{Thing} \u2014 no wonder it is on your mind.",
    "{Thing}. The day itself is usually easier than the wait.",
)

A_MILESTONE = re.compile(r"\b(?:\d{1,3})(?:st|nd|rd|th)\b", re.I)


def _the_plan_a_date_belongs_to(text):
    said = " ".join(str(text or "").lower().split())
    if not said:
        return "", ""
    words = re.findall(r"[a-z']+", said)
    occasion = next((word for word in words if word in OCCASIONS), "")
    if occasion:
        return occasion, "occasion"
    if A_MILESTONE.search(said) and re.search(r"\b(?:my|our)\b", said):
        return "birthday", "occasion"
    diary = DIARY_THING.search(said)
    if diary:
        return diary.group(0).lower(), "diary"
    if (TRIP_VERB.search(said) and DESTINATION.search(said) and not OBLIGED.search(said)
            and not set(words) & PAST_PLAN):
        head = DESTINATION.search(said).group(1).lower()
        if head not in NOT_A_TRIP and head not in THING_BEFORE:
            return "holiday", "trip"
    return "", ""


def _a_date_on_the_thing_in_hand(clean, memory):
    said = " ".join(str(clean or "").lower().split())
    found = A_DATE_ALONE.match(said)
    if not found:
        return None
    record = topics.current(memory)
    text = " ".join(str((record or {}).get("text") or "").lower().split())
    if not text:
        return None
    when = " ".join(found.group("when").lower().split())
    if not when or when in re.findall(r"[a-z']+", text):
        return None
    plan, kind = _the_plan_a_date_belongs_to(text)
    if not plan:
        return None
    thing = when[:1].upper() + when[1:]
    said_so_far = " ".join(
        [text] + [str(turn.get("user") or "").lower()
                  for turn in (memory.get("turns") or [])[-4:] if isinstance(turn, dict)])
    worried = bool(A_WORRIED_ABOUT_IT.search(said_so_far))
    a_day = A_MONTH_ALONE.match(when)
    if kind == "diary":
        if A_WEEKDAY.match(when):
            made = "the " + plan + " on " + thing
        elif a_day:
            made = "the " + plan + " in " + thing
        else:
            made = "the " + plan + " " + thing
    elif a_day:
        article = "an " if thing[0].lower() in "aeiou" else "a "
        made = article + thing + " " + plan
    elif A_WEEKDAY.match(when) or when in ("tomorrow", "tonight"):
        made = "the " + plan + " " + thing.lower()
    else:
        made = "the " + plan + " " + thing.lower()
    made = made[:1].upper() + made[1:]
    if a_day:
        pool = A_DATE_ON_A_HARD_PLAN if worried else A_DATE_ON_A_PLAN
        return pick(pool, memory).format(Thing=made)
    pool = A_DAY_ON_A_HARD_PLAN if worried else A_DAY_ON_A_PLAN
    return pick(pool, memory).format(Thing=made)


def _after_the_hello(clean):
    match = GREETING.match(clean)
    if not match:
        return ""
    return clean[match.end():].lstrip(" ,.!-:;")


def reply(text, memory):
    if not isinstance(text, str):
        return None
    clean = " ".join(text.split())
    if not clean or "?" in clean:
        return None
    dated = _a_date_on_the_thing_in_hand(clean, memory)
    if dated:
        return dated
    from ..compose import fallback as compose_fallback
    if compose_fallback._the_morning_has_a_clock(clean.lower()):
        return None
    from ..compose.fallback_data import A_DISMISSAL
    if A_DISMISSAL.match(clean):
        return None
    reported = facts._reported_clause(clean)
    if reported and facts.extract(reported):
        clean = " ".join(reported.split())
        text = clean
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if isinstance(understood, dict) and understood.get("suggestion"):
        return None
    if isinstance(understood, dict) and understood.get("errand"):
        return None
    read = _repaired(clean, memory)
    if GREETING.search(clean):
        rest = _after_the_hello(clean)
        if not rest or not facts.about_themselves(rest):
            return None
        clean = text = rest
        read = _repaired(clean, memory)
    elif MEET_GREET.search(clean) or SELF_INTRO.search(clean):
        return None
    had = the_job_they_had(clean, memory)
    if had:
        return had
    alone = a_person_named_alone(clean, memory)
    if alone:
        return alone
    if WANTS_ANSWER.search(read) and not facts.RELATION_WHOS_AGE.search(read):
        return None
    if _a_result_is_on_the_table(clean):
        return None
    limit = _a_limit_on_the_plan(read, memory)
    if limit:
        return limit
    second = a_second_person(clean, memory)
    if second:
        return second
    corrected = value_put_right(clean, memory)
    if corrected:
        return corrected
    aged = the_old_one_aged(clean, memory)
    if aged:
        return aged
    if not _statement(memory):
        return None
    given = pet_given_away(clean, memory)
    if given:
        return given
    if trouble.reads_as_trouble(read) is not None:
        return None
    limit = a_limit_reply(text, memory)
    if limit is not None:
        return limit
    if _no_subject(clean, memory):
        return None
    if reads_as_bad_news(read.lower()) or _a_loss(text, memory, read):
        return None
    if _bad_news_just_before(read, memory):
        return pick(THE_STORY_GOES_ON, memory, read)
    if reads_like_a_symptom(read.lower()):
        return None
    if reads_as_good_news(read.lower()):
        return None
    if reads_as_settled(clean.lower()) and worry_on_the_table(memory):
        return None
    if DEATH_WORDS.search(read):
        return None
    if WOULD_HAVE_BEEN.search(read) or BODY.search(read) or BLEED.search(read):
        return None
    if A_FEELING.search(clean):
        return None
    if _said_to_the_bot(clean):
        return None
    if _a_bare_state(clean.lower()):
        return None
    if GOOD_MOOD.search(clean) and not has_news(clean):
        return None
    alone = nobody_around(clean.lower(), memory)
    if alone:
        return pick(alone, memory, clean)
    deadline = _a_deadline(clean, read, memory)
    if deadline:
        return deadline
    clock = _a_clock_time(clean, read, memory)
    if clock:
        return clock
    if _after_a_feeling(clean, memory):
        thing = _echo(clean)
        if thing:
            return pick(EXPLAIN_TAIL, memory, seed_text=clean).format(
                thing=thing, Thing=thing[:1].upper() + thing[1:])
    lasting = _the_length(clean, memory)
    if lasting:
        return lasting
    hours = _the_hours(clean, read, memory)
    if hours:
        return hours
    chat = _offers_a_chat(clean, memory)
    if chat:
        return chat
    job = _a_job_to_do(clean, memory)
    if job:
        return job
    found = _learned(text, memory)
    if found and _only_a_wish(found):
        wanted = "a " + _the_wished_animal(found, clean)
        return pick(WISH_FOR_AN_ANIMAL, memory, seed_text=clean).format(
            Thing=wanted[:1].upper() + wanted[1:], thing=wanted)
    if found:
        nobody = _who_the_figure_is(found, memory, clean.lower())
        if nobody:
            return nobody
    if found and set(found) <= {"age", "height"} and not _only_the_figure(clean):
        return None
    animal_wanted = _an_animal_wanted(clean)
    if animal_wanted and not _on_record(animal_wanted, memory):
        return _what_a_wanted_animal_needs(animal_wanted, clean, memory)
    coming = _the_animal_coming(found) if found else ""
    if coming:
        return pick(ANIMAL_COMING, memory, coming).format(animal=coming)
    planned = _an_animal_only_planned(found, clean, memory)
    if planned:
        said = planned if planned.split()[0] in ("a", "an") else (
            "an " + planned if planned[:1] in "aeiou" else "a " + planned)
        return pick(A_BREED_BEING_CHOSEN, memory, clean).format(
            animal=said, Animal=said[:1].upper() + said[1:])
    if found and (_an_animal_taken_back(found) or _an_animal_turned_down(found, memory)):
        animal = _the_taken_back_animal(found)
        if animal and not _on_record(animal, memory):
            if _an_animal_they_had_once(clean):
                return pick(ANIMAL_HAD_ONCE, memory, animal).format(
                    animal=animal, Animal=animal[:1].upper() + animal[1:])
            return pick(ANIMAL_TAKEN_BACK, memory, animal).format(
                animal=animal, Animal=animal[:1].upper() + animal[1:])
        return None
    remark = _a_remark_on_what_was_said(clean, memory)
    if remark:
        _a_hand_back(remark, memory)
        return remark
    another = _another_of_what_we_said(clean, memory)
    if another:
        return another
    more = _adds_one_more_allergen(text, memory)
    if not more and (memory or {}).get("understood", {}).get("routine"):
        habit = _plain(clean, memory)
        if habit:
            return habit
    said = None
    if not found or (not more and not _tells_it(clean, found)):
        said = _a_thing_they_have(clean, memory)
    if said:
        return _the_opening_instead(said, clean, memory) or said
    if not found or (not more and not _tells_it(clean, found)):
        plain = _plain(clean, memory)
        return _the_opening_instead(plain, clean, memory) or plain
    pets = found.get("pets") if isinstance(found, dict) else None
    ill = not A_CHILD_IN_THE_LINE.search(clean) and reads_for_a_pet(clean.lower())
    if (pets and not more and set(found) == {"pets"} and not AS_WELL.search(clean)
            and not A_CHILD_IN_THE_LINE.search(clean) and ill):
        return None
    if (pets and not more and set(found) == {"pets"} and not AS_WELL.search(clean)
            and not A_CHILD_IN_THE_LINE.search(clean)
            and not _nothing_added_but_the_pet(clean, pets)):
        return None
    if (pets and not more and set(found) == {"pets"} and not AS_WELL.search(clean)
            and not A_CHILD_IN_THE_LINE.search(clean)
            and not _a_pet_that_is_all_right(clean, pets)):
        said, many = _the_pets_said(pets, clean)
        if said:
            if _the_pets_are_coming(pets, memory):
                pool = PET_TAIL_COMING_MANY if many else PET_TAIL_COMING
            else:
                pool = PET_TAIL_MANY if many else PET_TAIL_ONE
            return pick(pool, memory, clean).format(
                thing=said, Thing=said[:1].upper() + said[1:])
    kids = _children_with_ages(text)
    if kids:
        thing = _children_said(kids)
    elif more and list(found.get("allergies") or []) == more:
        thing = "you're allergic to " + " and ".join(more) + " too"
    else:
        thing = _echo(clean, memory)
    if not thing:
        return None
    plan = _plan_tails(found, clean, memory)
    if plan:
        return _pick_ending(plan, memory,
                            thing=thing, Thing=thing[:1].upper() + thing[1:],
                            food=CONDITION_FOOD.get(str(found.get("condition") or "").lower(), "that"))
    frames = _frames(found, _heavy(memory), clean, memory)
    if frames is FRAMES:
        opened = opening.the_opening(thing, clean, memory)
        if opened:
            return opened
    return _pick_ending(frames, memory,
                        thing=thing, Thing=thing[:1].upper() + thing[1:],
                        food=CONDITION_FOOD.get(str(found.get("condition") or "").lower(), "that"))

REMARK_BACK = re.compile(
    r"^(?:it|its|it's|that|thats|that's|they|them|he|she|the|this|those|these|everything|nothing"
    r"|none|all)\b", re.I)
REMARK_EXPENSE = re.compile(
    r"\b(?:cost|costs|costing|expensive|pricey|a fortune|a bomb|not cheap|money pit|"
    r"over budget|over the budget|cost a lot|costs a lot|adds? up)\b", re.I)
REMARK_STILL_TO_COME = re.compile(
    r"\b(?:going\s+to|gonna|planning|plan\s+to|planning\s+to|thinking\s+of|want\s+to\s+"
    r"(?:go|buy|get|book|move|build|do)|hoping\s+to|about\s+to|next\s+"
    r"(?:week|month|year|summer|spring|autumn|winter|june|july|august|september|october|"
    r"november|december|january|february|march|april|may|weekend|christmas)|"
    r"in\s+(?:january|february|march|april|may|june|july|august|september|october|november|"
    r"december|the\s+summer|the\s+spring|the\s+autumn|the\s+winter)|"
    r"before\s+i\s|when\s+i\s+go|once\s+i)\b", re.I)
REMARK_ALREADY_PAID = re.compile(
    r"\b(?:was|were|cost|costs|costing|cost\s+me|has\s+been|had\s+been|paid|spent|bought|"
    r"redid|redecorated|renovated|built|installed|fitted|took|got|had|already|last\s+"
    r"(?:year|month|week|summer|winter|spring|autumn)|ago|in\s+the\s+end|all\s+in)\b",
    re.I)
REMARK_LONG = re.compile(
    r"\b(?:took|takes|taking|take)\s+(?:forever|ages|hours|all day|all week|all weekend|weeks|"
    r"months|for ever|forever and a day)\b|\bso long\b|\blonger than\b|\bdragged on\b", re.I)
REMARK_BETTER = re.compile(
    r"\b(?:better|easier|nicer|cheaper|faster|less stressful|more money|pays better|pays more|"
    r"worth it)\b", re.I)
REMARK_HARD = re.compile(
    r"\b(?:hard|harder|difficult|tough|stressful|exhausting|draining|knackering|hectic|"
    r"a nightmare|a slog|a struggle)\b", re.I)
REMARK_WORK = re.compile(
    r"\bneeds?\s+(?:a lot of|some|lots of|loads of)\s+work\b|\bneeds? work\b|"
    r"\bneeds? doing\b|\bmore than i thought\b|\bbigger than i thought\b", re.I)
REMARK_GONE = re.compile(
    r"\b(?:got them|got it|ate them|ate it|ruined|ruined it|killed them|all gone|"
    r"eaten them|stole it|stole them|knocked them|gone to the slugs)\b", re.I)
GROWING = re.compile(
    r"\b(?:tomato|tomatoes|potato|potatoes|plant|plants|planted|seed|seeds|seedling|seedlings|"
    r"lettuce|beans|peas|carrot|carrots|onion|onions|squash|courgette|courgettes|pumpkin|"
    r"strawberr\w+|raspberr\w+|blackberr\w+|herb|herbs|flower|flowers|bulbs?|garden|allotment|"
    r"veg|vegetables?|crop|crops|greenhouse|bed|beds)\b", re.I)

REMARK_REPLIES = {
    "expense": (
        "Not cheap, that.",
        "They never are.",
        "The bits nobody quotes for are always the ones that cost.",
        "Ouch. Do you think it was worth it?",
    ),
    "long": (
        "It always takes longer than the plan says it will.",
        "Longer than anyone warns you, every time.",
        "That is the way of it, and at least it is done.",
    ),
    "better": (
        "Good - that is the bit that matters.",
        "That is the bit that makes the difference.",
        "That sounds like the right move.",
    ),
    "hard": (
        "That is the thing nobody warns you about.",
        "It does take it out of you.",
        "It is - and it gets easier once the new bit is routine.",
        "Fair enough. What has been the hardest bit?",
    ),
    "work": (
        "Bigger job than it looked, then.",
        "That is how these go: the first quote is never the whole of it.",
        "Worth getting a second price before you say yes to it.",
    ),
    "gone": (
        "Ah, that is a shame.",
        "That is gutting.",
        "Netting is the only thing that stops it happening again.",
        "Will you put another lot in?",
    ),
}

REMARK_PRICE_AHEAD = (
    "Not cheap, that.",
    "They never are.",
    "What are they quoting for it? That is usually the bit worth moving.",
    "Worth pricing it a couple of ways round before you commit.",
)

REMARK_TWO_SIDED = re.compile(r"\b(?:but|though|although|however|except|apart from|other than"
                              r"|worse|less|harder|longer|slower)\b", re.I)
REMARK_JUDGES_THE_PRICE = re.compile(
    r"\b(?:expensiv\w*|pricey|pricier|dear|dearer|a\s+fortune|a\s+bomb|a\s+packet|not\s+cheap|"
    r"cheap\s+enough|money\s+pit|over\s+(?:the\s+)?budget|cost(?:s|ing)?\s+(?:me\s+)?a\s+lot|"
    r"cost\s+me|too\s+much|so\s+much|that\s+much|a\s+lot\s+of\s+money|loads|rip[-\s]*off|"
    r"overpriced|adds?\s+up|worth\s+it|not\s+worth|daylight\s+robbery|steep)\b", re.I)

REMARK_FIGURE = re.compile(
    r"(?:£|\$|€)\s*\d|\b\d{2,}\b|\b\d+\s*(?:quid|pounds?|euros?|dollars?|grand|k)\b", re.I)
REMARK_FIGURE_REPLIES = (
    "Then it comes down to what you get for it, and a second price usually moves the figure.",
    "That is the number to weigh up against what doing nothing would cost you.",
    "Worth checking that against one more quote before you commit to it.",
)

REMARK_KINDS = ((REMARK_EXPENSE, "expense"), (REMARK_LONG, "long"), (REMARK_BETTER, "better"),
                (REMARK_HARD, "hard"), (REMARK_WORK, "work"), (REMARK_GONE, "gone"))


def _the_opening_instead(said, clean, memory):
    if not said or not reads_as_a_receipt(said):
        return None
    thing = _echo(clean, memory)
    if not thing:
        return None
    return opening.the_opening(thing, clean, memory)


def _a_hand_back(reply, memory):
    if not isinstance(memory, dict):
        return
    said = " ".join(re.findall(r"[a-z0-9']+", str(reply or "").lower().replace("\u2019", "'")))
    if not said:
        return
    kept = memory.get("hand_backs")
    if not isinstance(kept, list):
        kept = []
        memory["hand_backs"] = kept
    kept.append(said)
    del kept[:-4]


def _a_remark_on_what_was_said(clean, memory):
    if not isinstance(memory, dict):
        return None
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns:
        return None
    body = clean.strip()
    if len(body.split()) > 9:
        return None
    if not REMARK_BACK.match(body) or "?" in body:
        return None
    if REMARK_TWO_SIDED.search(body):
        return None
    topic_text = str((memory.get("topic") or {}).get("text") or "") if isinstance(
        memory.get("topic"), dict) else ""
    for pattern, kind in REMARK_KINDS:
        if not pattern.search(body):
            continue
        if kind == "gone" and not GROWING.search(body + " " + topic_text):
            continue
        if kind == "expense" and not REMARK_JUDGES_THE_PRICE.search(body):
            if not REMARK_FIGURE.search(body):
                continue
            return pick(REMARK_FIGURE_REPLIES, memory, seed_text=body)
        options = REMARK_REPLIES[kind]
        if kind == "expense" and _a_price_still_to_come(body, topic_text):
            options = REMARK_PRICE_AHEAD
        if _asked_last(memory):
            options = tuple(one for one in options if not one.endswith("?")) or options
        return pick(options, memory, seed_text=body)
    return None


def _a_price_still_to_come(body, topic_text):
    said = " ".join(part for part in (body or "", topic_text or "") if part)
    if REMARK_STILL_TO_COME.search(said):
        return True
    return not REMARK_ALREADY_PAID.search(said)


def _a_result_is_on_the_table(clean):
    from ..compose import fallback
    return fallback.reads_as_a_result_line(clean)


_HOLE = re.compile(r"\{[^}]*\}")
_NOT_WORDS = re.compile(r"[^a-z0-9]+")


def _ending_of(frame):
    parts = _HOLE.split(frame)
    return " ".join(_NOT_WORDS.sub(" ", parts[1].lower()).split()) if len(parts) > 1 else ""


def _pick_ending(frames, memory, **fields):
    turns = memory.get("turns") or []
    last = ""
    if turns and isinstance(turns[-1], dict):
        last = " ".join(_NOT_WORDS.sub(" ", str(turns[-1].get("bot") or "").lower()).split())
    fresh = [frame for frame in frames if not (_ending_of(frame) and _ending_of(frame) in last)]
    return pick(fresh or list(frames), memory).format(**fields)


PERSON_WORDS = frozenset(facts.RELATIONS) | frozenset((
    "kids", "children", "child", "baby", "toddler", "twins", "them", "they", "he", "she",
    "him", "her", "us", "we", "both"))


A_REASON_MARKER = re.compile(
    r"^(?:(?:and|but|well|so|see)\s+)?(?:because|cos|coz|cause|cuz)\b(?:\s+of\b)?[\s,:]*", re.I)
NO_REASON = re.compile(
    r"^(?:(?:i\s+)?(?:dont|do not|dunno|havent a clue|no idea|not sure)\b"
    r"(?:\s+(?:really\s+)?(?:know\b\s*)?(?:why)?)?|no reason|not a clue)\s*[.!]*$", re.I)
A_CLAUSE_OF_ITS_OWN = re.compile(
    r"\b(?:is|are|was|were|isnt|arent|wasnt|werent|gets?|got|makes?|made|keeps?|kept|feels?|felt"
    r"|never|always|doesnt|dont|didnt|wont|cant|couldnt|has|have|had|am|been|being|takes?|took"
    r"|wears?|wore|drives?|drove|works?|worked|goes|went|gives?|gave)\b", re.I)
AN_AGE_ALONE = re.compile(
    r"^(?:i'?m|im|i am|ive|i've|i just turned|i turned)\s+(\d{1,3})"
    r"(?:\s*(?:years?|yrs?)(?:\s+old)?)?(?:\s+(?:now|this year))?\s*[.!]?$", re.I)


def _after_a_feeling(clean, memory):
    if AN_AGE_ALONE.match(str(clean or "").strip()):
        return False
    if not isinstance(memory, dict):
        return False
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns:
        return False
    index = len(turns) - 1
    last = turns[index]
    said = last.get("user") if isinstance(last, dict) else None
    if not isinstance(said, str) or not said.strip():
        return False
    if NO_REASON.match(said.strip()) and A_CLAUSE_OF_ITS_OWN.search(str(clean or "")):
        index -= 1
        if index < 0:
            return False
        back = turns[index]
        said = back.get("user") if isinstance(back, dict) else None
        if not isinstance(said, str) or not said.strip():
            return False
    read = understanding(said)
    if read.get("emotion") == "confused":
        return False
    if AN_AIM.search(said):
        now = understanding(clean)
        if not (now.get("intent") == "feeling" and (now.get("polarity") or 0) < 0) \
                and not A_FEELING_ABOUT_IT.search(clean):
            return False
    if read.get("intent") != "feeling" or (read.get("polarity") or 0) > 0:
        if not _a_heavy_reply_just_before(memory, index):
            return False
    words = clean.split()
    if not words or len(words) > 12:
        return False
    first = words[0].lower().strip(",;:!")
    if first in ("i", "im", "i'm", "ive", "i've", "we", "we're", "were"):
        return True
    return bool(PERSON_WORDS & {word.lower().strip(",;:!") for word in words})


def _a_heavy_reply_just_before(memory, index):
    if not isinstance(memory, dict):
        return False
    note = memory.get("heavy_reply")
    if not isinstance(note, dict):
        return False
    return note.get("turn") == index


THE_STORY_GOES_ON = (
    "I'm listening \u2014 say more if it helps.",
    "Go on. I'm here.",
    "That sounds like a lot to be in the middle of. Tell me the rest.",
    "I'm with you. Keep going if you want to.",
)
THIRD_PERSON = re.compile(r"^(?:he|she|they|him|her|his|their|them|hes|shes|theyre|theyd|"
                          r"theyll|she'd|he'd|she'll|he'll)\b", re.I)


def _bad_news_just_before(clean, memory):
    if not THIRD_PERSON.match(_strip_lead_in(clean)):
        return False
    for turn in (memory.get("turns") or [])[-2:]:
        if not isinstance(turn, dict):
            continue
        said = str(turn.get("user") or "").lower()
        if reads_as_bad_news(said) or loss.reads_as_loss(said):
            return True
    return False


def carries_the_story_on(text, memory):
    if not isinstance(text, str) or "?" in text:
        return False
    clean = " ".join(text.split())
    if not clean:
        return False
    return _bad_news_just_before(clean, memory)


LENGTH_TAIL = (
    "{length} of it \u2014 has anything changed in that time?",
    "{length} of it. How are you finding it now?",
    "{length} of it already. Is it going the way you want it to?",
    "{length} of it \u2014 and has anything you have tried made a difference?",
)

SINCE_TAIL = (
    "Since {when} \u2014 has anything changed in that time?",
    "Since {when}. How are you finding it now?",
    "Since {when}. Is it going the way you want it to?",
    "Since {when} \u2014 and has anything you have tried made a difference?",
)

LENGTH_KEEPS = frozenset(("nearly", "almost", "over", "going on"))


THE_OLD_ONE = re.compile(
    r"^\W*(?:the|my|our)\s+(?:old|current|existing|present)?\s*one"
    r"(?:\s+(?:i|we)\s+(?:have|'ve|ve|got|use|used))?"
    r"\s+(?:is|was|'s|s)\s+(?P<n>\d{1,2}|[a-z]{3,9})\s*(?:years?|yrs?)(?:\s+old)?\W*$", re.I)
REPLACING = re.compile(
    r"\b(?:new|getting|get|got|bought|buy|buying|replace|replacing|upgrade|upgrading|"
    r"order|ordering|shopping for|looking at|need a|needs a|want a|after a)\b", re.I)
OLD_ONE_TAIL = (
    "{n} years on the old one \u2014 it has done its share. What are you after this time?",
    "{n} years is a good run out of one, so you are not replacing it early.",
    "{n} years \u2014 that is a fair innings, and it has earned the swap.",
)


def the_old_one_aged(clean, memory):
    if not isinstance(clean, str):
        return None
    found = THE_OLD_ONE.match(clean)
    if not found or len(clean.split()) > 9:
        return None
    said_age = found.group("n").lower()
    if said_age.isdigit():
        age = int(said_age)
    else:
        spoken = facts.WORD_NUMBERS.get(said_age)
        if not isinstance(spoken, int):
            return None
        age = spoken
    if not 5 <= age <= 40:
        return None
    turns = memory.get("turns") if isinstance(memory, dict) else None
    said = [str(turn.get("user") or "") for turn in (turns or []) if isinstance(turn, dict)]
    if not said or not REPLACING.search(said[-1]):
        return None
    if A_FEELING.search(clean) or DEATH_WORDS.search(clean) or BLEED.search(clean):
        return None
    return pick(OLD_ONE_TAIL, memory, seed_text=clean).format(n=age)


def _the_length(clean, memory):
    if not narrow.only_a_length(clean):
        return None
    from . import tried

    if not tried.after_an_answer(memory):
        return None
    if reads_like_a_symptom(clean.lower()) or reads_as_bad_news(clean.lower()):
        return None
    if A_FEELING.search(clean) or DEATH_WORDS.search(clean):
        return None
    found = narrow.A_LENGTH.search(clean)
    lead = found.group("lead").lower()
    amount = found.group("amount")
    unit = found.group("unit").lower()
    if lead == "since":
        when = unit[0].upper() + unit[1:] if unit in narrow.LENGTH_NAMED_DAYS else unit
        return pick(SINCE_TAIL, memory, seed_text=clean).format(when=when)
    length = "%s %s" % (amount, unit) if amount else unit
    if lead in LENGTH_KEEPS:
        length = "%s %s" % (lead, length)
    return pick(LENGTH_TAIL, memory, seed_text=clean).format(
        length=length[0].upper() + length[1:])


def _the_hours(clean, read, memory):
    if "?" in clean or WANTS_ANSWER.search(read):
        return None
    if NOT_THE_HOURS.search(read):
        return None
    if DEATH_WORDS.search(read) or A_FEELING.search(clean) or BLEED.search(read):
        return None
    if reads_like_a_symptom(read.lower()) or reads_as_bad_news(read.lower()):
        return None
    turns = [one for one in (memory.get("turns") or []) if isinstance(one, dict)]
    recent = " ".join(str(one.get("user") or "") for one in turns[-3:])
    if recent and DEATH_WORDS.search(recent):
        return None
    last_ask = str(turns[-1].get("user") or "") if turns else ""
    if turns and turns[-1].get("module") == "answers" and reads_as_an_ask(last_ask):
        return None
    family, pool = _hours_family(read)
    if pool is None:
        return None
    hours_after.note(memory, family)
    return pick(pool, memory, clean)

def _a_deadline(clean, read, memory):
    found = WHEN_DETAIL.search(clean)
    if not found:
        return None
    if len(clean.split()) > 7:
        return None
    turns = [one for one in (memory.get("turns") or []) if isinstance(one, dict)]
    if not turns:
        return None
    last = turns[-1]
    said = str(last.get("bot") or "")
    if last.get("module") != "answers" or len(said.split()) < 18:
        return None
    if not _tells_them_what_to_do(said):
        return None
    recent = said + " " + " ".join(str(one.get("user") or "") for one in turns[-3:])
    if DEATH_WORDS.search(recent) or BLEED.search(recent) or A_FEELING.search(clean):
        return None
    when = found.group("when").strip()
    pools = {"today": WHEN_TODAY_TAIL, "tomorrow": WHEN_TOMORROW_TAIL, "days": WHEN_DAYS_TAIL}
    pool = pools.get(_shape_of(when), WHEN_ROOMY_TAIL)
    return pick(pool, memory, clean).format(when=when, When=when[:1].upper() + when[1:])


def _an_hour_on_the_day(text):
    if not isinstance(text, str) or not text:
        return None
    if CLOCK_EVENT.search(text):
        return "nerves"
    if CLOCK_FLAT.search(text):
        return "flat"
    from . import when as clock

    return "nerves" if clock.EVENT_WORD.search(text) else None


THE_NOUN_IS_AT = re.compile(r"\bthe\s+(?P<noun>[a-z'-]+)\s+is\s+(?:at|for)\s+", re.I)
A_MARKED_HOUR = re.compile(
    r"\d{1,2}\s*(?:am|pm|a\.m\.|p\.m\.)|\d{1,2}[:.]\d{2}|o'?\s?clock|"
    r"\b(?:half|quarter)\b|\b" + TIME_WORD + r"\b", re.I)


def _the_figure_is_an_hour(when):
    head = re.match(r"\s*(\d{1,2})(?!\d)", when)
    if not head:
        return True
    return 1 <= int(head.group(1)) <= 24


def _a_clock_time(clean, read, memory):
    if len(clean.split()) > 8:
        return None
    found = CLOCK_DETAIL.search(clean) or CLOCK_AT.search(clean)
    if not found:
        return None
    from . import when as clock

    turns = [one for one in (memory.get("turns") or []) if isinstance(one, dict)]
    if not turns:
        return None
    last = turns[-1]
    said = str(last.get("bot") or "")
    module = last.get("module")
    theirs = " ".join(str(one.get("user") or "") for one in turns[-3:])
    if module == "greeting" and not len(said.split()) < 5:
        if not (_an_hour_on_the_day(said) or _an_hour_on_the_day(theirs)):
            return None
    elif module not in ("answers", "chat", "memory_store") or len(said.split()) < 5:
        return None
    kind = _an_hour_on_the_day(theirs)
    if not kind:
        return None
    recent = said + " " + theirs
    if DEATH_WORDS.search(theirs) or BLEED.search(clean) or A_FEELING.search(clean):
        return None
    when = found.group("when").strip()
    if not _the_figure_is_an_hour(when):
        return None
    named = THE_NOUN_IS_AT.search(clean)
    if named and not A_MARKED_HOUR.search(when) and not _an_hour_on_the_day(named.group("noun")):
        return None
    at = "At " + when
    if kind == "flat":
        pool = CLOCK_FLAT_TAIL
    else:
        pool = CLOCK_AFTER_TAIL if _clock_shape(when) == "after" else CLOCK_MORNING_TAIL
    return pick(pool, memory, clean).format(At=at[:1].upper() + at[1:], When=when[:1].upper()
                                            + when[1:], when=when)


def _hours_family(read):
    if ON_NIGHTS.search(read):
        return "nights", NIGHT_TAIL
    if SHIFT_LATE.search(read):
        return "late", LATE_TAIL
    if SHIFT_EARLY.search(read):
        return "early", EARLY_TAIL
    if EARLY_RISE.search(read):
        return "early", EARLY_TAIL
    if LATE_FINISH.search(read):
        return "late", LATE_TAIL
    if LONG_SHIFT.search(read):
        return "long", LONG_TAIL
    if SHIFTS_ALL_OVER.search(read):
        return "spread", SPREAD_TAIL
    if WORK_FROM_HOME.search(read):
        return "home", HOME_TAIL
    return None, None


AS_WELL = re.compile(r"\b(?:as\s+well|too|also|another)\b", re.I)
A_CHILD_IN_THE_LINE = re.compile(
    r"\b(?:kid|kids|child|children|son|sons|daughter|daughters|baby|babies|toddler)\b", re.I)
PET_ADDED = re.compile(
    r"\A\s*,?\s*(?:"
    r"(?:(?:is|are|was|were)\s+)?(?:called|named)\b[\w' ]*"
    r"|(?:is|are|was|were)\s+(?:\d\w*|one|two|three|four|five|six|seven|eight|nine|ten"
    r"|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty"
    r"|thirty|forty|fifty)\b(?:\s*(?:years?|months?|weeks?|days?)\s*old|\s+old)?\s*\Z"
    r"|(?:is|are)\s+(?:a|an|another)\s+[\w' ]{1,20}\Z"
    r"|,\s*\w[\w' ]*"
    r"|(?:and|with|plus|,)\s+(?:a|an|another|one|\d+)?\s*[\w' ]{1,24}\Z"
    r"|\Z"
    r")", re.I)


PET_ALL_RIGHT = re.compile(
    r"\b(?:is|are|was|were|'s)\s+(?:(?:doing|feeling)\s+)?(?:fine|ok|okay|better|well|healthy|"
    r"alright|all\s+right|great)\b", re.I)


def _a_pet_that_is_all_right(clean, kept):
    text = str(clean or "")
    for pet in kept or []:
        if not isinstance(pet, dict):
            continue
        word = str(pet.get("breed") or pet.get("animal") or "").strip().lower()
        if not word:
            continue
        found = re.search(r"\b" + re.escape(word) + r"s?\b", text, re.I)
        if found and PET_ALL_RIGHT.search(text[found.end():]):
            return True
    return False


INTRODUCED_BEFORE = re.compile(
    r"\b(?:named|called)\s+(?:the|my|our|a|an|his|her|their|its)?\s*\Z", re.I)
A_NAME_AFTER = re.compile(r"\s*,?\s*[a-z][\w'-]*[.!]?\Z", re.I)


def _nothing_added_but_the_pet(clean, kept):
    text = str(clean or "")
    for pet in kept or []:
        if not isinstance(pet, dict):
            continue
        word = str(pet.get("breed") or pet.get("animal") or "").strip().lower()
        if not word:
            continue
        found = re.search(r"\b" + re.escape(word) + r"s?\b", text, re.I)
        if not found:
            continue
        if PET_ALL_RIGHT.search(text[found.end():]):
            continue
        if (INTRODUCED_BEFORE.search(text[:found.start()])
                and A_NAME_AFTER.match(text[found.end():])):
            continue
        if not PET_ADDED.match(text[found.end():]):
            return False
    return True


A_VAGUE_MANY = re.compile(r"\b(?:lots|loads|plenty|several|many|a\s+few|some)\b\s*(?:of\s+)?",
                          re.I)


ANIMAL_TAKEN_BACK = (
    "No {animal}, then.",
    "Fair enough \u2014 no {animal}.",
    "Right \u2014 no {animal}.",
)


A_WANTED_ANIMAL = re.compile(
    r"\b(?:want|wants|wanted|wanting|would\s+like|'d\s+like|would\s+love|fancy|"
    r"fancied|i'?d\s+love|id\s+love|after|asked\s+for|"
    r"asking\s+for|been\s+asking|begging\s+for|dream(?:s|ing)?\s+of|keen\s+on|"
    r"desperate\s+for|mad\s+(?:on|for)|hoping\s+(?:for|to\s+get)|"
    r"(?:thinking|thought|talking)\s+(?:of|about)\s+getting|going\s+to\s+get)\b", re.I)
A_WANT_TURNED_DOWN = re.compile(
    r"\b(?:don'?t|dont|doesn'?t|doesnt|didn'?t|didnt|won'?t|wont|not|never|no\s+longer)\b"
    r"[^.!?;]{0,16}\b(?:want|wants|wanted|like|keen|after|ask(?:ed|ing))\b", re.I)
A_HAD_AN_ANIMAL = re.compile(
    r"\b(?:had|used\s+to\s+have|use\s+to\s+have|grew\s+up\s+with)\b", re.I)


ANIMAL_HAD_ONCE = (
    "A {animal} growing up, then \u2014 would you have another?",
    "You had a {animal} before. Do you think you would again?",
    "A {animal} when you were younger, then. What do you miss about it?",
)

A_PET_WANTED = (
    "Which animal are they after \u2014 a dog, a cat, something small?",
    "What have they got in mind? A pet is a long commitment and the answer changes with the animal.",
)

A_WANTED_ANIMAL_TAIL = (
    "A {animal}, then \u2014 what is putting you off getting one?",
    "So you are thinking about a {animal}. Who would look after it in the day?",
    "A {animal} is a long commitment. How soon were you thinking?",
)


def _a_wanted_animal(clean):
    low = str(clean or "")
    if A_WANT_TURNED_DOWN.search(low):
        return False
    return bool(A_WANTED_ANIMAL.search(low))


def _an_animal_wanted(clean):
    low = str(clean or "")
    if not _a_wanted_animal(low):
        return ""
    for match in facts.PETS.finditer(low):
        return match.group(1).lower()
    if PET_WORD.search(low):
        return "pet"
    return ""


def _an_animal_they_had_once(clean):
    low = str(clean or "")
    if _a_wanted_animal(low):
        return False
    return bool(A_HAD_AN_ANIMAL.search(low))


PET_WORD = re.compile(r"\b(?:pet|pets)\b", re.I)


def _what_a_wanted_animal_needs(animal, clean, memory):
    reading = {}
    try:
        from ..knowledge import lookup
        reading = understanding("what do i need for a " + animal)
        found = lookup.find(reading)
    except Exception:
        found = None
    if found is not None:
        reply = getattr(found, "reply", None)
        try:
            reply = reply(memory, reading) if callable(reply) else reply
        except Exception:
            reply = ""
        if isinstance(reply, str) and reply.strip():
            return reply.strip()
    if animal == "pet":
        return pick(A_PET_WANTED, memory, seed_text=clean)
    return pick(A_WANTED_ANIMAL_TAIL, memory, seed_text=clean).format(
        animal=animal, Animal=animal[:1].upper() + animal[1:])


ANIMAL_COMING = (
    "A {animal} on the way, then \u2014 is everything ready for it?",
    "A {animal} coming home. Have you picked a name yet?",
    "A {animal} to look forward to.",
)


PET_TAIL_COMING = (
    "{Thing} \u2014 when does it arrive?",
    "{Thing}. Not long now.",
    "{Thing} \u2014 the waiting is the worst part.",
)
PET_TAIL_COMING_MANY = (
    "{Thing} \u2014 when do they arrive?",
    "{Thing}. Two at once, that's a houseful.",
    "{Thing}. Not long now.",
)


def _the_pets_are_coming(pets, memory):
    coming = set()
    for pet in ((memory or {}).get("user") or {}).get("pets") or []:
        if isinstance(pet, dict) and pet.get("coming"):
            kind = facts.ANIMAL_KINDS.get(str(pet.get("animal") or "").strip().lower(), "")
            if kind:
                coming.add(kind)
    if not coming:
        return False
    for pet in pets or []:
        if not isinstance(pet, dict):
            continue
        if pet.get("name") or (pet.get("count") or 0) > 1 or not pet.get("breed"):
            continue
        kind = facts.ANIMAL_KINDS.get(str(pet.get("animal") or "").strip().lower(), "")
        if kind in coming:
            return True
    return False


def _the_animal_coming(found):
    for pet in (found or {}).get("pets") or []:
        if isinstance(pet, dict) and pet.get("coming"):
            animal = str(pet.get("animal") or "").strip().lower()
            if animal:
                return animal
    return ""



def _the_taken_back_animal(found):
    for pet in (found or {}).get("pets") or []:
        if isinstance(pet, dict) and pet.get("not_theirs"):
            animal = str(pet.get("animal") or "").strip().lower()
            if animal:
                return animal
    return ""


def _an_animal_turned_down(found, memory):
    if not isinstance(found, dict):
        return False
    pets = [pet for pet in (found.get("pets") or []) if isinstance(pet, dict)]
    if not pets or not all(pet.get("not_theirs") for pet in pets):
        return False
    if set(found) - {"pets", "tastes"}:
        return False
    animal = _the_taken_back_animal(found)
    if not animal or _on_record(animal, memory):
        return False
    named = {str(pet.get(field) or "").strip().lower()
             for pet in pets for field in ("animal", "breed")}
    named.discard("")
    tastes = [taste for taste in (found.get("tastes") or []) if isinstance(taste, dict)]
    return bool(tastes) and all(str(taste.get("thing") or "").strip().lower() in named
                                for taste in tastes)


def _on_record(animal, memory):
    user = (memory or {}).get("user") if isinstance(memory, dict) else None
    pets = (user or {}).get("pets") if isinstance(user, dict) else None
    for pet in pets or []:
        if isinstance(pet, dict) and str(pet.get("animal") or "").strip().lower() == animal:
            return True
    return False


WISH_FOR_AN_ANIMAL = (
    "{Thing}? Where are you up to with it?",
    "{Thing} - what's drawing you to one?",
    "{Thing}. What would you have to sort out first?",
)
A_BREED_BEING_CHOSEN = (
    "{Animal} \u2014 are you settled on that one?",
    "{Animal}, then. What made you pick that one?",
    "{Animal} \u2014 have you met one before?",
)


def _an_animal_only_planned(found, clean, memory):
    pets = [pet for pet in ((found or {}).get("pets") or []) if isinstance(pet, dict)]
    if len(pets) != 1:
        return ""
    pet = pets[0]
    if pet.get("wanted") or pet.get("coming") or pet.get("not_theirs"):
        return ""
    if not topics.NAMES_THE_THING.match(" ".join(str(clean or "").lower().split())):
        return ""
    record = memory.get("topic") if isinstance(memory, dict) else None
    plan = str(record.get("text") or "") if isinstance(record, dict) else ""
    if not plan or plan.strip().lower() == str(clean or "").strip().lower():
        return ""
    if not topics.A_THING_ON_ITS_WAY.search(plan):
        return ""
    return str(pet.get("breed") or pet.get("animal") or "").strip().lower()


def _the_wished_animal(found, clean=""):
    for pet in (found or {}).get("pets") or []:
        if isinstance(pet, dict) and pet.get("wanted"):
            said = str(pet.get("breed") or pet.get("animal") or "").strip().lower()
            if said:
                return said
    words = [word for word in str(clean or "").split() if word.isalpha()]
    return words[-1] if words else "one"


def _only_a_wish(found):
    if not isinstance(found, dict) or set(found) - {"pets"}:
        return False
    pets = [pet for pet in (found.get("pets") or []) if isinstance(pet, dict)]
    return bool(pets) and all(pet.get("wanted") for pet in pets)


def _an_animal_taken_back(found):
    if not isinstance(found, dict) or set(found) - {"pets"}:
        return False
    pets = [pet for pet in (found.get("pets") or []) if isinstance(pet, dict)]
    if any(pet.get("wanted") for pet in pets):
        return False
    return bool(pets) and all(pet.get("not_theirs") for pet in pets)


def _the_pets_said(kept, clean=""):
    number = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven",
              8: "eight", 9: "nine", 10: "ten"}
    groups = []
    for pet in kept or []:
        if not isinstance(pet, dict):
            continue
        try:
            count = int(pet.get("count") or 1)
        except (TypeError, ValueError):
            count = 1
        breed_word = "" if pet.get("breed_of_one") else str(pet.get("breed") or "")
        animal = str(breed_word or pet.get("animal") or "").strip().lower()
        if not animal:
            continue
        for group in groups:
            if group[0] == animal:
                group[1] += count
                break
        else:
            groups.append([animal, count])
    if not groups:
        return "", False
    if len(groups) == 1 and groups[0][1] == 1 and A_VAGUE_MANY.search(str(clean or "")):
        return "", False
    parts = []
    for animal, count in groups:
        if count == 1:
            parts.append(("an " if animal[:1] in "aeiou" else "a ") + animal)
        else:
            word = animal if animal.endswith("s") else animal + "s"
            parts.append(f"{number.get(count, str(count))} {word}")
    said = ", ".join(parts[:-1]) + " and " + parts[-1] if len(parts) > 1 else parts[0]
    names = [n[:1].upper() + n[1:]
             for n in (str(pet.get("name") or "").strip() for pet in kept
                       if isinstance(pet, dict)) if n]
    if len(names) == 1:
        said += f" called {names[0]}"
    elif names:
        said += ", " + ", ".join(names[:-1]) + f" and {names[-1]}"
    many = sum(count for _, count in groups) > 1
    return said, many


def _plain(clean, memory):
    body = _strip_lead_in(clean)
    if not body or trouble.reads_as_trouble(clean) is not None:
        return None
    if not _about_them(body):
        return None
    if not HABIT.search(body) and not GOING.search(body):
        return None
    if OBLIGED.search(body):
        return None
    if TROUBLE.search(body) or FEELING.search(body):
        return None
    thing = _echo(clean, memory)
    if not thing:
        return None
    if HABIT.search(body):
        options = HABIT_TAIL
    elif GOING.search(body) and not GOING_BAD.search(body):
        options = GOING_TAIL
    else:
        return None
    return pick(options, memory).format(thing=thing, Thing=thing[:1].upper() + thing[1:])


def _about_them(body):
    first = body.split()[0].lower().strip(",;:") if body.split() else ""
    return first in ("i", "i'm", "im", "i've", "ive", "i'd", "we", "we're", "were", "my", "our")


NOBODY_AROUND = re.compile(
    r"\bi\s+(?:don'?t|do not)\s+(?:really\s+|even\s+|actually\s+)?know\s+"
    r"(?:anyone|anybody|a soul|any ?one else|a single person|one person)\b"
    r"|\bi\s*'?ve\s+(?:got|gotten)\s+no\s*(?:one|body|friends|mates)\b"
    r"|\bi\s+have\s+no\s*(?:one|body|friends|mates)\b"
    r"|\bno ?(?:one|body)\s+to\s+(?:talk|chat|go out|spend|turn)\b",
    re.I)
NOBODY_AROUND_ASK = re.compile(r"\b(?:who|that)\s+(?:can|could|would|will|to)\b", re.I)
ANYBODY_AT_ALL = re.compile(
    r"\b(?:know|knows)\s+(?:lots|plenty|loads|a few|some|quite a few|lots of|plenty of)\b",
    re.I)
OTHER_PERSON = frozenset("""he she they his her their hes shes theyve him them him/her""".split())
GOING_HOME = re.compile(
    r"\b(?:should|might|will|hopefully|due|going|expected|allowed)\s+(?:to\s+)?(?:be\s+)?"
    r"(?:out|home|discharged|released)\b"
    r"|\b(?:out|home|discharged|released)\s+(?:of\s+(?:hospital|there)\s+)?"
    r"(?:next week|this week|tomorrow|soon|on (?:monday|tuesday|wednesday|thursday|friday|saturday"
    r"|sunday)|in a (?:few|couple of) days|by the weekend)\b"
    r"|\bcoming home\b|\bout of hospital\b", re.I)
ON_THE_MEND = re.compile(
    r"\b(?:doing|getting|feeling|looking)\s+(?:a lot |much |a bit |so much |a little )?better\b"
    r"|\bon the mend\b|\bon the up\b|\bturned (?:a|the) corner\b|\bout of (?:the )?danger\b"
    r"|\bpicking up\b|\bback to (?:her|his|their) old self\b|\bwell on the way\b", re.I)
BACK_AT_IT = re.compile(
    r"\bback (?:at work|to work|in work|at school|on (?:her|his|their) feet|to (?:normal|it|"
    r"herself|himself|themselves|training|the gym|uni|university))\b"
    r"|\bup and about\b|\bwalking (?:again|now)\b|\bwell enough to\b", re.I)
GOING_HOME_TAIL = (
    "Out {soon} \u2014 that is the news you want. The first days at home are usually the flat ones, "
    "so keep them quiet.",
    "That is a relief. Coming home is the milestone; the tiredness tends to last a few weeks past "
    "it.",
    "Good to hear. Home beats any ward for sleeping, even with the stairs in the way.",
)
ON_THE_MEND_TAIL = (
    "Good to hear it. Recovery goes in fits and starts \u2014 a good day, then a flat one, and both "
    "are normal.",
    "That is the direction you want. Better is slower than people expect, and it counts all the "
    "same.",
    "Worth saying out loud. On the mend is the part that takes patience from everyone round them.",
)
BACK_AT_IT_TAIL = (
    "Back at it already is quick going. The first week back is the tiring one for most people.",
    "That is a good sign. Getting back to normal takes longer than people expect, and the first "
    "week of it is the hardest.",
    "Good news. Back to it \u2014 and the first week is the one to take gently.",
)


GOING_HOME_MINE = (
    "Out {soon} \u2014 good. The first days at home are the flat ones, so keep them quiet and let "
    "people bring things.",
    "That is a relief to hear. Home is where the sleep happens; the ward is not.",
)
ON_THE_MEND_MINE = (
    "Good to hear. Recovery goes in fits and starts \u2014 a good day, then a flat one, and both are "
    "normal.",
    "That is the direction you want. Better is slower than people expect, and it counts all the "
    "same.",
    "Worth saying out loud. Take the good days as they come rather than testing them.",
)
BACK_AT_IT_MINE = (
    "Back at it already is quick going. The first week back is the tiring one for most people.",
    "Good sign. Getting back to normal takes longer than people expect, so keep the first week "
    "light.",
    "Good news. Back to it \u2014 and the first week is the one to take gently.",
)
A_RELATION = frozenset("""mum mom mother dad father nan nanna granny gran grandma grandad grandpa
    son daughter kid child baby sister brother mate friend partner wife husband aunt uncle cousin
    niece nephew colleague boss neighbour neighbor lodger flatmate housemate""".split())


def _who_is_getting_better(low):
    words = set(re.findall(r"[a-z']+", low))
    if words & (OTHER_PERSON | A_RELATION):
        return "them"
    if words & frozenset(("i", "im", "ive", "me", "my", "myself")):
        return "me"
    return ""


def a_person_getting_better(clean, memory=None):
    plain = str(clean or "").replace("\u2019", "'").replace("\u2018", "'")
    low = plain.lower()
    if not low.strip() or DEATH_WORDS.search(low):
        return None
    if not _who_is_getting_better(low):
        return None
    said = " ".join([low] + _the_words_of_the_last_two_turns(memory))
    if not re.search(r"\b(?:ill|sick|hospital|operation|op|surgery|broke|broken|stroke|chemo"
                     r"|treatment|injury|injured|fell|fall|accident|recovering|recovery|bug"
                     r"|flu|pneumonia|infection)\b", said):
        return None
    mine = _who_is_getting_better(low) == "me"
    for pattern, theirs, ours in ((GOING_HOME, GOING_HOME_TAIL, GOING_HOME_MINE),
                                  (ON_THE_MEND, ON_THE_MEND_TAIL, ON_THE_MEND_MINE),
                                  (BACK_AT_IT, BACK_AT_IT_TAIL, BACK_AT_IT_MINE)):
        match = pattern.search(low)
        if match and not negated(low, match.group(0)):
            return _with_the_time(ours if mine else theirs, low)
    return None


def _the_words_of_the_last_two_turns(memory):
    words = []
    for turn in (memory or {}).get("turns") or []:
        if isinstance(turn, dict):
            words.append(str(turn.get("user") or "").lower())
        elif isinstance(turn, str):
            words.append(turn.lower())
    return words[-2:]


def _with_the_time(pool, low):
    match = re.search(r"\b(next week|this week|tomorrow|soon|on (?:monday|tuesday|wednesday"
                      r"|thursday|friday|saturday|sunday)|in a (?:few|couple of) days"
                      r"|by the weekend)\b", low)
    when = match.group(1) if match else "soon"
    return tuple(line.replace("{soon}", when) for line in pool)

A_MOVE = re.compile(r"\b(?:moved|moving|move|relocat|emigrat|new (?:city|town|area|job|country))",
                    re.I)
ALONE_AFTER_A_MOVE = (
    "The first months somewhere new are the emptiest part of a move, and it does ease off. "
    "Whatever meets weekly near you - a class, a club, a five-a-side - fills it faster than "
    "waiting to be asked.",
    "That's the hard part of moving, and nobody warns you how long it lasts. One thing you turn "
    "up to at the same time every week is how the same faces start.",
    "Being new somewhere is lonely in a way that has nothing to do with how likeable you are. "
    "Say yes to the first small invitation that comes, even the boring one.",
)
ALONE_TAIL = (
    "That's a lonely way to spend the week, and it isn't a fault in you. One message to someone "
    "you already like does more than waiting for a night out.",
    "That's a quiet way to live. The people who get to know you are the ones you see at the same "
    "time each week, so it is worth having one of those.",
    "That's hard going. Being on your own in a place with no history to it wears thin, and the "
    "way out is nearly always the same small step: one regular thing, one person you keep saying "
    "hello to.",
)


ALONE_AFTER_A_LOSS = (
    "That's the hardest part of it, the empty week afterwards. The people who knew them are "
    "usually the ones who most want to hear from you.",
    "Being on your own after something like that is a weight of its own, and it is not something "
    "to push through. A short call to someone who knew them helps more than you'd think.",
)


def nobody_around(clean, memory):
    plain = str(clean or "").replace("\u2019", "'").replace("\u2018", "'")
    hit = NOBODY_AROUND.search(plain)
    if not hit or NOBODY_AROUND_ASK.search(plain) or ANYBODY_AT_ALL.search(plain):
        return None
    if set(plain[:hit.start()].split()) & OTHER_PERSON:
        return None
    if negated(plain, hit.group(0)[:12]):
        return None
    said = " ".join([plain] + [str(one or "") for one in (memory.get("turns") or [])[-2:]])
    if DEATH_WORDS.search(said):
        return ALONE_AFTER_A_LOSS
    return ALONE_AFTER_A_MOVE if A_MOVE.search(said) else ALONE_TAIL


_WORDS = re.compile(r"[a-z']+")


_THE_BOT_AS_SUBJECT = re.compile(
    r"^\s*(?:(?:oh|aw+|ah|ha+|tbh|honestly|ok|okay|well|and|but|so|yeah)[,\s]+)*"
    r"you(?:'?re| are| were| seem| look| sound| make| keep| always| really| definitely)\b",
    re.I)
_SOMEONE_ELSE_IN_IT = re.compile(r"\b(?:i|im|i'm|i've|ive|i'd|we|we're|our|my|mine)\b", re.I)


def _said_to_the_bot(clean):
    if not _THE_BOT_AS_SUBJECT.match(clean or ""):
        return False
    return not _SOMEONE_ELSE_IN_IT.search(clean or "")


def _no_subject(clean, memory=None):
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if isinstance(understood, dict) and understood.get("dropped_subject"):
        return True
    words = [word for word in _WORDS.findall(_repaired(clean, memory).lower()) if word]
    while words and words[0] in LEADERS:
        words = words[1:]
    return bool(words) and opens_without_subject(words, 0)


def _asked_last(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return False
    last = turns[-1] if isinstance(turns[-1], dict) else {}
    return str(last.get("bot") or "").strip().endswith("?")


def _a_diary_plan(found, clean):
    if not isinstance(found, dict) or not found.get("plan"):
        return None
    said = " ".join(str(clean or "").lower().split())
    if not said or not DATE_AHEAD.search(said):
        return None
    if set(re.findall(r"[a-z']+", said)) & PAST_PLAN:
        return None
    who = None
    named = re.search(r"\b(?:my|our)\s+([a-z]+)", said)
    if named:
        word = named.group(1)
        person = next((one for one in (word, re.sub(r"'s$", "", word), word[:-1])
                       if one in facts.RELATIONS), "")
        at_home = re.search(r"\b(?:coming|heading|getting|moving|flying) (?:back )?home\b", said)
        if person in facts.RELATIONS and COMING_TO_STAY.search(said) and not at_home:
            who = ("they" if _more_than_one_coming(said, named.end(), word) else
                   "she" if person in facts.SHE and person not in facts.HE else
                   "he" if person in facts.HE and person not in facts.SHE else "they")
    if who == "they":
        return VISIT_TAIL_MANY
    if who:
        return tuple(one.replace("{who}", who) for one in VISIT_TAIL_ONE)
    if DIARY_THING.search(said):
        return DIARY_TIME_TAIL if DIARY_TIME.search(said) else DIARY_TAIL
    if re.search(r"\b(?:meet|meeting|seeing)\b", said):
        return MEETING_TAIL if DIARY_TIME.search(said) else MEETING_TIME_TAIL
    if set(re.findall(r"[a-z']+", said)) & OCCASIONS:
        return OCCASION_TAIL
    return None


def _plan_tails(found, clean, memory):
    kind = reads_as_a_trip(clean)
    if kind == "trip":
        options = TRIP_TAIL
    elif kind == "occasion":
        options = OCCASION_TAIL
    elif kind == "occasion_flat":
        options = OCCASION_FLAT_TAIL
    else:
        options = _a_diary_plan(found, clean)
        if not options:
            return None
    if HOW_LONG_ALREADY.search(clean):
        options = tuple(one for one in options if "how long" not in one.lower()) or options
    if _asked_last(memory):
        options = tuple(one for one in options if not one.endswith("?")) or options
    return options


PLACED_IN_THE_PAST = re.compile(
    r"\b(?:last (?:year|summer|winter|spring|autumn|month|week|night)|years ago|months ago|"
    r"weeks ago|back in|when i was|used to)\b", re.I)


def _about_a_body(read, memory=None):
    try:
        read_it = understanding(read, memory if isinstance(memory, dict) else {})
    except Exception:
        return False
    return isinstance(read_it, dict) and read_it.get("topic") == "health"


JOB_TO_DO = re.compile(
    r"\bto\s+(?:sort|fix|clear|clean|paint|do|tidy|finish|replace|handle|deal\s+with|"
    r"get\s+(?:rid\s+of|done|sorted)|put\s+up|take\s+down|strip|sand|wire|plumb|service|"
    r"return|file|chase|book|renew|sell|pack|prepare|plan|write|organise|organize|arrange|"
    r"fill\s+(?:in|out)|sign|complete|send\s+(?:off|back)|post\s+off|"
    r"build|assemble|learn|study|wrap|draft|collate|make|iron|wash|mow|weed|dig|tile|grout|"
    r"seal|hang|fit|install|mount|mend|sew|hem|scrub|hoover|vacuum)\b", re.I)
JOB_HAS_A_DAY = re.compile(
    r"\b(?:today|tonight|tomorrow|tmrw|this\s+(?:week|weekend|month|evening)|next\s+week|"
    r"weekend|by\s+(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday|the\s+end)|"
    r"monday|tuesday|wednesday|thursday|friday|saturday|sunday|the\s+end\s+of\s+the\s+month)\b",
    re.I)
JOB_TAIL = (
    "{Thing} \u2014 is that the weekend, or are you fitting it in around work?",
    "{Thing}. Do you know where to start with it, or is that the hard part?",
    "{Thing} \u2014 what's the first thing that needs doing?",
    "{Thing}. Is it a bigger job than it looked?",
)


JOB_BEFORE = re.compile(r"\bbefore\s+(?:the|my|we|i|having|that)\b|\b(?:until|till|up to)\s+\d",
                        re.I)
PAST_JOB = (
    "{X} — that is a real thing to have behind you. What has changed since then?",
    "{X} is not nothing to have behind you. Whatever comes next, you are not starting from the "
    "bottom of anything.",
    "{X}, then. You know that work from the inside, which counts for more than it looks.",
)
PAST_JOB_PLAIN = (
    "{X} — that is not nothing to have behind you. Do you miss it, or are you glad to be out of "
    "it?",
    "{X} is a thing you already know how to do, which is more than most people start with.",
    "{X}, then. What is it that has you thinking about it now?",
)


def the_job_they_had(clean, memory):
    if not isinstance(clean, str) or "?" in clean:
        return None
    if not facts.JOB_WAS.search(clean):
        return None
    job = " ".join(str(facts.extract(clean).get("job") or "").split())
    if not job:
        return None
    if job.split()[0].lower() in facts.WAS_NOT_A_JOB:
        return None
    pool = PAST_JOB if JOB_BEFORE.search(clean) else PAST_JOB_PLAIN
    return pick(pool, memory, seed_text=clean).format(
        x=job, X=job[:1].upper() + job[1:])


def a_job_to_do(text, memory=None):
    try:
        return _a_job_to_do(text, memory)
    except Exception:
        return None


def _a_job_to_do(clean, memory=None):
    read = _spoken(_repairs(clean, memory)) or clean
    if not JOB_TO_DO.search(read):
        return None
    match = HAVE_THING.search(read)
    if not match:
        return None
    thing = match.group(1).lower().strip("-'")
    if not thing or thing in NOT_A_THING or thing.isdigit():
        return None
    if _about_a_body(read, memory) or PLACED_IN_THE_PAST.search(read):
        return None
    if HABIT.search(read):
        return None
    what = _echo(clean, memory)
    if not what:
        return None
    what = HAVE_A.sub(r"\1've got a", what)
    tails = JOB_TAIL[1:] if JOB_HAS_A_DAY.search(read) else JOB_TAIL
    return pick(tails, memory, seed_text=read).format(
        thing=what, Thing=what[:1].upper() + what[1:])


WHO_THE_FIGURE_IS = (
    "Who's {figure}?",
    "{Figure} \u2014 who's that?",
)
WHO_IS_IT = (
    "Who do you mean?",
    "Who's that, then?",
    "Who are we talking about?",
)
WHAT_OF_THEM = (
    "{Count} of what?",
    "{Count} of what, sorry?",
)
WHICH_ONES = (
    "Which ones do you mean?",
    "Which one do you mean?",
)
POINTS_BACK = re.compile(r"\b(?:them|those|these|ones|it)\b", re.I)
A_COUNT_OF_THEM = re.compile(
    r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|a few|a couple|\d{1,3})"
    r"\s+of\s+(?:them|those|these)\b", re.I)


A_DATE_STILL_TO_COME = re.compile(
    r"\b(?:turning|turns)\s+(?:\d{1,3}|[a-z]+)\b"
    r"|\b(?:next|this)\s+(?:week|month|year|weekend|summer|christmas|spring|autumn|winter)\b"
    r"|\b(?:in|by|until|till)\s+(?:the\s+)?(?:new\s+year|summer|christmas)\b", re.I)


def _the_chat_holds_something(memory):
    return there_is_a_chat(memory)


def _the_pronoun_points_at_somebody(low, memory):
    if _person_from_pronoun(low, memory):
        return True
    held = memory or {}
    theirs = held.get("user") if isinstance(held.get("user"), dict) else {}
    if any(isinstance(pet, dict) for pet in (theirs.get("pets") or [])):
        return True
    fits = None
    if re.search(r"\b(?:she|shes|she's|her)\b", low or "", re.I):
        fits = facts.SHE
    elif re.search(r"\b(?:he|hes|he's|his)\b", low or "", re.I):
        fits = facts.HE
    if fits:
        said = " ".join(str((turn or {}).get("user") or "").lower()
                        for turn in (held.get("turns") or [])[-4:])
        for word in sorted(PERSON_WORDS.union(CHILD), key=len, reverse=True):
            if not re.search(r"\b" + word + r"\b", said):
                continue
            if _pronoun_fits(word, fits):
                return True
    if not re.search(r"\b(?:they|theyre|they're|them|their|theirs|those|these)\b", low or "", re.I):
        return False
    words = set(re.findall(r"[a-z']+", low or ""))
    for turn in (held.get("turns") or [])[-4:]:
        words |= set(re.findall(r"[a-z']+", str((turn or {}).get("user") or "").lower()))
    for word in words:
        if word in PERSON_GROUP or word in CHILD:
            return True
    return any(str(entry.get("who") or "").strip() and not str(entry.get("who")).endswith("s")
               for entry in (held.get("others") or []) if isinstance(entry, dict))


def _somebody_was_being_hurt(memory):
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)] \
        if isinstance(memory, dict) else []
    if not turns:
        return False
    return reads_as_cruelty(str(turns[-1].get("user") or ""))


def _who_the_figure_is(found, memory, low):
    entries = found.get("others") if isinstance(found, dict) else None
    if not entries:
        return None
    if SOMEONE_MILESTONE.search(low or "") or A_DATE_STILL_TO_COME.search(low or ""):
        return None
    for entry in entries:
        if not isinstance(entry, dict) or entry.get("who"):
            continue
        figure = entry.get("age") or entry.get("height")
        if not figure:
            continue
        if entry.get("pronoun") and _the_pronoun_points_at_somebody(low, memory):
            return None
        if entry.get("pronoun") and _somebody_was_being_hurt(memory):
            pron = str(entry.get("pronoun") or "").strip().lower()
            said = ("%s's %s" % (pron, figure)) if isinstance(figure, int) else ""
            if said:
                return pick(HEAVY_FRAMES, memory, seed_text=low).format(
                    thing=said, Thing=said[:1].upper() + said[1:])
            return None
        if isinstance(figure, int) and figure:
            return pick(WHO_THE_FIGURE_IS, memory, seed_text=low).format(
                figure=str(figure), Figure=str(figure))
        return pick(WHO_IS_IT, memory, seed_text=low)
    return None


def _what_the_pointer_is(read, memory):
    if _the_chat_holds_something(memory):
        return None
    if not POINTS_BACK.search(read or ""):
        return None
    count = A_COUNT_OF_THEM.search(read or "")
    if count:
        counted = count.group(1)
        return pick(WHAT_OF_THEM, memory, seed_text=read).format(
            Count=counted[:1].upper() + counted[1:])
    return pick(WHICH_ONES, memory, seed_text=read)

A_WONDERED_CONDITION = re.compile(
    r"\bi\s+(?:think|believe|reckon|suspect|might|may)\b[^.!?,;]{0,30}?\b"
    r"(?:i(?:['\u2019]?ve|\s+have)?\s+)?(?:have|got)\s+(?P<thing>[a-z][a-z'\u2019 \-]{2,30})",
    re.I)
A_WONDER_SAID_NO = re.compile(
    r"\b(?:don'?t|do not|didn'?t|did not|never|not)\s+(?:think|believe|reckon|suspect)\b"
    r"|\bnot sure\b|\bno idea\b", re.I)
WITH_AN_ARTICLE = frozenset("a an the some any my our his her their this that these those".split())
A_CONDITION_KIND = re.compile(r"(?:disorder|syndrome|disease|infection|deficiency|condition|"
                              r"intolerance|allergy|virus|ulcer|fracture|clot|itis|concussion|"
                              r"hernia|mole|reaction|abscess|boil|polyp|stones?)$")
CONDITION_INITIALS = frozenset("""sti dvt uti hiv ibs ocd adhd ptsd ms me cf ibd copd gerd pnd
    tmj pcos""".split())
CONDITION_FAMILIES = (
    (re.compile(r"\b(?:depression|depressed|anxiety|ptsd|adhd|autism|autistic|bipolar|ocd|"
                r"eating|anorexi\w*|bulimi\w*|burnout|self.?harm)\b"), (
        "Whether it's {thing} isn't something I can judge from a chat - that takes a proper "
        "assessment, and the way in is a GP appointment or a self-referral to talking therapy. "
        "Say how long it has been like this and what has changed; that is where the assessment "
        "starts.",
        "I can't diagnose {thing} and a guess would be no use to you. Book a GP appointment and "
        "ask about a referral; with something like this the waiting list is the annoying part, "
        "so the useful move is to get in the queue now rather than when it gets worse.")),
    (re.compile(r"\b(?:sti|hiv|chlamydia|gonorrhoea|gonorrhea|herpes|syphilis|thrush|warts|"
                r"piles|haemorrhoids|hemorrhoids)\b"), (
        "I can't tell you from here whether it's {thing}. Get it checked: a sexual health "
        "clinic sees you without a GP referral, the test is quick and usually free, and they "
        "can treat it there too.",
        "Whether it's {thing} is a test question, not a chat one. Clinics do free, confidential "
        "testing and you can walk in without a referral - go sooner rather than later, because "
        "most of these are easy to sort once you know what it is.")),
    (None, (
        "Whether it's {thing} is a doctor's call, not something a chat can settle. Book an "
        "appointment and take a note of when it started and what has changed - that is what "
        "turns a hunch into an answer.",
        "I can't tell you whether you have {thing}, and a guess would be worse than no answer. "
        "Get it looked at - a GP or a walk-in clinic - and write down how long it has been going "
        "on first, because that is the first thing they ask.",
        "Whether it's {thing} is not something I can say from here - that needs someone who can "
        "examine you or run a test. Book it, and take three things: when it started, what has "
        "changed, and what you want out of the appointment.")),
)


def _the_route_for(thing):
    low = thing.lower()
    for family, frames in CONDITION_FAMILIES:
        if family is not None and family.search(low):
            return frames
    return CONDITION_FAMILIES[-1][1]


def _the_entry_names(entry, head):
    keys = getattr(entry, "key", ())
    if not keys:
        return True
    if head in keys:
        return True
    for word in keys:
        if len(word) > 3 and (word[:4] == head[:4] or word[:5] == head[:5]):
            return True
    return False


def _a_condition_they_wonder_about(clean, memory=None):
    if not clean or A_WONDER_SAID_NO.search(clean):
        return ""
    match = A_WONDERED_CONDITION.search(clean)
    if not match:
        return ""
    words = " ".join(match.group("thing").lower().split()).strip("-' ").split()
    if not words:
        return ""
    article = words[0] if words[0] in WITH_AN_ARTICLE else ""
    if article:
        words = words[1:]
    if not words:
        return ""
    head = words[-1]
    if head in NOT_A_THING or head.isdigit():
        return ""
    if any(word in NUMBER_WORDS for word in words) or any(ch.isdigit() for ch in head):
        return ""
    if any(word in VERBISH for word in words) and not A_CONDITION_KIND.search(head):
        return ""
    initials = head in CONDITION_INITIALS
    if article and not (A_CONDITION_KIND.search(head) or initials):
        return ""
    if reads_like_a_symptom(clean.lower()):
        return ""
    entry = topics.an_entry_for(clean)
    if entry is not None and _the_entry_names(entry, head):
        return ""
    phrase = " ".join([head.upper() if initials else word for word in words])
    if article:
        phrase = article + " " + phrase
    return pick(_the_route_for(phrase), memory, phrase).format(thing=phrase)


def _a_thing_they_have(clean, memory=None):
    read = _spoken(_repairs(clean, memory)) or clean
    match = HAVE_THING.search(read)
    if not match:
        return None
    thing = match.group(1).lower().strip("-'")
    if not thing or thing in NOT_A_THING or thing.isdigit():
        return None
    if _about_a_body(read, memory) or PLACED_IN_THE_PAST.search(read):
        return None
    if HABIT.search(read):
        return None
    what = _echo(clean, memory)
    if not what:
        return None
    pointer = _what_the_pointer_is(read, memory)
    if pointer:
        return pointer
    return pick(FRAMES, memory).format(thing=what, Thing=what[:1].upper() + what[1:])


RAISED = re.compile(r"\b(?:stretch\s+(?:it\s+)?(?:up\s+)?to|go\s+up\s+to|"
                    r"push\s+(?:it\s+)?(?:up\s+)?to)\b", re.I)


def _a_spending_budget(clean, memory):
    if PERIOD.search(clean or "") or A_SPAN_OF_TIME.search(clean or ""):
        return False
    if (facts.INTENDED_SPEND.search(clean or "") or facts.THE_THING_MAY_COST.search(clean or "")
            or facts.ALL_I_CAN_DO.search(clean or "")):
        return True
    if FOR_A_THING.search(clean or ""):
        return True
    recent = [clean or ""]
    for turn in (memory.get("turns") or [])[-3:] if isinstance(memory, dict) else []:
        if isinstance(turn, dict):
            recent.append(str(turn.get("user") or ""))
    for topic in (memory.get("topics") or [])[-2:] if isinstance(memory, dict) else []:
        if isinstance(topic, dict):
            recent.append(str(topic.get("text") or ""))
    said = (clean or "").strip().lower()
    others = [line for line in recent if line.strip().lower() != said]
    if RAISED.search(clean or ""):
        for line in others:
            if FOR_A_THING.search(line) or BUYING.search(line):
                return True
            if PERIOD.search(line) or A_SPAN_OF_TIME.search(line):
                return False
    if MONEY.search(" ".join(others).lower()):
        return False
    return bool(BUYING.search(" ".join(recent).lower()))


def _frames(found, heavy=False, clean="", memory=None):
    if found.get("budget"):
        return SPENDING_FRAMES if _a_spending_budget(clean, memory) else BUDGET_FRAMES
    condition = str(found.get("condition") or "").lower()
    if condition in CONDITION_FOOD:
        return CONDITION_FRAMES
    if found.get("diet") or found.get("allergies"):
        if "alcohol" in str(found.get("diet") or "").lower():
            return DRINK_FRAMES
        return FOOD_FRAMES
    if heavy and not _just_a_liking(found):
        return HEAVY_FRAMES if _about_the_family(found) else STILL_FRAMES
    if any(isinstance(entry, dict) and entry.get("allergies")
           for entry in (found.get("others") or [])):
        return OTHER_LIMIT_FRAMES
    if _about_someone_else(found, clean):
        if SOMEONE_GOOD.search(str(clean or "")):
            return SOMEONE_TAIL
        if _the_milestone(clean):
            return SOMEONE_MILESTONE_TAIL
        if _a_visit(clean):
            return VISIT_TAIL
    if _a_workplace(found, heavy, memory):
        step = len(clean or "") % len(WORK_FRAMES)
        return WORK_FRAMES[step:] + WORK_FRAMES[:step]
    coming = _a_day_coming(clean)
    if coming:
        return coming
    if _only_a_liking(found) and a_liked_thing(found) and _a_like_of_one_thing(clean, memory):
        step = len(clean or "") % len(LIKES_FRAMES)
        return LIKES_FRAMES[step:] + LIKES_FRAMES[:step]
    return FRAMES


THEIRS = re.compile(
    r"\b(?:my|our)\s+(?:mum|mom|mam|mother|dad|father|son|daughter|sister|brother|wife"
    r"|husband|partner|aunt|uncle|gran|granny|grandma|grandad|grandpa|nan|cousin|niece|nephew"
    r"|mate|mates|friend|neighbour|neighbor|colleague|boss|stepson|stepdaughter|stepdad|stepmum"
    r"|boyfriend|girlfriend|fiance|fiancee)(?:'?s)?\b", re.I)


def _about_someone_else(found, clean=""):
    for key in ("people", "others", "kids", "relations"):
        if (found or {}).get(key):
            return True
    return bool(THEIRS.search(str(clean or "")))


def _a_visit(clean):
    said = str(clean or "")
    if not said.strip() or said.rstrip().endswith("?") or NOT_A_VISIT.search(said):
        return False
    if re.match(r"\s*(?:when|what|how|why|where|who|is|are|does|do|will|did)\b", said, re.I):
        return False
    return bool(SOMEONE_COMING.search(said))


def _the_milestone(clean):
    return bool(SOMEONE_MILESTONE.search(str(clean or "")))


def _a_workplace(found, heavy=False, memory=None):
    if heavy or not isinstance(found, dict) or not found.get("job"):
        return False
    rest = [key for key, value in found.items()
            if value and key != "job" and not key.endswith("_frame")]
    if rest:
        return False
    frame = ""
    if isinstance(memory, dict):
        known = memory.get("user") if isinstance(memory.get("user"), dict) else {}
        frame = str(known.get("job_frame") or "").strip().lower()
    return bool(frame) and frame.split()[0] in WORK_PLACE


FAMILY = ("people", "others", "kids", "relations")


def _about_the_family(found):
    return any((found or {}).get(key) for key in FAMILY)


def _just_a_liking(found):
    rest = {key for key, value in (found or {}).items()
            if value and key != "tastes" and not key.endswith("_frame")}
    return bool((found or {}).get("tastes")) and not rest


def _heavy(memory):
    for turn in (memory.get("turns") or [])[-HEAVY_TURNS:]:
        if not isinstance(turn, dict):
            continue
        said = " ".join(str(turn.get("user") or "").split())
        if not said:
            continue
        if loss.reads_as_loss(said) or SEPARATION.search(said.lower()) or reads_as_cruelty(said):
            return True
    return False


def _statement(memory):
    understood = memory.get("understood")
    kind = understood.get("kind") if isinstance(understood, dict) else None
    if isinstance(kind, str) and kind:
        return kind in ("statement", "tell", "news")
    return True


def _a_loss(text, memory, clean):
    understood = memory.get("understood")
    topics = understood.get("topics") if isinstance(understood, dict) else None
    return loss.reply_for(text, memory, clean, topics) is not None


def _learned(text, memory=None):
    found = facts.extract(_spoken(text)) or facts.extract(text)
    kept = {key: value for key, value in found.items() if key in FACTS and value}
    if kept:
        return kept
    if _adds_one_more_allergen(text, memory):
        return {"allergies": _adds_one_more_allergen(text, memory)}
    if _adds_a_detail(text, memory):
        return {"detail": True}
    return {}


def _children_with_ages(text):
    reader = getattr(facts, "_kids_named_with_ages", None)
    try:
        return reader(text) if reader else []
    except Exception:
        return []


def _children_said(kids):
    parts = []
    for kid in kids[:4]:
        name = str(kid.get("name") or "")
        if not name:
            continue
        parts.append(name[:1].upper() + name[1:] + " is " + str(kid.get("age")))
    return " and ".join(parts)


def _adds_one_more_allergen(text, memory):
    if not isinstance(memory, dict):
        return []
    known = memory.get("user") if isinstance(memory.get("user"), dict) else {}
    held = known.get("allergies") or []
    if not isinstance(held, list) or not held:
        return []
    return facts.one_more(text)


def _adds_a_detail(text, memory):
    if memory is None:
        return False
    record = topics.carried_topic(memory, text) or topics.current(memory)
    if not record:
        return False
    clean = " ".join(str(text or "").split())
    read = _repaired(clean, memory)
    if "?" in clean or WANTS_ANSWER.search(read) or TROUBLE.search(read):
        return False
    if trouble.reads_as_trouble(read, read.split()):
        return False
    said_words = _words(clean)
    if len(said_words) < 2:
        return False
    if not re.search(r"[A-Za-z\u00c0-\u024f]", _strip_lead_in(clean)):
        return False
    if not re.search(r"[A-Za-z\u00c0-\u024f]", REPAIR_FRAME.sub("", clean)):
        return False
    if len(clean.split()) <= 2 and not DIGIT.search(clean):
        return False
    carried = (record.get("text") or "") + " " + " ".join(
        str(turn.get("user") or "") for turn in (memory.get("turns") or [])[-3:]
        if isinstance(turn, dict))
    if DEATH_WORDS.search(carried) or _NOT_A_DETAIL_SUBJECT.search(carried):
        return False
    for turn in (memory.get("turns") or [])[-2:]:
        if isinstance(turn, dict) and reads_as_bad_news(str(turn.get("user") or "")):
            return False
    known = set(_words(record.get("text") or ""))
    for earlier in record.get("details") or []:
        known |= set(_words(str(earlier)))
    if (_NOT_A_DETAIL.search(read) or _ANSWER_OPENER.match(read) or _ASKED_FOR.match(read)
            or _SAID_YES_NO.match(read) or _ASKS_MIDWAY.search(read) or _FAULT.search(read)):
        return False
    return any(word not in known for word in said_words)


REPAIR_FRAME = re.compile(
    r"^\s*(?:(?:no|nope|sorry|apologies|actually|wait|hold\s+on|oops|and|so|oh|right|ok|okay)"
    r"\b[\s,]*)*(?:i\s+(?:mean|meant)(?:\s+to\s+say)?|make\s+that|you\s+mean)\b[\s,]*", re.I)


def _words(text):
    out = []
    for word in WORD.findall(str(text or "").lower()):
        if word in _EMPTY:
            continue
        out.append(word)
    return out


VAGUE = frozenset("""everything anything something nothing all stuff things thing lot lots
    bit bits more less much many one ones again once anyway same usual normal worse better
    else other others""".split())


def _names_nothing(body):
    named = [word for word in _words(body) if word not in VAGUE]
    return not named


_OPENS_WITH_A_LINK = re.compile(r"^(?:for|about|to|of|with|in|on|at|over|into|like|as)\b", re.I)
MONEY_ONLY = re.compile(
    r"^(?:(?:about|around|under|below|less than|up to|max(?:imum)?|no more than|not more than)\s*)?"
    r"(?:[£$€]\s?\d[\d,.]*(?:\s?(?:k|pounds?|quid|euros?|dollars?|bucks))?"
    r"|\d[\d,.]*\s?(?:pounds?|quid|euros?|dollars?|bucks|k)\b)$", re.I)


def _repairs(clean, memory):
    understood = memory.get("understood") if isinstance(memory, dict) else None
    plain = understood.get("plain") if isinstance(understood, dict) else None
    if not isinstance(plain, str) or not plain.strip():
        return clean
    typed, fixed = clean.split(), plain.split()
    if not typed:
        return clean
    pairs, was_at, now_at = [], 0, 0
    while was_at < len(typed) and now_at < len(fixed):
        words = LEFT_OFF_CONTRACTION.get(typed[was_at].lower())
        if words and fixed[now_at:now_at + len(words)] == list(words):
            pairs.append((typed[was_at], " ".join(words)))
            now_at += len(words)
        elif (typed[was_at].lower() == fixed[now_at].lower()
              or (typed[was_at].isalpha()
                  and fixed[now_at].replace("'", "").replace("\u2019", "").isalpha())):
            pairs.append((typed[was_at], fixed[now_at]))
            now_at += 1
        else:
            return clean
        was_at += 1
    if was_at != len(typed) or now_at != len(fixed):
        return clean
    words = []
    for was, now in pairs:
        if (was != now and was.isalpha()
                and (now.replace("'", "").replace("\u2019", "").isalpha() or " " in now)
                and was.lower() != now.lower()):
            words.append(now[:1].upper() + now[1:] if was[:1].isupper() else now)
        else:
            words.append(was)
    return " ".join(words)


KIN_POSSESSIVE = re.compile(
    r"\b(your (?:mum|mom|mother|dad|father|son|daughter|sister|brother|wife|husband|partner"
    r"|nan|nana|granny|gran|grandma|grandad|grandpa|aunt|auntie|uncle|niece|nephew"
    r"|boyfriend|girlfriend|fiance|fiancee))s"
    r"(?= (?:\d+|called|named|name|age|coming|doing|gone|been|had|has|is|was|turns|turned)\b)",
    re.I)


A_COUNT_NOT_A_STATE = re.compile(
    r"^you're ((?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve))\s+"
    r"([a-z]{2,}s)\b", re.I)
UNITS_OF_MEASURE = frozenset((
    "years", "months", "weeks", "days", "hours", "minutes", "seconds", "nights", "mornings",
    "evenings", "hrs", "mins", "secs",
    "kilos", "kilograms", "kgs", "pounds", "lbs", "stones", "grams", "grammes", "ounces",
    "miles", "yards", "metres", "meters", "kilometres", "kilometers", "litres", "liters",
    "pints", "cups", "calories", "degrees", "inches"))
WHOS = re.compile(r"\bwhos\b", re.I)


def _says_something(body):
    return facts._tail_has_a_verb(re.findall(r"[a-z']+", str(body or "").lower()))
NO_REFERENT = (
    "The same one as what?",
    "Which one do you mean?",
    "Same as what? Tell me what we are talking about and I will pick it up.",
    "I have lost the thread - which one do you mean?",
)
POINTS_AT_ANOTHER = re.compile(
    r"\b(?:another one|one more|another|one too|one as well|one aswell|one before"
    r"|one of those|the same one|one like it|one like that)\b", re.I)
A_DECISION = re.compile(
    r"\b(?:want|wants|wanted|should|shall|might|could|would|thinking|think|planning|planned"
    r"|considering|maybe|tempted|weighing|worth)\b", re.I)
REPORTS_AN_ACTION = re.compile(
    r"\b(?:saw|seen|read|made|bought|finished|started|watched|met|caught|found|killed"
    r"|sold|won|lost)\b", re.I)
POINTER_FILLER = frozenset("""
i we you he she they it me my our your his her their its us them mine ours
the a an and but so also too as well just even still already now again then
had has have got gotten get gets bought buy buying made make makes making
finished finish started start read reading seen saw did do does doing
one ones another more of that this these those there here before after
""".split()) | frozenset(facts.RELATIONS) | frozenset("""
wife husband partner boyfriend girlfriend son daughter child kid kids baby mum mom mother
dad father brother sister friend mate colleague boss family parents in laws
""".split())
NOT_A_THING_TO_HAVE_ANOTHER = frozenset("""
another more one ones same other else lot bit piece time times day days week weeks
month months year years hour hours minute minutes while thing things stuff kind sort
""".split()) | frozenset(facts.RELATIONS)

ANOTHER_ONE = (
    "Another {thing}?",
    "A second {thing}, then. How is it going?",
    "Another {thing} - what is this one like?",
    "Two {things}, then. How are they getting on?",
)
ANOTHER_ONES = (
    "More {things}?",
    "Another lot of {things}, then. How are they getting on?",
    "More {things} - how are the first lot doing?",
)
BEFORE_ONE = (
    "How does this one compare to the last?",
    "What happened to the first {thing}?",
    "Still got the first {thing}?",
)
SOMEONE_ELSE_POINTS_AT_ANOTHER = re.compile(
    r"\b(?:my|our)\s+([a-z]+(?:[- ](?:in[- ]law|law))?)\s+"
    r"(?:has|have|got|gets|bought|buys|wants|wanted|had|found|rescued|adopted|is getting"
    r"|is buying|is having)\s+"
    r"(?:another one|one too|one as well|one aswell|one of those|the same one|another)\b", re.I)
PRONOUN_POINTS_AT_ANOTHER = re.compile(
    r"\b(?:she|he|they)\s+(?:has|have|got|gets|bought|wants|wanted|had|found|rescued|adopted)\s+"
    r"(?:another one|one too|one as well|one aswell|one of those|the same one)\b", re.I)
ANOTHER_ONE_FOR_SOMEONE = (
    "Your {person} too, then. How is the {thing} going?",
    "Your {person} as well, then - what is the {thing} like?",
)
ANOTHER_SOME_FOR_SOMEONE = (
    "Your {person} has some too, then. How are the {things} going?",
    "Your {person} as well, then - how are the {things} getting on?",
)


def _the_person_the_pointer_is_about(body, memory):
    found = SOMEONE_ELSE_POINTS_AT_ANOTHER.search(body)
    if found:
        word = found.group(1).strip().lower()
        return "" if word in ("own", "self") else word
    if PRONOUN_POINTS_AT_ANOTHER.search(body):
        for turn in reversed((memory.get("turns") or [])[-3:]):
            if not isinstance(turn, dict):
                continue
            said = str(turn.get("user") or "").lower()
            for word in facts.RELATIONS:
                if re.search(r"\bmy\s+" + re.escape(word) + r"\b", said):
                    return word
    return ""


def _the_thing_the_chat_is_on(memory):
    phrase = " ".join(str(topics.subject(memory) or "").split()).lower()
    if not phrase:
        return "", False, ""
    named_words = set()
    for turn in reversed((memory.get("turns") or [])[-3:]):
        if isinstance(turn, dict):
            named_words.update(_a_thing_the_line_named(turn.get("user")))
    named_words -= NOT_A_SECOND_OF
    if not named_words:
        return "", False, ""
    stems = {topics.stem(word) for word in named_words}
    stem = ""
    for word in re.split(r"[^a-z]+", phrase):
        if (len(word) > 2 and word not in named.NOT_THE_THING
                and word not in NOT_A_THING_TO_HAVE_ANOTHER
                and (word in named_words or topics.stem(word) in stems)):
            stem = word
    if not stem or stem in NOT_A_THING_TO_HAVE_ANOTHER or stem in facts.RELATIONS:
        return "", False, ""
    if _something_they_avoid(memory, stem) or _a_name_the_store_holds(memory, stem):
        return "", False, ""
    said = ""
    for turn in reversed((memory.get("turns") or [])[-3:]):
        if not isinstance(turn, dict):
            continue
        for word in re.findall(r"[a-z']+", str(turn.get("user") or "").lower()):
            if word == stem or topics.stem(word) == stem:
                said = word
                break
        if said:
            break
    said = said or stem
    return said, said != stem, _plural(said)


A_NAME_GIVEN = re.compile(r"\b(?:called|named|name is|name's|names)\s+([a-z']+)", re.I)


def _a_name_the_store_holds(memory, stem):
    if not isinstance(memory, dict):
        return False
    names = []
    known = memory.get("user") if isinstance(memory.get("user"), dict) else {}
    for pet in known.get("pets") or []:
        if isinstance(pet, dict) and pet.get("name"):
            names.append(str(pet["name"]))
    for other in memory.get("others") or []:
        if isinstance(other, dict) and other.get("name"):
            names.append(str(other["name"]))
    person = memory.get("person")
    if isinstance(person, dict) and person.get("name"):
        names.append(str(person["name"]))
    for turn in (memory.get("turns") or [])[-3:]:
        said = str((turn or {}).get("user") or "") if isinstance(turn, dict) else ""
        found = A_NAME_GIVEN.search(said)
        if found:
            names.append(found.group(1))
    return any(topics.stem(name) == stem for name in names if name)


def _something_they_avoid(memory, stem):
    if not isinstance(memory, dict):
        return False
    known = memory.get("user") if isinstance(memory.get("user"), dict) else {}
    meal = memory.get("meal") if isinstance(memory.get("meal"), dict) else {}
    for word in list(known.get("allergies") or []) + list(meal.get("avoid") or []):
        if topics.stem(str(word)) == stem:
            return True
    return False


def _plural(word):
    if word.endswith("s"):
        return word
    if word.endswith(("x", "z", "ch", "sh")):
        return word + "es"
    if len(word) > 2 and word.endswith("y") and word[-2] not in "aeiou":
        return word[:-1] + "ies"
    return word + "s"


ENDS_THE_THING_VERB = frozenset("""
aint arent cant couldnt didnt doesnt dont hadnt hasnt havent isnt mustnt neednt shant wasnt
werent wont wouldnt shouldnt
went gone came got gotten took taken gave given told said seen knew known kept
brought bought found goes comes says keeps sees knows thinks tells gives takes makes
""".split())


def _is_a_contraction(word):
    return "n't" in word or word in ENDS_THE_THING_VERB


A_DETERMINER = re.compile(
    r"\b(?:a|an|the|my|our|his|her|their|your|another|some|two|three|four|five|six|"
    r"seven|eight|nine|ten)\b", re.I)
ENDS_THE_THING = frozenset("""
in on at to for with from of about by into onto over under out up down off through across along
after before during since until while when where why how what which who whom whose that this
these those and but or so because if than then
i me you we us they them he him she it its am is are was were be been being have has had do does
did will would can could should may might must not no
very really quite too also just still again now last next
bit lot few couple other same whole rest most least more less only first
""".split())


NOT_A_SECOND_OF = frozenset("""
traffic weather news advice information knowledge music homework housework work sleep noise mess
rubbish luck rain snow water wind light heat fun health pain stress exercise help space shopping
cleaning washing food drink dinner breakfast lunch tea coffee time money
""".split())


def _a_thing_the_line_named(text):
    words = re.findall(r"[a-z']+", str(text or "").lower())
    out = set()
    for at, word in enumerate(words):
        if not A_DETERMINER.fullmatch(word):
            continue
        head = ""
        for after in words[at + 1:at + 4]:
            if after in ENDS_THE_THING or len(after) <= 2 or _is_a_contraction(after):
                break
            head = after
        if head:
            out.add(head)
    return out


def _a_loss_just_before(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return False
    for turn in turns[-2:]:
        if isinstance(turn, dict) and facts.DIED.search(str(turn.get("user") or "")):
            return True
    return False


def _another_of_what_we_said(clean, memory):
    if not isinstance(memory, dict):
        return None
    turns = memory.get("turns")
    body = clean.strip()
    if not body or "?" in body or len(body.split()) > 8:
        return None
    if A_DECISION.search(body):
        return None
    found = POINTS_AT_ANOTHER.search(body)
    if not found:
        return None
    left = [word for word in re.findall(r"[a-z']+", POINTS_AT_ANOTHER.sub(" ", body).lower())
            if word not in POINTER_FILLER]
    if left:
        return None
    if (REPORTS_AN_ACTION.search(body)
            and found.group(0).lower() not in ("one before", "the same one")):
        return None
    if _a_loss_just_before(memory):
        return None
    one, several, plural = _the_thing_the_chat_is_on(memory)
    if not one:
        return pick(NO_REFERENT, memory, seed_text=body)
    person = _the_person_the_pointer_is_about(body, memory)
    if person:
        pool = ANOTHER_SOME_FOR_SOMEONE if several else ANOTHER_ONE_FOR_SOMEONE
        return pick(pool, memory, seed_text=body).format(
            person=person, thing=one, things=plural)
    if found.group(0).lower() == "one before":
        return pick(BEFORE_ONE, memory, seed_text=body).format(thing=one)
    if several:
        return pick(ANOTHER_ONES, memory, seed_text=body).format(things=plural)
    return pick(ANOTHER_ONE, memory, seed_text=body).format(thing=one, things=plural)


def _only_the_correction_in_front(kept, body):
    kept = " ".join(str(kept or "").split())
    body = " ".join(str(body or "").split())
    if not kept or not body or kept == body:
        return False
    if not kept.lower().endswith(body.lower()):
        return False
    front = kept[:len(kept) - len(body)]
    return bool(front.strip() and facts.is_a_correction_opener(front))


HAVE_GOT = re.compile(r"\b(you|we)\s+have\s+got\b", re.I)
HAVE_A = re.compile(r"\b(You|you|We|we)\s+have\s+a\b")


def _echo(clean, memory=None):
    clean = without_a_leading_exclamation(clean)
    said_it = _repairs(clean, memory)
    body = _strip_lead_in(said_it)
    if body and not _says_something(body):
        kept = _strip_lead_in(said_it, keep_the_repair=True)
        if kept != body and not _only_the_correction_in_front(kept, body):
            body = kept
    if not body:
        return None
    if _names_nothing(body):
        return None
    if (_OPENS_WITH_A_LINK.match(body) and len(body.split()) <= 3
            and not MONEY_ONLY.match(body.strip(" .,!?"))):
        return None
    if len(body) <= MOST:
        said = body
    else:
        clauses = [clause.strip() for clause in STOP.split(body) if clause.strip()]
        said = ", ".join(clauses[:CLAUSES]) if clauses else body
    said = _cut(said).strip(" ,;:-!?.\u2014")
    said = POLITE.sub("", said).strip(" ,;:-")
    said = _tail_off(said)
    said = _contrast_off(said).strip(" ,;:-")
    said = _reason_off(said, clean).strip(" ,;:-")
    said = _pick_off(said).strip(" ,;:-")
    if not said:
        return None
    back = _tidy(KIN_POSSESSIVE.sub(r"\1's", say_it_back(_spoken(said)).strip(" ,;:-")))
    if not back:
        return None
    back = HAVE_GOT.sub(r"\1've got", back)
    counted = A_COUNT_NOT_A_STATE.match(back)
    if counted and counted.group(2).lower() not in UNITS_OF_MEASURE:
        back = "you've got " + back[counted.start(1):]
    return WHOS.sub("who's", back)


def said_back(clean, memory=None):
    return _echo(clean, memory)


def _only_a_dislike(body, found):
    if not (found or {}).get("tastes"):
        return False
    return not TROUBLE.search(taste.DISLIKE_IN.sub(" ", body))


def only_a_dislike(text, memory=None):
    clean = " ".join(str(text or "").split())
    if not clean:
        return False
    return _only_a_dislike(_strip_lead_in(clean), _learned(clean, memory))


def _tells_it(clean, found=None):
    body = _strip_lead_in(clean)
    others = [entry for entry in (found or {}).get("others") or [] if isinstance(entry, dict)]
    if any("name" in entry or "age" in entry for entry in others):
        return True
    if facts.foods_ruled_out(found):
        return True
    if TROUBLE.search(body) and not _a_diet(found) and not _only_a_dislike(body, found):
        return False
    if (found or {}).get("done"):
        return True
    return bool(STATE.search(body)) or len(body) <= FRAGMENT


def _a_diet(found):
    if not isinstance(found, dict):
        return False
    if found.get("diet") or found.get("no_meat"):
        return True
    return any(entry.get("diet") for entry in (found.get("others") or [])
               if isinstance(entry, dict))


FIGURE_LEAD = re.compile(
    r"^(?:i\s*(?:'m|am)|im|i\s+just\s+turned|my\s+(?:age|height)\s+is)\b[\s,]*", re.I)
FIGURE_FILLER = frozenset("""year years yrs yr old this now today already and""".split())
FIGURE_UNIT = frozenset("""ft foot feet in inch inches cm m st stone pounds pound lbs lb
    kilo kilos kg metres meters""".split())
FIGURE_WORD = frozenset("""one two three four five six seven eight nine ten eleven""".split())


def _only_the_figure(clean):
    body = " ".join(FIGURE_LEAD.sub("", _strip_lead_in(clean)).split())
    words = [word.strip(".,!;:") for word in body.split()]
    words = [word for word in words if word and word.lower() not in FIGURE_FILLER]
    return all(re.fullmatch(r"\d{1,3}(?:st|nd|rd|th)?(?:(?:cm|m|ft|in|kg|st|lbs?)s?)?", word)
               or word.lower() in FIGURE_UNIT or word.lower() in FIGURE_WORD for word in words)


A_CONTINUATION = re.compile(r"^(?:and|also|plus|or|what about|how about|and what about)\b", re.I)
A_CLAUSE = re.compile(
    r"\b(?:is|are|am|was|were|be|been|being|isnt|arent|wasnt|werent|has|have|had|hasnt|havent|"
    r"hadnt|do|does|did|dont|doesnt|didnt|will|wont|would|wouldnt|can|cant|could|couldnt|should|"
    r"shouldnt|shall|may|might|must|got|get|gets|getting|go|goes|going|went|gone|need|needs|"
    r"needed|want|wants|wanted|like|likes|liked|think|thinks|thought|know|knows|knew|take|takes|"
    r"taking|took|make|makes|making|made|start|starts|started|come|comes|came|live|lives|lived|"
    r"work|works|worked|feel|feels|felt|keep|keeps|kept|try|tries|trying|look|looks|looking|"
    r"plan|plans|planning|book|booked|hope|hoping|wait|waiting|see|saw|seen|say|says|said)\b",
    re.I)
A_SOMEONE = re.compile(
    r"\b(?:i|i'm|im|i've|ive|i'd|id|i'll|ill|me|my|we|we're|were|we've|our|us)\b", re.I)


def _the_rest_of_a_question(clean, before=""):
    line = " ".join(str(clean or "").split())
    match = A_CONTINUATION.match(line)
    if not match:
        return False
    rest = line[match.end():].strip(" ,.;:-!?")
    if not rest:
        return False
    if A_CLAUSE.search(rest) or A_SOMEONE.search(rest):
        return False
    return reads_as_an_ask(before)


the_rest_of_a_question = _the_rest_of_a_question


NO_THEN_A_LINE = (
    r"no\s+(?=(?:"
    r"i|im|i'm|we|we're|were|you|youre|you're|he|hes|he's|she|shes|she's|it|its|it's|"
    r"they|theyre|they're|this|that|thats|that's|these|those|there|"
    r"the|not|my|our|your|his|her|their"
    r")\b)")

NO_THEN_A_LINE_ONLY = re.compile(r"^\s*" + NO_THEN_A_LINE, re.I)
NO_LEAD = re.compile(
    r"^\s*(?:(?:"
    r"no\s*,"
    r"|" + NO_THEN_A_LINE +
    r"|(?:no\s+|oh\s+|sorry\s+|actually\s+)?(?:wait|hang\s+on|hold\s+on)\s*,"
    r"|(?:i\s+(?:meant|mean)(?:\s+to\s+say)?"
    r"(?!\s*,?\s*(?:it|that|this|so)\b(?:\s*,?\s*\w+){0,2}\s*[.!?]*\s*$)"
    r"|you\s+mean|make\s+that)\b\s*,?"
    r"|(?:sorry|apologies|actually|oops|oh)\s*,"
    r")\s*)+", re.I)


REACTION_PHRASES = frozenset((
    "quiet one", "quiet day", "busy one", "busy day", "slow day", "long day", "not bad",
    "not much", "nothing much", "not a lot", "all good", "can't complain", "cant complain",
    "same as ever", "good thanks", "fine thanks", "no complaints", "same old", "usual stuff",
    "you too", "likewise", "went ok", "went well", "went fine", "so so", "so-so", "up and down",
    "not too bad",
))
REACTION_WORDS = frozenset("""
lucky you fair enough got it sounds good sound good great nice cool lovely perfect ace brilliant
oh dear dear me good luck well done makes sense same here me too that's right exactly agreed
no worries okay ok thanks ta cheers haha lol ha magic typical bless you what a shame that's a
shame of course indeed true sure yeah yes oh wow ouch yikes a
""".split())
_REACTION_CLAUSE = re.compile(r"^([^.?!,;:]{1,32})[.?!,;:]+\s*(?=\S)")


def _after_a_reaction(text):
    match = _REACTION_CLAUSE.match(text)
    if not match:
        return text
    clause = " ".join(match.group(1).split()).lower()
    words = [word.strip("'\u2019") for word in match.group(1).split()]
    if not words or len(words) > 5:
        return text
    if clause not in REACTION_PHRASES and not all(word.lower() in REACTION_WORDS
                                                for word in words):
        return text
    return text[match.end():].strip()


def _strip_lead_in(clean, keep_the_repair=False):
    text = clean.strip(" ,;:-")
    text = NO_THEN_A_LINE_ONLY.sub("", text)
    if not keep_the_repair:
        text = NO_LEAD.sub("", text)
    changed = True
    while changed:
        changed = False
        bare = text if keep_the_repair else NO_LEAD.sub("", text)
        if bare != text:
            text, changed = bare, True
            continue
        for lead in sorted(LEAD_IN, key=len, reverse=True):
            low = text.lower()
            if low.startswith(lead) and low[len(lead):len(lead) + 1] in ("", " ", ",", ";", ":",
                                                                       "-", "!", "?", "."):
                text = text[len(lead):].lstrip(" ,;:-!?.")
                changed = True
                break
        if not changed:
            done = _after_a_reaction(text)
            if done != text:
                text, changed = done, True
    return text


def without_the_frame(clean):
    return _strip_lead_in(" ".join(str(clean or "").split()))


COUNTED_STARS = re.compile(
    r"\b(?:(?:a|an)\s+)?(?P<count>[1-9]|1[0-2])\s+a[\s*'-]?stars?\b", re.I)
ONE_STAR = re.compile(r"\b(?:an?|one)\s+a[\s*-]?star\b", re.I)
STAR_COUNT = {1: "an A*", 2: "two A*s", 3: "three A*s", 4: "four A*s", 5: "five A*s",
              6: "six A*s", 7: "seven A*s", 8: "eight A*s", 9: "nine A*s", 10: "ten A*s",
              11: "eleven A*s", 12: "twelve A*s"}
COUNTED_LETTERS = re.compile(
    r"\b(?P<count>[2-9]|1[0-2])\s+(?P<letter>a|b|c|d)(?:'?s|s)\b"
    r"(?=\s*(?:$|[,.;!?]|and\b|but\b))", re.I)
LETTER_COUNT = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight",
                9: "nine", 10: "ten", 11: "eleven", 12: "twelve"}
A_DEGREE = re.compile(r"\b(?:degree|degrees|uni|university|graduat\w*|honours|bsc|ba|masters?|"
                      r"phd|dissertation|final year)\b", re.I)
DEGREE_CLASS = re.compile(r"\b(?P<first>[12])\s*[:.\- ]\s*(?P<second>[12])\b")


def _spoken(said):
    said = COUNTED_STARS.sub(lambda match: STAR_COUNT[int(match.group("count"))], said)
    said = ONE_STAR.sub("an A*", said)
    said = COUNTED_LETTERS.sub(
        lambda match: LETTER_COUNT[int(match.group("count"))] + " " + match.group("letter").upper()
        + "s", said)
    if A_DEGREE.search(said):
        said = DEGREE_CLASS.sub(lambda match: match.group("first") + ":" + match.group("second"),
                                said)
    said = WITH_SLASH.sub("with ", said)
    said = TWO_TO.sub(lambda match: match.group(0)[:-1] + "to", said)
    said = TWO_PLACE.sub("to ", said)
    said = TWO_VERB.sub("to ", said)
    out = []
    words = said.split()
    for place, word in enumerate(words):
        bare = word.lower().strip(".,;:!?")
        tail = word[len(word.rstrip(".,;:!?")):]
        after = words[place + 1].lower().strip(".,;:!?") if place + 1 < len(words) else ""
        before = words[place - 1].lower().strip(".,;:!?") if place else ""
        if bare == "yer":
            out.append(("yeah" if not after or after in YES_AFTER else "your") + tail)
        elif bare == "its" and before in ITS_OWNS_AFTER:
            out.append(word)
        elif bare in SPEAK:
            out.append(SPEAK[bare] + tail)
        elif bare in SHORT:
            out.append(SHORT[bare] + tail)
        else:
            out.append(word)
    return " ".join(out)


CONTRAST = re.compile(r"\s*,?\s+not\s+(?P<old>[\w'’$£€.,:/-]+"
                      r"(?:\s+[\w'’$£€.,:/-]+){0,3})\s*$", re.I)
CONTRAST_SAID_AGAIN = re.compile(
    r"^(?P<thing>[a-z]+(?:\s+[a-z]+){0,2})\s+not\s+(?P<old>[\w'’$£€.,:/-]+)\s+"
    r"(?P=thing)\s+(?P<new>[\w'’$£€.,:/-]+(?:\s+[\w'’$£€.,:/-]+){0,2})\s*$",
    re.I)
NOT_A_VALUE = frozenset("""a an the any sure really very too that this it them me you him her us
say said tell go going gone get got want need like mind be been being am is are was were have
has had can could would should will do does did make take give put keep try yet even still
allowed able bothered""".split())


PICK_FRAME = re.compile(
    r"^\W*(?:"
    r"(?:let'?s|let\s+us|i'?ll|we'?ll|i\s+will|we\s+will)\s+go\s+(?:with|for)\b"
    r"|(?:i|we)\s+(?:have\s+|had\s+)?(?:settled|decided|decide|settle)\s+(?:on|for)\b"
    r"|(?:i|we)\s+(?:have\s+|had\s+)?(?:opted|opt)\s+for\b"
    r"|(?:i|we)\s+(?:picked|pick|chose|choose)\b"
    r"|(?:i|we)'?ve\s+(?:settled|decided|gone)\s+(?:on|for|with)\b"
    r"|(?:make|makes)\s+(?:it|that)\b"
    r")", re.I)


def _pick_off(said):
    match = PICK_FRAME.match(said or "")
    if not match:
        return said
    rest = (said or "")[match.end():].strip(" ,;:-.!?\u2014")
    if len(rest.split()) < 1:
        return said
    return rest


def _tail_off(said):
    said = without_filler(said)
    words = said.split()
    while words:
        low = " ".join(words).lower().strip(" ,;:-")
        cut = next((phrase for phrase in facts.FILLER_TAIL_PHRASES if low.endswith(phrase)), None)
        if not cut or len(words) <= len(cut.split()):
            break
        words = words[:-len(cut.split())]
    return " ".join(words).strip(" ,;:-")


def _contrast_off(said):
    again = CONTRAST_SAID_AGAIN.match(str(said or "").strip())
    if again and _a_value(again.group("old")):
        return "%s %s" % (again.group("thing"), again.group("new"))
    match = CONTRAST.search(said or "")
    if not match:
        return said
    old = [word for word in re.split(r"\s+", match.group("old").strip(" .,;:-")) if word]
    if old and old[0].lower() in ("the", "a", "an"):
        old = old[1:]
    if not old or not re.search(r"[a-z0-9]", old[0], re.I):
        return said
    kept = [word for word in re.split(r"\s+", said[:match.start()].strip(" .,;:-")) if word]
    if old[0].lower() in NOT_A_VALUE:
        return said
    if not (_a_value(old[0]) or (kept and _a_value(kept[-1]))):
        return said
    restated = _the_value_put_right(said, match)
    if restated:
        return restated
    return said[:match.start()]


A_REASON_TAIL = re.compile(r"\s+(?:because|cos|coz|cuz|'cause|since)\b[^.!?]*", re.I)
A_CORRECTION_IN_FRONT = re.compile(
    r"^\s*(?:actually|no|nope|sorry|wait|oh|i\s+mean|i\s+meant|make\s+that)\b", re.I)


def _reason_off(said, clean):
    if not A_CORRECTION_IN_FRONT.match(clean or ""):
        return said
    match = A_REASON_TAIL.search(said or "")
    if not match or not said[:match.start()].strip(" ,;:-"):
        return said
    return said[:match.start()]


BETWEEN_VALUES = frozenset("""he she it they we you i his her its their our my
is was are be been am just only now actually really still but
hes shes its theyre im youre were s""".split())


def _the_value_put_right(said, match):
    head = " ".join(str(said or "")[:match.start()].split()).strip(" ,;:-—")
    if not head:
        return ""
    if any(_a_value(word) for word in re.split(r"\s+", head)):
        return ""
    words = [word for word in re.split(r"\s+", match.group("old").strip(" .,;:-")) if word]
    if len(words) < 3:
        return ""
    second = next((at for at in range(1, len(words)) if _a_value(words[at])), None)
    if second is None:
        return ""
    between = [word.lower().strip(".,!?'\u2019") for word in words[1:second]]
    if not between or any(word not in BETWEEN_VALUES for word in between):
        return ""
    return head + " " + " ".join(words[second:])


VALUE = re.compile(r"\d|^(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
                   r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|"
                   r"thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|a|an|"
                   r"grand|quid|pm|am)$", re.I)


MAKE_A_VALUE = re.compile(
    r"^\s*(?:(?:no|nope|sorry|ah|oh|ok|okay|right|and|so|well|actually|wait|hmm)[,.]?\s+)*"
    r"(?:make\s+(?:it|that)|change\s+(?:it|that)\s+to|switch\s+(?:it|that)\s+to)\s+"
    r"(?P<value>[^,.!?;]{1,40}?)\s*[.!]*\s*$", re.I)
VALUE_WORDS = frozenset("""half quarter past to oclock am pm once twice one two three four five six
seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen
twenty thirty forty fifty sixty seventy eighty ninety hundred thousand a an grand the
every of hour hours minute minutes week weeks day days month months year years time times per a
kilo kilos kg mile miles km pound pounds quid dollar dollars euro euros""".split())
UNITS_AFTER = frozenset("""times time a an per week weeks day days month months year years hour
hours minute minutes mile miles km kilo kilos pound pounds quid egg eggs cup cups spoon
spoons every morning evening night weekend""".split())


def _a_value(word):
    low = str(word or "").strip(" .,;:!?\u2019'").lower()
    if not low:
        return False
    if VALUE.match(low):
        return True
    return low in DAYS or low in MONTHS


def _cut(said):
    if len(said) <= MOST:
        return said
    kept = said[:MOST].rsplit(" ", 1)[0].rstrip(" ,;:-")
    return kept if " " in kept else said[:MOST]


FIRST_WORD = frozenset((
    "he", "he's", "he'll", "she", "she's", "she'll", "it", "it's", "it'll", "they", "they're",
    "they'll", "they've", "we", "we're", "we'll", "we've", "our", "there's", "there'll",
    "the", "this", "that", "these", "those", "a", "an", "my", "his", "her", "its", "just",
    "not", "no", "and", "but", "so", "also", "then", "now", "still", "only", "even", "both",
    "all", "every", "at", "in", "on", "for", "after", "about", "around", "one", "two", "three",
    "four", "five", "six", "seven", "eight", "nine", "ten", "half", "someone", "something",
    "nothing", "theres", "theyll",
))


def _tidy(text):
    words = text.split()
    out = []
    for index, word in enumerate(words):
        low = word.lower()
        if low in ("you", "your", "you're", "you've", "we", "our", "yourself"):
            word = low
        elif index == 0 and low in FIRST_WORD:
            word = low
        out.append(word)
    return " ".join(out)
