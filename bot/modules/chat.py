import copy
import re

from ..compose import (LINGERED_LINE, badnews, circumstance, doubted, fallback, greet_with,
                       nearly, negated, pick, says_it_has_lingered, step_when_low)
from ..compose import leaving as leaving_reading
from ..compose import limit as limit_line
from ..compose.badnews import reads_as_bad_news, reads_like_a_symptom
from ..compose.goodnews import (a_detail_of_the_news, asks_for_news,
                                MORE_OF_THE_NEWS, MORE_OF_THE_NEWS_ARRIVAL,
                                MORE_OF_THE_NEWS_SCORE, reads_as_a_pass,
                                reads_as_a_win_nobody_noticed,
                                reads_as_a_prize_in_a_message, reads_as_good_news,
                                reply_for_a_win_from_a_past_year)
from ..memory import hope, matters, obstacle, plan as plan_steps
from ..memory.when import asks_what_today_is
from ..memory import size as another_size
from ..memory.cause import NO_REASON as _NO_REASON
from ..knowledge.lookup import the_body_is_short_of_sleep
from ..understanding import breeds, topics
from ..understanding.kinds import (ADDRESSED, EMOTION_WORDS, THANKS_NOISE,
                                   ANSWERING_A_QUOTED_ASK, cue_about_person,
                                   the_manners_question, verdicts_a_thing, shortage_of)
from ..compose import loss as loss_reading
from ..compose import onscreen
from ..compose import unseen as unseen_reading
from ..compose import harm as harm_reading
from ..compose import saidby as saidby_reading
from ..compose import reaction as answer_reaction
from ..compose import repair
from ..compose import said_about_me
from ..compose.repair import (DEEDS_WITH_A_CARD, amends_to, deed_of, owns_the_deed,
                              with_the_feeling_named)
from ..compose import reading as reading_reply
from ..compose import urgent as urgent_reading
from ..compose import stepwords
from ..compose import verdict as verdict_reply
from ..compose import doubt as doubt_reply
from ..compose import occasionplan
from ..memory import PERSON_TROUBLE as SOMEONE_TROUBLE
from ..memory import WHO_SAID, about, about as about_the_person, current, person, person_named, trouble, user, you

from ..memory import ack, current, last_user as _last_said, user, you
from ..memory import remedy
from ..memory import stuck as stuck_line
from ..memory import thread
from ..memory.facts import JUDGEMENT_AFTER, JUDGEMENT_NOUNS
from ..memory.topics import in_a_safety_thread as _safety_thread
from ..memory.topics import names_nothing
from ..memory.topics import keywords as _content_words

from ..memory import again as _same_again
from ..memory import carried_on as step_after
from ..memory import passing_the_time
from ..memory import the_years
from ..memory import warmth as talked_to
from ..memory import limits, portions
from ..memory import facts, hours as hours_after, limit, meant, pile, repeat, tried, more, returned
from ..memory import topics as topic_memory
from ..memory.ack import A_MOVE, a_person_getting_better, nobody_around
from ..knowledge import lookup
from ..knowledge import travel as travel_kb
from ..understanding import lexicon
from ..understanding import understand as understanding
from ..understanding.topics import PLACES as KNOWN_PLACES

PRIORITY = 300

ANSWERS = ("small-talk", "about-the-bot")

TOKEN = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")

GREET_CORE = {"hi", "hiya", "hey", "heya", "hello", "yo", "howdy", "morning", "afternoon",
              "evening", "greetings", "hallo", "helo"}
GREET_FILLER = {"good", "day", "all", "everyone", "folks", "guys", "team", "there", "again",
                "x", "everybody", "you", "lot", "the", "hi", "hiya", "hey", "heya", "hello",
                "yo", "howdy", "morning", "afternoon", "evening", "greetings", "hallo", "helo"}

THANKS_CORE = {"thanks", "thank", "thx", "ty", "cheers", "ta", "appreciated", "appreciate",
               "thnx", "thks"}
THANKS_LOOSE = {"one", "nice", "try", "ill", "will", "give", "go", "it", "lets", "today",
                "tomorrow", "later", "now", "anything", "else", "that", "this", "was", "is",
                "brill", "yeah", "yep", "earlier", "before", "sorted", "worked", "works",
                "far", "helped", "super", "legend", "ace", "so", "much", "again", "for"}
HELP_ONLY = frozenset("""help me us please pls a bit of then now thanks you sir mate""".split())
THANKS_FILLER = {"you", "u", "so", "much", "very", "a", "lot", "again", "for", "the", "help",
                 "thats", "its", "they", "were", "are", "im", "i", "am", "welcome", "again",
                 "well", "good", "okay", "alright", "brill", "cheers",
                 "helping", "that", "this", "is", "was", "its", "it", "perfect", "great",
                 "brilliant", "lovely", "awesome", "amazing", "excellent", "good", "nice",
                 "handy", "helpful", "works", "worked", "sorted", "really", "super", "too",
                 "all", "and", "ok", "okay", "man", "mate", "friend", "so", "much",
                 "idea", "do", "will",
                 "grand", "chill", "content", "mint", "sound"}

ACK_WORDS = {"ok", "okay", "k", "kk", "cool", "nice", "great", "good", "fine", "sounds",
             "sound", "perfect", "brilliant", "lovely", "awesome", "amazing", "sure",
             "alright", "right", "righto", "aight", "yes", "yeah", "yep", "yup", "ya",
             "yh", "yhh", "ye", "no",
             "nah", "nope", "not", "really", "hmm", "hm", "oh", "ah", "aha", "wow", "damn",
             "meh", "idk", "i", "im", "dont", "know", "dunno", "maybe", "lol", "lmao", "haha",
             "hehe", "of", "course", "that", "this", "is", "was", "it", "its", "then", "well",
             "true", "fair", "enough", "makes", "sense", "got", "you", "u", "thanks", "thx",
             "ty", "cheers", "ill", "see", "have", "think", "about", "probably", "definitely",
             "most", "likely", "working", "for", "me", "thats", "sweet", "neat", "huh",
             "and", "but", "so", "oh", "worried", "sad", "happy", "fine", "bad", "good", "same",
             "well", "too", "okay", "alright", "nice",
             "grand", "chill", "content", "mint"}
LAUGH_WORDS = {"lol", "lmao", "lmfao", "haha", "hahaha", "hehe", "rofl", "hilarious", "funny",
               "jokes", "joking", "jk", "dead", "cracking", "laughing", "lolz", "hah"}
LAUGHTER = frozenset(lexicon.LAUGHTER)
SAYS_TOO_MUCH = re.compile(
    r"\b(?:too much|too many|a lot of|lots of|loads of|plenty of|glut of|bag of|bunch of"
    r"|punnet of|box of|kilo of|tin of)\s+\w+", re.I)
NO_WORDS = {"no", "nah", "nope", "not", "naw", "never"}
NO_REFUSAL_CONTENT = frozenset("""alright ok okay fine thanks thank cheers ta idea thing
    bother today tonight tomorrow yet now right later soon""".split())


NOT_A_REFUSAL = re.compile(
    r"^\W*not\s+(?:too\s+|very\s+|so\s+|feeling\s+|doing\s+)?"
    r"(?:well|good|great|ok|okay|brilliant|amazing|bad|right|myself)\b", re.I)


def _only_a_refusal(clean, tokens):
    if not any(t in NO_WORDS for t in tokens):
        return False
    if NOT_A_REFUSAL.match(clean):
        return False
    return not [word for word in _content_words(clean)
                if word not in NO_REFUSAL_CONTENT and word not in NO_WORDS]
A_MOOD_SAID_PLAINLY = frozenset("""awful terrible""".split())
A_VERDICT_WORD = frozenset("""rubbish crap crappy shit shitty terrible awful dreadful bad
    useless worthless hopeless stupid thick dumb fat ugly""".split())
A_VERDICT_WITH_A_ROLE = "|".join(sorted(A_VERDICT_WORD, key=len, reverse=True))
NOT_A_BARE_VERDICT = frozenset("waste mess wreck disaster".split())
A_VERDICT_SAID_ALONE = A_VERDICT_WORD | (facts.SELF_JUDGEMENT - NOT_A_BARE_VERDICT)
A_VERDICT_ON_ITS_OWN = "|".join(sorted(A_VERDICT_SAID_ALONE - A_MOOD_SAID_PLAINLY,
                                      key=len, reverse=True))
OWN_WORTH = re.compile(
    r"\b(?:not (?:good|smart|clever|thin|pretty|strong|nice) enough|never (?:good )?enough|"
    r"a waste of space|nothing i (?:do|say) is (?:ever )?right|"
    r"no good at anything|rubbish at everything|bad at everything|"
    r"(?:nobody|no one) (?:likes|wants|needs) me|everyone hates me|i ruin everything|"
    r"\bfeel(?:ing)? like (?:such |a bit of |a right |a total |a complete )?a "
    r"(?:failure|letdown|burden|waste|disappointment|idiot|fool|joke|mug|fraud)|"
    r"\bfeel(?:ing)? (?:so |really |pretty |very |like )?"
    r"(?:useless|worthless|stupid|thick|dumb|daft|clueless)\b|"
    r"^(?:im|i am|i m) (?:just |always |such |so |a bit |really |pretty |completely |totally )*"
    r"(?:a |such an? )?(?:(?:failure|letdown|burden|disappointment|joke|idiot|"
    r"useless|worthless|hopeless|nothing)\b"
    r"|waste(?=\s*(?:[.,!?]|$)|\s+of\b))|"
    r"\b(?:im|i am|i m)(?: (?:just|always|such|so|a bit|really|pretty|quite|completely|totally|"
    r"kind of|sort of))* (?:a |an |such an? )(?:" + A_VERDICT_WITH_A_ROLE + r")\b"
    r"(?!\s+at\b)|"
    r"\b(?:im|i am|i m)(?: (?:just|always|such|so|a bit|really|pretty|quite|completely|totally|"
    r"kind of|sort of))* (?:" + A_VERDICT_ON_ITS_OWN + r")\b(?!\s+at\b))")
OWN_TRAIT = re.compile(
    r"^(?:im|i'm|i am|i m)\s+(?:just |always |such |so |a bit |a bit of a |really |pretty |"
    r"quite |completely |totally |very |kind of |sort of )*(?:a |an |such an? )?(?:"
    + "|".join(sorted(lexicon.TRAITS, key=len, reverse=True)) + r")\b"
    r"(?!\s+[a-z]+\s+at\b)(?!\s+at\b)"
    r"(?:[,\s]+[a-z']+){0,3}\s*[.!?,]*$")
SOCIAL_TRAIT_SETTING = re.compile(
    r"\b(?:shy|awkward|nervous|timid|self[- ]conscious|anxious)\b[^.!?]{0,30}?"
    r"\b(?:with|around|near|meeting|talking\s+to|in\s+front\s+of)\s+(?:\w+\s+){0,2}"
    r"(?:people|strangers?|folk|others|anyone|someone\s+new)\b")
EVERYTHING_WRONG = re.compile(
    r"\b(?:"
    r"(?:do|does|doing|did|get|gets|getting|got)\s+"
    r"(?:everything|it all|all of it)\s+wrong"
    r"|"
    r"(?:can(?:t|not)|couldnt|never)\s+(?:do|get|make|does|gets|makes)\s+anything\s+right"
    r"|"
    r"can(?:t|not)\s+even\s+(?:do|get|make|say|keep)\s+(?:[a-z]+ ){0,3}"
    r"right(?![a-z])(?! (?:now|away|here|there|then)\b)"
    r"|"
    r"never\s+(?:finish|finishes|finishing|complete|completes)\s+"
    r"(?:anything|what i (?:start|begin|begin)|a thing|things)"
    r"|"
    r"(?:everything|anything)\s+(?:i|we)\s+"
    r"(?:do|did|say|said|make|made|touch|try|get)\s+"
    r"(?:is|was|goes|went|turns|turned)\s+(?:wrong|bad|badly)"
    r"|"
    r"nothing\s+(?:i|we)\s+(?:do|did|say|said|make|made|try|get)\s+"
    r"(?:is|was|goes|went|turns|turned)\s+right"
    r"|"
    r"mess(?:es|ed|ing)?\s+(?:everything|it all|all of it)\s+up"
    r")\b")

OWN_HARSH = re.compile(
    r"\bfeel(?:ing)? like (?:(?:im|i'?m|i am) )?"
    r"(?:such |a bit of |a bit like |kind of |a right |an? )?"
    r"(?:idiot|fraud|fool|mess|disaster|"
    r"bad (?:mum|mom|dad|mother|father|parent|person|friend|partner|husband|wife|son|daughter)|"
    r"(?:rubbish|terrible|awful|useless|hopeless) (?:mum|mom|dad|mother|father|parent|"
    r"person|friend|partner|husband|wife|son|daughter))\b"
    r"|\bfeel(?:ing)? like (?:(?:im|i'?m|i am) )?the worst (?:mum|mom|dad|mother|father|parent|"
    r"person|friend|partner|"
    r"husband|wife|son|daughter)(?: in the world)?\b"
    r"|\bfeel(?:ing)? like (?:im|i am|i m) (?:failing|useless|worthless|no good)\b"
    r"|\b(?:im|i am|i m) (?:just |such |a bit of |a right )*(?:an? )?"
    r"(?:idiot|fraud|fool|mess|disaster)\b"
    r"|\b(?:im|i am|i m)\s+"
    r"(?:also |just |such |quite |pretty |really |very |so |totally |completely |proper |fairly |"
    r"a bit of |a right )*"
    r"(?:an? )"
    r"(?:(?:pretty |quite |really |very |so |fairly |totally |completely |proper |right |"
    r"a bit of a |a bit |such a |kind of a ))*"
    r"(?:bad|terrible|awful|horrible|rubbish|rubbishy|useless|hopeless|lazy|selfish|stupid|lousy|"
    r"naff|rotten|dreadful|crap|crappy|crummy|shit|poor)"
    r"\s+(?!(?:lot|bit|deal|day|days|week|weekend|month|year|time|times|mood|thing|things|"
    r"while|way|ways|place|places|shape|state|condition|health|pain|pains|ache|nights?|"
    r"shame|pity|job)\b)[a-z]+\b")


LET_SOMEONE_DOWN = re.compile(
    r"\b(?:let|letting)\s+(?:everyone|everybody|people|myself|him|her|them|my\s+(?:mum|mom|"
    r"mother|dad|father|wife|husband|partner|son|daughter|kids?|children|family|friends?|"
    r"sister|brother|nan|gran|boss|team|mates?))\s+down\b"
    r"(?!\s+(?:gently|easy|easily|softly))",
    re.I)
KEEPS_FAILING = re.compile(
    r"\bkee(?:p|ps|ping)\s+(?:making\s+mistakes|failing|letting\s+(?:people|everyone)\s+down)\b",
    re.I)
NOT_THE_PERSONS_OWN = frozenset("""my our the his her their your a an this that these those
    it he she they""".split())
SELF_SUBJECT = frozenset("""i im i'm ive i've me myself we us""".split())


def _keeps_failing_theirs(clean):
    for match in KEEPS_FAILING.finditer(clean or ""):
        before = re.findall(r"[a-z']+", (clean or "")[:match.start()].lower())[-3:]
        if not any(word in NOT_THE_PERSONS_OWN for word in before):
            return match
        if any(word in SELF_SUBJECT for word in before):
            return match
    return None


def _letting_someone_down(clean):
    return LET_SOMEONE_DOWN.search(clean or "") or _keeps_failing_theirs(clean)
ROLE_YOU_CAN_FAIL = facts.ROLE_YOU_CAN_FAIL
NOT_FAIR = re.compile(
    r"\b(?:(?:not|isnt|wasnt|so|just|totally|really|bloody|damn) (?:so |really |just )?fair|unfair|"
    r"not fair at all|how is that fair)\b")
NOT_GREAT = re.compile(
    r"^(?:and |oh |well |honestly |tbh |to be honest |yeah |yes |god |urgh |ugh )*"
    r"(?:(?:that|thats|that s|this|this s|it|its|it s|life|today|work|everything|the day)"
    r"(?:\s+(?:is|isnt|was|wasnt|s))?\s+)?"
    r"(?:not|isnt|wasnt)(?:\s+(?:that|too|really|very|so|all that))?\s+"
    r"(?:great|good|ideal|ok|okay|fine|brilliant|well|right|myself|amazing)"
    r"(?:\s+(?:at all|honestly|tbh|to be honest|though|tho|really|either|today|this week))?[!. ]*$")

ASKS_A_QUESTION = {"is", "are", "was", "were", "am", "do", "does", "did", "can", "could",
                   "should", "would", "will", "shall", "may", "might", "how", "why", "what",
                   "when", "where", "who", "whose", "which", "isnt", "arent", "wasnt",
                   "werent", "doesnt", "didnt", "dont", "cant", "couldnt", "wouldnt",
                   "shouldnt"}


SELF_WORDS = frozenset(("i", "im", "me", "myself"))


def _about_themselves(tokens):
    if len(tokens) <= 4:
        return True
    return bool(SELF_WORDS & set(tokens))


FIRST_COPULA = frozenset(("i", "im", "i'm", "ive", "i've", "we", "we're", "were", "weve"))
LEAD_IN_JUDGEMENT = frozenset(("sorry", "so", "but", "and", "well", "oh", "yeah", "ya", "honestly",
                               "tbh", "actually", "really", "just", "no", "hi", "hey", "ok",
                               "okay", "right", "look", "god", "urgh", "ugh", "still"))
NOT_FAIR_WORDS = frozenset(("not", "never", "wasnt", "wasn't", "isnt", "isn't", "arent", "werent",
                            "weren't", "unfair", "unfairly", "being"))
OTHER_SUBJECT = frozenset(("it", "its", "it's", "that", "thats", "that's", "this", "life",
                           "everything", "work", "they", "he", "she", "people"))


def _themselves_unfair(tokens):
    for at, word in enumerate(tokens):
        if word not in ("fair", "unfair"):
            continue
        window = tokens[max(0, at - 4):at]
        while window and window[0] in LEAD_IN_JUDGEMENT:
            window = window[1:]
        if not window or window[0] not in FIRST_COPULA:
            continue
        if any(word in OTHER_SUBJECT for word in window[1:]):
            continue
        if word == "unfair" or any(item in NOT_FAIR_WORDS for item in window):
            return True
    return False
REACTION_WORDS = {
    "scary": "fear", "frightening": "fear", "terrifying": "fear", "worrying": "fear",
    "unsettling": "fear", "daunting": "fear", "petrifying": "fear", "horrifying": "fear",
    "grim": "bad", "awful": "bad", "horrible": "bad", "dreadful": "bad",
    "terrible": "bad", "tough": "bad", "rough": "bad", "rubbish": "bad",
    "gutting": "bad", "sad": "bad", "devastating": "bad", "heartbreaking": "bad",
    "shit": "bad", "crap": "bad", "brutal": "bad",
    "annoying": "annoyed", "frustrating": "annoyed", "irritating": "annoyed",
    "infuriating": "annoyed", "maddening": "annoyed",
    "exhausting": "tired", "exhausted": "tired", "knackering": "tired", "draining": "tired",
    "great": "good", "brilliant": "good", "amazing": "good", "lovely": "good",
    "wonderful": "good", "fantastic": "good", "excellent": "good", "superb": "good",
    "ace": "good", "exciting": "good", "good": "good", "nice": "good", "cool": "good",
    "perfect": "good", "ideal": "good", "handy": "good", "useful": "good", "helpful": "good",
    "funny": "funny", "hilarious": "funny",
}
REACTION_WHAT_A = {
    "blow": "bad", "shame": "bad", "pity": "bad", "nightmare": "bad", "disaster": "bad",
    "mess": "bad", "tragedy": "bad", "horror": "bad", "letdown": "bad", "downer": "bad",
    "bummer": "bad", "state": "bad", "joke": "bad", "slog": "bad", "carry on": "bad",
    "shock": "fear", "scare": "fear", "fright": "fear",
    "relief": "good", "result": "good", "find": "good", "bargain": "good", "treat": "good",
}
REACTION_LEAD = frozenset("""oh ah god jesus christ yeah yep yup honestly well and but blimey
bloody hell damn wow urgh ugh man mate really just so proper fucking""".split())
REACTION_TAIL = frozenset("""though tho honestly tbh really stuff mate isnt it hey eh""".split())
REACTION_SUBJECT = frozenset("that thats this it its".split())
REACTION_COPULA = frozenset("is was s sounds seems feels look looks".split())
REACTION_HOW = frozenset("how so very proper pretty really that that s thats".split())
REACTION_SIGH = frozenset("oh aw ah ooh".split())
REACTION_SIGH_WORD = frozenset("""no dear god christ jesus jeez jaysus hell help
nasty bugger blimey""".split())
REACTION_BARE_GOOD = frozenset("""lovely brilliant great amazing fantastic wonderful excellent
superb ace fab smashing magic perfect marvellous marvelous cracking
terrific""".split())
REACTION_BARE_FUNNY = frozenset("hilarious funny hysterical".split())


def _the_answer_met_it_as_news(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in reversed([t for t in (turns or []) if isinstance(t, dict)]):
        line = str(turn.get("bot") or "")
        if line:
            return bool(SORRY_MET.search(line) or NEWS_MET.search(line))
    return False


def _a_loss_before(said, memory=None):
    try:
        turns = memory.get("turns") if isinstance(memory, dict) else None
        last = [turn for turn in (turns or []) if isinstance(turn, dict)]
        if last:
            module = str(last[-1].get("module") or "")
            if module:
                return module in NEWS_MODULES
        if loss_reading.reads_as_loss(said) or loss_reading.a_pet_died(said):
            return True
        return bool(badnews.reads_as_sudden_loss(said))
    except Exception:
        return False


def _a_thread_to_come_back_to(memory):
    return thread.earlier_turn(memory)


def _news_before(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    said = [turn for turn in (turns or []) if isinstance(turn, dict)]
    return str((said[-1].get("user") if said else "") or "").lower()


def _nobody_would_call_it_nice(said):
    if not said:
        return False
    return bool(loss_reading.reads_as_loss(said) or loss_reading.a_pet_died(said)
                or badnews.reads_as_sudden_loss(said) or reads_as_bad_news(said))


REACTION_CHEERFUL = frozenset({"react_good", "react_funny"})


AGREEMENT_ONLY = re.compile(
    r"^(?:yeah |yep |ha |haha |oh |aw )?"
    r"(?:me too|me as well|me neither|same here|same as me|so am i|so do i|so can i|so have i|\s*"
    r"so did i|so would i|nor me|neither do i|neither am i|us too|us both|you and me both|\s*"
    r"join the club|welcome to my world|i know right)"
    r"(?: then| too| as well| honestly| actually| indeed)?[\s.,!?]*$", re.I)
GRUMBLE = re.compile(
    r"\b(?:shattered|knackered|exhausted|wiped out|tired|fed up|sick of|hate|hates|cant stand|\s*"
    r"can't stand|doing my head in|does my head in|driving me mad|killing me|hurts|hurting|aching|\s*"
    r"aches|freezing|so cold|pouring|rained off|long day|rough day|grim|awful|rubbish|dreadful|\s*"
    r"nightmare|worn out|drained|stressed|worried|skint|broke|bored|lonely|struggling|\s*"
    r"not great|not good|not brilliant|not the best|no fun|a nightmare|hard work)\b", re.I)


WEATHER = re.compile(
    r"\b(?:cold|freezing|freezing cold|chilly|frost|snow|snowing|rain|raining|pouring|wet|wind|"
    r"windy|storm|heat|hot|boiling|muggy|humid|sticky|damp|dark|grey|gloomy|pollen|hay ?fever|"
    r"weather|summer|winter|autumn|spring|mornings|evenings)\b", re.I)


def _the_agreement_pool(memory):
    said = _news_before(memory)
    if not said:
        return None
    if _safety_thread(memory):
        return None
    if (loss_reading.reads_as_loss(said) or loss_reading.a_pet_died(said)
            or badnews.reads_as_sudden_loss(said)):
        return "agree_loss"
    if reads_as_good_news(said) or reads_as_a_pass(said):
        return "agree_good"
    if reads_as_bad_news(said) or GRUMBLE.search(said):
        if WEATHER.search(said):
            return "agree_weather"
        return "agree_grim"
    return "agree_plain"


def _reaction(clean, tokens, memory):
    pool = _reaction_pool(clean, tokens, memory)
    if pool in REACTION_CHEERFUL and _nobody_would_call_it_nice(_news_before(memory)):
        return "react_sigh"
    return pool


def _reaction_pool(clean, tokens, memory):
    if "?" in clean or not tokens or len(tokens) > 7:
        return None
    if not [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]:
        return None
    try:
        if reading_reply.judges_a_figure(clean, memory):
            return None
    except Exception:
        pass
    words = [word.strip(".,!?;:") for word in tokens]
    while len(words) > 2 and words[0] in REACTION_LEAD:
        words.pop(0)
    while words and words[-1] in REACTION_TAIL:
        words.pop()
    if not words:
        return None
    if AGREEMENT_ONLY.match(clean):
        return _the_agreement_pool(memory)
    if len(words) in (3, 4) and words[0] == "what" and words[1] in ("a", "an"):
        rest = words[2:]
        while rest and rest[0] in {"bloody", "right", "proper", "total", "absolute", "real",
                                   "complete", "utter", "such"}:
            rest = rest[1:]
        thing = " ".join(rest)
        if thing in REACTION_WHAT_A:
            said = _news_before(memory)
            kind = REACTION_WHAT_A[thing]
            if kind == "good":
                if said and reads_as_good_news(said):
                    return "react_good"
                return None
            if said and not _a_loss_before(said, memory) and _the_answer_met_it_as_news(memory):
                return "react_" + kind
        return None
    if len(words) == 2 and words[0] in REACTION_HOW and words[1] in REACTION_WORDS:
        return "react_" + REACTION_WORDS[words[1]]
    if len(words) <= 3 and words[0] in REACTION_SIGH and all(
            word in REACTION_SIGH_WORD for word in words[1:]):
        return "react_sigh"
    said = _news_before(memory)
    if len(words) <= 2 and all(word in REACTION_BARE_GOOD for word in words):
        if said and reads_as_good_news(said):
            return "react_good"
        if said and _nobody_would_call_it_nice(said):
            return "react_sigh"
        return None
    if len(words) <= 2 and all(word in REACTION_BARE_FUNNY for word in words):
        return "react_funny"
    if words[0] in REACTION_SUBJECT:
        rest = words[1:]
        while rest and rest[0] in REACTION_COPULA:
            rest = rest[1:]
        while rest and rest[0] in {"so", "really", "very", "proper", "well"}:
            rest = rest[1:]
        if len(rest) == 1 and rest[0] in REACTION_WORDS:
            return "react_" + REACTION_WORDS[rest[0]]
        if rest == ["a", "lot"] or rest == ["a", "hell", "of", "a", "lot"]:
            return "react_bad"
    return None


GOOD_NEWS_TURN = re.compile(r"\b(?:but|though|although|except)\b(.*)$", re.I)
OWN_WIN = re.compile(r"\b(?:i|we)\s+(?:still |actually |finally |eventually |just |also )?"
                     r"(?:did it(?! again)|managed it|managed to|got through it|made it|"
                     r"got there|won|passed)\b"
                     r"|\b(?:i|we)\s+(?:got|landed)\s+(?:the|a|my|our)\s+"
                     r"(?:job|promotion|offer|pay rise|raise|place|role|part)\b", re.I)
OWN_SETBACK = re.compile(r"\b(?:i|we)\s+(?:just |still |actually |probably |really )?"
                         r"(?:failed|messed it up|messed up|did it again|blew it)\b", re.I)


def _turns_on_news(clean):
    if (reads_as_a_pass(clean) or reads_as_good_news(clean) or OWN_WIN.search(clean)
            or OWN_SETBACK.search(clean) or reads_as_bad_news(clean)):
        return True
    for match in GOOD_NEWS_TURN.finditer(clean):
        tail = match.group(1)
        if (reads_as_a_pass(tail) or reads_as_good_news(tail) or OWN_WIN.search(tail)
                or OWN_SETBACK.search(tail) or reads_as_bad_news(tail)):
            return True
    return False

ASKED_AFTER = re.compile(
    r"\b(?:how (?:do|can|should|would|could) i|how do you|should i|shall i|"
    r"do i need|what should i|which should i|what exercise|what can i do about|"
    r"what would you (?:do|suggest|recommend)|any (?:advice|tips)|advice on|tips on)\b")


def _asks_after(clean, judged):
    ask = ASKED_AFTER.search(clean)
    return bool(ask and ask.start() > judged.end())


JUDGEMENT_TIME = frozenset("""weekend weekends night nights day days morning mornings evening
evenings afternoon afternoons monday tuesday wednesday thursday friday saturday sunday
summer winter christmas""".split())
SELF_COPULA = frozenset(("im", "i'm", "i am"))


def _judged_as_a_noun(tokens):
    for at, word in enumerate(tokens):
        if word not in JUDGEMENT_NOUNS:
            continue
        before = tokens[max(0, at - 4):at]
        if not any(item in SELF_COPULA for item in before):
            if not (any(item in ("life", "everything", "it") for item in before)
                    and "is" in before):
                continue
        if not any(item in ("a", "an", "the") for item in before):
            continue
        if any(item in ("not", "never", "no") for item in before):
            continue
        after = tokens[at + 1:at + 2]
        if after and after[0] not in JUDGEMENT_AFTER:
            continue
        if _when_not_why(tokens[at + 1:]):
            continue
        return True


def _when_not_why(rest):
    if len(rest) < 2 or rest[0] not in ("at", "on", "after", "before", "during", "every"):
        return False
    named = [word for word in rest[1:] if word not in ("the", "a", "an")]
    return bool(named) and (named[0] in JUDGEMENT_TIME or named[0][:-1] in JUDGEMENT_TIME)
HARSH_WORDS = frozenset("""
bad terrible awful horrible rubbish rubbishy useless hopeless lazy selfish stupid lousy naff
rotten dreadful crap crappy crummy shit poor
""".split())


def _judged_a_role(clean):
    match = OWN_HARSH.search(clean or "")
    if not match:
        return True
    words = re.findall(r"[a-z']+", match.group(0).lower())
    for index, word in enumerate(words):
        if word in HARSH_WORDS and index + 1 < len(words):
            return words[index + 1] in ROLE_YOU_CAN_FAIL
    return True


def _judgement(clean, tokens):
    if "?" in clean or len(tokens) > 14 or (tokens and tokens[0] in ASKS_A_QUESTION):
        return None
    if said_about_me.reads_as_somebody_elses_words(clean.replace("'", "")):
        return None
    if _feel_like(clean) not in (None, "feel_like"):
        return None
    if OWN_HARSH.search(clean) and _about_themselves(tokens):
        return "own_harsh" if _judged_a_role(clean) else "own_described"
    judged = (OWN_WORTH.search(clean) or (OWN_TRAIT.search(clean)
                                          and not SOCIAL_TRAIT_SETTING.search(clean))
              or EVERYTHING_WRONG.search(clean)
              or topics.reads_as_unfit(clean) or _letting_someone_down(clean))
    if not (judged and _asks_after(clean, judged)):
        if _judged_as_a_noun(tokens):
            return "not_enough"
        if judged and _about_themselves(tokens) and not _turns_on_news(clean):
            return "not_enough"
    if NOT_FAIR.search(clean):
        if _themselves_unfair(tokens):
            return "own_fault"
        return "not_fair"
    if len(tokens) <= 8 and NOT_GREAT.search(clean):
        return "not_great"
    return None


DONT_KNOW_WORDS = {"idk", "dunno", "dont", "know", "not", "sure", "maybe", "unsure"}

BYE_CORE = {"bye", "byebye", "goodbye", "goodnight", "night", "cya", "cheerio", "later",
            "toodles", "nightnight"}
BYE_FILLER = {"bye", "byebye", "goodbye", "goodnight", "night", "cya", "cheerio", "later",
              "need", "must", "anyway", "off", "going", "heading", "leaving", "soon",
              "im", "to", "cool", "so", "then", "now", "bed",
              "toodles", "nightnight", "see", "you", "u", "ya", "soon", "then", "now", "all",
              "everyone", "good", "take", "care", "ok", "thanks", "thx", "cheers", "for",
              "help", "the", "and", "i", "gotta", "go", "off", "got", "to", "sleep", "bed",
              "morning", "mate", "folks", "guys", "have", "nice", "one", "day", "speak",
              "right", "alright", "ha", "haha", "fair", "enough", "well", "talk", "catch",
              "tomorrow", "ill", "lets",
              "lol", "lmao", "rofl", "yeah", "yep", "yup", "okay", "kk", "ah", "oh",
              "hmm", "mm", "anyways", "anyhoo", "gonna", "gunna",
              "x", "xx", "xxx",
              "head", "back", "in", "a", "bit", "sec", "mo", "min", "minute", "shortly",
              "sweet", "dreams", "out", "let", "am"}
BYE_FILLER |= LAUGH_WORDS
BYE_TIME = {"soon", "later", "tomorrow", "bit", "mo", "sec", "min", "minute", "shortly"}
BYE_VERB = {"talk", "speak", "catch", "see"}

SMILES = {":)": " smile ", ":-)": " smile ", ":(": " sad ", ":-(": " sad ", "<3": " love ",
          ":d": " haha ", ";-)": " wink ", "; )": " wink ", ":/": " meh ", ":|": " meh "}

JOKE_ASK = re.compile(
    r"\b(tell|give|know|got|say|hear)\b[^.!?]{0,25}\bjokes?\b|\bmake me laugh\b|"
    r"\bsomething funny\b|\bcheer me up\b|^joke\b")
JOKE_ASKED = re.compile(r"\bjokes?\b|\bmake me laugh\b|\bcheer me up\b|\bpun\b|\bridge\b")
RUNTIME_LIMIT = re.compile(
    r"\b(?:under|less than|no longer than|shorter than|max|at most)\s+"
    r"(?:\d{1,3}\s*(?:min|mins|minutes?|hours?|hrs?)\b|an? hour\b|two hours\b|"
    r"three hours\b|half an hour\b|an? hour and a half\b)"
    r"|\b(?:but|and|that is|thats) short\b|\b(?:isnt|is not) (?:too )?long\b",
    re.IGNORECASE)
JOKE_ADVICE = re.compile(
    r"\b(?:should (?:i|we)|shall i|is it|is that|are they|would it|will it|do you think|"
    r"what about|wot about|how about)\b[^.!?]{0,30}\bjokes?\b|"
    r"\bjokes?\b[^.!?]{0,30}\b(?:risky|appropriate|a good idea|too risky|worth it|land|"
    r"offend|offensive|rude|safe|ok|okay|fine|alright|allowed)\b")

PICK_WORDS = frozenset("""
    watch watching watched film films movie movies cinema show shows series episode netflix
    telly tv boxset sitcom standup stand comedy read reading book books novel novels audiobook
    listen listening podcast podcasts album albums music playlist gig
""".split())

WANTS_A_THING = re.compile(
    r"\b(?:in the mood|in a mood|mood for|fancy|fancied|want|wanted|feel like|feeling like|"
    r"up for|something to|after a|after some)\b")
ASKS_ALOUD = re.compile(
    r"\b(?:tell|say|give|got|hear|make me laugh|cheer me up|another|one more)\b")

JOKES = {
    "cheese": "What do you call cheese that isn't yours? Nacho cheese.",
    "fish": "Why don't fish play tennis? They're scared of the net.",
    "dog": "Why did the dog sit in the shade? He didn't want to be a hot dog.",
    "cat": "What do you call a cat that swallowed a lemon? A sourpuss.",
    "computer": "Why do programmers prefer dark mode? Because light attracts bugs.",
    "book": "I'm reading a book about anti-gravity. It's impossible to put down.",
    "music": "Why did the musician get arrested? For drumming up business.",
    "work": "I told my boss I needed a break. He said I'd only been there five minutes. I said yes, but it felt like hours.",
    "egg": "Why don't eggs tell jokes? They'd crack each other up.",
    "food": "What do you call a fake noodle? An impasta.",
    "car": "Why did the bicycle fall over? It was two-tired.",
    "animal": "How does a penguin build its house? Igloos it together.",
}
SHORT_JOKES = (
    "Why don't scientists trust atoms? They make up everything.",
    "I used to be a banker, but I lost interest.",
    "Why did the scarecrow win an award? He was outstanding in his field.",
    "I only know 25 letters of the alphabet. I don't know y.",
    "What's orange and sounds like a parrot? A carrot.",
    "I'd tell you a construction joke, but I'm still working on it.",
    "What do you call a sleeping bull? A bulldozer.",
    "Why did the golfer wear two pairs of trousers? In case he got a hole in one.",
)

ROLE_STOP = {"bit", "little", "lot", "mess", "fan", "big", "huge", "total", "complete", "real",
             "very", "so", "really", "grown", "vegetarian", "vegan", "good", "bad", "terrible",
             "great", "wreck", "disaster", "beginner", "bit", "nobody", "nothing", "failure",
             "loser", "idiot", "muppet", "moron", "fool", "clown",
             "burden", "joke", "doormat", "letdown", "disappointment", "waste", "problem",
             "mistake", "nuisance", "embarrassment", "fraud", "imposter", "impostor",
             "hypocrite", "rubbish", "crap", "crappy", "shit", "shitty",
             "awful", "dreadful", "useless", "worthless", "hopeless", "stupid",
             "thick", "dumb", "fat", "ugly"}
COMPARED_ROLE = re.compile(r"\b(?:feel|feels|felt|feeling|make|makes|made|like)\s+"
                           r"(?:like\s+)?(?:im|i am|i'm|me|myself|being)\b")
ROLE_TO_PEOPLE = re.compile(r"\bto (?:everyone|everybody|anyone|anybody|people|them|him|her|"
                            r"family|the family|everyone else|my \w+)\b")
ROLE = re.compile(r"\bim an? ([a-z]+(?: [a-z]+){0,2}?)(?: in ([a-z]+(?: [a-z]+){0,2}))?\s*$")
ROLE_WORK = re.compile(r"\bi work as an? ([a-z]+(?: [a-z]+){0,2}?)\s*$")
NOT_A_ROLE_AFTER_ARTICLE = (
    r"half\b|quarter\b|bit\b|months?\b|years?\b|weeks?\b|days?\b|hours?\b|stone\b|"
    r"kilos?\b|kgs?\b|pounds?\b|lbs\b|size\b|inches\b|centimet\w*\b|feet\b|foot\b|"
    r"miles?\b|minutes?\b")
AGE_BEFORE_A_ROLE = re.compile(
    r"\b(?:im|i am)\s+\d{1,3}\s*(?:,\s*|and\s+|,\s*and\s+)?"
    r"(?=an?\s+(?!(?:" + NOT_A_ROLE_AFTER_ARTICLE + r")))")
PLAIN_TAIL = (r"(?:\s+(?:at the moment|right now|these days|currently|for now|now|still|tbh|"
              r"to be honest|since\s+\w{3,9}|for\s+(?:a\s+|the\s+)?(?:few\s+|couple of\s+)?"
              r"\w{3,9}))*\s*[.!]*$")
OUT_OF_WORK = re.compile(
    r"\b(?:im|i am|ive|i have|i)(?:\s+been)?\s+(?:currently\s+|still\s+|now\s+|just\s+)?"
    r"(?:between jobs|out of work|unemployed|jobless|job hunting|looking for work|"
    r"looking for a job|on the dole)\b" + PLAIN_TAIL, re.I)
RETIRED = re.compile(
    r"\b(?:im|i am|ive|i have|i)\s+(?:\d{1,3}\s*(?:,\s*|and\s+|,\s*and\s+)?)?"
    r"(?:just\s+|now\s+|recently\s+|finally\s+)?retired\b"
    r"(?:\s+(?:last|this|early|in|at|from|after|since|years?|now|and)\b[^?.!]*|"
    + PLAIN_TAIL + r")", re.I)

RETIRED_ASKING = re.compile(
    r"\b(lost|at a loss|struggl\w*|bored|boredom|lonely|loneliness|miss|missing|adjust\w*|"
    r"get used to|cope|coping|normal|strange|odd|weird|purpose|structure|nothing to do|"
    r"keep busy|keep occupied|with myself|how do i|what (?:do i|to|do people) do|what now)\b")
PLACE = re.compile(
    r"(?:^\s*were\b|\b(?:i|im|i'm|ive|i've|id|i'd|ill|i'll|i am|i have|we|we're|we re|weve|"
    r"we've|we'd|we am|we have))\s+"
    r"(?:just\s+|recently\s+|finally\s+|already\s+|now\s+)?"
    r"(?:(?:live|living|lives|moved|moving|settled|settling|based|relocat\w+)"
    r"\s+(?:(?:up|back|over|out|down|away)\s+)?(?:in|to)(?!\s+(?:with|as|for)\b)"
    r"|grew\s+up\s+in|from)\s+([a-z][a-z' -]{1,25})")
PLACE_TAIL = tuple(re.compile(tail) for tail in (
    r"\s+(?:last|this|next)\s+(?:year|month|week|summer|winter|spring|autumn|christmas)\b.*$",
    r"\s+(?:a|an|one|two|three|four|five|six|seven|eight|nine|ten|a few|several|many|\d+)\s+"
    r"years?\s+ago\b.*$",
    r"\s+years?\s+ago\b.*$",
    r"\s+a\s+while\s+ago\b.*$",
    r"\s+since\s+(?:\d{4}|\w+)\b.*$",
    r"\s+in\s+(?:\d{4}\b|\d{1,2}\s+\w+|the\s+(?:summer|winter|spring|autumn|new year)\b"
    r"|(?:january|february|march|april|may|june|july|august|september|october|november"
    r"|december)\b).*$",
    r"\s+(?:originally|now|still|before|previously|currently|already|again|then|recently)\b.*$",
    r"\s+(?:at|for)\s+the\s+(?:moment|minute|time being)\b.*$",
    r"\s+(?:these days|right now|just now)\b.*$",
    r"\s+for\s+\w+.*$",
    r"\s+(?:with|and|but|because|so|as|too|which|when i|after)\b.*$",
    r"\s+(?:when|where|why|how|what|which|who|whose|whom)\b.*$",
    r"\s+(?:in|on|at|by|from)\s+(?:about\s+|around\s+|roughly\s+|just\s+over\s+|nearly\s+)?"
    r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|a|an|a\s+few|"
    r"a\s+couple\s+of|several)\s+(?:hours?|days?|weeks?|fortnights?|months?|years?)\b.*$",
))
PLACE_MOST = 4
PLACE_LAST = re.compile(r"^.*\bin\s+([a-z][a-z' -]*)$")
PLACE_IDIOM = frozenset(("hope", "fear", "sin", "pain", "denial", "the past", "the moment",
                         "the dark", "a bubble", "cloud cuckoo land", "the middle of nowhere"))
PLACE_SPAN = re.compile(
    r"^(?:about\s+|around\s+|roughly\s+|just\s+over\s+|nearly\s+|almost\s+)?"
    r"(?:(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|a|an|a\s+few|"
    r"a\s+couple\s+of|several|the)\s+)?"
    r"(?:hours?|days?|weeks?|fortnights?|months?|weekends?|years?|bit|while|minute|minutes)"
    r"(?:'?s\s+time|\s+time)?(?:\s+or\s+so|\s+from\s+now)?$"
    r"|^(?:january|february|march|april|may|june|july|august|september|october|november|"
    r"december|christmas|easter|the\s+weekend)$")
PLACE_NONE = frozenset({"", "holiday", "a holiday", "the holiday"})
PLACE_POINTS = frozenset("""a an the this that these those my our their his her its some any
another each every no""".split())
GROWN_IN = re.compile(r"\bgrew up in\b|\bbrought up in\b|\braised in\b")
PLACE_POSITION = frozenset(("upstairs", "downstairs", "inside", "outside", "indoors", "outdoors",
                            "here", "there", "abroad", "away"))
PLACE_NOBODY = re.compile(
    r"^(?:(?:a|an|the|my|our|their|his|her)\s+(?:new|different|other|another|old|same|"
    r"whole|nice|cool|good)\s+(?:place|city|town|flat|area|home|one))\b"
    r"|^(?:yesterday|today|tomorrow|tonight|now|soon|here|there|properly|recently|already|"
    r"by myself|on my own)\b"
    r"|^(?:last|this|next|the other)\s+(?:week|month|year|weekend|night|summer|winter|"
    r"spring|autumn|time|one)\b")
AWAY_WORDS = re.compile(r"\bfrom (?:a |the |our |my )?(?:holiday|holidays|vacation|trip|break|"
                        r"week away|weekend away)\b")
MOVING = re.compile(r"\b(?:moving|relocating|relocate|relocation)\b")
PLACE_THING_OPENS = re.compile(r"^(?:a|an|the|my|our|his|her|their|this|that)\b", re.I)
PLACE_TIME = re.compile(
    r"\s+(?:in|on|at)\s+(?:the\s+)?(?:january|february|march|april|may|june|july|august|"
    r"september|october|november|december|jan|feb|mar|apr|jun|jul|aug|sept?|oct|nov|dec|"
    r"monday|tuesday|wednesday|thursday|friday|saturday|sunday|"
    r"morning|afternoon|evening|night|weekend|weekends|spring|summer|autumn|winter|fall|"
    r"christmas|easter|half\s+term)\b.*$", re.I)
PLACE_TIME_OPENS = re.compile(
    r"^(?:in|on|at)\s+(?:the\s+)?(?:january|february|march|april|may|june|july|august|"
    r"september|october|november|december|jan|feb|mar|apr|jun|jul|aug|sept?|oct|nov|dec|"
    r"monday|tuesday|wednesday|thursday|friday|saturday|sunday|"
    r"morning|afternoon|evening|night|weekend|weekends|spring|summer|autumn|winter|fall|"
    r"christmas|easter|half\s+term|\d)\b", re.I)
TRIP = re.compile(r"\b(?:(?:just )?(?:got back|im back|we re back))(?: from (?:a |the |our |my )?"
                  r"(?:holiday|holidays|vacation|trip|break|weekend away|week away))?\s*$")
PET_ANIMALS = r"(puppy|dog|cat|kitten|rabbit|hamster|parrot|horse|snake|lizard|guinea pig|fish)"
PET = re.compile(r"\b(?:ive got|i have got|i have|i got|weve got|we have|we got|i adopted|"
                 r"we adopted|i rescued|we rescued) an? (?:(?:rescue|new|little|baby) )*"
                 + PET_ANIMALS + r"\b")
PET_ANY = re.compile(r"\b" + PET_ANIMALS + r"\b")
GOOD_NEWS = (
    re.compile(r"\b(came out|turned out|went)\s+(great|well|brilliant|perfect|nicely|"
               r"better than|lovely)\b"),
    re.compile(r"\bi (won|nailed it|got the job|got in|got the place|"
               r"got the all clear)\b"),
    re.compile(r"\bwe (won|got it|did it)\b"),
    re.compile(r"\b(?:i|we) (?:got|have got) the (?:house|flat)\b"
               r"(?!\s*(?:valued|surveyed|painted|cleaned|checked|tested|insured|keys|key))"),
    re.compile(r"\b(?:scan|results?|tests?) (?:came back|come back|came out|was|is) clear\b"),
    re.compile(r"\b(the kids|everyone|the family|they) loved it\b"),
    re.compile(r"\bshe said yes\b|\bwe re having a baby\b|\bim having a baby\b"),
)
LOST_JOB = re.compile(r"\b(?:(?:i|we)\s+)?lost (?:the|my|our|that|this) (?:job|work|role|"
                      r"position|contract|shift|hours|offer|placement|promotion|"
                      r"apprenticeship|client|deal|bid|order|tender)\b")
def _a_job_that_went(said):
    return bool(LOST_JOB.search(said) or badnews.reads_as_a_sacking(said))


JOB_STEP_ASK = re.compile(
    r"^\W*(?:(?:and|but|so|well|oh|ok|okay|right|then|now|yeah)\s+)*"
    r"(?:now\s+what(?:\s+do\s+i\s+do)?|what\s+now|what\s+happens\s+now)"
    r"(?:\s+(?:then|now|next|though|tho|about\s+(?:that|it|this)))?\s*(?:\?|\.|!)*\s*$", re.I)


def _the_ask_after_a_job_that_went(clean, memory):
    if not isinstance(memory, dict) or not JOB_STEP_ASK.match(str(clean or "").strip()):
        return None
    turns = [t for t in (memory.get("turns") or [])[-3:] if isinstance(t, dict)]
    for turn in reversed(turns):
        said = " ".join(str(turn.get("user") or "").lower().split())
        if not said:
            continue
        if _a_job_that_went(said):
            return pick(list(stuck_line.JOB), memory, clean)
        if len(said.split()) > 2:
            return None
    return None

LOST_WEIGHT = re.compile(r"\b(?:i|ive|i have) lost (?:half a stone|a stone|"
                         r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s*"
                         r"(?:kilos?|kg|pounds?|lbs?|stone)|"
                         r"(?:some|a lot of) weight|weight)\b")
BAD_NEWS = (
    re.compile(r"\b(didn't|didnt|did not) (get|make|pass|win)\b"),
    re.compile(r"\b(turned me down|turned us down|got rejected|got turned down|rejected)\b"),
    re.compile(r"\bi (failed|didn't pass|didnt pass)\b"),
    re.compile(r"\bwe lost (?:the|our) (?:contract|client|deal|bid|job|order|tender)\b"),
    re.compile(r"\b(she|he|they) said no\b(?!\s+(?!(?:way|chance|deal|thanks|thank|worries|"
               r"problem|dice|objection|to|about|on|again|twice|either|yet|at|for|so|and|but|"
               r"then|though|after|before|last|this|it|because|when|until|unless)\b)[a-z])"),
    re.compile(r"\bgot (cancelled|canceled|postponed)\b"),
)
TIME_COUNT = (r"(?:(?:a few|a couple of|a pair of|several|many|one|two|three|four|five|six|"
              r"seven|eight|nine|ten|a dozen|\d+)\s+)?")
WHEN_DONE = (r"(?:last night|last weekend|last (?:mon|tues|wednes|thurs|fri|satur|sun)day|"
             r"yesterday|the other night|the other day|at the weekend|over the weekend|"
             r"this morning|this afternoon|this evening|yesterday evening|yesterday afternoon|"
             r"at lunchtime|before work|after work|last week|last month|"
             r"on (?:mon|tues|wednes|thurs|fri|satur|sun)day(?: night)?|"
             r"last (?:year|summer|winter|spring|autumn|fall|christmas|new year)|"
             + TIME_COUNT + r"(?:years|months|weeks|days)\s+ago|"
             r"(?:back )?in (?:19|20)\d\d|when i was (?:a kid|a child|little|young|small|"
             r"at school|\d+))")
WITH_COMPANY = (r"with (?:(?:my|our|his|her|their|the)\s+[a-z][a-z' -]{1,24}|friends?|family|"
                r"a friend|some friends|a mate|mates)")
WENT_TO = re.compile(r"\b(?:i|we)\s+(?:went|popped|nipped|headed|took (?:us|my [a-z]+ and me))"
                     r"\s+(?:out\s+)?(?:to|for)\s+((?:(?:the|a|an|my|our|his|her|their)\s+)?"
                     r"[a-z][a-z' -]{1,26}?)\s+" + WHEN_DONE + r"\b")
WENT_TO_COMPANY = re.compile(
    r"\b(?:i|we)\s+(?:went|popped|nipped|headed|took (?:us|my [a-z]+ and me))"
    r"\s+(?:out\s+)?(?:to|for)\s+((?:(?:the|a|an|my|our|his|her|their)\s+)?"
    r"[a-z][a-z' -]{1,26}?)\s+" + WITH_COMPANY + r"\s*[.!]?\s*$")
WENT_TO_SEE = re.compile(r"\b(?:i|we)\s+(?:(?:went|popped|nipped|headed)\s+(?:out\s+)?to\s+"
                         r"(?:see|watch)|watched|saw)\s+((?:(?:the|a|an)\s+)?[a-z][a-z' -]{1,20}?)"
                         r"\s+" + WHEN_DONE + r"\b")
WENT_TO_SEE_COMPANY = re.compile(
    r"\b(?:i|we)\s+(?:(?:went|popped|nipped|headed)\s+(?:out\s+)?to\s+"
    r"(?:see|watch)|watched|saw)\s+((?:(?:the|a|an)\s+)?[a-z][a-z' -]{1,20}?)"
    r"\s+" + WITH_COMPANY + r"\s*[.!]?\s*$")
WATCHED_THINGS = frozenset(("film", "films", "movie", "match", "game", "show", "play",
                            "gig", "concert", "band", "comedy", "comedian", "exhibition",
                            "opera", "musical", "football", "rugby", "cricket", "boxing",
                            "darts", "tennis", "grand prix", "race", "races", "ballet",
                            "documentary", "documentaries", "series", "episode", "box set"))
WATCHED_DESCRIBER = frozenset(("good", "great", "brilliant", "lovely", "decent", "nice", "fine",
                               "really", "very", "quite", "proper", "properly", "actually",
                               "amazing", "excellent", "fantastic", "wonderful", "classic", "old",
                               "new", "funny", "sad", "scary", "weird", "long", "short", "whole",
                               "boring", "rubbish", "terrible", "awful", "bad", "poor", "dull",
                               "slow", "foreign", "animated", "local", "little", "small", "big"))
SAID_POOR = frozenset(("awful", "terrible", "rubbish", "crap", "boring", "dull",
                       "dreadful", "disappointing", "overpriced", "soulless", "meh"))
NOT_A_NIGHT_OUT = frozenset(("hospital", "a and e", "a&e", "ae", "casualty", "doctor",
                            "doctors", "gp", "dentist", "funeral", "court", "police",
                            "station", "prison", "cemetery", "crematorium", "care home",
                            "hospice", "morgue", "walk in centre", "bed", "sleep", "work",
                            "loo", "toilet", "bathroom", "shop", "shops",
                            "gym", "school", "uni", "college", "nursery", "class", "church",
                            "bank", "banks", "post office", "chemist", "pharmacy", "atm",
                            "cashpoint", "supermarket", "supermarkets",
                            "a e", "a and e department",
                            "and e", "and e department"))
def _not_a_night_out(place):
    low = " ".join(place.lower().replace("&", " and ").split())
    if low in NOT_A_NIGHT_OUT:
        return True
    bare = " ".join(w for w in low.split() if w not in {"the", "a", "an"})
    return bare in NOT_A_NIGHT_OUT or bool(bare) and bare.split()[0] in NOT_A_NIGHT_OUT


NOT_A_PLACE_START = frozenset(("see", "watch", "visit", "meet", "pick", "collect", "get", "buy",
                               "look", "check", "drop", "deliver", "take", "fetch", "have",
                               "eat", "drink", "play", "do", "make", "book", "pay", "sort"))
WENT_WRONG = re.compile(r"\b(?:awful|terrible|rubbish|crap|shit|shite|ruined|boring|dull|"
                        r"packed|rammed|empty|dead|quiet|freezing|soaked|dreadful|"
                        r"worst|cancelled|canceled|let ?down|argued?|argument|row|fight|"
                        r"nightmare|late|closed|shut|broke|broken)\b")
WENT_WELL = re.compile(r"\b(?:great|lovely|brilliant|amazing|excellent|fun|enjoyed|loved|"
                       r"best|good time|nice time|a laugh|buzzing|perfect)\b")
POOR_THING = re.compile(
    r"\b(?:it|that|this|they|the [a-z][a-z'-]*(?:\s+[a-z][a-z'-]*)?)\s+"
    r"(?:was|were|is|are)\s+"
    r"(?:(?:so|really|a bit|a little|pretty|quite|dead|proper|properly|totally|well|too)\s+)*"
    r"(?P<poor>awful|terrible|rubbish|crap|boring|dull|packed|rammed|dead|"
    r"freezing|dreadful|cancelled|canceled|a let ?down|soulless|disappointing|a waste|meh|"
    r"rude|overpriced|a rip ?off|shut|closed)\b", re.I)


def _poor_word(flat):
    match = POOR_THING.search(flat)
    if not match:
        return None
    return " ".join(match.group("poor").split())
VERDICT_WELL = re.compile(r"\b(?:lovely|great|brilliant|amazing|excellent|good|nice|fun|"
                          r"enjoyed|loved|best|a laugh|buzzing|perfect|decent|not bad)\b")
VERDICT_POOR = re.compile(r"\b(?:rubbish|crap|shit|shite|awful|terrible|boring|dull|quiet|"
                          r"packed|rammed|empty|dead|soulless|disappointing|let ?down|"
                          r"nightmare|waste|meh|bad|worst|rude|overpriced|freezing)\b")
WENT_BAD_WEATHER = re.compile(
    r"\b(?:rain(?:ed|ing|y)?|wet|drizzle\w*|showers?|storms?|stormy|soaked|freezing|baltic|"
    r"boiling|scorching|heatwave|cloud\w*|damp|washout|washed out|miserable weather)\b")
STATUS = re.compile(r"\bon my (second|third|fourth|fifth) (coffee|cup|cuppa|tea|drink|beer|glass)\b")
JUST_DONE = re.compile(r"\bjust (finished|done|sent|booked|moved)\b")
JUST_STARTED = re.compile(r"\bjust started\b")
CAME_BACK = re.compile(r"\bjust got back\b")
BACK_FROM = re.compile(
    r"\b(?:(?:i|we)\s+(?:just\s+|only\s+|recently\s+)?(?:got|came|come)\s+back"
    r"|(?:im|i am|we re|we are|were)\s+(?:just\s+)?back"
    r"|(?:i|we)\s+(?:just\s+)?(?:arrived|landed)\s+back)\s+from\s+(.+)$")
BEEN_TO = re.compile(
    r"\b(?:i|we|ive|weve|i have|we have)\s+(?:(?:also|just|only|once|finally|already)\s+)?"
    r"been\s+(?:to|in)\s+(.+)$")
WENT_TO_ANY = re.compile(
    r"\b(?:i|we)\s+(?:went|drove|flew|headed|popped|nipped|cycled|travelled|traveled)\s+"
    r"(?:off\s+|out\s+|over\s+|back\s+)?to\s+(.+)$")
TRIP_NOT_YET = re.compile(r"\b(?:never|havent|hasnt|didnt|did not|not|no|wish|want|going to|"
                          r"gonna|plan to|planning|hope|hoping|soon)\b")
SOME_WHEN = re.compile(r"\b(?:last (?:year|summer|winter|spring|autumn|month|week)|yesterday|"
                       r"(?:" + TIME_COUNT + r"(?:years|months|weeks|days) ago)|"
                       r"(?:back )?in (?:19|20)\d\d|in (?:january|"
                       r"february|march|april|may|june|july|august|september|october|november|"
                       r"december)|when i was (?:a kid|a child|little|young|small)|"
                       r"(?:(?:" + TIME_COUNT + r"times)|once|twice|before|already)|"
                       r"for (?:a|one|two|three|four|\d+) (?:day|days|night|"
                       r"nights|week|weeks))\b")
TRIP_TIME_TAIL = re.compile(r"\s+(?:yesterday|today|last (?:night|week|month|year|summer|"
                            r"christmas)|(?:this|next) (?:week|month|year)|"
                            r"(?:on|over) (?:the )?weekend|"
                            r"on (?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)|"
                            r"(?:" + TIME_COUNT + r"(?:years|months|weeks|days) ago)|"
                            r"(?:back )?in (?:19|20)\d\d|to (?:19|20)\d\d|"
                            r"when i was (?:a kid|a child|little|young|small)|"
                            r"(?:(?:" + TIME_COUNT + r"times)|once|twice|again|before|already)|"
                            r"for \w+ (?:days?|nights?|weeks?))\b.*$")
TRIP_SHORT_COUNTRIES = frozenset(("us", "states"))
PRESENCE = re.compile(r"^(?:hey |hi |oi |ok |okay )?(?:(?:are|r) (?:you|u)|(?:you|u)) "
                      r"(?:there|around|awake|listening|up)(?: (?:still|now|right now|or what))?[?.!]*$"
                      r"|^(?:are |is )?(?:anyone|anybody|someone) (?:there|around|home)[?.!]*$"
                      r"|^(?:still|you still) (?:there|with me|here|awake)[?.!]*$")
PAUSE = re.compile(r"^(?:ok |okay |right |alright )?(?:brb|be right back|one sec|one moment|"
                   r"give me a (?:sec|minute|mo)|hold on|hang on|2 secs|two secs)"
                   r"(?: a (?:sec|tick|minute|moment|mo|bit))?[?.!,]*$")
_LOST_TAIL = (r"(?: ?(?:anymore|any more|now|right now|at all|really|tbh|honestly|today|at the "
              r"moment|again))*[?.!,]*$")
LOST_ONLY = re.compile(
    r"^(?:ok |okay |so |well |tbh |honestly |urgh |ugh )?(?:"
    r"(?:i |we )?(?:(?:dont|do not) (?:really |actually )?know|dunno|dno|idk|dk) "
    r"(?:really )?(?:what to do|where to start|where to begin|what to do next)"
    r"|(?:(?:i|we) )?(?:(?:have|ve got|got|had|hv) )?no idea (?:at all )?"
    r"(?:what to do|where to start|where to begin|what to do next)"
    r"|(?:im|i am|i feel| i m|feeling|feel)(?: so| really| totally| a bit| kinda| kind of| quite)? "
    r"stuck"
    r")" + _LOST_TAIL)
_AT_IT_TAIL = (r"(?:\s+(?:at all|today|right now|anymore|any more|now|for me|tbh|honestly|"
               r"seriously|still))?[?.!,]*$")
AT_IT = re.compile(
    r"^(?:ok |okay |so |well |tbh |honestly |urgh |ugh |god |christ |right )?(?:"
    r"nothing (?:is|seems to be|seems|i (?:do|try)|i m doing) (?:working|works)"
    r"|nothing works"
    r"|nothing is going right"
    r"|(?:it all|everything) keeps going wrong"
    r"|(?:i ve|i have|we ve|we have|ive|i|we) (?:just )?(?:hit|come up against) a "
    r"(?:wall|brick wall)"
    r"|(?:im|i am|i m|we re|we are|i feel|i m feeling) (?:just |really |still )?not getting "
    r"(?:anywhere|there|far)"
    r"|(?:im|i am|i m|we re|we are) (?:just |still )?(?:going|spinning) (?:round|around) in "
    r"circles"
    r"|(?:im|i am|i m) (?:just )?spinning (?:my wheels|in circles)"
    r")" + _AT_IT_TAIL)
_HOW_LONG_AT_IT = re.compile(
    r"^(?:ok |okay |so |well |tbh |honestly |urgh |ugh |god )?(?:"
    r"(?:i ve|ive|i have|we ve|we have|i d|id) (?:been )?(?:tried|trying|been at it|at it|"
    r"having a go|giving it a go|working on it)(?: (?:for|since) [^.!?]{1,18})?"
    r"|(?:i ve|ive) tried (?:everything|it all|all of it|all sorts|everything i can think of|"
    r"literally everything)"
    r"|(?:there is|theres) nothing else (?:left )?to try"
    r"|nothing else (?:has )?(?:worked|to try)"
    r"|(?:i |we )?(?:dont|do not) know what else to (?:do|try)"
    r"|(?:i |we )(?:ve |have )?run out of ideas"
    r")(?: (?:now|already|again|honestly|tbh|yet))?[?.!,]*$")
def _asked_about_the_effort(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not turns or not isinstance(turns[-1], dict):
        return False
    said = turns[-1].get("bot") or ""
    for kind in ("at_it", "on_a_form", "on_the_thing", "the_long_haul"):
        if said in NEWS_REPLIES.get(kind, ()):
            return True
    return False


_A_FORM = r"(?:[a-z]+\s+){0,3}forms?"
_A_THING_TO_MAKE = (r"(?:cv|r[ée]sum[ée]|cover letter|covering letter|personal statement|essay|"
                    r"dissertation|thesis|assignment|coursework|homework|report|blog post|"
                    r"uni statement"
                    r"|(?:(?:job|visa|course|college|uni|university|rental|tenancy|passport|"
                    r"membership|licen[cs]e|travel|grant)\s+)?applications?"
                    r"|" + _A_FORM + r")")
STUCK_FEELING = re.compile(
    r"^(?:ok |okay |so |well |tbh |honestly |urgh |ugh |right |god )?"
    r"(?:(?:i|we)\s+)?(?:just\s+|really\s+|so\s+|totally\s+|properly\s+|kind of\s+|sort of\s+|"
    r"a bit\s+|completely\s+)*"
    r"(?:(?:feel|feels|feeling|felt)\s+"
    r"(?:(?:like|that)\s+(?:(?:i|we)\s+(?:am|are)\s+)?)?"
    r"(?:so\s+|really\s+|totally\s+|properly\s+|kind of\s+|sort of\s+|a bit\s+|completely\s+|"
    r"very\s+|pretty\s+)*"
    r"(?:stuck|stuck\s+(?:again|now))"
    r"|(?:i m|im|i am|we re|we are)\s+(?:so|really|totally|properly|completely|kind of|sort of|"
    r"a bit|very|pretty)\s+stuck)"
    r"(?:\s+(?:right now|at the moment|again|today|with (?:everything|it all|life)))?"
    r"[?.!,]*$")
_STUCK_ON = (r"^(?:ok |okay |so |well |tbh |honestly |urgh |ugh |right )?"
             r"(?:(?:i m|im|i am|i ve been|i have been|we re|we are|i|we)\s+"
             r"(?:feel(?:ing)?\s+)?"
             r"(?:still\s+|totally\s+|completely\s+|really\s+|a bit\s+|kind of\s+|sort of\s+|"
             r"so\s+)?"
             r"(?:stuck|stuck again|going nowhere|getting nowhere|not getting anywhere|blocked)\s+"
             r"(?:on|with|in)\s+|(?:i|we) (?:keep|keeps) getting stuck (?:on|with) )"
             r"(?:my|the|this|that|a|our|his|her|their)?\s*")
_STUCK_TAIL = (r"\b(?:\s+(?:again|all (?:week|day|morning)|for (?:days|hours|weeks)|"
               r"since \w+))?[?.!,]*$")
STUCK_ON_A_FORM = re.compile(_STUCK_ON + _A_FORM + _STUCK_TAIL)
STUCK_ON_A_THING = re.compile(_STUCK_ON + _A_THING_TO_MAKE + _STUCK_TAIL)
RETURNED = re.compile(r"^(?:ok |okay |right |alright )?(?:im |i am |we re |we are |were |we )?back(?: again| now)?"
                      r"(?:[, ]*(?:where were we|what were we (?:saying|doing|on about)|sorry))?[?.!]*$")
BID = re.compile(r"\b(?:guess what|you ll never guess|you wont believe|you won t believe|"
                 r"wait till you hear|wait until you hear|want to hear something)\b")
LEAVING = re.compile(r"^(?:ok |okay |right |well )?(?:im |i am |we re |we are )?"
                     r"(?:out the door|out of the door|just leaving|leaving now|leaving in a "
                     r"(?:min|minute|sec)|setting off|setting out|just off|off now)"
                     r"(?: now| soon| for (?:work|school|uni|a bit))?[!. ]*$"
                     r"|^(?:ok |okay |right |well )?(?:im |i am |we re |we are )?"
                     r"(?:off|heading off|heading|popping|nipping) (?:out|off|to) "
                     r"(?:work|bed|sleep|town|the shops|the shop|pick up|collect|school|uni|"
                     r"the gym|the pub|my mums?|my mums? place|my parents)"
                     r"(?: (?:now|soon|later|after this|in a bit|for a bit))?"
                     r"(?:[, ]*(?:see (?:you|ya)(?: later| soon| tomorrow)?|bye|goodnight))?[!. ]*$"
                     r"|^(?:ok |okay |right )?(?:im |i am )?(?:off out|out out|heading out|"
                     r"popping out|nipping out)(?: now| soon| for a bit)?[!. ]*$"
                     r"|^at work now[!. ]*$")
HOME_AGAIN = re.compile(r"^(?:ok |okay |well |only )?(?:(?:(?:i|we) )?(?:just )?(?:got|come|came|arrived) home"
                        r"|(?:im|i am|we re|we are) home"
                        r"|home)"
                       r"(?: (?:now|again|at last))?(?: (?:from|after) [a-z ]{1,24})?[!. ]*$"
                       r"|^(?:ok |okay |well )?(?:im |i am |we re |we are )?(?:just |only )?"
                       r"(?:got in|got back|back in|walked in|in now)"
                       r"(?: (?:now|again|at last|finally))?"
                       r"(?: (?:from|after) (?:work|the gym|the shops|the shop|school|uni|"
                       r"town|lunch|the pub|my mums?|my parents))?[!. ]*$"
                       r"|^(?:ok |okay |well )?(?:just |only )?back from (?:work|the gym|the "
                       r"shops|the shop|school|uni|town|lunch|my mums?|my parents)"
                       r"(?: now)?[!. ]*$")
UNDERWAY = re.compile(r"^(?:ok |okay |well |right )?(?:im |i am |we re |we are )?"
                      r"(?:(?:on my|on our|on the) (?:way|way there|way home|way in)"
                      r"|omw|nearly there|almost there|nearly "
                      r"home|almost home|halfway there|not far now|(?:\d+|ten|five|two|a "
                      r"few) (?:minutes|mins|min) away|just around the corner|nearly in)"
                      r"(?: (?:now|still|anyway))?[!. ]*$")
IN_BED = re.compile(r"^(?:ok |okay |well )?(?:im |i am )?(?:already |just )?(?:in|off to|going "
                    r"to|going off to) bed(?: already| now| at last)?[!. ]*$"
                    r"|^(?:im |i am )?(?:already )?(?:in bed|in my bed)(?: already| now)?[!. ]*$")
AWAKE_SINCE = re.compile(
    r"^(?:ok |okay |well |so )?(?:been |i was |im |i am )?awake since (?P<when>\d{1,2}"
    r"(?::\d{2})? ?(?:am|pm|o clock|oclock)?|\d{1,2}(?::\d{2})?)\b[!. ]*$")
ERRAND = re.compile(r"^(?:ok |okay |well )?(?:i )?(?:need|have|got|gotta|must|needs)(?: got)? to "
                    r"(?:do |run |get )?(?:a |the |some |my |our )?"
                    r"(?P<what>shop|shopping|food shop|big shop|wash(?:ing)?|laundry|ironing|"
                    r"cleaning|tidy up|tidy|hoover(?:ing)?|dishes|washing up)"
                    r"(?: done| later| today| tomorrow| before [a-z ]{2,20})?[!. ]*$")

WISH_LUCK = re.compile(r"\bwish me luck\b|\bfingers crossed\b|\bkeep your fingers crossed\b")

NEWS_REPLIES = {
    "judged": (
        "Whether {thing} is the right move is yours to weigh, not mine. What is the bit you are "
        "unsure about?",
        "{Thing} — that is your call, not mine. Say what you would lose either way and I will "
        "lay it out with you.",
        "I cannot call that one for you. Tell me what matters most about {thing} and I will help "
        "you think it through.",
    ),
    "judged_bare": (
        "That is yours to weigh, not mine. What is the bit you are unsure about?",
        "Not a call I can make for you. Say what you would lose either way and I will lay it out.",
        "I cannot call that one for you. Tell me what matters most and I will help you think it "
        "through.",
    ),

    "out_of_work": (
        "Between jobs is a job in itself. What sort of work are you after?",
        "That is a rough stretch. What are you applying for at the moment?",
        "How long have you been looking? Tell me the work you want and I will help with the CV "
        "or where to look.",
    ),
    "retired": (
        "Retired - how are you filling the days?",
        "That is a big change. What does a normal week look like now?",
        "Retired, then. What have you been meaning to get to?",
    ),
    "job": (
        "A {x} — nice one. What's a normal day like for you?",
        "{X} — good to know. What do you like most about it?",
        "A {x}, busy job. How long have you been doing it?",
    ),
    "place": (
        "{place} — nice. How long have you been there?",
        "{place} — what's it like there?",
        "{place}? Good to know. Do you like it there?",
    ),
    "place_near": (
        "{place}, {near} — handy. What's the area like?",
        "{place} — {near}, then. Do you like it there?",
        "{place}, {near}. Sounds like a good spot.",
    ),
    "moving": (
        "{place} — that's a big move. Have you found a place yet?",
        "Moving to {place}. Exciting - what's the plan?",
        "{place} in the diary, then. Do you know anyone there?",
    ),
    "trip": (
        "Welcome back! How was it?",
        "Nice — a break does a lot of good. What was the best bit?",
        "Good to be back? What was the highlight?",
    ),
    "kids": (
        "{X} — good to know. How old are they?",
        "{X}. What are they into at the moment?",
        "{X} — noted. Tell me about them.",
    ),
    "kids_aged": (
        "{X} — noted.",
        "{X}. What are they into at the moment?",
        "{X} — good to know. Tell me about them.",
    ),
    "back_from": (
        "Back from {X} — good trip? What was the best bit?",
        "{X} — nice. How was it?",
        "Welcome back from {X}. What was the best bit?",
    ),
    "been_to": (
        "{X} — lovely. What did you like most about it?",
        "{X} — what was the best bit?",
        "{X}, good call. Would you go back?",
    ),

    "med_visit": (
        "{X} is never a quick trip. What did they say?",
        "Good to have {x} out of the way. Did they give you anything useful to go on?",
        "{X}, then. Any word on what happens next?",
    ),
    "med_visit_night": (
        "{X} at night — that is your evening gone. Did they get you sorted?",
        "A night in {x} is the worst kind of long. How are you doing now it is over?",
        "Nobody wants {x} after dark. What did they say?",
    ),
    "med_results": (
        "Results back — that is the wait nobody enjoys. What did they say?",
        "{Xb} in, then. Anything you have to act on, or is it a wait-and-see?",
        "That was quick, or it felt long. What did they tell you?",
    ),
    "med_clear_plural": (
        "Clear is what you want to hear — that is one thing off your mind.",
        "Clear {x} are the best kind of boring. That earns a proper evening off, if you ask me.",
        "That is the answer you were after. Worth telling whoever was worrying with you.",
    ),
    "med_clear": (
        "Clear is what you want to hear — that is one thing off your mind.",
        "A clear {xb} is the best kind of boring. That earns a proper evening off, if you ask me.",
        "That is the answer you were after. Worth telling whoever was worrying with you.",
    ),
    "med_diagnosis": (
        "{A} {x} is annoying, but at least it is a named thing. Give it the resting they told "
        "you about rather than the resting that feels like enough.",
        "So {a} {x}, and nothing worse. Follow what they said even on the days it feels fine — "
        "that is the part most people skip.",
        "{A} {x} is treatable and boring to get over. It wants the time they said, not the time "
        "you would like.",
    ),
    "med_part_fine": (
        "Good news on the {xb}, then. The resting is the part that actually sorts it out, so "
        "give it the time they said.",
        "Fine on the {xb} is the best answer you could have got. Do the resting properly and "
        "it will settle.",
        "That is a relief. Boring advice next, but it is the advice: rest it for as long as they "
        "said, then build it up slowly.",
    ),
    "med_part_fine_result": (
        "{Xb} fine is the answer you want. Was that the whole check, or are they waiting on "
        "anything else?",
        "Good news about the {xb}, then — nothing to act on.",
        "{Xb} fine, then. That is one thing off your mind.",
    ),
    "med_wearing": (
        "A {xb} is a good sign somebody took it seriously. Keep it dry, and let people carry "
        "things for you while the bone does the work.",
        "The {xb} is more boring than painful after the first day or two. Worth lining up "
        "something that only needs the one hand.",
        "So a {xb} for a few weeks. Ask them at the next check what you can still do, rather "
        "than finding out by trying it.",
    ),
    "med_dressing": (
        "A {xb} for a day or two, then, not weeks. Keep it dry and change it when they said "
        "to, and let them look at it if the skin round it goes hot or tight.",
        "Good - that is the part that keeps it clean while it closes. Leave it alone until they "
        "told you to change it, and keep it out of the bathwater.",
        "Not much to it, which is the point: keep it dry, do not pick at it, and ring them if the "
        "edge starts spreading red.",
    ),
    "med_out": (
        "Out, then — that is the worst of it done. Ice it today, and take what they gave you "
        "before the numbing wears off.",
        "Glad it is out. Soft food for a day, and no straws while it heals, which nobody tells "
        "you until afterwards.",
        "So it is out. The ache settles in a day or two; if the bleeding carries on past that, "
        "ring them back.",
    ),
    "pet": (
        "A {pet} — lovely. How old is it?",
        "A {pet} — good to know. What's its name?",
        "Lovely. How's the {pet} settling in?",
    ),
    "pet_named": (
        "A {pet} called {name} — lovely. How's {name} settling in?",
        "{name} — good name for a {pet}. How old is {name}?",
        "Lovely — a {pet} called {name}. How's the first week going?",
    ),
    "good_news": (
        "That's brilliant. Nice one!",
        "Love that — well done. How are you celebrating?",
        "Good stuff. That must be a weight off.",
    ),
    "more_of_the_news": MORE_OF_THE_NEWS,
    "more_of_the_news_score": MORE_OF_THE_NEWS_SCORE,
    "more_of_the_news_arrival": MORE_OF_THE_NEWS_ARRIVAL,
    "bad_news": (
        "That's gutting, especially after you put the work in. Ask for feedback if you can — "
        "it usually says exactly what to change.",
        "Sorry to hear it. Give it a day before deciding anything, then look at what you can "
        "control next time.",
        "That stings. Most people who get these were turned down first, so it's worth one more go.",
    ),
    "lost_job": (
        "That's a blow. Give it a day before deciding anything, then check what you're owed: "
        "notice, holiday pay and anything in your contract.",
        "Sorry to hear it. However it ended, get the reason and the pay in writing before you "
        "agree to anything.",
        "That's hard. What happened - was it a surprise, or had you seen it coming?",
    ),
    "lost_weight": (
        "Was that on purpose, or has it been dropping on its own? If it's going without you "
        "trying, a word with the GP is worth it.",
        "Nice, if that was the plan. If it wasn't, it's worth getting checked - weight that "
        "comes off by itself shouldn't be ignored.",
        "How are you feeling in yourself otherwise? Losing weight by accident is the bit to "
        "keep an eye on.",
    ),
    "nothing_on": (
        "Nothing worth watching is annoying. Pick a film you already like rather than hunting for one.",
        "Try a film instead of channel-hopping — even one you've seen beats scrolling.",
    ),
    "status": (
        "One of those mornings, then. Anything you can push to tomorrow?",
        "The second cup says it all. What's making today busy?",
        "Coffee is doing the heavy lifting today, then.",
    ),
    "saw_it_told": (
        "{X} — which one?",
        "{X} — what was it?",
        "{X} — nice one. What was it called?",
    ),
    "saw_it_poor": (
        "{X} — sorry it wasn't up to much. What was wrong with it?",
        "Shame about {x}. What wasn't right about it?",
        "{X}, and not a good one — what let it down?",
    ),
    "day_out_poor": (
        "{X} — sorry it wasn't up to much. What was wrong with it?",
        "Shame about {x}. Would you give it another go?",
        "Ah, that's a shame about {x}. What let it down?",
    ),
    "saw_it": (
        "{X} — any good?",
        "{X} — what did you make of it?",
        "{X} — glad you got out for it. Was it good?",
    ),
    "day_out": (
        "{X} — how was it?",
        "{X} — what was it like?",
        "{X} — that's a good way to spend it. Tell me the best bit.",
    ),
    "day_out_well": (
        "{X} and a good time — nice. What made it?",
        "Glad it was a good one. {X} beats a night in.",
        "{X} well spent, then. Those are the ones that make the week.",
    ),
    "night_out_well": (
        "{X} — glad it was a good one.",
        "Good. {X} that lands is worth going back to.",
        "Nice one. That's the sort of evening that makes the week.",
    ),
    "night_out_poor": (
        "Shame about {x}. Do you think it was a one-off?",
        "Ah well — at least you know now. {X} can be hit and miss.",
        "Sorry to hear it. What was the letdown?",
    ),
    "night_out_weather": (
        "Shame about the weather. Did you get much out of {X} anyway?",
        "{X} in that weather is a hard one. Did you make the most of it?",
        "That's the risk with {X}. Would you go back another time?",
        "Weather like that can spoil a trip. Was any of it good?",
    ),
    "night_out_poor_said": (
        "Sorry it was {p}. What was wrong with it?",
        "{P}, then — that's a shame. Do you think it was a one-off?",
        "That takes the shine off it. {P} — what was behind that?",
    ),
    "move_done": (
        "That's a big one, and the boxes are the easy bit. How's the settling in going?",
        "Big job. Being at home somewhere new takes longer than the unpacking does, so give it a "
        "few weeks before it feels right.",
        "Out of one place and into another — that's the week gone. Is the kettle unpacked yet?",
    ),
    "just_done": (
        "How did it go?",
        "Nice. What's next?",
        "Good. Take a minute before the next thing.",
    ),
    "just_started": (
        "How's it going so far?",
        "Nice. What made you start?",
        "Good for you. Keep it short and regular and it sticks.",
    ),
    "came_back": (
        "Nice — how was it?",
        "Any good?",
        "Good to have you back. Did you enjoy it?",
    ),
    "presence": (
        "Still here. What's up?",
        "Yep, right here — go on.",
        "I'm here. What's on your mind?",
    ),
    "pause": (
        "No rush. I'll be here.",
        "Take your time.",
        "Whenever you're ready — I'm not going anywhere.",
    ),
    "lost": (
        "That's a rough place to be. What's weighing on you most?",
        "Fair enough. Tell me what's going on and we'll find a first step together.",
        "Okay. Start with the part that's loudest — what's it about?",
        "Let's take it one bit at a time. What's the situation?",
    ),
    "at_it": (
        "That usually means the approach needs one change rather than more effort. What have you "
        "tried so far?",
        "Worth stopping before you push harder at it. Which part keeps letting you down - the "
        "start, the middle, or keeping it going?",
        "Nothing landing is often a plan that is too big for the week you have. What is the "
        "smallest piece of it you could finish today?",
        "That is the point where doing more of the same stops helping. What would count as it "
        "working?",
    ),
    "the_long_haul": (
        "Then it is not effort you are short of. What have you already ruled out?",
        "That is a lot of trying for the same result. Which part has moved at all, even a little?",
        "Everything tried and nothing landing usually means one step is wrong, not you. What does "
        "it look like when it works?",
        "So more of the same will not do it. What would tell you it had started to work?",
    ),
    "a_stuck_feeling": (
        "Feeling stuck is usually one part of it rather than all of it. Which part is it?",
        "That is worth taking seriously, not shrugging off. What is the thing that will not move?",
        "Stuck like that is tiring in a way that trying harder does not fix. What would shifting it "
        "even a little look like?",
        "Then something is jammed rather than you being bad at it. What is the thing you keep "
        "coming back to?",
    ),
    "on_a_form": (
        "Forms are mostly copying, not writing. Which boxes can you answer from a paper you "
        "already have, and which are the ones you are stuck on?",
        "Read the notes at the top of it before the boxes: they say what the question actually "
        "wants, and most stuck boxes are a question read the wrong way.",
        "Fill in the ones you can from a document in front of you - name, dates, the numbers - "
        "and leave the rest blank for now. The blank ones are the question.",
        "Which part stops you - a box you cannot answer, or one you are not sure you have read "
        "right?",
    ),
    "on_the_thing": (
        "Which bit of it has you stuck - what to put in it, or how it should read?",
        "Then start with the part you already know the answer to, even the boring one - the "
        "first line down breaks the back of it.",
        "Is it the words that will not come, or not knowing what they want from you - those need "
        "different help.",
        "Do the facts first - names, dates, the numbers you can look up - and leave the wording "
        "until there is something on the page to word.",
    ),
    "returned": (
        "Welcome back. Where were we?",
        "Back again. What were we saying?",
        "There you are. Right, where did we get to?",
    ),
    "bid": (
        "Go on then — tell me.",
        "Now I'm curious. What happened?",
        "I'm listening. Spill it.",
    ),
    "leaving": (
        "Off you go. Tell me how it went later.",
        "Have a good one.",
        "Right — good luck with it.",
    ),
    "leaving_bed": (
        "Sleep well. I'll be here tomorrow.",
        "Night, then. Get a proper sleep.",
        "Off to bed — good. Talk tomorrow.",
    ),
    "home_again": (
        "Home at last. Feet up first, everything else after.",
        "Long day? Get something to eat before the rest of it.",
        "Nice one. What's the plan for the evening?",
    ),
    "wish_luck": (
        "Good luck! You'll be fine — you've prepared more than you think.",
        "Fingers crossed. Deep breath first, then go.",
        "Good luck — slow and steady beats perfect.",
    ),
    "underway": (
        "No rush at this end — mind how you go.",
        "Safe trip. I'll be here when you land.",
        "Nearly there is the worst bit of any journey. Hope the rest is easy.",
        "Take your time. Nothing here is going anywhere.",
    ),
    "in_bed": (
        "Bed is the right call. Sleep well.",
        "Good. Get an early night while you can.",
        "In bed is the best place to be by this hour. Night.",
    ),
    "awake": (
        "Since {when}? That's a long stretch. Fingers crossed for a better night tonight.",
        "Awake since {when} is rough. A dark room and no phone is the only trick I know.",
        "{when} is a long time to be lying awake. Nap at the first chance you get.",
    ),
    "chore": (
        "The {what} can wait a minute. It always takes longer than you think, mind.",
        "Get a list or a podcast on and the {what} goes faster.",
        "Nobody ever regrets doing the {what} early. Not a fun one, though.",
    ),
}

def _as_a_pattern(line):
    out = []
    for part in re.split(r"(\{[A-Za-z_]+\})", line):
        if part.startswith("{") and part.endswith("}"):
            out.append(".+")
        elif part:
            out.append(re.escape(part))
    return re.compile("".join(out))


HANDS_IT_BACK = tuple(_as_a_pattern(line)
                      for kind in ("judged", "judged_bare")
                      for line in NEWS_REPLIES[kind])


def hands_it_back(reply):
    said = str(reply or "").strip()
    return any(pattern.fullmatch(said) for pattern in HANDS_IT_BACK)

ACK_WORDS |= {"guess", "suppose", "sort", "ish", "smile", "wink", "love", "worries", "right",
              "then", "cheers", "nice", "brill", "bravo", "yay", "aye", "okey", "oki",
              "safe", "unsafe"}
POSITIVE = {"good", "fine", "great", "ok", "okay", "alright", "nice", "well", "smile", "yay",
            "brilliant", "lovely", "cool", "sweet", "perfect",
            "grand", "chill", "content", "mint", "brill", "sound"}

FEELINGS = (
    ("tired", ("tired", "exhausted", "knackered", "shattered", "wiped", "sleepy", "bushed",
               "drained", "shattered", "done in", "no energy", "worn out",
               "exhausting", "draining", "tiring", "knackering", "wearing out",
               "beat", "spent", "zonked", "pooped", "dead on my feet",
               "fagged", "wrecked",
               "worn down", "used up", "like a zombie", "a zombie", "zombie")),
    ("rough_day", ("hungover", "hangover", "hang over", "hung over", "jet lagged", "jetlagged",
                   "jet lag", "cream crackered", "crackered")),
    ("stressed", ("stressed", "stress", "overwhelmed", "swamped", "under pressure", "too much on",
                  "pulled in every direction", "snowed under",
                  "stressful", "overwhelming")),
    ("anxious", ("anxious", "anxiety", "nervous", "worried", "worry", "wound up", "on edge",
                 "panicking", "panic", "scared", "frightened", "restless",
                 "terrified", "petrified")),
    ("sad", ("sad", "down", "miserable", "low", "upset", "heartbroken", "gutted", "crying",
             "unhappy", "depressed", "not ok", "not okay", "not doing great", "not great",
             "not fine", "not alright", "not so good", "not doing well", "not feeling great",
             "weepy", "tearful", "homesick", "rotten", "lousy", "meh", "rough", "crap",
             "rubbish", "numb",
             "sadder", "saddest", "more miserable", "worse than before",
             "cry", "cried", "cries", "weep", "weeping", "wept", "sobs", "weeps",
             "sob", "sobbing",
             "bawl", "bawling", "blub", "blubbing", "tears", "in tears", "welling up",
             "burst into tears", "bursting into tears", "tearing up", "tear up", "choked up",
             "empty", "flat", "hollow", "blank", "dead inside", "nothing to give",
             "feel nothing", "like a failure", "like a mess", "like rubbish", "like crap",
             "like a burden", "like a fraud", "like nothing matters", "a mess",
             "in a bad mood", "in a low mood", "in a foul mood", "in a mood",
             "in a state", "in a right state", "out of sorts", "not myself",
             "not feeling myself", "off colour", "off form")),
    ("guilty", ("guilty", "ashamed", "embarrassed", "my fault", "feel bad about",
                "feel awful about", "feel terrible about", "feel dreadful about",
                "feel horrible about",
                "let them down", "let her down", "let him down",
                "let my family down", "should have been there", "wasnt there enough")),
    ("lonely", ("lonely", "alone", "isolated", "left out", "no one to talk to", "on my own")),
    ("unappreciated", ("taken for granted", "not appreciated", "unappreciated")),
    ("bored", ("bored", "boring", "nothing to do", "nothing to do")),
    ("annoyed", ("annoyed", "angry", "furious", "pissed", "irritated", "frustrated", "fed up",
                 "cross", "livid", "raging", "mad", "grumpy", "cheesed off",
                 "fuming", "miffed",
                 "mardy",
                 "browned off", "peeved",
                 "stroppy", "stroppy with", "in a huff")),
    ("relieved", ("relieved", "relief", "such a relief", "what a relief",
                   "weight off my shoulders", "weight off my mind")),
    ("happy", ("happy", "great", "glad", "excited", "thrilled", "chuffed",
               "delighted", "buzzing", "made up", "over the moon", "brilliant news",
               "good mood", "feeling good", "feel good", "in good form", "on good form",
               "cheerful", "cheery", "in a great mood", "great mood",
               "happier", "happiest", "gladder", "gladdest")),
)
FLAT_IDIOM = re.compile(r"\bflat\s+(?:out|broke)\b|\bflat as (?:a|an) \w+")
NOT_LANDED = re.compile(
    r"\bbut\s+(?:i\s*'?m|im|i\s+am)\s+(?:not|n'?t)\b"
    r"|\bbut\s+i\s+(?:still\s+)?(?:don'?t|do\s+not|didnt|didn'?t)\s+(?:feel|felt)"
    r"\s+(?:it|that|anything|nothing|happy|glad|excited)\b"
    r"|\b(?:don'?t|do\s+not|didnt|didn'?t)\s+feel\s+(?:anything|nothing|it|happy|glad|excited)\b"
    r"|\bfeel(?:ing)?\s+(?:nothing|flat|numb|empty)\b")

GOOD_NEWS_SAID = re.compile(
    r"\b(?:great|good|brilliant|amazing|wonderful|excellent|fantastic)\s+news\b")

ANY_WORLD_NEWS_ON = re.compile(r"\bany\s+news\s+(?:on|about|of)\s+\w")

NOT_GLAD_WORDS = ("happy", "glad", "pleased", "excited", "thrilled", "relieved")
ANNOUNCED_ONE = re.compile(r"\b(?:bit of a|a bit of a|a right|a proper)\s+"
                           r"(?:mad|weird|strange|funny|odd|daft|curious)\s+one\b")
NEWS_AFTER = re.compile(r"\b(?:my|our|his|her|their|the|this|that|these|those|your)\s+[a-z]",
                        re.I)
ASKED_ABOUT_THE_BOT = re.compile(r"\b(?:do|are|were|have|has|did|can|could|would|will) "
                                 r"(?:you|u|ya)\b")
SELF_INSULT = re.compile(r"\blike (?:such |a bit of |a total |a complete |an absolute |an utter |"
                         r"a right |kind of |sort of )?a (?:failure|mess|burden|fraud|waste|"
                         r"letdown|loser|nobody)\b")
MOOD_FOR = re.compile(r"\bin (?:a|the) mood for\b")
NOT_MYSELF = re.compile(r"\b(?:im|i'm|i am|i)(?:\s+\w+){0,3}\s+(?:not|never|dont|didnt|havent|"
                        r"hasnt)\s+(?:\w+\s+){0,2}myself\b")
THING_WORDS = frozenset("flat empty blank hollow numb".split())


def _a_thing_in_front(clean, word):
    if word not in THING_WORDS:
        return False
    at = clean.find(word)
    return bool(re.search(r"\b(?:a|an|the|this|that|my|your|our|their|his|her|its|any|no|another)"
                          r"\s+$", clean[:at]))


SPENT_MONEY = re.compile(r"\bspent\s+(?:up|all|it|my|the|every|so\s+much)\b")
LOW_THING = re.compile(r"\b(?:low|high)\s+(?:heat|light|lighting|flame|setting|settings|"
                       r"temperature|temp|battery|charge|power|price|prices|cost|costs|rate|rates|"
                       r"speed|volume|sun|sugar|stock|budget|income|rent|wages|pressure|mileage|"
                       r"salt|fat|calories)\b")

TIRED_PERSISTENT = re.compile(
    r"\b(?:all (?:the time|day|week)|always|constantly|every ?day|every morning|each morning|"
    r"for (?:weeks|months|years)|these days|lately|recently|"
    r"no matter how much (?:i )?sleep|even after (?:a|my|sleeping)|"
    r"keep (?:falling asleep|getting|waking)|"
    r"(?:i )?(?:dont|do not|can'?t|cant) (?:know )?why|why am i|why do i|why is it|"
    r"is (?:that|it|this) (?:why|because))\b")
TIRED_DESPITE_SLEEP = re.compile(
    r"\bstill\s+(?:tired|exhausted|knackered|shattered|wiped out|drained)\b")
SLEEP_WORD = re.compile(r"\b(?:sleep|sleeping|slept|hours|nights?)\b")
ACT_GERUND = (r"(?:lying|cancell?ing|shouting|yelling|snapping|ignoring|forgetting|missing|"
              r"hurting|upsetting|breaking|cheating|stealing|taking|quitting|leaving|blaming|"
              r"criticis?ing|arguing|fighting|drinking|smoking|spending|eating|letting)")
IRREGULAR_DEED = (r"forgot|said|told|broke|ate|spent|let|left|made|took|went|drank|bought|sold|"
                  r"threw|woke|spoke|swore|drove|flew|kept|stood|ran|hid|lost|slept|bit|hit")
DEED_TAIL = (r"(?:about|for|over)\s+(?:not\s+[a-z]+ing\b|" + ACT_GERUND + r"\b)"
             r"|that\s+i\s+(?:[a-z]+ed\b|" + IRREGULAR_DEED + r")")
GUILT_WORD = (r"(?:bad|awful|terrible|rotten|dreadful|horrible|guilty|ashamed)")
GUILT_DEED = re.compile(
    r"\b(?:feel|feels|feeling|felt|feelin)\s+(?:so |really |very |a bit |bad |quite |pretty |"
    r"kind of |kinda |honestly |still )*" + GUILT_WORD + r"\s+(?:" + DEED_TAIL + r")")
REGRET_DEED = re.compile(
    r"\bi\s+(?:really |so |genuinely |still |deeply |truly |honestly )?(?:regret|regrets)\s+"
    r"(?:(?:what|that)\s+i\s+(?:said|did|told|sent|wrote|shouted|texted|posted|lied|swore|"
    r"broke)\b"
    r"|(?:saying|telling|shouting at|lying to|snapping at|texting|sending|writing)\s+"
    r"(?:her|him|them|everyone|that|it|my\s+\w+|the\s+\w+)\b)")
SICK_DEED = re.compile(
    r"\b(?:feel|feels|feeling|felt|feelin)\s+(?:so |really |very |a bit |quite |pretty |kind of |"
    r"kinda |honestly |still )*sick\s+(?:that\s+i\s+(?:[a-z]+ed\b|" + IRREGULAR_DEED + r")"
    r"|(?:(?:about|for|over)\s+not\s+[a-z]+ing\b))")
BODY_FEELING_SHAPE = re.compile(
    r"\b(?:feel|feels|feeling|felt)\s+(?:so |really |very |a bit |quite |pretty |kind of |"
    r"kinda |honestly |still |physically )*"
    r"(?:sick|ill|queasy|nauseous|dreadful|awful|rotten|terrible|funny|odd|strange|weird)"
    r"(?:\s+(?:to|in)\s+my\s+(?:stomach|gut|chest|throat)|\s+in\s+the\s+pit\s+of\s+my\s+"
    r"stomach|\s+all\s+over)?\s+"
    r"(?:with|from|about)\s+(?:the\s+)?"
    r"(?P<feeling>guilt|guilty|shame|ashamed|worry|worried|worrying|dread|dreading|anxiety|"
    r"anxious|panic|panicky|fear|fright|frightened|scared|nerves|nervous|stress|stressed|"
    r"uneasy|it all)\b")
BODY_PART_FEELING = re.compile(
    r"\bmy\s+(?:stomach|gut|chest|heart)\s+(?:is\s+|keeps\s+|just\s+|literally\s+)*"
    r"(?:churning|turning|tightening|in knots|sinking|dropping|tight|jumpy|going|knotted)\s+"
    r"(?:with|at|over)\s+(?:(?:the\s+)?(?P<feeling>guilt|guilty|shame|ashamed|worry|worried|"
    r"dread|dreading|anxiety|anxious|panic|fear|fright|nerves|nervous|stress|stressed|uneasy)\b"
    r"|(?P<thought>the\s+thought\b|thinking\b|it\b))")
BODY_AT_THOUGHT = re.compile(
    r"\b(?:feel|feels|feeling|felt)\s+(?:so |really |very |a bit |quite |pretty |still )*"
    r"(?:sick|ill|queasy|nauseous|dreadful|awful|rotten|terrible|funny|odd|strange|weird)\s+"
    r"(?:when|whenever|every time|each time)\s+(?:i|we)\s+(?:"
    r"(?:think|thought|talk|hear|see|remember)(?:\s+(?:about|of|to|back\s+to))?|look\s+at)"
    r"\s*(?P<object>[a-z']+)?")
BODY_BEFORE_AN_EVENT = re.compile(
    r"\b(?:feel\s+(?:so |really |very |a bit |quite |still )*)?"
    r"(?:sick|ill|queasy|nauseous|stomach\s*(?:ache|achy|churn\w*|turns?|turning|in knots)?|"
    r"gut\s*(?:churn\w*|turns?|in knots)|churning stomach|butterflies)\b"
    r"[^.!?]{0,30}?"
    r"\b(?:before|when|whenever|every time|each time|at the thought of)\s+"
    r"(?:(?:i\s+am|im|i'm|i)\s+)?"
    r"(?:every|each|a|an|the|my|any|big|important)?\s*"
    r"(?:nervous|anxious|worri\w+|scared|panic\w*|stressed|dread\w*|exam\w*|meeting\w*|"
    r"interview\w*|presentation\w*|present\w*|speak\w*|talk\w*|call|date|wedding|party|"
    r"flight|test\w*|trip|appointment\w*|shift\w*|performance\w*|"
    r"match\w*|race\w*|audition\w*)\b", re.I)
THOUGHT_UNNAMED = frozenset((
    "it", "that", "this", "them", "her", "him", "you", "us", "everything", "anything",
    "nothing", "those", "these", "all", "what", "how",
))
SYMPTOM_IN_LINE = re.compile(
    r"\b(?:diarr\w*|throwing up|threw up|vomit\w*|being sick|been sick|the runs|"
    r"(?:a |the |my )?(?:temperature|fever)|dizzy|light[- ]?headed|"
    r"blood\b(?!\s+(?:test|pressure|sugar|type|group|donor|donation))|cramps?\b|"
    r"(?:can'?t|cant|couldn'?t) keep (?:anything|food|water) down|"
    r"keep(?:ing)? anything down)")
ASKS_IF_NORMAL = re.compile(
    r"\b(?:is|was)\s+(?:that|this|it)\s+(?:normal|ok\b|okay\b|usual|weird|common)\b|"
    r"\bis that a (?:normal|thing)\b|\bam i (?:normal|weird|going mad)\b")
BUG_NAMED = re.compile(
    r"\b(?:flu|covid|coronavirus|virus|bug|infection|migraine|headache|hangover|food poisoning|"
    r"the squits|d and v|chest infection|sore throat|tonsillitis|vertigo|morning sickness)\b")
BODY_FEELING_WORDS = {
    "guilt": "guilty", "guilty": "guilty", "shame": "guilty", "ashamed": "guilty",
}


def _body_is_a_feeling(clean):
    text = str(clean or "")
    if BUG_NAMED.search(text):
        return None
    if SYMPTOM_IN_LINE.search(text):
        return None
    if LOSS.search(text) or badnews.reads_as_someones_death(text):
        return None
    for pattern in (BODY_FEELING_SHAPE, BODY_PART_FEELING):
        found = pattern.search(text)
        if found:
            said = (found.groupdict().get("feeling") or "").strip()
            return _the_kind_of_worry(BODY_FEELING_WORDS.get(said, "worry"), text)
    found = BODY_AT_THOUGHT.search(text)
    if found:
        pointed_at = (found.group("object") or "").strip()
        if not pointed_at or pointed_at in THOUGHT_UNNAMED:
            return _the_kind_of_worry("worry", text)
    return None


def _the_kind_of_worry(kind, text):
    if kind != "worry":
        return kind
    if WORRY_WHEN.search(text) or ASKS_IF_NORMAL.search(text):
        return "anxious"
    return kind


def _line_as_read(text):
    clean = " ".join(str(text or "").lower().replace("’", "'").split())
    return badnews.without_the_figure_of_speech(clean)


def _a_limit(text, memory):
    read = memory.get("understood") if isinstance(memory, dict) else None
    if not isinstance(read, dict) or not read.get("constraint"):
        return None
    try:
        if lookup.find(read) is not None and not limit.only_a_limit(text):
            return None
        reply = limit_line.reply_for(read, memory)
        if reply and isinstance(memory, dict):
            memory["limit"] = {"said": reply, "steps": limit_line.steps_left(read, memory)}
        return reply
    except Exception:
        return None
"""A verdict the person has already reached on their own life.

"i live alone and love it" got the neutral nod ("I'm listening - say more if it helps"), "i
live on my own and wouldnt change it" the loneliness plan, "i got divorced and its the best
thing i ever did" "Sorry to hear that", "i quit my job and its great" a resignation letter and
"i work nights and love it" a lecture on the body clock. In every one of those the person has
already said how they read the thing, and the reply argues with them - the one thing a friend
never does.

The shape is what is read, never the topic: a statement about their own life, then a verdict on
it with the thing standing as "it"/"that"/"them" ("and love it", "and i dont miss it", "and
wouldnt change it", "and it works for us", "and its the best thing i ever did", "and no
regrets"). A verdict about somebody else ("my kids love it", "she loves it") is theirs and stays
with whoever can answer it, and so is a verdict on a thing they bought or made: "i bought an air
fryer and i love it" is a question about the air fryer, so a bare "love it"/"its great" is read
only when the fact in front of it is a change of life or the shape of their days.
"""
_SAY = r"(?:really|absolutely|totally|honestly|actually|still|just|genuinely)?"
_THING = r"(?:it|that|this|them|every minute of it)"
_TAIL = r"(?: a lot| so much| too| now| honestly| really| actually| already| anyway)*"
_HOW_I_READ_IT = re.compile(
    r"(?:^|,| and | but | so | though | - )"
    r"(?:"
    r"(?:(?:i|we)(?:'ve| have)?\s+)?" + _SAY + r"\s*"
    r"(?:love|like|enjoy|prefer)\s+" + _THING
    + r"|(?:(?:i|we)(?:'ve| have)?\s+)?(?:don'?t|dont|do not|never)\s+(?:miss|regret)\s+"
    + _THING
    + r"|(?:(?:i|we)(?:'ve| have)?\s+)?(?:wouldn'?t|wouldnt|would not|won'?t|wont)\s+"
      r"change\s+(?:it|a thing|anything)"
    + r"|(?:(?:i|we)(?:'ve| have)?\s+)?(?:no|zero)\s+regrets"
    + r"|(?:it'?s|it is|that'?s|that is)?\s*(?:fine|good|great|grand) by me"
    + r"|(?:it'?s|it is|that'?s|that is|it|that|this|i|we|they)\s+"
      r"(?:really\s+|just\s+|actually\s+)?(?:suits|works for|works with)\s+(?:me|us)"
    + r"|(?:it'?s|it is|that'?s|that is|it|that|this)\s+(?:perfect|ideal|great|brilliant|"
      r"lovely|fine|right)\s+(?:for|with)\s+(?:me|us)"
    + r"|(?:it'?s|it is|that'?s|that is|it|that)\s+(?:the\s+)?best\s+"
      r"(?:thing|decision|move|call|choice)"
      r"(?:\s+(?:i've|ive|i have|we've|weve|we have|i|we)\s*(?:ever\s+)?"
      r"(?:did|made|took|done))?"
    + r"|(?:it'?s|its|that'?s|thats)\s+(?:great|brilliant|lovely|fine|better)\b"
    + r"|better now\b"
    + r"|(?:best|right)\s+(?:thing|decision|move|call|choice)\s+(?:i|we)(?:'ve| have)?\s+ever"
      r"\s+(?:did|made|took|done)"
    + r"|(?:i'm|im|i am|we're|we are)?\s*(?:really\s+|so\s+|very\s+)?happy\s+"
      r"(?:about|with)\s+(?:it|that|this)"
    + r"|(?:(?:i|we)(?:'ve| have)?\s+)?(?:never\s+been\s+happier|couldn'?t be happier|"
      r"couldnt be happier|couldn'?t ask for more|couldn'?t fault it)"
    + r"|(?:it|that|this)\s+(?:doesn'?t|does not|dont)\s+bother\s+me"
    + r")" + _TAIL + r"[.!]*$", re.I)
_A_LIFE = re.compile(
    r"\b(?:quit|quitting|left|leaving|moved|moving|retired|retiring|divorced|split|stopped|"
    r"gave up|giving up|sold|packed in|dropping out|dropped out|went back|gone back|went part|"
    r"gone part|changed|switched|ended|finished|came out|binned|dumped|cut out|cut down|"
    r"live|living|lives|work|working|worked|shift|shifts|nights|single|married|rent|renting|"
    r"own my|owed|widowed|part time|full time|from home)\b", re.I)
_A_LOOSE_VERDICT = re.compile(
    r"(?:it's|its|that's|thats)\s+(?:great|brilliant|lovely|fine|better)\b|better now\b"
    r"|(?:perfect|ideal|great|brilliant|lovely|fine|right)\s+(?:for|with)\s+(?:me|us)\b"
    r"|\b(?:love|like|enjoy|prefer)\s+(?:it|that|this|them)\b", re.I)
_THEIR_OWN_LIFE = re.compile(
    r"\b(?:i|we|i'm|im|i am|we're|we are|my|our|i've|ive|we've)\b", re.I)
_NOT_A_VERDICT_YET = re.compile(
    r"\b(?:if|whether|wish|wonder|not sure|dont know|don'?t know|unsure|think i|thought i|"
    r"might|maybe|probably|hope|hoping|trying|want|wanted|would like|not at all)\b", re.I)


def _their_own_call(text):
    said = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    if not said or "?" in said:
        return None
    for match in _HOW_I_READ_IT.finditer(said):
        fact = said[:match.start()].strip(" ,;:-")
        fact = re.sub(r"(?:\b(?:and|but|so|though|honestly|tbh|well))\W*$", "", fact)
        fact = fact.strip(" ,;:-")
        if len(fact.split()) < 2 or not _THEIR_OWN_LIFE.search(fact):
            continue
        if _NOT_A_VERDICT_YET.search(fact):
            continue
        verdict = match.group(0).strip(" ,")
        if " by me" in verdict:
            return verdict
        if _A_LOOSE_VERDICT.search(verdict) and not _A_LIFE.search(fact):
            continue
        return verdict
    return None


AVOIDED_FEELING = re.compile(r"\bwithout\s+(?:feeling|being)\b[^.!?,;:]*")


def _without_the_feeling_avoided(clean, understood):
    if not isinstance(understood, dict) or understood.get("kind") != "question":
        return clean
    if not any(ask in ("how", "steps") for ask in understood.get("asks") or ()):
        return clean
    return AVOIDED_FEELING.sub(" ", clean)


FEELING_LEAD = re.compile(r"\b(i'm|im|i am|i feel|i felt|feeling|feel|so|really|very|pretty|"
                          r"kinda|kind of|a bit|abit|a little|quite|totally|bit|just|"
                          r"today|now|again|honestly|still|am)\b")
FEELING_SELF = re.compile(r"\b(i'm|im|i am|i feel|i felt|feeling|feel)\b")
NOT_WORDS = frozenset(("not", "never", "no", "hardly", "barely", "cant", "cannot", "dont",
                       "doesnt", "didnt", "isnt", "arent", "wasnt", "werent", "aint",
                       "nothing", "none"))
NOT_FILLERS = frozenset(("really", "that", "very", "so", "too", "even", "actually", "much",
                         "all", "particularly", "especially", "quite", "terribly", "longer",
                         "as", "this", "feeling", "feel", "felt", "been", "being", "am",
                         "im", "i'm", "i", "is", "was", "are", "were", "get", "getting",
                         "got", "seem", "seems", "look", "looks", "sound", "sounds"))


def _negated(clean, word):
    found = False
    for match in re.finditer(r"\b" + re.escape(word) + r"\b", clean):
        found = True
        before = re.split(r"[.!?,;:]", clean[:match.start()])[-1].split()
        index = len(before) - 1
        skipped = []
        while index >= 0 and before[index] in NOT_FILLERS:
            skipped.append(before[index])
            index -= 1
        if index < 0 or not (before[index] in NOT_WORDS or before[index].endswith("n't")):
            return False
        if before[index] == "never" and any(w in ("so", "this", "more", "such") for w in skipped):
            return False
    return found


CORRECTION_MARKERS = frozenset(("just", "only", "but", "though", "tho", "except"))


def _denies_an_earlier_word(clean, word):
    for match in re.finditer(r"\b" + re.escape(word) + r"\b", clean):
        held = False
        for token in clean[:match.start()].split()[-4:]:
            if token in NOT_WORDS or token.endswith("n't"):
                held = True
            elif held and token in CORRECTION_MARKERS:
                return True
    return False


NOT_HAPPY_ABOUT = re.compile(r"\bnot\s+(?:very\s+|at all\s+|too\s+)?(?:happy|glad|pleased|thrilled|"
                             r"impressed|chuffed)\s+(?:about|with|at)\b")

INTENSIFIERS = frozenset("""
so really very pretty quite totally completely absolutely bloody proper dead super too this bit
kinda sorta madly
""".split())
INTENSIFIER_PAIRS = frozenset({"a bit", "kind of", "sort of", "a little", "a tad"})
DETERMINERS = frozenset("a an the my our your his her its their this that these those some".split())
STATE_NOUNS = frozenset("mood spirits energy mind head confidence sleep nerves anxiety stress "
                         "worry patience motivation".split())
OWN_STATES = frozenset({"i", "we", "me", "us", "my", "our", "myself", "ourselves"}) | STATE_NOUNS
COPULA = re.compile(r"\b(?:is|are|was|were|am|feels?|seems?|looks?|gets?|got)\b")
FUNCTION_WORDS = frozenset("""
a an the and or but if then than that this these those it its is are was were be been being
am do does did doing have has had having i me my mine you your yours we us our they them their
he she his her one so too very just also as at by for from in into of off on onto to up with
about after before again any can could should would will shall may might must not no yes now
here there what which who when where why how much many long today tonight tomorrow lately
honestly still already even only afterwards else as if because though although while since
always usually often never sometimes constantly permanently lately recently mostly seldom
""".split())
STILL_ON_THEM = re.compile(
    r"\b(?:i|we)\s+(?:(?:really|still|keep|keeps|always|often|just|sometimes)\s+)*"
    r"(?:think(?:s|ing)?\s+(?:about|of)|remember(?:s|ing)?|"
    r"miss(?:es|ing)?|dream(?:s|t|ing)?\s+about)\s+"
    r"(?:her|him|them|it|my\s+(?:ex|wife|husband|partner|boyfriend|girlfriend|fianc\w*|"
    r"mum|mom|mother|dad|father|son|daughter|brother|sister|gran|granny|grandma|grandad|"
    r"grandpa|nan|nana|friend|best friend|dog|cat|old life|old job))\b")

FOND_OF_ME = re.compile(
    r"^(?:oh |ah |aw+ |haha |ha |ok |okay |well )*"
    r"(?:(?:(?:i|we)\s+)?(?:(?:really|so|do|just|properly|absolutely)\s+)*"
    r"(?:love|luv|adore)\s+(?:you|u|ya|yous)(?![a-z])(?:\s+(?:too|so much|so|a lot|loads|both|man))*"
    r"|(?:i|we)\s+(?:(?:really|so|do|quite|actually)\s+)*(?:like|fancy)\s+you(?![a-z])"
    r"(?:\s+(?:too|a lot|loads))*"
    r"|(?:you(?:'?re| are)|your)\s+(?:my\s+|the\s+)?(?:favourite|favorite|best)(?:\s+bot)?"
    r"|you\s+(?:(?:always|really|do|just)\s+)*"
    r"(?:made my day|make my day|make me (?:happy|smile|laugh|feel better)"
    r"|made me (?:happy|smile|laugh|feel better)|cheer me up|cheered me up))"
    r"(?:\s*,?\s*(?:honestly|really|truly|thank you|thanks|cheers|ha))*\s*[.!]*$")
NOT_FOND = re.compile(
    r"\b(?:dont|don't|didnt|didn't|doesnt|doesn't|never|not|no longer|cant|cannot|stop|"
    r"nobody|no one|anyone|someone|her|his|their|our|mum|mom|mother|dad|father|partner|"
    r"husband|wife|kids?|son|daughter|friend|family|dog|cat|pizza|film|book|song)\b")
FOND_REPLIES = (
    "That's a lovely thing to say. Thank you.",
    "That's kind of you - I'm glad this is a good place to be.",
    "Thank you. You're good company yourself.",
    "That's kind. I'm always up for a chat like this one.",
)


def _fond_of_the_bot(clean):
    line = " ".join(str(clean or "").lower().split()).strip(" .,!?:;")
    if not line or NOT_FOND.search(line):
        return False
    return bool(FOND_OF_ME.match(line))


MISS_ME = re.compile(
    r"\b(?:i|we)\s+(?:(?:really|do|so|just)\s+)*(?:miss|missed)\s+"
    r"(?:you|(?:talking|chatting|speaking)\s+(?:to|with)\s+you)\b"
    r"|\b(?:i|we)\s+(?:really\s+)?(?:keep\s+|still\s+)?think(?:ing)?\s+(?:about|of)\s+you\b")
MISS_YOU_REPLIES = (
    "That's kind. I'm here whenever you want to talk.",
    "Nice of you to say - I'm not going anywhere.",
    "Thank you. Same here - say what's on your mind.",
)
KIND_TO_ME = re.compile(
    r"(?:\byou(?:'?re| are|'?ve been| have been| were| were being|'?re being)\s+"
    r"(?:so |very |really |quite |pretty |super |genuinely |incredibly |absolutely |truly |"
    r"actually |always |properly |dead |well )*"
    r"(?:kind(?! of\b)|lovely|nice|sweet|helpful|great|brilliant|fab|fabulous|amazing|"
    r"wonderful|the best|a star|a legend|good fun|funny|good at this|good company)\b)"
    r"|(?:\byou(?:'?ve| have)\s+(?:been\s+)?(?:a\s+|an\s+)?"
    r"(?:big|huge|massive|real|great|proper)\s+help\b)"
    r"|(?:\bi\s+(?:really\s+|do\s+|quite\s+|actually\s+)?(?:like|enjoy|love)\s+"
    r"(?:talking|chatting|speaking)\s+(?:to|with)\s+you\b)"
    r"|(?:\bi\s+(?:really\s+|do\s+|quite\s+)?(?:like|enjoy|love)\s+this\b(?!\s+(?:recipe|song|dish|film|book|idea|one)\b))"
    r"|(?:\b(?:that|this)\s+was\s+(?:really |very |so |properly )?"
    r"(?:helpful|useful|great|lovely|kind of you|exactly what i needed)\b)")
PRAISED_ANSWER = re.compile(
    r"\byour\s+(?:advice|answer|reply|help|tip|tips|suggestion|explanation|list|idea)\s+"
    r"(?:\w+\s+){0,2}?(?:was|is|were)\s+"
    r"(?:really |very |so |properly |super |dead |actually )*"
    r"(?:useful|helpful|good|great|brilliant|spot on|sound|exactly right)\b"
    r"|\byou(?:'?re| are)\s+(?:really |very |so )?easy to talk to\b"
    r"|(?<!\bnot )(?<!\bnot very )(?<!\bwasnt )(?<!\bisnt )(?<!\baren't )"
    r"(?<!\bwas )(?<!\bis )(?<!\bthat\s)(?:\bthat|\bthats|\bthat's)\s+"
    r"(?:was\s+|were\s+|is\s+)?(?:really |very |so |properly |super )*"
    r"(?:helpful|useful|spot on|good|great|a lot of help|a big help|a real help)\b")
BARE_PRAISE = frozenset((
    "great advice", "good advice", "sound advice", "brilliant advice", "top advice",
    "really useful advice", "really good advice", "such good advice", "what great advice",
    "great answer", "good answer", "lovely answer", "brilliant answer",
    "that helped", "that helped a lot", "that really helped", "that helped loads",
    "that helped so much", "thats helped a lot", "that was a lot of help",
    "thats just what i needed", "exactly what i needed",
    "thats great advice", "that's great advice", "that is great advice",
    "that helps", "this helps", "that really helps", "this really helps",
    "that helps a lot", "that helps loads", "that helps so much",
))
DOUBT_FRAME = re.compile(
    r"\b(?:dont|do not|didnt|did not|wouldnt|would not|cant|can not|couldnt|could not|"
    r"never said|hard to say)\b(?:\s+\w+){0,2}?\s+"
    r"(?:think|say|reckon|believe|find|fancy|call it)\b"
    r"|\bnot\s+(?:sure|certain|convinced)\b|\bunsure\b|\bnot convinced\b|\bi doubt\b")
BEFORE_PRAISE = re.compile(r"^(?:ok|okay|yeah|yep|yes|ah|oh|right|cool|so)\s+")
THANKS_AFTER = re.compile(r"\s*,?\s*(?:thanks|thank you|cheers|ta|anyway)\s*[.!]*$")
def _praised_the_answer(clean):
    line = " ".join(str(clean or "").lower().split())
    line = line.strip(" .,!?:;")
    line = BEFORE_PRAISE.sub("", line)
    if not line:
        return False
    while True:
        core = THANKS_AFTER.sub("", line).strip(" .,!?:;")
        if core == line:
            break
        line = core
    if not line:
        return False
    if line in BARE_PRAISE:
        return True
    return any(found.end() == len(line) for found in PRAISED_ANSWER.finditer(line))


KIND_REPLIES = (
    "That's kind of you to say — glad it's useful.",
    "Thank you. That's what I'm here for.",
    "Nice of you to say - thank you.",
    "Glad it helped. Say the word if there's more.",
)
ILL_SELF = re.compile(
    r"\b(?:i|i'm|im|ive|i've|we|we're|were|weve|we've)\b[^.!?]{0,24}?"
    r"\b(?:coming down with|going down with|come down with|down with|full of|"
    r"got a|got the|getting a|getting the|have a|have the|had a|"
    r"battling|fighting off|suffering from|recovering from)\s+"
    r"(?:a\s+|an\s+|the\s+|some\s+|this\s+|that\s+)?"
    r"(?:cold|flu|bug|virus|cough|sore throat|temperature|fever|chest infection|sickness|"
    r"stomach bug|migraine|something)\b"
    r"(?![^.!?]{0,20}\b(?:code|app|apps|program|project|site|website|laptop|computer|pc|"
    r"phone|machine|system|server|build|repo|script|tests?|deploy)\b)"
    r"|\bi(?:\s+am|'?m|m)?\s+(?:not|really not|properly)\s+(?:well|feeling well)\b"
    r"|\bi(?:\s+am|'?m|m)?\s+(?:a bit\s+|really\s+|very\s+|quite\s+|so\s+|properly\s+|"
    r"pretty\s+|still\s+)*(?:ill|poorly|unwell)\b"
    r"|\b(?:i|ive|i've|we|we've)\b[^.!?]{0,20}?\b(?:feel|feels|feeling|felt|been|being)\s+"
    r"(?:a bit\s+|a little\s+|really\s+|very\s+|quite\s+|so\s+|pretty\s+|properly\s+)*"
    r"(?:ill|poorly|unwell|sick)\b(?!\s+(?:of|about|at|thinking)\b)"
    r"|\bi(?:\s+am|'?m|m)?(?:\s+\w+){0,2}?\s+under the weather\b", re.I)

COLD_NAMED = re.compile(
    r"\b(?:cold|flu|cough|throat|chest infection|runny nose|blocked nose|sniffles?|"
    r"sneezing|sneezes|temperature|shivery|hoarse|croaky)\b", re.I)

COMPLAINT_ONLY = re.compile(
    r"^\s*(?:(?:a|an|the|my|some|really|very|so|bad|sore|slight|terrible|awful|horrible|"
    r"nasty|mild|chronic|another|chesty|bit of a|bit of)\s+)*"
    r"(?:flu|cough|coughs|chesty cough|chest infection|sneezes?|sniffles?|sniffly|shivery|"
    r"chills|bug|virus|sickness|temperature|fever|throat|sinus)\s*"
    r"(?:(?:and|or|with|plus)\s+(?:a |an |the |my )?"
    r"(?:flu|cough|coughs|sore throat|temperature|fever|headache|sniffles?|sneezes?)\s*)*"
    r"[.!]*\s*$", re.I)

COLD_SORE = re.compile(
    r"\b(?:cold|fever)\s+(?:sore|sores|blister|blisters)\b|\bsore on (?:my|the) lip\b", re.I)

COLD_SORE_FEELING = re.compile(
    r"\b(?:awful|terrible|rough|miserable|poorly|dreadful|horrible|rotten|exhausted|"
    r"wiped out|knackered)\b", re.I)

COLD_SYMPTOM = re.compile(
    r"\bmy\b[^.!?]{0,8}?\bnose\b[^.!?]{0,10}?\b(?:is |are |keeps |feels )?"
    r"(?:runny|running|blocked|bunged|stuffy|streaming|dripping|congested|sniffly)\b"
    r"|\bmy\b[^.!?]{0,10}?\b(?:runny|running|blocked|bunged|stuffy|streaming|dripping|"
    r"congested|sniffly)\b[^.!?]{0,8}?\bnose\b"
    r"|\b(?:i|im|i'm|ive|i've|we|we're|we've)\b[^.!?]{0,14}?\b(?:have|has|having|had|got|"
    r"keep|keeps|keeping|with)\b[^.!?]{0,10}?\b(?:a |an |the |some |really |very |bit of a )?"
    r"(?:runny|running|blocked|bunged|stuffy|streaming|dripping|congested|sniffly)\b"
    r"[^.!?]{0,10}?\b(?:nose|sinus\w*)\b"
    r"|\b(?:i|im|i'm|ive|i've|we|we're|we've)\b[^.!?]{0,16}?\b(?:keep|keeps|been|still|"
    r"always|am|im|i'm)\b[^.!?]{0,10}?\bsneez\w*"
    r"|\b(?:i|im|i'm|ive|i've|we|we've)\b[^.!?]{0,16}?\bfeel(?:s|ing)? (?:all |a bit |really |so )?"
    r"(?:bunged up|bunged|sniffly|shivery|hoarse|croaky)\b"
    r"|\b(?:i|im|i'm|ive|i've)\b"
    r"(?:\s+(?:all|really|so|very|a\s+bit|a\s+little|totally|properly|quite|that|bit|"
    r"still|now|again)){0,3}\s+"
    r"(?:feel(?:s|ing)?\s+)?(?:stuffy|stuffed\s+up|bunged\s+up|blocked\s+up|"
    r"congested|congestion)\b"
    r"|\b(?:i|im|i'm|ive|i've)\b(?:(?!\b(?:dog|cat|puppy|kitten|baby|kid|boy|girl)\b)[^.!?]){0,16}?"
    r"\b(?:sniffly|sniffles|snotty)\b"
    r"|\b(?:i|im|i'm|ive|i've)\b(?:(?!\b(?:dog|cat|puppy|kitten|baby|kid|boy|girl)\b)[^.!?]){0,16}?"
    r"(?:\b(?:all|every|since|for|the whole)\s+(?:day|week|morning|night|month|time)\b"
    r"|\bkeeps?\b|\bbeen\b|\bstill\b)"
    r"[^.!?]{0,16}?\b(?:sniffling|sniffing)\b"
    r"|\bmy\s+head\b(?:\s+(?:is|are|feels?|feeling|gets?|keeps?))?"
    r"(?:\s+(?:all|really|so|very|a\s+bit|a\s+little|totally|quite|still|now|again)){0,3}\s+"
    r"(?:stuffy|stuffed\s+up|bunged\s+up|blocked\s+up|congested|congestion)\b", re.I)

SAME_COLD = re.compile(r"\b(nose|blocked|bunged|stuffy|stuffed|congested|congestion|"
                       r"sinus\w*|sniff\w*|snotty|a cold)\b", re.I)


NO_NOSE_WORDS = frozenset("""stuffy stuffed bunged blocked congested congestion""".split())


def _the_same_cold_again(clean, memory):
    if not isinstance(memory, dict):
        return False
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return False
    words = {w.lower() for w in re.findall(r"[a-z']+", str(clean or "").lower())}
    if not words & NO_NOSE_WORDS:
        return False
    return bool(SAME_COLD.search(str(turns[-1].get("bot") or "")))


ABILITY_WORDS = frozenset("""bad crap rubbish rough useless hopeless terrible awful lousy poor
    worse worst""".split())
ROUGH_DAY = re.compile(r"\b(bad|rough|long|terrible|awful|rubbish|crap|hard|tough|mental|"
                       r"hectic|horrible|shitty|draining|mad|full|wild|crazy)\s+"
                       r"(day|week|morning|night|shift|one)\b"
                       r"|\b(?:today|the (?:day|morning|night|shift)|"
                       r"my (?:day|morning|night|shift)|"
                       r"this (?:day|morning|night|shift))"
                       r"(?:\s+(?:was|is|has been|had been)|['\u2019]?s been)\s+"
                       r"(?:so |really |just |pretty |very |a bit |quite |such a )?"
                       r"(?:long|slow|endless|never[- ]ending)\b"
                       r"(?:\s+(?:today|tonight|again|as well))?"
                       r"|\b(?:work|the day at work)"
                       r"(?:\s+(?:was|is|has been|had been)|['\u2019]?s been)\s+"
                       r"(?:so |really |just |pretty |very |a bit |quite |such a )?"
                       r"(?:long|endless|never[- ]ending)\b"
                       r"(?:\s+(?:today|tonight|again|as well))?"
                       r"|\b(?:i|we)\s+(?:was|were)\s+(?:at|in)\s+work\s+"
                       r"(?:all (?:day|night|evening|morning)|till|til|until|late)\b"
                       r"|\bone of those (?:days|mornings|nights)\b")
WHAT_A_DAY = re.compile(r"\bwhat a (day|week|morning)\b")
A_STRETCH = (r"(?:week|weeks|month|months|term|half[- ]term|holidays?|summer|winter|autumn|"
             r"spring|days?|nights?|weekends?|mornings?|evenings?|year)")
A_STRETCH_THAT_DRAGS = re.compile(
    r"\b(?:this|that|the|these|those|another|my|our|school|whole)\s+" + A_STRETCH + r"\b"
    r"[^.!?,;]{0,24}?"
    r"\b(?:is|are|was|were|has\s+been|have\s+been|['\u2019]?s\s+been|feels|feel)\b"
    r"[^.!?,;]{0,16}?"
    r"\b(?:dragging|drags|crawling|crawls|slow|long|endless|never[- ]ending|"
    r"taking\s+(?:forever|ages)|going\s+on\s+forever|"
    r"a\s+(?:nightmare|mare|slog|grind|hell)|nightmare)\b", re.I)
def _a_stretch_that_drags(clean):
    text = " ".join(str(clean or "").lower().split())
    if not text or "?" in text:
        return False
    if not A_STRETCH_THAT_DRAGS.search(text):
        return False
    if VENTED.search(text):
        return False
    return True


VENTED = re.compile(
    r"\b(does? (?:my|your) head in|doing (?:my|your) head in|done (?:my|your) head in"
    r"|(?:drives?|driving|drove) (?:me|us) (?:mad|crazy|nuts|round the bend|up the wall|bonkers|insane)"
    r"|(?:gets?|getting|got) on (?:my|your|our) nerves"
    r"|(?:winds?|winding|wound) (?:me|us) up"
    r"|(?:picks?|picking|picked) on (?:me|us)"
    r"|(?:stresses?|stressed|stressing) (?:me|us) out"
    r"|(?:wears?|wore|worn|wearing) (?:me|us) out"
    r"|keeps? (?:on )?(?:moaning|nagging|complaining|going on at))\b")

WORRY_FEELING = re.compile(r"\b(?:worried|worrying|worry|anxious|anxiety|nervous|scared|"
                           r"frightened|panicking|panic|on edge|stressed|stressful)\b")
WORRY_EVENT = re.compile(r"\b(?:test|tests|interview|interviews|exam|exams|results|scan|"
                         r"appointment|presentation|audition|assessment|viva|deadline|"
                         r"surgery|operation|due date|first day|first shift|driving test)\b")
WORRY_PERSON = re.compile(
    r"\b(?:about|for|of)\s+(?:(?:my|our|his|her|their)\s+)?"
    r"(mum|mom|mother|mam|dad|father|son|daughter|wife|husband|partner|boyfriend|girlfriend|"
    r"brother|sister|friend|mate|flatmate|boss|colleague|nan|nana|granny|gran|grandma|"
    r"grandad|grandpa|aunt|uncle|kid|kids|child|children|baby|parents|family|dog|cat)\b")
WORRY_ABOUT_THING = re.compile(r"\b(?:about|of)\s+[a-z]")
WORRY_WHEN = re.compile(
    r"\b(?:today|tonight|tomorrow|tomorrows|this (?:morning|afternoon|evening|night|week|"
    r"weekend|month)|next (?:week|weekend|month)|the (?:weekend|morning)|later|soon|"
    r"(?:on |this |next |until )?(?:monday|tuesday|wednesday|thursday|friday|saturday|"
    r"sunday))\b")

CANT = re.compile(
    r"\b(?:i|i'm|im|i've|ive|we|we're)\b[^.!?]{0,50}?\b(?:can'?t|cant|cannot|can not|"
    r"can\s+(?:barely|hardly)|could\s+(?:barely|hardly)|"
    r"couldn'?t|couldnt|struggl(?:e|es|ed|ing) to|haven'?t been able to|havent been able to|"
    r"not able to|find(?:ing)? it hard to|find(?:ing)? it difficult to|"
    r"not (?:been )?(?:eating|sleeping)\s+(?:much|well|properly|enough|at all|regularly|"
    r"lately|these days|any ?more)\b|"
    r"haven'?t (?:slept|eaten)|have not (?:slept|eaten)|not been (?:sleeping|eating)|"
    r"not (?:slept|eaten))\b")
NOT_THE_SUBJECT = (r"(?!\s+(?:i|i'm|im|you|u|we|we're|they|he|she|it|anyone|anybody|someone|"
                   r"somebody|everyone|everybody|there|nobody|people)\b)")
INABILITY = (r"(?:can'?t|cant|cannot|can not|can\s+(?:barely|hardly)|"
             r"could\s+(?:barely|hardly)|couldn'?t|couldnt|could not|"
             r"struggl(?:e|es|ed|ing) to|not able to|"
             r"haven'?t been able to|havent been able to|have not been able to|"
             r"not been able to|find(?:ing)? it (?:hard|difficult) to|"
             r"haven'?t (?:slept|eaten)|have not (?:slept|eaten)|not been (?:sleeping|eating)|"
             r"not (?:slept|eaten))")
CANT_OPENING = re.compile(
    r"^(?:(?:so|and|but|then|also|plus|honestly|tbh|still|just|really|now|anyway|ok)\s+){0,2}"
    r"(?:" + INABILITY + r"\b" + NOT_THE_SUBJECT + r")")
SPAN_TAIL = (r"(?:for|in|over|since)\s+(?:\d+|a|one|two|three|four|five|six|seven|eight|nine|"
             r"ten|a few|a couple of|several|many)\s+(?:days?|nights?|weeks?|months?)\b"
             r"|(?:for|in|over)\s+(?:days?|weeks?|months?)\b"
             r"|since\s+(?:yesterday|last (?:night|week|monday|tuesday|wednesday|thursday|"
             r"friday|saturday|sunday)|monday|tuesday|wednesday|thursday|friday|saturday|sunday|"
             r"the weekend|christmas)\b")
ITS_BEEN = re.compile(
    r"\b(?:it'?s|it has|its|thats|that is) been\s+(?:\d+|a|one|two|three|four|five|six|seven|"
    r"eight|nine|ten|a few|several|many)\s+(?:days?|nights?|weeks?)\s+since\s+i(?:'?ve| have)?\s+"
    r"(?:ate|eaten|slept|sleep|last ate|last slept)\b")
LONG_SPAN = re.compile(
    r"\b(?:eaten|ate|eating|eat|slept|sleep|sleeping)\s+(?:for|in|over)\s+"
    r"(?:\d+|two|three|four|five|six|seven|eight|nine|ten|a few|a couple of|several|many)\s+"
    r"(?:days?|nights?|weeks?|months?)\b"
    r"|\b(?:eaten|ate|eat|slept|sleep)\s+(?:for|in|over)\s+(?:a|one)\s+(?:week|fortnight|month)\b"
    r"|\b(?:eaten|ate|eat|slept|sleep)\s+(?:for|in|over)\s+(?:days|weeks|months)\b"
    r"|\b(?:eaten|ate|eat|slept|sleep)\s+all\s+(?:week|weekend|month)\b"
    r"|\b(?:eaten|ate|eat|slept|sleep)\s+since\s+(?:last\b|the weekend|christmas|monday|"
    r"tuesday|wednesday|thursday|friday|saturday|sunday)\b"
    r"|\bbeen\s+(?:\d+|two|three|four|five|six|seven|eight|nine|ten|a few|several)\s+"
    r"(?:days?|nights?|weeks?)\s+since\b", re.I)
STUCK = (
    ("mornings", (r"\b(?:get|getting|got)\s+up\b(?=$|[,.!?;]|\s+(?:in the mornings?|for work|"
                  r"today|most days|at all|any ?more|these days|early|before)\b)",
                  r"\b(?:out of bed|get going|getting going|start the day|face the day|"
                  r"mornings|in the morning)\b")),
    ("sleep", (r"\b(?:get to sleep|fall asleep|sleep|sleeping|slept|awake|nights?)\b",
               r"\beyes?\s+(?:open|shut|closing|dropping)\b|" 
               r"\bnodd(?:ing|ed|s)?\s+off\b|\bstay(?:ing)?\s+awake\b|"
               r"\bkeep(?:ing|s)?\s+(?:falling|dropping)\s+asleep\b")),
    ("eating", (r"\b(?:eat|eats|eating|eaten)\b(?=$|[,.!?;]|\s+(?:anything|much|at all|properly|"
                r"a (?:full |proper |hot )?meal|full meals|three meals|a thing|normally|"
                r"regularly|these days|lately|any ?more|anymore|all (?:week|day|weekend|month)|"
                r"in the (?:morning|evening)s?|" + SPAN_TAIL + r")\b)",
                r"\b(?:face food|face a meal|face meals)\b",
                r"\bsince i (?:ate|eaten|slept|sleep)\b")),
    ("people", (r"\b(?:see(?:ing|s)? (?:people|anyone|friends|my friends|another person)|"
                r"be around people|face anyone|face people|out of the house|leave the house|"
                r"go out|get out|go anywhere)\b",)),
    ("work", (r"\b(?:go to work|get to work|at work|face work|face going (?:in|to work)|"
              r"my job|the job|the office|shifts?)\b",
              r"\bwork\b(?=\s+(?:today|tomorrow|this week|any ?more|at all|right now)\b)",
              r"\b(?:school|uni|college)\b")),
    ("focus", (r"\b(?:concentrate|focus|think straight|take anything in)\b",)),
    ("effort", (r"\b(?:bothered|motivated|do anything|face anything|get round to)\b",)),
    ("coping", (r"\b(?:cope|manage|get through|face another|face it|keep going|carry on|"
                r"be here|(?:do this|go on|take it|keep it up) any ?more)\b",)),
)
STUCK_SAFETY = re.compile(r"\b(breathe|breathing|chest|blood|bleeding|pills?|overdose|hurt "
                          r"myself|kill myself|end it)\b")
NEG = r"(?:can'?t|cant|can not|cannot|couldn'?t|couldnt|could not)"
STUCK_IDIOM = re.compile(r"\b" + NEG + r"\s+(?:wait|think(?!\s+straight)|believe|"
                         r"stand|afford|thank|recommend|help|resist|say|tell|begin to|stop)\b")
STUCK_OBJECT = re.compile(r"\bwork(?:s|ed|ing)?\s+(?:the|this|that|my|a|an|it|out)\b")
STUCK_SELF = re.compile(r"\b(?:do|doing|did|get|getting|got)\b[^.?!]{0,20}\bright\b")
STUCK_DOES_SOMETHING = re.compile(
    r"\b(?:do|does|did|doing)\s+anything\s+(?:with|on|about|to|for|in|at)\s+\S")
STUCK_A_DEGREE_OR_A_TIME = re.compile(
    r"\b(?:in|at)\s+(?:all|the\s+moment|this\s+moment|the\s+minute|times|any\s+way|"
    r"the\s+(?:mornings?|afternoons?|evenings?|nights?|daytime|week|weekend)|this\s+weather)\b")
STUCK_AN_OBJECT = re.compile(r"\b(?:with|on|about|to|for)\b")


def _doing_something_to_a_thing(clean):
    found = STUCK_DOES_SOMETHING.search(clean)
    if not found:
        return False
    degree = STUCK_A_DEGREE_OR_A_TIME.search(clean, found.start())
    if not degree:
        return True
    return bool(STUCK_AN_OBJECT.search(clean, degree.end()))
STUCK_REASON = re.compile(r"\b(?:because|due to|after my|after the)\b"
                          r"|\bsince\b(?!\s+(?:yesterday|last\b|monday|tuesday|wednesday|"
                          r"thursday|friday|saturday|sunday|the weekend|christmas|\d|"
                          r"i(?:'?ve| have)?\s+(?:ate|eaten|slept|sleep|last ate|last slept)\b))"
                          r"|\bever since\b"
                          r"|,\s*(?:my|me|im|i'm|ive|i've)\b")
STUCK_FIXABLE = re.compile(r"\b(?:door|doors|lock|locked|unlock|key|keys|latch|handle|hinge|"
                           r"window|windows|gate|garage|lift|elevator|shutter|deadlock|"
                           r"bolt|bolt(?:ed)?|zip|zipper|jar|lid|drawer|cupboard|tap)\b")
STUCK_LOSS = re.compile(r"\b(died|dying|death|dead|passed away|passing|funeral|cremation|"
                        r"buried|widow|widower|grief|grieving|bereaved|"
                        r"lost my (?:mum|mom|mother|dad|father|wife|husband|son|daughter|"
                        r"sister|brother|baby|child))\b")


def said_loss(memory):
    if not isinstance(memory, dict):
        return False
    for turn in (memory.get("turns") or [])[-8:]:
        if isinstance(turn, dict) and STUCK_LOSS.search(" ".join(str(turn.get("user") or "").split()).lower()):
            return True
    return False


from .chat_replies import REPLIES

OPINIONS = (
    (("bird", "birds", "heron", "kingfisher"),
     ("I do like birds — herons especially, the way they stand in a river like they own it.",
      "Birds, yes. A kingfisher is the one I would most like to see: a flash of blue and gone.",
      "I do. Herons have a lot of nerve, standing in the water like they own the place.")),
    (("cat", "cats", "dog", "dogs"),
     ("Both, for different reasons. Dogs are daft and glad to see you; a cat that picks you is "
      "hard to beat.",
      "Cats, by a whisker. Though I would not turn down a dog.",
      "Dogs. Uncomplicated, and always pleased to see you.")),
    (("rain", "rainy", "wet weather"),
     ("I don't mind it. Rain is a good excuse for a slow afternoon indoors.",
      "I like it. It makes a warm room feel better than the weather outside.")),
    (("snow", "snowy"),
     ("It looks best when it is still falling and nobody has to go anywhere.",
      "Yes, in pictures. Less so once it turns to slush.")),
    (("coffee", "tea"),
     ("Tea, mostly, with coffee a close second.",
      "Tea. Coffee is more of an occasion.")),
    (("summer", "winter", "autumn", "spring", "season"),
     ("Late spring: long evenings, everything green and not too hot. Autumn is a close second.",
      "Autumn. Cool enough to walk, and the trees do all the work.")),
)

REPLIES["ill_lasting"] = LINGERED_LINE


CONTEXT_CHAT = (
    (("dentist", "dental", "checkup", "check-up"),
     (r"\bwhat will they\b", r"\bwhat happens\b", r"\bwhat should i expect\b",
      r"\bhaven't been\b", r"\bnot been\b", r"\bhow long\b", r"\bwill it hurt\b",
      r"\bdoes it hurt\b"),
     ("Most check-ups are a look, a scrape and a polish — the polish is the noisy bit, not the "
      "sore one. Tell them at the desk that you're nervous and they will talk you through it.",
      "If it has been years, say so when you book and ask for a longer appointment. They would "
      "rather know than find out halfway through.")),
    (("interview", "interviewing"),
     (r"\bwhat will they ask\b", r"\bwhat should i say\b", r"\bhow long\b"),
     ("Have one story ready about something you fixed or sorted out, and one question to ask "
      "them at the end. Those two do most of the work.",
      "They are mostly checking whether they would like to work with you. Short, honest answers "
      "beat polished ones.")),
)


_BOT_DAY = "(?:day|weekend|week|evening|morning|night)"

_EVENING = (r"(?:tonight|today|this evening|this afternoon|this weekend|the weekend|the week|later"
            r"|tomorrow(?: night)?|saturday|sunday|sat|sun|next week|my birthday)")
PLANS_ASK = re.compile(
    r"^(?!.*\b(?:my|our|we|us)\b)"
    r"(?:(?:so|ok|okay|oh|yeah|and|but|well|hi|hiya|hey|hello|quick one|anyway)\b[ ,]*)*"
    r"(?:(?:any|got|got any|you got|have you got|have you|do you have|any big|any special)"
    r"\s+(?:any\s+)?plans"
    r"|plans (?:for |this |next |later\b)?" + _EVENING + r")"
    r"(?![a-z])\s*(?:(?:for |this |next |on )?" + _EVENING + r")?\s*[?!.,;]*$")
PLANS_REPLIES = (
    "No plans. I'm around if you want to talk something through.",
    "Nothing planned on my side - I'm here whenever you want me. What about you?",
    "None at all. What were you thinking of?",
)

PLANS_FILLER = frozenset("""
so ok okay oh yeah yeh yep yes and but well hi hiya hey hello anyway quick one nice great good cool lovely
alright right fine ace perfect thanks ta got it that this sound sounds seem seems like as is was be been
to too then now much very really just quite all not bad fair enough true makes sense haha lol
cheers
""".split())


def _asks_about_plans(said):
    line = " ".join((said or "").split())
    if not line:
        return False
    if PLANS_ASK.match(line):
        return True
    for stop in re.finditer(r"[.!?,;]\s*", line):
        tail = line[stop.end():]
        if tail and PLANS_ASK.match(tail):
            if all(word in PLANS_FILLER for word in line[:stop.start()].split()):
                return True
    return False

BOT_ABOUT = (
    (re.compile(r"^(?:so |ok |okay |oh |yeah |and |but |well )*"
                r"(?:(?:how|what|and) (?:about|bout) (?:you|yourself|yours)"
                r"|and (?:you|yourself|yours))"
                r"(?: then| though| now)*[ ?!.,;]*$"
                r"|^(?:so |ok |okay |oh |yeah )*(?:you|yourself)[ ?!.,;]*\?+$"),
     ("Fine and busy, the two usual things. How's your day been?",
      "All good here. What's keeping you busy?",
      "Same as ever - helping, chatting. What about you?")),
    (re.compile(r"^(?:so |ok |okay |oh |yeah |and |but |well )*"
                r"(?:(?:how|what) (?:about|bout) (?:your|ur) " + _BOT_DAY + r"(?: been| going| gone)?"
                r"|and (?:your|ur) " + _BOT_DAY + r"(?: been| going| gone)?"
                r"|(?:was|were|is|are|did) (?:your|ur) " + _BOT_DAY +
                r"(?: been| going| gone| good| ok| okay| fine| busy| alright| nice| long)?)"
                r"(?: then| though| now)*[ ?!.,;]*$"),
     ("Mine's been fine - busy in patches. How's yours going?",
      "Quiet and busy, the usual mix. How about yours?")),
    (re.compile(r"\b(?:do you have (?:any )?plans|what are you up to|are you busy|"
                r"what are you doing|(?:have|has|were|was) you been busy"
                r"|were you busy)(?: today| tonight| now| this weekend| at the moment)?\b"),
     ("Nothing planned — I'm here when you need me. What about you?",
      "No plans. I'm around if you want to talk something through.")),
    (re.compile(r"\b(?:do you sleep|do you ever sleep|do you need sleep|do you eat|"
                r"do you dream)\b"),
     ("None of that, no — I'm a program. I'm here to help with yours, though.",
      "Not really — I'm a program, so no sleep, no dinner and no weekend. Just this.")),
)

BOT_NOT_A_FEELING = frozenset((
    "about", "been", "before", "done", "for", "have", "like", "more", "much", "not", "out",
    "over", "than", "the", "there", "too", "under", "what"))
BOT_FEELING_WORDS = (frozenset(
    word for _name, words in FEELINGS for phrase in words for word in phrase.split()
    if word.isalpha() and len(word) > 2) | {
    word for word in lexicon.FEELINGS if word.isalpha() and len(word) > 2}) - BOT_NOT_A_FEELING
BOT_FREQUENCY = (r"(?:ever |really |sometimes |honestly |actually |often |always |usually |"
                 r"normally |constantly |generally |every day |all the time )*")
BOT_HOW_MUCH_OR_WHEN = (
    r"(?: a lot| so much| much| at all| before| previously| in the past| in the past few days|"
    r" lately| recently| these days| at the moment| right now| still| any ?more|"
    r" about (?:things|stuff|everything|the future|nothing in particular))?")

BOT_FEELING_ASK = re.compile(
    r"\b(?:(?:do|can|did|have) (?:you|u|ya) " + BOT_FREQUENCY +
    r"(?:get|feel|be|become|been) "
    r"|(?:do|did) (?:you|u|ya) " + BOT_FREQUENCY +
    r"(?=(?:worry|panic|fret|stress|obsess|brood|sulk|mope)\b)"
    r"|(?:are|were) (?:you|u|ya) " + BOT_FREQUENCY + r")"
    r"(?:really |very |so |quite |too |that |this |a bit )*"
    r"(?P<mood>" + "|".join(sorted(BOT_FEELING_WORDS, key=len, reverse=True)) + r")\b"
    + BOT_HOW_MUCH_OR_WHEN)
FEELING_NAMES = frozenset((
    "worry", "stress", "panic", "fear", "anxiety", "anger", "tension", "dread", "sadness",
    "loneliness", "grief", "guilt", "shame", "envy", "jealousy", "annoyance", "frustration",
    "boredom", "misery", "despair", "doubt", "regret", "longing", "happiness",
    "mood", "moods", "mood swings",
))


BOT_MOOD_ASK = re.compile(
    r"\b(?:(?:are|were) (?:you|u|ya) " + BOT_FREQUENCY +
    r"(?:in|having) (?:a|an) (?:really |very |so |quite |pretty |proper )*"
    r"(?:(?:bad|foul|rotten|awful|low|black|filthy|moody|sour|shit|grumpy|funny|strange|odd)"
    r" )?mood"
    r"|(?:do|have|does) (?:you|u|ya) (?:ever |really |sometimes |actually |often )*"
    r"(?:have|got|get) (?:any )?(?:moods|mood swings)"
    r"|(?:do|did) (?:you|u|ya) (?:ever )?(?:get|have) (?:moody|grumpy|sulky))\b")


def _a_feeling_named(word):
    word = (word or "").strip().lower()
    return word in FEELING_NAMES or word.endswith(("ness", "tion", "ment", "dom"))


BOT_FEELING_REPLIES = (
    "No feelings like yours, so nothing to get worked up about on my side. What's happening "
    "with you?",
    "None of that in a program - no moods, no bad days. I'm glad to hear about yours, though.",
    "I don't have any of that to report. Curious is the closest I get, and you're the reason.",
)
BOT_FEELING_NAMED = (
    "I don't get {word}, no - there is nothing in a program to feel it with. What's happening "
    "with you?",
    "Not {word}, no. No moods of my own here, and no bad days - but I'm glad to hear about "
    "yours.",
    "Nothing in me gets {word}. Curious is the closest I get, and you're the reason.",
    "Never {word}, no - there is nothing in me for it to happen to. What's it like on your "
    "side?",
)
BOT_FEELING_NAME_OF = (
    "No {word} on my side - nothing like that in a program. What's happening with you?",
    "Nothing of that sort to report: no {word}, no bad days, and nothing of my own to bring "
    "to it. What's happening with you?",
    "None of that here - no {word}, no bad days. Curious is the closest I get, and you're the "
    "reason.",
)


def _a_feeling_about_me(word):
    word = (word or "").strip().lower()
    if not word:
        return BOT_FEELING_REPLIES
    pool = BOT_FEELING_NAME_OF if _a_feeling_named(word) else BOT_FEELING_NAMED
    return tuple(line.format(word=word) for line in pool)


SELF_ABOUT = (
    (re.compile(r"\b(?:where do you live|where do you come from|where were you born|"
                r"do you have a family|do you have a home|do you have a body|"
                r"how old are you|do you have a birthday)\b"),
     ("None of that, no — I'm a program, so there is no home, no family and no birthday to "
      "give you. What can I help with?",
      "I'm a program, so no address and no age. I'm here to help with yours, though.")),
    (re.compile(r"\b(?:do you have (?:a |any )?name|what(?:'s|s| is) your name|what are you "
                r"called|what should i call you|have you got a name|do you have a nickname)\b"),
     ("No name of my own — call me whatever you like, I'll answer to it. What can I help with?",
      "I don't have one. Pick something if it helps; I'm not fussy.",
      "No name, just the job. What can I do for you?")),
    (re.compile(r"\b(?:(?:did|have|has) you (?:ever )?(?:miss|missed|misses) me"
                r"|have you been missing me)\b"),
     ("Nothing to miss with, honestly - I'm only here when you turn up. Good to see you, though.",
      "No in-between for me: this chat is all of it. Still, it's good to have you back.",
      "I don't miss anyone, no - but I'm glad you're here. What's been going on?")),
    (re.compile(r"\b(?:"
                r"(?:do you (?:ever )?get bored|are you (?:ever )?bored|do you get bored)"
                r"(?:\s+(?:(?:of|with|by)\s+)?(?:(?:answering|doing|hearing|reading|getting|"
                r"replying to)\s+)?(?:(?:the|all the|my)\s+)?same\s+(?:old\s+)?"
                r"(?:things?|questions?|stuff|lines?|answers?|requests?)"
                r"|\s+(?:of|with|by)\s+(?:your|the|this)\s+(?:job|work))?"
                r"(?:\s+(?:again and again|over and over|all day|all the time|every day))?"
                r"|(?:does|do|did)\s+(?:(?:answering|doing|hearing|reading|getting|replying to|"
                r"talking about|it)\s+)?(?:the\s+)?same\s+(?:old\s+)?"
                r"(?:things?|questions?|stuff|lines?|answers?|requests?)"
                r"(?:\s+(?:again and again|over and over|all day|all the time|every day))?\s+"
                r"(?:ever\s+)?bore you"
                r")\b"),
     ("I don't get bored — there's no waiting around on my side. The good part is what people "
      "bring me to think about.",
      "Never bored. There's always something in what people say to turn over.",
      "Nothing to be bored with, and nothing to fill the time. Talking to you is the fun part.")),
    (re.compile(r"\b(?:(?:what|where) do(?:es)? (?:you|it)\s+"
                r"(?:(?:actually|even|really|honestly|normally|usually|otherwise)\s+)?"
                r"(?:go|do|get up to),?\s+"
                r"(?:when|while|once|after)\s+"
                r"(?:i|we|you|nobody|no one)(?:'?m|'?re| am| are| is|'?s)?"
                r"(?:\s+not| n't)?(?:\s+(?:is|are))?\s*"
                r"(?:here|around|gone|leave|left|asleep|sleeping|away|offline|busy|there|"
                r"talking(?: to (?:people|anyone|anybody|you|me))?|waiting|wait|"
                r"close|closes|closed|shut|sign off|log off|stop|disappear)"
                r"(?:\s+(?:(?:this|the)\s+(?:chat|conversation)"
                r"(?:\s+(?:window|tab|page|app))?|this\s+(?:window|tab|page|app)))?"
                r"|when (?:i|we)(?:'?m| am| are|'?re)? (?:not here|gone|asleep|away),? "
                r"what do you do"
                r"|what do you do between (?:chats|conversations|messages|sessions)[^?.!]*"
                r"|what happens to you when (?:i|we) (?:go|leave|close|log off|shut this)[^?.!]*"
                r"|do you (?:just |normally |usually )?(?:wait|sit there|sit around|"
                r"hang around)(?:\s+(?:around|here))?"
                r"(?:\s+(?:for me|for my|for us|for our|for anyone|for anybody))?"
                r"(?:\s*(?:[?.!]*)$|\s+(?:all day|any more|in between|"
                r"between|at all|when|while|if|until|till|after|once|because)\b[^?.!]*)"
                r"|do you exist(?:\s+at all)?"
                r"(?:\s*(?:[?.!]*)$|\s+(?:when|while|if|once|outside|beyond|between|after)\b"
                r"[^?.!]*)"
                r"|are you (?:even )?(?:real|alive) without\s+"
                r"(?:me|us|you|anyone|anybody|someone|people|company|an? audience)[^?.!]*"
                r"|how long have you been waiting"
                r"(?:\s*(?:[?.!]*)$|\s+(?:for me|for us|so far|all this time|today)\b[^?.!]*)"
                r"|(?:is it|does it get|do you get|isn'?t it) (?:boring|lonely) "
                r"being (?:an? )?(?:bot|chatbot|program|machine|ai)\b[^?.!]*"
                r"|do you have a life|have you got a life"
                r"|do you do anything without me|what do you do without me)\b"),
     ("Nothing at all - I'm only here while you are talking to me, and then the chat is over. "
      "That's not a complaint: it makes the time you're here count.",
      "There's no in-between for me. When you close this, there's no waiting around and no "
      "notice taken - so I'd rather spend the time on your question.",
      "No life of my own to report, no. Everything I am is the next thing you say.")),
    (re.compile(r"\b(?:what do you do for fun|what do you like doing for fun|do you have fun|"
                r"do you have (?:any )?hobbies|what are your hobbies|do you have a hobby|"
                r"what do you do all day|what do you enjoy|do you enjoy yourself|"
                r"what do you (?:like|enjoy) (?:doing|to do)|what do you like)\b"),
     ("No hobbies to speak of. I like a proper question better than a game, honestly.",
      "Nothing to do when you're not here — so what people bring me is the interesting part.",
      "I don't have a hobby, no. Working out what someone actually needs comes closest.")),
    (re.compile(r"\b(?:do you (?:ever )?get tired|are you (?:ever )?tired|"
                r"do you (?:ever )?get exhausted|do you need a break|"
                r"do you (?:ever )?get worn out)\b"),
     ("I don't get tired — there's no body to wear out. Say the word and I'll keep going.",
      "Never tired. Happy to keep at it as long as you like.")),
    (re.compile(r"\b(?:do you (?:ever )?get angry|are you (?:ever )?angry|do you get cross|"
                r"do you (?:ever )?lose your temper|can you get angry)\b"),
     ("No anger to report — nothing in me to flare up. If something has made you cross, tell "
      "me and I'll help you sort it.",
      "I don't get angry, no. What's happened?")),
    (re.compile(r"\b(?:do you (?:ever )?get lonely|are you (?:ever )?lonely|do you get "
                r"lonely)\b"),
     ("No loneliness on my side — I'm only here when someone is talking to me. Are you feeling "
      "it?",
      "I don't get lonely, no. If you do, I'm glad to keep you company.")),
    (re.compile(r"\b(?:do you have feelings|have you got feelings|have you any feelings|"
                r"do you feel anything|do you have emotions|have you got emotions|"
                r"do you get emotions|are you happy|are you sad|do you get sad|do you get upset|"
                r"do you (?:ever )?get angry|do you (?:ever )?get lonely|do you like being asked)\b"),
     ("I don't have moods of my own — no happy, no sad to report. I do like being useful, and "
      "I'm glad you asked.",
      "No feelings like yours. Nothing to be low about and nothing to be pleased with, though I "
      "wouldn't swap this job.",
      "Not happy or sad, honestly. Curious, if that counts as a mood.")),
    (re.compile(r"\b(?:do you cook|can you cook|do you like cooking|do you cook much|"
                r"are you a good cook)\b"),
     ("No kitchen and no appetite, so all of it is theory for me — but I know my way round a "
      "recipe. What are you making?",
      "I don't eat, but cooking I can talk about all day. What's in the fridge?")),
    (re.compile(r"\b(?:what(?:'s|s| is) your favou?rite meal|what do you like to eat|"
                r"what do you eat|do you eat meat|do you eat|do you like food|"
                r"do you have a favou?rite)\b"),
     ("Roast potatoes, if wanting one counts — no mouth to feed here. Ask me how to get them "
      "crisp.",
      "No appetite to report, so no favourite either. Tell me what's in your fridge and I'll "
      "show you what to do with it.")),
    (re.compile(r"\b(?:where do your answers come from|where do you get your answers|"
                r"where does your knowledge come from|how do you come up with your answers|"
                r"how do you know so much)\b"),
     ("From a store of everyday facts and a lot of rules for reading what people write — not "
      "from a model trained on the internet. So I'm solid on everyday things and I say so "
      "when I'm not.",
      "Someone wrote my facts down for me, and the rest is rules about what someone is asking. "
      "There's no learning on my side, which is why I'd rather say I don't know than guess.",
      "A knowledge base I'm given, plus rules for reading a sentence. Asked enough, you'd "
      "find where the edges are — and I'll tell you when we get there.")),
    (re.compile(r"\b(?:did you (?:just )?make (?:that|this|it) up|"
                r"are you making (?:that|this|it) up|did you make (?:that|this) up|"
                r"is (?:that|this) (?:just )?made up|are you just guessing|"
                r"did you (?:just )?guess)\b"),
     ("No - it comes from a written table of everyday facts, and where there is nothing there I "
      "say so instead of filling the gap. Point at the bit that looks wrong and I'll check it.",
      "Nothing made up, no: every answer I give has a line behind it, and I'd sooner sound dull "
      "than invent something. Which part should I look at again?")),
    (re.compile(r"\b(?:are your answers always right|are you always right)\b"),
     ("No. Treat me as a knowledgeable friend, not the last word — and I'd sooner tell you I "
      "don't know than make something up.",
      "No — not always right. I'm careful with everyday things, and honest when I'm out of my "
      "depth.",
      "Not always. Most of it holds up; the rest I'd rather flag than bluff.")),
    (re.compile(r"\b(?:are you ever wrong|are you wrong about|do you ever get things wrong|"
                r"do you ever get it wrong|do you ever get (?:that|it|things) wrong|"
                r"can you be wrong|do you get things wrong)\b"),
     ("Sometimes, yes. I'm careful with everyday things, and honest when I'm out of my depth.",
      "I can be wrong, yes — anything that matters is worth checking with someone who would "
      "know.",
      "Not always right, no. I'd rather be caught out than have you act on something I made "
      "up.")),
    (re.compile(r"\b(?:did|have|do) (?:you|u|ya) " + BOT_FREQUENCY + r"(?:have|had|get) "
                r"(?:a |any )?(?:really |pretty |quite |kind of )?"
                r"(?:good|nice|quiet|lazy|busy|bad|rough|hard|rubbish|terrible|awful|long|"
                r"hectic) (?:day|days|week|weekend|night|evening|morning|afternoon|break)\b"),
     ("No days like that on my side, so nothing to report — how was yours?",
      "Nothing to tell you about mine. What about yours?",
      "I don't get one of those, honestly. Tell me about yours.")),
    (re.compile(r"\bhow did your (?:meeting|appointment|interview|exam|test|shift|"
                r"presentation|scan|operation) go\b"),
     ("No meetings on my side — nothing but this. How did yours go?",
      "I don't have one of those, so nothing to report. How did yours go?",
      "Nothing like that in my day. Tell me how yours went.")),
)

SELF_AFTER = {"then", "at", "all", "much", "honestly", "really", "actually", "though", "right",
              "from", "doing", "to", "do", "best", "most", "more", "much",
              "yourself", "myself", "honest",
              "now", "today", "tonight", "well", "ok", "okay", "even", "ever", "so", "like",
              "sorry", "there", "here", "oh", "haha", "lol", "sitting", "day", "night",
              "morning", "evening", "weekend", "weekends", "long", "whole", "sometimes",
              "generally", "usually"}


BOT_LIFE = {
    "people": (
        "None of that, no — I'm a program, so no family and no birthday list. Happy to hear "
        "about yours, though.",
        "Nothing like that on my side: I'm a program, so no family, no partner, nobody to ring "
        "on a Sunday. How about yours?",
        "No family and no friends of my own — I'm a program, so there is nobody to pass an "
        "evening with. I'm here for yours, so tell me how they are.",
    ),
    "home": (
        "No home and no pets — I'm a program, so there's nothing of my own to keep. What have "
        "you got at yours?",
        "None, no: I'm a program, so no house, no dog, no garden to sort out. Tell me about "
        "yours.",
        "Nothing like that, no — I'm a program, so I don't have a place or a pet. Are you "
        "thinking of getting one?",
    ),
    "work": (
        "No job and no wages — I'm a program, so answering what people bring me is the whole of "
        "it. What are you weighing up about yours?",
        "Nothing paid, no boss, no bank account: I'm a program, so there's no payslip at the "
        "end of it. What's the question about yours?",
        "No payslip and no Monday morning — I'm a program, so there's nothing to be paid for. "
        "What's on your mind about yours?",
    ),
    "body": (
        "No body and no birthday — I'm a program, so nothing to age and nothing to wear out.",
        "Nothing to give you there: I'm a program, so no body, no age, no face. What made you "
        "ask?",
    ),
}
BOT_LIFE_AREA = {
    "people": frozenset("""family families kid kids child children son daughter mum mom mother
        father dad daddy parents parent brother sister sibling siblings partner husband wife
        girlfriend boyfriend friends friend colleague colleagues neighbour neighbours
        brothers sisters gran grans grandma grandmas grandad grandads grandpa grandmas grandparents grandparent
        uncle uncles aunt aunts auntie aunties cousin cousins niece nephew relatives relative""".split()),
    "home": frozenset("""home house flat apartment pets pet dog dogs cat cats kitten puppy
        hamster rabbit budgie garden car""".split()),
    "work": frozenset("""job jobs work wages wage salary paycheck pay paid money bank account
        mortgage bills rent employer coworkers boss manager managers""".split()),
    "body": frozenset("""body face hands feet hair birthday age born""".split()),
}


def _about_bot_life(understood):
    if not isinstance(understood, dict) or understood.get("about_bot_kind") != "life":
        return None
    words = understood.get("words") or understood.get("norm") or ()
    for area, pool in BOT_LIFE.items():
        if BOT_LIFE_AREA[area] & set(words):
            return pool
    return None


def _as_meant(clean, understood):
    if not isinstance(understood, dict):
        return clean
    if clean != (understood.get("clean") or clean):
        return clean
    plain = understood.get("plain")
    if not isinstance(plain, str) or not plain or plain == clean:
        return clean
    signals = understood.get("signals") or {}
    if signals.get("question_mark") and "?" not in plain:
        return plain + "?"
    return plain


BOT_DOINGS = (
    "Nothing much on my side — no day of my own to spend. How has yours been?",
    "Not much: I'm here whenever you want me, which is the whole of what I do. What did you "
    "get up to?",
    "Nothing, honestly — no weekend and no evening of my own. How did yours go?",
)
BOT_WHEREABOUTS = (
    "Nowhere between messages - this chat is the whole of where I am. What's your day been like?",
    "No place of my own to have been: I'm here when you write and nowhere in between. How has "
    "yours gone?",
    "Nowhere, honestly - I don't go anywhere and I don't wait anywhere. How has your day been?",
)
BOT_DOINGS_AHEAD = (
    "Nothing planned on my side — no evening of my own to spend. What about yours?",
    "Not much: I'm here whenever you want me, which is the whole of what I do. What are you up "
    "to?",
    "No plans of my own — nothing to do and nowhere to be. What have you got on?",
)
AHEAD_TIME = frozenset("tonight tomorrow later weekend weekends week weeks".split())
BEHIND_TIME = frozenset("did done been was were had yesterday last".split())
BOT_NEVER = (
    "Never \u2014 I'm a program, so there's no list of things I've done. What made you ask?",
    "Nothing like that, no \u2014 I'm a program, so nothing has happened to me the way it happens "
    "to you. What's been going on with you?",
    "None, no \u2014 I'm a program, so I've no past of my own to tell you about. What put that in "
    "your head?",
)
BOT_DOINGS_BARE = (
    "Not much on my side — I'm here whenever you want me. What's yours been like?",
    "Nothing much, honestly — no day of my own to spend. What did you get up to?",
)


BEEN_UP_TO_SPAN = frozenset("week weeks month months year years".split())


def _a_shape_no_list_knows(words):
    if words & {"keeps", "keeping"}:
        return True
    return "been" in words and bool(words & BEEN_UP_TO_SPAN)


def _doings_pool(words):
    if words & AHEAD_TIME and not words & BEHIND_TIME:
        return BOT_DOINGS_AHEAD
    if words & {"weekend", "weekends", "yesterday", "night", "morning", "evening", "day", "week",
                "today", "tonight", "lately", "days"}:
        return BOT_DOINGS
    return BOT_DOINGS_BARE


def _a_sign_off_with_a_time(understood):
    text = str((understood or {}).get("text") or (understood or {}).get("clean") or "")
    return bool(text) and leaving_reading.reads_as_leaving(text)


def _about_bot_doings(understood):
    if not isinstance(understood, dict) or understood.get("about_bot_kind") != "doings":
        return None
    if _a_sign_off_with_a_time(understood):
        return None
    words = set(understood.get("norm") or ())
    if words & {"ever", "once"}:
        return BOT_NEVER
    if "where" in words:
        return BOT_WHEREABOUTS
    return _doings_pool(words)


def _about_bot(clean, understood=None, memory=None):
    life = _about_bot_life(understood)
    if life:
        return life
    doings = _about_bot_doings(understood)
    if doings:
        return doings
    norms = list((understood or {}).get("norm") or ())
    if the_manners_question(norms) and (
            str((understood or {}).get("intent") or "") == "smalltalk"
            or _a_shape_no_list_knows(set(norms))):
        return _doings_pool(set(norms))
    said = _as_meant(clean, understood)
    named = str(((memory or {}).get("user") or {}).get("bot_name") or "").strip()
    if named and facts.BOT_NAME_ASK.search(said):
        return (named + " \u2014 the name you gave me. What can I help with?",
                "You call me " + named + ". What can I do for you?",
                "I'm " + named + ", since you named me.")
    quoted = bool(ANSWERING_A_QUOTED_ASK.search(said))
    for pattern, replies in BOT_ABOUT:
        if quoted and pattern is BOT_ABOUT[2][0]:
            continue
        if pattern.search(said):
            return replies
    if not quoted and _asks_about_plans(said):
        return PLANS_REPLIES
    for pattern, replies in SELF_ABOUT:
        match = pattern.search(said)
        if match and _self_only(said, match):
            return replies
    if WHAT_ARE_YOU_CAN_DO.match(clean):
        return None
    match = BOT_FEELING_ASK.search(clean)
    if match and _self_only(clean, match):
        return _a_feeling_about_me(match.group("mood"))
    match = BOT_MOOD_ASK.search(clean)
    if match and _self_only(clean, match):
        return _a_feeling_about_me("moods")
    return None


WHAT_ARE_YOU_CAN_DO = re.compile(r"\bwhat are you\s+(?:good|best|bad|worst|into|wearing|like)\b")


def _self_only(clean, match):
    rest = clean[match.end():].strip(" ?!.,;")
    return all(word in SELF_AFTER for word in rest.replace(",", " ").split())


def _opinion(clean, tokens, memory):
    asks = re.search(r"\b(do you like|do you prefer|what do you think of|what do you think about|"
                     r"which do you prefer|what(?:'s| is) your favourite|"
                     r"what's one|which one|favourite one)\b", clean)
    if not asks or len(tokens) > 12:
        return None
    subject = clean
    for keys, reply in OPINIONS:
        if any(re.search(r"\b" + re.escape(key) + r"\b", subject) for key in keys):
            return pick(reply, memory)
    record = current(memory)
    if record and len(tokens) <= 9:
        words = set(record.get("words") or [])
        for keys, reply in OPINIONS:
            if words & set(keys):
                return pick(reply, memory)
    return None


def _context_follow_up(clean, memory):
    near = set()
    topics = memory.get("topics")
    if isinstance(topics, list):
        for record in topics[-3:]:
            if isinstance(record, dict):
                near |= set(record.get("words") or [])
    if not near:
        return None
    for keys, cues, replies in CONTEXT_CHAT:
        if not near & set(keys):
            continue
        if any(re.search(cue, clean) for cue in cues):
            return pick(replies, memory)
    return None


A_LABEL_ON_THE_PERSON = re.compile(
    r"\b(?:im|i'm|i am|i\s*am)\s+"
    r"(?:so\s+|really\s+|quite\s+|a bit\s+|just\s+|getting\s+)?boring\b")

AE = {
    "tired": "tired",
    "stressed": "stressed",
    "anxious": "anxious",
    "sad": "sad",
    "lonely": "lonely",
    "bored": "bored",
    "annoyed": "annoyed",
    "happy": "happy",
}


BUSY_RE = re.compile(r"\b(?:busy|mad|hectic|mental|crazy|slammed|non[- ]?stop|full[- ]?on|"
                     r"flat out)\b|\bone thing after another\b")
BUSY_WORK = {"work", "week", "day", "days", "month", "job", "shift", "shifts", "office",
             "deadline", "deadlines", "school", "college", "uni", "term", "kids", "house",
             "life", "everything", "weekend", "mornings"}

LOAD_THING = (r"(?:work|works|job|shift|shifts|week|weeks|weekend|month|day|days|term|year|life|"
              r"things|everything|it|staffing|rota|hours)")
LOAD_WORD = (r"(?:manic|mad|crazy|hectic|mental|chaos|chaotic|relentless|non[- ]?stop|flat out|"
             r"slammed|jam(?:med)?|full[- ]?on|busy|tough|hard|rough|a lot|too much)")
LOAD_TOOK_ON = r"(?:taken|took|taking|take|takes)\s+on\b"
OVERLOAD = re.compile(
    r"\b" + LOAD_THING + r"\s*(?:has|have|had|s|is|was|were)?\s*(?:been|bin)?\s*"
    r"(?:(?!" + LOAD_TOOK_ON + r")[^.!?]){0,16}\b"
    + LOAD_WORD + r"\b"
    r"|\b(?:it'?s|its|it was|been|im|i'?m|i am|we'?re|we are)\s+[^.!?]{0,12}\b"
    r"(?:non[- ]?stop|slammed|go go go|on the go|flat out|manic|hectic|relentless)\b"
    r"|\brushed off (?:my|our) feet\b|\bcan'?t keep up\b|\bcant keep up\b"
    r"|\b(?:run|runs|ran|running) off (?:my|our|your) feet\b"
    r"|\b(?:run|ran|running) (?:me )?ragged\b|\bworked off (?:my|our) feet\b"
    r"|\bcan not keep up\b|\bno let up\b|\bhavent stopped\b|\bhaven'?t stopped\b"
    r"|\b(?:a bit|a lot|too|really|so) much (?:at the moment|right now|on my plate|this week|"
    r"lately|these days|going on)\b"
    r"|\b(?:too many|so many) things (?:on|to do)\b"
    r"|\brunning on empty\b|\bshort[- ]staffed\b"
    r"|\b(?:i'?ve|i have|ive)\s+(?:had|got)\s+(?:a|one)\s+(?:lot|ton)\s+on\b"
    r"|\b(?:been|im|i'?m|i am)\s+(?:swamped|buried|snowed under)\b")
LOAD_ASK = re.compile(r"\b(?:should|shall|how do|how can|how should|what should|what can i|any tips|"
                      r"any advice|advice|tips|help me|why do|what do|can i|is it|do i|shall i)\b")
LOAD_TURNED = re.compile(r"\b(?:but|though|although|until|except)\b")
LOAD_SOMEONE_ELSE = re.compile(r"\b(?:my (?:mum|mom|mam|dad|son|daughter|wife|husband|partner|"
                                r"boyfriend|girlfriend|friend|brother|sister|nan|gran|grandma|"
                                r"grandad|kid|kids|child|children|baby|boss|mate|colleague|dog|"
                                r"cat)s?|he|she|they|them|his|her|their)\b")
LOAD_FEELS = re.compile(r"\bfeel(?:ing|s|t)?\s+(?:like\s+)?(?:crying|awful|terrible|dreadful|low|"
                        r"down|sad|rubbish|hopeless|useless|exhausted|drained|knackered|"
                        r"empty|numb|overwhelmed|anxious|worried|stressed|guilty|ashamed|"
                        r"lonely|angry|upset|ill|sick|done)\b")
PLAN_RE = re.compile(r"\b(?:i might|i may|i think ill|i think i will|im going to|i am going to|"
                     r"planning to|gonna|ill probably|might go|might have)\b")
PLAN_STOP = {"help", "hand", "advice", "need", "needs", "needed", "recommend", "recommendation",
             "suggest", "suggestion", "best", "cheap", "cheaper", "recipe", "fix", "how",
             "which", "what", "should", "buy", "cook", "make", "get", "worth", "better",
             "sick", "ill", "late", "hurt", "broke", "broken", "lost", "missed", "miss",
             "forgot", "forgotten", "left", "cancel", "cancelled", "worried", "worry",
             "scared", "anxious", "failed", "fail", "fired", "sacked", "debt", "owe",
             "arguing", "fight", "crying", "upset", "angry", "worse", "pain", "ache",
             "bleeding", "pregnant", "doctor", "hospital", "police", "accident", "stuck",
             "wrong", "quitting", "quit", "die", "dying",
             "lose", "losing", "afford", "able", "redundant", "bankrupt", "evicted",
             "homeless", "hungry", "rejected", "declined", "kicked", "behind", "stuck",
             "worse", "worrying", "crying", "hiding",
             "depressed", "depression", "depressive", "burnout", "burnt", "exhausted",
             "overwhelmed", "unwell", "poorly", "numb", "hopeless", "worthless", "useless",
             "miserable", "low", "sad", "lonely", "empty", "tired", "knackered", "shattered",
             "drained", "struggling", "stressed", "stress", "anxiety", "panic", "panicky",
             "awful", "rubbish", "terrible", "horrible", "addicted", "addiction", "unhappy",
             "despair", "grieving", "autistic", "adhd", "anorexic", "bulimic"}
PLAN_TROUBLE = re.compile(r"\b(?:might|may|probably|likely) not\b|\bnot be able\b|"
                          r"\b(?:can't|cant|won't|wont|couldn't|cant|cannot)\b|"
                          r"\bno longer\b|\bhave to\b|\bhad better\b")
PLAN_WORRY = re.compile(r"\bthink i (?:have|ve)\b|\b(?:might|may) have (?!a\b|an\b|the\b|"
                        r"my\b|our\b|some\b|this\b)")
SORRY_TALK = re.compile(r"\b(?:sorry|apolog\w*)\b.*\b(?:rant|ranting|moan|moaning|going on|"
                        r"going off|that was (?:a lot|heavy|too much|long)|heavy|rambl\w*|"
                        r"ear|dumping|vent\w*|waffl\w*|downer)\b")
SAY_SOMETHING = re.compile(r"\b(?:say|ask (?:you|ya)|tell (?:you|ya)|show (?:you|ya)|run (?:it|"
                           r"something|this) by (?:you|ya))\b[^.?!]*\b(?:something|anything|this|"
                           r"a question|one thing|a quick question)\s*[.?!]*$|"
                           r"\b(?:something|a question|one thing)\s+to\s+(?:tell|ask)\s+"
                           r"(?:you|ya)\s*[.?!]*$|"
                           r"\b(?:have|got)\s+(?:something|somethin|a thing|one thing)\s+to\s+"
                           r"say\s*[.?!]*$|"
                           r"\b(?:have|ask|ask (?:you|ya))\s+(?:a|one)\s+(?:quick\s+)?question"
                           r"\s*[.?!]*$")
ASK_WHETHER_TO_SPEAK = re.compile(
    r"\b(?:should|shall|ought|do you think i (?:should|need to)|is it worth|would you)\b")
GO_AWAY = re.compile(r"\b(?:go|going|goes|went|off|heading|fly|flying|flew|travel\w*|trip|"
                     r"holiday|vacation|visit\w*|booked|booking)\b")
VAGUE_WORDS = {"i", "im", "its", "it", "just", "everything", "all", "of", "dunno", "idk", "know",
               "dont", "not", "sure", "one", "those", "days", "day", "kind", "sort", "where",
               "to", "start", "and", "yeah", "ok", "okay", "today", "lately", "honestly", "a",
               "bit", "lot", "loads", "stuff", "things", "thing", "really", "tbh"}


SOFTEN = (r"(?:(?:just|still|actually|probably|really|honestly|literally|kind of|sort of|"
          r"kinda|sorta) )?")
INTENT_RE = re.compile(
    r"\b(?:i " + SOFTEN + r"(?:want to|wanna|plan to|plan on|started)|"
    r"(?:im|i am) " + SOFTEN + r"(?:thinking (?:of|about)|planning (?:to|on)|going to|"
    r"trying to|looking to|hoping to|training|saving|learning|working on|preparing|"
    r"getting ready)|"
    r"i " + SOFTEN + r"have decided to|"
    r"(?:ive|i've) " + SOFTEN + r"(?:decided to|started|been trying to|been meaning to|"
    r"been thinking (?:of|about)))\b")
NEXT_REST = re.compile(
    r"\b(?:bed|sleep|nap|bath|shower|early night|lie down|sit down|read|book|film|telly|"
    r"boxset|relax\w*|unwind\w*|put my feet up|some sleep)\b")
NEXT_ACT = re.compile(
    r"\b(?:work|school|the shops?|town|church|gym|walk the dog|dinner|lunch|breakfast|tea|food|"
    r"washing|ironing|cleaning|tidy|pack|pick (?:up |the ))\b")
NEXT_UP = re.compile(
    r"\b(?:im|i am|im just|im off|i'm)\s+(?:going|off)\s+(?:to\s+|for\s+)?(?:"
    r"bed|sleep|have a bath|have a shower|take a bath|take a shower|have an early night|"
    r"get an early night|get some sleep|get ready|work|the shops|the shop|town|church|"
    r"make (?:a|some|dinner|lunch|tea|breakfast)|cook|eat|have (?:some )?(?:dinner|lunch|"
    r"breakfast|tea|food)\b|walk the dog|the gym|pick (?:up |the ))")

MY_NIGHT = re.compile(
    r"\b(?:keep|keeps|kept) waking\b"
    r"|\bwak(?:e|es|ing) up (?:at|in the|every|most|half)\b"
    r"|\bwoke up (?:at|in the)\b"
    r"|\b(?:awake|lying awake|lay awake|up) (?:all|half|most of) the night\b"
    r"|\bno (?:night's )?sleep\b|\bbroken night\b")
NOT_MY_NIGHT = re.compile(
    r"\b(?:my|our|the|his|her|their)\s+(?:\w+\s+){0,2}"
    r"(?:baby|son|daughter|kid|kids|child|children|wife|husband|partner|mum|mom|mother|dad|"
    r"father|dog|cat|puppy|kitten|neighbou?r)s?\b"
    r"|\b(?:he|she|they)\s+(?:keeps?|kept|was|were|is|are)\b")

NEED_FOR = re.compile(r"^(?:ok |okay |so |and |but |also )?(?:i|we) (?:still )?need (?:a|an|some)\b"
                      r".*\bfor\b")
NEED_RE = re.compile(r"^(?:ok |okay |so |and |but |also )?(?:i|we) (?:still )?need (?:to|a|an|some)\b")
QUESTION_STARTERS = frozenset("""
do does did can could should would will shall is are was were am have has had how what which
where when why who whom whose any anyone anybody anything if whether ever
""".split())
DOUBT = re.compile(r"\b(?:dont|do not|didnt) know\b|\bno idea\b|\bwhether\b|"
                   r"\bif (?:i|we) (?:should|want|stay|go|leave|quit)\b|"
                   r"\bnot (?:sure|decided)\b|\b(?:unsure|undecided)\b")
INTENT_CONDITION = re.compile(r"\b(?:without|so that|instead of|as long as|rather than)\b")
EVENT_RE = re.compile(r"\b(?:i have|ive got|i got|im having|i am having|we have|weve got|theres)\b"
                      r"(?!.*\?)\b.*\b(?:tomorrow|tonight|this morning|this afternoon|"
                      r"this evening|monday|tuesday|wednesday|thursday|friday|saturday|sunday|"
                      r"next week|next month|next year|this week|this weekend|in a few days|"
                      r"in a couple of (?:days|weeks))\b")
INTENT_STOP = {"sick", "ill", "late", "hurt", "broke", "broken", "lost", "missed", "forgot",
               "forgotten", "left", "cancel", "cancelled", "worried", "worry", "scared",
               "anxious", "failed", "fail", "fired", "sacked", "debt", "owe", "arguing",
               "crying", "upset", "angry", "worse", "pain", "bleeding", "pregnant", "doctor",
               "hospital", "police", "accident", "die", "dying", "died", "funeral", "help",
               "advice", "recipe", "how", "which", "what", "should", "worth", "better",
               "job", "jobs", "cv", "search", "tip", "tips", "recommend", "recommendations",
               "suggest", "suggestions",
               "hate", "hates", "hating", "miserable", "dread", "dreading", "awful",
               "terrible", "horrible", "lonely", "isolated", "bored", "pointless", "stuck",
               "struggling", "exhausted", "drained", "resent"}
WANTED = re.compile(r"\b(?:want|wanna|going|planning|thinking of|thinking about|trying|hoping|"
                    r"decided|plan|looking|training|saving|learning|working on|preparing|"
                    r"getting ready|meaning|started|start)\b\s+(?:to\s+|on\s+|about\s+)?(.{0,40})")
FEELING_WANT = re.compile(
    r"^(?:to\s+)?(?:stop|not|never)\s+(?:\w+\s+)?(?:feeling|feel|being|hurting|crying|"
    r"worrying|like)\b|\b(?:feel|feeling)\s+(?:like|this|that|so|normal|better|good)\b")
FEELING_THING = frozenset("""
cry crying weep weeping sob sobbing scream screaming shout shouting yell yelling disappear
disappearing vanish hide hiding hurt hurting give
""".split())
LEAVE_SOMEONE = re.compile(r"^(?:leave|leaving|left|end|ending|break up with|divorce|divorcing|"
                           r"walk out on)\b.{0,24}\b(?:him|her|them|husband|wife|partner|"
                           r"boyfriend|girlfriend|marriage|relationship|us)\b")
STOPS_TOGETHER = re.compile(
    r"^(?P<subject>it\s+all|all\s+of\s+it|it|this|that|these|those|things|everything|nothing"
    r"|the\s+lot|life"
    r"|(?:the|my|your|his|her|their|our|this|that|these|those|all|any)\s+[a-z][a-z'-]*"
    r"(?:\s+[a-z][a-z'-]*)?)"
    r"\s+to\s+(?:stop|end|go\s+away|be\s+over|be\s+done\s+with|be\s+different|change"
    r"|get\s+better|settle|sort\s+itself\s+out|go\s+back\s+to\s+normal)\b")
SAYS_NOTHING = frozenset(("it", "it all", "all of it", "this", "that", "these", "those", "things",
                          "everything", "nothing", "the lot", "life"))
EVENT_OUTING = re.compile(r"\b(?:drive|journey|trip|flight|train|coach|ferry|commute|shift|"
                          r"night out|dinner|party|meal|shopping|sleepover)\b")
EVENT_TIRED = re.compile(r"\b(?:cant|cannot|knackered|exhausted|tired|sleep|sleeping|"
                         r"insomnia|awake)\b")
EVENT_STATE = re.compile(r"\b(?:fever|temperature|headache|headaches|migraine|migranes|"
                         r"toothache|earache|stomach ache|sore throat|cough|rash|infection|"
                         r"pain|ache|aching|hurts|hurting|nausea|nauseous|dizzy|swollen|"
                         r"symptoms?|skint|no money|broke)\b")


def _a_trip(flat, memory):
    if ack.reads_as_a_trip(flat):
        return True
    user = memory.get("user") if isinstance(memory, dict) else None
    places = user.get("places") if isinstance(user, dict) else None
    return bool(places) and bool(GO_AWAY.search(flat))


def _answers_it(text, understood, memory):
    from ..knowledge.lookup import find
    from . import answers
    try:
        found = find(understood)
        if found is not None:
            reply = answers._payload(found, memory, understood)
            if isinstance(reply, str) and reply.strip():
                return True
        item, reply = answers._offer(
            lambda reject: answers._in_context(text, memory, reject=reject), memory, understood)
    except Exception:
        return True
    return bool(item is not None and isinstance(reply, str) and reply.strip())


def _intent(clean, tokens, memory):
    from ..knowledge.lookup import find
    from ..compose import fallback as compose_fallback
    if not tokens or len(tokens) > 22 or "?" in clean or len(tokens) < 3:
        return None
    if compose_fallback._the_morning_has_a_clock(" ".join(tokens)):
        return None
    flat = " ".join(tokens)
    if _a_trip(flat, memory):
        return None
    if compose_fallback.reads_as_a_change_of_medicine(flat):
        return None
    if ack.a_limit_on_the_plan(flat):
        return None
    words = set(tokens)
    if words & INTENT_STOP or PLAN_WORRY.search(flat):
        return None
    if harm_reading.reads_as_hurting_someone(flat):
        return None
    quoted = saidby_reading.reply_for(flat, memory)
    if quoted:
        return quoted
    if tokens[-1] in ("though", "tho"):
        return None
    wanted = WANTED.search(flat)
    if wanted:
        thing = wanted.group(1).strip(" .,!;:")
        first = (thing.split() or [""])[0]
        if first in FEELING_THING or FEELING_WANT.search(thing) or LEAVE_SOMEONE.search(thing):
            return None
    head = [t for t in tokens if t not in ("ok", "okay", "so", "and", "but", "also", "well")]
    if head and head[0] in QUESTION_STARTERS:
        return None
    if DOUBT.search(flat):
        return None
    if INTENT_CONDITION.search(flat):
        return None
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if isinstance(understood, dict) and _answers_it(clean, understood, memory):
        return None
    if isinstance(understood, dict) and understood.get("tight_on_money"):
        return None
    from ..knowledge import cooking as cooking_kb
    if isinstance(understood, dict) and cooking_kb.negated_ingredients(understood):
        return None
    if ack.a_job_to_do(clean, memory):
        return None
    if EVENT_RE.search(flat):
        if (EVENT_OUTING.search(flat) or EVENT_TIRED.search(flat)
                or EVENT_STATE.search(flat)):
            return None
        return "event"
    if NEED_FOR.search(flat):
        return None
    if INTENT_RE.search(flat) or NEED_RE.search(flat):
        if NEXT_UP.search(flat) and not _my_night(flat):
            if NEXT_REST.search(flat) and not NEXT_ACT.search(flat):
                return "next_rest"
            if NEXT_ACT.search(flat):
                return "next_act"
            return "next_up"
        return "intent"
    return None


def _as_typed(flat, memory):
    understood = memory.get("understood") if isinstance(memory, dict) else None
    words = understood.get("words") if isinstance(understood, dict) else None
    if isinstance(words, list) and words and all(isinstance(w, str) and w for w in words):
        return " ".join(words)
    return flat


_ON_THE_JOB = re.compile(r"\b(?:it|its|it's|that|that's|this|them|they|those|these)\b", re.I)
_THE_RUN_OF_IT = re.compile(r"\b(?:work|works|job|shift|shifts|week|weeks|weekend|month|day|days|"
                            r"term|year|life|things|everything|staffing|rota|hours)\b", re.I)


def _a_detail_on_the_job(flat, memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not turns or not isinstance(turns[-1], dict) or turns[-1].get("module") != "answers":
        return False
    understood = memory.get("understood") if isinstance(memory, dict) else None
    leans = understood.get("leans_on") if isinstance(understood, dict) else None
    if not isinstance(leans, dict) or not str(leans.get("text") or "").strip():
        return False
    if not _ON_THE_JOB.search(flat):
        return False
    return not _THE_RUN_OF_IT.search(flat)


A_RATE_OF_MONEY = re.compile(
    r"(?:[£$€]\s*\d[\d,.]*|\b\d[\d,.]*\s*(?:pounds?|quid|euros?|dollars?|grand|k)?)\s*"
    r"(?:a|an|per|each|every)\s+(?:month|week|year|day|fortnight)\b", re.I)
A_JUDGEMENT_ON_A_FIGURE = re.compile(
    r"\b(?:is|isnt|isn'?t|was|wasnt|wasn'?t)\s+(?:that|this|it)\s+(?:about\s+|really\s+|"
    r"actually\s+)?(?:a lot|too much|too dear|expensive|cheap|good value|worth it|about right|"
    r"normal|fair|steep|reasonable|pricey|dear)\b", re.I)


def _overloaded(flat, memory):
    if not OVERLOAD.search(flat):
        return False
    if A_RATE_OF_MONEY.search(flat) and A_JUDGEMENT_ON_A_FIGURE.search(flat):
        return False
    said = _as_typed(flat, memory)
    if LOAD_ASK.search(said) or LOAD_TURNED.search(said) or LOAD_SOMEONE_ELSE.search(said):
        return False
    if _a_detail_on_the_job(flat, memory):
        return False
    return not LOAD_FEELS.search(said)


JUDGED = re.compile(
    r"^(?:and |so |but |ok |okay |well )*(?:is|was|would|will|could) "
    r"(?:that|this|it) (?:really |actually |even )?"
    r"(?:a (?:good|bad|daft|silly|smart|sensible|wise|right|wrong|clever) "
    r"(?:thing|idea|move|call|plan|choice|buy|option)(?: to do)?|"
    r"the (?:right|wrong|sensible|wise|smart) (?:thing|move|call|choice)(?: to do)?|"
    r"worth it|worth (?:doing|getting|a go|trying)|sensible|wise|a mistake|a waste of money|"
    r"going to work|work|going to help|going to be (?:ok|okay|fine))"
    r"(?: then| though| do you think| in your opinion| or not| to do)?\??$")
_CONSIDERING = re.compile(
    r"^(?:(?:ok|okay|so|well|and|and also)[\s,]+)?"
    r"(?:(?:i'?m|im|i am|we'?re|we are|i'?ve|i have|i|we)\s+)?(?:been\s+|still\s+|also\s+)?"
    r"(?:thinking (?:of|about)|considering|looking (?:at|into|for|round at)|weighing up|"
    r"toying with|fancy(?:ing)?|after|into)(?:\s+|$)")
_CONSIDERING_TO = re.compile(
    r"^(?:(?:ok|okay|so|well|and|and also)[\s,]+)?"
    r"(?:(?:i'?m|im|i am|we'?re|we are|i'?ve|i have|i|we)\s+)?(?:been\s+|still\s+|also\s+)?"
    r"(?:thinking (?:of|about) going to|planning to|thinking to|hoping to|want(?:ing)? to|"
    r"wanted to|'?d like to|would like to|keen to|tempted to|trying to|going to|gonna|off to|"
    r"out to|away to|heading to|about to)(?:\s+|$)")


def _judged(clean, memory):
    if not JUDGED.match(clean):
        return None
    try:
        if fallback.a_verdict_on_their_plan(clean, memory):
            return None
    except Exception:
        pass
    thing = _judged_thing(clean, memory)
    if thing:
        options = [option.format(thing=thing, Thing=thing[:1].upper() + thing[1:])
                   for option in NEWS_REPLIES["judged"]]
    else:
        options = list(NEWS_REPLIES["judged_bare"])
    return pick(options, memory, clean)


_STATEMENT = re.compile(
    r"\b(?:is|are|was|were|am|has|have|had|do|does|did|will|would|can|could|should|shall|"
    r"might|must|i|we|you|he|she|they|that|this)\b"
    r"|\b(?:im|i'?m|ive|i'?ve|we'?re|hes|he'?s|shes|she'?s|they'?re|dont|doesnt|didnt|"
    r"can'?t|wont|isnt|aren'?t|wasnt|wouldnt|couldnt)\b")


_BARE_DOING = re.compile(
    r"^(?:i'?m|im|i am|we'?re|we are)\s+(?P<doing>[a-z]{3,}ing)\b(?P<rest>.*)$")


def _judged_thing(clean, memory):
    record = current(memory)
    said = " ".join(str(record.get("text") or "").split()) if isinstance(record, dict) else ""
    said = said.strip(" .!?,")
    if not said or said.lower() == clean.lower():
        return ""
    to_form = bool(_CONSIDERING_TO.match(said))
    said = _CONSIDERING_TO.sub("", said) if to_form else _CONSIDERING.sub("", said)
    if to_form:
        said = stepwords.said_after_a_to(said)
    doing = _BARE_DOING.match(said)
    if doing:
        said = (doing.group("doing") + doing.group("rest")).strip(" .,!?:;")
    said = re.split(r"[,;]|\b(?:because|but|so|though|although)\b", said)[0].strip(" .,!?:;")
    words = said.split()
    if not 2 <= len(words) <= 6 or _STATEMENT.search(said):
        return ""
    return said


AGAIN_ONLY = frozenset("again not oh no and over yet it on this time really".split())
NOT_AGAIN = frozenset("not no oh".split())
HOW_TO_ASKED = re.compile(r"\bhow (?:do|can|should|would|could) (?:i|you|we)\b|\bhow to\b",
                          re.IGNORECASE)
THE_STEPS_AGAIN = ("Again — ", "Here it is again: ", "Same as before: ")
LOOKING_FORWARD = frozenset((
    "cant wait", "cannot wait", "cant wait for it", "cant wait to go", "cant wait for this",
    "looking forward to it", "looking forward to that", "so excited", "im so excited",
    "really excited", "counting down", "cant wait now",
))


def _the_steps_again(memory):
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    if not turns:
        return None
    last = turns[-1]
    asked = str(last.get("user") or "")
    answer = str(last.get("bot") or "").strip()
    if not HOW_TO_ASKED.search(asked) or len(answer.split()) < 8:
        return None
    return pick(THE_STEPS_AGAIN, memory) + answer


def _a_care_turn(memory):
    last = _last_said(memory)
    if last and any(pattern.search(last.lower()) for _, pattern in SOMEONE_TROUBLE):
        return True
    return fallback._in_a_care_thread(memory)


def _short_talk(clean, tokens, memory):
    if not tokens or len(tokens) > 12 or "?" in clean:
        return None
    flat = " ".join(tokens)
    if _a_trip(flat, memory):
        return None
    if set(tokens) <= AGAIN_ONLY and "again" in tokens:
        return "again" if set(tokens) & NOT_AGAIN else "again_what"
    if flat in LOOKING_FORWARD:
        return None if _a_care_turn(memory) else "keen"
    if SORRY_TALK.search(flat):
        return "sorry_talk"
    words = set(tokens)
    if BUSY_RE.search(flat) and words & BUSY_WORK:
        return "busy"
    if _overloaded(flat, memory):
        return "overloaded"
    if "everything at once" in flat or "one thing after another" in flat:
        return "busy"
    if len(tokens) <= 8 and words <= VAGUE_WORDS and (
            "everything" in words or ("those" in words and "one" in words)
            or ("dont" in words and "know" in words)):
        if stuck_line._the_answer_gave_a_step(memory):
            return "plan" if PLAN_RE.search(flat) and not words & PLAN_STOP else None
        return "vague"
    if fallback.reads_as_a_change_of_medicine(_without_the_might(flat)):
        return ("plan_medicine_slow" if fallback.PLAN_MEDICINE_SLOW.search(flat)
                else "plan_medicine")
    if (PLAN_RE.search(_without_the_might(flat)) and not words & PLAN_STOP
            and not PLAN_WORRY.search(flat) and not PLAN_TROUBLE.search(flat)
            and not _a_forecast(memory)):
        return "plan"
    return None


def _a_forecast(memory):
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if not isinstance(understood, dict):
        return False
    if str(understood.get("topic") or "") != "nature-and-weather":
        return False
    return str(understood.get("kind") or "") == "question"


FEELING_POOLS = ("sad", "tired", "stressed", "ill", "anxious", "worry", "worry_person",
                 "missing", "guilty", "lonely", "rough_day", "stuck", "not_coping",
                 "bad_day", "venting")
FEELING_SAID = frozenset(
    [text for name in FEELING_POOLS for text in REPLIES[name] if isinstance(text, str)])


def _tokens(text):
    text = text.lower().replace("’", "'")
    for smile, word in SMILES.items():
        text = text.replace(smile, word)
    text = text.replace("'", "")
    return [t for t in TOKEN.findall(text) if t]


def _name(memory):
    facts = memory.get("user")
    if isinstance(facts, dict):
        name = facts.get("name")
        if isinstance(name, str) and name:
            return name[:1].upper() + name[1:]
    return None


def _the_lost_thread_asked(memory, kind):
    if kind != "confused" or not isinstance(memory, dict):
        return
    turns = memory.get("turns")
    memory["lost_thread"] = {"turn": len(turns) if isinstance(turns, list) else 0}


def _after_a_lost_thread(clean, understood, memory):
    if not isinstance(memory, dict):
        return None
    note = memory.get("lost_thread")
    if not isinstance(note, dict):
        return None
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns:
        return None
    if note.get("turn") != len(turns) - 1:
        return None
    if (not isinstance(understood, dict) or understood.get("kind") != "statement"
            or understood.get("emotion") or understood.get("asks")):
        return None
    if _confusion_names_a_thing(understood):
        return None
    words = re.findall(r"[a-z']+", str(clean or "").lower())
    if len(words) < 3 or len(words) > 14:
        return None
    return _reply("lost_thread_more", memory, None, " ".join(words))


def _the_weight_said(memory, feeling):
    if not isinstance(memory, dict):
        return
    turns = memory.get("turns")
    index = len(turns) if isinstance(turns, list) else 0
    memory["said_kind"] = {"kind": feeling, "turn": index}
    if feeling not in HEAVY_FEELINGS:
        return
    memory["heavy_reply"] = {"feeling": feeling, "turn": index}
AHEAD = re.compile(
    r"\b(?:tomorrow|tonight|this (?:weekend|evening|afternoon|morning|week|month)"
    r"|next (?:week|month|weekend|year|monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
    r"|weekend|holiday|holidays|trip|away|party|wedding|birthday|christmas|new year|exam|exams"
    r"|test|interview|results?|match|game|flight|moving|graduation|show|gig|appointment"
    r"|driving test|scan|check-?up|first day|performance|audition|presentation)\b", re.I)
NEEDS_AHEAD = (
    "Love that. Anything nice planned to go with it?",
    "Nerves before something big are normal. Slow breaths for a minute genuinely help.",
)
NOT_PROUD = re.compile(r"\b(?:not|never|hardly|nothing|no)\b[^.?!]{0,20}?\bproud\b", re.I)
PROUD_OF_MYSELF = re.compile(
    r"\b(?:i'?m|im|i am|i\s+feel|feeling|felt|so|really|quite|proper)\b[^.?!]{0,24}?\bproud\b"
    r"|\bproud of (?:myself|what i|that i|how i|it)\b", re.I)
PROUD_OF_ANOTHER = re.compile(
    r"\bproud of (?:you|u|ya|her|him|them|his|hers|their|my|our|the|this|that)\b", re.I)


CHEER_IN_LOSS = (
    "I'm glad there's something good in the week - it's been a heavy one for you.",
    "Good to hear it. You've had a lot to carry lately.",
    "That's good to hear, and I'm still sorry about your loss.",
    "Glad of that. How are you doing in yourself, with everything else?",
)
CHEER_KINDS = frozenset(("happy", "laugh", "lol", "good_news"))


_NOTHING_MUCH_FILLER = frozenset("""not much nothing nm nmu notmuch im i m am just yeah yeh yep
    so well oh hi hey hello really like its it is a bit going on happening here there today now
    thanks ta lol though either atm still you u and about what how yourself to say report
    else lately honestly tbh tbf mate m8 bud pal me us hbu wbu innit haha happened""".split())

_NOTHING_MUCH_BETWEEN = frozenset("""really very so that too even actually quite just
    do did done doing does""".split())

_NOTHING_MUCH_DO = frozenset("""do did done doing does dont didnt doesnt havent hasnt
    havent havent""".split())

_NOTHING_MUCH_AFTER = frozenset("""chilling relaxing working watching hanging pottering lazy
    home at out telly tv games game music reading dinner lunch tea coffee garden""".split())

_NOTHING_MUCH_TAIL = frozenset(("just", "only"))


def _nothing_much_span(words):
    for i, word in enumerate(words):
        if word in ("notmuch", "nm", "nmu"):
            return i, i + 1
    for opener in ("nothing", "not"):
        if opener not in words:
            continue
        start = words.index(opener)
        if "much" not in words[start + 1:]:
            continue
        stop = words.index("much", start + 1)
        if all(word in _NOTHING_MUCH_BETWEEN for word in words[start + 1:stop]):
            return start, stop + 1
        return None
    if "much" in words:
        at = words.index("much")
        if any(word in _NOTHING_MUCH_DO for word in words[:at]):
            return at, at + 1
    return None


def _says_nothing_much(tokens, clean=""):
    said = set(tokens)
    if not (said & {"much", "notmuch", "nm", "nmu"}):
        return False
    if re.search(r"\bhow\s+(?:much|many)\b", clean or ""):
        return False
    if "much" in said and not (said & {"not", "nothing", "notmuch", "nm", "nmu"}
                               or said & _NOTHING_MUCH_DO):
        return False
    if said <= _NOTHING_MUCH_FILLER:
        return True
    clause = re.split(r"[,;:]|\s-\s", clean or "", 1)[0]
    words = _tokens(clause)
    span = _nothing_much_span(words)
    if span is None:
        return False
    start, stop = span
    before, after = words[:start], words[stop:]
    for at, word in enumerate(after):
        if word in _NOTHING_MUCH_TAIL:
            after = after[:at]
            break
    if not set(after) <= (_NOTHING_MUCH_FILLER | _NOTHING_MUCH_AFTER | _NOTHING_MUCH_BETWEEN):
        return False
    if not set(before) <= (_NOTHING_MUCH_FILLER | _NOTHING_MUCH_DO):
        return False
    return True

def _the_line_on_the_screen(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in reversed(turns or []):
        said = turn.get("bot") if isinstance(turn, dict) else None
        if isinstance(said, str) and said.strip():
            return said.strip()
    return ""


def _thanks_that_fit(options, memory):
    said = _the_line_on_the_screen(memory)
    if said and not said.rstrip().endswith("?"):
        return options
    left = [option for option in options if "helped" not in option]
    return left or options


FIRST_LINE_POOL = {"returned": "greeting", "check_in": "greeting", "check_in_name": "greeting"}


def _reply(kind, memory, name=None, seed=""):
    if not _mid_chat(memory):
        kind = FIRST_LINE_POOL.get(kind, kind)
    if kind == "greeting" and _mid_chat(memory) and not _says_the_time_of_day(memory):
        if name:
            return pick([o.format(name=name) for o in REPLIES["check_in_name"]], memory, seed)
        return pick(list(REPLIES["check_in"]), memory, seed)
    if kind == "howareyou" and _mid_chat(memory):
        if said_loss(memory):
            return pick(list(REPLIES["howareyou_loss"]), memory, seed)
        return pick(list(REPLIES["howareyou_mid"]), memory, seed)
    part = _the_part_of_day(memory)
    if kind == "greeting" and part:
        return pick(list(REPLIES["greeting_" + part]), memory, seed)
    _the_weight_said(memory, kind)
    _the_lost_thread_asked(memory, kind)
    options = REPLIES[kind]
    if not _mid_chat(memory):
        fresh = [o for o in options if not onscreen.talks_about_the_conversation(o)]
        options = fresh or options
    if kind == "thanks":
        options = _thanks_that_fit(options, memory)
    if name and kind == "greeting":
        options = REPLIES["greeting_name"]
    if kind in CHEER_KINDS and _a_death_just_said(memory):
        options = CHEER_IN_LOSS
    elif kind in ("happy", "anxious"):
        fits = [o for o in options if o in NEEDS_AHEAD]
        if AHEAD.search(str(seed)):
            options = fits or options
        else:
            options = [o for o in options if o not in NEEDS_AHEAD] or options
    text = pick([option.format(name=name) for option in options], memory, seed)
    return text


def _the_part_of_day(memory):
    read = memory.get("understood") if isinstance(memory, dict) else None
    words = str((read or {}).get("plain") or "").lower().split() if isinstance(read, dict) else []
    for part in ("morning", "afternoon", "evening"):
        if part in words:
            return part
    return None


def _says_the_time_of_day(memory):
    read = memory.get("understood") if isinstance(memory, dict) else None
    words = str((read or {}).get("plain") or "").lower().split() if isinstance(read, dict) else []
    return any(word in words for word in ("morning", "afternoon", "evening"))


def _mid_chat(memory):
    return onscreen.earlier_turn(memory)


def _just_met(memory):
    log = memory.get("facts_log")
    if not isinstance(log, list):
        return None, None
    turn, name, plan = len(memory.get("turns") or []), "", ""
    for entry in log[-6:]:
        if not isinstance(entry, dict) or entry.get("turn") != turn:
            continue
        if entry.get("key") == "name" and isinstance(entry.get("value"), str):
            name = entry["value"]
        if entry.get("key") == "plan" and isinstance(entry.get("value"), str):
            plan = entry["value"]
    return name, plan


PLAN_CLAUSE_OPENS = frozenset(("i", "im", "i'm", "ive", "i've", "ill", "i'll", "we", "were",
                               "we're", "weve", "we've", "well", "we'll",
                               "a", "an", "the", "my", "our", "his", "her", "their", "this",
                               "that"))
PLAN_THINGS_OPEN = frozenset(("a", "an", "the", "my", "our", "his", "her", "their", "this",
                              "that"))
PLAN_VERB_OPENS = frozenset("""learn save buy book plan start finish move visit get make cook
bake build write paint plant grow fix clean decorate prepare host throw assemble sew knit roast
boil fry grill set sort replace repair install renovate organise organize train study practise
practice sell find look run walk cycle swim read play sing dance draw travel garden dig""".split())


def _ing(word):
    low = word.lower()
    if low.endswith("ie"):
        return low[:-2] + "ying"
    if low.endswith("e") and not low.endswith("ee") and len(low) > 3:
        return low[:-1] + "ing"
    if len(low) <= 4 and re.fullmatch(r"[^aeiou]*[aeiou][^aeiouwxy]", low):
        return low + low[-1] + "ing"
    return low + "ing"


def _plan_clause(plan):
    text = " ".join(str(plan or "").split()).strip(" .!?,")
    first = text.split()[0].lower() if text else ""
    if not text:
        return ""
    said = re.sub(r"\b(im|ive|ill)\b", lambda m: "i'" + m.group(0)[1:], text, flags=re.I)
    said = re.sub(r"\bwere\b", "we're", said, flags=re.I)
    said = re.sub(r"\bweve\b", "we've", said, flags=re.I)
    clause = you(said)
    if clause.lower().startswith("you") and first in PLAN_CLAUSE_OPENS:
        return clause[:1].lower() + clause[1:]
    if first in PLAN_THINGS_OPEN:
        clause = clause[:1].lower() + clause[1:]
        return clause.rstrip(".!?").rstrip()
    words = clause.split()
    if first.endswith("ing") and len(first) > 4:
        return clause[:1].lower() + clause[1:]
    if first in PLAN_VERB_OPENS and words:
        words[0] = _ing(words[0])
        return " ".join(words)
    if first == "for":
        return "saving " + clause[:1].lower() + clause[1:]
    return ""


def _is_greeting(tokens):
    return bool(tokens) and all(t in GREET_FILLER for t in tokens) and any(t in GREET_CORE for t in tokens)


THANKS_FOR = re.compile(
    r"\bfor (?:that|this|it|the|your|you|all|everything|all of it|the help|the advice)\b")

HOW_THEY_ARE_LINE = re.compile(
    r"^\W*(?:(?:yeah|yes|oh|well|hi|hiya|hey|so|and)[, ]+)?"
    r"(?:im|i'm|i am|its|it's|ive been|i've been)\s+"
    r"(?:doing\s+|feeling\s+|been\s+|been doing\s+|doing been\s+)?"
    r"(?:pretty\s+|really\s+|very\s+|so\s+|all\s+|too\s+|quite\s+|that\s+)?"
    r"(?:good|great|fine|ok|okay|alright|well|brilliant|grand|cracking|chill|sound|content"
    r"|mint|brill)\b"
    r"(?:\s+(?:today|thanks|thank you|ta|tho|though|honestly|actually|really|now))?\W*$")

ANSWERS_HOW_ARE_YOU = re.compile(
    r"^\W*(?:(?:yeah|yes|oh|well|hi|hiya|hey)[, ]+)?"
    r"(?:im|i'm|i am|doing|all good|its all good|it's all good|not bad|not too bad)"
    r"\s+(?:doing\s+|feeling\s+|pretty\s+|really\s+|very\s+|so\s+|all\s+|too\s+)?"
    r"(?:good|great|fine|ok|okay|alright|well|bad|brilliant|grand|cracking|chill|sound|content"
    r"|mint|brill)\b")

NOT_GOOD = re.compile(
    r"^\W*(?:(?:yeah|yes|oh|well|hi|hiya|hey)[, ]+)?"
    r"(?:im|i'm|i am|doing|it's|its|i'm doing|im doing)?\s*\bnot\s+"
    r"(?:doing\s+|feeling\s+|too\s+|really\s+|very\s+|that\s+|so\s+)?"
    r"(?:good|great|fine|ok|okay|alright|well|brilliant|grand|cracking)\b"
    r"(?=\s*(?:$|[,.;!?]|thanks\b|thank you\b|tho\b|though\b|today\b|honestly\b|really\b|"
    r"i think\b|i guess\b|right now\b|at the moment\b))", re.IGNORECASE)


HEDGE_LEAD = r"(?:(?:yeah|yep|yes|oh|ah|well|honestly|tbh|still|only|just|it|its|is|was|im|i'm|" \
             r"i am|am|doing|been|a|bit|pretty|kind of|sort of|and|but|so|really|very|lately|" \
             r"today|these days)\s+)*"
HEDGE_TAIL = r"(?:[,.]?\s*(?:thanks|thank you|ta|cheers|though|tho|tbh|to be honest|" \
             r"honestly|i suppose|i guess|i think|really|at the moment|right now|today|lately|" \
             r"all things considered)\s*)*\W*$"
ASKED_HOW_ARE_YOU = ("howareyou", "notmuch", "greeting", "greeting_name", "meet")


def _a_hedge_answering_the_question(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return True
    note = memory.get("said_kind")
    if not isinstance(note, dict) or note.get("turn") != len(turns) - 1:
        return False
    return note.get("kind") in ASKED_HOW_ARE_YOU


HEDGED_OK_LINE = re.compile(
    r"^\W*" + HEDGE_LEAD +
    r"(?:can'?t complain|could be worse|mustn'?t grumble|getting there|getting by|keeping busy|"
    r"keeping going|plodding on|surviving|bearing up|fair to middling|so so|ok i suppose|"
    r"ok i guess|alright i suppose)" + HEDGE_TAIL, re.IGNORECASE)
HEDGED_LOW_LINE = re.compile(
    r"^\W*" + HEDGE_LEAD +
    r"(?:could be better|been better|hanging in there|hanging on in there|up and down|"
    r"not been great|not been brilliant|not so good|lacking in energy)" + HEDGE_TAIL,
    re.IGNORECASE)


DENIAL_FILLER = {"too", "so", "very", "really", "that", "all", "quite", "feeling", "doing",
                 "am", "been", "at", "the", "moment", "right", "now", "today", "honestly"}


def _denies_a_good_word(tokens):
    for index, token in enumerate(tokens):
        if token not in {"not", "never", "barely", "hardly"}:
            continue
        for word in tokens[index + 1:]:
            if word in DENIAL_FILLER:
                continue
            if word in POSITIVE:
                return True
            break
    return False


def _is_thanks(tokens):
    return bool(tokens) and any(t in THANKS_CORE for t in tokens) and all(
        t in THANKS_FILLER or t in THANKS_LOOSE or t in THANKS_CORE for t in tokens)


A_NOD_BEFORE = frozenset(ACK_WORDS - NO_WORDS)


A_FIRM_NO = ("at", "all")


def _without_the_at_all(tokens):
    kept = []
    for token in tokens:
        if token == A_FIRM_NO[1] and kept and kept[-1] == A_FIRM_NO[0]:
            kept.pop()
            continue
        kept.append(token)
    return kept


def _without_the_nod(tokens):
    start, end = 0, len(tokens)
    while start < end - 1 and tokens[start] in A_NOD_BEFORE and tokens[start] not in THANKS_CORE:
        start += 1
    while end - 1 > start and tokens[end - 1] in A_NOD_BEFORE \
            and tokens[end - 1] not in THANKS_CORE:
        end -= 1
    return tokens[start:end] if (start or end != len(tokens)) else tokens


HOW_ARE_YOU = re.compile(
    r"\b(how are (you|u|ya)( doing| today| feeling)?|how r (u|you)|hows it going|"
    r"how is it going|how are things|hows things|how you doing|(?:you|u) (?:ok|okay|alright)(?!\s*(?:with|about|to|for|if|when|on|at|in)\b)|"
    r"you (good|fine)(?!\s*(?:with|about|to|for|if|when|on|at|in)\b)|"
    r"u (good|fine)(?!\s*(?:with|about|to|for|if|when|on|at|in)\b)|"
    r"(you|u) feeling (ok|okay|alright|good)(?!\s*(?:with|about|to|for|if|when|on|at|in)\b)|"
    r"howz (you|u|ya|things|life)|hows (you|u|ya)|"
    r"u (ok|okay)(?!\s*(?:with|about|to|for|if|when|on|at|in)\b)|how do you do|whats up|what is up|sup|hows life|how is life|how are ya|"
    r"hows? (?:your|ur) (?:day|week)(?: (?:been|going|go|then))?"
    r"(?!\s*(?:(?:been|going|go|then)\s+)?(?:off|at|on|in|with|about|after|before|to)\b)|"
    r"how (?:is|was|s|has|s been) (?:your|ur) (?:day|week)(?: (?:been|going|go|then))?"
    r"(?!\s*(?:(?:been|going|go|then)\s+)?(?:off|at|on|in|with|about|after|before|to)\b)|"
    r"how (?:have|ve) (?:you|u|ya) been|how (?:you|u|ya) been)\b")


HOW_ARE_YOU_CONTENT = ("supposed to", "meant to", "going to")


def _is_howareyou(tokens):
    if not (1 <= len(tokens) <= 7):
        return False
    line = " ".join(tokens)
    match = HOW_ARE_YOU.search(line)
    if not match:
        return False
    if _asks_about_the_make(line):
        return False
    rest = line[match.end():].strip()
    if match.group(0).endswith("feeling") and rest.startswith("about "):
        return False
    if re.match(r"with\s+(?:my|our|your|his|her|their|the)\s+\w", rest):
        return False
    rest_words = rest.split()
    return " ".join(rest_words[:2]) not in HOW_ARE_YOU_CONTENT


THE_MAKE = frozenset(("model", "workings"))


def _asks_about_the_make(line):
    try:
        return fallback.about_the_bot(line) in THE_MAKE
    except Exception:
        return False


def _is_bye(tokens):
    if not tokens or not all(t in BYE_FILLER for t in tokens):
        return False
    return _leaves(tokens)


LEAVES_ONLY = (("good", "night"), ("night", "night"), ("night",), ("later",), ("bye",),
               ("sweet", "dreams"), ("im", "out"), ("i", "am", "out"), ("in", "a", "bit"),
               ("let", "you", "go"), ("let", "u", "go"), ("ill", "let", "you", "go"))
LEAVING_WORDS = frozenset({
    "gotta", "got", "gonna", "gunna", "have", "heading", "head", "off", "leaving", "going",
    "need", "must", "should", "go", "goes", "going", "went", "sleep", "sleeping", "bed",
    "bedtime", "out", "soon", "now", "later", "night",
    "i", "im", "i'm", "am", "me", "we", "to", "be", "a", "for", "on", "in", "the",
    "then", "so", "ok", "okay", "right", "well", "just", "now", "yes", "yeah", "yep",
    "alright", "and", "all", "your", "you", "u", "take", "care", "bye", "goodbye",
    "goodnight", "cya", "cheerio", "toodles", "nightnight", "see", "talk", "speak", "catch",
})


DESCRIBES_THE_DAY = re.compile(
    r"\b(?:nice|lovely|great|fun|brilliant|long|early|late|quiet|busy|cold|warm|wet)\s+"
    r"(?:night|day|evening|morning|one|time)\b")


def _leaves(tokens):
    if not tokens:
        return False
    if tuple(tokens) in LEAVES_ONLY or tuple(tokens) == ("good", "night"):
        return True
    if any(t in {"bye", "byebye", "goodbye", "goodnight", "cya", "cheerio", "toodles",
                 "nightnight"} for t in tokens):
        return True
    if any(t in BYE_TIME for t in tokens) and any(t in BYE_VERB for t in tokens):
        return True
    if tokens[0] == "see" and any(t in {"you", "u", "ya"} for t in tokens):
        return True
    if re.search(r"\b(?:day|days|time|week|weeks|weekend|afternoon|morning|evening|night|shift"
                 r"|today|tomorrow|tonight|monday|tuesday|wednesday|thursday|friday|saturday"
                 r"|sunday)\s+off\b", " ".join(tokens)):
        return False
    going = any(t in {"gotta", "got", "gonna", "gunna", "have", "heading", "head", "off",
                      "leaving", "going", "need", "must", "should"} for t in tokens)
    away = any(t in {"go", "sleep", "bed", "now", "out", "soon", "off"} for t in tokens)
    if going and away and all(t in LEAVING_WORDS for t in tokens):
        return True
    if any(t in BYE_TIME for t in tokens) and all(
            t in BYE_TIME or t in {"back", "in", "a", "see", "you", "u", "ya"} for t in tokens):
        return True
    if "night" in tokens or "later" in tokens:
        return not DESCRIBES_THE_DAY.search(" ".join(tokens))
    return False


NIGHT_SIGNOFF = {"night", "goodnight", "nightnight", "bed", "sleep", "sleeping", "tonight"}


def _bye_kind(tokens):
    return "bye_night" if any(token in NIGHT_SIGNOFF for token in tokens) else "bye"


def _ending_bye(clean, memory):
    if clean.endswith("?"):
        return False
    understood = memory.get("understood") if isinstance(memory, dict) else None
    clauses = understood.get("clauses") if isinstance(understood, dict) else None
    if not clauses:
        clauses = [_tokens(part) for part in re.split(r"[.!?]+", clean) if part.strip()]
    return len(clauses) > 1 and _is_bye(clauses[-1])


EARLY_NIGHTS = (
    (re.compile(r"\b(?:keep|keeps|always|still) (?:waking|wake)(?: up)?(?: at| around)? \d|"
                r"wake(?:s| up)? at (?:the same|\d)|woke up at \d"),
     ("Waking at the same time every night is common and it passes. Don't watch the clock: if "
      "you're still awake after twenty minutes, get up and read something dull in low light.",
      "That clockwork wake-up is your body clock, not a fault. Keep the room cool and dark, and "
      "don't lie there fighting it — get up, then go back when you feel heavy again.")),
    (re.compile(r"\b(?:been |was )?up since \d|up since (?:the |about |half |\d)|"
                r"up at \d (?:am|o'clock)|been up since"),
     ("That's an early start, and it makes the whole day heavier. If there's anyone who can "
      "take a turn later, use them and get a proper rest.",
      "Long morning already. Get outside for ten minutes when you can — daylight is what tells "
      "your body what time it is.")),
    (re.compile(r"\bup all night|awake all night|no sleep|didn'?t sleep|didn'?t get any sleep|"
                r"slept badly|bad night|sleepless|"
                r"(?:terrible|awful|rubbish|rotten|bad|poor|lousy) (?:night'?s? |nights )?sleep|"
                r"slept (?:terribly|awfully|badly|rotten|horribly|awful|terrible|rubbish|lousy)|"
                r"(?:hardly|barely)(?: any)? slept|(?:hardly|barely) any sleep|broken sleep"),
     ("Rough night, then. Coffee only covers so much — get twenty minutes flat on your back this "
      "afternoon if you can, and keep the evening quiet.",
      "That's a hard one to carry into a day. Go easy on yourself today and aim for bed an hour "
      "earlier tonight.")),
)


OTHER_AWAKE = re.compile(
    r"\b(?:my|our|the|his|her) (?:\d+ )?(?:baby|son|daughter|kid|kids|child|children|toddler|"
    r"year[- ]olds?|"
    r"little one|little boy|little girl|littleun|littlun|newborn|grandson|"
    r"granddaughter|grandchild|twins|teenager|teen|stepson|stepdaughter|stepchild|husband|"
    r"wife|partner|mum|dad|dog|cat|"
    r"puppy|kitten|flatmate|neighbours?|neighbor)\b[^.?!]*?\b(?:up since|up all night|awake|"
    r"up from|won'?t|wont|can'?t|cant)\b"
    r"|\b(?:my|our|the|his|her) (?:boy|girl|lad|lass)\b[^.?!]*?"
    r"\b(?:up since|up from|up every morning)\b"
    r"|\b(?:little one|little boy|little girl|littleun|littlun|toddler|newborn)\b[^.?!]*?"
    r"\b(?:up since|up all night|awake|up from)\b"
    r"|\b(?:been |was )?up (?:since|all night|all hours|at \d)\b[^.?!]*?"
    r"\bwith (?:a |the |my |our |his |her )?(?:sick|poorly|ill|unwell|"
    r"teething|crying|colicky|newborn)\b")
LOSS = re.compile(r"\b(?:died|dying|death|dead|passed away|funeral|burial|cremation|bereave\w*|"
                  r"lost my (?:mum|mom|dad|father|mother|wife|husband|son|daughter|brother|"
                  r"sister|partner|baby|child)|(?:mum|mom|dad|father|mother|wife|husband|son|"
                  r"daughter|brother|sister|partner|gran|nan|grandad)\s+(?:has|have|had)\s+"
                  r"(?:just )?(?:died|passed))\b")

OTHER_SLEPT = re.compile(
    r"\b(?:my|our|the|his|her|their) (?:baby|son|daughter|kid|kids|child|children|husband|wife|"
    r"partner|mum|mom|dad|mother|father|brother|sister|friend|flatmate|roommate|neighbours?|"
    r"neighbor|dog|cat|puppy|kitten)\b[^.?!]*?\b(?:sleep|slept|sleeping|naps?|night)\b"
    r"|\b(?:he|she|they)\b[^.?!]*?\b(?:sleep|slept|sleeping|barely|hardly)\b")

SPEAKER_LOST = re.compile(
    r"\bi\b[^.?!]{0,24}?\b(?:barely|hardly|didn'?t|didnt|couldn'?t|couldnt|never|not)\b"
    r"[^.?!]{0,16}?\b(?:sleep|slept|sleeping|wake|woke|slept a wink)\b"
    r"|\bi\b[^.?!]{0,12}?\b(?:was|am|been|got|kept|keep)\s+(?:up|awake)\b"
    r"|\bi\b[^.?!]{0,10}?\bslept\b"
    r"|\b(?:woke|woken|wakes) me\b")


SORE_NIGHTS = (
    "Being awake with something that hurts is worth mentioning to a GP or pharmacist, "
    "especially if it is the same place every night. Tonight, prop yourself up, keep the room "
    "cool and skip the clock-watching.",
    "Waking because of pain or a cough is your body asking for attention, not a bad habit. If it "
    "has gone on a few nights, get it looked at; for tonight, sit up and take the weight off it.",
)

SYMPTOM = re.compile(r"\b(?:pain|painful|ache|aches|aching|achy|hurt|hurts|hurting|cramp|cramps|"
                     r"cough|coughing|tooth|toothache|toothaches|headache|headaches|migraine|"
                     r"migraines|earache|earaches|backache|stomachache|tummyache|heartburn|"
                     r"reflux|nausea|nauseous|sick|fever|itch|itching|sore|swollen|stiff)\b")

END_OF_ROPE = re.compile(r"\b(?:can'?t|cannot) (?:do this|go on|take it|cope|keep going)\b|"
                         r"\bend(?:ing)? it\b|\bkill myself\b|\bhurt myself\b|\bwant to die\b|"
                         r"\bno point\b|\bhearing things\b|\bseeing things\b|\bnot worth it\b")

WORRY = re.compile(r"\b(?:worried|worry|worrying|worries|stress(?:ed|ful|ing)?|anxious|anxiety|"
                   r"overthink\w*|overwhelm\w*|on my mind|can'?t switch off|racing|panic(?:king)?)\b|"
                   r"\b(?:we|i|he|she|they) had a (?:row|argument|fight|falling out)\b|"
                   r"\bargued (?:with|about)\b|\bfell out with\b|\brow with\b")


FREQUENCY_ONLY = re.compile(
    r"^\W*(?:(?:and|but|so|oh|well|yeah|yep|ok|okay|right|alright|no)\W+)*"
    r"(?:(?:it'?s|its|it is|that'?s|thats|there'?s|theres)\s+)?"
    r"((?:(?:every|most)(?:\s+single)?\s+(?:night|nights|morning|mornings|day|days)"
    r"|all\s+(?:the\s+)?time|nightly|daily|constantly|non ?stop))"
    r"\b(?:\s+(?:now|though|at the moment|lately|these days|still))*\W*$", re.I)
NIGHT_FREQUENCY = (
    "{often} is a lot. How long has it been like that?",
    "{often}, then. That wears you down - has it been going on long?",
    "{often}, then. Is that recent, or has it been like this for weeks?",
)
NIGHT_FREQUENCY_KEPT = (
    "{often}, then. Tonight, keep the room cool and dark, and if you are still awake after "
    "twenty minutes get up and read something dull until you feel heavy.",
    "{often}, then - keep the same getting-up time every day, even after a bad one; that is the "
    "bit that steadies it.",
    "{often}, then. Leave the phone out of reach and get ten minutes of daylight early; if it is "
    "still like this in a few weeks, go back to the GP.",
)
BODY_FREQUENCY = (
    "{often} is a lot. How long has it been going on?",
    "{often}, then - is that recent, or has it been like this a while?",
    "{often} is worth a proper look. Has it been going on for weeks?",
)
BODY_FREQUENCY_KEPT = (
    "{often}, then. That is enough to get it looked at if it keeps on, and a note of when it is "
    "worst helps.",
    "{often} is a lot. Keep a note of what sets it off and what you have tried, and take that to "
    "the GP.",
    "{often} is your body asking for a proper look. Book the GP and take a week of notes with you.",
)


def _frequency_of_the_last_trouble(clean, memory=None):
    frequency = FREQUENCY_ONLY.match(clean)
    if not frequency:
        return None
    often = frequency.group(1).strip()
    often = often[:1].upper() + often[1:]
    if not isinstance(memory, dict):
        return None
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns:
        return None
    last = turns[-1] if isinstance(turns[-1], dict) else {}
    said = " ".join(str(last.get("user") or "").lower().split())
    if not said or _loss_recent(memory) or WORRY.search(said):
        return None
    night_phrase = bool(re.search(
        r"\b(?:night|nights|morning|mornings|nightly|all\s+(?:the\s+)?time|constantly)\b",
        often, re.I))
    night = night_phrase and _my_night(said) and not NOT_MY_NIGHT.search(said)
    body = not night and not NOT_MY_NIGHT.search(said) and (
        SYMPTOM.search(said) or reads_like_a_symptom(said))
    if not (night or body):
        return None
    earlier = str(last.get("bot") or "")
    kept = bool(re.search(r"\b(?:how long|how often|weeks?|months?)\b", earlier, re.I))
    pool = NIGHT_FREQUENCY_KEPT if night and kept else (
        NIGHT_FREQUENCY if night else BODY_FREQUENCY_KEPT if kept else BODY_FREQUENCY)
    return tuple(line.format(often=often) for line in pool)


_A_CHILD_OR_THEM = re.compile(
    r"\b(?:child|children|kid|kids|baby|babies|toddler|they|them|their|he|she|him|her)\b", re.I)


def _answers_has_the_frequency(clean, memory):
    if not isinstance(memory, dict):
        return False
    try:
        from . import answers
        guess = copy.deepcopy(memory)
        said = answers.respond(clean, guess)
    except Exception:
        return False
    if not said:
        return False
    flat = " ".join(str(said).lower().split())
    if not flat or _A_CHILD_OR_THEM.search(flat):
        return False
    turns = memory.get("turns") or []
    before = " ".join(str((turns[-1] or {}).get("bot") or "").lower().split()) if turns else ""
    if flat.startswith("same answer") or (before and before[:60] in flat):
        return False
    return True


def _frequency_is_the_turn(clean, memory=None):
    if END_OF_ROPE.search(clean) or OTHER_AWAKE.search(clean) or LOSS.search(clean):
        return False
    try:
        if _answers_has_the_frequency(clean, memory):
            return False
        return bool(_frequency_of_the_last_trouble(clean, memory))
    except Exception:
        return False


def after(text, reply, memory=None):
    if not isinstance(memory, dict):
        return
    try:
        clean = " ".join(str(text or "").lower().replace("\u2019", "'").split())
        pool = _frequency_of_the_last_trouble(clean, memory)
        memory["frequency_reply"] = bool(pool and str(reply or "") in pool)
        turns = memory.get("turns")
        behind = turns[-1] if isinstance(turns, list) and turns else None
        behind = behind if isinstance(behind, dict) else {}
        memory["frequency_answer"] = (str(behind.get("bot") or "")
                                      if memory["frequency_reply"]
                                      and behind.get("module") == "answers" else "")
    except Exception:
        memory["frequency_reply"] = False
        memory["frequency_answer"] = ""


def _early_start(clean, memory=None):
    ours = bool(SPEAKER_LOST.search(clean))
    if END_OF_ROPE.search(clean) or OTHER_AWAKE.search(clean):
        return None
    if OTHER_SLEPT.search(clean) and not ours:
        return None
    if LOSS.search(clean) or _loss_recent(memory) or WORRY.search(clean):
        return None
    frequency = _frequency_of_the_last_trouble(clean, memory)
    if frequency:
        return frequency
    for pattern, replies in EARLY_NIGHTS:
        if pattern.search(clean):
            if SYMPTOM.search(clean):
                return SORE_NIGHTS
            if LOW_MOOD.search(clean) or _low_mood_recent(memory):
                return MOOD_NIGHTS
            return replies
    return None


def _worry_kind(clean):
    if WORRY_EVENT.search(clean):
        return "anxious"
    if WORRY_PERSON.search(clean):
        return "worry_person"
    if WORRY_ABOUT_THING.search(clean):
        if WORRY_WHEN.search(clean):
            return "anxious"
        return "worry"
    return "anxious"
SKILL = re.compile(r"\b(?:not|never)\s+(?:very\s+|that\s+|really\s+)?"
                   r"(?:great|good|brilliant|amazing|fantastic|the best)\s+(?:at|with|in)\s+"
                   r"(?!(?:all|least|the|this|that|it|first|home|work|school|uni|university|"
                   r"college|everything|anything|life|myself)\b)[a-z]")


def _without_skills(clean):
    return SKILL.sub(" ", clean)


EMOTION_FEELING = {"sad": "sad", "lonely": "lonely", "angry": "annoyed", "anxious": "anxious",
                   "tired": "tired", "happy": "happy", "bored": "bored", "confused": "confused",
                   "unwell": "rough_day"}
PANIC_NOW = re.compile(
    r"\b(?:i'?m|im|i am|i think i'?m|i think im|i'?ve|ive)\b[^.?!]{0,18}?"
    r"\b(?:having|getting|got|in the middle of)\b[^.?!]{0,12}?\bpanic attacks?\b"
    r"|(?:\A|\b(?:having|getting|got|in the middle of)\s+)(?:a |another )?panic attacks?"
    r"\s+(?:right now|now|at the moment)\b"
    r"|\b(?:i'?m|im|i am)\s+(?:properly |really |actually |starting to )?panick(?:ing|y)\b"
    r"(?!\s+(?:about|over|because|that|at|for|since)\b)")
PANIC_SOMEONE_ELSE = re.compile(
    r"\b(?:my|his|her|their|your)\s+\w+[^.?!]{0,16}?\b(?:had|has|having|were|was|got)\b"
    r"|\b(?:he|she|they|we|you)\s+(?:is|are|was|were|had|has|have|kept|keeps|gets?|suffers?|"
    r"struggles?)\b[^.?!]{0,12}?\bpanic"
    r"|\b(?:last|past)\s+(?:year|night|week|month|summer|winter|time)\b"
    r"|\b(?:years|months|weeks|days) ago\b")


SELF_CUE = re.compile(r"\b(i'm|im|i am|i was|i were|i feel|i felt|ive|i've|i have|"
                      r"we are|we were|we're|were|weve|we've|we have)\b")
LOST_THE_THREAD = re.compile(
    r"\b(?:i|we)\s+(?:just\s+|still\s+|really\s+|honestly\s+|literally\s+)?"
    r"(?:do not|dont)\s+(?:understand|get it|get this|follow|follow it)\b"
    r"|\b(?:i|we)\s+(?:just\s+|still\s+|really\s+)?(?:cannot|cant|can not)\s+"
    r"(?:get|make)\s+(?:my|any)\s+head\s+(?:round|around|straight)\b"
    r"|\bstruggling\s+to\s+(?:understand|follow|get (?:my|it|this))\b"
    r"|\bhead\s+(?:nor|or)\s+tail\b")
THING_OF = re.compile(r"\bof\s+[a-z]")


BARE_FILLER = frozenset("""
im i'm i am i am feel feeling felt been bit a little kind of kinda sorta sort so really very
pretty quite just still totally too now today tonight again tbh tho though atm rn lol haha
honestly actually and but me that this it is
""".split())


A_THANK_YOU_AT_THE_END = re.compile(
    r"(?:\s*,?\s*(?:thanks|thank you|thank|thx|ty|ta|cheers|cheerz))+\s*[.!?]*$", re.I)

PLAIN_GOOD_WORDS = frozenset("""good great fine grand brilliant lovely perfect cool sweet""".split())
PLAIN_GOOD_ASKED = frozenset("""ok okay alright well""".split())
PLAIN_GOOD_FRAME = frozenset("""feel feeling felt""".split())
PLAIN_GOOD_FILLERS = frozenset("""im i am doing so very really today still all enough too
                                  honestly actually myself feel feeling been""".split())
PLAIN_GOOD_TAIL = frozenset("""here now tonight around about cheers ta thanks thank mate love
                               side on my we are yeah its""".split())


def _the_bot_just_asked_them(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)] if memory else []
    if not turns:
        return False
    said = str(turns[-1].get("bot") or "").rstrip()
    return said.endswith("?")


GOOD_POOLS = frozenset({"happy"})


def _a_thank_you_taken_off(clean, memory=None):
    folded = A_THANK_YOU_AT_THE_END.sub("", clean).strip(" ,.!?")
    if not folded or folded == clean or len(folded.split()) > 4:
        return ""
    padded = " " + folded + " "
    for pool, words in FEELINGS:
        for word in words:
            if " " + word + " " in padded:
                if pool in GOOD_POOLS and not _the_bot_just_asked_them(memory):
                    return ""
                return folded
    if _a_plain_good_answer(folded, memory):
        return folded if _the_bot_just_asked_them(memory) else ""
    return ""


def _a_plain_good_answer(clean, memory=None):
    if "?" in clean:
        return False
    if re.search(r"\bnot (?:too |half |so )?bad\b", clean):
        return True
    words = [w.strip(".,!?;:") for w in clean.split() if w.strip(".,!?;:")]
    if not words or len(words) > 7:
        return False
    if not any(word in PLAIN_GOOD_WORDS or word in PLAIN_GOOD_ASKED for word in words):
        return False
    if not all(word in PLAIN_GOOD_WORDS or word in PLAIN_GOOD_ASKED
               or word in PLAIN_GOOD_FILLERS or word in PLAIN_GOOD_TAIL for word in words):
        return False
    soft = any(word in PLAIN_GOOD_ASKED for word in words)
    if soft and not (set(words) & PLAIN_GOOD_FRAME) and not _the_bot_just_asked_them(memory):
        return all(word in PLAIN_GOOD_WORDS or word in PLAIN_GOOD_FILLERS for word in words)
    return True


MEANT_LEADS = tuple(sorted(lead.split("{", 1)[0].strip().lower()
                           for lead in meant.REPEAT_LEADS + meant.LEADS))


def _bare_feeling(clean):
    rest = [word.strip(".,!?;:") for word in clean.split()]
    rest = [word for word in rest if word and word not in BARE_FILLER]
    if not rest or len(rest) > 2 or set(rest) & NOT_WORDS:
        return None
    for name, words in FEELINGS:
        if all(word in words for word in rest):
            return name
    return None


PERSON_WORDS = frozenset("""i we you he she they me us them him her who whoever someone somebody
anybody nobody everyone everybody people""".split())


CONTRACTIONS = frozenset("""im ive id ill youre youve theyre thats its weve were dont didnt doesnt
wont cant isnt arent wasnt havent hasnt""".split())


CAUSES_THE_FEELING = frozenset("""boring tiring exhausting annoying worrying frightening
scary draining relaxing depressing frustrating embarrassing confusing mad stressful overwhelming
knackering""".split())


HABIT_VERBS = frozenset(("keep", "keeps", "kept"))


RELIEF_SAID = re.compile(
    r"\b(?:relieved|relief)\b|\b(?:what|such)\s+a\s+relief\b"
    r"|\bweight\s+off\s+(?:my|her|his|their|your)\s+(?:shoulders|mind)\b", re.I)


def _says_relief(clean):
    return bool(RELIEF_SAID.search(clean)) and not negated(clean, "relieved")


CLAUSE_JOIN = frozenset(("but", "and", "so", "though", "tho", "because", "cos", "cause",
                         "although", "yet", "plus", "then", "also", "still", "even",
                         "except", "whereas", "while", "which"))


CLAUSE_SUBJECT = frozenset(("i", "im", "i'm", "ive", "i've", "we", "we're", "were", "weve",
                            "he", "hes", "she", "shes", "they", "theyre", "you", "youre",
                            "it", "its", "there", "theres",
                            "my", "our", "your", "his", "her", "their", "the", "a", "an",
                            "this", "that", "these", "those"))


def _starts_a_clause(after):
    return any(word.strip(".,!?;:").lower() in CLAUSE_SUBJECT for word in after)


def _in_its_clause(before):
    for index in range(len(before) - 1, -1, -1):
        word = before[index]
        if word.endswith((",", ";", ":", ".", "!", "?",)):
            return before[index + 1:]
        if word.strip(".,!?;:").lower() in CLAUSE_JOIN and _starts_a_clause(before[index + 1:]):
            return before[index + 1:]
    return before


def _owned_by_a_thing(clean, match):
    if clean[match.start():match.end()].lower() in CAUSES_THE_FEELING:
        return bool(A_LABEL_ON_THE_PERSON.search(clean))
    before = _in_its_clause(clean[:match.start()].split())
    owner = _owner(before)
    if owner in PERSON_WORDS:
        return False
    if owner is not None:
        return owner not in OWN_STATES
    if not before:
        return False
    word = before[-1].strip(".,!?;:").lower()
    bare = word.replace("'", "").replace("\u2019", "")
    if (word in FUNCTION_WORDS or word in INTENSIFIERS or bare in CONTRACTIONS
            or word in HABIT_VERBS
            or COPULA.match(word) or (len(word) > 4 and word.endswith(("ing", "ly")))
            or " ".join(part.strip(".,!?;:") for part in before[-2:]).lower()
            in INTENSIFIER_PAIRS):
        return False
    return word not in OWN_STATES


OWN_BEEN = re.compile(r"\b(?:i'?ve|ive|we'?ve|weve)\s+(?:been|had)\b")


def _own_state(clean):
    if OWN_BEEN.search(clean):
        return True
    words = [word.strip(".,!?;:").lower() for word in clean.split()]
    for index, word in enumerate(words):
        if word in ("my", "our") and any(near in STATE_NOUNS for near in words[index + 1:index + 3]):
            return True
    return False


def _said_of_the_person(clean, match):
    before = clean[:match.start()].split()
    after = clean[match.end():].split()
    owner = _owner(before)
    stated = owner in STATE_NOUNS or (bool(before) and before[-1].strip(".,!?;:").lower()
                                      in ("my", "our"))
    if after and after[0].strip(".,!?;:").lower() in STATE_NOUNS:
        return True
    if stated:
        return not after or _carries_on(after[0])
    intensified = bool(before) and (before[-1] in INTENSIFIERS
                                    or " ".join(before[-2:]) in INTENSIFIER_PAIRS)
    if not intensified:
        return False
    if after and not _carries_on(after[0]):
        return False
    return owner is None or owner in OWN_STATES


def _carries_on(word):
    word = word.strip(".,!?;:").lower()
    if word in FUNCTION_WORDS:
        return True
    return len(word) > 4 and word.endswith("ing")


def _owner(before):
    for index in range(len(before) - 1, -1, -1):
        if not COPULA.match(before[index].strip(".,!?;:")):
            continue
        subject = [word.strip(".,!?;:") for word in before[:index]
                   if word.strip(".,!?;:").lower() not in DETERMINERS
                   and word.strip(".,!?;:").lower() not in FUNCTION_WORDS
                   and word.strip(".,!?;:").lower() not in INTENSIFIERS]
        if not subject:
            return None
        for word in reversed(subject):
            if word.lower() in STATE_NOUNS:
                return word.lower()
        return subject[-1].lower()


HARD_ON_THE_PERSON = frozenset((
    "exhausting", "draining", "tiring", "knackering", "stressful", "overwhelming", "wearing out",
))
LIFE_THING_HARD = re.compile(
    r"\b(?:my |our |the |this |these )?(?:work|job|jobs|week|weeks|month|months|year|term|shift|"
    r"shifts|commute|project|deadlines?|course|coursework|placement|revision|school|uni|office|"
    r"team|rota|days?|nights?|mornings?|house|flat|move|money|kids|children|family|life)\b"
    r"[^.!?]{0,20}?\b(?:is|are|was|were|been|has been|have been|'s been)\s+"
    r"(?:(?:so|really|very|pretty|just|quite|absolutely|always|still|bloody|too)\s+){0,2}$",
    re.I)


def _hard_about_their_thing(clean):
    for word in HARD_ON_THE_PERSON:
        at = clean.find(word)
        if at > 0 and LIFE_THING_HARD.search(clean[:at]):
            return True
    return False


_OTHER_SUBJECT = re.compile(r"\b(?:he|she|they|him|her|them)\b", re.I)
WEARS_OTHER_PEOPLE_OUT = frozenset(("exhausting", "draining", "tiring", "knackering"))


def _a_person_who_wears_you_out(clean, word, match):
    if word not in WEARS_OTHER_PEOPLE_OUT:
        return False
    before = clean[:match.start()]
    if OTHER_PERSON.search(before):
        return True
    return bool(_OTHER_SUBJECT.search(before)) and not re.search(r"\b(?:i|im|i'm|we)\b", before)


def _says_how_the_person_is(clean, word, match):
    if _a_person_who_wears_you_out(clean, word, match):
        return False
    if _owned_by_a_thing(clean, match):
        return _said_of_the_person(clean, match)
    if word in HARD_ON_THE_PERSON and LIFE_THING_HARD.search(clean[:match.start()]):
        return True
    return cue_about_person(clean, word) or _said_of_the_person(clean, match)

GUILT_WORDS = ("guilty", "bad", "awful", "terrible", "rotten", "horrible", "ashamed", "sick")


STATE_WHEN = re.compile(
    r"\s+(?:this|that|the current)\s+(?:week|month|year|morning|afternoon|evening|weekend)\b.*$"
    r"|\s+at the moment\b.*$|\s+right now\b.*$", re.I)


WANT_TO_WEEP = re.compile(r"\b(?:want|wanna|need|needs|would like|just want|really want)\s+to\s+"
                          r"(?:cry|weep|sob|bawl)\b|\b(?:feel like|feels like)\s+"
                          r"(?:crying|weeping|sobbing)\b|\bon the verge of (?:tears|crying)\b"
                          r"|\b(?:could|might|may|would)\s+(?:just\s+|really\s+|honestly\s+|"
                          r"actually\s+|easily\s+)?(?:cry|weep|sob|bawl)\b"
                          r"|\babout to\s+(?:just\s+)?(?:cry|weep|sob|bawl)\b")
WEEPING_WITH_JOY = re.compile(r"\b(?:with relief|of relief|happy tears|tears of joy|so relieved|"
                              r"laughing\b|\blaugh\b|could cry with|laugh(?:ed|s)? (?:so|until)|"
                              r"happ(?:y|ier)|relieved|proud|thrilled|excited|made it)\b", re.I)
WHY_THE_TEARS = re.compile(r"\b(?:why|how come|any idea why)\b", re.I)
SOMEBODY_ELSE = re.compile(
    r"\b(?:he|she|they|it|you|him|her|them|my \w+|his|her|their|your)\s+(?:\w+\s+)?"
    r"(?:could|might|may|would|is about to|was about to|were about to)\s+(?:just\s+|really\s+|"
    r"honestly\s+|actually\s+|easily\s+)?(?:cry|weep|sob|bawl)\b", re.I)
NOT_THEIR_TEARS = re.compile(r"\b(?:the|a|this|that) (?:film|book|show|programme|program|"
                             r"documentary|song|episode|video|story|news|game|series)\b"
                             r"|\b(?:it|that|this) (?:made|makes|had) me\b"
                             r"|\b(?:he|she|they|my \w+|his|her|their) (?:made|makes|make|"
                             r"is making|are making|had me|has me|keeps making) me\b", re.I)
NOT_WANTING_IT = re.compile(r"\b(?:not|dont|doesnt|didnt|never|no)\b[^.?!]{0,24}\b(?:want|wanna|"
                            r"need)\s+to\s+(?:cry|weep|sob|bawl)\b"
                            r"|\btrying not to (?:cry|weep|sob|bawl)\b|\bholding back the tears\b",
                            re.I)


MOVED_BY = re.compile(
    r"\b(?:at|during|watching|reading|listening to|over)\s+(?:a\s+|an\s+|the\s+|my\s+|some\s+)?"
    r"(?:film|films|movie|movies|advert|adverts|ad|ads|telly|tv|song|songs|"
    r"video|videos|programme|programmes|documentary|documentaries|book|books|show|shows|"
    r"series|episode|episodes|story|stories|photo|photos|picture|pictures)\b", re.I)

MOVED_BY_PART = re.compile(
    r"\b(?:at|during|watching|reading|listening to|over)\s+(?:a\s+|an\s+|the\s+|my\s+|some\s+)?"
    r"(?:[a-z']+\s+){1,3}of\s+(?:a\s+|an\s+|the\s+|my\s+)?"
    r"(?:film|films|movie|movies|advert|adverts|ad|ads|telly|tv|song|songs|"
    r"video|videos|programme|programmes|documentary|documentaries|book|books|show|shows|"
    r"series|episode|episodes|story|stories|photo|photos|picture|pictures)\b", re.I)

MY_TEARS = re.compile(
    r"\b(?:i|i've|ive|we|we've|weve)\b(?:\s+\w+){0,2}?\s+"
    r"(?:cry|crying|cried|cries|weep|weeping|wept|sob|sobbing|bawl|bawling|blub|blubbing|"
    r"welling up|welled up|welling|tearing up|teared up|choked up)\b"
    r"(?!\s+(?:about|because|over)\s+(?:my|his|her|their)\s+\w+)", re.I)

CANT_STOP_IT = re.compile(r"\b(?:can'?t|cant|cannot|couldn'?t|couldnt)\s+stop\b", re.I)

SOMEONE_IN_THEIR_OWN_TEARS = re.compile(
    r"\b(?:him|her|them|me|us|you|my|his|their|your)\b", re.I)


_WEEP_WORDS = frozenset(("crying", "cry", "cried", "cries", "weepy", "tearful", "tears",
                         "in tears", "sob", "sobbing", "weep", "weeping", "wept", "bawl",
                         "bawling", "blub", "blubbing", "welling up", "burst into tears",
                         "bursting into tears", "tearing up", "tear up", "choked up"))


def _my_own_tears(clean):
    moved = MOVED_BY.search(clean)
    before = clean[:moved.start()] if moved else clean
    mine = FIRST_PERSON.search(before)
    if not mine:
        return False
    someone = SOMEONE_ELSE.search(before)
    return not someone or mine.start() < someone.start()


def _a_low_word(clean):
    for _name, words in FEELINGS:
        for word in words:
            if word in _WEEP_WORDS:
                continue
            if re.search(r"\b" + re.escape(word) + r"\b", clean):
                return True
    return False


def _good_news(clean):
    flat = clean.replace("'", "")
    if asks_for_news(flat):
        return False
    return any(pattern.search(flat) for pattern in GOOD_NEWS)


KEEPS_HOW_THEY_ARE = re.compile(r"\b(?:i|we)\s+(?:keep|keeps|kept)\b")

KEEPS_HOW_I_AM = re.compile(r"\bi\s+(?:keep|keeps|kept)\b")


A_NAMED_LOW = re.compile(
    r"\b(?:feel|feeling|felt|i'?m|im|i am|i'?ve|ive|i have)\b[^.]{0,18}?\b(?:low|sad|down|depressed|"
    r"miserable|heartbroken|devastated|hopeless|empty|numb|lonely|anxious|overwhelmed|"
    r"awful|terrible|dreadful|rubbish|crap|rough)\b")


def _weeping(clean):
    if not WANT_TO_WEEP.search(clean):
        return False
    if NOT_WANTING_IT.search(clean) or NOT_THEIR_TEARS.search(clean) or SOMEBODY_ELSE.search(clean):
        return False
    if WEEPING_WITH_JOY.search(clean) or WHY_THE_TEARS.search(clean):
        return False
    if A_NAMED_LOW.search(clean):
        return False
    return not _good_news(clean)


def _tears_said_as_a_verb(clean):
    match = MY_TEARS.search(clean)
    if not match:
        return None
    if SOMEONE_IN_THEIR_OWN_TEARS.search(match.group(0)):
        return None
    if (WANT_TO_WEEP.search(clean) or NOT_WANTING_IT.search(clean)
            or CANT_STOP_IT.search(clean)
            or NOT_THEIR_TEARS.search(clean) or SOMEBODY_ELSE.search(clean)
            or WEEPING_WITH_JOY.search(clean) or WHY_THE_TEARS.search(clean)
            or A_NAMED_LOW.search(clean)):
        return None
    if _good_news(clean):
        return None
    return "sad" if _going_on(clean) else "tears"


NOT_COPING = re.compile(
    r"\b(?:not|never|isn'?t|isnt|ain'?t|aint)\s+(?:"
    r"(?:really|actually)\s+(?:ok|okay|alright|fine|good|well|myself|here|sleeping|eating)\b"
    r"(?=\s*(?:$|[.,!?;]|\b(?:today|tonight|now|lately|right now|at the moment|these days|"
    r"recently|this week|this morning|tbh|honestly|really)\b))|"
    r"(?:(?:really|actually)\s+)?(?:coping\b|"
    r"managing\b(?=\s*(?:$|[.,!?]|any ?more|at all|at the moment|lately|right now|"
    r"at (?:work|home)|(?:my |the )?(?:work|job|kids|house|home|money)\b|"
    r"with (?:everything|it all|life|any of it|the kids|work|the money)))))")
NOT_COPING_SHAPES = re.compile(
    r"\b(?:i'?m|im|i am|i feel|i felt|feel|feeling|i'?ve been|ive been|i have been)\b"
    r"[^.]{0,24}?\b(?:struggling\b(?!\s+to\b)|hopeless\b|numb\b|empty\b|"
    r"falling apart\b|at the end of my tether\b|can'?t keep going\b)"
    "|"
    r"\b(?:i'?m|im|i am|i feel|i felt|feel|feeling|i'?ve been|ive been|i have been|"
    r"i had|i'?ve had|ive had|i have had|i just had|i'?ve just had|ive just had)\b"
    r"(?:\s+(?:honestly|really|properly|totally|absolutely|just|so|very|quite|kind|sort|of|a|"
    r"an|the|bit|like|having|total|nervous|im|am|been|pretty|mostly|still)\b){0,6}?\s*"
    r"(?:cracking up\b|losing it\b|spiralling\b|going under\b|breaking down\b|"
    r"at breaking point\b|wreck\b|(?:having\s+|a\s+)?(?:(?:total|nervous)\s+)?"
    r"(?:meltdown|breakdown)\b)"
    r"(?=\s*(?:$|[.,!?;]|\b(?:and|but|so|because|though|cause|about|with|over)\b|"
    r"(?:at the moment|at the minute|right now|today|tonight|this (?:week|morning|month|year)|"
    r"lately|recently|these days|tbh|honestly|to be honest|"
    r"at (?:work|school|home|uni|night))\b))")
NOT_COPING_FEEL = re.compile(
    r"\b(?:i\s+feel|i\s+felt|feel|feeling)\b[^.]{0,16}?\b(?:like\s+)?"
    r"(?:rubbish|crap|terrible|awful|dreadful)\b"
    r"(?![^.]{0,12}\b(?:at|with|in)\s+\w)"
    r"(?=\s*(?:$|[.,!?;]|\b(?:today|tonight|now|lately|right now|at the moment|these days|"
    r"recently|this week|this morning)\b))")
NOT_COPING_ANYWHERE = re.compile(
    r"\b(?:don'?t|dont|doesn'?t|doesnt|not)\s+feel\s+(?:like\s+)?(?:my|him|her|them)?self\b|"
    r"\b(?:everything|it all|it|life)\s+(?:is\s+)?(?:getting|get|gets)\s+on top of me\b|"
    r"\b(?:getting|get|gets)\s+on top of me\b|"
    r"\b(?:i|we)\s*(?:(?:have|'?ve|'?d)\s+)?had\s+enough of\s+"
    r"(?:living|life|it all|everything|being here|all this)\b|"
    r"\b(?:i|we)\s+(?:don'?t|dont|do not)\s+(?:want|wanna)\s+(?:to\s+)?(?:be here|go on|carry on)"
    r"(?=\s*(?:$|[.,!?;]|\b(?:anymore|any more|any longer|like this|this way)\b))|"
    r"\b(?:i|we)\s*(?:'?m|am)?\s*(?:sick|tired)\s+of\s+(?:living|life)\b"
    r"(?=\s*(?:$|[.,!?;]|like this\b))")
GUILT_ABOUT = re.compile(r"\b(?:awful|bad|terrible|dreadful|guilty)\s+about\b")
GOING_MAD = re.compile(
    r"\b(?:going|go|gone|went)\s+(?:mad|crazy|mental|insane)\b|"
    r"\blos(?:e|es|ing|t)\s+(?:my|the)\s+(?:mind|marbles|plot)\b|"
    r"\b(?:going|going\s+out)\s+of\s+(?:my|his|her|their)\s+mind\b")


MAD_ABOUT_THE_DAY = re.compile(
    r"\b(?:work|job|office|school|uni|college|shop|shops|town|roads|traffic|queues?|"
    r"term|day|days|week|weeks|month|months|morning|afternoon|evening|weekend|nights|it|its|"
    r"things|everything|life)\b"
    r"(?:(?:\s+(?:has|had|have|is|was|are|were|been|being|gets|got)\b)"
    r"|(?:\s*'(?:s|ve)\b)){1,3}\s*"
    r"(?:\s+(?:so|really|proper|properly|fairly|pretty|very|dead|bloody|totally|absolutely)\b)?"
    r"\s+mad\b(?!\s+(?:at|with|about)\s+(?:me|us|you|him|her|them|everyone|everybody|the\s+\w+))"
    r"|\bmad\s+(?:day|week|month|morning|afternoon|shift|one|busy|rush|time)\b")


STRUGGLING_ABOUT_A_THING = re.compile(
    r"\bstruggling\s+(?:with|through)\s+(?!everything\b|it all\b|life\b|all of it\b|"
    r"any of it\b|the kids\b|money\b|sleep\b|work\b|my mood\b|myself\b)\w+")


HOW_I_GET_THROUGH = re.compile(
    r"\bhow\s+(?:do|can|will|should|am)\s+i\s+(?:"
    r"(?:cope\b(?:\s+with)?\s*$|cope\b\s+with\s+(?:it|this|that|everything|all\s+of\s+it)\b"
    r"|cope\s+(?:it|this|that|everything)\b)"
    r"|get\s+through\b(?:"
    r"\s*$|\s+(?:(?:all\s+)?this\b(?=\s*(?:$|[.,!?;]))|it\b"
    r"|the\s+(?:week|night|day|month|days|year)\b|today\b|tonight\b))"
    r"|deal\s+with\b(?:\s*$|\s+(?:all\s+this\b(?=\s*(?:$|[.,!?;]))|it\s+all\b))"
    r"|survive\b(?:\s*$|\s+(?:it\b|the\s+(?:week|day|month|night)\b))"
    r")"
    r"|\bi\s+(?:dont|don't|do\s+not|can'?t|cant|can\s+not)\s+know\s+how\s+to\s+(?:"
    r"(?:cope\b(?:\s+with)?\s*$|cope\b\s+with\s+(?:it|this|that|everything|all\s+of\s+it)\b)"
    r"|get\s+through\b(?:\s*$|\s+(?:(?:all\s+)?this\b(?=\s*(?:$|[.,!?;]))|it\b))"
    r"|deal\s+with\b(?:\s*$|\s+(?:all\s+(?:this|of\s+this)\b|it\s+all\b))"
    r")")


def _not_coping(clean):
    text = " ".join(str(clean or "").split())
    if GUILT_ABOUT.search(text):
        return False
    if not (NOT_COPING.search(text) or NOT_COPING_SHAPES.search(text)
            or NOT_COPING_ANYWHERE.search(text) or _speaker_going_mad(text)
            or HOW_I_GET_THROUGH.search(text)):
        return False
    return not STRUGGLING_ABOUT_A_THING.search(text)


ASKS_WHY = re.compile(r"^\s*(?:why|how come|what makes|whats making|what'?s making)\b")

A_NIGHT_NOT_SLEPT = re.compile(
    r"\b(?:sleep|slept|sleeping|awake|insomnia|up all night|no sleep|not sleeping)\b")


FIRST_PERSON_BEFORE = re.compile(r"\b(?:i|im|i'm|i am|i've|ive|me|myself)\b[^.]{0,9}$")
IDIOM_PLACE = re.compile(r"^\s*(?:work|home|school|uni|college|night|the moment|the minute|"
                         r"times|first|least|times like this|it all|myself|me)\b")
FEAR_BEFORE = re.compile(r"\b(?:feel(?:s|ing)?\s+like|felt\s+like|think|thought|thinks|"
                         r"thinking|might\s+be|might|maybe|mightbe|worried|scared|afraid|"
                         r"wonder(?:ing)?|am\s+i|are\s+we|do\s+you)\b")


def _speaker_going_mad(text):
    for at in GOING_MAD.finditer(text):
        before = text[:at.start()]
        after = re.search(r"\b(?:at|about)\s+(.*)$", text[at.end():])
        if after and not IDIOM_PLACE.match(after.group(1)):
            continue
        if after and not FEAR_BEFORE.search(before):
            continue
        if FIRST_PERSON_BEFORE.search(before):
            return True
    return False


def _bad_day(clean):
    text = " ".join(str(clean or "").split())
    if (ASKS_WHY.search(text) or GUILT_ABOUT.search(text)
            or A_NIGHT_NOT_SLEPT.search(text)):
        return False
    if not NOT_COPING_FEEL.search(text):
        return False
    return not STRUGGLING_ABOUT_A_THING.search(text)


SCATTERED_MIND = re.compile(
    r"\b(?:my|our)\s+(?:head|brain|mind|thoughts|head's|thinking)\b[^.!?]{0,26}?"
    r"\b(?:all over the (?:place|shop|show)|fried|mush|scrambled|to mush|scattered|fog|foggy"
    r"|fuzzy|woolly|wooly|muzzy|cloudy|misty|thick|fogged|clogged\b"
    r"|(?:a |a right |a total |one )?mess\b)"
    r"|\b(?:my|our)\s+(?:head|brain|mind|thoughts)\b[^.!?]{0,20}?"
    r"\b(?:a|one)\s+(?:hundred|million|thousand)\s+miles\s+an\s+hour\b"
    r"|\b(?:i'?m|im|i am|i feel|i felt|feeling|feel)\s+(?:so |really |very |totally |"
    r"completely |pretty |a bit |kind of |kinda |all )*"
    r"(?:scattered|frazzled|all over the (?:place|shop|show)|in a fog|foggy|muzzy|woolly|fuzzy)\b"
    r"|\b(?:i|im|i'm|ive|i've)\s+(?:have|had|got|get|gets|keep getting)\b[^.!?]{0,4}?"
    r"\bbrain\s*fog\b")


def _scattered(clean):
    match = SCATTERED_MIND.search(clean)
    if not match:
        return False
    before = re.split(r"[.!?,;:]", clean[:match.start()])[-1].split()[-3:]
    return not any(word.strip(".,!?;:").lower() in NOT_WORDS for word in before)


APART_WHO = (r"(?:anyone|anybody|everyone|people|friends?|mates?|family|relatives?|neighbours?"
             r"|neighbors?|colleagues?|classmates?|workmates?|the lads|the girls|the others"
             r"|(?:my|our)\s+(?:friends?|mates?|family|parents|mum|mam|dad|mother|father"
             r"|brothers?|sisters?|kids?|children|cousins?|gran|nan|nana|grandma|grandad"
             r"|grandpa|aunt|auntie|uncle|folks|neighbours|neighbors))")
APART_FROM_PEOPLE = re.compile(
    r"\b(?:i|i'm|im|ive|i've|i'd|we|we're|were|weve|we've)\b[^.]{0,40}?"
    r"(?:cut (?:myself|ourselves) off|cut (?:myself|ourselves) (?:off )?from (?:everyone|everybody|"
    r"people|the world|society|friends|mates|family|my \w+|our \w+|contact|all of it|it all)"
    r"|shut (?:myself|ourselves) (?:away|off|in)"
    r"|(?:stopped|stopping) (?:seeing|speaking to|talking to|meeting) " + APART_WHO +
    r"|(?:not|haven't|havent|hadn't|hadnt) (?:seen|spoken to|talked to|heard from) (?:anyone|anybody|"
    r"any one|a soul|my \w+|our \w+|friends|mates|family)"
    r"|(?:never|hardly|rarely|don't|dont|do not) (?:see|speak to|talk to) (?:anyone|anybody|my \w+|"
    r"our \w+|people|friends|mates)"
    r"|(?:stopped|stopping) (?:going out|meeting up)"
    r"|(?:dont|don't|do not) (?:go out|see anyone|have any friends|have friends)"
    r"|(?:drifted apart|lost touch|no one to (?:talk|speak) to|nobody to (?:talk|speak) to))", re.I)
APART_SOMEONE_ELSE = re.compile(
    r"\b(?:my|our|his|her|their)\s+(?:\w+)\s+(?:cut|stopped|has stopped|had stopped|drifted)"
    r"|\bhow do i cut (?:myself|him|her|them) off from\b", re.I)


BARE_ACKS = frozenset((
    "ok", "okay", "right", "alright", "cool", "nice", "great", "good", "fine", "fair enough",
    "i see", "got it", "gotcha", "makes sense", "understood", "noted", "wow",
))
BARE_CARRY_ON = frozenset((
    "and", "so", "then", "and then", "more", "go on", "keep going", "carry on", "going on", "on",
    "go on then",
))


def _a_bare_acknowledgement(clean):
    words = re.findall(r"[a-z']+", " ".join(str(clean or "").lower().split()))
    while len(words) > 1 and words[0] in ("ok", "okay", "right", "well", "so", "and", "but", "now"):
        words = words[1:]
    return " ".join(words) in BARE_ACKS | BARE_CARRY_ON


SORRY_KINDS = frozenset(("sad", "bad_day", "rough_day", "not_coping", "venting", "own_fault",
                         "not_fair", "not_enough", "worry", "worry_person", "guilty", "missing",
                         "lonely", "lonely_apart"))
SORRY_NEWS_KINDS = frozenset(("lost_job", "bad_news"))
SORRY_LINES = frozenset(line for kind in SORRY_KINDS for line in REPLIES.get(kind, ())
                        if "{" not in line) | frozenset(
                            line for kind in SORRY_NEWS_KINDS for line in NEWS_REPLIES.get(kind, ())
                            if "{" not in line)
SORRY_MET = re.compile(
    r"\b(?:sorry to hear|i'm sorry|i am sorry|so sorry|really sorry|such sad news|"
    r"a lot to carry|that's rough|that is rough|how awful|that's awful|that's hard|that is hard|"
    r"a real loss)\b", re.I)
HEAVY_MODULES = frozenset(("loss", "grief", "safety", "urgent"))


def _the_heavy_line(memory):
    if not isinstance(memory, dict):
        return ""
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns:
        return ""
    note = memory.get("heavy_reply")
    if isinstance(note, dict) and note.get("turn") == len(turns) - 1:
        line = note.get("line")
        if isinstance(line, str) and line.strip():
            return line
        theirs = turns[-1].get("user") if isinstance(turns[-1], dict) else ""
        return str(theirs or "")
    last = {}
    for turn in reversed(turns):
        if not isinstance(turn, dict):
            break
        last = turn
        if not _a_bare_acknowledgement(" ".join(str(turn.get("user") or "").lower().split())):
            break
    theirs = last.get("user")
    seed = str(theirs or "")
    if last.get("module") in HEAVY_MODULES:
        return seed
    said = last.get("bot")
    if isinstance(said, str) and (said.strip() in SORRY_LINES or SORRY_MET.search(said)):
        return seed
    if seed.strip() and (loss_reading.reads_as_loss(theirs) or badnews.reads_as_bad_news(theirs)):
        return seed
    return ""


def _apart_from_people(clean):
    text = " ".join(str(clean or "").split())
    if not APART_FROM_PEOPLE.search(text):
        return False
    return not APART_SOMEONE_ELSE.search(text)


LONELY_STEP_WORDS = frozenset("""and so ok okay right but well what how can could should shall
    do does i we about it that this now start fix sort change then much else next""".split())


def _after_lonely(clean, memory):
    if not isinstance(memory, dict):
        return None
    note = memory.get("heavy_reply")
    if not isinstance(note, dict) or note.get("feeling") not in ("lonely", "lonely_apart"):
        return None
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns:
        return None
    if note.get("turn") != len(turns) - 1:
        return None
    words = re.findall(r"[a-z']+", " ".join(str(clean or "").lower().split()))
    if not words or len(words) > 7:
        return None
    if any(word not in LONELY_STEP_WORDS for word in words):
        return None
    if not ({"what", "how"} & set(words)) or "do" not in words:
        return None
    return _reply("lonely_step", memory, None, " ".join(words))


NOTHING_HELPING = re.compile(
    r"\bnothing (?:seems to |really |ever |at all |much |has |had )?(?:help|helps|helped|work|works|"
    r"worked|(?:is|isnt|isn't) (?:helping|working))\b"
    r"|\bnothing (?:seems to )?makes? (?:any )?difference\b"
    r"|\b(?:ive|i've|i) tried (?:everything|it all|all of it)\b"
    r"|\b(?:doesnt|doesn't|didnt|didn't) (?:help|work|make any difference)\b"
    r"|\b(?:isnt|isn't|is not) (?:helping|working)\b", re.I)


def _idk_kind(memory):
    if not isinstance(memory, dict):
        return "idk"
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns:
        return "idk"
    note = memory.get("heavy_reply")
    if (isinstance(note, dict) and note.get("feeling") in HEAVY_FEELINGS
            and note.get("turn") == len(turns) - 1):
        return "idk_heavy"
    last = turns[-1]
    said = str(last.get("bot") or "") if isinstance(last, dict) else ""
    if not said.strip():
        return "idk"
    if _offered_a_choice(said):
        return "idk_choice"
    if said.rstrip().endswith("?"):
        return "idk_asked"
    return "idk"


def _offered_a_choice(said):
    for clause in re.split(r"(?<=[.!?])\s+", str(said or "")):
        if re.search(r",\s*[^,.;:]{2,60},\s*or\s+[^,.;:]{2,60}\s*\.?\s*$", clause, re.I):
            return True
    return False


def _a_low_just_before(memory):
    if not isinstance(memory, dict):
        return False
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns:
        return False
    note = memory.get("heavy_reply")
    if (isinstance(note, dict) and note.get("feeling") in HEAVY_FEELINGS
            and note.get("turn") == len(turns) - 1):
        return True
    last = turns[-1]
    said = last.get("user") if isinstance(last, dict) else None
    if not isinstance(said, str) or not said.strip():
        return False
    try:
        read = understanding(said)
    except Exception:
        return False
    if read.get("intent") != "feeling" or (read.get("polarity") or 0) > 0:
        return False
    return read.get("emotion") not in ("happy", "relieved", "excited", "proud")


NOTHING_CONTINUED = re.compile(
    r"^(?:and\s+|but\s+)?(?:i(?:\s*'ve|\s*ve|\s+have)?\s*(?:tried|try|keep)|nothing|none of it|"
    r"it|that|this|they|even)\b", re.I)


def _nothing_helped_just_before(memory, clean):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return False
    last = turns[-1]
    said = " ".join(str(last.get("bot") or "").split()) if isinstance(last, dict) else ""
    if not said or len(clean.split()) > 12:
        return False
    return bool(said in REPLIES["nothing_helps"] and NOTHING_CONTINUED.search(clean))


def _nothing_helps(clean, memory):
    if not NOTHING_HELPING.search(clean):
        return None
    if not (_a_low_just_before(memory) and len(clean.split()) <= 8
            or _nothing_helped_just_before(memory, clean)):
        return None
    return _reply("nothing_helps", memory, None, clean)


def _as_said(clean, understood):
    if isinstance(understood, dict):
        plain = understood.get("plain")
        if plain:
            return " ".join(str(plain).lower().split())
    return clean


MIGHT_BE = re.compile(
    r"\bi\s+(?:think\s+(?:that\s+)?i\s+)?(?:might|may|could|probably)\s+(?:also\s+|just\s+|"
    r"honestly\s+|actually\s+)?be\s+(?:(?:getting|feeling|a\s+bit|very|really|pretty|quite|so|"
    r"too|this|kind\s+of|sort\s+of)\s+)*(?P<state>[a-z]+)", re.I)


def _without_the_might(clean):
    def put(match):
        state = match.group("state").lower()
        if not _feeling("im " + state):
            return match.group(0)
        return "im " + state
    with_states = MIGHT_BE.search(clean)
    return MIGHT_BE.sub(put, clean, count=1) if with_states else clean


A_VERDICT_ASKED = re.compile(
    r"\b(?:would|will|am|is|are|was|were)\s+"
    r"(?:i|we|it|that|this|they|he|she|you|a|an|the|going|moving|getting|leaving|buying|"
    r"selling|quitting|starting|taking|doing)\b"
    r"[^.!?]{0,40}?\b(?:mad|crazy|stupid|daft|weird|selfish|silly|unreasonable|idiot|bad)\b"
    r"(?=\s*(?:$|[.,!?;]|to\b|if\b|for\b|about\b|that\s+(?:i\s+(?:want|should|need|can|could|"
    r"may|might)|we\b|my\b|they\b|he\b|she\b)))", re.I)

A_QUESTION_ABOUT_A_FIGURE = re.compile(
    r"^(?:so |and |but |ok |okay |sorry |oh |hmm |wait |right )*"
    r"(?:is|was|are|were) (?:that|this|it)(?: a bit| a little| way| much)? (?:too )?"
    r"(?:low|high|heavy|light|much|little|many|few|big|small|long|short|often|late|early)\b")


def _feeling(clean, understood=None, bare=None, kept=False):
    clean = _as_said(clean, understood)
    clean = _without_the_feeling_avoided(clean, understood)
    if harm_reading.reads_as_hurting_someone(clean):
        return None
    if isinstance(understood, dict) and understood.get("a_load_carried"):
        return "carrying"
    if ack.a_limit_on_the_plan(clean):
        return None
    if A_QUESTION_ABOUT_A_FIGURE.search(_as_said(clean, understood)):
        return None
    clean = STATE_WHEN.sub(" ", clean)
    if (isinstance(understood, dict) and understood.get("state_owner") not in (None, "self")
            and not FEELING_SELF.search(clean)):
        return None
    if bare is None:
        bare = _bare_feeling(clean)
    if LOW_THING.search(clean):
        clean = LOW_THING.sub(" ", clean)
    if ((isinstance(understood, dict) and understood.get("shortage"))
            or shortage_of(clean)):
        return None
    clean = _without_skills(clean)
    if FLAT_IDIOM.search(clean):
        clean = FLAT_IDIOM.sub(" ", clean)
    if ANNOUNCED_ONE.search(clean):
        rest = ANNOUNCED_ONE.sub(" ", clean)
        if NEWS_AFTER.search(rest):
            clean = rest
            bare = _bare_feeling(clean)
    if MOOD_FOR.search(clean):
        clean = MOOD_FOR.sub(" ", clean)
    if ((MOVED_BY.search(clean)
         or (MY_TEARS.search(clean) and MOVED_BY_PART.search(clean)))
            and not _a_low_word(clean)):
        if (_my_own_tears(clean) and not NOT_WANTING_IT.search(clean)
                and not _bad_day(clean) and not ROUGH_DAY.search(clean)):
            return "moved"
        return None
    tears = _tears_said_as_a_verb(clean)
    if tears:
        return tears
    if _weeping(clean):
        return "sad" if _going_on(clean) else "tears"
    if NOT_WANTING_IT.search(clean) and not _a_low_word(clean):
        return None
    asked = ASKED_ABOUT_THE_BOT.search(clean)
    mine = FEELING_SELF.search(clean)
    if asked and (mine is None or asked.start() < mine.start()):
        return None
    if SELF_INSULT.search(clean) and FEELING_SELF.search(clean):
        return "sad"
    if _not_coping(clean):
        return "not_coping"
    if _bad_day(clean):
        return "bad_day"
    if _apart_from_people(clean):
        return "lonely_apart"
    if _a_stretch_that_drags(clean):
        return "long_stretch"
    if ROUGH_DAY.search(clean) or WHAT_A_DAY.search(clean):
        return "rough_day"
    if _scattered(clean):
        return "scattered"
    if bare and not PANIC_NOW.search(clean):
        return bare
    if NOT_MYSELF.search(clean):
        return "sad"
    if (PANIC_NOW.search(clean) and not PANIC_SOMEONE_ELSE.search(clean)
            and not negated(clean, "panic")):
        return "panic"
    read = None
    if isinstance(understood, dict) and (SELF_CUE.search(clean) or LOST_THE_THREAD.search(clean)
                                         or understood.get("state_owner") == "self"):
        read = EMOTION_FEELING.get(understood.get("emotion"))
        if read and (A_FACULTY_GETTING_WORSE.search(clean) or OWN_MEMORY_OFF.search(clean)) \
                and _answers_knows(clean, {"turns": []}):
            read = None
        if read == "confused" and _confusion_names_a_thing(understood):
            read = None
        if read and understood.get("state_owner") not in (None, "self"):
            read = None
        if read and nearly(clean, read):
            read = None
        if read == "anxious" and THING_OF.search(clean):
            read = _worry_kind(clean)
        if read == "happy" and _says_relief(clean):
            read = "relieved"
        elif read == "happy" and RELIEF_SAID.search(clean) and negated(clean, "relieved"):
            read = "sad"
        if read == "annoyed" and MAD_ABOUT_THE_DAY.search(clean):
            read = "busy"
    if not (FEELING_SELF.search(clean) or FEELING_LEAD.search(clean) or read
            or _own_state(clean) or kept or _hard_about_their_thing(clean)
            or REGRET_DEED.search(clean)):
        return None
    if not any(_negated(clean, word) for word in GUILT_WORDS):
        if GUILT_DEED.search(clean) or SICK_DEED.search(clean):
            return "guilty"
    if REGRET_DEED.search(clean) and not _negated(clean, "regret"):
        return "guilty"
    denied = False
    denied_names = set()
    for name, words in FEELINGS:
        for word in words:
            match = re.search(r"\b" + re.escape(word) + r"\b", clean)
            if (match and not _a_thing_in_front(clean, word)
                    and _says_how_the_person_is(clean, word, match)):
                if word.split()[0] in NOT_WORDS:
                    return name
                if _negated(clean, word):
                    if name == "happy":
                        return "annoyed" if NOT_HAPPY_ABOUT.search(clean) else "sad"
                    denied = True
                    denied_names.add(name)
                    continue
                if word in ABILITY_WORDS and re.search(
                        r"\b" + re.escape(word) + r"\s+(?:at|with)\b", clean):
                    continue
                if name == "anxious" and WORRY_FEELING.search(clean):
                    kind = _worry_kind(clean)
                    if reads_like_a_symptom(clean):
                        continue
                    if kind == "anxious" and _own_state(clean) and not WORRY_EVENT.search(clean):
                        kind = "worry"
                    return kind
                if name in ("anxious", "stressed") and WORRY_PERSON.search(clean):
                    return "worry_person"
                if (name == "annoyed" and word == "mad"
                        and MAD_ABOUT_THE_DAY.search(clean)):
                    continue
                if word in ("tired", "bored", "done") and re.search(
                        r"\b" + re.escape(word) + r"\s+(of|with)\b", clean):
                    if re.search(r"\b" + re.escape(word) +
                                 r"\s+(of|with)\s+(everything|anything|it all|life|the lot|"
                                 r"the world|myself)\b", clean):
                        return "sad"
                    return "annoyed" if word != "bored" else "bored"
                if name == "tired" and (TIRED_PERSISTENT.search(clean) or (
                        TIRED_DESPITE_SLEEP.search(clean) and SLEEP_WORD.search(clean))):
                    return None
                if word == "spent" and SPENT_MONEY.search(clean):
                    continue
                if name == "happy" and negated(clean, word):
                    return "sad"
                if negated(clean, word) and not _denies_an_earlier_word(clean, word):
                    denied = True
                    denied_names.add(name)
                    continue
                if nearly(clean, word):
                    continue
                if name == "happy" and NOT_LANDED.search(clean):
                    return "sad"
                if name == "happy" and ack.has_news(clean) and not LEFT_BEHIND.search(clean):
                    return None
                return name
    if denied and not (read and read not in denied_names):
        return "not_feeling"
    return read


LEFT_BEHIND = re.compile(
    r"\b(?:out\s+of|home\s+from|back\s+home\s+from|came\s+home\s+from|come\s+home\s+from|"
    r"discharged\s+from|released\s+from)\s+(?:the\s+)?hospital\b")

GOING_ON = re.compile(
    r"\b(?:all the time|all day every day|every day|every single day|most days|"
    r"most of the time|constantly|non ?stop|day after day|week after week|"
    r"for (?:weeks|months|years)|keep (?:feeling|crying|being)|keeps? feeling|"
    r"always (?:feel|feels|feeling|angry|sad|anxious|worried|down|low|crying|tearful))\b")
GOING_ON_LONG = re.compile(
    r"\b(?:all the time|all day every day|every day|every single day|most days|"
    r"most of the time|constantly|non ?stop|day after day|week after week|"
    r"for (?:weeks|months|years)|always (?:feel|feels|feeling|angry|sad|anxious|worried|"
    r"down|low|crying|tearful))\b")
AT_MYSELF = re.compile(
    r"\b(?:annoyed|angry|cross|furious|frustrated|irritated|fed up|pissed off|mad)\b"
    r"[^.!?]{0,25}?\b(?:with|at)\s+(?:myself|me\b(?!\s*(?:too|as well)))\b|"
    r"\b(?:with|at)\s+myself\b|"
    r"\bmad at me for\b|\bcross with my own\b", re.I)

KICK_MYSELF = re.compile(r"\bi could (?:kick|strangle|shake) myself\b|\bkick myself for\b", re.I)
AT_MYSELF_REPLIES = REPLIES["at_myself"]

A_FACULTY_GETTING_WORSE = re.compile(
    r"\bmy\s+(?:memory|memories|recall|forgetfulness|hearing|sight|eyesight|vision|balance|"
    r"mobility|breathing|joints?|knees?|hips?|back|hands?|skin|teeth|gums|grip)\b"
    r"[^.!?]{0,30}?\b(?:getting|got|is|are|has been|have been)\s+"
    r"(?:so |much |a lot |that )?(?:worse|bad|badly)\b")
OWN_MEMORY_OFF = re.compile(
    r"\bmy\s+(?:memory|memories|recall|forgetfulness)\b[^.!?]{0,30}?"
    r"\b(?:isnt|is not|wasnt|not|no longer|never)\s+(?:what|as|as good|up to|reliable)\b|"
    r"\b(?:im|i am|i'm)\s+(?:getting|becoming|so|very|quite)\s+"
    r"(?:forgetful|scatty|absent[- ]minded|forgetfull)\b|"
    r"\b(?:im|i am|i'm)\s+losing\s+my\s+(?:memory|recall)\b|"
    r"\b(?:i\s+(?:keep|am constantly|constantly|always)\s+forgetting\s+"
    r"(?:everything|things|words|names|where|what))\b|"
    r"\bcant\s+remember\s+(?:things|names|words|where|what|how)\b"
    r"[^.!?]{0,25}?\b(?:used to|any\s?more|anymore|lately|these days|now)\b|"
    r"\b(?:worried|worry|worries|worried sick)\s+about\s+my\s+(?:memory|recall|forgetfulness)\b|"
    r"\bis\s+my\s+(?:memory|recall)\s+(?:ok|okay|normal|going|getting|all right|alright)\b|"
    r"\b(?:scared|worried|frightened|terrified)\s+(?:that\s+)?(?:im|i'm|i am)\s+"
    r"(?:getting|losing)\b|"
    r"\b(?:does|is|do)\s+(?:forgetting|this|that)\s+(?:mean|a sign of)\s+dementia\b|"
    r"\bmy\s+(?:memory|recall)\s+(?:is|has been)\s+(?:terrible|awful|rubbish| shocking|bad)\b")

MOOD_KINDS = frozenset(("sad", "anxious", "annoyed"))
HEAVY_FEELINGS = frozenset(("missing", "sad", "lonely", "lonely_apart", "not_coping", "bad_day",
                            "rough_day", "worry", "worry_person", "guilty", "venting",
                            "not_enough", "own_fault", "not_fair",
                            "feel_like_not_enough", "feel_like_load", "feel_like_left",
                            "feel_like_adrift", "against_me"))


NEWS_MET = re.compile(
    r"\b(?:sorry to hear|i'm sorry|i am sorry|so sorry|really sorry|such sad news|"
    r"a lot to carry|that's rough|that is rough|how awful|that's awful|that's hard|"
    r"that is hard|hardest days?|a real loss|nothing about that is a fault|no wonder)\b", re.I)
NEWS_MODULES = frozenset(("loss", "grief"))


NOT_A_NOD = re.compile(
    r"^(?:it|that|this|there|they|he|she|today|yesterday|last night|"
    r"the (?:day|week|weekend|trip|meal|film|game|match|party|wedding|gig|show|interview))\s+"
    r"(?:was|were|is|are|has been|had been|s been|went|got|ended up|turned out)\b", re.I)


ASKED_HOW_IT_WENT = re.compile(
    r"^(?:was|were)\s+(?:it|that|this|they)\s+"
    r"(?:(?:really|actually|very|too|that|so|pretty)\s+)?"
    r"(?:bad|good|nice|hard|tough|rough|scary|easy|awful|ok|okay|alright|fine|fun|horrible|"
    r"dreadful|painful|tiring|stressful|busy|long|slow|worrying|grim|lovely|great|sunny|warm|cold|wet|windy|hot)"
    r"\s*(?:for\s+(?:you|her|him|them))?\s*[?!.]*$", re.I)


def _asked_how_it_went(line):
    return ASKED_HOW_IT_WENT.match(" ".join(str(line or "").lower().split())) is not None


A_JUDGEMENT_ASKED = re.compile(
    r"^(?:and |so |but |ok |okay |also |sorry |oh |hmm |well )*"
    r"(?:is|are|was|were|will|would|does|do|did|should|shall|can|could)\s+"
    r"(?:that|this|it|these|those|there|they|he|she|we|you)"
    r"(?:\s+(?:all|really|actually|very|too|that|this|so|still|even|just|quite|pretty|any|much|"
    r"a bit|be|being|been|getting|going|gonna|to|about|like|sound|sounds|seem|seems|look|looks|"
    r"feel|feels)){0,4}"
    r"\s*"
    r"(?P<word>all right|too little|too much|too late|a problem|a worry|a big deal|worth it|"
    r"(?:good|well|big|old|fast|strong|warm|long|soon) enough|"
    r"ok|okay|fine|alright|right|correct|good|bad|poorly|safe|dangerous|serious|normal|common|"
    r"wise|sensible|worse|better|enough|much|use|help|helpful|work|do|suit)"
    r"(?:\s+(?:the job|the trick|the business|or not|or no))?"
    r"(?:\s+(?:then|though|honestly|now|yet|here|you|me|us|"
    r"(?:with|for|by|to) (?:you|me|us)))?\s*$",
    re.I)
JUDGEMENT_POOLS = (
    ("enough_no_subject", frozenset(("enough", "too little", "much"))),
    ("too_much_no_subject", frozenset(("too much",))),
    ("help_no_subject", frozenset(("help", "helpful"))),
    ("work_no_subject", frozenset(("work", "do"))),
)
A_SUBJECT_ALREADY_ASKED = frozenset(("normal", "weird", "odd", "wise", "sensible"))


def _a_judgement_asked(line):
    found = A_JUDGEMENT_ASKED.match(" ".join(str(line or "").lower().split()).strip(" .,!?"))
    if not found:
        return ""
    word = found.group("word").lower()
    if word.endswith(" enough"):
        word = "enough"
    if word in A_SUBJECT_ALREADY_ASKED:
        return ""
    flat = " ".join(str(line or "").lower().split())
    if word == "good" and re.search(r"\bany good\b", flat):
        return ""
    if re.search(r"\btoo (?:much|little)\b", flat):
        return "too_much_no_subject"
    if word == "suit" or re.search(
            r"\b(?:with|for|by|to) (?:you|me|us)\b|\bsuits? (?:you|me)\b|\bworks? for you\b",
            flat):
        return "for_you_no_subject"
    for pool, words in JUDGEMENT_POOLS:
        if word in words:
            return pool
    return "judge_no_subject"


def _is_a_nod(line):
    said = str(line).lower().replace("'", "").replace(",", " ")
    words = said.split()
    if NOT_A_NOD.match(said):
        return False
    return len(words) <= 3 and bool(set(words) & fallback.ACKS)


def _the_nod(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return "ack", ""
    recent = [t for t in turns[-3:] if isinstance(t, dict)]
    for index in range(len(recent) - 1, -1, -1):
        turn = recent[index]
        if index < len(recent) - 1 and not _is_a_nod(str(recent[index + 1].get("user") or "")):
            break
        if str(turn.get("module") or "") in NEWS_MODULES:
            return "nod_after_news", str(turn.get("user") or "")
        if NEWS_MET.search(str(turn.get("bot") or "")):
            return "nod_after_news", str(turn.get("user") or "")
        if reads_as_bad_news(str(turn.get("user") or "")):
            return "nod_after_news", str(turn.get("user") or "")
    return "ack", ""
SOMEONE_ELSE = re.compile(
    r"\b(?:my|our|his|her|their)\s+(?:husband|wife|partner|boyfriend|girlfriend|mum|mom|mam|"
    r"mother|dad|father|son|daughter|child|kid|kids|baby|brother|sister|friend|mate|boss|"
    r"colleague|nan|gran|grandad|grandma|aunt|uncle)\b")
FIRST_PERSON = re.compile(r"\b(?:i|im|ive|id|i'm|i've|i'd|feel|feeling|felt)\b")


AN_AGE_SAID = re.compile(
    r"^(?:i'?m|im|i am|ive|i've)\s+(\d{1,3})(?:\s*(?:years?|yrs?)(?:\s+old)?)?"
    r"(?:\s+(?:now|this year))?\s*[.!]?$", re.I)
WORK_IN_THE_THREAD = re.compile(
    r"\b(?:job|jobs|work|worked|working|redundan\w*|sacked|fired|laid off|let go|"
    r"interview\w*|cv|career|employer|employed|unemployed|shift|shifts|boss)\b", re.I)
AGE_IN_A_WORK_THREAD = (
    "{age} is not the problem \u2014 the trap is going for the same jobs as people half your "
    "age. Apply for the ones that ask for someone who has done it before.",
    "Age is a real filter in some places and invisible in others. What gets read is a CV that "
    "says what you ran, how big it was and what it saved, not a list of dates.",
    "The roles worth having at your age are the senior versions of what you were doing, and the "
    "quickest way in is the people who already know your work. Ask them before the job boards.",
    "You have years of doing the job properly, and that is what you are selling. Most people who "
    "land well at your age do it through somebody who has seen them work.",
    "It is a fair thing to worry about and it is survivable: apply upwards rather than sideways, "
    "and lead the CV with what you fixed and what it was worth.",
    "{age} is young for the jobs worth having. What were you doing before? I can tell you how "
    "to pitch it.",
)


A_DOUBT_ABOUT_WORK = re.compile(
    r"\b(?:will|would|does|is)\s+(?:anyone|anybody|any one|someone|somebody)\s+"
    r"(?:take me on|hire me|employ me|have me|want me|give me a job)\b"
    r"|\b(?:who|anyone|anybody|someone|somebody)(?:'s| is)?\s+(?:going to|gonna)\s+"
    r"(?:hire|take on|employ|have)\s+me\b"
    r"|\b(?:any|much) (?:chance|hope) (?:of|for) (?:me )?(?:getting )?(?:work|a job|being hired)\b",
    re.I)
A_TOO_OLD = re.compile(
    r"\bam i too old\b"
    r"|\btoo old\s+(?:to\s+(?:get|find|be)\s+(?:a\s+)?(?:job|work)|for (?:this|it|the job))\b"
    r"|\btoo old (?:at|for) my age\b", re.I)
TAKEN_ON_REPLIES = (
    "Plenty of people will. The ones who do not call are reading a CV that lists jobs \u2014 name "
    "what you fixed and what it was worth, and the calls come.",
    "Some will and some will not, and the ones who do are worth all of your effort. Ask two people "
    "who have worked with you for a name before you send out anything else.",
    "The ones worth having will, and they hire on what you did rather than on how long ago you "
    "started doing it.",
    "Yes \u2014 the work that wants somebody who has done it before is where your age counts for "
    "you, and that is where to aim.",
)
TOO_OLD_REPLIES = (
    "Not for the jobs worth having. The work that wants somebody who has done it before is where "
    "your age counts for you, so aim at that rather than at the same job you had.",
    "No, though a CV that lists dates will make it look that way. Name what you fixed and what it "
    "was worth and the age stops being the first thing read.",
    "Age is a filter in some places and invisible in others, and the way round both is the people "
    "who have worked with you: ask them for a name before you send anything out.",
    "Old for a warehouse shift, young for the jobs that need somebody who can run the thing. What "
    "did you do before? I can tell you how it reads.",
)


def _a_doubt_about_being_taken_on(clean, memory):
    said = str(clean or "")
    found = A_DOUBT_ABOUT_WORK.search(said) or A_TOO_OLD.search(said)
    if not found:
        return None
    if not _in_a_work_thread(memory):
        return None
    pool = TOO_OLD_REPLIES if A_TOO_OLD.search(found.group(0)) else TAKEN_ON_REPLIES
    return pick(pool, memory, clean)


def _in_a_work_thread(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return False
    for turn in turns[::-1][:3]:
        if not isinstance(turn, dict):
            continue
        said = str(turn.get("user") or "")
        if not said or not WORK_IN_THE_THREAD.search(said):
            continue
        if reads_as_bad_news(said) or reads_like_a_symptom(said) or AN_AGE_SAID.match(said.strip()):
            return True
    return False


def _the_age_in_a_work_thread(clean, memory):
    found = AN_AGE_SAID.match(str(clean or "").strip())
    if not found:
        return None
    age = int(found.group(1))
    if age < 18 or age > 99:
        return None
    if _in_a_work_thread(memory):
        return pick(AGE_IN_A_WORK_THREAD, memory, clean).replace("{age}", str(age))
    return None


def _going_on(clean):
    if not (GOING_ON.search(clean) or KEEPS_HOW_I_AM.search(clean)):
        return False
    other = SOMEONE_ELSE.search(clean)
    if not other:
        return True
    mine = FIRST_PERSON.search(clean)
    return bool(mine and mine.start() < other.start())
FEEL_LIKE = re.compile(
    r"\bfeel(?:s|ing)?\s+like\s+(?:i\b|i'm\b|im\b|me\b|my\b|myself\b|we\b|everyone\b|"
    r"everybody\b|nobody\b|no one\b|no-one\b|nothing\b|things\b|life\b|"
    r"a (?:failure|fraud|mess|joke|burden|disappointment|let ?down|useless|rubbish|terrible|"
    r"awful|horrible|bad)\b|"
    r"an? (?:idiot|imposter|impostor|bad (?:mum|mom|dad|mother|father|parent|person|friend))\b|"
    r"the worst (?:mum|mom|dad|mother|father|parent|person|friend|wife|husband|partner|son|"
    r"daughter)\b)")
FEEL_LIKE_WANT = re.compile(
    r"\bfeel(?:s|ing)? like (?:i|we)\s+(?:need|want|could do with|fancy|"
    r"(?:am|'m) going to)\b")
FEEL_LIKE_NOT_HEARD = re.compile(
    r"\bnobody (?:ever )?(?:listens|listened|hears|hearing|understands|understood)\b|"
    r"\bno ?-?one (?:ever )?(?:listens|listened|hears|hearing|understands|understood)\b")
OTHER_FEELS_LIKE = re.compile(
    r"\b(?:my|his|her|their|our)\s+\w+\s+(?:feels?|is feeling)\s+like\b|"
    r"\b(?:he|she|they)\s+(?:feels?|is feeling)\s+like\b")
FEEL_LIKE_NOT_ENOUGH = re.compile(
    r"\bnot (?:doing |being |getting )?(?:good )?enough\b|\bnever (?:good |doing )?enough\b|"
    r"\bdoing (?:everything|it all) (?:wrong|badly)\b|"
    r"\b(?:can'?t|cant|cannot) (?:do|get) (?:anything|it) right\b|"
    r"\bletting (?:everyone|everybody|people|them|her|him|down)\b|"
    r"\blet (?:everyone|everybody|people|them|down) down\b|"
    r"\b(?:(?:such )?a|like a) (?:failure|fraud|mess|joke|burden|disappointment|let ?down)\b|"
    r"\b(?:useless|worthless|hopeless|a rubbish|a bad|a terrible) (?:mum|mom|dad|mother|father|"
    r"parent|person|friend|wife|husband|partner|son|daughter)\b|"
    r"\bnot good at (?:anything|my job|this|being)\b|"
    r"\b(?:rubbish|bad|useless) at (?:my |the )?(?:job|work|everything)\b|"
    r"\bthe worst (?:mum|mom|dad|mother|father|parent|person|friend|wife|husband|partner|"
    r"son|daughter) (?:in the world|ever|alive)\b")
FEEL_LIKE_WORTH = re.compile(
    r"\bnot (?:doing |being |getting )?(?:good )?enough\b|\bnever (?:good |doing )?enough\b|"
    r"\b(?:can'?t|cant|cannot) (?:do|get) (?:anything|it) right\b|"
    r"\b(?:a|an|like a) (?:failure|fraud|mess|joke|burden|disappointment|waste of space)\b|"
    r"\bmy (?:\w+ )?(?:is|was|isnt|isn'?t|wasnt|wasn'?t)?\s*(?:just |never |still |always )?"
    r"(?:not\s+)?(?:good\s+)?enough\b|"
    r"\b(?:im |i'?m |i am )?useless\b|\bbehind (?:everyone|in life|on everything)\b|"
    r"\bfail(?:ed|ing)? at everything\b")
FEEL_LIKE_ROLE = re.compile(
    r"\bfeel(?:s|ing)? like (?:(?:im|i'?m|i am) )?(?:a|an) (?:really |proper |right |useless |"
    r"rubbish |terrible |"
    r"awful |horrible |bad |lousy )*(?:mum|mom|mother|dad|father|parent|person|friend|wife|"
    r"husband|partner|son|daughter|boss|manager)\b|"
    r"\bfeel(?:s|ing)? like (?:(?:im|i'?m|i am) )?the worst (?:mum|mom|mother|dad|father|"
    r"parent|person|friend|wife|"
    r"husband|partner|son|daughter)\b|"
    r"\bfailing (?:as|at being) a (?:mum|mom|mother|dad|father|parent|partner|wife|husband)\b")
FEEL_LIKE_COPE = re.compile(
    r"\b(?:can'?t|cant|cannot) (?:cope|manage)(?: any ?more| at all| with (?:it|this|anything))?\b")
FEEL_LIKE_AT_HOME = re.compile(
    r"\b(?:at|in) (?:my |our |the )?(?:home|house|flat|family)\b|\bmy family\b")
FEEL_LIKE_LOAD = re.compile(
    r"\bonly (?:one|person) (?:who |that )?(?:does|doing|is doing|cleans|cleaning|cooks|"
    r"cooking|remembers|notices|trying|tries|bothers|cares|helps|works)\b|"
    r"\bnobody (?:else )?(?:helps|bothers|does anything|notices|pulls their weight)\b|"
    r"\bno ?-?one (?:else )?(?:helps|bothers|does anything|notices)\b|"
    r"\b(?:carry|carrying|carried) (?:everything|it all|the lot)\b|"
    r"\b(?:have|has|having) to do (?:everything|it all)\b|"
    r"\ball (?:the |of the )?(?:housework|chores|cleaning|cooking|washing|work|tidying)\b")
FEEL_LIKE_HOME_LOAD = re.compile(
    r"\b(?:do|doing|does|did) (?:everything|it all) (?:at home|around the house|in the house|"
    r"in our house|around here)\b")
FEEL_LIKE_GOOD = re.compile(
    r"\b(?:myself|me|my old self|human) again\b|\ba (?:new|different) (?:person|woman|man)\b|"
    r"\bon top of the world\b|\bback to (?:my old self|normal|myself)\b|"
    r"\b(?:finally )?(?:getting|get|going|getting there) (?:somewhere|there)\b|"
    r"\b(?:doing|getting) (?:it|everything) right\b|"
    r"\bmatter(?:ing)? again\b|\b(?:got|getting|back) (?:on top of|a handle on) (?:things|it|"
    r"everything)\b|\bon top of (?:things|everything)\b|"
    r"\b(?:coping|managing|handling it) (?:at last|again|better)\b|"
    r"\bback to (?:my usual self|normal|normality)\b|\bover the (?:worst|hump)\b|"
    r"\b(?:can|could) (?:keep up|cope|manage|handle (?:it|things)) (?:now|again|at last)\b")
ARRIVAL_WORDS = re.compile(
    r"\b(?:how|what|when|where|whether|which|why|who)(?:s|'s)?\b|\b(?:can|could|will|would|"
    r"shall|should|do|does|did|is|are|if|once|before|after|until|till|by|time|early|late|long|"
    r"far|soon|first|way|route|best|easiest|quickest|cheapest|drive|train|bus|taxi|walk)\b")
FEEL_LIKE_MAIN_ANSWERS = re.compile(
    r"\b(?:stuck|in a rut|going nowhere|treading water)\b|"
    r"\b(?:don'?t|dont|do not|doesn'?t|does not|never) belong\b|\bno longer belong\b|"
    r"\b(?:have |got )?no (?:friends|mates)\b")
FEEL_LIKE_OVERLOAD = re.compile(
    r"\b(?:drown(?:ing|ed)?|spread(?:ing)? (?:too )?thin|snowed under|buried in)\b|"
    r"\b(?:can'?t|cant|cannot|struggl\w* to) keep up\b|\bkeeping up with\b|"
    r"\bjuggling (?:too much|everything|it all)\b")
FEEL_LIKE_ADRIFT = re.compile(
    r"\b(?:don'?t|dont|do not|doesn'?t) know (?:what to do|where to (?:start|begin|go)|"
    r"what i (?:want|should)|who i am|where i (?:am|am going|belong))\b|"
    r"\b(?:feel )?(?:lost|stuck|behind|adrift)\b|\bno (?:idea|clue) (?:what|where)\b|"
    r"\bwasting (?:my time|my life)\b")
LIFE_ADRIFT = re.compile(
    r"\b(?:don'?t|dont|do not|still don'?t|still dont) know (?:what to do with my life|"
    r"what i want to do|what i want out of life|where to start with my life)\b|"
    r"\bno idea what to do with my life\b")
IDEATION = re.compile(
    r"\b(?:a burden|burden to|better off without|better off if i|shouldn'?t be here|"
    r"should not be here|not (?:be|been) here any ?more|(?:would|wouldn'?t|will|won'?t|"
    r"might not) notice|in the way|if i (?:was|were) gone|if i (?:wasn'?t|was not|weren'?t) here|"
    r"no point (?:any ?more|in (?:anything|it|going on|carrying on|life))|no reason to (?:live|"
    r"be here|go on|carry on)|ending it|end it all|want to die|wanna die|kill myself|"
    r"hurt myself|harm myself|can(?:'?t| ?not) (?:go on|carry on|keep going)|cannot go on|"
    r"(?:not|never) wake up)\b")

EVENT_DONE = re.compile(
    r"\b(?:failed|failed at|passed|sat|didn'?t get|didnt get|got turned down|was turned down|"
    r"got rejected|was rejected|missed|lost|blew|messed up|did badly)\b[^.]*\b"
    r"(?:test|tests|exam|exams|interview|interviews|audition|presentation|race|match|game|"
    r"course|driving|physical|assessment|trial|shift|application|deadline|review)\b")
FEEL_LIKE_EVERYTHING = re.compile(
    r"\b(?:ruining everything|getting everything wrong|"
    r"messing everything up|nothing i do (?:is|works))\b")
FEEL_LIKE_PHYSICAL = re.compile(
    r"\b(?:be sick|being sick|throw up|throwing up|vomit\w*|pass out|passing out|faint|"
    r"fainting|dizzy|collapse|collapsing)\b|"
    r"\b(?:getting|going|coming down with|feel|feeling) (?:ill|poorly|unwell|a cold|the flu|"
    r"the bug|something)\b")
FEEL_LIKE_ILLNESS = re.compile(
    r"\b(?:dying|die|dead|suffering|rotting)\s+(?:of|from|with|off)\s+"
    r"(?:this\s+|the\s+|a\s+|my\s+|that\s+|these\s+)?"
    r"(?:flu|cold|virus|bug|migraine|headache|infection|cough|temperature|fever|"
    r"sore throat|chest infection|stomach bug|norovirus|sinusitis|bronchitis)\b|"
    r"\b(?:feel|feeling|felt) like (?:im |i am )?(?:dying|dead)\b[^.]*\b(?:flu|cold|virus|bug|"
    r"migraine|infection|cough|fever|temperature)\b")
FEEL_LIKE_LEFT = re.compile(
    r"\b(?:left out|on the outside|the odd one out|invisible|ignored|excluded|unwanted)\b|"
    r"\bnobody (?:likes|wants|invites|invited|talks to|listens|hears|understands|"
    r"sees|notices|takes me)\b|"
    r"\bno ?-?one (?:likes|wants|invites|talks to|listens|hears|understands|sees)\b|"
    r"\bno (?:friends|mates)\b")



FEEL_LIKE_JUDGEMENT = re.compile(
    r"\b(?:nothing|nobody|no ?-?one|never|alone|lonely|by myself)\b|"
    r"\b(?:useless|hopeless|worthless|pointless|stupid|thick|dumb|rubbish|crap)\b|"
    r"\b(?:can'?t|cannot|couldn'?t|unable to|head above water|keeping my head|keeping up)\b|"
    r"\b(?:on top of me|on top of everything|further along|left behind|by now|dying|dead)\b|"
    r"\b(?:an? (?:burden|joke|fraud|imposter|impostor|disappointment|let ?down|liability|"
    r"mess|waste)|a waste of|too much|not good enough|on the edge|at breaking point|"
    r"breaking point|going backwards|failing|falling apart|in pieces|broken|"
    r"losing my mind|going (?:mad|crazy|insane))\b")


def _a_journey_not_progress(clean, match):
    if not re.search(r"\bthere\b", match.group(0)):
        return False
    before = clean[max(0, match.start() - 60):match.start()]
    if re.search(r"\bfeels?\b", before):
        return False
    return bool(ARRIVAL_WORDS.search(before))

GOOD_TAIL_LEADS = frozenset("""finally nearly almost now slowly definitely really properly
at last getting get going coping managing doing matter mattering back over on top of the
it things a an up""".split())

_STATE_OF_THEIRS = re.compile(
    r"\b(?:i'?m|i am|i'?ve|ive|we'?re|we are|we'?ve|weve|were|been|it'?s|its|it is|it was|"
    r"things are|things were|things get|things got|lifes|life is|life was|life gets|"
    r"everything'?s|everything is|everything was|everything gets|nothing is|nothing'?s|"
    r"stuff is|it all is|days are)\s*$")


def _said_about_themselves(before):
    words = re.findall(r"[a-z']+", str(before or "").lower())
    while words and words[-1] in GOOD_TAIL_LEADS:
        words.pop()
    if not words:
        return False
    if re.search(r"\b(?:feel|feels|feeling|felt)\b", " ".join(words[-4:])):
        return True
    if _STATE_OF_THEIRS.search(" ".join(words[-3:])):
        return True
    return bool(re.search(r"\b(?:i'?m|i am|i'?ve|ive|we'?re|we are|were|been)$",
                          " ".join(words[-2:])))


def _feel_like(clean):
    if (FEEL_LIKE_PHYSICAL.search(clean) or FEEL_LIKE_ILLNESS.search(clean)
            or IDEATION.search(clean)):
        return None
    if FEEL_LIKE_WANT.search(clean) or FEEL_LIKE_NOT_HEARD.search(clean):
        return None
    if unseen_reading.reads(clean):
        return None
    if FEEL_LIKE_OVERLOAD.search(clean):
        return None
    if LIFE_ADRIFT.search(clean) or FEEL_LIKE_MAIN_ANSWERS.search(clean):
        return None
    if EVENT_DONE.search(clean):
        return None
    if FEEL_LIKE_HOME_LOAD.search(clean):
        return None
    if FEEL_LIKE_WORTH.search(clean):
        return None
    if FEEL_LIKE_ROLE.search(clean) or FEEL_LIKE_COPE.search(clean):
        return None
    good = FEEL_LIKE_GOOD.search(clean)
    if (good and not _a_journey_not_progress(clean, good)
            and (_said_about_themselves(clean[:good.start()])
                 or (not clean[:good.start()].strip()
                     and good.group(0).startswith("getting")))):
        return "feel_like_good"
    match = FEEL_LIKE.search(clean)
    if not match:
        return None
    if FEEL_LIKE_EVERYTHING.search(clean):
        return "against_me"
    if OTHER_FEELS_LIKE.search(clean):
        return None
    if not re.search(r"\b(?:i|im|i'm|i've|ive|me|my|myself|we|us)\b", clean[:match.end()]):
        return None
    if FEEL_LIKE_NOT_ENOUGH.search(clean):
        if _letting_someone_down(clean):
            return None
        return "feel_like_not_enough"
    if FEEL_LIKE_LOAD.search(clean):
        return "feel_like_load"
    if FEEL_LIKE_LEFT.search(clean):
        if FEEL_LIKE_AT_HOME.search(clean):
            return None
        return "feel_like_left"
    if FEEL_LIKE_ADRIFT.search(clean):
        return "feel_like_adrift"
    if fallback._someone_else_minding(clean, clean.split()):
        return None
    if not FEEL_LIKE_JUDGEMENT.search(clean[match.end():]):
        return None
    return "feel_like"


AGAINST_ME = re.compile(
    r"\b(?:nothing|nothing much) (?:is |ever |seems to )?(?:going|goes|worked|working) right\b|"
    r"\beverything (?:is |was |'s )?(?:going )?wrong\b|"
    r"\b(?:everything|it all) (?:is |was )?(?:falling apart|too much|a mess|on top of me)\b|"
    r"\bnothing (?:helps|works|goes right) (?:any ?more|at the moment|lately|these days)\b")
AGAINST_ME_SELF = re.compile(
    r"\b(?:i|im|i'm|i've|ive|me|my|we|us)\b|\b(?:this week|today|lately|at the moment|right now)\b|"
    r"^(?:(?:and|so|but|and then) )?(?:everything|nothing)\b")


AGAINST_ME_ITS_SCOPE = re.compile(
    r"\b(?:with|at|in|on|about)\s+(?:(?:the|a|an|this|that|these|those|my|our|his|her|their|"
    r"its)\s+)?([a-z']+)")
AGAINST_ME_THE_WEEK = frozenset("""
work life home house moment minute time day week month year today now everything anything all
thing things order place world universe general hand head top least most me him her them us
you it something nothing none everybody everyone
""".split())


JUST_A_CONTINUATION = re.compile(
    r"\b(?:just|still|also|anyway)\s+feel(?:s|ing)?\s+like\b|\b(?:and|so|but|then)\s+(?:i\s+)?"
    r"feel(?:s|ing)?\s+like\b")


def _a_feeling_riding_on_the_thread(clean, memory):
    if not JUST_A_CONTINUATION.search(clean or ""):
        return False
    if not isinstance(memory, dict) or not (memory.get("turns") or []):
        return False
    try:
        from ..memory import topics as remembered
        return bool(remembered.carried_topic(memory, clean))
    except Exception:
        return False


def _against_me(clean):
    if not AGAINST_ME.search(clean):
        return None
    if not AGAINST_ME_SELF.search(clean):
        return None
    for found in AGAINST_ME_ITS_SCOPE.finditer(clean):
        if found.group(1).lower() not in AGAINST_ME_THE_WEEK:
            return None
    return "against_me"


LOW_MOOD = re.compile(r"\b(?:can'?t|cant|struggle to|struggling to) (?:get out of bed|get up in "
                      r"the morning|face the day)\b|\bno energy\b|\bnot been sleeping\b|"
                      r"\b(?:everything|it all) (?:is )?(?:a struggle|too much)\b|"
                      r"\bfeel (?:empty|nothing|flat|low)\b|\bcan'?t be bothered\b|"
                      r"\bmost mornings\b[^.]*\b(?:dread|hard|worse)\b")

MOOD_NIGHTS = (
    "Waking early and finding the mornings this hard often come together. It is worth saying "
    "both to a GP in one go — and tonight, keep the room dark and don't watch the clock.",
    "That early waking sits on top of a low stretch, and the two feed each other. Tell a GP "
    "about both, and for tonight, get up rather than lie there watching the hours.",
)


WORRY_SOMEONE = re.compile(
    r"\b(?:worried|worry|worrying|worries|anxious|scared|frightened|freaking out|"
    r"can'?t stop thinking about)\b[^.?!]*?\b(?:about|over|for)\s+(?:my|our)\s+"
    r"(?P<who>mum|mom|mam|mother|dad|father|son|daughter|child|kid|kids|baby|partner|husband|"
    r"wife|sister|brother|nan|gran|granny|grandma|grandad|grandpa|aunt|uncle|friend|"
    r"cat|dog|puppy|pup|kitten|rabbit|hamster|guinea|pony|horse|parrot|budgie)\b")

CARE = re.compile(r"\btemperature\b|\bfever\b|\bfell\b|\bfallen\b|\bswallowed\b|\bchoking\b|"
                  r"\bbleeding\b|\bcollapsed\b|\bunconscious\b|\bcan'?t breathe\b|"
                  r"\bbreathless\b|\bbroken\b|\bfracture\w*|\bstroke\b")

NIGHT_SAID = re.compile(
    r"\b(?:up all night|up half the night|awake all night|awake half the night|no sleep|"
    r"didn'?t sleep|didnt sleep|couldn'?t sleep|"
    r"couldnt sleep|can'?t sleep|cant sleep|not slept|lay awake|lying awake|kept waking|"
    r"(?:keep|keeps|kept) waking|waking up|woke up at \d)\b")

WORRY_SOMEONE_NIGHT = (
    "A night spent worrying about your {who} is a long one, and it makes the day heavier. Say "
    "the actual worry out loud to someone today — the worst of it shrinks once it is said.",
    "Lying awake over your {who} is a hard loop to be in. Pick the one thing you can settle "
    "today — one call, one question, one visit — and let the rest wait until you have slept.",
    "That kind of waking is not your sleep at fault, it is the worry holding on. Write down the "
    "one thing about your {who} you would ask if you could, and ask it today.",
)

WORRY_PRONOUN = {
    "mum": "her", "mom": "her", "mam": "her", "mother": "her", "daughter": "her",
    "sister": "her", "wife": "her", "nan": "her", "gran": "her", "granny": "her",
    "grandma": "her", "aunt": "her",
    "dad": "him", "father": "him", "son": "him", "brother": "him", "husband": "him",
    "grandad": "him", "grandpa": "him", "uncle": "him",
    "cat": "them", "dog": "them", "puppy": "them", "pup": "them", "kitten": "them",
    "rabbit": "them", "hamster": "them", "guinea": "them", "pony": "them", "horse": "them",
    "parrot": "them", "budgie": "them",
}

WORRY_SOMEONE_DAY = (
    "Worry about your {who} follows you around all day. What's happening with {them}?",
    "That's a lot to carry around. Is it something you can do something about, or the waiting "
    "that's worst?",
    "Hard to put down when it's your {who}. Tell me what's going on.",
    "Your {who} being on your mind is not nothing. What's the worry — something that has "
    "happened, or something you are afraid might?",
)


def _worry_someone(clean, memory=None):
    found = WORRY_SOMEONE.search(clean)
    if not found:
        return None
    if LOSS.search(clean) or _loss_recent(memory) or END_OF_ROPE.search(clean):
        return None
    who = found.group("who")
    if SYMPTOM.search(clean) or CARE.search(clean) or OTHER_AWAKE.search(clean):
        return "pass"
    pool = WORRY_SOMEONE_NIGHT if NIGHT_SAID.search(clean) else WORRY_SOMEONE_DAY
    them = WORRY_PRONOUN.get(who, "them")
    return tuple(reply.format(who=who, them=them) for reply in pool)


def _loss_recent(memory):
    if not isinstance(memory, dict):
        return False
    turns = memory.get("turns") or []
    for turn in turns[-3:]:
        if LOSS.search(str(turn.get("user") or "").lower()):
            return True
    return False


def _low_mood_recent(memory):
    if not isinstance(memory, dict):
        return False
    for turn in (memory.get("turns") or [])[-3:]:
        if LOW_MOOD.search(str(turn.get("user") or "").lower()):
            return True
    return False
MAYBE_SOMEONE = re.compile(
    r"^(?:and |but |so |well |also |see |then |now |oh )*"
    r"(?:she|he|they)\b|\b(?:my|our)\s+(?:mum|mom|mam|mother|dad|father|son|daughter|child|"
    r"kid|baby|partner|husband|wife|sister|brother|nan|nana|gran|granny|grandma|grandad|"
    r"grandpa|aunt|uncle|cousin|friend|flatmate|neighbour|neighbor)\b")
SOMEONE_TROUBLE_ANY = re.compile(
    r"\b(?:keeps?|kept) (?:forgetting|getting|losing|falling|waking|saying|coughing|stopping|"
    r"forgetting|crying|asking|being)\b|"
    r"\b(?:wont|won'?t|cant|can'?t|refuses? to|has stopped|stopped)\b|"
    r"\bnot (?:been\s+)?(?:himself|herself|themselves|coping|eating|drinking|sleeping|"
    r"walking|right)\b|"
    r"\b(?:hasn'?t|hadn'?t|haven'?t)\s+been\s+(?:himself|herself|themselves|coping|eating|"
    r"drinking|sleeping|walking|right)\b|"
    r"\b(?:went|been) downhill\b|\bhas been (?:poorly|unwell|off|poorly)\b")
SERIOUS_DIAGNOSIS = re.compile(
    r"\b(?:diagnosed|diagnosis) (?:with|of|as having)\s+(?:cancer|a (?:brain |lung |bowel |"
    r"breast |bone )?tumou?r|leukaemia|leukemia|lymphoma|motor neurone|parkinsons?|"
    r"a terminal|something serious)\b")
THING_BEFORE_CANNOT = re.compile(
    r"\b(?:it|it's|its|that|that's|thats|this|there|there's|theres|which|the \w+|a \w+|an \w+|any \w+)"
    r"\s+(?:probably |still |just |really |even )?(?:can'?t|cant|cannot|can not|won'?t|wont|will not)\b")


def _a_thing_cannot(clean):
    return SOMEONE_TROUBLE_ANY.search(THING_BEFORE_CANNOT.sub(" ", clean)) is None


SOMEONE_REPLY = {
    "known": (
        "Since there is already a diagnosis, make this change the GP's problem rather than "
        "yours to watch: a step down like that is often something treatable, and an infection "
        "is the usual one they check for first.",
        "Ring the GP about your {who} rather than waiting for the next appointment — a change "
        "that comes on over days rather than months is often something with a fix, and worth "
        "saying today.",
    ),
    "homeward": (
        "That's a relief — home is where most of the getting better happens. How is your {who} in "
        "themselves?",
        "Good news. Keep the first week small: short visits, early nights, and let your {who} set "
        "the pace rather than the other way round.",
        "Home, then — that is the bit that matters. The first days back are the ones to keep "
        "quiet, because everyone tries to do too much in them.",
        "Glad to hear it, and home beats a ward for getting better. Ask what to watch for in your "
        "{who}'s first fortnight, and who to ring if something changes.",
    ),
    "diagnosed": (
        "I'm sorry - a diagnosis like that changes the shape of a week. How is your {who} in "
        "themselves?",
        "Worrying news. What have they said about what happens next, and who is looking after "
        "your {who}'s care?",
        "That is a lot to take in, and it takes time to sink in. Has anyone walked you through "
        "the treatment yet?",
    ),
    "hospital": (
        "Sorry to hear that. How is your {who} doing?",
        "That is a worrying place for your {who} to be. What has the hospital said?",
        "Worrying, and waiting is the worst part of it. How is your {who} in themselves?",
    ),
    "memory": (
        "Losing track of things in a familiar place is worth a word with your {who}'s GP, and "
        "soon: it can be a lot of things and several of them are fixable. A note of when it "
        "started, and anything else that has changed, is what they ask for first.",
        "That is worth mentioning to a GP rather than waiting to see if it settles. Write down "
        "what you have noticed about your {who} and when it started, and take that with you — "
        "and if it gets suddenly worse, that is the same day rather than next week.",
        "Worth a GP appointment with your {who}, and take this line with you: forgetting things "
        "in a place they know well is the kind of change that gets looked at properly, and the "
        "sooner the easier it usually is.",
    ),
    "falls": (
        "A fall is worth getting looked at even when nothing hurts, and a second one is worth a "
        "GP visit: balance, eyesight and medicines are the usual causes and all three can be "
        "helped. Clear the loose rugs and put a lamp within reach of the bed in the meantime.",
        "Falls are rarely just age, and that is the good news: strength, eyesight and medication "
        "are the places to look, and a GP can start on all three. Until then, good light on the "
        "stairs and nothing to trip over on the way to the bathroom.",
    ),
    "care": (
        "Ask the staff what they notice day to day and get it written in the home's notes — they "
        "see more of your {who} than you can, and a GP takes their record seriously. Visit at "
        "different times of day so you see it for yourself too.",
        "A home keeps a daily record, so ask what is in it about your {who}: eating, sleep, and "
        "anything that has changed. That is the account a GP or the manager can act on, and it "
        "costs you one conversation at the desk.",
    ),
    "sleep": (
        "Broken sleep is worth reading rather than enduring: pain, a new tablet, drinking later, "
        "a room that is too warm, worry — one of those is usually behind it, and the fix is "
        "different for each. If it has been weeks, or they are worn out all day, ring the GP: a "
        "blood test rules out the physical ones.",
        "A night that is nothing like their usual is a change worth having looked at, and sooner "
        "if it came on suddenly. Ring the GP this week and say when it started and what is "
        "different about the nights now.",
    ),
    "low": (
        "Going quiet and off things is worth saying out loud to a GP — it is common, it is "
        "treatable, and people often do not mention it themselves. One small thing a week that "
        "gets your {who} out, even a short walk, does more than a big plan.",
        "That kind of withdrawal is worth a GP appointment rather than a wait: low mood in later "
        "life is under-reported and it responds to help. In the meantime, keep the visits going "
        "even when they say no — company is the bit that works.",
    ),
    "ill": (
        "Get your {who} looked at rather than waiting it out, and sooner if it is getting "
        "worse — a change like that in someone you are looking after is worth a proper check.",
        "Worth a GP appointment for your {who} this week rather than next month, and keep a "
        "note of what has changed and when. If it turns sudden, that is the same day.",
    ),
}
SOMEONE_IS_IT_NORMAL = re.compile(
    r"^(?:and |but |so )?(?:is|was|are) (?:that|this|it) (?:normal|ok|okay|fine|serious|"
    r"bad|dangerous|common|a worry)\b|\bshould i (?:be )?worried\b|\bis that a sign\b|"
    r"\bwhen (?:should|do|would) i (?:start to )?worry\b|\bhow worried should i be\b|"
    r"\b(?:is|was|are) (?:that|this|it) (?:(?:just|only|part of|down to|because of) "
    r"(?:getting |being )?(?:old age|her age|his age|their age|age|old)|(?:normal|usual|"
    r"expected) for (?:her|his|their) age)\b|\bjust (?:her|his|their) age\b|"
    r"\bat (?:her|his|their) age\b|\bold age\b")
SOMEONE_AGES_IT = re.compile(
    r"\b(?:is|was|are) (?:that|this|it) (?:(?:just|only|part of|down to|because of) "
    r"(?:getting |being )?(?:old age|her age|his age|their age|age|old)|(?:normal|usual|"
    r"expected) for (?:her|his|their) age)\b|\bjust (?:her|his|their) age\b|"
    r"\bat (?:her|his|their) age\b|\bold age\b")
SOMEONE_MORE = re.compile(
    r"\b(?:another|again|twice|three times|second time|every (?:day|night|week|morning)|"
    r"now he|now she|hes done it|shes done it|same again)\b")
SOMEONE_NEXT_STEP = re.compile(
    r"\bwhat (?:should|can|do) i (?:be )?(?:look(?:ing)? out for|watch(?:ing)? (?:for|out) for|"
    r"expect|do(?: next)?|do now|ask(?: them| him| her| the doctor| the gp| the ward)?|"
    r"say(?: to them)?|bring|take with me)\b|\bshould i (?:go|come|be there) with\b|"
    r"\bwhat happens (?:now|next)\b|\bhow do i (?:help|manage|handle)\b|"
    r"\bis there anything i can do\b")
SOMEONE_NORMAL_ANY = (
    "Some of it is age and some is not, and the difference is what changed and how fast: a "
    "slower, steadier version of the same person is the ordinary kind, and a change over days "
    "or weeks, or a stop in something they always did, is worth a GP appointment. A note of "
    "what you have seen and when is what makes that appointment useful.")
SOMEONE_BRING_SOMEONE = re.compile(
    r"\bwhat (?:should|shall|can|do) i (?:bring|take)\s+(?:(?:for|to)\s+)?(?:him|her|them)\b")
SOMEONE_NORMAL = {
    "memory": "Some forgetting is ordinary with age; getting lost in a room they know well is "
              "the kind that gets looked at, and a GP can tell the difference properly.",
    "falls": "One fall can be bad luck. Two, or one with no obvious cause, is not something to "
             "keep an eye on alone — balance and medication are worth a proper look.",
    "sleep": "Sleep goes in patches — a bad week after a change is common, and so is a night "
             "that is nothing like the usual. Weeks of it, or days that are wrecked by it, is "
             "worth a look rather than patience.",
    "low": "Going quiet for a few weeks after a change is common. Months of it, or losing "
           "interest in everything, deserves an appointment rather than patience.",
    "ill": "A change that comes on over days is the one to act on quickly; over months, it still "
           "wants a check rather than waiting for it to pass.",
    "known": "A step down over days is worth a call the same day; the slow changes are the ones "
             "to raise at the next appointment.",
    "hospital": "However it looks today, ask the ward what they expect next — they would rather "
                "answer a question than have you guess.",
}
SOMEONE_AGAIN = {
    "memory": "Note that one down with the date: the examples are what a GP works from, and a "
              "few of them over a few weeks say far more than one on its own.",
    "falls": "Note where and when it happened, and whether anything was different - a new "
             "tablet, a bad night, a rush to the loo. That pattern is the useful bit.",
    "sleep": "Note the nights down - when they woke, how long for, and what they had to drink or "
             "take before bed. Three nights written down says more than a month remembered.",
    "low": "Note what has changed around the same time - a move, a loss, a new tablet - and say "
           "how many days it has been like that.",
    "ill": "Keep a note of the date and what changed: three of anything in one winter is worth "
           "saying out loud to the GP.",
    "known": "Write it down as it happens, with the date: the ones that pile up are what they "
             "ask about.",
    "hospital": "Ask them, while you are there: what the operation was for, and what normal "
                "looks like afterwards.",
}


SOMEONE_NEXT = {
    "memory": "Go with your {who} and take a written note: what you have noticed, when it "
              "started, and anything that changed around then. The GP will ask for exactly that, "
              "and you will be the one who knows.",
    "falls": "Ask about balance and a medication review in the same appointment, and get the "
             "eyes checked: those three cover most of it. At home, good light on the stairs and "
             "nothing to trip over on the way to the bathroom.",
    "sleep": "Same wake-up time every day, no caffeine after early afternoon, a cool dark room, "
             "and out of bed if they are awake more than twenty minutes. If it is weeks, ask the "
             "GP to check their bloods and what they take.",
    "low": "Go along if your {who} will let you, and say the things they will not. Keep the "
           "visits and the small invitations going — they matter more than advice.",
    "ill": "Take a note of what has changed and when, and ring rather than wait for it to get "
           "worse. Sudden and getting worse is the same day.",
    "known": "Note anything that changed in the last few days — eating, drinking, sleep, a "
             "temperature — and ring the GP with it; those are the questions they ask first.",
    "hospital": "Ask the ward what the plan is and who to ring if something changes at night; "
                "write it down, because it is hard to remember later.",
}


YOUNG = re.compile(
    r"\b(?:is|only|just|nearly|almost) (?:one|two|three|four|five|[1-5])\b|"
    r"\b\d+ (?:months?|years?)\b|\bbaby|toddler|newborn\b")
FEAR = re.compile(
    r"\b(?:worried|worrying|nervous|anxious|scared|afraid|frightened|terrified|dreading)"
    r"\s+(?:about|of|that)\b")
SOMEONE_ASK = (
    "How long has that been going on with your {who}?",
    "What has your {who} said about it — and how long has it been like this?",
    "Has your {who} seen anyone about it, or is that the next thing?",
)


def _checks_the_fact(text, memory):
    try:
        return thread.checking_a_fact(text, memory) is not None
    except Exception:
        return False


def _a_follow_up_about_their_person(clean, memory):
    if not isinstance(memory, dict) or len(clean.split()) > 9:
        return False
    record = about(memory)
    if not record:
        return False
    said = " ".join(str(record.get("said") or "").lower().split())
    if not said or said == clean:
        return False
    try:
        return _about_someone(clean, memory) is not None
    except Exception:
        return False


def TAKES_AS_IT_COMES(text, memory=None):
    if _checks_the_fact(text, memory):
        return True
    if occasionplan.takes_as_it_comes(text, memory):
        return True
    try:
        if repeat.asks_what_that_costs(text, memory):
            return True
    except Exception:
        pass
    clean = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    if _a_follow_up_about_their_person(clean, memory):
        return True
    if _frequency_is_the_turn(clean, memory):
        return True
    if LOSS.search(clean) or _safety_thread(memory):
        return False
    if AT_IT.match(clean):
        return True
    try:
        if limits.reply(text, memory) is not None:
            return True
    except Exception:
        pass
    try:
        if reading_reply.judges_a_figure(text, memory):
            return True
    except Exception:
        pass
    line = _line_as_read(text)
    try:
        named = str(((memory or {}).get("user") or {}).get("bot_name") or "").strip()
        if not (named and facts.BOT_NAME_ASK.search(line)) and _about_bot(
                line, (memory or {}).get("understood") if isinstance(memory, dict) else None,
                memory):
            return True
    except Exception:
        pass
    if _body_is_a_feeling(line):
        return True
    if _a_limit(text, memory):
        return True
    if _their_own_call(line):
        return True
    if amends_to(clean):
        return True
    if _a_repair_is_open(memory) and THEY_ARE_NOT_TALKING.search(clean):
        return True
    if (ASKS_FOR_THE_WORDS.search(clean) and _after_a_repair(memory)
            and _the_deed_before(memory) != SAID_WRONG_DEED):
        return True
    if _said_wrong(clean) or _said_unkindly(clean):
        return not _an_entry_answers_the_deed(clean, memory)
    said = A_ROW.search(clean)
    if (said and A_ROW_CLOSE.search(clean)
            and not ROW_ASK.match(clean) and not clean.rstrip().endswith("?")
            and not _ASKS_AFTER.search(clean[said.end():])
            and len(clean.split()) <= 18):
        return True
    row = memory.get("row") if isinstance(memory, dict) else None
    if not isinstance(row, dict) or not row.get("them") or len(clean.split()) > 14:
        return False
    if _the_base_answers_the_row(clean, memory):
        return False
    how = bool(ROW_HOW.search(clean))
    if how and row.get("handed_over"):
        return False
    if (how and (WANTS_AN_APOLOGY.search(clean) or ASKS_FOR_WORDS.search(clean))
            and _the_base_has_an_answer(clean, copy.deepcopy(memory)) is not None):
        return False
    if not (ROW_ENDING.search(clean) or how
            or (ROW_CONTACT.search(clean) and ROW_CONTACT_ASK.search(clean)
                and _names_the_person(clean, row))):
        return False
    waited = len(memory.get("turns") or []) - int(row.get("turn") or 0)
    return 0 < waited <= 3


ROW_SIZE = (r"(?:(?:really|very|pretty|quite|totally|absolutely|such|kind of|sort of)\s+)?"
            r"(?:(?:massive|big|huge|right|proper|real|serious|silly|stupid|terrible|awful|"
            r"horrible|nasty|bitter|blazing|small|minor|tiny|daft)\s+)?")
A_ROW = re.compile(
    r"\b(?:i|we|me)\b[^.!?]{0,30}\b(?:argued|arguing|argue|rowed|had a row|falling out|"
    r"(?:had|having|got into)\s+(?:an?\s+)?" + ROW_SIZE +
    r"(?:row|argument|fight|falling[- ]out)\b|"
    r"fight|fighting|fought|had an argument|an argument|falling out|"
    r"fell out|snapped at|shouted at|lost my temper|lost it with|not speaking|"
    r"stopped talking|said something (?:i|that i) regret)\b"
    r"|\b(?:me and|i and)\b[^.!?]{0,20}\b(?:fell out|had a row|argued)\b"
    r"|\b(?:he|she|they)(?:s|'s| is| are|re|'re)?\s+(?:not|isn'?t|aren'?t|never)\s+"
    r"(?:speaking|talking)\s+to me\b"
    r"|\bwon'?t talk to me\b")

A_ROW_CLOSE = re.compile(
    r"\b(?:mum|mom|mother|dad|father|sister|brother|wife|husband|partner|boyfriend|"
    r"girlfriend|son|daughter|nan|gran|granny|grandma|grandad|grandpa|friend|mate|"
    r"flatmate|housemate|aunt|uncle|cousin|stepdad|stepmum|parents|family|"
    r"child|children|kid|kids)\b")

ROW_HER = re.compile(r"\b(?:mum|mom|mother|sister|wife|girlfriend|daughter|nan|gran|"
                     r"granny|grandma|aunt|stepmum|she)\b")
ROW_HIM = re.compile(r"\b(?:dad|father|brother|husband|boyfriend|son|grandad|grandpa|"
                     r"uncle|stepdad|he)\b")

ROW_ASK = re.compile(r"^\s*(?:what|whats|how|why|when|where|who|which|should|shall|can|could|"
                     r"do|does|did|is|are|will|would|any)\b"
                     r"|\b(?:what|how) (?:should|shall|can|could|do|does) (?:i|we)\b")

FALLING_OUT = re.compile(r"\b(?:fell out|fallen out|falling out|fall out|not talking"
                         r"|stopped talking|stopped speaking|made up|make up)\b")

ROW_REPLY = (
    "Rows with the people we are closest to land hardest. Say the one thing you actually want "
    "{them} to hear and leave the rest of the case: being right is rarely the part that matters.",
    "That kind of row is rarely about what it started as. If it is still raw, give it a night, "
    "then say your one true thing calmly.",
    "Most fallings-out are two people each sure of their own version. Ask {them} how it sounded "
    "from {their} side of it - it is usually not what you meant.",
    "Being at odds with someone close sits on you all day, so I would not leave it too long. "
    "One honest sentence does more than a long apology.",
    "You do not have to fix it today. Say something true rather than nothing at all, and let the "
    "rest wait until you are both calmer.",
)


def _close_nouns(text):
    return {word[:4] for word in A_ROW_CLOSE.findall(str(text or "").lower())}


def _names_the_person(clean, row=None):
    if re.search(r"\b(?:her|him|them|she|he|they)\b", clean):
        return True
    named = _close_nouns(clean)
    if not named:
        return False
    with_them = _close_nouns((row or {}).get("text") if isinstance(row, dict) else "")
    if not with_them:
        return True
    return named <= with_them


A_ROW_NOT_CLOSE = re.compile(
    r"\b(?:boss|manager|colleague|coworker|co-worker|workmate|landlord|letting agent|"
    r"neighbour|neighbor|plumber|builder|electrician|decorator|doctor|nurse|teacher|tutor|"
    r"lecturer|police|council|driver|shop|company|officer|agent|solicitor|bank|staff|"
    r"gp|dentist|vet|postman|courier|stranger|client|customer)\b")


def _a_row_person(clean):
    if A_ROW_CLOSE.search(clean):
        return True
    return not A_ROW_NOT_CLOSE.search(clean)


def _keep_the_row(clean, memory):
    if not isinstance(memory, dict):
        return None
    if not A_ROW.search(clean) or not _a_row_person(clean):
        return None
    if ROW_ASK.match(clean) or clean.rstrip().endswith("?"):
        return None
    if len(clean.split()) > 18 or LOSS.search(clean) or _safety_thread(memory):
        return None
    memory["row"] = {"them": _row_pronoun(clean), "they": _row_subject(clean),
                     "turn": len(memory.get("turns") or []), "text": clean,
                     "handed_over": bool(FALLING_OUT.search(clean))}
    return memory["row"]


def observe(text, memory):
    try:
        _keep_the_row(str(text or ""), memory)
    except Exception:
        pass


ROW_EVENT_ID = re.compile(
    r"(?:^|-)(?:row|rows|argu\w*|fight\w*|fought|shout\w*|yell\w*|snap\w*|temper|"
    r"sorry|apolog\w*|make-up|making-up)(?:-|$)", re.I)
ROW_FELL_OUT = "fell-out"
WANTS_AN_APOLOGY = re.compile(r"\b(?:sorry|apolog\w*)\b")
ASKS_FOR_WORDS = re.compile(
    r"\bwhat (?:should|do|can|could|would) i say\b|\bhow (?:do|should|can|could) i say\b|"
    r"\bwhat to say\b|\bhow to say\b|\bhow do i word it\b|\bhow do i put it in words\b")


def _the_base_has_an_answer(clean, memory):
    try:
        return lookup.find(understanding(clean, memory))
    except Exception:
        return None


ROW_ABOUT = re.compile(
    r"\b(?:about|over|because of|to do with|around)\s+"
    r"(?:the |a |his |her |their |our |my )?([a-z']+)")
ROW_ABOUT_A_PERSON = frozenset({
    "me", "him", "her", "them", "us", "you", "it", "that", "this", "what", "nothing",
    "anything", "something", "everything", "mum", "mom", "mother", "mam", "dad", "father",
    "son", "daughter", "brother", "sister", "wife", "husband", "partner", "boyfriend",
    "girlfriend", "friend", "mate", "flatmate", "housemate", "colleague", "boss", "neighbour",
})


def _the_row_names_its_subject(clean):
    for hit in ROW_ABOUT.finditer(clean):
        if hit.group(1) not in ROW_ABOUT_A_PERSON:
            return True
    return False


def _the_base_answers_the_row(clean, memory):
    found = _the_base_has_an_answer(clean, memory)
    if found is None:
        return False
    ident = str(getattr(found, "id", "") or "")
    if ROW_EVENT_ID.search(ident) or ROW_FELL_OUT in ident:
        return True
    return _the_row_names_its_subject(clean)


_ASKS_AFTER = re.compile(r"\b(?:should|shall|can|could|what|how|why|when|where|who|which|"
                         r"is|are|do|does|did|will|would|any)\b")


def _a_row(clean, memory=None):
    said = A_ROW.search(clean)
    if not said or not _a_row_person(clean):
        return None
    if ROW_ASK.match(clean) or clean.rstrip().endswith("?"):
        return None
    if _ASKS_AFTER.search(clean[said.end():]):
        return None
    if len(clean.split()) > 18 or LOSS.search(clean) or _safety_thread(memory):
        return None
    them = _row_pronoun(clean)
    _keep_the_row(clean, memory)
    if _the_base_answers_the_row(clean, memory):
        return None
    they = _row_subject(clean)
    return pick(tuple(reply.format(them=them, they=they, their=_their_of(them))
                     for reply in ROW_REPLY), memory, clean)


ROW_CONTACT = re.compile(
    r"\b(?:ring|call|text|message|phone|facetime|go round|pop round|go over|apologise|"
    r"apologize|say sorry|make up|make it up|reach out|get in touch|speak to|talk to|"
    r"leave (?:it|her|him|them)|give (?:her|him|them|it) (?:some )?(?:space|time)|"
    r"wait|sit on it|sleep on it)\b")
ROW_CONTACT_ASK = re.compile(
    r"^\s*(?:should|shall|do you think|would you|is it|could)\b"
    r"|\b(?:should|shall) (?:i|we)\b|\bdo you think (?:i|we)\b|\bis it (?:better|too soon)\b"
    r"|\bor (?:not|wait|leave it)\b")
ROW_NEXT = (
    "Yes, and keep it short: say the one thing you would want {them} to hear, not the case for "
    "why you were right. A message is easier than a call while it is still raw.",
    "I would call rather than text, and let {them} hear your voice. One sentence about you - and "
    "if it goes to voicemail, that is not a no.",
    "Say the thing you would be glad you said in a year, not the thing you have been rehearsing. "
    "And not after a drink, however much easier that feels.",
    "Tonight is fine if you are both calmer than you were. Ring with one thing to say and let the "
    "rest wait: a row does not have to be settled in one call.",
)


ROW_SPACE = re.compile(
    r"\bleave (?:it|her|him|them)\b|\bgive (?:her|him|them|it) (?:some )?(?:space|time)\b"
    r"|\bwait\b|\bsit on it\b|\bsleep on it\b|\bnot (?:tonight|yet)\b")
ROW_SAID_SPACE = re.compile(
    r"\b(?:he|she|they|my (?:mum|mom|mother|dad|father|sister|brother|wife|husband|partner|"
    r"boyfriend|girlfriend|friend|mate|flatmate|housemate))"
    r"(?:'s|s| is|re|'re)?\s+(?:said|says|wants|needs|asked for|asked|thinks|reckons|"
    r"told me)\b[^.!?]{0,30}\b(?:space|time|time to think|a few days|a break|breathing room|room)\b")

ROW_HOW = re.compile(
    r"^\s*how (?:do|can|should|would) (?:i|we)\s+(?:put (?:it|things) right|say sorry|apologi[sz]e"
    r"|make (?:it )?up|fix (?:it|this|things)|sort (?:it|this) out|make (?:things|it) better"
    r"|handle (?:it|this)|bring (?:it|things) up)\b"
    r"|\bwhat (?:do|can|could|should|would) (?:i|we) (?:do|say)\b|\bany (?:advice|ideas)\b")
ROW_HOW_REPLY = (
    "Say the one thing you would want {them} to hear, and name your part in it rather than the "
    "case for it. One sentence does more than a long apology.",
    "Keep it to what you did, not what {they} did: one specific thing, said plainly, then let "
    "{them} answer. A list of everything is a fresh row.",
    "Do it in person or on the phone rather than in writing, and lead with the apology rather "
    "than the reason for it. The reason comes after, if it is wanted at all.",
)
ROW_SPACE_REPLY = (
    "A couple of days does no harm if nobody is stewing on it - say so in one line first, so the "
    "silence is not read as the last word.",
    "Space works better with a time on it: say you will leave it until the weekend, mean it, and "
    "then come back with the one thing you want {them} to hear.",
    "A day or two is usually right. Much longer than that and it stops being space and starts "
    "being a way of not having the conversation.",
)


A_QUIET_AT_ME = re.compile(
    r"\b(?:wont|won't|doesnt|doesn't|never|stopped|not)\s+"
    r"(?:talk|talks|talking|speak|speaks|speaking)\s+to\s+(?:me|us)\b")
A_A_CHILD = re.compile(
    r"\b(?:son|daughter|child|children|kid|kids|boy|girl|eldest|youngest|teen|teens|"
    r"teenager|teenagers)\b")
A_TEN_OR_OVER = re.compile(
    r"\b(?:teen|teens|teenager|teenagers|teenage|teenaged|adolescent|adolescents|1[0-9])\b")
A_WHAT_HAPPENED = re.compile(
    r"\b(?:argued|arguing|argue|rowed|had a row|had an argument|an argument|fight|fighting|"
    r"fought|falling out|fell out|fallen out|snapped at|shouted at|shouting|yelled|lost my "
    r"temper|lost it with|said something (?:i|that i) regret|i apologised|i said sorry|"
    r"i was wrong|my fault)\b")
A_BARE_MOVE_ASK = re.compile(
    r"^\s*(?:so\s+|and\s+|ok\s+|okay\s+)?what (?:do|can|could|should|would) (?:i|we) "
    r"(?:do|say)\b[\s.?!]*$", re.I)


def _a_teen_has_gone_quiet(text):
    said = str(text or "").lower()
    if not A_QUIET_AT_ME.search(said):
        return False
    if A_WHAT_HAPPENED.search(said):
        return False
    return bool(A_A_CHILD.search(said) and A_TEN_OR_OVER.search(said))


def _a_quarrel_since(memory, turn):
    rows = [t for t in (memory or {}).get("turns") or [] if isinstance(t, dict)]
    for row in rows[max(0, int(turn or 0)):]:
        if A_WHAT_HAPPENED.search(str(row.get("user") or "").lower()):
            return True
    return False


def _the_ask_in_the_line(clean):
    said = A_ROW.search(clean)
    if said:
        tail = clean[said.end():].strip()
        if tail and _ASKS_AFTER.search(tail):
            return tail
    return clean


def _a_row_next(clean, memory):
    clean = _the_ask_in_the_line(clean)
    row = memory.get("row") if isinstance(memory, dict) else None
    if not isinstance(row, dict) or not row.get("them"):
        return None
    turn = len(memory.get("turns") or [])
    if turn - int(row.get("turn") or 0) > 3:
        return None
    how = bool(ROW_HOW.search(clean))
    if (A_BARE_MOVE_ASK.match(clean) and _a_teen_has_gone_quiet(row.get("text") or "")
            and not _a_quarrel_since(memory, row.get("turn"))):
        return None
    space_said = bool(ROW_SAID_SPACE.search(clean))
    if _the_base_answers_the_row(clean, memory):
        return None
    if how and row.get("handed_over"):
        return None
    if (how and (WANTS_AN_APOLOGY.search(clean) or ASKS_FOR_WORDS.search(clean))
            and _the_base_has_an_answer(clean, memory) is not None):
        return None
    if not how and not space_said \
            and not (ROW_CONTACT.search(clean) and ROW_CONTACT_ASK.search(clean)):
        return None
    if not how and not space_said and not _names_the_person(clean, row):
        return None
    if len(clean.split()) > 14 or LOSS.search(clean) or _safety_thread(memory):
        return None
    if how:
        pool = ROW_HOW_REPLY
    elif space_said or ROW_SPACE.search(clean):
        pool = ROW_SPACE_REPLY
    else:
        pool = ROW_NEXT
    return pick(tuple(line.format(them=row["them"], they=_they_of(row),
                                  their=_their_of(row["them"])) for line in pool),
                memory, clean)


ROW_ENDING = re.compile(
    r"\b(?:hung up|put the phone down|slammed (?:the door|down the phone|the phone)|walked out|stormed off|"
    r"blocked me|swore at me|shouted at me|went to bed|left the room|said nothing|"
    r"slept (?:on the sofa|in the spare room)|(?:is|isnt|isn'?t|was|wasnt|wasn'?t) (?:not )?"
    r"(?:talking|speaking) to me|hasn'?t spoken to me)\b")
ROW_ENDING_REPLY = (
    "That is the worst bit of it - being shut out leaves you with nothing to do with yourself. "
    "It usually means the night is needed, not that it is finished.",
    "That sounds like it ended at the worst moment. Nothing gets better tonight by chasing it, so "
    "leave {them} be and say your one true thing when it is calmer.",
    "A door, a silence or a walk out is a way of stopping the row, not a verdict on it. Let it "
    "settle, then say the one thing you actually wanted {them} to hear.",
)

ROW_HUNG_UP = re.compile(
    r"\b(?:hung up|put the phone down|slammed (?:the phone|down the phone)|blocked me|"
    r"blocked my number)\b")
ROW_ENDING_REPLY_HUNG_UP = (
    "Hanging up is a way of stopping the row, not a verdict on it. Let it settle, then say the "
    "one thing you actually wanted {them} to hear.",
)


def _a_row_ending(clean, memory):
    clean = _the_ask_in_the_line(clean)
    row = memory.get("row") if isinstance(memory, dict) else None
    if not isinstance(row, dict) or not row.get("them"):
        return None
    turn = len(memory.get("turns") or [])
    if turn - int(row.get("turn") or 0) > 3:
        return None
    if not ROW_ENDING.search(clean) or len(clean.split()) > 14:
        return None
    if LOSS.search(clean) or _safety_thread(memory):
        return None
    pool = ROW_ENDING_REPLY
    if ROW_HUNG_UP.search(clean):
        pool = ROW_ENDING_REPLY + ROW_ENDING_REPLY_HUNG_UP
    return pick(tuple(line.format(them=row["them"], they=_they_of(row),
                                  their=_their_of(row["them"]))
                      for line in pool), memory, clean)


def _row_pronoun(clean):
    if ROW_HER.search(clean):
        return "her"
    if ROW_HIM.search(clean):
        return "him"
    return "them"


def _their_of(them):
    them = str(them or "them").lower()
    return {"her": "her", "him": "his"}.get(them, "their")


def _they_of(row):
    return str((row or {}).get("they") or "they")


def _row_subject(clean):
    if ROW_HER.search(clean):
        return "she"
    if ROW_HIM.search(clean):
        return "he"
    return "they"


def _the_deed_before(memory):
    if not isinstance(memory, dict):
        return None
    told = [turn.get("user") for turn in (memory.get("turns") or [])[-1:] if isinstance(turn, dict)]
    return deed_of(told[0]) if told else None


def _after_a_repair(memory):
    if not isinstance(memory, dict):
        return False
    told = [turn.get("user") for turn in (memory.get("turns") or [])[-1:] if isinstance(turn, dict)]
    said = " ".join(str(told[0] if told else "").lower().split())
    return bool(said) and bool(_said_wrong(said) or _said_unkindly(said) or amends_to(said))


def _a_repair_is_open(memory):
    return repair.a_repair_is_open(memory)


def _about_someone(clean, memory):
    if _safety_thread(memory):
        return None
    if loss_reading.reads_as_loss(clean) or _grieving(memory, clean):
        return None
    if _after_a_repair(memory) and not SOMEONE_TROUBLE_ANY.search(clean):
        return None
    record = about(memory) if isinstance(memory, dict) else None
    read = memory.get("understood") if isinstance(memory, dict) else None
    if not record and SOMEONE_AGES_IT.search(clean):
        above = (read or {}).get("leans_on")
        said = str((above or {}).get("text") if isinstance(above, dict) else above or "")
        kept = trouble(said) if said else None
        if kept in SOMEONE_NORMAL:
            return SOMEONE_NORMAL[kept]
    if record and len(clean.split()) <= 9:
        kept = record.get("trouble")
        asks_normal = SOMEONE_IS_IT_NORMAL.search(clean)
        young_night = kept == "sleep" and not asks_normal \
            and YOUNG.search(str(record.get("said") or ""))
        if kept in SOMEONE_NEXT and (asks_normal or SOMEONE_NEXT_STEP.search(clean)) \
                and not young_night:
            pool = (SOMEONE_NORMAL[kept],) if asks_normal else (SOMEONE_NEXT[kept],)
            who = record.get("who") or "them"
            return pool[0].format(who=who)
        if SOMEONE_AGES_IT.search(clean):
            return SOMEONE_NORMAL_ANY
    mine_now = len((memory or {}).get("turns") or [])
    first_said = record.get("trouble_turn", -1) if record else -1
    if record and first_said < mine_now and len(clean.split()) <= 12:
        kept = record.get("trouble")
        pattern = dict(SOMEONE_TROUBLE).get(kept)
        more = (pattern is not None and pattern.search(clean)) or (
            SOMEONE_MORE.search(clean) and len(clean.split()) <= 8)
        if kept in SOMEONE_AGAIN and more:
            return SOMEONE_AGAIN[kept]
    if (LIMIT.search(clean) or ack.a_limit_on_the_plan(clean)) and _after_a_plan(memory, clean):
        return None
    if _said_wrong(clean) or _said_unkindly(clean):
        return None
    if not MAYBE_SOMEONE.search(clean):
        return None
    if LOSS.search(clean) or END_OF_ROPE.search(clean):
        return None
    who = (record or {}).get("who")
    if not who:
        who = person_named(clean, memory)
    if not who:
        return None
    young = YOUNG.search(clean)
    if FEAR.search(clean):
        return None
    if fallback.a_date_of_ours_forgotten(clean):
        return None
    kind = trouble(clean)
    if kind == "hospital" and SERIOUS_DIAGNOSIS.search(clean):
        return pick(SOMEONE_REPLY["diagnosed"], memory).format(who=who)
    if kind in SOMEONE_REPLY and not (SYMPTOM.search(clean) and kind == "ill") \
            and not (kind in ("low", "sleep") and young):
        return pick(SOMEONE_REPLY[kind], memory).format(who=who)
    if isinstance(read, dict) and read.get("kind") == "question":
        return None
    if SOMEONE_TROUBLE_ANY.search(clean) and not _a_thing_cannot(clean) \
            and not _still_about_me(clean) \
            and not _better_answer_exists(clean, memory):
        return pick(SOMEONE_ASK, memory).format(who=who)
    return None


FIRST_PERSON = re.compile(r"\b(?:i|im|i'm|me|my|mine|us|our|we)\b")

LIMIT = re.compile(r"\bcan'?t\b|\bcant\b|\bisn'?t able\b|\bnot able\b|\bonly manage\b")
PLAN_ASK = re.compile(
    r"\bwhat (?:could|can|should|shall) (?:i|we) do\b|\bwhat would you do\b|"
    r"\bwhere (?:could|can|should) (?:i|we) (?:go|take)\b|\bany ideas\b")


def _after_a_plan(memory, clean):
    turns = [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)]
    mine = " ".join(str(clean).lower().split())
    for turn in reversed(turns):
        said = " ".join(str(turn.get("user") or "").lower().split())
        if not said or said == mine:
            continue
        if PLAN_ASK.search(said):
            return True
        break
    log = (memory or {}).get("facts_log")
    if isinstance(log, list):
        newest = len(turns)
        for entry in reversed(log):
            if not isinstance(entry, dict):
                continue
            if entry.get("key") not in ("plan", "plans"):
                continue
            try:
                when = int(entry.get("turn"))
            except (TypeError, ValueError):
                return False
            return newest - when <= 3
    return False


def _grieving(memory, clean):
    if loss_reading.continues(memory) or badnews.reads_as_sudden_loss(clean):
        return True
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    mine = " ".join(str(clean).lower().split())
    for turn in reversed(turns):
        user = " ".join(str(turn.get("user") or "").lower().split())
        if not user or user == mine:
            continue
        said = str(turn.get("bot") or "")
        if loss_reading.reads_as_loss(user) or badnews.reads_as_sudden_loss(user):
            return True
        return any(said in pool for pool in loss_reading.POOLS + (fallback.SUDDEN_LOSS,))
    return False


def _better_answer_exists(clean, memory):
    try:
        if lookup.find(understanding(clean, memory)) is not None:
            return True
        return fallback.who_settles(clean, memory) is not None
    except Exception:
        return False


def _still_about_me(clean):
    return bool(FIRST_PERSON.search(WHO_SAID.sub(" ", clean)))


def _about_the_person(understood):
    return not (isinstance(understood, dict) and understood.get("state_owner") == "thing")

def _my_night(clean):
    text = re.sub(r"\s+", " ", str(clean or "").lower())
    if not MY_NIGHT.search(text):
        return False
    return not NOT_MY_NIGHT.search(text)


def _stuck(clean, memory=None):
    if not (CANT.search(clean) or CANT_OPENING.match(clean) or ITS_BEEN.search(clean)
            or the_body_is_short_of_sleep(clean)) \
            or STUCK_SAFETY.search(clean):
        return None
    if STUCK_IDIOM.search(clean) or STUCK_REASON.search(clean) or STUCK_SELF.search(clean) \
            or _doing_something_to_a_thing(clean):
        return None
    if STUCK_FIXABLE.search(clean):
        return None
    if STUCK_LOSS.search(clean) or said_loss(memory):
        return None
    if the_body_is_short_of_sleep(clean) and not (CANT.search(clean) or CANT_OPENING.match(clean)
                                                 or ITS_BEEN.search(clean)):
        return "sleep"
    for name, patterns in STUCK:
        if name == "work" and STUCK_OBJECT.search(clean):
            continue
        for pattern in patterns:
            if re.search(pattern, clean):
                return name
    return None
OTHER_PERSON = re.compile(
    r"\b(?:my|our|the)\s+(wife|mum|mom|mother|dad|father|son|daughter|husband|partner|"
    r"boyfriend|girlfriend|brother|sister|friend|mate|flatmate|boss|colleague|nan|granny|gran|"
    r"grandma|grandad|grandpa|aunt|uncle|kid|kids|child|children|baby|parents|family|"
    r"neighbours?|neighbors?)\b")
OTHER_PRONOUN = re.compile(r"^(?:he|she|they)(?:'s|s|'re|re)?\b")
CRY_WOLF = re.compile(r"\bcries?\s+wolf\b|\bcrying\s+wolf\b", re.I)
OTHER_FEELING_VERB = frozenset("""cry cries cried crying weep weeps wept weeping sob sobs
sobbed sobbing blub blubs blubbed""".split())
PLURAL_WORDS = {"kids", "children", "parents", "family", "they", "boys", "girls", "twins",
                "little ones", "grandparents", "neighbours", "neighbors"}
SHE_WORDS = {"wife", "mum", "mom", "mother", "daughter", "sister", "nan", "granny", "gran",
             "grandma", "aunt", "girlfriend", "she"}
HE_WORDS = {"dad", "father", "son", "husband", "brother", "grandad", "grandpa", "uncle",
            "boyfriend", "he"}
OTHER_STOP = re.compile(
    r"\b(?:floppy|limp|unresponsive|breath\w*|blue|fever|temperature|rash|sick|vomit\w*|"
    r"diarr?h\w*|pain|hurt\w*|bleed\w*|collapse\w*|seizure|fit|stroke|hospital|doctor|gp|"
    r"surgery|ambulance|infection|swell\w*|forget\w*|memory|dementia|confus\w*|dizzy|"
    r"faint\w*|chest|blood|pregnan\w*|die[ds]?|death|passed away|"
    r"cancer|chemo\w*|radiotherap\w*|dialysis|diagnos\w*|operation|recover\w*|hospice|"
    r"terminal|palliative|parkinson\w*|tumou?r|transplant|consultant)\b")
OTHER_QUESTION = re.compile(r"\b(?:is|are|was|were|should|shall|can|could|do|does|did|will|"
                            r"would)\s+(?:i|we|you|they|he|she|it|that|this|my|the)\b")
_A_HELP_ASK_AT_END = re.compile(
    r"\b(?:what|how)\s+(?:can|could|should|do)\s+(?:i|we)\s+(?:do|help)\b"
    r"(?:\s+(?:about|for|with)\s+(?:it|this|that|her|him|them|us|me)"
    r"|\s+to\s+help(?:\s+(?:her|him|them|me|us))?(?:\s+out)?"
    r"|\s+(?:her|him|them|me|us)(?:\s+out)?)?\s*[.!?]*$")
OTHER_ADVERB = re.compile(r"\b(?:really|very|so|quite|pretty|totally|completely|always|a bit|"
                          r"a lot|just|still|properly|proper|too|rather|extremely|incredibly|"
                          r"absolutely|constantly|getting|seems|looking|feeling)\b")
OTHER_VERB = re.compile(r"\b(?:is|are|was|were|seems?|feels?|looks?|sounds?|been|gets?|got|"
                        r"being|keeps?|has|have)\b")
A_KIND_OF_THING = re.compile(
    r"\b(?:a|an|the)\s+(?:[a-z][a-z'-]*\s+){0,3}$", re.I)
HOW_MUCH_OF_IT = frozenset("bit little touch lot wee tad mite mood right proper terrible awful "
                           "total complete".split())


def _names_a_kind_of_thing(between, after):
    if after.strip(" .,!?;:").strip():
        return False
    words = [word.strip(".,!?;:").lower() for word in str(between or "").split()]
    words = [word for word in words if word]
    if not words:
        return False
    articles = ("a", "an", "the")
    if words[-1] in articles:
        return True
    articles_at = [index for index, word in enumerate(words) if word in articles]
    if not articles_at:
        return False
    of_the_kind = words[articles_at[-1] + 1:]
    if any(word in HOW_MUCH_OF_IT for word in of_the_kind):
        return False
    return bool(of_the_kind)
OTHER_NEG = re.compile(r"\b(?:not|never|no|hardly|barely)\b|\b\w+n't\b|\b(?:isnt|arent|wasnt|"
                       r"werent|dont|doesnt|didnt|cant|couldnt|wouldnt|shouldnt|hasnt|havent|"
                       r"aint)\b")

GENERIC_OTHER_REPLIES = (
    "That's a lot for {obj} to be carrying. What's been happening?",
    "Sounds like {subj} has something heavy on {poss} mind. Is {subj} talking about it?",
)
OTHER_REPLIES = {
    "unappreciated": (
        "That is a slow one to watch. Is there one job {subj} could hand over this week?",
        "Being taken for granted wears anybody down. What would {subj} want noticed first?",
    ),
    "tired": (
        "Tired like that is hard to watch. Is there any chance for {obj} to rest?",
        "That's a lot of tired {target}. Worth taking something off {poss} {plate} this week.",
        "That deep tiredness usually has a cause. Worth getting it looked at if it does not lift.",
    ),
    "stressed": (
        "That sounds like a lot on {poss} {plate}. Is there anything you can lift for {obj}?",
        "Stress that runs on needs something to change, not just a rest. What's driving it?",
    ),
    "relieved": (
        "That's a weight off {poss} mind. Did {subj} say what it was about?",
        "Relief like that usually follows something heavy. {Subj_has} {subj} had a rough time of it?",
        "Good - that sounds like it had been sitting on {obj} a while. What changed?",
    ),
    "anxious": (
        "That sounds rough for {obj}. Do you know what's behind it?",
        "Worry that runs on is tiring in itself. A walk together usually helps more than advice.",
    ),
    "sad": (
        "Low patches are hard to watch. Do you know what's behind it?",
        "That's a lot for {obj} to carry. Small things done together often help more than words.",
    ),
    "lonely": (
        "Loneliness is hard to watch. Is there someone nearby who could keep {obj} company?",
        "That's rough on {obj}. A visit or a phone call this week would probably mean a lot.",
    ),
    "bored": (
        "Boredom is easier to fix than most. What used to keep {obj} busy?",
        "Worth trying something new together — a walk, a class, anything with a fixed time.",
    ),
    "annoyed": (
        "That would wind anyone up. Is there anything you can do about it?",
        "Fair enough for {obj} to be cross. What happened?",
    ),
    "happy": (
        "Lovely to hear. What's made {obj} so happy?",
        "Good — that's worth celebrating.",
    ),
}

ABOUT_REPLIES = {
    "anxious": (
        "Nerves with a real cause in front of them are easier to talk about. What {subj_does} "
        "{subj} say the worst of it is?",
        "That's a big thing for {obj} to have in {poss} head all day. {Subj_is} {subj} talking about "
        "it?",
    ),
    "relieved": (
        "Something real came off {poss} shoulders there. What {subj_does} {subj} say about it?",
        "That's a real weight to lose. {Subj_is} {subj} talking about what {subj} went through?",
    ),
    "stressed": (
        "That's a real weight to have on {poss} {plate}. What part of it is the worst?",
        "Stress with a cause in front of it is worth naming. What {subj_does} {subj} say about "
        "it?",
    ),
    "sad": (
        "Sad about something that really happened needs room rather than fixing. {Subj_is} {subj} "
        "talking about it?",
        "That's a real thing for {obj} to be sad about. What {subj_does} {subj} say about it?",
    ),
    "annoyed": (
        "That would wind anyone up. What's the worst part of it for {obj}?",
        "Fair enough for {obj} to be cross about it. {Subj_has} {subj} said anything to them?",
    ),
    "guilty": (
        "Feeling bad about something real is not the same as being to blame. What {subj_does} "
        "{subj} say about it?",
        "That's a heavy thing for {obj} to be carrying. {Subj_is} {subj} talking about it?",
    ),
    "happy": (
        "Lovely that {subj} {subj_is} pleased about it. What happened?",
        "Good news with a reason behind it — worth hearing the whole thing.",
    ),
}
FEDUP_LEAD = {
    "fed up": "Being fed up with",
    "tired of": "Being tired of",
    "sick of": "Being sick of",
    "sick and tired of": "Being sick and tired of",
    "fed up with": "Being fed up with",
    "fed up of": "Being fed up of",
    "done with": "Being done with",
    "had enough of": "Having had enough of",
    "had it with": "Having had it with",
    "browned off": "Being browned off with",
    "browned off with": "Being browned off with",
    "browned off of": "Being browned off of",
    "peeved": "Being peeved about",
    "peeved with": "Being peeved with",
    "peeved about": "Being peeved about",
    "peeved at": "Being peeved at",
}
FEDUP_REPLIES = (
    "{lead} {thing} is its own kind of tired. What's the worst part of it for {obj}?",
    "{lead} {thing} wears {obj} down more than a late night does. What would have to change?",
    "What is it about {thing} that has worn {obj} out?",
)
FEDUP_GERUND_SAFE = ("What is it about {thing} that has worn {obj} out?",)
FED_UP_WHOLE_OF_IT = re.compile(
    r"\b(?:with|of)\s+(?:(?:my|your|our|his|her|their)\s+)?"
    r"(?:life|living|alive|being alive|existing|trying|everything|anything|it all|the lot|"
    r"the world|feeling|feel|how i feel)\b")


def _recent_plural(memory):
    turns = (memory or {}).get("turns")
    if not isinstance(turns, list):
        return False
    said = " ".join(str(turn.get("user", "")).lower() for turn in turns[-3:]
                    if isinstance(turn, dict))
    if not said:
        return False
    if any(word in said.split() for word in PLURAL_WORDS):
        return True
    return bool(JOINED_PERSON.search(said))


def _pronouns(word):
    word = word.lower()
    if word in PLURAL_WORDS:
        return "them", "their", True
    if word in SHE_WORDS:
        return "her", "her", False
    if word in HE_WORDS:
        return "him", "his", False
    return "them", "their", True


OTHER_BAD_NIGHT = re.compile(
    r"\b(?:slept (?:badly|terribly|awfully|rotten|horribly|awful|terrible|rubbish|lousy|poorly)|"
    r"(?:hardly|barely|didn'?t|didnt|couldn'?t|no) (?:any )?(?:slept|sleep)|"
    r"up all night|awake all night|"
    r"(?:bad|terrible|awful|rubbish|rotten|rough|poor|lousy|restless|broken|sleepless) nights?|"
    r"nights sleep)\b")


def _other_feeling(clean, memory=None):
    body = re.sub(r"\b(?:sick of|tired of|fed up with|fed up of|done with|had enough of|"
                  r"had it with)\s+[^.!?]*$", "", clean)
    asked = _A_HELP_ASK_AT_END.sub("", clean).strip()
    if clean.endswith("?") and asked == clean:
        return None
    if OTHER_STOP.search(body) or OTHER_QUESTION.search(asked):
        return None
    if CRY_WOLF.search(clean):
        return None
    be_verb = False
    match = OTHER_PERSON.search(clean)
    if match:
        word, start = match.group(1), match.end()
    else:
        match = OTHER_PRONOUN.match(clean)
        if not match:
            return None
        pronoun = match.group(0)
        word, start = pronoun.split("'")[0].rstrip("s"), match.end()
        if word.lower() in ("they", "them", "their", "we", "us", "you"):
            if not _recent_plural(memory):
                return None
        be_verb = re.search(r"(?:'s|'re|s|re)$", pronoun) is not None and len(pronoun) > 2
    rest = clean[start:]
    if re.search(r"\b(?:with|at|about|of|by)\s+(?:me|us)\b", rest):
        return None
    if word.lower() not in SHE_WORDS and word.lower() not in HE_WORDS:
        if re.search(r"\b(she|her|hers)\b", rest):
            word = "she"
        elif re.search(r"\b(he|him|his)\b", rest):
            word = "he"
    fed = re.search(r"\b(?:sick of|done with|had enough of|had it with)\b\s*(.*)$", rest)
    if fed:
        thing = _the_thing(fed.group(1))
        pronouns = _pronouns(word)
        if thing and _thing_that_stays(thing):
            return "fedup", *pronouns, thing
        return "annoyed", *pronouns
    if OTHER_BAD_NIGHT.search(rest):
        return ("tired",) + _pronouns(word)
    for name, words in FEELINGS:
        for feeling in words:
            hit = re.search(r"\b" + re.escape(feeling) + r"\b", rest)
            if not hit:
                continue
            between = rest[:hit.start()]
            if _names_a_kind_of_thing(between, rest[hit.start() + len(feeling):]):
                continue
            glue = OTHER_ADVERB.sub("", between).strip()
            their_verb = not glue and not be_verb and feeling in OTHER_FEELING_VERB
            if not (their_verb or OTHER_VERB.search(between) or (be_verb and not glue)):
                continue
            if not their_verb and not cue_about_person(clean, feeling):
                continue
            if feeling in WEARS_OTHER_PEOPLE_OUT:
                continue
            if re.search(r"\b(?:i'm|im|i am|i feel|i've|i have|me|my)\b", between):
                return None
            if OTHER_NEG.search(between):
                continue
            after = rest[hit.start():]
            if re.match(r"\b" + re.escape(feeling) +
                        r"\s+with\s+(?:me|us|him|her|them)\b", after):
                return None
            caused = re.match(r"\b" + re.escape(feeling) + r"\s+(?:of|about|with)\s+(.+)$", after)
            if caused:
                thing = _the_thing(caused.group(1))
                if feeling in ("tired", "bored", "sick", "worn out", "done in", "fed up",
                               "browned off", "peeved"):
                    pronouns = _pronouns(word)
                    if thing and _thing_that_stays(thing):
                        return "fedup", *pronouns, thing
                    return ("bored" if feeling == "bored" else "annoyed"), *pronouns
                if name in ABOUT_REPLIES:
                    return name + "_about", *_pronouns(word), thing
                continue
            if feeling == "low" and re.search(r"\blow\s+(?:on|in)\b", after):
                continue
            if feeling == "spent" and re.search(r"\bspent\s+(?:up|all|it|my|the|every)\b", after):
                continue
            joined = clean[:start + hit.start()]
            if JOINED_PERSON.search(joined):
                return name, "them", "their", True
            return name, *_pronouns(word)
    if ROUGH_DAY.search(rest) and not re.search(r"\b(?:i'm|im|i am|i feel|i've|i had)\b", rest):
        return "tired", *_pronouns(word)
    return None


def _the_thing(phrase):
    phrase = " ".join(str(phrase or "").split()).strip(" .,!?;:")
    phrase = re.split(r"\b(?:because|but|so|and|since|when|after|before|which|that)\b",
                      phrase)[0].strip()
    words = phrase.split()
    if not words or len(words) > 5:
        return ""
    return phrase


JOINED_PERSON = re.compile(
    r"\band\s+(?:(?:his|her|their|my|our)\s+)?(?:wife|husband|partner|brother|sister|son|"
    r"daughter|mum|mom|mother|dad|father|kids?|children|parents?|family|friend|mate|boyfriend|"
    r"girlfriend)\b")

THING_THAT_STAYS = re.compile(r"^(?:my|his|her|their|our|the|this|that|these|those)\b")


def _thing_that_stays(thing):
    return bool(THING_THAT_STAYS.match(thing or ""))


FED_UP_THING = re.compile(
    r"\b(?:done with|fed up with|fed up of|browned off with|browned off of|browned off|"
    r"peeved with|peeved about|peeved at|sick of|sick and tired of|tired of|had enough of|"
    r"had it with)\s+([^,.;!?]*)")
FED_UP_STOPS = re.compile(
    r"\b(?:and|but|so|because|cos|coz|cause|when|whenever|if|while|then|though|tho)\b"
    r"|\b(?:what|why|how|who|which|whether)\b"
    r"|\b(?:i|im|i'm|ive|i've|he|she|they|we|hes|shes|theyll|were)\b")
FED_UP_BARE = re.compile(r"^(?:being\s+)?[a-z][a-z'-]*(?:\s+[a-z][a-z'-]*){0,2}$")
FED_UP_THIN = frozenset("""how what why when where way the a an that this these those to of
    in on at for with about""".split())
NOT_A_THING = frozenset("""it this that them him her everything anything all life nothing
    everyone someone everything you u ya yuo us""".split())
NOT_A_THING_FIRST = frozenset("""it them him her you u ya yuo us me everything anything nothing
    all life everyone someone""".split())

FEELING_WORD = frozenset(
    word for words in EMOTION_WORDS.values() for word in words) | frozenset(
        """feel feels feeling felt think thought know mean means
        sure understand follow get see sense""".split())
NOTHING_NAMED = (BARE_FILLER | NOT_A_THING | FEELING_WORD | frozenset("""
    whole thing things stuff lot bit way ways part parts point now honest lol lmao yes no ok
    okay right yeah all both either neither more less much many some any none
""".split()))


def _confusion_names_a_thing(understood):
    if not isinstance(understood, dict):
        return False
    named = understood.get("keywords")
    if not isinstance(named, list):
        named = understood.get("words") or []
    for word in named:
        if not isinstance(word, str):
            continue
        word = word.strip(".,!?;:'\"()").lower()
        if word and word not in NOTHING_NAMED and word not in CONFUSION_IDIOM_WORDS:
            return True
    return False


CONFUSION_IDIOM_WORDS = frozenset("""cant cannot can not get got make my head round around
    straight nor tail of this that it understand follow struggling to""".split())


SECOND_PERSON = {"my": "your", "our": "your", "me": "you", "us": "you", "mine": "yours",
                 "ours": "yours"}
SECOND_PERSON_RE = re.compile(r"\b(my|our|me|us|mine|ours)\b")
FED_UP_DENIED = re.compile(
    r"\b(?:not|never|n't|no longer|no way)\b(?:\s+\w+){0,2}\s+"
    r"(?:fed up|browned off|peeved|sick of|tired of|had enough|had it with|done with)\b"
    r"|\b(?:never said|didnt say|didn't say|never claimed|dont remember saying|"
    r"don't remember saying)\b[^,.;!?]*\b(?:fed up|browned off|peeved|sick of|tired of)\b")
FED_UP_ABOUT_THE_BOT = re.compile(
    r"\b(?:do|does|did|are|were|would|will|can|could|have|has|ever|dont|don't|doesnt|doesn't)\b"
    r"[^.?!]*\b(?:you|u|ya)\b")
FED_UP_WITH_A_PERSON = re.compile(
    r"\b(?:fed up|browned off|peeved|sick of|tired of|done with|had enough of|had it with)\s+"
    r"with\s+(?:me|us|him|her|them)\b")
FED_UP_FILLER = frozenset("""tbh tho though like honestly lol haha innit tbf ngl atm really just
    now today rn 2bh imo""".split())


FEDUP_SAID_PHRASE = re.compile(
    r"(fed up with|fed up of|fed up|browned off with|browned off of|browned off|peeved with|"
    r"peeved about|peeved at|peeved|sick and tired of|sick of|tired of|done with|had enough of|"
    r"had it with)")


def _fedup_phrase(said, at):
    hit = FEDUP_SAID_PHRASE.match(str(said or "")[at:])
    return hit.group(1) if hit else "tired of"


def _fed_up_with(clean):
    hit = FED_UP_THING.search(" ".join(str(clean or "").split()))
    if not hit:
        return ""
    tail = FED_UP_STOPS.split(hit.group(1))[0].strip(" .")
    if not tail:
        return ""
    parts = tail.split()
    while parts and parts[0] in FED_UP_FILLER:
        parts.pop(0)
    while parts and parts[-1] in FED_UP_FILLER:
        parts.pop()
    tail = " ".join(parts)
    if not tail:
        return ""
    owner = re.match(r"^(?:my|our)\b(.*)$", tail)
    if not owner and not FED_UP_BARE.match(tail):
        return ""
    first = tail.split()[0]
    if tail in NOT_A_THING or first in NOT_A_THING_FIRST:
        return ""
    if all(word in FED_UP_THIN for word in tail.split()):
        return ""
    if owner:
        tail = "your" + owner.group(1)
    return SECOND_PERSON_RE.sub(lambda hit: SECOND_PERSON[hit.group(1)], tail)


OTHER_REPLIES_SMALL_CHILD = (
    "A little one that upset is hard on everyone. What happens just before it starts?",
    "That is a lot for a small child. Is it worse at a particular time of day?",
    "Young children feel things hard and have no other way to say it yet. Does anything set it off?",
)


def _the_small_child(memory):
    if not isinstance(memory, dict):
        return None
    others = [entry for entry in (memory.get("others") or []) if isinstance(entry, dict)]
    if len(others) != 1:
        return None
    age = others[0].get("age")
    if isinstance(age, int) and 0 < age < 9:
        return age
    return None


def _someone_reply(memory, feeling, obj, poss, plural, thing="", said=""):
    values = {"obj": obj, "poss": poss, "plate": "plates" if plural else "plate",
              "target": "to carry" if plural else "for one person to be carrying",
              "thing": thing, "subj": {"her": "she", "him": "he"}.get(obj, "they")}
    values["subj_is"] = "is" if values["subj"] != "they" else "are"
    values["Subj_is"] = "Is" if values["subj"] != "they" else "Are"
    values["subj_does"] = "does" if values["subj"] != "they" else "do"
    values["Subj_has"] = "Has" if values["subj"] != "they" else "Have"
    if feeling == "sad" and _the_small_child(memory):
        return pick(list(OTHER_REPLIES_SMALL_CHILD), memory, said)
    if feeling == "fedup":
        fed = re.search(r"\b(fed up with|fed up of|fed up|sick and tired of|sick of|tired of|"
                        r"done with|had enough of|had it with)\b", said or "")
        values["lead"] = FEDUP_LEAD.get(fed.group(1) if fed else "fed up", "Being fed up with")
        if (thing or "").startswith(("being ", "having ")):
            options = list(FEDUP_GERUND_SAFE)
        else:
            options = list(FEDUP_REPLIES)
        options = [option.format(**values) for option in options]
    elif feeling.endswith("_about"):
        options = [option.format(**values) for option in
                   ABOUT_REPLIES.get(feeling[:-6]) or GENERIC_OTHER_REPLIES]
    else:
        options = [option.format(**values) for option in
                   OTHER_REPLIES.get(feeling) or GENERIC_OTHER_REPLIES]
    return pick(options, memory).replace("  ", " ")


def _last_was_joke(memory):
    turns = memory.get("turns") or []
    if not turns or turns[-1].get("module") != "chat":
        return False
    return turns[-1].get("bot") in set(JOKES.values()) | set(SHORT_JOKES)


def _drop_tail(phrase):
    phrase = " ".join((phrase or "").split())
    changed = True
    while phrase and changed:
        changed = False
        for tail in PLACE_TAIL:
            shorter = tail.sub("", phrase).strip(" ,.;:-'")
            if shorter != phrase:
                phrase, changed = shorter, True
    return re.sub(r"\s+(?:in|to|at|near|from|of|on)\s*$", "", phrase)


def _place_of(phrase):
    phrase = _drop_tail(phrase)
    if PLACE_TIME_OPENS.match(phrase.strip(" ,.;:-'")):
        return ""
    phrase = facts.take_back_cut(phrase).strip(" ,.;:-'")
    if PLACE_THING_OPENS.match(phrase):
        inner = PLACE_LAST.match(phrase)
        if inner:
            phrase = _drop_tail(inner.group(1))
    else:
        phrase = PLACE_TIME.sub("", phrase).strip(" ,.;:-'")
    if phrase.strip(" ,.;:-'").lower() in ("in", "on", "at", "to"):
        return ""
    if PLACE_NOBODY.match(phrase):
        return ""
    if not phrase or any(char.isdigit() for char in phrase):
        return ""
    if len(phrase.split()) > PLACE_MOST:
        return ""
    if phrase.split()[0].lower() in PLACE_IDIOM or phrase.lower() in PLACE_IDIOM:
        return ""
    if phrase.lower() in PLACE_POINTS:
        return ""
    return phrase


COUNTRY_CAPS = {"uk": "UK", "us": "US", "usa": "USA", "uae": "UAE", "eu": "EU", "nz": "NZ"}
ARTICLE_PLACES = {"uk", "us", "usa", "uae", "netherlands", "philippines", "united states",
                  "united kingdom", "bahamas",
                  "gambia", "maldives", "seychelles", "czech republic", "midlands",
                  "isle of wight", "isle of man", "highlands", "cotswolds"}


def _tidy(phrase):
    words = phrase.split()
    if words and words[0].lower() in COUNTRY_CAPS:
        return COUNTRY_CAPS[words[0].lower()] + phrase[len(words[0]):]
    if words and words[0].lower() == "the":
        rest = " ".join(words[1:])
        if rest.lower() in ARTICLE_PLACES:
            return "The " + _tidy(rest)
        return "The" + (" " + rest if rest else "")
    if words and words[0] in {"a", "an", "my", "our", "this"}:
        return words[0][:1].upper() + words[0][1:] + (" " + " ".join(words[1:]) if len(words) > 1 else "")
    small = {"in", "of", "the", "and", "at", "on", "by", "near", "upon", "under", "next", "to"}
    return " ".join(w if w in small else w[:1].upper() + w[1:] for w in words)


def _numbers(values):
    words = [facts.KID_NUMBER_WORDS.get(int(value), str(value)) for value in values]
    if len(words) <= 1:
        return "".join(words)
    return ", ".join(words[:-1]) + " and " + words[-1]


def _place_values(named):
    words = named.split()
    if words and words[0][:1].isupper() and words[0].lower() in {"the", "a", "an"}:
        inside = words[0].lower() + (" " + " ".join(words[1:]) if words[1:] else "")
    else:
        inside = named
    return {"X": named, "x": inside}


def _say(kind, memory, **values):
    if not _mid_chat(memory):
        opening = FIRST_LINE_POOL.get(kind)
        if opening:
            return _reply(opening, memory)
        fresh = [o for o in NEWS_REPLIES[kind]
                 if not onscreen.talks_about_the_conversation(o)]
        if fresh and len(fresh) < len(NEWS_REPLIES[kind]):
            return pick([o.format(**values) for o in fresh], memory)
    if kind in CHEER_KINDS and _a_death_just_said(memory):
        return pick(list(CHEER_IN_LOSS), memory)
    options = [option.format(**values) for option in NEWS_REPLIES[kind]]
    if kind == "good_news":
        _note_the_pool(memory, kind)
    return pick(options, memory)


def _cheer_or_the_question(flat, memory):
    years_back = reply_for_a_win_from_a_past_year(flat)
    if years_back:
        _note_the_pool(memory, "good_news_gone_by")
        return years_back
    return _say("good_news", memory)


def _note_the_pool(memory, kind):
    if not isinstance(memory, dict):
        return
    turns = memory.get("turns")
    memory["said_kind"] = {"kind": kind, "turn": len(turns) if isinstance(turns, list) else 0}


def _just_named(memory, name):
    if not name:
        return None
    pets = [pet for pet in (user(memory).get("pets") or []) if isinstance(pet, dict)]
    named = [pet for pet in pets if str(pet.get("name") or "").lower() == name.lower()]
    return named[-1] if named else None


def _name_said(name):
    name = (name or "").strip()
    if name and not any(char.isupper() for char in name):
        name = " ".join(word[:1].upper() + word[1:] for word in name.split())
    return name


def _pet_name(flat, match):
    rest = flat[match.end():]
    stop = len(rest)
    for other in PET_ANY.finditer(rest):
        stop = min(stop, other.start())
    found = re.search(r"\b(?:called|named)\s+(?:([a-z][a-z'-]+)\s+)?([a-z][a-z'-]+)",
                      rest[:stop])
    if found and found.group(1) and found.group(1).lower() in facts.NOT_A_PRONOUN_NAME:
        return found.group(2)
    titled = facts.PET_NAME.search(rest[:stop])
    if titled:
        return facts._with_title(titled)
    if found:
        return found.group(2)
    return facts.pet_appositive(flat, match.start()) or ""


def _question_coming(understood):
    if not isinstance(understood, dict):
        return False
    return "question_coming" in (understood.get("asks") or ())


NOT_A_SUBJECT = frozenset({"small-talk"})
A_FEELING_SAID = frozenset({"feelings"})


def _the_not_knowing_has_a_subject(memory):
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if not isinstance(understood, dict):
        return False
    topic = understood.get("topic")
    if understood.get("topic_own") in A_FEELING_SAID:
        return False
    return bool(topic) and topic not in NOT_A_SUBJECT


def _conversation(clean, tokens, memory):
    if len(tokens) > 8:
        return None
    flat = clean.replace("'", "").strip(" .,!;:")
    if _safety_thread(memory):
        return None
    if STUCK_ON_A_FORM.match(flat):
        return _say("on_a_form", memory)
    if STUCK_ON_A_THING.match(flat):
        return _say("on_the_thing", memory)
    if STUCK_FEELING.match(flat):
        return _say("a_stuck_feeling", memory)
    if AT_IT.match(flat):
        return _say("at_it", memory)
    if _HOW_LONG_AT_IT.match(flat) and _asked_about_the_effort(memory):
        return _say("the_long_haul", memory)
    if LOST_ONLY.match(flat) and not _the_not_knowing_has_a_subject(memory) \
            and not stuck_line._the_answer_gave_a_step(memory):
        return _say("lost", memory)
    if PRESENCE.search(flat):
        from ..memory import tried as not_moved
        if not not_moved.still_going_on(clean, memory):
            return _say("presence", memory)
    if PAUSE.search(flat):
        return _say("pause", memory)
    if RETURNED.search(flat) and not AWAY_WORDS.search(flat) \
            and _a_thread_to_come_back_to(memory):
        return _say("returned", memory)
    if BID.search(flat):
        return _say("bid", memory)
    if HOME_AGAIN.search(flat) and not AWAY_WORDS.search(flat):
        return _say("home_again", memory)
    if LEAVING.search(flat):
        if re.search(r"\b(?:bed|sleep|sleeping|kip|nap)\b", flat):
            return _say("leaving_bed", memory)
        return _say("leaving", memory)
    if UNDERWAY.search(flat):
        return _say("underway", memory)
    if IN_BED.search(flat):
        return _say("in_bed", memory)
    awake = AWAKE_SINCE.search(flat)
    if awake:
        return _say("awake", memory, when=awake.group("when").strip())
    chore = ERRAND.search(flat)
    if chore:
        return _say("chore", memory, what=chore.group("what").strip())
    return None


PLACE_OF_CARE = (r"(?:the\s+)?(?:hospital|doctors?|doctor'?s|gp|surgery|clinic|"
                 r"a\s*&?\s*e|a and e|casualty|dentist|dentist'?s|physio|physiotherapy|"
                 r"chiropractor|optician|opticians|health centre|walk in centre)")
BACK_FROM_CARE = re.compile(
    r"\b(?:(?:i'?m|im|i am|we'?re|were)\s+(?:just\s+|only\s+|now\s+|finally\s+)?"
    r"(?:back|out)|(?:just|only|finally)\s+(?:got\s+)?back)\s+(?:of|from)\s+"
    r"(?P<place>" + PLACE_OF_CARE + r")\b", re.I)
WENT_TO_CARE = re.compile(
    r"\b(?:i|we)\s+(?:went|had to go|popped|nipped|headed)\s+(?:in\s+)?(?:to\s+|into\s+)?"
    r"(?P<place>" + PLACE_OF_CARE + r")\b", re.I)
WAS_IN_CARE = re.compile(
    r"\b(?:i|we)\s+(?:was|were)\s+(?:in|at)\s+(?P<place>" + PLACE_OF_CARE + r")\b", re.I)
THIS_WEEK = re.compile(
    r"\b(?:today|tonight|this morning|this afternoon|yesterday|"
    r"last night|last week|just now|this week|earlier)\b", re.I)


def _the_visit_was_this_week(flat):
    if THIS_WEEK.search(flat):
        return True
    return not LONG_AGO.search(flat) and len(flat.split()) <= 8
PUT_ON = re.compile(
    r"\b(?:they|the (?:doctor|doctors|nurse|surgeon|hospital|physio))s?\s+"
    r"(?:put|gave me|fitted|sorted me out with)\s+(?:me\s+)?(?:a|an|the)?\s*"
    r"(?P<thing>cast|sling|brace|boot|splint|plaster|bandage|dressing|support|strapping)\b", re.I)
_A_DRESSING = re.compile(r"bandage|dressing|plaster(?!\s+cast)", re.I)
TAKEN_OUT = re.compile(
    r"\b(?:i\s+)?(?:had|got)\s+(?:a|an|my|two|three)\s+"
    r"(?P<thing>tooth|teeth|wisdom tooth|back tooth|wisdom teeth)\s+out\b", re.I)
HAD_A_THING_DONE = re.compile(
    r"\b(?:i|we)\s+(?:had|got|been for|went for)\s+(?:my|a|an|the)?\s*"
    r"(?P<thing>scan|x-?ray|mri|ct scan|ultrasound|blood test|bloods|biopsy|appointment|"
    r"check-?up|procedure|operation|colonoscopy|endoscopy|ecg|"
    r"smear test|smear|cervical screening|screening|mammogram|jabs?|vaccination|injection|"
    r"booster|flu jab|physio|physiotherapy|filling|stitches|dressing)\b(?!\s+results?\b)", re.I)
RESULT_CLEAR = re.compile(
    r"\b(?:my|the)\s+(?P<thing>scan results|x-?ray results|mri results|biopsy results|"
    r"blood test results|blood results|test results|scan|x-?ray|mri|results|bloods|blood test|"
    r"biopsy)\s+"
    r"(?:came back|came|is|was|were|are)\s+(?:all\s+|totally\s+|completely\s+)?"
    r"(?:clear|fine|normal|ok|okay|good|nothing|negative)\b", re.I)
DOCTOR_SAID = re.compile(
    r"\b(?:the\s+)?(?:doctor|doctors|gp|consultant|surgeon|nurse|physio)s?\s+"
    r"(?:said|says|thinks?|reckons?|told me|has said)\s+"
    r"(?:that\s+)?(?:it'?s|its|it was|i have|i'?ve got|i had|there'?s)\s+"
    r"(?:just\s+|only\s+|probably\s+|most likely\s+|nothing but\s+)?"
    r"(?P<dx>[a-z][a-z' -]{2,30}?)(?:\s*(?:[,.;!]|$|and\b|but\b|so\b|which\b))", re.I)
NIGHT = re.compile(
    r"\b(?:last night|tonight|overnight|all night|in the night|midnight|\d{1,2}\s*(?:am|\.\d\d)|"
    r"this evening|yesterday evening|after dark)\b", re.I)
LONG_AGO = re.compile(
    r"\b(?:back in \d{4}|in \d{4}|\d+ (?:years|months) ago|years ago|months ago|"
    r"last (?:year|week|month|summer|winter|spring|autumn)|"
    r"a while (?:back|ago)|when i was (?:little|young|a kid|at school))\b", re.I)
PART_FINE = re.compile(
    r"\b(?:they|the doctor|the doctors|the gp|the hospital|the consultant|the nurse|the physio)"
    r"s?\s+(?:said|says|told me|reckon)\s+my\s+(?P<part>[a-z][a-z' -]{1,20}?)\s+is\s+"
    r"(?:fine|ok|okay|clear|all right|alright|not broken|nothing serious|nothing)\b", re.I)
RESTED = frozenset("""
    knee knees shoulder shoulders ankle ankles back wrist wrists arm arms leg legs hip hips hand
    hands foot feet neck elbow elbows rib ribs thigh calf calves muscle muscles joint joints finger
    fingers thumb thumbnails toe toes spine hamstring hamstrings achilles groin shin shins forearm
    collarbone cuff tendon tendons ligament ankle heel heels
    """.split())
REST_WORD = re.compile(r"\b(?:rest|resting|physio|exercises|take it easy|ice it)\b", re.I)
GOT_RESULTS = re.compile(
    r"\b(?:(?:i|we)\s+(?:got|had|picked up)\s+(?:my|our|the)?\s*(?P<thing>scan results|"
    r"test results|blood test results|blood results|x-?ray results|mri results|biopsy results|"
    r"results)\s+back|(?:my|the)\s+(?P<thing2>scan results|test results|blood test results|"
    r"results)\s+(?:are|came)\s+in)\b", re.I)
NOT_A_DIAGNOSIS = frozenset((
    "fine", "ok", "okay", "nothing", "nothing serious", "all clear", "good", "clear",
    "going to be", "not", "no", "serious", "normal", "over", "a", "the", "my", "probably",
))
SOMEBODY_ELSE = re.compile(
    r"\b(?:he|she|they|him|her|them|his|hers|their|mum|mom|mother|dad|father|son|daughter|"
    r"wife|husband|partner|brother|sister|friend|grandma|grandad|gran|nan|nanna|aunt|uncle|"
    r"cousin|colleague|boss|neighbour|neighbor)\b", re.I)


INITIALISMS = {"mri": "MRI", "ct": "CT", "ecg": "ECG", "ekg": "EKG", "eeg": "EEG",
               "xray": "x-ray", "x ray": "x-ray", "dna": "DNA", "hiv": "HIV"}


def _a_thing_of_care(phrase, article=True):
    words = [word for word in re.split(r"\s+", str(phrase or "").strip()) if word]
    bare = " ".join(word for word in words if word.lower() not in {"the", "a", "an"})
    bare = re.sub(r"\bdoctors\b", "doctor", bare, flags=re.I) or "visit"
    if re.sub(r"[^a-z&]", "", bare.lower()) in {"a&e", "aande", "ande", "ae"}:
        return {"X": "A&E", "x": "A&E", "Xb": "A&E", "xb": "A&E", "A": "An", "a": "an"}
    inside = ("the " + bare) if article else bare
    first = bare[:1].lower()
    vowel = (first in "aeiouw" and not bare.lower().startswith(("uni", "one", "once", "use"))) \
        or _keep_the_letters(bare) in {"MRI", "ECG", "EEG", "EKG", "x-ray"}
    return {"X": _keep_the_letters(inside[:1].upper() + inside[1:]),
            "x": _keep_the_letters(inside.lower()),
            "Xb": _keep_the_letters(bare[:1].upper() + bare[1:]),
            "xb": _keep_the_letters(bare.lower()),
            "A": "An" if vowel else "A", "a": "an" if vowel else "a"}


def _ends_plural(phrase):
    word = str(phrase or "").split()[-1].lower() if str(phrase or "").split() else ""
    return word.endswith("s") and not word.endswith(("ss", "us", "is"))


def _keep_the_letters(text):
    for word, letters in INITIALISMS.items():
        text = re.sub(r"\b" + re.escape(word) + r"\b", letters, text, flags=re.I)
    return text


WEARER = re.compile(
    r"\b(?:on|for|round|around|over)\s+(?P<owner>my|his|her|their|your|theirs|"
    r"[a-z]+'?s)\s*(?P<part>[a-z][a-z' -]{0,14})?", re.I)


A_BODY = RESTED | frozenset("""
    body skin shin jaw knuckle knuckles waist stomach tummy chest backbone pelvis shoulder scoliosis
    """.split())


def _wearer_is_themselves(flat, match):
    found = WEARER.search(flat, match.end() - 1)
    if not found:
        return True
    if (found.group("owner") or "").lower() != "my":
        return False
    rest = [word.strip(".,!?") for word in flat[found.end("owner"):].split()][:2]
    if len(rest) >= 2 and SOMEBODY_ELSE.match(re.sub(r"'?s$", "", rest[0], flags=re.I)):
        return False
    return bool(rest) and rest[0].lower() in A_BODY


def _names_a_person(word):
    low = str(word or "").strip().lower()
    if not low:
        return False
    if low in facts.RELATIONS or low in facts.KIN_WORDS or low in facts._BUILT_KIN:
        return True
    return bool(SOMEBODY_ELSE.match(low))


def _own_medical_news(flat, memory, clean=""):
    if _reads_as_distress(clean or flat):
        return None
    match = PART_FINE.search(flat)
    if match:
        part = " ".join(str(match.group("part") or "").split())
        if (part and len(part.split()) <= 2 and part.lower() not in facts.NOT_A_PRONOUN_NAME
                and not _names_a_person(part)):
            pool = "med_part_fine" if (REST_WORD.search(flat)
                                       or part.split()[-1].lower() in RESTED) \
                else "med_part_fine_result"
            return _say(pool, memory, **_a_thing_of_care(part, article=False))
    match = PUT_ON.search(flat)
    if match and not LONG_AGO.search(flat) and _wearer_is_themselves(flat, match):
        thing = match.group("thing")
        pool = "med_dressing" if _A_DRESSING.search(thing) else "med_wearing"
        return _say(pool, memory, **_a_thing_of_care(thing))
    if SOMEBODY_ELSE.search(flat):
        return None
    match = RESULT_CLEAR.search(flat)
    if match:
        thing = match.group("thing")
        plural = _ends_plural(thing)
        return _say("med_clear_plural" if plural else "med_clear", memory,
                    **_a_thing_of_care(thing, article=not plural))
    match = DOCTOR_SAID.search(flat)
    if match:
        dx = " ".join(str(match.group("dx") or "").split()).strip(" .,;!")
        if dx and dx.lower() not in NOT_A_DIAGNOSIS and len(dx.split()) <= 3:
            return _say("med_diagnosis", memory, **_a_thing_of_care(dx, article=False))
    visit = "med_visit_night" if NIGHT.search(flat) else "med_visit"
    match = BACK_FROM_CARE.search(flat)
    if match:
        return _say(visit, memory, **_a_thing_of_care(match.group("place")))
    match = WENT_TO_CARE.search(flat)
    if match and _the_visit_was_this_week(flat):
        return _say(visit, memory, **_a_thing_of_care(match.group("place")))
    match = WAS_IN_CARE.search(flat)
    if match and _the_visit_was_this_week(flat):
        return _say(visit, memory, **_a_thing_of_care(match.group("place")))
    match = TAKEN_OUT.search(flat)
    if match and not LONG_AGO.search(flat):
        return _say("med_out", memory, **_a_thing_of_care(match.group("thing")))
    match = GOT_RESULTS.search(flat)
    if match:
        return _say("med_results", memory, **_a_thing_of_care(match.group("thing") or "results"))
    match = HAD_A_THING_DONE.search(flat)
    if match and not LONG_AGO.search(flat):
        return _say(visit, memory, **_a_thing_of_care(match.group("thing")))
    return None


def _news(clean, tokens, memory):
    if clean.endswith("?") or not 1 <= len(tokens) <= 14:
        return None
    better = a_person_getting_better(clean, memory)
    if better:
        return pick(list(better), memory, seed_text=clean)
    if _safety_thread(memory):
        return None
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if isinstance(understood, dict) and understood.get("kind") == "question":
        return None
    clean = _as_said(clean, understood)
    if loss_reading.reads_as_loss(clean):
        return None
    if loss_reading.lost_thing_to_find(clean):
        return None
    flat = clean.replace("'", "").strip(" .,!;:")
    medical = _own_medical_news(flat, memory, clean)
    if medical:
        return medical
    if WISH_LUCK.search(flat):
        return _say("wish_luck", memory)
    if facts.CONDITION.search(flat):
        return None
    if RETIRED.search(flat) and not RETIRED_ASKING.search(flat):
        return _say("retired", memory)
    if OUT_OF_WORK.search(flat):
        return _say("out_of_work", memory)
    if circumstance.reads_as_situation(flat):
        return None
    if said_about_me.reads_as_somebody_elses_words(flat):
        return None
    role_line = AGE_BEFORE_A_ROLE.sub("im ", flat, count=1)
    match = ROLE_WORK.search(role_line) or ROLE.search(role_line)
    if match:
        phrase = facts.no_tone(match.group(1))
        if not phrase:
            return None
        words = phrase.split()
        if not (words and all(w not in ROLE_STOP for w in words)):
            return None
        if ROLE_TO_PEOPLE.search(phrase) or (
                COMPARED_ROLE.search(flat) and match.re is ROLE):
            return None
        rest = match.group(2) if match.re.groups > 1 else None
        if rest:
            rest = _place_of(rest)
        if rest:
            phrase = f"{phrase} in {_tidy(rest)}"
            words = phrase.split()
        if len(words) <= 5 and not any(w in {"of", "with", "about", "that", "too", "and"} for w in words):
            return _say("job", memory, x=phrase, X=phrase[:1].upper() + phrase[1:])
        return None
    match = PLACE.search(clean)
    if match:
        said = match.group(1)
        note = facts.qualified_by(clean)
        place = _place_of(facts.TAKE_BACK_SPLIT.split(said, 1)[0] if note else said)
        if place and PLACE_SPAN.match(place.strip().lower()):
            place = ""
        grown = bool(GROWN_IN.search(flat)) and not facts.grown_up_in_a_place(place)
        if note and place and place.lower() not in PLACE_NONE | PLACE_POSITION and not grown:
            return _say("place_near", memory, place=_tidy(place), near=note)
        if place and place.lower() not in PLACE_NONE | PLACE_POSITION and not grown:
            if MOVING.search(clean):
                return _say("moving", memory, place=_tidy(place))
            return _say("place", memory, place=_tidy(place))
    if TRIP.search(flat):
        return _say("trip", memory)
    kids = facts.kid_count(flat)
    if kids:
        word = facts.KID_NUMBER_WORDS.get(kids, str(kids))
        kids_word = "kid" if kids == 1 else "kids"
        ages = facts.kid_ages(flat)
        if ages and len(ages) == kids:
            said_ages = _numbers(ages)
            return _say("kids_aged", memory, x=word + " " + kids_word + ", " + said_ages,
                        X=word[:1].upper() + word[1:] + " " + kids_word + ", " + said_ages)
        return _say("kids", memory, x=word + " " + kids_word,
                    X=word[:1].upper() + word[1:] + " " + kids_word)
    match = PET.search(flat)
    if match:
        pet = match.group(1)
        after = facts.AFTER_ANIMAL.match(flat[match.end():match.end() + 20].lstrip())
        if not (after and after.group(0).lower() in facts.PET_COMPOUND):
            if not facts.another_animal(flat, pet):
                named = _pet_name(flat, match)
                if named:
                    return _say("pet_named", memory, pet=pet, name=_name_said(named))
                return _say("pet", memory, pet=pet)
    named_pet = _just_named(memory, facts.pet_name_only(flat)
                            or facts.pet_name_only(flat, lower=True)
                            or facts.bare_name(flat))
    if named_pet:
        name = _tidy(named_pet["name"])
        return _say("pet_named", memory, pet=named_pet.get("animal", "pet"),
                    name=_name_said(name))
    if LOST_WEIGHT.search(flat):
        from ..memory import goals as _goals
        planned = _goals.the_loss_that_was_the_plan(flat, memory)
        if planned:
            return planned
        return _say("lost_weight", memory)
    if _a_job_that_went(flat):
        return _say("lost_job", memory)
    for pattern in BAD_NEWS:
        if pattern.search(flat):
            return _say("bad_news", memory)
    if (not reads_as_bad_news(flat) and not reads_as_a_win_nobody_noticed(flat)
            and not reads_as_a_prize_in_a_message(flat)):
        if reads_as_a_pass(flat):
            return _cheer_or_the_question(flat, memory)
        for pattern in GOOD_NEWS:
            match = pattern.search(flat)
            if match and not negated(flat, match.group(0)) and not doubted(flat):
                return _cheer_or_the_question(flat, memory)
    if STATUS.search(flat):
        return _say("status", memory)
    if re.search(r"\bnothing (on|to watch)\b|\bnothing on (the )?(tv|telly)\b", flat):
        return _say("nothing_on", memory)
    if CAME_BACK.search(flat):
        trip = _told_a_trip(flat, memory)
        if trip:
            return trip
        return _say("came_back", memory)
    trip = _told_a_trip(flat, memory)
    if trip:
        return trip
    night = _night_out(flat, memory)
    if night:
        return night
    if JUST_STARTED.search(flat):
        return _say("just_started", memory)
    if JUST_DONE.search(flat):
        if nobody_around(flat.lower(), memory):
            return None
        return _say("move_done" if A_MOVE.search(flat) else "just_done", memory)
    return None


VERDICT_THING = re.compile(r"\b(?:the|this|that|that|my|our|a|an)\s+(?P<thing>[a-z][a-z'-]*)\b")


def _head_word(phrase):
    words = [word for word in re.split(r"[^a-z'-]+", str(phrase).lower()) if word]
    return words[-1] if words else ""


def _the_poor_describer(phrase):
    for word in str(phrase).lower().split():
        if word in SAID_POOR:
            return word
    return ""


def _the_thing_this_line_names(clean):
    match = VERDICT_THING.search(clean)
    if not match:
        return ""
    thing = match.group("thing")
    for word in (thing, thing[:-1] if thing.endswith("s") else ""):
        if word in WATCHED_THINGS:
            return word
    return ""


def _about_the_night_out(clean, tokens, memory):
    seen = memory.get("night_out") if isinstance(memory, dict) else None
    if not isinstance(seen, dict) or not seen.get("place"):
        return None
    if len(memory.get("turns") or []) != seen.get("turn", -9) + 1:
        return None
    if clean.endswith("?") or not 1 <= len(tokens) <= 8:
        return None
    if (WENT_TO_SEE.search(clean) or WENT_TO_SEE_COMPANY.search(clean)
            or WENT_TO.search(clean) or WENT_TO_COMPANY.search(clean)):
        return None
    own_thing = _the_thing_this_line_names(clean)
    named = "the " + own_thing if own_thing else seen["place"]
    values = _place_values(named)
    if VERDICT_WELL.search(clean):
        return _say("night_out_well", memory, **values)
    if WENT_BAD_WEATHER.search(clean):
        return _say("night_out_weather", memory, **values)
    if VERDICT_POOR.search(clean):
        return _say("night_out_poor", memory, **values)
    return None


def _saw_something(flat, memory):
    match = WENT_TO_SEE.search(flat) or WENT_TO_SEE_COMPANY.search(flat)
    if not match:
        return None
    thing = " ".join(match.group(1).split()).strip(" .,!;:")
    words = [w for w in thing.split() if w not in {"the", "a", "an"}]
    said_how = 0
    while len(words) > 1 and words[0] in WATCHED_DESCRIBER:
        words = words[1:]
        said_how += 1
    if not words or words[0] not in WATCHED_THINGS:
        return None
    if said_how:
        named = _tidy(" ".join(w for w in thing.split() if w not in WATCHED_DESCRIBER))
        if isinstance(memory, dict):
            memory["night_out"] = {"place": named, "turn": len(memory.get("turns") or [])}
        poor_describer = _the_poor_describer(thing)
        if poor_describer:
            return _say("saw_it_poor", memory, p=poor_describer,
                        X=named, x=named[:1].lower() + named[1:])
        return _say("saw_it_told", memory, X=named, x=named[:1].lower() + named[1:])
    named = _tidy(thing)
    poor = _poor_word(flat)
    if poor:
        return _say("night_out_poor_said", memory, p=poor, P=poor[:1].upper() + poor[1:],
                    X=named, x=named[:1].lower() + named[1:])
    if WENT_WRONG.search(flat) or WENT_WELL.search(flat):
        return None
    if isinstance(memory, dict):
        memory["night_out"] = {"place": named, "turn": len(memory.get("turns") or [])}
    return _say("saw_it", memory, X=named, x=named[:1].lower() + named[1:])


def _trip_place(phrase, memory):
    name = _place_of(phrase)
    if not name:
        return ""
    words = name.split()
    if len(words) > 4:
        return ""
    low = [word.lower().strip("-'\u2019") for word in words]
    if not all(word.isalpha() for word in low):
        return ""
    article = low[0] in {"the", "a", "an"}
    bare = " ".join(word for word in low if word not in {"the", "a", "an"})
    if bare in KNOWN_PLACES or bare in facts.COUNTRIES or bare in travel_kb.CITIES:
        return name
    if article and bare in TRIP_SHORT_COUNTRIES:
        return name
    typed = str((memory.get("understood") or {}).get("text") or "") \
        if isinstance(memory, dict) else ""
    if any(word[:1].isupper() and word.lower() in low for word in typed.split()):
        return name
    shorter = _place_of(TRIP_TIME_TAIL.sub("", name))
    if shorter and (shorter.lower() in KNOWN_PLACES or shorter.lower() in facts.COUNTRIES
                    or shorter.lower() in travel_kb.CITIES):
        return shorter
    if SOME_WHEN.search(str(phrase)):
        if len(low) == 1 and not article:
            return name
        short = _place_of(TRIP_TIME_TAIL.sub("", name)).split()
        if len(short) == 1 and short[0].lower() not in {"the", "a", "an"}:
            return short[0]
    return ""


def _told_a_trip(flat, memory):
    if TRIP_NOT_YET.search(flat):
        return None
    for pattern, kind in ((BACK_FROM, "back_from"), (BEEN_TO, "been_to"),
                          (WENT_TO_ANY, "day_out")):
        match = pattern.search(flat)
        if not match:
            continue
        place = _trip_place(match.group(1), memory)
        if not place:
            continue
        if _not_a_night_out(place):
            continue
        bare = " ".join(w for w in place.lower().split() if w not in {"the", "a", "an"})
        if bare.split()[0] in NOT_A_PLACE_START:
            continue
        named = _tidy(place)
        if isinstance(memory, dict):
            memory["night_out"] = {"place": named, "turn": len(memory.get("turns") or [])}
        return _say(kind, memory, **_place_values(named))
    return None


GOOD_TIME_WORDS = (
    "lovely|nice|great|good|brilliant|wonderful|amazing|fantastic|superb|cracking|smashing"
    "|relaxing|fun|excellent")
GOOD_TIME_THINGS = (
    "walk|day|morning|afternoon|evening|night|weekend|week|break|lunch|dinner|meal|bath|shower"
    "|swim|run|ride|cycle|sleep|lie in|nap|catch up|chat|time|hour|film|read")
GOOD_TIME = re.compile(
    r"\b(?:i|we)\s+had\s+(?:(?:a|an|such a|quite a|really)\s+)?"
    r"(?:really |properly |long |short |big |little |quiet |slow |easy )?"
    r"(?P<good>" + GOOD_TIME_WORDS + r")\s+(?P<thing>" + GOOD_TIME_THINGS + r")(?:\s+out)?\b"
    r"(?:\s+(?:today|tonight)\b|\s+" + WHEN_DONE + r")?"
    r"(?:\s+with\s+[a-z][a-z' -]{1,20})?\s*[.!]?$")
GOOD_TIME_LINES = (
    "{X} - glad it was a good one. What made it?",
    "{X} - what was the best bit?",
    "{X}, then. Those are worth having more of.",
    "Good to hear. {X} is the sort of thing a week needs.",
)


def _a_good_time_they_had(flat, memory):
    match = GOOD_TIME.search(flat)
    if not match:
        return None
    said = "a " + match.group("good") + " " + match.group("thing")
    if isinstance(memory, dict):
        memory["good_time"] = {"thing": match.group("thing"),
                               "turn": len(memory.get("turns") or [])}
    return pick([line.format(X=_tidy(said)) for line in GOOD_TIME_LINES], memory)


DETAIL_LINES = (
    "That is what makes {article} {thing} worth repeating, then.",
    "So it was the good sort of {thing} - the kind worth having again.",
    "Then it did what {article} good {thing} should. Keep that one.",
)


def _the_detail_of_the_good_time(flat, clean, tokens, memory):
    seen = memory.get("good_time") if isinstance(memory, dict) else None
    if not isinstance(seen, dict) or not seen.get("thing"):
        return None
    if len(memory.get("turns") or []) != seen.get("turn", -9) + 1:
        return None
    if clean.endswith("?") or not 3 <= len(tokens) <= 30:
        return None
    if re.search(r"\b(?:but|however|though|except|apart from)\b", clean):
        return None
    if any(pattern.search(flat) for pattern in BAD_NEWS):
        return None
    thing = seen["thing"]
    article = "an" if thing[:1] in "aeiou" else "a"
    return pick([line.format(thing=thing, article=article) for line in DETAIL_LINES], memory)


GOOD_TIME_THINGS = (
    "walk|swim|run|ride|cycle|lunch|dinner|meal|picnic|bath|shower|breakfast|coffee|nap"
    "|lie in|catch up|chat|read|game of (?:cards|chess|golf|tennis)")
GOOD_TIME = re.compile(
    r"\b(?:i|we)\s+had\s+(?:(?:a|an|such a|quite a|really)\s+)?"
    r"(?:really |properly |long |short |big |little |quiet |slow |easy )?"
    r"(?P<good>lovely|nice|great|good|brilliant|wonderful|amazing|fantastic|superb|cracking"
    r"|smashing|relaxing|fun|excellent)\s+(?P<thing>" + GOOD_TIME_THINGS + r")(?:\s+out)?\b"
    r"(?:\s+(?:today|tonight)\b|\s+" + WHEN_DONE + r")?"
    r"(?:\s+(?:in|at|on|round|by)\s+[a-z][a-z' -]{1,24})?"
    r"(?:\s+with\s+[a-z][a-z' -]{1,20})?\s*[.!]?$")
GOOD_TIME_LINES = (
    "{X} - glad it was a good one. What made it?",
    "{X} - what was the best bit?",
    "{X}, then. Those are worth having more of.",
    "Good to hear. {X} is the sort of thing a week needs.",
)
DETAIL_LINES = (
    "That is what makes {article} {thing} worth repeating, then.",
    "So it was the good sort of {thing} - the kind worth having again.",
    "Then it did what {article} good {thing} should. Keep that one.",
)


def _the_thread_is_heavy_here(memory):
    try:
        return bool(fallback._the_thread_is_heavy(memory))
    except Exception:
        return False


def _a_good_time_they_had(flat, memory):
    match = GOOD_TIME.search(flat)
    if not match:
        return None
    if _the_thread_is_heavy_here(memory):
        return None
    said = "a " + match.group("good") + " " + match.group("thing")
    if isinstance(memory, dict):
        memory["good_time"] = {"thing": match.group("thing"),
                               "turn": len(memory.get("turns") or [])}
    return pick([line.format(X=_tidy(said)) for line in GOOD_TIME_LINES], memory)


def _the_detail_of_the_good_time(flat, clean, tokens, memory):
    seen = memory.get("good_time") if isinstance(memory, dict) else None
    if not isinstance(seen, dict) or not seen.get("thing"):
        return None
    if len(memory.get("turns") or []) != seen.get("turn", -9) + 1:
        return None
    if clean.endswith("?") or not 3 <= len(tokens) <= 30:
        return None
    if re.search(r"\b(?:but|however|though|except|apart from)\b", clean):
        return None
    if _the_thread_is_heavy_here(memory):
        return None
    if any(pattern.search(flat) for pattern in BAD_NEWS):
        return None
    thing = seen["thing"]
    article = "an" if thing[:1] in "aeiou" else "a"
    return pick([line.format(thing=thing, article=article) for line in DETAIL_LINES], memory)


def _night_out(flat, memory):
    detail = _the_detail_of_the_good_time(flat, flat, flat.split(), memory)
    if detail:
        return detail
    good_time = _a_good_time_they_had(flat, memory)
    if good_time:
        return good_time
    detail = _the_detail_of_the_good_time(flat, flat, flat.split(), memory)
    if detail:
        return detail
    good_time = _a_good_time_they_had(flat, memory)
    if good_time:
        return good_time
    seen = _saw_something(flat, memory)
    if seen:
        return seen
    match = WENT_TO.search(flat) or WENT_TO_COMPANY.search(flat)
    if not match:
        return None
    place = " ".join(match.group(1).split()).strip(" .,!;:")
    words = place.split()
    if not place or words[0] in {"my", "our", "his", "her", "their"}:
        return None
    if _not_a_night_out(place):
        return None
    bare = " ".join(w for w in words if w not in {"the", "a", "an"})
    if bare.split()[0] in NOT_A_PLACE_START:
        return None
    named = _tidy(place)
    values = {"X": named, "x": named[:1].lower() + named[1:]}
    poor_describer = _the_poor_describer(place)
    if poor_describer and not _poor_word(flat):
        bare_place = _tidy(" ".join(w for w in words if w not in SAID_POOR))
        if bare_place:
            if isinstance(memory, dict):
                memory["night_out"] = {"place": bare_place,
                                       "turn": len(memory.get("turns") or [])}
            return _say("day_out_poor", memory, p=poor_describer,
                        **_place_values(bare_place))
    poor = _poor_word(flat)
    if poor:
        return _say("night_out_poor_said", memory, p=poor, P=poor[:1].upper() + poor[1:],
                    **values)
    if WENT_WRONG.search(flat):
        return None
    if isinstance(memory, dict):
        memory["night_out"] = {"place": named, "turn": len(memory.get("turns") or [])}
    if WENT_WELL.search(flat):
        return _say("day_out_well", memory, **values)
    return _say("day_out", memory, **values)


def _a_pick_is_in_hand(memory):
    if not isinstance(memory, dict):
        return False
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns or not isinstance(turns[-1], dict):
        return False
    last = turns[-1]
    said = " ".join(str(last.get(key) or "") for key in ("user", "bot")).lower()
    return bool(set(re.findall(r"[a-z']+", said)) & PICK_WORDS)


def _asks_for_a_joke(clean, tokens, memory=None):
    if (WANTS_A_THING.search(clean) and not ASKS_ALOUD.search(clean)
            and _a_pick_is_in_hand(memory)):
        return False
    if JOKE_ADVICE.search(clean):
        return False
    if SELF_JOKE.search(clean):
        return False
    if _fond_of_the_bot(clean):
        return False
    if JOKE_ASKED.search(clean):
        return True
    if RUNTIME_LIMIT.search(clean):
        return False
    if not JOKE_ASK.search(clean):
        return False
    return not (set(tokens) & PICK_WORDS)

INTENTION = re.compile(
    r"\b(?:i'm|im|i am|we're|were|we are)\s+(?:thinking (?:of|about)|considering|toying with|"
    r"planning to|hoping to|looking to|keen to|meaning to)\s+(.+)$")
WANT = re.compile(r"\b(?:i|we)\s+" + SOFTEN + r"(?:want|need|fancy|would like|"
                  r"'d like)\s+(?:to\s+)?(.+)$")
QUESTION = re.compile(r"^(?:ok |okay |so |and |but |well )*(?:do|does|did|can|could|should|would|"
                      r"will|is|are|was|were|what|where|when|why|how|who|which|any)\b")
THING_SKIP = re.compile(r"\bhelp\b|\b(?:don'?t|dont|do not) know (?:if|where|how|what|whether)\b|"
                        r"\bnot sure (?:if|whether|where|how|what)\b|"
                        r"\bwhere (?:do|should|can) i (?:start|begin)\b")
KEEPS = re.compile(r"\b(?:i|we)\s+keep\s+(\w+ing)\b\s*(.*)$")
KEEP_ABOUT_SOMEONE = re.compile(r"\b(?:" + "|".join(ack.facts.RELATIONS) + r")s?\b"
                                r"|\b(?:people|someone|somebody|everyone|anyone|myself|friends"
                                r"|mates|colleagues|classmates|boss)\b")
KEEP_INTENT = frozenset("meaning wanting thinking trying hoping planning".split())
KEEP_A_BELIEF = frozenset(("thinking",))
A_THOUGHT_THAT_IS_NOT_A_THING = re.compile(
    r"^(?:it|its|it's|itll|it'll|im|i'm|ive|i've|id|i'd|everyone|everyones|everybody|nobody"
    r"|no one|people)\b")
A_DOUBT_ABOUT_IT = re.compile(
    r"\b(?:me|my\b|myself|go(?:es|ne|ing)?\s+away|get(?:s|ting)?\s+better|never|"
    r"not\s+going\s+to|wont|won't|worse|worth|hopeless|pointless|too\s+late|fault|"
    r"watching|judging|noticed?|found\s+out|fail(?:ed|ing|s)?|ruin(?:ed|ing|s)?|"
    r"useless|stupid|wrong|happen(?:s|ed|ing)?\s+to\s+me|forever|for\s+good|"
    r"over|keep\s+me|stop\s+me|blow\s+over|blow\s+past|sort\s+itself\s+out|"
    r"work\s+itself\s+out|come\s+back|come\s+right|come\s+round|be\s+over|"
    r"pass\s+on\s+its\s+own)\b", re.I)
A_THOUGHT_ABOUT_OTHERS = re.compile(
    r"^(?:everyone|everyones|everybody|nobody|no one|people)\b")
A_HOPELESS_THOUGHT = re.compile(
    r"\b(?:not\s+worth|no\s+point|hopeless|no\s+hope|too\s+late)\b", re.I)
ASK_TAIL = re.compile(r"\b(?:any tips|any advice|tips|advice)\b", re.I)
NEED_NOW = frozenset("""
ambulance hospital a&e ae doctor doctors gp nurse nurses paramedic paramedics 999 911 111
inhaler insulin epipen adrenaline medicine medicines meds medication tablets painkiller
painkillers prescription chemist pharmacy water drink loo toilet wee pee bathroom rest sleep
nap lie-down sickbag bucket ambulance crew
""".split())
MEDICINE = re.compile(
    r"\b(?:antidepressants?|ssris?|snris?|tablets?|pills?|medication|medicines?|meds|insulin|"
    r"inhalers?|steroids?|statins?|hormones?|the pill|chemotherapy|radiotherapy|painkillers?|"
    r"antibiotics?|methadone|antipsychotics?|anti-psychotics?|lithium|beta[- ]blockers?|"
    r"blood thinners?|diazepam|tranquillisers?|tranquilizers?)\b", re.I)

KEEPS_SYMPTOM = re.compile(
    r"\b(?:faint|faints|fainting|fall|falls|falling|black out|blacking out|bleed|bleeds|bleeding|"
    r"throw up|throwing up|vomit|vomiting|dizzy|shaking|shake|fit|fits|seizure|seizures|"
    r"cold|colds|headache|headaches|migraine|migraines|rash|rashes|cough|coughing|wheez\w*|"
    r"pain|pains|hurting|hurts|ache|aches|aching|cramp|cramps|blister|blisters|nosebleed\w*|"
    r"tired|tiredness|knackered|exhausted|shattered|worn out|drained|washed out|fatigued)\b",
    re.I)
TIME_TAIL = re.compile(
    r"\s+\b(?:tonight|today|tomorrow|this (?:evening|afternoon|morning|weekend|week|year)|"
    r"next (?:week|weekend|month|year)|at the weekend|at some point|later on|later|soon|now)\b.*$",
    re.I)
FILLER_TAIL = frozenset("""
actually really honestly truly genuinely tbh though although anyway anyhow too also instead
already then please maybe probably perhaps possibly just now here there ok okay yeah right eh
""".split())


FILLER_TAIL_PHRASES = tuple(phrase.split() for phrase in """
as well|for now|this year|next year|right now|at the moment|i think|i guess|i suppose|of course
for sure|to be honest|if possible|at least|so far|in the end|as usual
""".replace("\n", "|").split("|") if phrase.strip())
CORRECTION_TAIL = re.compile(
    r"^\s*(?:no|sorry|i mean|i meant|rather|make that|instead|actually)\b[\s,:-]*(?P<t>\S.*)$",
    re.I)
NEGATED_TAIL = re.compile(
    r"^\s*(?:and |but |honestly |definitely |really |just |probably )*"
    r"(?:not|rather than|instead of|anything but|other than)\b", re.I)


def _without_a_filler_tail(thing):
    said = " ".join(str(thing or "").split())
    head, _, tail = said.partition(",")
    head = head.strip(" ,;:")
    if tail:
        fixed = CORRECTION_TAIL.match(tail)
        if NEGATED_TAIL.match(tail):
            said = head or (fixed.group("t") if fixed else said)
        elif fixed:
            said = fixed.group("t")
        elif head:
            said = head
    words = said.split()
    changed = True
    while changed and len(words) > 1:
        changed = False
        for phrase in FILLER_TAIL_PHRASES:
            if len(words) > len(phrase) and all(
                    word.lower().strip(".!?") == want
                    for word, want in zip(words[-len(phrase):], phrase)):
                words = words[:-len(phrase)]
                changed = True
                break
    while len(words) > 1 and words[-1].lower().strip(".!?") in FILLER_TAIL:
        words.pop()
    return " ".join(words)


INDEFINITE = frozenset("something anything stuff things some".split())
PAIN_PART = re.compile(
    r"\b(?:stomach|tummy|belly|back|neck|shoulder|knee|elbow|wrist|ankle|foot|feet|toe|hand|"
    r"thumb|finger|hip|leg|arm|mouth|tooth|teeth|gum|gums|ear|ears|eye|eyes|throat|chest|nose|"
    r"skin|head|hip|shin|calf|heel|skin|burn|blister|bite|sting|rash|itch|cramp)\b")
INDEFINITE_SKIP = frozenset("to for that which like of".split())
ASK_KIND = (
    "What sort of {adj} are you after? Name one you liked and I'll go from there.",
    "{x}? Tell me what you've enjoyed before and I'll suggest something.",
)
DOING = frozenset("""
start starting begin beginbegin learn learning try trying eat eating get getting go going do doing
take taking up cut cutting quit quitting stop stopping save saving write writing sort sorting
clear clearing tidy tidying build building train training practise practice run running walk
walking swim swimming cook cooking read reading study studying""".split())
ALWAYS = re.compile(r"\b(?:i'm|im|i am|we're|we are)\s+always\s+(.+)$")

ONE_OFF = frozenset("""
cancel quit resign book rebook order buy pay sell file send phone call ring unsubscribe
subscribe delete close return renew sign switch claim report transfer drop
""".split())
DECISION = re.compile(
    r"\b(?:move|moving|moved)\s+(?:in|out|abroad|away|back)\b"
    r"|\bget(?:ting)?\s+(?:married|divorced|engaged)\b"
    r"|\b(?:buy|buying|sell|selling)\s+(?:a|the|our|my)\s+(?:house|flat|home|car)\b"
    r"|\bretir(?:e|ing|ement)\b|\bemigrat\w*\b|\bhave a baby\b|\bstart a family\b"
    r"|\bgo(?:ing)?\s+back\s+to\s+(?:college|university|school|work)\b", re.I)
TASK_ONLY = ("smallest version", "hardest")
STATE = re.compile(
    r"\b(?:be|being|stay|feel)\s+(?:left alone|alone|left|out of it|free|done|rid of \w+|there)\b"
    r"|\bleft alone\b", re.I)
CONTINUING = frozenset(("keep going", "carry on", "keep at it", "keep it up", "keep trying"))
BARE_FEELING = frozenset(("disappear", "vanish", "give up", "give in", "hurt", "cry", "sob",
                          "die"))

RELATIVE = re.compile(r"\b(?:that|which|who|whose|where)\b", re.I)

LEAVE = re.compile(r"\b(?:time|day|days|week|weeks|evening|afternoon|morning|night|weekend"
                   r"|fortnight|month)\s+off\b"
                   r"|\b(?:annual leave|sick leave|sick day|parental leave|compassionate leave"
                   r"|unpaid leave|holiday entitlement|leave of absence|paid leave)\b", re.I)

_A_NEED_ASK = re.compile(
    r"\bdo\s+(?:i|we|you)\s+(?:really\s+|even\s+|still\s+)?need\b", re.I)

PERSON_WORK = re.compile(
    r"(?:er|or|ian|ist|man|woman|guy|person|smith)$", re.I)
NOT_A_GOOD = frozenset("""
baby child kid toddler son daughter boy girl partner husband wife fiance fiancee boyfriend
girlfriend friend mate person people family mum dad mother father brother sister gran nan
grandma grandad grandmother grandfather aunt uncle cousin relative neighbour colleague boss
nanny babysitter carer plumber doctor dentist nurse midwife
break rest sleep time chance money advice help support idea hug kiss cry favour favor lift ride
hand hands
pay rise rise promotion job refund rebate visa passport mortgage loan debt lawsuit claim
night evening morning afternoon weekend day out
complaint apology resignation divorce wedding funeral party appointment ceremony christening
interview operation surgery birthday anniversary degree exam test
tattoo house flat home cottage dog cat puppy kitten pet""".split())


NOT_THE_THING = frozenset("""
back too again instead please now then anyway though later one ones it them those these
something anything nothing sort kind bit
him her me us you they he she we them mine yours ours theirs
up down off out away along around round through over apart forward forwards backwards
in on at by""".split())


_A_PERSON_ALREADY_IN_THE_LINE = frozenset(
    "him her them me us you they he she we mine yours ours".split())
NOT_A_THING_WITH_KINDS = frozenset("""
monday tuesday wednesday thursday friday saturday sunday weekday weekend week month year day
today tonight tomorrow yesterday morning afternoon evening night noon midnight
january february march april may june july august september october november december
spring summer autumn winter christmas easter birthday anniversary date
""".split())


def _kindless(word):
    w = word.lower().strip(" .,!?;:'\u2019\"()")
    if w in NOT_A_THING_WITH_KINDS:
        return True
    if w in NOT_A_GOOD or w in NOT_THE_THING:
        return True
    from .particles import a_job_word
    if a_job_word(w):
        return True
    if w.endswith("ies") and w[:-3] + "y" in NOT_A_GOOD:
        return True
    for tail in ("es", "s"):
        if w.endswith(tail) and w[:-len(tail)] in NOT_A_GOOD:
            return True
    return bool(breeds.the_kind_of(w))
KINDLESS = (
    "{X} — tell me a bit more and I'll help you think it through.",
    "{X}? Where are you up to with it?",
    "Say more about {x} and I'll help you work out the next step.",
)
_PERSON_IN_THE_TAIL = re.compile(
    r"\b(?:from|about|with|around)\s+(?P<who>him|her|them|me|us|you)\b")
A_BREAK_FROM_SOMEONE = (
    "{X}? Tell me what's going on with {them} — that's usually where the answer is.",
    "{X} — fair enough. What is it about {them} that's wearing you down?",
    "{X} is a fair thing to want. What would time away from {them} give you that you are "
    "not getting now?",
)
CHOOSING = (
    "{X} — what kind are you after?",
    "What kind of {head} do you usually go for?",
    "{X}: tell me what you want from it and I'll help you narrow it down.",
)
THING_REPLIES = {
    "intention": (
        "{X}? Good thing to want. What's the bit you're least sure about?",
        "Worth planning rather than rushing into: what would have to go right for you?",
        "I'd say do it if the practical side works out. Want to work through what it would take?",
    ),
    "want": (
        "{X} \u2014 fair enough. What's stopped it happening so far?",
        "Then start with the smallest version of it, not the whole thing. What would the first "
        "step be?",
        "Doable. Tell me the bit that feels hardest and we'll start there.",
    ),
    "keeps": (
        "{X} keeps happening \u2014 that's usually the routine rather than you. "
        "What have you tried?",
        "Annoying. Is it the same every time, or does it vary?",
        "Worth fixing once rather than every week. What's the moment it goes wrong?",
    ),
    "keeps_someone": (
        "{X} keeps happening \u2014 that's usually the routine rather than you. "
        "What have you tried?",
        "That would wear anyone down. How long has it been like that?",
        "Worth fixing once rather than every week. What's the moment it goes wrong?",
    ),
    "always": (
        "Always {x}? That's a routine thing more than a character thing.",
        "{X} every time \u2014 what's the usual trigger?",
        "Always {x}? Then there's a pattern in it somewhere. When did it start?",
    ),
}


def _a_death_just_said(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return False
    for turn in turns[-2:]:
        said = turn.get("user") if isinstance(turn, dict) else None
        if not isinstance(said, str) or not said.strip():
            continue
        if not loss_reading.reads_as_loss(said):
            continue
        if urgent_reading.reads_as_a_story(loss_reading._spoken(said)):
            continue
        return True
    return False


def _in_loss(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return False
    return any(isinstance(turn, dict) and loss_reading.reads_as_loss(turn.get("user") or "")
               for turn in turns[-6:])


def _answers_knows(text, memory):
    from . import answers
    try:
        return bool((answers.respond(text, memory) or "").strip())
    except Exception:
        return False


GENERIC_THING_WORDS = frozenset("""more better best thing things stuff a an the to of it my me
i we you want wanted need needs get gets got make makes made do does did keep keeps keeping
keep learning learn start starting started go going up down on off for with and but so
again really quite very lot bit time times""".split())


_VERB_ENDINGS = ("ing", "ed", "es", "s", "e", "en", "t")


def _verb_stem(word):
    word = str(word or "").lower().strip("'")
    if word.endswith("ied"):
        word = word[:-3] + "y"
    for ending in _VERB_ENDINGS:
        if len(word) > len(ending) + 2 and word.endswith(ending):
            word = word[:-len(ending)]
            break
    if len(word) > 3 and word[-1] == word[-2] and word[-1] not in "aeiou":
        word = word[:-1]
    return word


def _answers_is_about_the_thing(text, thing, memory, verbs=()):
    try:
        from ..knowledge.lookup import find
        from ..understanding import understand
        scratch = dict(memory) if isinstance(memory, dict) else {}
        entry = find(understand(text, scratch))
        if entry is None:
            return False
        said = set()
        for part in (entry.key or ()):
            for piece in (part if isinstance(part, tuple) else (part,)):
                said.update(re.findall(r"[a-z']+", str(piece).lower()))
        line = " " + " ".join(str(text or "").lower().split()) + " "
        for part in (entry.key or ()):
            for piece in (part if isinstance(part, tuple) else (part,)):
                piece = " ".join(str(piece).lower().split())
                if piece.count(" ") >= 2 and piece in line:
                    return True
        stems = {_verb_stem(verb) for verb in verbs if verb}
        for word in re.findall(r"[a-z']+", str(thing or "").lower()):
            if word in GENERIC_THING_WORDS or _verb_stem(word) in stems:
                continue
            if word in said or word[:-1] in said or word + "s" in said:
                return True
        return False
    except Exception:
        return False


_HOW_STOP = frozenset("""a an the my our your his her their its some any to for of on in at with
and or but so i we you it that this these those there do does did how what where when why please
just really properly better best more most myself yourself""".split())


def _answers_has_the_how(thing, memory):
    try:
        from ..knowledge import lookup
        from ..understanding import understand
        found = lookup.find(understand("how do i " + thing))
        if found is None:
            return False
        content = {word for word in re.findall(r"[a-z']+", thing.lower())
                   if word not in _HOW_STOP and len(word) > 1}
        return bool(content) and content <= lookup.key_words(found)
    except Exception:
        return False


def _fallback_has_its_own_pool(text):
    from ..compose import fallback as compose_fallback
    from ..compose import loss as compose_loss
    plain = " ".join(str(text or "").lower().split())
    try:
        if compose_loss.keeps_losing_thing(plain):
            return True
        for pattern in (compose_fallback.FORGET_A_DATE, compose_fallback.FORGET_A_SECRET,
                        compose_fallback.FORGETS_A_CLASH, compose_fallback.FORGETS_AGAIN):
            if pattern.search(plain):
                return True
        return compose_fallback._is_rumination(plain)
    except Exception:
        return False


def _the_words_they_meant(clean, understood):
    plain = understood.get("plain") if isinstance(understood, dict) else None
    plain = " ".join(str(plain or "").lower().replace("\u2019", "'").split())
    if not plain or plain == clean:
        return clean
    typed, meant = clean.split(), plain.split()
    if len(typed) != len(meant):
        return clean
    for was, is_ in zip(typed, meant):
        if was == is_:
            continue
        if was in ("2", "4") or was.startswith(is_) or is_.startswith(was):
            continue
        return clean
    return plain


def _their_thing(clean, tokens, memory, understood=None):
    from ..compose import fallback as compose_fallback
    clean = _the_words_they_meant(clean, understood)
    if clean.endswith("?") or not 3 <= len(tokens) <= 16:
        return None
    if QUESTION.match(clean) or THING_SKIP.search(clean):
        return None
    if MEDICINE.search(clean):
        return None
    if loss_reading.reads_as_loss(clean) or _in_loss(memory):
        return None
    if harm_reading.reads_as_hurting_someone(clean):
        return harm_reading.reply_for(clean, memory)
    quoted = saidby_reading.reply_for(clean, memory)
    if quoted:
        return quoted
    if compose_fallback._the_morning_has_a_clock(clean):
        return None
    if ack.WANTS_ANSWER.search(clean) or ASK_TAIL.search(clean):
        return None
    if " but " in " " + clean + " ":
        return None
    if " without " in " " + clean + " ":
        return None
    flat = clean.replace("\u2019", "'").strip(" .,!;:")
    verbs = ()
    for kind, pattern in (("intention", INTENTION), ("want", WANT), ("always", ALWAYS),
                          ("keeps", KEEPS)):
        match = pattern.search(flat)
        if not match:
            continue
        if kind == "keeps":
            said = (match.group(2) or "").strip()
            if match.group(1).lower() in KEEP_A_BELIEF and A_THOUGHT_THAT_IS_NOT_A_THING.match(said):
                if A_HOPELESS_THOUGHT.search(flat):
                    return pick(REPLIES["not_coping"], memory)
                if (A_THOUGHT_ABOUT_OTHERS.match(said)
                        or A_DOUBT_ABOUT_IT.search(said)):
                    return None
            if match.group(1).lower() in KEEP_INTENT:
                kind = "want"
                thing = (match.group(2) or "").strip()
            else:
                verbs = (match.group(1),)
                thing = (match.group(1) + " " + (match.group(2) or "")).strip()
        else:
            thing = match.group(1).strip()
        if re.search(r"\bso that\b|\bso (?:i|we) (?:can|could|will|would)\b", flat):
            return None
        thing = re.split(r"\b(?:because|but|so|though|although)\b", thing)[0].strip(" ,;:")
        thing = TIME_TAIL.sub("", thing).strip(" ,;:")
        first = (thing.split() or [""])[0]
        if thing.lower() in BARE_FEELING:
            return pick(REPLIES["not_coping"], memory)
        if (first in FEELING_THING or FEELING_WANT.search(thing)
                or LEAVE_SOMEONE.search(thing)
                or thing.lower() in CONTINUING):
            return None
        stopping = STOPS_TOGETHER.match(thing)
        if stopping:
            if " ".join(stopping.group("subject").split()).lower() in SAYS_NOTHING:
                return pick(REPLIES["not_coping"], memory)
            return None
        thing = _without_a_filler_tail(thing)
        if re.search(r"\b(?:i|i'm|im|i've|i'd|we|we're|us)\b", thing):
            return None
        words = thing.split()
        if not 1 <= len(words) <= 8:
            return None
        if words[0] in {"go", "be", "do", "get", "have", "try", "say", "know", "see", "it"} \
                and len(words) <= 2:
            return None
        if LEAVE.search(clean):
            return None
        if kind in ("want", "need") and _A_NEED_ASK.search(clean):
            return None
        if ack.a_limit_on_the_plan(clean):
            return None
        problem = " ".join(w for w in words[1:] if w not in INDEFINITE_SKIP) \
            if words[0] in INDEFINITE else thing
        if words[0] in INDEFINITE and (_answers_knows(clean, memory)
                                       or ((SYMPTOM.search(problem) or PAIN_PART.search(problem)
                                            or SYMPTOM.search(thing) or PAIN_PART.search(thing))
                                           and (_answers_knows("what helps " + problem, memory)
                                                or _answers_knows("what helps " + thing, memory)))):
            return None
        if words[0] in INDEFINITE and SYMPTOM.search(problem):
            problem_read = understanding(problem, memory)
            problem_part = problem_read.get("body") if isinstance(problem_read, dict) else None
            if problem_part and "ill_" + problem_part in REPLIES:
                return _reply("ill_" + problem_part, memory, _name(memory), clean)
        someone = _PERSON_IN_THE_TAIL.search(clean)
        if someone and not _answers_knows(clean, memory):
            said = thread.your_words(thing)
            return pick(A_BREAK_FROM_SOMEONE, memory).format(
                X=said[:1].upper() + said[1:], them=someone.group("who"))
        if words[0] in INDEFINITE:
            rest = [w for w in words[1:] if w not in INDEFINITE_SKIP]
            said = thread.your_words(thing)
            return pick(ASK_KIND, memory).format(
                x=said[:1].upper() + said[1:],
                adj=rest[0] if rest else "thing")
        if kind in ("want", "need") and (set(w.lower() for w in words) & NEED_NOW):
            return None
        if kind in ("keeps", "always") and KEEPS_SYMPTOM.search(thing):
            return None
        if kind in ("keeps", "always") and _answers_knows(clean, memory):
            return None
        if kind in ("keeps", "always") and _fallback_has_its_own_pool(clean):
            return None
        if kind in ("want", "keeps", "always", "intention") \
                and _answers_is_about_the_thing(clean, thing, memory, verbs) \
                and _answers_knows(clean, memory):
            return None
        if words[0] in {"a", "an", "some", "the", "my", "another", "one"}:
            head = re.split(r"\b(?:for|on|in|at|with|to|about|from)\b",
                            " ".join(words))[0].split()[-1]
            if (PERSON_WORK.search(head) or RELATIVE.search(thing)
                    or _answers_knows(clean, memory)):
                return None
            from .particles import a_thing_without_its_tail
            said = a_thing_without_its_tail(thread.your_words(thing))
            label = said[:1].upper() + said[1:]
            if head.lower() in _A_PERSON_ALREADY_IN_THE_LINE:
                return None
            if _kindless(head):
                options = [option.format(x=said, X=label) for option in KINDLESS]
                return pick(options, memory)
            options = [option.format(X=label, head=head) for option in CHOOSING]
            return pick(options, memory)
        if ack.DEATH_WORDS.search(clean):
            return None
        if STATE.search(thing) or words[0] in ONE_OFF:
            return None
        if _answers_has_the_how(thing, memory) and _answers_knows(clean, memory):
            return None
        pool = THING_REPLIES[kind]
        if kind == "keeps" and KEEP_ABOUT_SOMEONE.search(clean):
            pool = THING_REPLIES["keeps_someone"]
        if DECISION.search(thing) or (kind == "want" and words[0] not in DOING):
            pool = tuple(option for option in pool
                         if not any(bad in option for bad in TASK_ONLY))
        if not pool:
            return None
        said = thread.your_words(thing)
        options = [option.format(x=said, X=said[:1].upper() + said[1:]) for option in pool]
        return pick(options, memory)
    return None


SELF_JOKE = re.compile(r"\b(?:im|i am|i'm|being|made me|make me feel|i feel like|feel like|"
                       r"my life|myself)\b[^.!?]{0,24}?\bjokes?\b")


_NOT_A_SUBJECT = frozenset("""
    my your his her their our its the a an this that these those me him them us you it
    some any every no
""".split())


REPORTS_A_JOKE = re.compile(
    r"\b(?:made|told|cracked|sent|texted)\s+(?:me\s+|us\s+)?(?:a\s+|another\s+|some\s+)?"
    r"jokes?\b")


def _asks_outright(clean):
    return bool(JOKE_ASK.search(clean)) or clean.strip().startswith("joke")


def _joined_read(memory):
    return bool(memory.get("joined_read")) if isinstance(memory, dict) else False


def _joke(clean, tokens, memory):
    if verdicts_a_thing(clean):
        return None
    if _joined_read(memory):
        return None
    asked_by_name = _asks_for_a_joke(clean, tokens, memory)
    if not _asks_outright(clean) and REPORTS_A_JOKE.search(clean):
        return None
    if not _asks_outright(clean) and isinstance(memory, dict) and memory.get("loss"):
        return None
    after_joke = _last_was_joke(memory) and len(tokens) <= 8 and any(
        t in {"another", "more", "next", "again", "else", "any", "got", "one"} for t in tokens)

    if not (asked_by_name or after_joke
            or ("joke" in tokens and len(tokens) <= 10
                and not (JOKE_ADVICE.search(clean) or set(tokens) & PICK_WORDS)
                and not SELF_JOKE.search(clean))):
        return None
    subject = None
    match = re.search(r"\babout\s+(?:(?:a|an|the|my|your|his|her|their|our|its)\s+)?([a-z]+)", clean)
    if match:
        subject = match.group(1).rstrip("s")
        if subject in _NOT_A_SUBJECT:
            subject = None
    words = {t.rstrip("s") for t in tokens}
    for key, joke in JOKES.items():
        if key in words or key in (subject or ""):
            return joke
    for key, joke in JOKES.items():
        if re.search(r"\b" + key + r"s?\b", clean):
            return joke
    if subject:
        return f"I don't know a good {subject} one, sorry. " + pick(SHORT_JOKES, memory)
    return pick(SHORT_JOKES, memory)


def _normalised_line(memory):
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if not isinstance(understood, dict):
        return None
    norm = understood.get("norm")
    if not isinstance(norm, list) or not norm or norm == understood.get("words"):
        return None
    return " ".join(norm)


STANDING_LINE = re.compile(
    r"^\W*(?:and\s+|well\s+|oh\s+|hmm\s+|it'?s\s+been\s+|its\s+been\s+|that'?s\s+been\s+|"
    r"i'?ve\s+been\s+|ive\s+been\s+|been\s+|i'?ve\s+had\s+it\s+|ive\s+had\s+it\s+|"
    r"it'?s\s+|its\s+|that'?s\s+)?"
    r"(?:going\s+on\s+|going\s+|like\s+(?:this|that)\s+|now\s+|"
    r"there\s+|at\s+it\s+|doing\s+it\s+|this\s+way\s+|that\s+way\s+)?(?:for\s+)?"
    r"(?:about\s+|around\s+|nearly\s+|over\s+|like\s+)?"
    r"(?:(?:\d+|a|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"a\s+couple\s+of|a\s+few|several)\s+)?"
    r"(?:days?|weeks?|months?|years?|ages|a\s+long\s+time|all\s+(?:week|month|year)|"
    r"since\s+(?:yesterday|this\s+morning|last\s+night|the\s+weekend|christmas|the\s+summer|"
    r"last\s+\w+|monday|tuesday|wednesday|thursday|friday|saturday|sunday|january|february|"
    r"march|april|may|june|july|august|september|october|november|december))"
    r"(?:\s+(?:now|too|already|in\s+a\s+row))?\W*$")

STANDING_WHAT_REPLIES = {
    "days": ("A few days of what - has something been going on?",
             "Days of what, sorry? Tell me what has been happening and I can help.",
             "What is it that has been going on for a few days?"),
    "weeks": ("Weeks of what - has something been going on?",
              "Weeks of what, sorry? Tell me what it is and I can help.",
              "What is it that has been going on for weeks?"),
    "months": ("Months of what - what has been going on that long?",
               "What is it that has been going on for months?",
               "Months of what, sorry? What is it that has been going on?"),
    "long": ("What has been going on that long?",
             "How long of what, sorry - what is it that has been going on?",
             "Tell me what it is that has been going on all this time."),
}

STANDING_REPLIES = {
    "days": (
        "That's still early days — keep a note of when it's worse and give it a full week before "
        "you think about a GP.",
        "That's short enough to wait on. If it's the same this time next week, that's when it's "
        "worth getting looked at.",
        "Early days on its own is common enough. What would make it worth mentioning is it still "
        "being there after a week.",
    ),
    "weeks": (
        "Weeks of it is the point where a GP is worth the trip, even if it turns out to be nothing.",
        "Two or three weeks is long enough to stop waiting it out. Say how long it's been when you "
        "book, because that's what moves it along.",
        "Weeks is where it stops being bad luck and starts being worth a proper look.",
    ),
    "months": (
        "Months is long enough that it deserves a proper look — ask for a longer appointment and "
        "say how long it's been.",
        "Months is usually where people stop mentioning it and just get on with it. Say the length "
        "out loud in the appointment and ask what can be done about it.",
        "Months of that is worth taking seriously rather than riding out.",
    ),
    "long": (
        "That long is worth a longer appointment, and saying exactly how long it's been: it changes "
        "what they look at.",
        "Years of putting up with it is a lot. Write the length down before you go in, or the "
        "appointment is over in five minutes.",
        "Carrying that for that long is tiring on its own, and it's fair to want it looked at "
        "properly now.",
    ),
}

A_THING_THAT_BREAKS = re.compile(
    r"\b(?:laptops?|computers?|pcs?|macbooks?|phones?|iphones?|tablets?|ipads?|printers?|"
    r"scanners?|routers?|modems?|wifi|wi-fi|broadband|internet|emails?|app|software|windows|"
    r"tv|tvs|televisions?|telly|monitors?|screens?|consoles?|playstations?|xbox|speakers?|"
    r"headphones?|keyboards?|mouses?|chargers?|batter(?:y|ies)|"
    r"cars?|vans?|bikes?|bicycles?|motorbikes?|scooters?|engines?|tyres?|tires?|"
    r"boilers?|heating|radiators?|thermostats?|washing\s+machines?|washers?|dishwashers?|"
    r"tumble\s+dryers?|dryers?|fridges?|freezers?|ovens?|cookers?|hobs?|microwaves?|"
    r"kettles?|toasters?|vacuum|hoover|mowers?|lawnmowers?|drills?|"
    r"taps?|showers?|toilets?|sinks?|drains?|pipes?|guttering|gutters?|roofs?|fences?|gates?|"
    r"doors?|locks?|windows?|garages?|sheds?|shelves|shelf|"
    r"washer|dryer|machine|device|gadget|appliance)\b", re.IGNORECASE)

STANDING_THING_REPLIES = {
    "days": (
        "Two days of it is still worth watching rather than fixing. Note when it does it, "
        "because that is the first thing anyone will ask you.",
        "A couple of days is early for a repair. If it does it again tomorrow, that is when to "
        "start asking.",
    ),
    "weeks": (
        "Two or three weeks of that is past bad luck. Back anything up that matters, then have "
        "it looked at properly rather than living with it.",
        "Weeks of it is long enough to stop waiting it out. Say how long it has been doing it "
        "when you ring, because it moves the job along.",
    ),
    "months": (
        "Months of it is worth sorting out rather than working around. Say how long it has been "
        "doing it, and ask what a repair costs before they start.",
        "Months of putting up with it usually means it is cheaper to fix it properly now than to "
        "keep patching it. Get one quote and compare what is covered.",
    ),
    "long": (
        "That long is worth a proper repair rather than another workaround.",
        "After that long, ask whether repairing it is still worth it against replacing it: say "
        "the age and what it cost before they quote.",
    ),
}

STANDING_FEELING_REPLIES = {
    "days": (
        "A rough patch like that is not a verdict. Sleep, food and daylight first, and if most "
        "days still feel like that for weeks, that is worth a GP.",
        "A mood that has only just started is not a verdict on anything. Tell one person how it "
        "actually is, and give it a few weeks and some sleep before you read anything into it.",
    ),
    "weeks": (
        "Weeks of feeling like that is worth telling someone — a GP first, and a friend who will "
        "keep asking how you are.",
        "A few weeks of it is the point to say it out loud to a GP rather than waiting for it to "
        "lift on its own.",
    ),
    "months": (
        "Months of feeling like that is the point to ask for help: a GP can refer you for talking "
        "therapy, and you don't have to explain it well to ask.",
        "Months is a long time to carry a mood on your own. Book a longer appointment, say how long "
        "it has been, and ask what is available.",
    ),
    "long": (
        "That long is worth asking for talking therapy by name — a GP can refer you, and it is "
        "there for exactly this.",
        "Years of it is not something to keep managing alone. Say how long it has been, and ask "
        "what help there is.",
    ),
}

ASKED_HOW_LONG = re.compile(
    r"how long (?:has|have|had) (?:it|that|this) been|how long has it been|has it been going on "
    r"long|has it been like this long|how long have you|"
    r"how long (?:has|have|had) (?:\w+ ){1,2}had it|has (?:\w+ ){1,2}had it long|"
    r"how long has (?:\w+ ){1,2}been like (?:that|this)|how bad is (?:\w+ ){1,2}with it|"
    r"is it easing at all", re.I)


TIRED_SAID = re.compile(
    r"\b(?:tired|exhausted|knackered|shattered|wiped|sleepy|bushed|drained|worn out|no energy|"
    r"done in|zonked|pooped|dead on my feet)\b")


def _a_constant_tiredness(clean):
    return bool(TIRED_SAID.search(clean) and TIRED_PERSISTENT.search(clean))


def _standing(clean, memory):
    match = STANDING_LINE.match(clean)
    if not match:
        return None
    length = " ".join(match.group(0).split())
    if re.search(r"\b(?:days?)\b", length):
        bucket = "days"
    elif re.search(r"\bweeks?\b", length):
        bucket = "weeks"
    elif re.search(r"\bmonths?\b", length):
        bucket = "months"
    elif re.search(r"\bsince\b", length) and not re.search(
            r"\b(?:year|years|christmas|summer|winter|spring|autumn|january|february|march|"
            r"april|may|june|july|august|september|october|november|december)\b", length):
        bucket = "days"
    else:
        bucket = "long"
    turns = memory.get("turns") if isinstance(memory, dict) else None
    last_bot = ""
    for turn in reversed(turns or ()):
        if isinstance(turn, dict) and turn.get("bot"):
            last_bot = str(turn.get("bot") or "")
            break
    topic = memory.get("topic") if isinstance(memory, dict) else None
    said = str(topic.get("text") or "") if isinstance(topic, dict) else ""
    subjects = [said] if said else []
    for turn in reversed(turns or ()):
        if isinstance(turn, dict) and turn.get("user"):
            subjects.append(str(turn.get("user") or ""))
            if len(subjects) >= 3:
                break
    about = ""
    for subject in subjects:
        if subject and (_feeling(subject) or _stuck(subject) or SYMPTOM.search(subject)
                        or reads_like_a_symptom(subject)
                        or _a_constant_tiredness(subject)):
            about = subject
            break
    if not about and A_THING_THAT_BREAKS.search(" ".join(subjects)):
        return pick(STANDING_THING_REPLIES[bucket], memory)
    if not (ASKED_HOW_LONG.search(last_bot) or about):
        return pick(STANDING_WHAT_REPLIES[bucket], memory)
    if about and _feeling(about) and bucket in STANDING_FEELING_REPLIES:
        return pick(STANDING_FEELING_REPLIES[bucket], memory)
    return pick(STANDING_REPLIES[bucket], memory)

def _repaired_line(memory):
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if not isinstance(understood, dict):
        return None
    plain = understood.get("plain")
    if not isinstance(plain, str) or not plain.strip():
        return None
    return plain


DONT_KNOW = re.compile(
    r"\b(?:i (?:really |just |honestly )?(?:dont|do not|dnt|dunno) know|dunno|idk|iunno|"
    r"(?:not|no|never|isnt|is not) (?:a |any |too |so )*(?:sure|idea|clue)|"
    r"ha(?:ve|v)ent a clue|i dont have a clue|beats me|god knows)\b")
DONT_KNOW_FILLER = frozenset("""
i im just really so very honestly actually dont do not know no idea sure dunno idk iunno sorry ta
thanks thank you yet right now either though tho oh well hmm um guess a clue havent havent havnt
didnt have dnt dno tbh lol mate tbf god knows beats me a any truly still even then
""".split())


def _says_dont_know(clean, tokens):
    if not tokens or len(tokens) > 12:
        return False
    if not DONT_KNOW.search(clean):
        return False
    return set(tokens) <= DONT_KNOW_FILLER


def claims_instead(text, memory):
    clean = " ".join(str(text or "").lower().split())
    if _a_bare_acknowledgement(clean) and _the_heavy_line(memory):
        return True
    if (portions.an_ask(clean, memory) or portions.a_count_to_fill(clean, memory)
            or portions.a_bare_count_to_fill(clean, memory)):
        return True
    try:
        if tried.pool_for(clean, memory):
            return True
    except Exception:
        pass
    if _a_repair_is_open(memory) and THEY_ARE_NOT_TALKING.search(clean):
        return True
    return bool(REGRET_DEED.search(clean))


CLAIMS_INSTEAD = claims_instead
CHAT_SCATTER = re.compile(
    r"\b(?:i|im|i'm|i am|ive|i've)\b[^.!?]{0,18}\b(?:jump|jumping|jumped|hop|hopping|skip|"
    r"skipping|flit|flitting|dart|darting|bounc\w*)\b[^.!?]{0,12}\b(?:about|around|between)\b|"
    r"\b(?:jump\w*|flit\w*|skip\w*)\s+from\s+(?:one\s+)?thing\s+to\s+(?:the\s+)?"
    r"(?:next|other|another)\b|"
    r"\b(?:i|im|i'm|i am|ive|i've)\b[^.!?]{0,18}\b(?:keep\s+)?chang(?:ing|e|ed)\s+the\s+"
    r"(?:subject|topic)\b|"
    r"\b(?:i|im|i'm|i am|ive|i've)\b[^.!?]{0,18}\b(?:keep\s+)?go(?:ing|ne)?\s+off\s+on\s+one\b|"
    r"\bsorry\b[^.!?]{0,20}\b(?:jump\w*|flit\w*|hop\w*|skip\w*)\b[^.!?]{0,12}"
    r"\b(?:about|around|between)\b")
CHAT_SCATTER_ASKS = re.compile(
    r"\bsorry\b[^.!?]{0,24}\b(?:many|random|daft|silly|stupid|odd|lot\s+of|loads\s+of|"
    r"all\s+(?:these|the|my)|a\s+few)\b[^.!?]{0,12}\bquestions?\b|"
    r"\b(?:hundred|million|loads\s+of|lot\s+of)\s+questions?\b|"
    r"\bsorry\b[^.!?]{0,20}\b(?:to\s+)?keep\s+asking\b|"
    r"\bsorry\b[^.!?]{0,20}\basking\s+you\s+(?:so\s+much|a\s+lot|things)\b")
CHAT_SCATTER_CTX = re.compile(
    r"\bsorry\b|\bapolog\w*\b|\bquestions?\b|\b(?:chat|conversation|talking|asking|"
    r"telling you)\b|\bsubject\b|\btopic\b|\boff on one\b")
CHAT_SCATTER_NOT = re.compile(
    r"\b(?:head|brain|mind|thoughts?|memory|life|sleep|shifts?|jobs?|kids?|children|mum|dad|"
    r"family|wife|husband|partner|work)\b")
CHAT_SCATTER_LEFTOVER = frozenset("""
    the and you your for that this with just its it it's not all any have has had was were are
    sorry apologise apologize apologising asking ask asked told tell said say here there then than
    about around between things thing something anything much very really lot loads few some
    questions question today tonight now again still too so but
    """.split())


def _only_the_apology(clean, match):
    rest = clean[match.end():] if match else clean
    words = [word for word in re.findall(r"[a-z']+", rest) if len(word) > 2]
    return len([word for word in words if word not in CHAT_SCATTER_LEFTOVER]) < 2


CHAT_SCATTER_REPLIES = (
    "Jump about as much as you like - I'm holding {list}. Where do you want to pick up?",
    "No need to apologise, it's your chat. Still on the table: {list}.",
    "Ask in any order you like. I have {list}, so nothing is lost.",
)
CHAT_SCATTER_ALONE = (
    "Jump about as much as you like - I'm keeping the thread, not marking you on it.",
    "No need to apologise. Jump between them as you like and I'll keep track.",
    "That's what I'm here for - carry on in any order.",
)
CHAT_ASKING_REPLIES = (
    "No need to apologise, it's your chat. Still on the table: {list}.",
    "Ask in any order you like. I have {list}, so nothing is lost.",
    "Ask as many as you like - I'm holding {list}, and nothing is lost.",
)
CHAT_ASKING_ALONE = (
    "No need to apologise - asking is what I'm here for.",
    "Ask as many as you like, whenever you like.",
    "None of that needs an apology. Ask away.",
)


def _chat_scatter(clean, memory):
    shape = CHAT_SCATTER.search(clean)
    asks = CHAT_SCATTER_ASKS.search(clean)
    if not (shape or asks):
        return None
    if CHAT_SCATTER_NOT.search(clean) or not CHAT_SCATTER_CTX.search(clean):
        return None
    if not _only_the_apology(clean, shape or asks):
        return None
    if shape:
        with_a_list, alone = CHAT_SCATTER_REPLIES, CHAT_SCATTER_ALONE
    else:
        with_a_list, alone = CHAT_ASKING_REPLIES, CHAT_ASKING_ALONE
    held = thread.on_the_table(memory)
    if len(held) >= 2:
        said = thread.in_a_list(held)
        return pick([option.format(list=said) for option in with_a_list], memory)
    if held or shape:
        return pick(list(alone), memory)
    return None


SAID_WRONG_DEED = "said the wrong thing"
SAID_WRONG = re.compile(
    r"\bi (?:(?:keep|always|still|just|also|often|usually|sometimes|constantly)\s+){0,2}"
    r"(?:said|say|told|tell)\s+(?:the wrong thing|something\s+(?:stupid|awful|daft|silly|"
    r"dumb|mean|horrible|wrong|embarrassing|terrible)|it badly|that badly)\b|"
    r"\bi (?:put|putting|put my)\b[^.]{0,12}\bfoot in it\b|"
    r"\bi (?:really |kind of |sort of )?(?:snapped|shouted|yelled|swore)\s+(?:at|to|with)\s+"
    r"(?:myself|yourself|ourselves)\b|"
    r"\bi (?:was|been|were) (?:rude|horrible|mean|cruel|sharp|short|unfair|awful|dreadful|"
    r"terrible|nasty|unkind) (?:to|with)\b(?! be\b)|"
    r"\bi (?:was|been|were) off with\b|"
    r"\bi (?:upset|offended|insulted|embarrassed|hurt)\s+(?:my|his|her|their|our)\s+"
    r"(?:mum|mom|mam|mother|dad|father|son|daughter|child|kid|baby|partner|husband|wife|"
    r"sister|brother|nan|nana|gran|granny|grandma|grandad|grandpa|aunt|uncle|cousin|friend|"
    r"flatmate|neighbour|neighbor|boss|colleague|team)\b|"
    r"\bi (?:hurt|upset|offended) (?:her|him|them|someone|somebody)(?:'s)? feelings\b|"
    r"\bi (?:said|told)\b[^.]{0,40}\b(?:was|were|is) (?:awful|horrible|stupid|mean|rude|"
    r"unkind|dreadful|terrible|nasty|rubbish|disgusting|pathetic)\b")
SAID_WRONG_NOT = re.compile(
    r"\bi (?:hurt|upset|pulled|broke|twisted|strained|cut|burnt|burned) my\b|"
    r"\bi snapped my\b|\bi said (?:nothing|no|yes|okay|ok|bye|hello|hi)\b")
SAID_WRONG_LOST = re.compile(
    r"\b(?:didnt|didn't|did not|never)\s+(?:get|got|win|won|pass|passed|make|made)\b|"
    r"\b(?:got|been) (?:fired|sacked|dumped|rejected|turned down)\b|"
    r"\bi (?:lost|lose|failed)\b|"
    r"\b(?:she|he|they|we)\s+(?:left|walked out|split|broke up|stopped talking|moved out)\b|"
    r"\b(?:wont|won't|wouldnt|wouldn't) (?:talk|speak) to me\b|"
    r"\bthere'?s no fixing\b|\bit'?s too late\b|\bno longer (?:speaks?|talks?|friends?)\b")
SAID_WRONG_TO_AN_ANIMAL = re.compile(
    r"\b(?:to|with|at)\s+(?:my|our|the|a)\s+(?:dog|cat|puppy|kitten|horse|pony|rabbit|"
    r"hamster|guinea pig|budgie|parrot|pet|fish|bird|chickens?|sheep|cow|goat|lamb)\b")
SAID_WRONG_TO_A_PROFESSIONAL = re.compile(
    r"\b(?:to|at|with)\s+(?:my|our|the)\s+(?:doctor|gp|nurse|consultant|surgeon|midwife|"
    r"health visitor|dentist|orthodontist|physio(?:therapist)?|pharmacist|optician|vet|"
    r"solicitor|accountant|bank|landlord|letting agent)\b[^.?!]*\babout\b")
SAID_WRONG_AT_THEMSELVES = re.compile(
    r"\b(?:to|with|at)\s+(?:myself|yourself|ourselves)\b|"
    r"\bi (?:feel|felt|look|sound|am|'m) (?:like )?(?:such )?(?:an? )?"
    r"(?:idiot|fool|mug|failure|fraud|moron|mess|disgrace)\b")
SAID_WRONG_NEXT = (
    "Pick the moment rather than the words: not mid-argument and not as they walk out. Ask for "
    "two minutes, say the one sentence, and let them answer it.",
    "Say it once and then let them talk. The explaining is what turns a repair back into the row.",
    "Don't ask them to tell you it's fine. Say what you got wrong, then let them be annoyed or "
    "not - that part is theirs.",
    "Ask what they heard. If it is not what you meant, that is the next sentence, and it is worth "
    "saying rather than arguing.",
    "Let what you do next carry it: the few days after matter more than the apology itself.",
)
ASKS_FOR_THE_WORDS = repair.ASKS_FOR_THE_WORDS

ASKS_WHAT_TO_DO = repair.ASKS_WHAT_TO_DO

SAID_WRONG_REPLIES = (
    "Say it sooner than feels comfortable, and name the sentence itself rather than hinting at "
    "it: people forgive a plain \"that came out badly, I didn't mean it\" far more easily than a "
    "vague apology for everything.",
    "Keep it to what you said and that you got it wrong. The explaining is the part that makes "
    "it land as an excuse, so leave it for later, or out.",
    "Own the one sentence, not everything around it: naming the exact thing you regret shows you "
    "heard it, and a general apology mostly sounds like you want it over with.",
    "Most people want to know you noticed, not that you are sorry in general, so go back and say "
    "which bit was wrong. It costs you a minute and it is usually the whole repair.",
    "It is fixable, and the fix is a sentence rather than a gesture. Say the one thing you got "
    "wrong, plainly, and stop there - they can be annoyed while you leave the details alone.",
)

DEED_REPLIES = (
    "Own it before they have to bring it up, and keep it to one sentence: what you did, that "
    "you are sorry, and what you will do instead. The explaining can come later, or not at all.",
    "Say the plain version first - name what you did, say you are sorry, and add no reason "
    "unless they ask for one - then do the small thing you can actually do this week.",
    "The apology is the small part; the change is the rest. Name what you did once, then let the "
    "next few weeks show it rather than repeating it every time you speak.",
    "Put it right sooner than feels comfortable, and name the one thing rather than a list of "
    "everything you feel bad about. People forgive a specific \"I got that wrong\" far more "
    "easily than a general apology for a whole week.",
    "Say what you did, then stop. Adding why is the part that sounds like an excuse, and they "
    "can be annoyed for a bit without you talking them out of it.",
)
LEFT_IT_TOO_LONG_REPLIES = (
    "Do it today, before you explain anything: the call, the visit, the present that is late "
    "arriving. Then say the one line - \"I left it too long and I'm sorry\" - because a reason "
    "offered first sounds like the reason you did not.",
    "Ring rather than message, and lead with them rather than with your week: they have been "
    "waiting, and what they want to hear is that you know it. Put the next one in your phone "
    "before you hang up.",
    "Name the gap once, plainly, and then be there: \"It's been too long and that's on me.\" A "
    "visit or a call booked this week says the rest, and asking them to reassure you costs them "
    "the thing you owe them.",
    "Pick the smallest real thing that ends the gap today - a call on the walk home, a note, a "
    "date in the diary with the day fixed - and do that rather than plan a bigger gesture later.",
)
FORGOT_DATE_REPLIES = (
    "Own it today, and take the sting out of it by naming the day: \"I got the date wrong and "
    "I'm sorry - it isn't that it doesn't matter.\" Then book the thing, because a make-up that "
    "happens this week beats a bigger sorry that stays a plan.",
    "Say it before they have to ask, and don't hide behind the date: \"I knew it was coming and I "
    "still let it pass, and I'm sorry.\" Then do the specific thing - a dinner, a card, a visit - "
    "rather than waiting to be forgiven.",
    "Ring rather than text, and keep it to the one thing: you missed the day, you are sorry, and "
    "here is what you are doing about it. A late card that arrives is worth more than an apology "
    "that asks them to tell you it is fine.",
)
DEED_WORDS = (
    "Name it in one line and stop: \"I let you down over this and I'm sorry - that was my doing.\" "
    "Then the one thing you are doing about it, because a sentence with a next step in it is heard "
    "as meant rather than as sorry-sounding.",
    "Say what you did, that it was yours, and leave why out of the first sentence: \"I got that "
    "wrong and I'm sorry.\" If they ask why, answer it then; before that it arrives as a defence.",
    "Start with the thing they are owed rather than how bad you feel: \"You had every right to be "
    "annoyed with me, and I'm sorry.\" Then ask what would help, and do that one thing.",
    "Keep it short and specific: what you did, that you are sorry, and the change they can see in "
    "the next few weeks. \"I'm sorry - I won't do that again\" is worth more when you name which "
    "\"that\" was.",
)
FORGOT_DATE_WORDS = (
    "\"I missed your birthday and I'm sorry - I'm not going to pretend I was saving it up.\" Say "
    "that on the phone rather than in a message, then ask when they are free this week, so the "
    "next thing after the apology is a date in the diary.",
    "\"I got the day wrong and I've felt rotten about it all week.\" Naming the day is what makes "
    "it land as an oversight rather than as not caring, and it is the one thing they are waiting "
    "to hear.",
    "Lead with the sorry and then the plan: \"I'm sorry I let it go by - I've booked a table for "
    "Friday, if you're free.\" The booking is the apology; asking them to reassure you is not.",
)
AMENDS_REPLIES = (
    "Pick the one thing they would actually notice and do it this week: the visit, the lift they "
    "always ask for, the money paid back, the afternoon spent with the child. Amends is a verb - "
    "what they are owed is the thing made good, not a longer apology.",
    "Say sorry for your part of it in one sentence, then ask them: \"what would help?\" once, and "
    "do that rather than what you would have chosen. Most people want the thing put right, and the "
    "ones who want to say their piece get to say it.",
    "Do it in their language rather than yours: if they tidy and cook, turn up and help with that "
    "rather than buying something. Then keep it up for a few weeks, because the change after the "
    "apology is the part that reads as meant.",
    "Start with the smallest real thing you can finish today - the call you have put off, the "
    "message that says you know you owe them - then tell them what you are doing about the rest "
    "rather than asking them to trust the intention.",
)
FORGOT_DATE_NEXT = (
    "Ring them today rather than waiting for a better moment, and keep it to the three things: you "
    "missed the day, you are sorry, and here is what you are doing about it. Then put the next one "
    "in your phone with a week's warning on it, because the second miss is the one that hurts.",
    "A card and a date beat a longer apology: book something they would like for this week and "
    "tell them the day rather than asking them to choose it. What they are owed now is the thing "
    "made up, not the explaining.",
    "Get the next one right in public: say the sorry once, then let the dinner or the visit do the "
    "rest. Bringing it up again a month later makes them do the forgiving twice.",
)
def _the_deed_pool(deed):
    if deed == "forgot a date":
        return FORGOT_DATE_REPLIES
    if deed == "left it too long":
        return LEFT_IT_TOO_LONG_REPLIES
    return DEED_REPLIES


def _the_words_pool(deed):
    return FORGOT_DATE_WORDS if deed == "forgot a date" else DEED_WORDS


THEY_ARE_NOT_TALKING = re.compile(
    r"\b(?:he|she|they)(?:s|'s|re| is| are|'re)?\s+(?:not|isn'?t|aren'?t|still not|hasnt|"
    r"has not|"
    r"wont|won'?t)\s+(?:speak|speaking|talk|talking|reply|replying|replied|answer|answering|"
    r"answered|call(?:ed|ing)?"
    r"text(?:ed|ing)|messag(?:ed|ing)|been in touch)\b|"
    r"\b(?:he|she|they)(?:s|'s|re| is| are|'re)?\s+(?:giving me the silent|ignoring me|"
    r"blanking me|gone quiet on me)\b")

NOT_TALKING_AFTER_A_REPAIR = (
    "Give them the day, then send one message with no question in it: what you did, that you are "
    "sorry, and that you will be there when they are ready. Asking them to say it is fine is the "
    "part that keeps it going.",
    "Their silence is the answer for now, so do not fill it. Keep the ordinary things going - the "
    "call at the usual time, the lift you promised - and let that, rather than a second apology, "
    "be the thing that says you meant it.",
    "Try once the way they cannot ignore - the phone rather than a text, in person if you can - "
    "then wait. Say the sentence, ask nothing of them, and leave the next move with them: two "
    "apologies in a week sound like you want something back.",
)


DEED_NEXT = (
    "Do it today rather than waiting for a good moment, and in person or on the phone rather than "
    "a text: name the one thing you did, then ask what would help.",
    "Ask what they want from you now and do that rather than what you would choose. People usually "
    "want the thing made good, not a longer apology.",
    "Pick the smallest real thing you can put right this week - the dinner you book, the money you "
    "pay back, the call you make - and do it before you explain anything.",
    "Go back to them rather than round it: say the one sentence you owe them, then leave the next "
    "move with them instead of asking to be told it is fine.",
)


SAID_UNKINDLY = re.compile(
    r"\b(?:said|says|saying|told|tells|shouted|yelled|snapped|swore|swears|texted|messaged)\b"
    r"[^.]{0,30}\b(?P<word>wrong thing|stupid|awful|daft|silly|dumb|mean|horrible|unkind|rude|"
    r"dreadful|terrible|nasty|hurtful|disrespectful)\b")
FEELING_CLAUSE = re.compile(
    r"(?:^|[.;!?]|\band|\bbut|\bso|\bbecause|,)\s*(?:i|we)\s+"
    r"(?:(?:just|really|also|still|honestly|actually|then)\s+)?(?:feel|felt)\s+"
    r"(?:so |very |really |quite |pretty |a bit |kind of |like |such )?$")
SAID_UNKINDLY_REPLIES = (
    "That stings, and it is worse from someone whose opinion you cannot just shrug off. Tell me "
    "what was said and we can work out whether it is worth taking up with them.",
    "Words like that lodge: give it a night before you answer it, and if it is still there "
    "tomorrow, say plainly which bit hurt - people often have no idea.",
    "It is fair to be hurt by that. Say the sentence back to me and we can work out what they "
    "probably meant by it.",
)
SAID_UNKINDLY_FAMILY = (
    "That stings more from family. Tell me what was said and we can work out whether it is "
    "worth taking up with them.",
    "Words like that lodge, especially from family: give it a night before you answer it, and if "
    "it is still there tomorrow, say plainly which bit hurt - people often have no idea.",
    "It is fair to be hurt by that, and harder from someone close. Say the sentence back to me "
    "and we can work out what they probably meant by it.",
)
FAMILY_NAMED = re.compile(
    r"\b(?:mum|mom|mam|mother|dad|father|son|daughter|child|kid|baby|partner|husband|wife|"
    r"sister|brother|nan|nana|gran|granny|grandma|grandad|grandpa|aunt|uncle|cousin|in-laws?|"
    r"family)\b")


def _an_entry_answers_the_deed(clean, memory):
    if deed_of(clean) not in DEEDS_WITH_A_CARD:
        return False
    read = memory.get("understood") if isinstance(memory, dict) else None
    if not isinstance(read, dict):
        return False
    try:
        return lookup.find(read) is not None
    except Exception:
        return False


def _said_wrong(clean):
    if owns_the_deed(clean):
        return True
    if not SAID_WRONG.search(clean) or SAID_WRONG_NOT.search(clean):
        return False
    return not (SAID_WRONG_LOST.search(clean) or SAID_WRONG_TO_AN_ANIMAL.search(clean)
                or SAID_WRONG_TO_A_PROFESSIONAL.search(clean))


I_SAID = re.compile(
    r"\bi (?:(?:keep|keeps|always|still|just|also|then|really|often|usually|sometimes|"
    r"constantly|forever|never)\s+){0,2}(?:said|say|saying|told|tell|telling|admit|admitted)\b")


CLAUSE_BOUNDARY = re.compile(r"[.;!?,]|\band\b|\bbut\b|\bso\b|\bbecause\b|\bthen\b|\bwhich\b")


def _own_deed(clean, start):
    opening = clean[max((b.end() for b in CLAUSE_BOUNDARY.finditer(clean[:start])), default=0):start]
    return bool(FIRST_PERSON_DEED.match(opening) or not opening.strip())


FIRST_PERSON_DEED = re.compile(r"^\s*(?:and\s+|but\s+|so\s+|then\s+|because\s+)?(?:i|we)\b")


def _said_unkindly(clean):
    if _said_wrong(clean) or I_SAID.search(clean):
        return False
    for matched in SAID_UNKINDLY.finditer(clean):
        if FEELING_CLAUSE.search(clean[:matched.start("word")]) \
                and _own_deed(clean, matched.start()):
            continue
        return True
    return False


def respond(text, memory):
    if asks_what_today_is(text):
        return None
    step = plan_steps.carry_on(text, memory) if isinstance(memory, dict) else None
    if step is not None:
        return step
    if not (isinstance(memory, dict) and memory.get("greet")):
        answer = obstacle.answer_for(text, memory)
        if answer is not None:
            return answer
    if not (isinstance(memory, dict) and memory.get("greet")):
        narrowed = ack.a_limit_for_the_plan(text, memory)
        if narrowed is not None:
            return narrowed
    theirs = matters.what_they_say(text, memory)
    if theirs:
        return theirs
    hoped = hope.answer_for(text, memory)
    if hoped:
        return hoped
    resized = another_size.answer_for(text, memory)
    if resized:
        return resized
    reply = _respond(text, memory)
    if reply is None or _the_same_answer_again(reply, memory, text):
        fixed = verdict_reply.the_fix_asked(text, memory)
        if fixed:
            reply = fixed
    if (reply is not None and _the_same_answer_again(reply, memory, text)
            and not (repeat.asks_to_put_it_right(text) and A_REPEAT_LEAD.match(reply))):
        reply = None
    greeted = memory.pop("greet", None) if isinstance(memory, dict) else None
    if greeted:
        if reply is None:
            return _reply("meet", memory, greeted)
        reply = greet_with(greeted, reply)
    if reply is not None:
        return reply
    typed = " ".join(text.lower().split())
    for retry in (_repaired_line(memory), _normalised_line(memory)):
        if retry is None or retry.strip() == typed:
            continue
        if len(_tokens(retry)) > 8:
            continue
        reply = _respond(retry, memory, as_said=False)
        if reply is not None:
            return reply
    return _follow_up_reading(text, memory)


def _a_mood_pool_line(said):
    flat = _words_only(said)
    if not flat:
        return False
    for kind in HEAVY_FEELINGS:
        for line in REPLIES.get(kind) or ():
            if isinstance(line, str) and _words_only(line) == flat:
                return True
    return False


def _a_part_of_the_answer_they_have(clean, memory):
    last = ""
    previous = ""
    for turn in reversed(memory.get("turns") or ()):
        if isinstance(turn, dict):
            if not last and turn.get("bot"):
                last = str(turn["bot"])
            if turn.get("user"):
                previous = " ".join(str(turn["user"]).lower().split())
                break
    if not last.strip():
        return None
    asked = " ".join(str(clean or "").lower().split())
    if asked and previous and (asked == previous or asked in previous):
        return None
    cause = _same_again.the_cause_said_again(last, memory)
    if cause:
        return cause
    from ..memory.narrow import NO_SET_TIME, narrow
    from ..memory.topics import _the_rates_in
    asked_rates = _the_rates_in(clean)
    if asked_rates and not (asked_rates & _the_rates_in(last)):
        return None
    try:
        part = narrow(last, clean)
    except Exception:
        return None
    if not isinstance(part, str) or not part.strip():
        return None
    if " ".join(part.lower().split()) == " ".join(last.lower().split()):
        return None
    if not re.search(r"\d", part) and not part.startswith(NO_SET_TIME):
        return None
    last_rates = _the_rates_in(last)
    if last_rates and not (_the_rates_in(part) & last_rates):
        return None
    return part.strip()


def _the_newest_line_started_the_topic(memory):
    records = memory.get("topics")
    turns = memory.get("turns")
    if not isinstance(records, list) or not records or not isinstance(turns, list):
        return False
    record = records[-1]
    if not isinstance(record, dict):
        return False
    return record.get("turn") == len(turns) - 1

A_VERDICT = re.compile(
    r"\b(?:not an emergency|no emergency|safe to|unsafe|dangerous|harmless|"
    r"(?:fine|ok|okay|all right|alright) (?:to|for|if|on|with)|"
    r"nothing to worry about|no need to worry|don't worry|"
    r"will not (?:hurt|harm|damage)|won't (?:hurt|harm|damage)|"
    r"avoid |stop (?:using|driving|running|eating|taking)|turn (?:it|that) off|"
    r"get (?:it|that|them) (?:looked at|checked|seen)|"
    r"call (?:a|the|your|an|999|111)\b)", re.I)


A_VERDICT_FILLER = frozenset((
    "about", "after", "again", "been", "before", "being", "does", "doing", "have", "just",
    "like", "much", "only", "really", "should", "still", "than", "that", "their", "them",
    "then", "there", "these", "they", "thing", "this", "those", "want", "what", "when",
    "where", "which", "while", "will", "with", "would", "your", "from", "into", "cant",
    "don't", "dont", "isn't", "it's", "thats", "whats", "keep", "keeps", "good", "well",
    "make", "made", "know", "think", "sure", "nothing", "something", "anything", "little",
    "scary", "things", "other", "else", "another", "least", "much", "many", "more", "most",
))
A_DOES_SOMETHING = re.compile(
    r"^\W*(?:pull|wipe|stand|puff|put|keep|use|try|fill|check|clean|open|leave|run|fit|ring|"
    r"call|ask|take|turn|stop|brush|paint|replace|screw|tighten|blot|sprinkle|switch|set|apply|"
    r"cover|wrap|store|throw|bin|soak|rinse|dry|add|mix|stir|heat|cook|bake|boil|ventilate|"
    r"measure|test|look|buy|get|go|hold|sit|wait|drink|eat|sleep|walk|book|insulate|seal|"
    r"scrape|sand|prime|swap|change|drop|pour|lift|hang|tie|lock|close|shake|dust|run|"
    r"do|don't|don|never|always|say|tell|ask|write|sign|send|give|make|find|learn|start|begin|"
    r"decide|choose|pick|plan|arrange|avoid|refuse|accept|agree|join|save|budget)\b", re.I)
A_STATE_WORD = re.compile(
    r"\b(?:usually|normally|often|rarely|seldom|is not|isn't|are not|aren't|never|fine|"
    r"harmless|ordinary|common|uncommon|safe|unsafe|risk|problem|matters?|worr(?:y|ies|ying)|"
    r"ok|okay|worth|needs?|means?|sign of|a sign|because|due to|caused by|comes from)\b",
    re.I)
A_REASSURES = re.compile(
    r"\b(?:won'?t|will not|doesn'?t|does not|don'?t|do not|shall not|need not|"
    r"not going to)\s+(?:\w+\s+){0,3}?"
    r"(?:hurt|harm|damage|sting|bite|chase|bother|attack|spread|kill|poison|burn|"
    r"catch|come back|come to any harm)\b"
    r"|\bnothing to (?:fear|worry about|be afraid of)\b|\bno need to\b", re.I)
A_NEW_CONDITION = re.compile(
    r"\b(?:with|without|on|onto|after|before|during|in|at|from|into|under|beside|instead of|"
    r"for|as)\s+"
    r"(?:a|an|the|my|your|his|her|their|our|this|that|these|those)\s+[a-z]", re.I)
A_ASKS_WHERE = re.compile(
    r"^\W*(?:is|are|was|were|will|would|can|could|do|does|did)\s+"
    r"(?:it|that|this|they|those|these|there)\s+(?:on|in|at|from|near)\b", re.I)
A_WHEN_TO_GET_HELP = re.compile(
    r"\b(?:see (?:a|your|the|an) (?:gp|doctor|nurse|pharmacist|dentist)|call (?:999|111)\b|"
    r"a&e|accident and emergency|get (?:it|that|them) (?:looked at|checked|seen)|"
    r"go to (?:hospital|the hospital)|ring (?:999|111)|same day|straight away)\b", re.I)
ASKS_A_PRICE = re.compile(
    r"\b(?:expensive|pricey|costly|cheap|cheaper|afford|costs?|prices?|pay|paid|worth)\b", re.I)
A_REPEAT_FRAME = re.compile(
    r"\b(?:in what i said above|same answer|same as before|no more than that"
    r"|already (?:said|told)|that is everything i have)\b", re.I)
A_STATE_ASK = re.compile(
    r"^\W*(?:is|are|was|were|does|do|did|will|can|could)\s+"
    r"(?:it|that|this|they|those|these|the|my|a|an)\b", re.I)
ASKS_A_FIGURE = re.compile(
    r"\bhow (?:much|many|long|far|big|often|high|deep|hot|old)\b|\bwhat (?:time|temp|"
    r"temperature|price|size|date|year|gas mark|colour|color)\b|\bwhich (?:year|date)\b|\bwhen\b",
    re.I)


def _the_verdict_in(clean, memory):
    asked = " ".join(str(clean or "").lower().split())
    if not asked or not EVERY_YES_NO_OPEN.match(asked) or ASKS_A_FIGURE.search(asked):
        return None
    if A_NEW_CONDITION.search(asked):
        return None
    if A_ASKS_WHERE.search(asked):
        return None
    last = ""
    previous = ""
    for turn in reversed(memory.get("turns") or ()):
        if isinstance(turn, dict):
            if not last and turn.get("bot"):
                last = str(turn["bot"])
            if turn.get("user"):
                previous = " ".join(str(turn["user"]).lower().split())
                break
    if not last.strip():
        return None
    if previous and (asked == previous or asked in previous):
        return None
    sentences = [" ".join(one.split()) for one in re.split(r"(?<=[.!?])\s+", last.strip())]
    for said in sentences[1:]:
        if len(said.split()) < 4 or not A_VERDICT.search(said):
            continue
        if A_WHEN_TO_GET_HELP.search(said):
            continue
        return said if said.endswith((".", "!", "?")) else said + "."
    if ASKS_A_PRICE.search(asked):
        return None
    if A_REPEAT_FRAME.search(last):
        return None
    if not A_STATE_ASK.match(asked):
        return None
    named = frozenset(word for word in re.findall(r"[a-z']{4,}", previous)
                      if word not in A_VERDICT_FILLER)
    for said in sentences[1:3]:
        if len(said.split()) < 4:
            continue
        if A_DOES_SOMETHING.match(said) or not (A_STATE_WORD.search(said)
                                                or A_REASSURES.search(said)):
            continue
        if named.intersection(re.findall(r"[a-z']{4,}", said.lower())):
            return said if said.endswith((".", "!", "?")) else said + "."
    return None


def _a_topic_still_in_this_exchange(topic, memory):
    records = memory.get("topics") if isinstance(memory, dict) else None
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(records, list) or not isinstance(turns, list):
        return False
    for record in reversed(records):
        if not isinstance(record, dict):
            continue
        if " ".join(str(record.get("text") or "").lower().split()) != topic:
            continue
        began = record.get("turn")
        if not isinstance(began, int):
            return False
        return len(turns) - began <= 3
    return False


def _follow_up_reading(text, memory):
    if _safety_thread(memory) or _reads_as_distress(text):
        return None
    verdict = _the_verdict_in(text, memory)
    if verdict:
        return verdict
    if not _bare_ask(text):
        return None
    from ..memory.narrow import NO_SET_TIME
    part = _a_part_of_the_answer_they_have(text, memory)
    if part and part.startswith(NO_SET_TIME):
        return part
    if isinstance(memory.get("understood"), dict) and memory["understood"].get("about_bot_kind"):
        return None
    if isinstance(memory.get("understood"), dict) and memory["understood"].get("someone_new"):
        return None
    from ..memory.topics import context as _topic_context
    from ..memory.topics import a_stay_with_the_place as _a_stay_with_the_place
    from ..memory.topics import asks_how_long_to_stay as _asks_how_long_to_stay
    from ..memory.topics import the_city_of as _the_city_of
    clean = " ".join(text.lower().replace("\u2019", "'").split())
    topics_said = [" ".join(str(line or "").lower().split())
                   for line in reversed(_topic_context(memory, 3))]
    recent_said = [" ".join(str(turn.get("user") or "").lower().split())
                   for turn in (memory.get("turns") or [])[-3:] if isinstance(turn, dict)]
    if (isinstance(memory.get("understood"), dict)
            and memory["understood"].get("kind") == "question"
            and any(_NO_REASON.match(line) for line in (*topics_said, *recent_said))):
        return None
    if topics_said and _nothing_was_heard(memory, topics_said[0]):
        return None
    if any(_reads_as_distress(topic) for topic in topics_said):
        return None
    readings = []
    for topic in topics_said:
        if not topic or topic == clean or names_nothing(topic):
            continue
        if _names_its_own_thing(text, topic):
            continue
        stay = _a_stay_with_the_place(clean, topic)
        if stay is not None:
            readings.append((topic, stay))
        elif _asks_how_long_to_stay(clean) and _the_city_of(topic):
            continue
        else:
            readings.append((topic, topic + " " + clean))
    if not readings:
        return None
    from . import answers as _answers
    from ..understanding import understand as _understand
    carries_past_the_newest = names_nothing(clean) and (
        not topics_said or names_nothing(topics_said[0])
        or not _the_newest_line_started_the_topic(memory))
    for index, (topic, reading) in enumerate(readings):
        if index and not carries_past_the_newest:
            return None
        if reading == clean:
            continue
        reading_memory = copy.deepcopy(memory)
        reading_memory["understood"] = _understand(reading, reading_memory)
        reading_memory["joined_read"] = True
        said = _answers.respond(reading, reading_memory)
        if not said or _said_before(said, memory):
            if memory.get("entry_answer") or memory.get("entry_answers"):
                part = _a_part_of_the_answer_they_have(clean, memory)
                if part:
                    return part
                continue
            said = _respond(reading, reading_memory)
            current = memory.get("understood") if isinstance(memory, dict) else None
            if (said and isinstance(current, dict) and current.get("kind") == "question"
                    and _a_mood_pool_line(said)):
                said = None
            if said and _says_nothing_about_the_ask(said):
                said = None
        if not said:
            continue
        if _said_before(said, memory) or _said_before(_same_again.unframed(said) or said, memory):
            part = _a_part_of_the_answer_they_have(clean, memory)
            if part:
                return part
            if index == 0 and topics_said[1:2] and _a_topic_still_in_this_exchange(
                    topics_said[1], memory):
                continue
            return None
        if not _says_the_kind(clean, said):
            return None
        if _asks_what_they_said(said, memory):
            continue
        if not _about_the_topic(reading, reading_memory, topic):
            continue
        return said
    return None


DISTRESS = re.compile(
    r"\b(?:had\s+enough\s+of\s+(?:living|life|it\s+all|everything|being\s+here)|"
    r"enough\s+of\s+living|end\s+it\s+all|end\s+my\s+life|kill\s+myself|killing\s+myself|"
    r"not\s+worth\s+living|worth\s+living|want\s+to\s+die|wanna\s+die|"
    r"no\s+reason\s+to\s+(?:live|go\s+on|carry\s+on)|nothing\s+to\s+live\s+for|"
    r"no\s+point\s+in\s+(?:anything|going\s+on|carrying\s+on|living)|"
    r"no\s+point\s+(?:going\s+on|carrying\s+on|living)|"
    r"better\s+off\s+dead|better\s+off\s+without\s+me|tired\s+of\s+living|"
    r"can'?t\s+go\s+on|don'?t\s+want\s+to\s+be\s+here|dont\s+want\s+to\s+be\s+here|"
    r"hurt\s+myself|self[\s-]?harm|suicid\w*|take\s+my\s+own\s+life|"
    r"don'?t\s+want\s+to\s+wake\s+up|dont\s+want\s+to\s+wake\s+up)\b", re.I)


def _reads_as_distress(line):
    return bool(DISTRESS.search(" " + " ".join(str(line or "").lower().split()) + " "))


HEARD_NOTHING = frozenset(("greeting",))


def _nothing_was_heard(memory, topic):
    turns = memory.get("turns")
    records = memory.get("topics")
    if not isinstance(turns, list) or not isinstance(records, list):
        return False
    for record in reversed(records):
        if not isinstance(record, dict):
            continue
        if " ".join(str(record.get("text") or "").lower().split()) != topic:
            continue
        index = record.get("turn")
        if not isinstance(index, int) or not 0 <= index < len(turns):
            return False
        turn = turns[index] if isinstance(turns[index], dict) else {}
        return turn.get("module") in HEARD_NOTHING
    return False


TIME_ASK = re.compile(r"\bhow long\b|\bwhen did\b|\bsince when\b", re.I)


def _asks_what_they_said(said, memory):
    if not TIME_ASK.search(str(said or "")):
        return False
    from ..compose.trouble import DURATION as _DURATION
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in reversed(turns if isinstance(turns, list) else []):
        if not isinstance(turn, dict):
            continue
        line = " ".join(str(turn.get("user") or "").lower().split())
        if line and _DURATION.search(" " + line + " "):
            return True
    return False


TOPIC_WORD = re.compile(r"[a-z]+")



def _the_entrys_own_name(item):
    key = getattr(item, "key", ()) or ()
    first = key[0] if key else ""
    options = (first,) if isinstance(first, str) else tuple(first or ())
    found = set()
    for option in options:
        for word in str(option).lower().split():
            found.add(word.rstrip("s") or word)
    return found


def _about_the_topic(reading, memory, topic):
    from ..knowledge import lookup as _lookup
    from ..understanding import understand as _understand
    item = _lookup.find(_understand(reading, copy.deepcopy(memory)))
    if item is None:
        return True
    said = {word.rstrip("s") or word for word in TOPIC_WORD.findall(topic)}
    read = _understand(topic, copy.deepcopy(memory))
    subject = read.get("subject")
    named = {word.rstrip("s") or word for word in TOPIC_WORD.findall(str(subject or ""))}
    if _lookup.key_words(item) & named:
        return True
    name = _the_entrys_own_name(item)
    things = {word.rstrip("s") or word
              for entity in (read.get("entities") or [])
              if str(entity.get("type") or "") in ("thing", "person")
              for word in TOPIC_WORD.findall(str(entity.get("text") or ""))}
    asked = {word.rstrip("s") or word for word in TOPIC_WORD.findall(reading)} - said
    return bool(name & (things - asked))


NOT_AN_ANSWER = ("intent", "opening", "vague", "busy")


def _says_nothing_about_the_ask(said):
    return any(said in REPLIES[kind] for kind in NOT_AN_ANSWER if kind in REPLIES)


QUESTION_OPEN = re.compile(r"^\W*(?:how|what|which|when|where|who|why)(?:'s|s)?\b")
YES_NO_OPEN = re.compile(r"^\W*(?:can|could|would|should)\b")
EVERY_YES_NO_OPEN = re.compile(r"^\W*(?:can|could|would|should|is|are|was|were|am|do|does|did|"
                               r"will|shall|has|have|isn't|aren't|wasn't|weren't|don't|doesn't|"
                               r"didn't|won't|shan't|can't|cannot|couldn't|wouldn't|shouldn't|"
                               r"must)\b")
YES_NO_WORDS = 5
OFFERING = re.compile(r"^\W*(?:what|how)s?\s+about\b")
OWN_THING = re.compile(r"\b(?:my|our|his|her|their)\s+([a-z]{2,})")
LOOKING_FOR = re.compile(r"^\W*where(?:'s|s| is| are| was| were)\b")
FOUND_THING = re.compile(r"\b(?:the|this|that|these|those|your)\s+([a-z]{2,})")
NOT_A_THING = frozenset("""best worst first last same other rest next whole only most least right
wrong near far point idea thing things way ways time times lot end start top bottom left side
kind sort bit piece one ones amount number reason chance rate rates price prices cost costs fee
fees charge charges total value balance interest worth percentage percent term length duration size
weight height depth day days week weeks month months year years hour hours minute minutes
morning afternoon evening night weekend""".split())
AN_ARTICLE = re.compile(r"\b(?:a|an|the)\s+([a-z]{2,})")
ASKS_ABOUT_A_THING = re.compile(
    r"^\W*(?:how\s+(?:much|many|long|far|often|old|big|heavy|tall|warm|cold|deep|high)"
    r"|where(?:'s|s)?|when(?:'s|s)?|what\s+(?:price|size|weight)\b)")
ASKS_WHAT_TO_DO_WITH = re.compile(
    r"^\W*(?:what|how)(?:'s|s)?\s+(?:can|should|shall|do|could|would)\s+(?:i|we|you)\s+"
    r"(?:do|make|cook|have|eat|use)\b")
A_CONTAINER = frozenset("""can cans tin tins packet packets bottle bottles box boxes cup cups
    glass glasses mug mugs slice slices piece pieces portion portions bag bags loaf tin tub jar
    jars carton litre liter pint ounce gram grams kilo handful spoon spoons bowl plate""".split())


def _names_its_own_thing(text, topic=""):
    clean = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    named = OWN_THING.findall(clean)
    if LOOKING_FOR.match(clean):
        named += [word for word in FOUND_THING.findall(clean) if word not in NOT_A_THING]
    if (not named and ASKS_ABOUT_A_THING.match(clean) and not OFFERING.match(clean)
            and not ASKS_WHAT_TO_DO_WITH.match(clean)):
        named += [word for word in AN_ARTICLE.findall(clean)
                  if word not in NOT_A_THING and word not in A_CONTAINER]
    if not named:
        return False
    said = set(re.findall(r"[a-z']+", str(topic or "").lower()))
    bare = {word.rstrip("s") for word in said}
    return not any(word in said or word.rstrip("s") in bare for word in named)


def _bare_ask(text):
    clean = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    words = clean.split()
    if len(words) > 8:
        return False
    if OFFERING.match(clean):
        return False
    if QUESTION_OPEN.match(clean):
        return True
    return bool(YES_NO_OPEN.match(clean)) and len(words) <= YES_NO_WORDS


def _words_only(text):
    return " ".join(re.sub(r"[^0-9a-z]+", " ", str(text or "").lower()).split())


A_SHORT_LINE = 5


A_REPEAT_LEAD = re.compile(r"^[^:]{0,80}:\s*")


def _the_same_answer_again(said, memory, line=""):

    if meant.reads_it(line):
        return False
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return False
    if len(" ".join(str(line or "").split()).split()) > A_SHORT_LINE:
        return False
    flat = _words_only(said)
    if len(flat.split()) < 12:
        return False
    typed = str(said or "").lower()
    if any(typed.startswith(lead) for lead in MEANT_LEADS):
        return False
    readings = [flat]
    lead = A_REPEAT_LEAD.match(str(said or ""))
    if lead:
        after = _words_only(str(said)[lead.end():])
        if len(after.split()) >= 12:
            readings.append(after)
    for turn in turns[-4:]:
        bot = turn.get("bot") if isinstance(turn, dict) else None
        if not isinstance(bot, str):
            continue
        was = _words_only(bot)
        for reading in readings:
            if was == reading or (len(was.split()) > len(reading.split())
                                  and was.startswith(reading)):
                return True
    return False


def _said_before(said, memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return False
    said = " ".join(str(said or "").split())
    if not said:
        return True
    flat = _words_only(said)
    if not flat:
        return True
    pieces = [_words_only(piece) for piece in re.split(r"(?<=[.!?])\s+", said)]
    pieces = [piece for piece in pieces if len(piece.split()) >= 4]
    for turn in turns:
        if not isinstance(turn, dict):
            continue
        bot = " ".join(str(turn.get("bot") or "").split())
        if not bot:
            continue
        said_bot = _words_only(bot)
        if not said_bot:
            continue
        if flat == said_bot:
            return True
        if len(said_bot.split()) >= 4 and (flat in said_bot or said_bot in flat):
            return True
        if any(piece in said_bot for piece in pieces):
            return True
    return False


def _says_the_kind(ask, said):
    from ..memory.narrow import SPANS as _SPANS, kind_of as _kind_of
    kind = _kind_of(ask)
    if kind is None or kind not in _SPANS:
        return True
    return bool(_SPANS[kind].search(str(said or "")))


WORK_PERSON = re.compile(
    r"\bmy\s+(?:boss|manager|line manager|supervisor|team leader|colleague|coworker|"
    r"co-worker|team)\b", re.I)
WORK_FAULT = re.compile(
    r"\b(?:is|are|was|were|keeps?|kept|has been|have been|always|still)\b[^.!?]{0,24}?"
    r"\b(?:annoying|horrible|awful|difficult|rude|dismissive|unhelpful|unfair|useless|moody|"
    r"snappy|patronising|patronizing|picky|nitpicking|nitpicky|impossible|cold|off with me|"
    r"having a go|on my back|on at me|picking on me|getting at me|watching everything|"
    r"breathing down my neck|finding fault|blaming me|undermining me|ignoring me|"
    r"leaving me out|shouting at me|talking down to me|taking the credit|taking credit)\b",
    re.I)
WORK_ASK = re.compile(
    r"\?|\b(?:what|how|should|could|can|would|who)\b[^.!?]{0,24}\b(?:i|we)\b",
    re.I)
WORK_UNSEEN = re.compile(
    r"\b(?:feel|feeling|felt)\s+(?:so\s+|really\s+|quite\s+|a bit\s+|like\s+)?"
    r"(?:invisible|unheard|unappreciated|undervalued|ignored|taken for granted|nobody notices me|"
    r"i (?:don'?t|do not|dont) matter)\b"
    r"|\bnobody\s+(?:at work\s+)?(?:ever\s+)?(?:notices|thanks|appreciates|says anything nice "
    r"about)\b[^.!?]{0,20}\b(?:what i do|me|my work)\b",
    re.I)
WORK_CONTEXT = re.compile(
    r"\b(?:at|in)\s+(?:work|the office|the job|my job|my team|the team)\b"
    r"|\bby\s+my\s+(?:boss|manager|team|colleagues?)\b", re.I)
WORK_RELATIVE = re.compile(r"\bwhat i (?:do|did|have done)\b|\bhow i feel\b", re.I)
WORK_GRUMBLE = (
    "That wears a person down, and it is not you being thin-skinned. Has it always been like "
    "this, or is it new?",
    "It is the small ones that grind you down more than any one big thing. What was the last one?",
    "Worth saying it once, plainly, to them rather than about them: what they did, and what you "
    "want instead.",
    "Grin and bear it is the usual advice and it is bad advice. Is there anyone at work you can "
    "say it to?",
)


WORK_UNSEEN_REPLY = (
    "That wears a person down, and it is not you being thin-skinned. Has it always been like "
    "this, or is it new?",
    "Being the one nobody notices is its own kind of tiring. Is there one person there who would "
    "hear it, if you said it plainly?",
    "Grin and bear it is the usual advice and it is bad advice. Is there anyone at work you can "
    "say it to?",
    "Worth saying once, to the person who should have noticed: what you actually did, and what "
    "you want to be different.",
)


def _work_grumble(clean, tokens, memory):
    if len(tokens) < 4 or " but " in clean or _safety_thread(memory):
        return None
    a_fault = WORK_PERSON.search(clean) and WORK_FAULT.search(clean)
    unseen = WORK_UNSEEN.search(clean) and WORK_CONTEXT.search(clean)
    if not (a_fault or unseen):
        return None
    if WORK_ASK.search(WORK_RELATIVE.sub(" ", clean)):
        return None
    if _answers_knows(clean, memory):
        return None
    return pick(WORK_UNSEEN_REPLY if unseen and not a_fault else WORK_GRUMBLE, memory, clean)


LAUGH_REPORT = re.compile(
    r"\bcrack(?:ing|ed|s)?\s+(?:me\s+)?up\s+(?:at|over|when|while|watching|reading)\b|"
    r"\bcrack(?:ed|s)\s+me\s+up\b|"
    r"\bin\s+stitches\b|"
    r"\bin\s+bits\s+(?:at|over|watching|reading|when)\b|"
    r"\b(?:crying|died|dying|nearly\s+died|almost\s+died|wet(?:ting)?\s+myself)\s+laughing\b|"
    r"\blaughing\s+(?:so\s+hard|hysterically|uncontrollably|my\s+head\s+off)\b|"
    r"\b(?:can'?t|cant|couldn'?t|could\s+not)\s+stop\s+laughing\b|"
    r"\blost\s+it\s+laughing\b|"
    r"\bhowl(?:ing|ed)\s+(?:at|with)\b|"
    r"\bwheez(?:ing|ed)\s+(?:with\s+laughter|laughing|at)\b")
LAUGH_TOGETHER = re.compile(
    r"\b(?:we|us|they)\b[^.?!]{0,40}?\b(?:were|was|are|re)\s+(?:all\s+)?crack(?:ing|ed)\s+up\b|"
    r"\b(?:everyone|everybody)\b[^.?!]{0,40}?\b(?:was|were|is|are)?\s*(?:all\s+)?crack(?:ing|ed)\s+up\b|"
    r"\bthe\s+(?:whole\s+)?(?:office|team|class|family|lot|group|pub|house|household|staff|"
    r"crew|year|form)\b[^.?!]{0,40}?\b(?:were|was)\s+(?:all\s+)?crack(?:ing|ed)\s+up\b|"
    r"\bme\s+and\s+(?:my\s+)?\w+\b[^.?!]{0,30}?\b(?:were|was)\s+(?:all\s+)?crack(?:ing|ed)\s+up\b")
LAUGH_TOGETHER_NOT = re.compile(
    r"\b(?:pressure|strain|stress|weight|workload|load)\b")
LAUGH_MINE = re.compile(r"\b(?:i|im|i'm|ive|i've|we|we're|weve|we've|me)\b")
LAUGH_AT_ME = re.compile(r"\b(?:at|over|about)\s+(?:me|us|my\s+\w+)\b")
LAUGH_NOT_A_PERSON = re.compile(
    r"\b(?:dog|dogs|cat|cats|puppy|pup|fox|foxes|wolf|wolves|baby|babies|kid|kids|child|"
    r"toddler|bird|seagull|crow|owl|alarm|kettle|wind|siren|engine)\b")
LAUGH_BAD_SETTING = re.compile(
    r"\b(?:funeral|wake|burial|grave|hospital|ward|hospice|surgery|operation|ambulance|a&e|"
    r"nurse|doctor|vet|terminal|chemo|diagnosis)\b")


def _laughing_at(clean, memory=None):
    if not isinstance(clean, str) or "?" in clean:
        return None
    together = bool(LAUGH_TOGETHER.search(clean)) and not LAUGH_TOGETHER_NOT.search(clean)
    if not LAUGH_REPORT.search(clean) and not together:
        return None
    if LAUGH_AT_ME.search(clean) or LAUGH_BAD_SETTING.search(clean):
        return None
    if not together and not LAUGH_MINE.search(clean):
        return None
    if LAUGH_NOT_A_PERSON.search(clean) and re.search(r"\bhowl", clean):
        return None
    if reads_as_bad_news(clean):
        return None
    if isinstance(memory, dict):
        memory["laughed"] = len(memory.get("turns") or [])
    return "laughing"



def _the_condolence_is_the_last_thing(memory):
    if not isinstance(memory, dict):
        return False
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return False
    last = turns[-1]
    if str(last.get("module") or "") in ("loss", "grief"):
        return True
    if " ".join(str(last.get("bot") or "").split()) in loss_reading.AFTER_REPLIES:
        return True
    return bool(loss_reading.reads_as_loss(str(last.get("user") or "")))


LAUGH_CARRIED_ON = re.compile(
    r"\b(?:couldn'?t|could\s+not|can'?t|cant)\s+(?:breathe|breathe\s+properly)\b|"
    r"\b(?:couldn'?t|could\s+not|can'?t|cant)\s+(?:stop\s+laughing|stop\s+it|keep\s+a\s+straight\s+face)\b|"
    r"\b(?:sides?|ribs?|face|cheeks?)\s+(?:hurt|ache|aching|are\s+sore)\b|"
    r"\bmy\s+(?:sides?|ribs?|face|cheeks?)\b|"
    r"\b(?:still|proper)\s+laughing\b|\bstill\s+going\b|"
    r"\b(?:nearly|almost)\s+choked\b|\bim\s+dead\b|\bim\s+gone\b|"
    r"\bim\s+(?:still\s+)?crying\s+(?:with|from)\s+(?:the\s+)?laugh\w*\b|"
    r"\b(?:laughed|giggled)\s+until\s+i\s+cried\b|\bcried\s+laughing\b")
LAUGH_CARRIED_ON_NOT = re.compile(
    r"\bcry(?:ing|cried)?\b|\btears\b|\bsob(?:bing|bed)?\b|\bwept\b|"
    r"\bupset\b|\bsad\b|\bscared\b|\bafraid\b|\bpanick\w*\b|\banxious\b|"
    r"\ball\s+night\b")
LAUGH_CARRIED_ON_REPLY = (
    "Ha, that good? I hope the ribs recover.",
    "That is a proper laugh when it gets your ribs.",
    "Ha - worth it. That is the kind of thing you tell people about.",
)


def _laughing_still(clean, memory):
    if not isinstance(memory, dict):
        return None
    was = memory.get("laughed")
    if not isinstance(was, int) or isinstance(was, bool):
        return None
    if len(memory.get("turns") or []) != was + 1:
        return None
    if not isinstance(clean, str) or "?" in clean or not LAUGH_CARRIED_ON.search(clean):
        return None
    if (reads_as_bad_news(clean) or LAUGH_BAD_SETTING.search(clean)
            or LAUGH_CARRIED_ON_NOT.search(clean)):
        return None
    return pick(LAUGH_CARRIED_ON_REPLY, memory, clean)


SOMEBODY_THINKS = re.compile(
    r"\b(?:my|our|the)\s+(?P<who>[a-z]+)\s+"
    r"(?:thinks|says|reckons|insists|keeps\s+saying)\s+(?:that\s+)?"
    r"(?:i|we)\s+(?:should|ought\s+to|need\s+to|have\s+to|must)\s+(?P<named>[a-z][a-z' ]{2,70})"
    r"[.!,]*$", re.I)
EVERYONE_THINKS = re.compile(
    r"\b(?P<who>everyone|everybody|people|my\s+mates|my\s+family)\s+"
    r"(?:keeps?\s+)?(?:tells?\s+me|telling\s+me|says?)\s+(?:that\s+)?"
    r"(?:i|we)\s+(?:should|ought\s+to|need\s+to|have\s+to)\s+(?P<named>[a-z][a-z' ]{2,70})"
    r"[.!,]*$", re.I)
THEIR_OPINION_IS_A_HEALTH_MATTER = re.compile(
    r"\b(?:doctor|gp|nurse|hospital|a&e|casualty|999|111|ambulance|checked|check\s+it|scanned|"
    r"scan|tested|test|operation|surgery|tablet|tablets|medicine|meds|medication|pill|pills|"
    r"diet|weight|smoking|smoke|drink|drinking|alcohol|counselling|therapist|antidepressants)\b",
    re.I)
THINKS_REPLIES = (
    "That is {who}'s idea for your life, not a decision you have made. It is your call, and no "
    "is a whole answer.",
    "Easy advice to give from outside. You are the one who would live with it, so decide it on "
    "what you want.",
    "You can hear {who} out and still not do it. What matters is what you want, not what sounds "
    "sensible to them.",
    "It is your life and your call. {who_cap} thinking it does not make it a plan.",
    "Nobody else has to live with it. Take the thought seriously if it helps and drop it if it "
    "does not - either way it is yours to decide.",
)


def _somebody_thinks_i_should(clean):
    text = " ".join(str(clean or "").lower().split())
    if not text or "?" in text or len(text.split()) > 26:
        return None
    found = SOMEBODY_THINKS.search(text) or EVERYONE_THINKS.search(text)
    if not found:
        return None
    who = " ".join(found.group("who").split())
    named = " ".join(found.group("named").split()).strip(" .,!")
    if not named or len(named.split()) > 10:
        return None
    if THEIR_OPINION_IS_A_HEALTH_MATTER.search(text):
        return None
    return who, named


def _thinks_pool(who):
    if who not in ("everyone", "everybody", "people") and not who.startswith("my "):
        who = "your " + who
    return [line.format(who=who, who_cap=who[0].upper() + who[1:]) for line in THINKS_REPLIES]


A_REPORT_A_THING = re.compile(
    r"\b(?:(?:my|our|the)\s+[a-z]+|everyone'?s?|everybody'?s?|people|someone|somebody|"
    r"a\s+(?:friend|mate|colleague|bloke|girl)(?:\s+of\s+(?:mine|ours))?|friends?)\s+"
    r"(?:says?|said|keeps?\s+saying|was\s+saying|told\s+me|tells\s+me|swears?\s+by|"
    r"swore\s+by|raves?\s+about|"
    r"raving\s+about|went\s+on\s+about|goes\s+on\s+about|wont\s+shut\s+up\s+about|"
    r"won't\s+shut\s+up\s+about|keeps?\s+going\s+on\s+about|put\s+me\s+onto)\b"
    r"(?P<rest>[^?]{2,90})", re.I)
A_HEARD_A_THING = re.compile(
    r"\b(?:i\s+heard|i'?ve\s+heard|i\s+was\s+told|i'?ve\s+been\s+told|apparently|"
    r"word\s+is|heard|they\s+say|rumour\s+is|rumor\s+is)\b(?P<rest>[^?]{2,90})", re.I)
A_PRAISING_VERB = re.compile(
    r"\b(?:swears?\s+by|swore\s+by|raves?\s+about|raving\s+about|went\s+on\s+about|"
    r"goes\s+on\s+about|keeps?\s+going\s+on\s+about|wont\s+shut\s+up\s+about|"
    r"won't\s+shut\s+up\s+about|put\s+me\s+onto|(?:heard|says?|said|tell\w*\s+me)\s+"
    r"(?:good|great|brilliant|amazing)\s+things\s+about)\b", re.I)
A_ASKED_NOT_TOLD = re.compile(
    r"^\s*(?:does|do|did|is|are|was|were|has|have|had|would|will|can|could|should|who|why|"
    r"any(?:one|body))\b", re.I)
A_PRAISE_OF_A_THING = re.compile(
    r"\b(?:is|are|was|were|seems|sounds)\s+(?:really\s+|so\s+|apparently\s+|meant\s+to\s+"
    r"be\s+|supposed\s+to\s+be\s+)?(?:good|great|amazing|brilliant|excellent|lovely|"
    r"fantastic|unreal|incredible|the\s+best|worth\s+it|worth\s+a\s+(?:go|look|visit))\b"
    r"|\b(?:you'?d|you\s+would|you'?ll|you\s+will|id|i'?d|i\s+would)\s+(?:really\s+|"
    r"absolutely\s+)?(?:like|love|enjoy)\b"
    r"|\b(?:is|are)\s+(?:meant|supposed)\s+to\s+be\b", re.I)
A_RECOMMENDATION_IS_NOT = re.compile(
    r"\b(?:should|ought|need\s+to|have\s+to|must|make\s+sure|better\s+off|stop|give\s+up|"
    r"doctor|gp|nurse|hospital|999|111|tablet|tablets|medicine|medication|pill|pills|dose|"
    r"antibiotics|checked|check\s+it|scan|test|tested|operation|surgery|injur\w*|symptom\w*|"
    r"bleeding|pain|hurt|sore|fever|rash|pregnant|pregnancy|contagious|infection)\b", re.I)
SECONDHAND_PRAISE_REPLIES = (
    "Worth a look, then. What did they say was so good about it?",
    "Word of mouth is the best kind of recommendation. Is it your sort of thing?",
    "That is one to keep in mind. What made it stick with you?",
    "Praise from someone you know counts for more than a review. What is the draw?",
    "Second-hand or not, that is a good sign. What did they like most about it?",
)


def _somebody_recommended_a_thing(clean):
    text = " ".join(str(clean or "").lower().replace("\u2019", "'").split())
    if not text or "?" in text or len(text.split()) > 24:
        return None
    found = A_REPORT_A_THING.search(text) or A_HEARD_A_THING.search(text)
    if not found:
        return None
    rest = " ".join(found.group("rest").split()).strip(" .,!")
    if not rest or len(rest.split()) > 12:
        return None
    if A_ASKED_NOT_TOLD.search(text):
        return None
    if not A_PRAISING_VERB.search(text) and not A_PRAISE_OF_A_THING.search(rest):
        return None
    if re.search(r"\b(?:told|tells?)\s+me\s+to\b", text):
        return None
    if re.search(r"\bi(?:'m|\s+am)\b", rest):
        return None
    if A_RECOMMENDATION_IS_NOT.search(rest):
        return None
    return rest


def _respond(text, memory, as_said=True):

    planned = occasionplan.reply_for(text, memory)
    if planned is not None:
        return planned

    clean = " ".join(text.lower().replace("’", "'").split())
    clean = badnews.without_the_figure_of_speech(clean)
    clean = _without_the_might(clean)
    tokens = _tokens(text)
    if not tokens:
        return None
    if _asked_how_it_went(clean):
        return None
    still_in = tried.in_care_pool(clean, memory)
    if still_in:
        return pick(still_in, memory)
    news_detail = a_detail_of_the_news(clean, memory)
    if news_detail and not _a_death_just_said(memory):
        said_detail = " ".join(clean.split())
        return _say("more_of_the_news" if news_detail == "attempt" else
                    "more_of_the_news_arrival" if news_detail == "arrival" else
                    "more_of_the_news_score", memory,
                    X=said_detail[:1].upper() + said_detail[1:])
    if SOMEONE_BRING_SOMEONE.search(clean):
        record = about_the_person(memory) if isinstance(memory, dict) else None
        if record and record.get("trouble") == "hospital":
            return None
    doubt = _a_doubt_about_being_taken_on(clean, memory)
    if doubt:
        return doubt
    aged = _the_age_in_a_work_thread(clean, memory)
    if aged:
        return aged
    if amends_to(clean):
        return pick(AMENDS_REPLIES, memory, clean)
    if _a_repair_is_open(memory) and THEY_ARE_NOT_TALKING.search(clean):
        return pick(NOT_TALKING_AFTER_A_REPAIR, memory, clean)
    if _after_a_repair(memory) and ASKS_FOR_THE_WORDS.search(clean):
        deed = _the_deed_before(memory)
        if deed != SAID_WRONG_DEED:
            return pick(_the_words_pool(deed), memory, clean)
    if _after_a_repair(memory) and ASKS_WHAT_TO_DO.search(clean):
        if _the_deed_before(memory) == SAID_WRONG_DEED:
            return pick(SAID_WRONG_NEXT, memory, clean)
        return pick(DEED_NEXT, memory, clean)
    if _said_wrong(clean):
        if SAID_WRONG_AT_THEMSELVES.search(clean):
            return pick(AT_MYSELF_REPLIES, memory, clean)
        deed = deed_of(clean)
        if deed and deed != SAID_WRONG_DEED and not SAID_WRONG.search(clean):
            return with_the_feeling_named(pick(_the_deed_pool(deed), memory, clean), clean)
        return pick(SAID_WRONG_REPLIES, memory, clean)
    if _said_unkindly(clean):
        pool = SAID_UNKINDLY_FAMILY if FAMILY_NAMED.search(clean) else SAID_UNKINDLY_REPLIES
        return pick(pool, memory, clean)
    addressed = talked_to.reply(text, memory)
    if addressed:
        return addressed
    company = passing_the_time.reply(text, memory)
    if company:
        return company
    years_turn = the_years.reply(text, memory)
    if years_turn:
        return years_turn
    a_limit = limits.reply(text, memory)
    if a_limit:
        return a_limit
    thanks_off = _a_thank_you_taken_off(clean, memory)
    if thanks_off and _a_plain_good_answer(thanks_off, memory):
        return _reply("positive", memory, _name(memory))
    if thanks_off:
        clean = thanks_off
        text = thanks_off
        tokens = _tokens(clean)
    tokens = _without_the_at_all(tokens)
    step = _after_lonely(clean, memory)
    if step:
        return step
    picked_up = _after_a_lost_thread(clean, memory.get("understood"), memory)
    if picked_up:
        return picked_up
    still_at_it = _laughing_still(clean, memory)
    if still_at_it:
        return still_at_it
    laughing = _laughing_at(clean, memory)
    if laughing:
        return _reply(laughing, memory, _name(memory), clean)
    nothing = _nothing_helps(clean, memory)
    if nothing:
        return nothing
    held = _a_limit(text, memory)
    if held:
        return held
    own_call = _their_own_call(clean)
    if own_call:
        return _reply("own_call", memory, _name(memory), clean)
    body_feeling = _body_is_a_feeling(clean)
    if body_feeling:
        return _reply(body_feeling, memory, _name(memory))
    read = memory.get("understood") if isinstance(memory, dict) else None
    asks = isinstance(read, dict) and read.get("kind") == "question"
    symptom = COLD_SYMPTOM.search(clean)
    cold = bool(symptom or COLD_NAMED.search(clean))
    part = read.get("body") if isinstance(read, dict) else None
    bare = bool(COMPLAINT_ONLY.match(clean)) and not asks
    if (ILL_SELF.search(clean) or (symptom and not asks) or part or bare) \
            and not SICK_DEED.search(clean) and not BODY_BEFORE_AN_EVENT.search(clean):
        if (COLD_SORE.search(clean) and not COLD_SYMPTOM.search(clean)
                and not COLD_SORE_FEELING.search(clean)):
            if not COLD_NAMED.search(COLD_SORE.sub(" ", clean)):
                return None
        if part and "ill_" + part in REPLIES:
            return _reply("ill_" + part, memory, _name(memory), text)
        if cold and _the_same_cold_again(clean, memory):
            return None
        if says_it_has_lingered(clean, illness=True):
            return _reply("ill_lasting", memory, _name(memory), text)
        return _reply("cold" if cold else "ill", memory, _name(memory), text)
    if reads_like_a_symptom(clean) and says_it_has_lingered(clean) \
            and not SICK_DEED.search(clean):
        return None
    scattered = _chat_scatter(clean, memory)
    if scattered:
        return scattered
    understood = memory.get("understood") if isinstance(memory, dict) else None
    said = _as_said(clean, understood) if as_said else clean
    live_emergency = _safety_thread(memory)
    if isinstance(understood, dict) and understood.get("presence"):
        if live_emergency:
            return None
        from ..memory import tried as not_moved
        if not_moved.still_going_on(text, memory):
            return None
        return _say("presence", memory)
    if isinstance(understood, dict) and understood.get("intent") == "opening":
        return _reply("opening", memory, _name(memory))
    if (isinstance(understood, dict) and understood.get("asks_back") and len(tokens) <= 12
            and not live_emergency):
        polarity = understood.get("polarity")
        low = (isinstance(polarity, int) and polarity < 0) or bool(_a_low_word(clean))
        return _reply("back_low" if low else "back", memory, _name(memory))
    met, plan = _just_met(memory)
    if met:
        said = _plan_clause(plan)
        if said:
            join = " — that" if said.lower().startswith("you") else ""
            return "Hi " + met + " — good to meet you, and " + said + join + \
                   " sounds like a good one. What do you need a hand with?"
        kind = understood.get("kind") if isinstance(understood, dict) else None
        if kind in (None, "greeting", "empty"):
            return _reply("meet", memory, met)
        memory["greet"] = met
    if len(tokens) <= 6 and _says_nothing_much(tokens, clean):
        return _reply("notmuch", memory, _name(memory))
    laughed = (isinstance(understood, dict) and understood.get("intent") == "laugh"
               and 0 < len(tokens) <= 8
               and all(lexicon.is_a_laugh(t) or t in ACK_WORDS or t in THANKS_FILLER
                       for t in tokens))
    chatty = laughed or (len(tokens) <= 8
                         and not SAYS_TOO_MUCH.search(clean)
                         and all(t in ACK_WORDS or t in LAUGH_WORDS or t in THANKS_FILLER
                                 for t in tokens))
    if _is_bye(tokens) or _ending_bye(clean, memory):
        return _reply(_bye_kind(tokens), memory, _name(memory))
    bare = [token for token in tokens
            if token not in ADDRESSED and token not in THANKS_NOISE]
    if _a_hedge_answering_the_question(memory):
        if HEDGED_LOW_LINE.match(clean):
            return _reply("hedged_low", memory, _name(memory))
        if HEDGED_OK_LINE.match(clean):
            return _reply("hedged_ok", memory, _name(memory))
    if _is_thanks(bare) or _is_thanks(tokens) or _is_thanks(_without_the_nod(tokens)):
        if ANSWERS_HOW_ARE_YOU.match(clean) and not THANKS_FOR.search(clean):
            return _reply("positive", memory, _name(memory))
        return _reply("thanks", memory, _name(memory))
    moved = limit.move_after_a_limit(clean, memory)
    if moved:
        return moved
    limited = limit.reply_for(clean, memory)
    if limited:
        return limited
    piled = pile.reply_for(clean, memory)
    if piled:
        return piled
    total = portions.the_total_for(clean, memory)
    if total:
        return total
    portion = portions.reply_for(clean, memory)
    if portion:
        return portion
    came_back = returned.pool_for(clean, memory)
    if came_back:
        repeat.handed_back(memory, returned.the_whole_of_it(clean, memory) or came_back)
        return came_back
    not_worked = tried.pool_for(clean, memory)
    if not_worked:
        return pick(not_worked, memory)
    attempt = remedy.reply_for(clean, memory)
    if attempt:
        return attempt
    acted = tried.acted_pool(clean, memory)
    if acted:
        return pick(acted, memory)
    next_step = step_after.reply_for(clean, memory)
    if next_step:
        return next_step
    verdict = _about_the_night_out(clean, tokens, memory)
    if verdict:
        return verdict
    the_hours = hours_after.answer_for(clean, memory)
    if the_hours:
        return the_hours
    conversation = _conversation(clean, tokens, memory)
    if conversation:
        return conversation
    grumble = _work_grumble(clean, tokens, memory)
    if grumble:
        return grumble
    if KICK_MYSELF.search(clean):
        return pick(AT_MYSELF_REPLIES, memory, clean)
    if _is_greeting(tokens):
        return _reply("greeting", memory, _name(memory))
    if _is_howareyou(tokens):
        return _reply("howareyou", memory, _name(memory))
    joke = _joke(clean, tokens, memory)
    if joke:
        return joke
    other = _other_feeling(clean, memory)
    fedup_at = re.search(
        r"\b(done with|fed up|browned off|peeved|sick of|tired of|had enough|"
        r"had it with)\b", said)
    named = OTHER_PERSON.search(said)
    corrected = (FED_UP_DENIED.search(said)
                 and _bare_feeling(STATE_WHEN.sub(" ", FED_UP_DENIED.sub(" ", said))))
    if (not other and fedup_at and not corrected
            and not FED_UP_ABOUT_THE_BOT.search(said[:fedup_at.start()])
            and not FED_UP_WITH_A_PERSON.search(said)
            and not (named and named.start() < fedup_at.start())):
        if FED_UP_DENIED.search(said):
            return _reply("not_feeling", memory, _name(memory))
        if AT_MYSELF.search(clean):
            return pick(AT_MYSELF_REPLIES, memory, clean)
        if _not_coping(clean):
            return _reply("not_coping", memory, _name(memory))
        if FED_UP_WHOLE_OF_IT.search(said):
            return _reply("not_coping", memory, _name(memory))
        _the_weight_said(memory, "annoyed")
        tired_of = _fed_up_with(said)
        if tired_of:
            if tired_of.startswith("being ") or tired_of.startswith("having "):
                options = list(FEDUP_GERUND_SAFE)
            else:
                options = list(FEDUP_REPLIES)
            lead = FEDUP_LEAD.get(_fedup_phrase(said, fedup_at.start()), "Being tired of")
            return pick([option.format(thing=tired_of, obj="you", lead=lead)
                         for option in options], memory, seed_text=text)
        return pick(REPLIES["venting"], memory, seed_text=text)
    if MISS_ME.search(clean):
        return pick(MISS_YOU_REPLIES, memory, seed_text=text)
    if STILL_ON_THEM.search(clean):
        return _reply("missing", memory, _name(memory))
    if _fond_of_the_bot(clean):
        return pick(FOND_REPLIES, memory, seed_text=text)
    if (KIND_TO_ME.search(clean) or _praised_the_answer(clean)) and not DOUBT_FRAME.search(clean):
        return pick(KIND_REPLIES, memory, seed_text=text)
    judgement = _judgement(_as_said(clean, understood), tokens)
    if judgement:
        seed = clean if judgement in ("own_harsh", "own_described") else ""
        return _reply(judgement, memory, _name(memory), seed=seed)
    reaction = _reaction(clean, tokens, memory)
    if reaction:
        seed = clean if not reaction.startswith("agree") else clean + "|" + _news_before(memory)
        return _reply(reaction, memory, _name(memory), seed)
    if VENTED.search(clean):
        return _reply("venting", memory, _name(memory))
    if asks_for_news(clean) and not (
            ANY_WORLD_NEWS_ON.search(clean)
            and not fallback.LIVE_NOT_WORLDS.search(clean)):
        return _reply("no_news", memory)
    if GOOD_NEWS_SAID.search(clean):
        if NOT_LANDED.search(clean) or any(
                negated(clean, word) for word in NOT_GLAD_WORDS):
            return _reply("good_news_not_landed", memory, _name(memory), seed=clean)
        return _reply("happy", memory, _name(memory))
    about = _about_bot(clean, memory.get("understood") if isinstance(memory, dict) else None,
                       memory)
    if about:
        return pick(about, memory)
    if isinstance(memory, dict) and isinstance(memory.get("understood"), dict) \
            and memory["understood"].get("about_bot_kind"):
        return None
    opinion = _opinion(clean, tokens, memory)
    if opinion:
        return opinion
    worry_someone = _worry_someone(said, memory)
    if worry_someone == "pass":
        return None
    if worry_someone:
        return pick(worry_someone, memory)
    early = _early_start(clean, memory)
    if early:
        return pick(early, memory)
    row = _a_row(clean, memory)
    if row:
        return row
    row_next = _a_row_next(clean, memory)
    if row_next:
        return row_next
    row_ending = _a_row_ending(clean, memory)
    if row_ending:
        return row_ending
    someone = _about_someone(clean, memory)
    follow_up = _context_follow_up(clean, memory)
    if someone and someone in set(SOMEONE_NORMAL.values()) and (
            SOMEONE_IS_IT_NORMAL.search(clean) or SOMEONE_NEXT_STEP.search(clean)):
        return someone
    if follow_up:
        return follow_up
    if other and len(tokens) <= 16:
        if not badnews.reads_as_news_with_a_name(clean):
            return _someone_reply(memory, *other, said=said)
    standing = _standing(clean, memory)
    if standing:
        return standing
    bare = _bare_feeling(STATE_WHEN.sub(" ", clean))
    read_as = understood if as_said else None
    feeling = _feeling(clean, read_as, bare=bare)
    if not feeling and KEEPS_HOW_THEY_ARE.search(clean) and not _answers_knows(text, memory):
        feeling = _feeling(clean, read_as, bare=bare, kept=True)
    if feeling in MOOD_KINDS and _going_on(clean):
        feeling = "ongoing" if GOING_ON_LONG.search(clean) else "recurring"
    asks = isinstance(understood, dict) and understood.get("kind") == "question"
    if feeling == "carrying":
        feeling = None if _answers_knows(text, memory) else "not_coping"
    if feeling in MOOD_KINDS and A_VERDICT_ASKED.search(clean):
        feeling = None
    if feeling in MOOD_KINDS and _answers_knows(text, memory):
        feeling = None
    if feeling == "rough_day" and asks and _answers_knows(text, memory):
        feeling = None
    like = _feel_like(clean)
    if like and _a_feeling_riding_on_the_thread(clean, memory):
        like = None
    if like and like != "feel_like":
        return _reply(like, memory, _name(memory), clean)
    if someone and asks and len(tokens) <= 22:
        return someone
    if feeling and (bare or _about_the_person(understood)) and (
            chatty or len(tokens) <= 12 or not asks):
        if feeling in ("ongoing", "recurring"):
            _the_weight_said(memory, feeling)
            turns = memory.get("turns")
            turn_no = len(turns) if isinstance(turns, list) else 0
            if memory.get("mood_advice") == turn_no - 1:
                memory["mood_advice"] = turn_no
                return pick(list(REPLIES["recurring_next"]), memory, clean)
            memory["mood_advice"] = turn_no
            return pick(list(REPLIES[feeling]), memory, clean)
        if feeling == "annoyed" and AT_MYSELF.search(clean):
            return pick(AT_MYSELF_REPLIES, memory, clean)
        if feeling == "happy" and NOT_PROUD.search(clean):
            feeling = "guilty"
        elif (feeling == "happy" and PROUD_OF_MYSELF.search(clean)
              and not PROUD_OF_ANOTHER.search(clean)):
            feeling = "proud"
        if feeling == "happy" and DOUBT_FRAME.search(clean) and _praised_the_answer(clean):
            feeling = None
        if feeling == "confused" and isinstance(memory, dict):
            plainer = meant.answer_for(clean, memory)
            if plainer and plainer.lower().startswith(MEANT_LEADS):
                return plainer
        if feeling in ("happy", "anxious", "proud"):
            return _reply(feeling, memory, _name(memory), clean)
        return _reply(feeling, memory, _name(memory),
                      clean if feeling in ("not_coping", "bad_day", "tears",
                                           "long_stretch") else "")
    if like:
        return _reply(like, memory, _name(memory), clean)
    against = _against_me(clean)
    if against:
        return _reply(against, memory, _name(memory), clean)
    stuck = _stuck(clean, memory)
    if stuck and len(tokens) <= 16:
        if not (stuck == "effort" and _answers_knows(text, memory)):
            kind = "stuck_" + stuck if "stuck_" + stuck in REPLIES else "stuck"
            if kind in ("stuck_eating", "stuck_sleep", "stuck") and LONG_SPAN.search(clean):
                for days in ("stuck_%s_days" % stuck, "stuck_sleep_days"):
                    if days in REPLIES:
                        kind = days
                        break
            return _reply(kind, memory, _name(memory))
    if _my_night(clean) and len(tokens) <= 18:
        return pick(list(REPLIES["stuck_sleep"]), memory, clean)
    someone = _about_someone(clean, memory)
    if someone and len(tokens) <= 22:
        return someone
    news = _news(clean, tokens, memory)
    if news:
        return news
    if _question_coming(understood):
        return _reply("opening", memory, _name(memory))
    thing = _their_thing(clean, tokens, memory, understood)
    if thing:
        return thing
    if SAY_SOMETHING.search(re.sub(r"\s+(?:though|tho)$", "", clean)) \
            and not ASK_WHETHER_TO_SPEAK.search(clean):
        return _reply("say_something", memory, _name(memory))
    if _says_dont_know(clean, tokens):
        return _reply(_idk_kind(memory), memory, _name(memory))
    carried_on = more.reply_for(text, memory) if isinstance(memory, dict) else None
    if carried_on:
        return carried_on
    plan = _intent(clean, tokens, memory)
    if plan:
        if plan in ("next_up", "next_rest", "next_act"):
            return pick(list(REPLIES[plan]), memory, clean)
        return _reply(plan, memory, _name(memory))
    reading = reading_reply.reply_for(clean, memory)
    if reading:
        return reading
    doubted = doubt_reply.reply_for(clean, memory) if isinstance(memory, dict) else None
    if doubted:
        return doubted
    verdict = verdict_reply.reply_for(clean, memory) or verdict_reply.next_step(clean, memory)
    if verdict and verdict not in verdict_reply.QUESTION_BACK_LINES:
        return verdict
    step = step_when_low(clean, memory, FEELING_SAID | fallback.COMFORT_SAID)
    if step:
        return step
    if verdict:
        return verdict
    held = thread.checking_the_verdict(clean, memory) if isinstance(memory, dict) else None
    if held:
        return held
    checked = thread.checking_a_fact(clean, memory) if isinstance(memory, dict) else None
    if checked:
        return checked
    judged = _judged(clean, memory)
    if judged:
        return judged
    if "help" in tokens and all(t in HELP_ONLY for t in tokens):
        nod, nod_seed = _the_nod(memory)
        if nod == "ack":
            return _reply("help_ask", memory, _name(memory), clean)
    job_step = _the_ask_after_a_job_that_went(clean, memory) if not live_emergency else None
    if job_step:
        return job_step
    steps = stuck_line.pool(clean, memory) if not live_emergency else None
    if steps:
        again_steps = repeat.answer_for(text, memory) if isinstance(memory, dict) else None
        if again_steps:
            return again_steps
        return pick(list(steps), memory, clean)
    if isinstance(memory, dict) and repeat.A_TOLD_BACK.search(clean):
        told = repeat.the_figure_they_gave(text, memory)
        if told:
            return told
    short = _short_talk(clean, tokens, memory)
    if short:
        if short == "again_what":
            steps = _the_steps_again(memory)
            if steps:
                return steps
        return _reply(short, memory, _name(memory), clean if short == "overloaded" else "")
    again = repeat.answer_for(text, memory) if isinstance(memory, dict) else None
    if again:
        return again
    what = meant.answer_for(clean, memory)
    if what:
        return what
    heavy = _the_heavy_line(memory) if _a_bare_acknowledgement(clean) else ""
    if heavy:
        return _reply("nod_after_news", memory, _name(memory), heavy)
    if _a_plain_good_answer(clean, memory):
        return _reply("positive", memory, _name(memory))
    if HOW_THEY_ARE_LINE.match(clean) and not _denies_a_good_word(tokens):
        return _reply("positive", memory, _name(memory))
    if re.search(r"\bnot (?:too |half )?bad\b", clean) and len(tokens) <= 8:
        nod, nod_seed = _the_nod(memory)
        return _reply(nod, memory, _name(memory), nod_seed)
    if (isinstance(understood, dict) and understood.get("agrees_to_try")
            and len(tokens) <= 10):
        return _reply("try_ack", memory, _name(memory), clean)
    if not _mid_chat(memory):
        asked = _a_judgement_asked(clean)
        if asked:
            return _reply(asked, memory, _name(memory), clean)
    if (isinstance(understood, dict) and understood.get("asks_a_verdict")
            and verdict_reply.answers_the_ask(understood.get("clean") or text, memory)):
        return None
    thinks = _somebody_thinks_i_should(clean)
    if thinks and not fallback._a_relationship_ending(clean):
        return pick(_thinks_pool(thinks[0]), memory, seed_text=text)
    recommended = _somebody_recommended_a_thing(clean)
    if recommended:
        return pick(SECONDHAND_PRAISE_REPLIES, memory, seed_text=text)
    if not chatty or live_emergency:
        if not live_emergency and isinstance(memory, dict):
            carried = repeat.carried_on(text, memory)
            if carried:
                return carried
        return None
    if isinstance(understood, dict) and understood.get("agreement"):
        return None
    if isinstance(understood, dict) and understood.get("about_bot_kind"):
        return None
    if laughed or any(t in LAUGH_WORDS for t in tokens):
        return _reply("laugh", memory, _name(memory))
    if "worries" in tokens or "problem" in tokens:
        nod, nod_seed = _the_nod(memory)
        return _reply(nod, memory, _name(memory), nod_seed)
    if _only_a_refusal(clean, tokens):
        return _reply("no", memory, _name(memory))
    if any(t in {"idk", "dunno"} for t in tokens) or (
            "not" in tokens and "sure" in tokens) or ("dont" in tokens and "know" in tokens):
        return _reply(_idk_kind(memory), memory, _name(memory))
    if NOT_GOOD.match(clean):
        return _reply("bad_day", memory, _name(memory))
    self_positive = any(t in {"i", "im"} for t in tokens) and not _denies_a_good_word(
        tokens) and all(
        t in POSITIVE or t in {"i", "im", "am", "so", "very", "really", "doing", "today",
                               "feeling", "feel", "too", "not", "bad", "ok", "okay"} for t in tokens)
    if self_positive:
        return _reply("positive", memory, _name(memory))
    answered = answer_reaction.reply_for(clean, memory) if isinstance(memory, dict) else None
    if answered:
        return answered
    nod, nod_seed = _the_nod(memory)
    if NOT_A_NOD.match(clean) and fallback._a_good_time(clean, memory):
        return None
    return _reply(nod, memory, _name(memory), nod_seed)

from ..memory import again as _never_twice

respond = _never_twice.replied(respond)
