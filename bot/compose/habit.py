import re

from . import pick

PEOPLE = (
    "mum", "mom", "mother", "dad", "father", "parent", "parents", "sister", "brother",
    "partner", "husband", "wife", "boyfriend", "girlfriend", "fiance", "fiancee", "flatmate",
    "housemate", "roommate", "landlord", "landlady", "boss", "manager", "colleague", "coworker",
    "co-worker", "teammate", "team mate", "workmate", "neighbour", "neighbor", "son", "daughter",
    "kid", "child", "children", "friend", "mate", "nan", "nana", "gran", "granny", "grandma",
    "grandad", "grandpa", "aunt", "uncle", "cousin", "ex", "stepson", "stepdaughter", "stepdad",
    "stepmum", "mother-in-law", "father-in-law", "brother-in-law", "sister-in-law",
    "daughter-in-law", "son-in-law", "in-laws", "household", "family",
    "childminder", "babysitter", "nanny", "carer", "cleaner", "hairdresser", "tutor",
    "twin", "grandkid", "boy", "girl", "lad", "relative", "sibling", "stepkid",
)
PEOPLE_SET = frozenset(PEOPLE)
A_PERSON = re.compile(r"\b(?:my|our|the)\s+(?:[a-z-]+\s+){0,2}?(?:" + "|".join(PEOPLE) + r")(?:s|es)?\b")
SOMEONE = re.compile(r"\b(?:someone|somebody|people|everyone|everybody)\b")

RECURS = re.compile(
    r"\b(?:keeps?|kept|always|never|constantly|continually|forever|again and again|"
    r"every (?:single |blessed )?(?:day|night|morning|week|weekend|time|month)|"
    r"all the time|time after time|over and over|wont stop|won'?t stop|doesnt stop|"
    r"doesn'?t stop|never stops)\b")

DONE_TO_ME = re.compile(
    r"\b(?:ask|asks|asked|asking|tell|tells|told|telling|invite|invites|invited|inviting|"
    r"thank|thanks|thanked|thanking|owe|owes|owed|blame|blames|blamed|criticis\w*|criticiz\w*|"
    r"interrupt|interrupts|interrupted|interrupting|nag|nags|nagged|nagging|moan|moans|moaned|"
    r"complain|complains|complained|ring|rings|ringing|rang|call|calls|calling|called|text|"
    r"texts|texted|texting|message|messages|messaged|messaging|phone|phones|phoned|phoning|"
    r"lecture|lectures|lectured|lecturing|mock|mocks|mocked|belittle|belittles|belittled|"
    r"ignore|ignores|ignored|ignoring|talk|talks|talked|talking|shout|shouts|shouted|shouting|"
    r"yell|yells|yelled|yelling|complain|moan|pick|picks|picked|picking)\b"
    r"(?:\s+[a-z]+)?\s+(?:me|us)\b")
ASK_FOR = re.compile(r"\b(?:ask|asks|asked|asking)\s+(?:me|us)\s+(?:for|to)\b")
NOT_ASKED = re.compile(
    r"\b(?:never|doesn'?t|doesnt|don'?t|dont|won'?t|wont|not)\b[^.?!]{0,26}?\b(?:"
    r"invit\w*|includ\w*|asks? me|ask me|asked me|picks? me|picks? up|leaves? me out|"
    r"left me out)\b")
UNSEEN = re.compile(
    r"\b(?:never|doesn'?t|doesnt|don'?t|dont|won'?t|wont|not)\b[^.?!]{0,26}?\b(?:"
    r"thank\w*|notic\w*|appreciat\w*|listen\w*|consider\w*|repl\w*|respond\w*|"
    r"visits?|visit me|talks? to me|talked to me)\b")
NOT_HELPED = re.compile(
    r"\b(?:never|doesn'?t|doesnt|don'?t|dont|won'?t|wont)\b[^.?!]{0,26}?\b(?:helps?|helping|"
    r"pulls? (?:his|her|their) weight|does (?:his|her|their) share)\b")
MY_THING = re.compile(
    r"\b(?:borrow|borrows|borrowed|borrowing|take|takes|took|taking|use|uses|used|using|"
    r"nick|nicks|nicked|nicking|eat|eats|ate|eating|drink|drinks|drank|drinking|spend|spends|"
    r"spent|spending|wear|wears|wearing|wore|hide|hides|hid|hoard|hoards|fill|fills|filled|"
    r"move|moves|moved|break|breaks|broke|break|throw|throws|threw|smash|smashes)\b"
    r"[^.?!]{0,20}?\b(?:my|our)\b")
MESS = re.compile(
    r"\b(?:everywhere|all over|all over the place|lying around|left around|in the way|"
    r"in (?:my|our) way|in the (?:hall|hallway|kitchen|sink|living room|lounge|bathroom|bath|"
    r"bedroom|fridge|bin|garden|yard|car|sofa|cupboard|garage|utility|passage|porch)|"
    r"on the (?:floor|table|sofa|bed|counter|stairs|side)|up the stairs|on the stairs|"
    r"out the front|outside the front|in the passage)\b")
STRAIN = (
    "drives me mad", "drives me nuts", "drives me crazy", "drives me insane",
    "drives me up the wall", "does my head in", "does my nut in", "gets to me", "getting to me",
    "winds me up", "wound me up", "it annoys me", "annoys me", "annoying me", "sick of",
    "fed up", "cant stand", "can't stand", "wearing me down", "wears me down", "worn me out",
    "wears me out", "boils my blood", "grates on me", "had enough of", "draining me",
)
CRITICISED = re.compile(
    r"\b(?:criticis\w*|criticiz\w*|comment\w*|picks? on|picked on|picking on|puts? me down|"
    r"putting me down|makes? fun of|made fun of|moan\w*|complain\w* about|lectur\w*|"
    r"tells? me how|tells? me what|remind\w* me|nag\w*|judge\w*|belittl\w*|mocks?|mocked|"
    r"rubs? it in)\b")
CRITICISED_MY = re.compile(
    r"\b(?:my|our)\s+(?:[a-z]+\s+){0,2}?(?:weight|looks?|cooking|house|parenting|driving|job|"
    r"money|hair|clothes|lifestyle|accent|english|kids?|children|body|figure|age)\b"
    r"|\b(?:how|the way)\s+(?:i|we)\s+(?:look|dress|speak|talk|walk|eat|spend|parent|drive)\b")
BAILS = re.compile(
    r"\b(?:cancel\w*|cancell\w*|bails?|bailed|bailing|pulls? out|pulled out|pulling out|"
    r"drops? out|dropped out|dropping out|lets? me down|let me down|letting me down|"
    r"messes? me about|messing me about|mess(?:es)? me around|messing me around|"
    r"not turn(?:ing)? up|doesn'?t turn up|didn'?t turn up|"
    r"stands? me up|stood me up|no[- ]?shows?|no[- ]?showed|changes? (?:the|our) plans?)\b")
KEEPS_THE_ARRANGEMENT = re.compile(
    r"\b(?:never|doesn'?t|doesnt|don'?t|dont|won'?t|wont)\b[^.?!]{0,20}?\b(?:cancel\w*|"
    r"cancell\w*|bails?|lets? me down|stands? me up|no[- ]?shows?|late|brings? (?:it|that) up)\b")
ALWAYS_DOES_IT = re.compile(
    r"\b(?:keeps?|kept|always|constantly|continually|every\s+(?:single\s+)?(?:day|week|time))\b"
    r"[^.?!]{0,26}?\b(?:invit\w*|includ\w*|thank\w*|say\w*\s+thank\w*|"
    r"ask(?:s|ing)? me (?:over|round|out|along|to)\b"
    r"|asks? after me\b)")
THANKED = re.compile(r"\bthank\w*|\bthank you\b|\bsays?\s+(?:a\s+)?thank")
COURTESY = re.compile(r"\b(?:thank\w*|invit\w*|includ\w*|asks? me (?:over|round|out|along))\b")
COURTESY_DENIED = re.compile(
    r"\b(?:never|not|doesn'?t|doesnt|don'?t|dont|won'?t|wont|hardly|rarely|only when)\b")
NOT_SINCERE = re.compile(
    r"\b(?:never|doesn'?t|doesnt|didn'?t|didnt|don'?t|dont|won'?t|wont|not)\s+"
    r"(?:really\s+|ever\s+|actually\s+|truly\s+)?mean(?:s|t)?\s+(?:it|a word of it)\b")
A_SHARED_OCCASION = re.compile(
    r"\bask(?:s|ing)? me (?:to |round for |over for )?(?:dinner|lunch|supper|tea|a meal|a drink|"
    r"drinks|a party|a barbecue|a bbq|a picnic|a night out|a wedding|a do)\b")
ARRIVES_LATE = re.compile(
    r"\b(?:turns? up late|turning up late|shows? up late|showing up late|arriv\w* late|"
    r"arrives? late|always late|never on time|keeps? me waiting|every time we meet| timekeeping)\b")
GOING_ON = re.compile(
    r"\b(?:goes? on about|going on about|goes? on and on|going on and on|keeps? on about|"
    r"bangs? on about|"
    r"harks? on about|keeps? bringing (?:it|that) up|brings? (?:it|that) up|"
    r"wont drop it|won'?t drop it|never drops it)\b")
EMAIL_HABIT = re.compile(
    r"\b(?:reply(?:ing|ies)? all|replies all|cc'?s? (?:everyone|the whole|us all)|"
    r"copies? (?:in )?(?:everyone|the whole team|the lot)|forwarding everything|"
    r"forwards everything)\b")
WORK_PEOPLE = frozenset(("boss", "manager", "colleague", "coworker", "co-worker", "teammate",
                         "team mate", "workmate"))
WORK_WORDS = ("goalpost", "goal", "goals", "deadline", "rota", "shift", "1:1",
              "one to one", "one-to-one",
              "meeting", "brief", "priority", "priorities", "workload", "target", "overtime",
              "annual leave", "holiday", "pay rise", "promotion", "review", "appraisal",
              "micromanage", "micromanaging", "email", "inbox", "projects?")
NOT_THIS = frozenset((
    "fall", "falls", "falling", "fell", "fallen", "cough", "coughs", "coughing", "cold", "flu",
    "sick", "ill", "unwell", "pain", "pains", "hurt", "hurts", "hurting", "ache", "aches",
    "dizzy", "faint", "fainting", "forget", "forgets", "forgetting", "forgot", "memory",
    "confused", "dementia", "alzheimers", "alzheimer's", "hospital", "doctor", "gp", "nurse",
    "tablets", "medication", "medicine", "chemo", "cancer", "stroke", "operation", "surgery",
    "bleed", "bleeding", "blood", "bruise", "bruises", "lump", "rash", "fever", "vomit",
    "vomiting", "hospital", "hit", "hits", "hitting", "punch", "punches", "kick", "kicks",
    "slap", "slaps", "grabbed", "grabs", "touched", "touches", "touching", "threaten",
    "threatens", "threatened", "abuse", "abusive", "bullies", "bullying", "bullied",
    "drunk", "drinks", "smokes", "smoking", "suicide", "suicidal", "self harm", "kill",
    "starving", "anorexic", "depressed", "depression", "anxious", "anxiety", "panic",
    "therapy", "therapist", "counselling", "counseling", "appointment", "appointments",
))
NOT_A_GRUMBLE = frozenset((
    "waking", "wakes", "woke", "sleep", "sleeps", "sleeping", "crying", "cries", "cried",
    "nappy", "nappies", "feeding", "feeds", "tantrum", "tantrums", "teething", "barking",
    "barks", "howling", "scratching", "litter", "bites", "biting", "chewing", "jumping up",
    "soiling", "weeing", "pooing",
))
CHILD_PEOPLE = frozenset(("son", "daughter", "kid", "child", "children", "stepson",
                          "stepdaughter", "teenager", "teenagers", "toddler", "baby"))
GOOD_WORDS = frozenset((
    "nicely", "kindly", "sweet", "lovely", "proud", "funny", "jokes", "joking", "hilarious",
    "thoughtful", "supportive", "helpful", "amazing", "brilliant", "wonderful", "affectionate",
    "cuddly", "cuddles",
))


ASKED = (
    "Decide your line before the next ask rather than in the moment, and make it one sentence: "
    "what you can do and what you can't. 'I can do Saturday, but not every Saturday' is a thing "
    "somebody can plan around, and you don't owe a reason.",
    "Say it once, calmly, and make it about the thing rather than the person: 'I'd rather you "
    "asked me first.' One clear line lands where a hint does not, and it is kinder than going "
    "quiet about it.",
    "Give them an answer they can work with: what you can do, and what you can't. 'I can help "
    "with the school run, but I can't lend money again' is a line somebody can plan around.",
)
TAKEN = (
    "Make it one rule rather than one row, said once and warmly the next time they ask: 'of "
    "course, if it's back by Sunday.' A rule they agree to is easier to hold than a complaint "
    "about the last time.",
    "Ask before the next time rather than after: 'can we agree I'm asked first, even if the "
    "answer is going to be yes?' It costs nothing when they would have asked anyway.",
    "Keep the two or three things you actually mind out of reach and let the rest go. Then the "
    "one sentence - 'anything of mine, just ask' - covers the lot without a list of every time.",
)
MESSY = (
    "Give the thing one place to go rather than asking for tidiness in general: 'the shoes live "
    "in the cupboard by the door.' A named place is something a person can do; 'clear up after "
    "yourself' is not.",
    "Ask for the one job, once, at a calm moment - 'can the dishes go in the dishwasher before "
    "bed?' - rather than for a change in character. One job named is one job done.",
    "Say it as the house rule rather than as a complaint about them: 'in this house the boots "
    "come off at the door.' A rule is easier to hear than a list of the times they didn't.",
)
LEFT_OUT = (
    "Say it once, plainly, as a wish rather than an accusation: 'I'd love to be asked next time, "
    "even at short notice.' People often don't know they've left somebody out, and one sentence "
    "is usually enough.",
    "Ask for the next one rather than for the reason: 'can I come to the next one?' A straight "
    "yes or no tells you more than any hint will, and it is easy for them to say yes to.",
    "Worth saying out loud once - 'I've noticed I don't get asked any more, and it does get to "
    "me' - and then letting them answer. The answer is the useful part, whatever it is.",
)
TAKEN_FOR_GRANTED = (
    "Say what you would like noticed rather than what they didn't do: 'a thanks when I've done "
    "the shopping would go a long way.' People often don't know which bit you want acknowledged, "
    "and a thing named is something they can do.",
    "Ask for it once, plainly and without a score kept: 'it would help if you said when it's "
    "good.' Then notice it when it comes, because the thanks you asked for is the one they are "
    "learning to give.",
    "Worth saying what the effect is, once: 'I do a lot round here and it goes unnoticed, and "
    "that is what wears me down.' It is easier to hear than 'you never thank me'.",
)
CRITICISED_LINES = (
    "Say it once, about one thing, in the moment: 'please don't comment on that - it isn't "
    "helping.' You don't have to justify it, and not liking it is reason enough.",
    "Name the thing and the effect in one sentence - 'when you say that, I stop wanting to tell "
    "you things' - and leave it there. It is a statement, not an argument to win.",
    "Answer flatly and warmly the first time, then give the same short answer every time after: "
    "'I heard you, and I'm not changing it.' Repetition is what ends it, not a better argument.",
)
WORK_LINES = (
    "Get it in writing and ask what moved: 'just to confirm, it's Tuesday now - what changed?' "
    "A written thread is what you can point at the next time it shifts, and it costs one email.",
    "Ask what moved and what comes off instead of why it moved: 'if this is the new priority, "
    "what drops?' That hands the choice to the person who can actually make it.",
    "Raise it once, at the end of a meeting, in plain words: 'when the plan changes twice a week "
    "I lose time on the rest.' Say what it costs you, not that it is annoying.",
)
CREDIT_LINES = (
    "Say what you did, in one sentence, in the room where it comes up: 'I did the analysis behind "
    "that.' Credit follows a clear claim, and the quiet hope that somebody notices is what leaves "
    "it with them.",
    "Ask for the part you want named rather than the whole thing: 'can the write-up say who did "
    "what?' It is a small, reasonable request, and it is much easier to say yes to than a row "
    "about taking credit.",
    "Keep a short note of what you did and when - not to send to anyone, but so you can say it "
    "plainly the next time it matters. Then say it once, warmly and without the charge: 'that was "
    "mine, and I'd like that known.'",
)
GOOD_HABIT_APPRECIATED = (
    "That is rarer than people think, and worth saying out loud once: 'I noticed you always say "
    "thank you, and it makes a difference.' People hear the complaint version far more often than "
    "the good one.",
    "It is worth naming to their face rather than just enjoying: 'you always notice, and I "
    "appreciate it.' A thank-you that goes unmentioned tends to stop, because nobody can tell it "
    "landed.",
    "Say it back in the same plain way, in the moment: 'I appreciate that you always think to say "
    "it.' One sentence is the whole of what it takes.",
)
GOOD_HABIT_INCLUDED = (
    "That is a good habit to be on the receiving end of, and worth naming to their face: 'I "
    "noticed you always think to ask me.' People rarely hear the good version of a habit, and it "
    "is usually never said.",
    "Say yes, and say why once: 'I like that you always think to include me.' The person who keeps "
    "asking is usually the one who never gets told that it lands.",
    "Enjoy it and say so in the moment rather than leaving it as a thing you only notice - 'I "
    "noticed, and I'm glad of it.' It costs nothing and it usually lands better than people "
    "expect.",
)
GOOD_HABIT = GOOD_HABIT_APPRECIATED + GOOD_HABIT_INCLUDED
WORDS_NOT_MEANT = (
    "Weigh what they do against what they say, because a thank-you nobody means is the cheapest "
    "thing there is to give. If nothing else in it matches the words, stop going out of your way "
    "for a while and see what they notice.",
    "Say the plain version once, without heat: 'I'd rather you said nothing than said it out of "
    "habit.' Either answer tells you more than the words did.",
    "Ask for the thing rather than the words: 'it would mean more if you helped with it than if "
    "you thanked me for it.' Somebody who won't do the thing has told you what the words are "
    "worth.",
)

RAISE = (
    "Say it once, at a calm time, about the pattern rather than today: 'this keeps happening and "
    "it's starting to get to me - can we sort it?' Name the thing they do and the one change you "
    "want; a list of every time turns it into a row.",
    "Raise it early rather than on the tenth time, and ask for the one change you actually want. "
    "'I'd rather you asked first' is something a person can act on; 'stop it' is not.",
    "Worth one plain sentence to them, said warmly and once. People can act on a request - 'can "
    "we agree the boots go by the door?' - not on a sigh.",
)
BAILING = (
    "Say it plainly once, and name the pattern rather than the last time: 'you've cancelled three "
    "times now and it leaves me stuck - can we agree a week's notice?' Then say what you will do "
    "if it happens again, and do that.",
    "Put a fallback in place before the next time, so the cost lands on them rather than on you: a "
    "backup for the childcare, somebody else who can drive, a plan that does not need them to turn "
    "up. Nothing about this changes until cancelling costs them something.",
    "It is fair to ask why, once: 'is something making it hard at the moment?' If there is a "
    "reason you can both work with, say what would help; if there is not, it is worth saying the "
    "arrangement no longer works for you.",
)
LATE_LINES = (
    "Agree the time out loud, then say what happens if it slips: 'if you're not here by seven I'll "
    "start without you.' A consequence you actually keep is what changes a habit; being annoyed "
    "on the night does not.",
    "Say it once, without the sarcasm, in the calmest voice you have: 'when you're late it means I "
    "am waiting, and I'd rather we set a time we both mean.' Then stop being the person who waits "
    "quietly.",
    "Ask for a message rather than for punctuality, because it is the waiting that costs you: 'if "
    "you'll be more than ten minutes, text me.' That is easy to say yes to, and it gets you the "
    "thing you actually wanted.",
)
SUBJECT_AGAIN = (
    "Ask what they want from the conversation: 'when you bring it up, is there something you want "
    "me to say?' Somebody who goes over the same ground is usually after an answer they have not "
    "had yet, and naming that ends it quicker than changing the subject.",
    "Say where the line is once, in a warm voice: 'I've said all I can about that one - I'd rather "
    "talk about something else tonight.' Then steer, gently, to something you both enjoy.",
)


AFTER_A_SAYING = (
    "went quiet", "didnt say anything", "didn't say anything", "said nothing", "got annoyed",
    "got defensive", "got funny", "got upset", "shrugged", "laughed it off", "laughed",
    "said sorry", "said they were sorry", "agreed", "promised", "said ok", "said okay",
    "didnt listen", "didn't listen", "ignored it", "did it again", "kept doing it",
    "went mad", "kicked off", "stormed off", "hung up", "walked off", "denied it",
)
THE_SAYING = (
    "i said", "i told", "i asked", "ive said", "i've said", "ive told", "i've told",
    "i explained", "i mentioned", "i brought it up", "i tried", "i texted", "i wrote",
)
ALWAYS_COUNT = (
    "every single day", "every single time", "every day", "every time", "all the time",
    "constantly", "again and again", "over and over", "non stop", "non-stop", "daily",
    "every week", "every night", "without fail", "for years", "so often",
)
SELF_DOUBT = (
    "am i overreacting", "am i being too sensitive", "am i being sensitive",
    "am i over thinking", "am i overthinking", "am i being unreasonable", "is it me",
    "should i just give up", "should i give up", "am i mad", "am i wrong to",
    "is that normal", "am i being daft", "am i being silly", "too sensitive",
)
ABOUT_ME = (
    "Ask for one example with a time and a place - 'when was the last time?' - instead of "
    "arguing about all of you. A real instance tells you what to change; a verdict does not.",
    "Take the grain of truth and say what you would like instead: 'you're right that I've been "
    "on my phone at dinner - I'll put it down.' That ends it faster than a defence does, and it "
    "does not mean agreeing with all of it.",
    "Ask what they would like more of rather than whether they are right: 'what would a good "
    "evening look like for you?' That is a question with an answer, and a verdict is not.",
    "Say it back before you answer, so you both know what is being said: 'so you feel like I'm "
    "not really here - is that it?' A fair amount of these turn out to be about one bad week.",
    "Give it a hearing without signing up to all of it: 'some of that lands and some of it "
    "doesn't - can we talk about the bit that matters most?' Then do that one thing.",
)
SAID_IT_POOL = (
    "Then you have said it, which is the hard half. Say the same sentence again next time, in "
    "the same words - a line that comes back identical is what makes it a rule rather than a "
    "mood, and it is the explaining that gives them something to argue with.",
    "The first time is usually the one that gets argued with, so say it once more the same way "
    "and then let it sit. Nothing changes in the moment; what changes is that they now know "
    "what you will say.",
    "A quiet reply to that is normal, and it is not the answer yet. Hold the line exactly as "
    "you put it - 'I can't do that' - and leave the door open for the next time: 'ask me again "
    "about Saturday and I'll say yes'.",
)
EVERY_TIME_POOL = (
    "Then it is a pattern rather than a bad week, and worth naming as one: 'this happens most "
    "days' lands differently from 'you did it again'. Ask for the smallest version of it - one "
    "thing, one place - because a whole list is easy to refuse and one thing is not.",
    "Each time it happens, say the same short line and nothing else. It feels repetitive to you "
    "because you are the one saying it; being boring about it is exactly what makes it stick.",
)
DOUBT_POOL = (
    "It is not you being sensitive: a small thing that happens every day is a different thing "
    "from a small thing that happens once. Being worn down by the repetition is the honest "
    "response to it, and it is worth saying as its own sentence.",
    "You are not asking for much - you are asking for the same small thing twice - so it is "
    "worth one clear go before you decide anything. If nothing changes after you have said it "
    "plainly, that is information about them rather than about you.",
    "A thing can be small and still wear you down when it lands every day. Say the one sentence "
    "you would say to a friend in the same spot, and take your own side in it.",
)
HOLD_THE_LINE = (
    "The line stays the same, and it is worth saying it once more the same way: what you can do, "
    "and what you can't. You don't have to give a reason twice.",
    "Then it is still the one plain sentence, said warmly and once: 'I can't do that.' After that "
    "the answer is no, and it does not need explaining again.",
    "Worth naming it once, plainly, rather than hinting: 'this is happening a lot and I'd like it "
    "to change.' Then leave the next move with them, which is where it belongs.",
)
MY_POOLS = (ASKED, TAKEN, MESSY, LEFT_OUT, TAKEN_FOR_GRANTED, CRITICISED_LINES, WORK_LINES,
            BAILING, LATE_LINES, SUBJECT_AGAIN, RAISE, ABOUT_ME, GOOD_HABIT, WORDS_NOT_MEANT)
THREAD_TURNS = 3


def _in_my_pools(line):
    said = " ".join(str(line or "").split())
    if not said:
        return False
    return any(said.startswith(reply[:30]) for pool in MY_POOLS for reply in pool)


def _thread_open(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return False
    for turn in reversed(turns[-THREAD_TURNS:]):
        if not isinstance(turn, dict):
            continue
        line = str(turn.get("bot") or "")
        if not line:
            continue
        return _in_my_pools(line)
    return False


def holds_the_thread(memory):
    return _thread_open(memory)


def _follow_up(clean, memory):
    if not _thread_open(memory):
        return None
    words = clean.split()
    asking_about_itself = re.search(r"\b(?:you|your|the bot|this bot)\b", clean)
    if asking_about_itself:
        return None
    if any(phrase in clean for phrase in SELF_DOUBT):
        return DOUBT_POOL
    if any(phrase in clean for phrase in ALWAYS_COUNT) and len(words) <= 12:
        return EVERY_TIME_POOL
    if re.search(r"\b(?:what|how)\b[^?]{0,30}\b(?:say|tell|word|phrase|put it|bring it up)\b",
                 clean):
        return None
    tried = any(phrase in clean for phrase in THE_SAYING)
    outcome = any(phrase in clean for phrase in AFTER_A_SAYING)
    if (tried or outcome) and len(words) <= 20:
        return SAID_IT_POOL
    if re.search(r"\b(?:says? (?:she|he|they)'?ll|said (?:she|he|they)'?d|promised|"
                 r"says? (?:she|he|they) (?:will|would)|doesn'?t|didn'?t|won'?t)\b", clean) \
            and len(words) <= 20:
        return SAID_IT_POOL
    if re.search(r"\b(?:he|she|they|him|her|them)\b", clean) and len(words) <= 12 \
            and "?" not in clean:
        return HOLD_THE_LINE
    return None


SAYS_ABOUT_ME = re.compile(
    r"\b(?:says?|said|tells?|told|thinks?|reckons?|calls?)\s+(?:me\s+|everyone\s+|people\s+)?"
    r"(?:that\s+)?(?:i'?m|im|i am|i never|i always|i dont|i don'?t|i only|i just)\b")
CREDIT = re.compile(r"\b(?:take|takes|took|taking|get|gets|got|getting)\s+(?:all\s+)?"
                    r"(?:the\s+)?credit\b|\b(?:takes|took|getting|gets)\s+the\s+blame\b")

def _the_one(word):
    if word in CHILD_PEOPLE or word in WORK_PEOPLE or word in PEOPLE_SET:
        return word
    for cut in (word[:-1], word[:-2]):
        if cut in CHILD_PEOPLE or cut in WORK_PEOPLE or cut in PEOPLE_SET:
            return cut
    return word


def _person_named(clean):
    match = A_PERSON.search(clean)
    if match:
        return match.group(0)
    return ""


def _shape(clean, person):
    last = _the_one(person.split()[-1]) if person else ""
    if NOT_SINCERE.search(clean):
        return WORDS_NOT_MEANT
    if (ALWAYS_DOES_IT.search(clean) and not BAILS.search(clean)
            and (A_SHARED_OCCASION.search(clean) or not ASK_FOR.search(clean))):
        return GOOD_HABIT_APPRECIATED if THANKED.search(clean) else GOOD_HABIT_INCLUDED
    if (COURTESY.search(clean) and not COURTESY_DENIED.search(clean)
            and not (BAILS.search(clean) or _strained(clean) or CRITICISED.search(clean)
                     or NOT_ASKED.search(clean) or UNSEEN.search(clean))):
        return GOOD_HABIT_APPRECIATED if THANKED.search(clean) else GOOD_HABIT_INCLUDED
    if last in WORK_PEOPLE and (any(word in clean for word in WORK_WORDS)
                                or DONE_TO_ME.search(clean)):
        return WORK_LINES
    if SAYS_ABOUT_ME.search(clean):
        return ABOUT_ME
    if (CRITICISED.search(clean) and (DONE_TO_ME.search(clean)
                                      or CRITICISED_MY.search(clean)
                                      or SAYS_ABOUT_ME.search(clean)
                                      or _strained(clean))):
        return CRITICISED_LINES
    if CREDIT.search(clean):
        return CREDIT_LINES
    if NOT_ASKED.search(clean):
        return LEFT_OUT
    if UNSEEN.search(clean):
        return TAKEN_FOR_GRANTED
    if ASK_FOR.search(clean):
        return ASKED
    if MESS.search(clean) and re.search(r"\b(?:leaves?|left|leaving|drops?|dropped|"
                                        r"dumping|dumps|put|puts|putting)\b", clean):
        return MESSY
    if MY_THING.search(clean):
        return TAKEN
    if NOT_HELPED.search(clean):
        return RAISE
    if BAILS.search(clean) and not KEEPS_THE_ARRANGEMENT.search(clean):
        return BAILING
    if ARRIVES_LATE.search(clean) and not KEEPS_THE_ARRANGEMENT.search(clean):
        return LATE_LINES
    if (GOING_ON.search(clean) and last not in CHILD_PEOPLE
            and not KEEPS_THE_ARRANGEMENT.search(clean)):
        return SUBJECT_AGAIN
    if EMAIL_HABIT.search(clean) and last in WORK_PEOPLE:
        return RAISE
    if DONE_TO_ME.search(clean):
        return CRITICISED_LINES
    if _strained(clean):
        return RAISE
    return None


def _said_at_work(clean, person):
    last = _the_one(person.split()[-1]) if person else ""
    return last in WORK_PEOPLE and any(word in clean for word in WORK_WORDS)


def _strained(clean):
    return any(phrase in clean for phrase in STRAIN)


def answer_for(text, memory):
    clean = " ".join(str(text or "").lower().split())
    if not clean or len(clean.split()) > 30:
        return None
    memory = memory if isinstance(memory, dict) else {}
    words = set(re.findall(r"[a-z']+", clean))
    if words & NOT_THIS:
        return None
    follow = _follow_up(clean, memory)
    if follow:
        return pick(list(follow), memory, clean)
    if not RECURS.search(clean) and not NOT_SINCERE.search(clean):
        return None
    someone = SOMEONE.search(clean)
    person = _person_named(clean) or (someone.group(0) if someone else "")
    if not person:
        return None
    if words & NOT_A_GRUMBLE or words & GOOD_WORDS:
        return None
    if clean.endswith("?") and not re.search(r"\b(?:what|how)\b[^?]{0,24}\b(?:say|tell|word|"
                                              r"phrase|put it|raise it)\b", clean):
        return None
    if not (DONE_TO_ME.search(clean) or MY_THING.search(clean) or MESS.search(clean)
            or NOT_ASKED.search(clean) or UNSEEN.search(clean) or NOT_HELPED.search(clean)
            or CRITICISED_MY.search(clean) or SAYS_ABOUT_ME.search(clean)
            or CREDIT.search(clean) or _strained(clean) or NOT_SINCERE.search(clean)
            or BAILS.search(clean) or ARRIVES_LATE.search(clean) or GOING_ON.search(clean)
            or EMAIL_HABIT.search(clean) or COURTESY.search(clean)
            or _said_at_work(clean, person) or ALWAYS_DOES_IT.search(clean)):
        return None
    pool = _shape(clean, person)
    if not pool:
        return None
    return pick(list(pool), memory or {}, clean)
