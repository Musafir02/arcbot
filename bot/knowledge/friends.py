import re

from ..compose.repair import owns_the_deed
from .dishes import KEEP_QUALITY_WORDS
from .lookup import entry
from .wording import TALKING_IS_NOT_A_CHAT


_COOKING_FOR_THEM = re.compile(
    r"\b(?:cook|cooks|cooking|cooked|make|makes|making|made|bake|baking|roast|roasting|"
    r"hosting|prepare|preparing)\b[^.?!]{0,30}\b(?:for|to)\b", re.IGNORECASE)


def _not_cooking_for_them(understood):
    if not isinstance(understood, dict):
        return True
    said = str(understood.get("clean") or understood.get("text") or "")
    return not _COOKING_FOR_THEM.search(said)

ANSWERS = ("friends-and-relationships",)
_GESTURE = re.compile(
    r"\b(?:something|somethin|anything|a thing|things|a present|a gift)\b"
    r"[^.?!]{0,20}\b(?:nice|good|kind|special|lovely)\b"
    r"|\bnice (?:little )?thing to do for\b"
    r"|\bdo something nice for\b", re.IGNORECASE)
_LOW_MOOD = re.compile(
    r"\b(?:sad|sadness|down|low|upset|unhappy|miserable|struggl\w*|rough time|hard time|"
    r"bad time|going through|cry|cries|crying|cried|bad news|not themselves?|not himself|"
    r"not herself|in a rut|stressed|grie\w*|bereave\w*|lonely|loneliness|depress\w*|"
    r"anxious|worried|hurt|cheer\w*|comfort\w*|console\w*|feel better|"
    r"having a hard)\b", re.IGNORECASE)


def _not_a_plain_gesture(understood):
    if not isinstance(understood, dict):
        return True
    said = str(understood.get("clean") or understood.get("text") or "")
    if not _GESTURE.search(said):
        return True
    return bool(_LOW_MOOD.search(said))



_THE_PERSON = (
    "my husband", "my wife", "my partner", "my boyfriend", "my girlfriend", "my fiance",
    "my friend", "my best friend", "my mate", "my mum", "my mom", "my mother",
    "my dad", "my father", "my parents", "my sister", "my brother", "my son", "my daughter",
    "my child", "my teenager", "my flatmate", "my housemate", "my roommate", "my landlord",
    "my boss", "my manager", "my colleague", "my coworker", "my team", "my neighbour",
    "my neighbor", "my mother in law", "my mother-in-law", "my in laws", "my ex", "my family",
    "a friend", "a colleague", "a coworker", "a flatmate", "a neighbour", "a family member",
    "someone at work", "with her", "with him", "with them", "to her", "to him", "to them",
    "tell her", "tell him", "tell them", "ask her", "ask him", "ask them")
_THE_TALK = (
    "conversation", "bring it up", "bring something up", "bring this up", "have it out",
    "open up", "my feelings", "about my feelings", "how i feel", "how i really feel",
    "confront", "confronting", "confrontation", "the subject", "broach", "hard talk")


def _names_a_person_and_is_not_a_deed(understood):
    return _names_a_person_or_the_talk(understood) and not owns_the_deed(understood)


def _names_a_person_or_the_talk(understood):
    words = " ".join(str(word).lower() for word in understood.get("words") or ())
    whole = " %s " % " ".join(words.split())
    return any(part in whole for part in _THE_PERSON + _THE_TALK)


HELPING_ASK = ("how do i help", "how can i help", "how do i best help", "how can i best help",
               "how do i support", "how can i support", "how best to support",
               "what do i do", "what should i do", "what can i do", "what could i do",
               "how do i start helping",
               "help them through", "help him through", "help her through",
               "help them cope", "help him cope", "help her cope")
HELPING_PERSON = ("friend", "friends", "mate", "mates", "best friend", "best mate", "bestie",
                  "partner", "husband", "wife", "boyfriend", "girlfriend", "fiance", "fiancee",
                  "mum", "mother", "mam", "dad", "father", "parent", "parents", "sister",
                  "brother", "son", "daughter", "child", "someone", "somebody", "person",
                  "colleague", "coworker", "neighbour", "neighbor", "them", "him", "her")
HELPING_TROUBLE = ("sad", "sadness", "down", "upset", "unhappy", "miserable", "struggling",
                   "rough time", "hard time", "bad time", "going through", "crying", "cried",
                   "cries", "tears", "bad news", "having a hard", "not themselves", "in a rut",
                   "stressed", "devastated", "hurting", "in bits", "broken",
                   "shut down", "shutting down", "grieving", "lost their", "lost his",
                   "lost her", "whose", "died", "death", "ill", "unwell", "in hospital")

_SAID_IN_A_LANGUAGE = re.compile(
    r"\bin (?:welsh|cymraeg|irish|gaeilge|scots|gaelic|french|spanish|espanol|portuguese|italian|"
    r"german|deutsch|dutch|polish|russian|greek|turkish|arabic|hebrew|hindi|urdu|bengali|punjabi|"
    r"japanese|chinese|mandarin|cantonese|korean|thai|vietnamese|swedish|norwegian|danish|"
    r"finnish|icelandic|latin)\b"
    r"|\b(?:translate|translation|pronounce)\b")


def said_in_a_language(understood):
    text = (understood.get("clean") or understood.get("text") or "").lower()
    return bool(_SAID_IN_A_LANGUAGE.search(text))


ENTRIES = [
    entry("passive-aggressive-backhanded", (("passive aggressive", "passive-aggressive", "passive agressive",
                                  "passive agression", "passive aggression", "being passive"),
                                 ("mean", "means", "meaning", "what does", "what is", "why",
                                  "someone", "friend", "mum", "mother", "sister", "brother",
                                  "colleague", "boss", "partner", "husband", "wife",
                                  "coworker", "deal with", "handle", "respond", "reply")),
          "Passive aggression is anger shown by what a person does not say: a flat 'fine', a sigh, "
          "a joke with an edge, being left out of the group chat, help that quietly stops. Treat it "
          "as anger that hasn't found words and name the behaviour once, plainly: 'You seemed "
          "annoyed when I said that - did it land badly?' Ask about the thing, not the tone, and "
          "don't answer it in kind; matching the silence is what turns a week into a year."),
    entry("off-with-me", (("friend", "friends", "mate", "bestie", "sister", "brother",
                           "colleague", "mum", "mother", "dad", "father", "they", "he", "she",
                           "someone", "somebody", "husband", "wife", "partner", "boyfriend",
                           "girlfriend",
                           "mrs", "missus", "oh", "hubby", "other half", "the wife",
                           "the husband", "fella", "lad", "bloke"),
                          ("off with me", "being off", "short with me", "snappy",
                           "cold with me", "distant with me", "weird with me", "off hand",
                           "offhand", "gone cold", "gone quiet with me", "annoyed", "upset",
                           "angry", "cross with me", "miffed", "pissed off", "not talking to me",
                           "ignoring me",
                           "mad at me", "mad with me", "furious with me", "furious at me",
                           "livid with me", "livid at me", "a mood with me", "hump with me",
                           "got the hump with me", "not happy with me", "angry with me",
                           "angry at me", "upset with me", "upset at me", "annoyed with me",
                           "annoyed at me", "cross at me", "mardy with me", "miffed with me",
                           "mad on me")),
          "Ask once, in your own words, and make it about them rather than a list of charges: "
          "'You seem a bit off with me - have I done something?' Then leave room for the answer. If "
          "they say nothing is wrong, take it at face value and carry on as normal; most of the "
          "time it is their week and not you, and a second and third 'are you okay?' is what makes "
          "it awkward.",
          avoid=("lent", "lend", "borrowed", "owes", "owe", "money", "quid", "birthday", "forgot",
                 "forgotten", "cancel", "cancelled", "canceled", "funeral", "died", "death",
                 "hospital", "cancer", "miscarriage", "pay rise", "promotion", "interview",
                 "secret santa", "gift", "present"),
          guard=lambda reading: not owns_the_deed(reading)),
    entry("cant-pay-back", (("can t pay", "cant pay", "cant pay me back", "can t pay me back",
                            "pay it back", "pay back", "pay me back"),
                            ("yet", "says", "said", "won t", "afford", "next month")),
          "Take yes for an answer and put a date on it: 'No problem — when do you think you can get "
          "me some of it?' A small amount you actually receive is better than a big promise you "
          "don't. If it happens twice, say plainly that you need a plan you can rely on.", bias=1,
          avoid=("i owe", "i still owe", "owe my", "owe him", "owe her", "owe them",
                 "i cant pay", "i can t pay")),
    entry("owe-friend-money", (("i owe", "i still owe", "owe my friend", "owe my mate",
                                "owe him", "owe her", "owe them", "cant pay it back",
                                "can t pay it back", "cant pay back", "cant afford to pay",
                                "cant pay", "can t pay", "pay my friend back", "pay him back",
                                "pay her back", "pay them back",
                                "havent paid", "haven't paid", "havnt paid", "havent payed",
                                "havent payed them", "not paid", "never paid",
                                "still havent paid", "still not paid", "i still owe them",
                                "owe them for", "owe him for", "owe her for"),
                               ("friend", "mate", "him", "her", "them", "back", "borrowed",
                                "lent", "tickets",
                                "cleaner", "window cleaner", "milkman", "babysitter",
                                "baby sitter", "childminder", "child minder", "nanny",
                                "tutor", "dog walker", "dogwalker", "hairdresser", "barber",
                                "gardener", "plumber", "electrician", "builder", "painter",
                                "decorator", "carer", "sitter", "driving instructor",
                                "piano teacher", "music teacher", "swimming teacher",
                                "handyman", "odd job", "man who fixed", "woman who cleans",
                                "tradesman", "roofer", "joiner", "locksmith", "mechanic")),
          "Say it before they have to ask, and bring a number, not just an apology: 'I haven't "
          "forgotten the money I owe you. I can't do it all at once, but I can give you some of it "
          "this month and the rest by the end of next.' Then do that — a small date you keep is "
          "worth more than a big one you miss.",
          bias=1),
    entry("forgive-someone", ((
        "forgive", "forgiving", "forgiveness", "forgave", "forgiven", "forgives",
        "forgiv", "4give",
        "should i forgive", "should i forgiv", "can i forgive", "do i forgive",
        "could i forgive", "is it ok to forgive", "is it ok not to forgive",
        "is it wrong to forgive", "is it weakness to forgive", "weak to forgive",
        "how do i forgive", "how to forgive", "how can i forgive", "how do you forgive",
        "cant forgive", "can t forgive", "cannot forgive", "wont forgive", "won t forgive",
        "able to forgive", "not forgiving", "never forgive", "to forgive someone",
        "forgive someone", "forgiving someone", "forgive and forget",
        "forgiving and forgetting", "forgiving the same", "same as forgetting",
        "forgiving mean", "means forgiving", "forgiveness mean", "worth forgiving",
        "i forgave", "i have forgiven", "i cant forgive", "i can t forgive",
        "i wont forgive", "i won t forgive", "i need to forgive", "i want to forgive",
        "i should forgive", "i will forgive", "i never forgive",
        "have to forgive", "must i forgive", "need to forgive", "to forgive",
        "long to forgive", "take to forgive", "forgive my", "forgave my", "forgiving my",
        "forgive him", "forgive her", "forgive them", "forgive the", "forgive that",
        "forgave him", "forgave her", "forgave them", "forgiving him", "forgiving her",
        "forgiveness is", "is forgiveness", "forgiveness has", "forgiveness takes",
        "hard to forgive", "forgive hard", "forgiving hard", "forgive someone who",
        "forgive a person", "forgive people", "forgive the person",
    )),
          "Forgiving is not saying it was fine, and it is not trusting them again: it is "
          "deciding to stop charging them for it, so the thing stops running your week. Do it as "
          "a decision rather than waiting to feel warm about them, and say what you are dropping "
          "- 'I am not bringing this up again, and I am not pretending it did not happen.' You "
          "can forgive someone and still keep them at arm's length, and nobody is owed the words "
          "back until they have said sorry.",
          bias=1,
          avoid=("myself", "my self", "for what i did", "for what i said", "i did it",
                 "my fault", "my own fault", "hate myself",
                 "plant", "plants", "houseplant", "houseplants", "garden", "gardening",
                 "recipe", "recipes", "pan", "pans", "saucepan", "meat", "chicken", "steak",
                 "cake", "bread", "pastry", "oven", "loan", "loans", "debt", "debts", "tax",
                 "parking", "fine", "fines", "student",
                 "affair", "affairs", "cheat", "cheated", "cheating", "unfaithful",
                 "slept with")),

    entry("forgive-yourself", ((
        "forgive myself", "forgiving myself", "forgive yourself", "forgiving yourself",
        "forgiveness myself", "cant forgive myself", "can t forgive myself",
        "cannot forgive myself", "never forgive myself", "not forgive myself",
        "let myself off", "forgave myself", "hate myself for", "beat myself up",
    )),
          "Forgiving yourself is not letting it slide: it is saying what you did plainly, making "
          "the amends you can, and then treating the debt as paid instead of re-running the "
          "court case every night. Pick the smallest real repair - the apology, the thing you "
          "would do differently - do it this week, and say privately that the next time you "
          "would act differently. If the same voice keeps going over it months later, that is "
          "worth talking through with someone.",
          bias=1),

    entry("friend-quiet", (("friend", "friends", "mate", "bestie"),
                           ("ignoring", "quiet", "not replying", "replying", "replied",
                            "not answered", "hasn t replied", "stopped replying", "distant",
                            "gone quiet", "no reply",
                            "isn t talking to me", "isnt talking to me", "not talking to me",
                            "wont talk to me", "won t talk to me", "stopped talking to me",
                            "isn t speaking to me", "isnt speaking to me", "not speaking to me",
                            "wont speak to me", "won t speak to me", "stopped speaking to me",
                            "havent heard from", "haven t heard from", "not heard from",
                            "no word from", "gone silent", "blanked me", "blocked me",
                            "has blocked me", "avoiding me", "off with me",
                            "text me back", "texted me back", "text back", "texted back",
                            "hasnt text", "havent text", "havent texted", "not texted",
                            "not text back", "no text back", "not texting", "stopped messaging",
                            "not messaged")),
          "Ask once, plainly and without accusation: 'I haven't heard from you in a while — are you "
          "okay?' Then give it time. People go quiet for their own reasons, and one warm message "
          "beats three worried ones.",
          avoid=("lent", "lend", "borrowed", "owes", "owe", "paid me back", "pay me back",
                 "money", "quid", "pounds", "tenner", "fiver", "deposit"),
          guard=lambda reading: not owns_the_deed(reading)),
    entry("ask-whats-wrong",
          (("ask her", "ask him", "ask them", "what s wrong", "whats wrong",
            "what do i say", "should i say", "what to say",
            "ask what", "ask if", "how to ask", "how do i ask"),
           ("friend", "annoyed", "upset", "off with me", "big thing", "row", "distant",
            "ignoring me", "isn t talking", "seems off")),
          "Make it a question about them, not an accusation: 'You seem a bit off with me \u2014 have I "
          "done something?' Say it once, in person or on the phone, not in a long message. If they "
          "say nothing is wrong, believe them and carry on normally; people often need a day before "
          "they can say it.",
          avoid=("died", "death", "passed away", "funeral", "grief", "bereave", "cancer",
                 "miscarriage", "hospital", "griev", "loss", "lost her job", "lost his job", "lost her mum",
                 "lost his dad", "fired", "redundant", "laid off", "lend", "borrow", "pay rise",
                 "promotion", "owe", "pay back", "pay it back", "money", "pounds", "quid",
                 "back", "cant pay", "can t pay", "bring it up", "brought it up", "broach",
                 "mention", "mentions", "raise it", "ruining",
                 "cook", "cooking", "cooked", "bake", "baking", "food", "meal", "dish",
                 "recipe", "pastry",
                 "turns into a row", "turns into an argument", "turns into a fight",
                 "always ends in", "partner", "husband", "wife", "boyfriend", "girlfriend",
                 "my mum", "my mother", "my dad", "my father", "my son", "my daughter",
                 "my kids", "the kids",
                 "birthday", "forgot", "forgotten", "missed",
                 "cancel", "cancelled", "canceled", "cancels", "cancelling", "bailed",
                 "let me down", "no show",
                 "space", "some space", "need space", "some room"),
          guard=lambda reading: not owns_the_deed(reading)),
    entry("introduce-friends",
          (("introduce", "introducing", "introduction", "introduce them", "introduce two"),
           ("friends", "friend", "friends who", "people", "each other", "two friends", "them",
            "how", "best", "awkward", "what do i say", "say")),
          "Give each one a reason to be pleased to meet the other - \"Sam, this is Priya, she runs "
          "the same ridiculous hill route as you\" - and then give them something to do with each "
          "other, even a question you are also part of. Say a little about what each does so nobody "
          "has to audition, and stay for the first few minutes rather than leaving them alone.",
          avoid=("myself", "me to", "yourself", "introduce me",
                 "baby", "babies", "newborn", "toddler", "toddlers", "sibling", "siblings",
                 "puppy", "puppies", "kitten", "kittens", "new dog", "new cat", "resident dog",
                 "resident cat", "to the dog", "to the cat", "to our dog", "to our cat",
                 "stepchild",
                 "a dog", "the dog", "our dog", "my dog", "two dogs", "dogs to", "my dogs",
                 "our dogs", "the dogs", "a cat", "the cat", "our cat", "my cat", "two cats",
                 "cats to", "my cats", "our cats", "the cats", "a puppy", "two puppies",
                 "a rabbit", "the rabbits", "my rabbit", "a guinea pig", "a hamster",
                 "a budgie", "a parrot", "a horse", "a pony", "two pets",
                 )),
    entry("better-listener",
          (("listener", "listen better", "listen well", "listening", "listen properly",
            "a better listener", "good listener", "bad listener", "interrupt", "interrupts",
            "interrupting", "talk over", "talks over"),
           ("how", "better", "be", "become", "am i", "do i", "advice", "tips", "learn",
            "he says", "she says", "they say", "people say", "says i")),
          "Stop preparing your reply while they are still talking: most of us are half a sentence "
          "ahead, and people can hear it. Then say back what you heard in one line - \"so the "
          "meeting went badly and your boss blamed you\" - before you offer anything, and ask one "
          "follow-up question instead of topping up with your own story. Sit still and leave a "
          "second of silence after they stop; that gap is usually where the real thing gets said.",
          avoid=("hearing", "hearing aid", "deaf", "ear", "tinnitus", "quiet", "ignoring",
                 "not replying", "podcast", "audiobook", "music", "radio", "tv", "speaker",
                 "headphones", "eavesdrop", "neighbour", "neighbor", "landlord",
                 "my friend talks over me", "over me", "cuts me off", "cut me off",
                 "interrupts me", "interrupting me", "keeps interrupting", "talks over my",
                 "every five minutes", "all day", "anything done", "get anything done",
                 "open plan", "open-plan", "phone",
                 "iphone", "android", "alexa", "echo", "siri", "microphone", "ads", "adverts",
                 "spying", "recording", "listening to me", "google home")),

    entry("text-after-date",
          (("text", "texting", "text back", "texted", "message", "reply",
            "call after", "calling after", "phone after", "phoning after", "ring after"),
           ("first date", "after a date", "after the date", "a date", "dating", "matched",
            "tinder", "hinge", "bumble", "how long should i wait", "wait before")),
          "Text the same evening or the next morning. There is no waiting rule worth playing, and "
          "a day of silence reads as disinterest rather than mystery. Say something specific - "
          "'still thinking about that story about the ferry' - and end with a question or a plan, "
          "so it is easy to answer in one line. If nothing comes back, one follow-up after a few "
          "days is fine and then leave it: no reply is a reply.",
          avoid=("my ex", "my mum", "my dad", "boss", "work", "landlord", "doctor", "school",
                 "girlfriend", "boyfriend", "wife", "husband", "bank")),
    entry("cheer-someone-up",
          (("cheer up", "cheered up", "cheering up", "cheer him up", "cheer her up",
            "cheer them up", "cheer my",
            "cheer someone up", "cheer somebody up", "cheer a friend up", "cheer up someone",
            "cheer up a friend", "cheer up my", "cheer their",
            "comfort", "comforting", "console", "consoling",
            "feel better", "feel any better", "make them feel", "make her feel", "make him feel",
            "do something nice for", "something nice for", "what can i do for",
            ),
           ("friend", "best friend", "mate", "bestie", "mum", "mother", "mam", "dad",
            "father", "parent", "parents", "sister", "brother", "partner", "husband",
            "wife", "boyfriend", "girlfriend", "son", "daughter", "child", "someone",
            "him", "her", "them", "person", "somebody", "colleague", "neighbour", "neighbor"),
           ("sad", "sadness", "down", "low", "upset", "unhappy", "miserable", "struggling",
            "rough time", "hard time", "bad time", "going through", "crying", "cried",
            "cheer up", "comfort", "bad news", "having a hard", "not themselves",
            "in a rut", "stressed")),
          "Small and specific beats big and vague. Send one message today saying you have been "
          "thinking of them, then offer a fixed thing: \"I'll bring dinner on Thursday\" or \"walk "
          "on Sunday?\" rather than \"let me know if you need anything\". Ask whether they want "
          "company or quiet before you turn up, and do not tell them to cheer up - being told to "
          "feel better is the one thing that never works.",
          ask=("cheer up", "cheered up", "cheering up", "cheer him up", "cheer her up",
               "cheer them up", "cheer my", "cheer someone up", "cheer somebody up",
               "cheer a friend up", "cheer up someone", "cheer up a friend", "cheer up my",
               "comfort", "comforting", "console", "consoling",
               "feel better", "feel any better", "make them feel", "make her feel",
               "make him feel", "do something nice for", "something nice for", "what can i do for",
               "what do i say", "what can i say", "what should i say",
               "rough time", "hard time", "bad time", "going through", "having a hard time"),
          avoid=("died", "death", "passed away", "funeral", "grief", "bereave", "burial",
                 "cancer", "miscarriage", "hospital", "diagnosis", "suicide", "killed",
                 "birthday", "birthdays", "80th", "70th", "90th", "anniversary", "retirement",
                 "lost", "loss", "losing", "gone", "widow", "widowed", "ill", "sick",
                 "hospice", "carer", "grieving", "grieves", "grieved", "bereavement",
                 "angry", "annoyed", "off with me", "row", "argument", "falling out",
                 "furious", "ignoring me", "ignores me", "owes", "owe", "borrow", "lent",
                 "money", "pay back", "birthday", "forgot",
                 "gift", "present", "presents", "buy", "buying", "what should i get",
                 "christmas", "anniversary"),
          guard=_not_a_plain_gesture),
    entry("help-someone-through", (HELPING_ASK, HELPING_PERSON),
          ("Be there before you fix anything: say the plain thing - \"that's really hard, I'm "
           "sorry\" - and then ask what they need today, company or quiet. A fixed offer helps "
           "more than an open one (\"I'll bring dinner on Thursday\", \"walk on Sunday?\"), and "
           "the message tomorrow, when the first day's fuss has died down, is the one they "
           "remember. If it has been weeks and they have stopped seeing anyone or stopped "
           "eating, say so plainly and help them book a GP appointment."),
          ask=HELPING_TROUBLE, bias=1,
          avoid=("reading", "homework", "maths", "math", "spelling", "revision", "exam",
                 "seem", "seems", "seemed", "acting", "noticed", "notice",
                 "let", "letting", "feel", "feels", "feeling", "felt", "guilt", "guilty",
                 "housework", "cleaning", "bins", "move house", "moving house", "downsize",
                 "job", "cv", "benefits", "allowance", "dementia", "phone", "laptop", "wifi",
                 "barking", "diet", "weight", "paperwork", "tax", "passport", "bins",
                 "suicide", "funeral", "eulogy", "miscarriage")),
    entry("a-favour-i-said-yes-to",
          (("said id", "said i would", "said i'd", "said i will", "promised", "agreed",
            "agreed to", "volunteered", "offered to", "said yes", "said yes to",
            "said yes when",
            "id"),
           ("help", "favour", "favor", "move", "moving", "lift", "babysit", "babysitting",
            "childcare", "paint", "decorate", "drive", "collect", "pick up", "house sit",
            "dog sit", "fix")),
          "Say it early, before they plan around you: \"I'm sorry - I said I'd help, but I'm not "
          "going to be able to.\" You don't owe a detailed reason; if you want to soften it, offer "
          "something smaller you can still do (\"I can drop the keys round on Friday\"). Don't "
          "leave it to the last minute, and don't say yes again to be kind - a clear no "
          "now is easier on them than a no then.",
          ask=("dont want", "don't want", "not want", "cant face", "can't face", "couldnt face",
               "couldn't face", "regret", "dreading", "dread", "rather not", "changed my mind",
               "wish i hadnt", "wish i hadn't", "no longer want", "dont fancy", "don't fancy"),
          avoid=("boss", "manager", "colleague", "work", "job", "office", "client", "shift",
                 "overtime", "meeting", "deadline"),
          bias=1),
    entry("meet-parents", (("parents", "family"), ("partner", "meet", "meeting", "first time")),
          "Take something small for the house, ask them questions about themselves, and don't try "
          "to impress — be interested and easy. Offer to help with the washing up; it's the "
          "cheapest way to be liked.",
          guard=_not_cooking_for_them),
    entry("ask-someone-out",
          (("ask out", "asking out", "asked out", "ask her out", "ask him out", "ask them out",
            "ask a girl out", "ask a boy out", "ask a guy out", "ask a lad out", "ask a man out",
            "ask the guy out", "ask the girl out", "ask someone out", "ask out my crush",
            "ask my crush out", "ask her on a date", "ask him on a date", "on a date",
            "out on a date", "first date",
            "chicken out", "chickening out", "chickened out", "get cold feet",
            "want to ask out", "want to ask her out", "want to ask him out",
            "talk to a girl i like", "talk to a boy i like", "talk to a guy i like",
            "someone i like", "somebody i like"),
           ("how", "should", "do i", "help", "nervous", "scared", "terrified", "chance",
            "way", "best", "do it", "pluck up", "brave",
            "shy", "too shy", "shyness", "embarrassed",
            "want", "wants", "wanted", "keep", "keeps", "kept", "cant", "can't", "cannot",
            "afraid", "frightened",
            "ask her", "ask him", "ask them", "asking her", "asking him", "asking them",
            "ask someone", "ask a girl", "ask a boy", "ask a guy", "crush", "out with",
            "on a date", "first date")),
          "Make it a small, specific invitation rather than a confession: \"I like talking to you - "
          "do you fancy a coffee on Saturday?\" Name a day and a thing, ask in person or in one "
          "short message, then leave it with them - the answer is theirs to give. A no is "
          "information, not a verdict: \"no worries, see you Thursday\", said warmly and meant, is "
          "what keeps the friendship. The only real mistake is the speeches.",
          ask=("how", "should", "do i", "what", "way", "best", "nervous", "scared",
               "chance", "help", "brave", "shy", "too shy", "shyness", "embarrassed",
               "want", "wants", "wanted", "chicken out", "chickening out", "chickened out"),
          avoid=("wear", "wearing", "outfit", "clothes", "dress", "shoes", "hair",
                 "restaurant", "wedding", "tax return", "use by", "best before", "expired",
                 "out of date", "throw out",
                 "done", "cooked", "cook", "cooking", "raw", "oven", "roast", "roasting",
                 "juices", "thermometer", "thaw", "defrost", "fridge", "freezer", "meat",
                 "temperature", "left out", "gone off",
                 "spatchcock", "joint", "jointing", "butterfly", "soup", "stock", "carcass",
                 "bone", "bones", "boneless", "skin", "skinless", "breast", "breasts",
                 "thigh", "thighs", "drumstick", "drumsticks", "wing", "wings", "nuggets",
                 "marinade", "marinated", "marinating", "marinate", "rub", "brine", "brining",
                 "drying out", "dry out", "dries out", "juicy", "tender",
                 "chicken fresh", "meat fresh", "keep it fresh", "keep them fresh",
                 "keep food fresh", "chicken in the fridge", "chicken in the freezer",
                 "poach", "poaching", "boil", "boiling", "grill", "grilling", "bake", "baking",
                 "barbecue", "bbq", "air fryer", "slow cooker", "curry", "tikka", "kebab",
                 "casserole", "traybake", "pie", "gravy", "stuffing", "sandwich", "wrap",
                 "salad", "pasta", "rice", "noodles", "stir fry", "stir-fry",
                 "text", "texts", "texting", "message", "messages", "messaging", "reply",
                 "replies", "wait", "how long", "chase", "ghosted",
                 "song", "songs", "playlist", "playlists", "tune", "tunes", "album", "albums",
                 "music", "band", "bands", "film", "films", "movie", "movies", "series",
                 "podcast", "podcasts", "book", "books", "novel", "poem", "poems", "quote",
                 "quotes", "gift", "gifts", "present", "presents",
                 "take the chicken out", "take a chicken out", "get the chicken out",
                 "taking the chicken out", "the chicken out of", "forgot to take",
                 "forget to take", "forgetting to take",
                 ) + KEEP_QUALITY_WORDS),

    entry("friend-busy",
          (("friend", "friends", "friendship", "mate", "mates", "friendships"),
           ("busy", "no time", "hard to keep", "keep in touch", "drifted", "drift", "drifted apart",
            "lost touch", "losing touch", "catch up", "see each other", "distance",
            "long distance", "kids", "work")),
          "Stop waiting for a free evening and put a small, regular thing in the diary instead: a "
          "twenty-minute call every second Sunday, or a walk at the same time each month. Say why "
          "you are doing it - 'I miss you, and I am bad at this, so I am booking us in' lands "
          "better than a vague let's catch up. Voice notes between times keep the thread alive, "
          "and doing one small favour beats a grand plan you both cancel.",
          ask=("busy", "time", "keep", "touch", "drifted", "drift", "lost", "losing", "catch up",
               "see each other", "distance"),
          avoid=("ignoring", "quiet", "not replying", "owes", "owe", "lent", "money", "parents",
                 "partner", "wedding", "argument", "fell out",
                 "died", "dies", "dying", "death", "dead", "passed away", "passing", "funeral",
                 "buried", "burial", "killed", "kill", "suicide", "grief", "grieving", "loss",
                 "lost him", "lost her", "lost them", "miss him", "miss her", "miss them",
                 "keep going over", "going over",
                 "over the last", "cant stop thinking", "can't stop thinking")),
    entry("keep-a-conversation-going",
          (("conversation", "chat", "small talk", "talking", "talk", "chatting",
            "nothing to say", "things to say", "silences", "silence", "stranger", "strangers"),
           ("keep going", "keep it going", "keep a conversation going", "keep a chat going",
            "keep the chat going", "keep chatting", "keep talking", "chat going", "going", "start",
            "starting", "starter", "starters", "open", "opening", "awkward", "silence",
            "nothing to say", "run out of things", "run out of", "dries up", "stalls",
            "stranger", "strangers", "someone new", "new people", "new person", "ice breaker",
            "icebreaker")),
          "Ask about the answer you just got instead of starting a new subject - \"how did that "
          "go?\" or \"what was the best bit?\" - because a conversation usually dies from "
          "answering and moving on, not from having nothing to say. Give a little of yourself so "
          "it is not an interview, and when the talk stalls offer something to look at or do: the "
          "weather lasts a line, a photo, a menu or a dog lasts ten minutes.",
          avoid=("end", "ending", "ends", "finish", "finishing", "leave", "leaving", "get out of",
                 "escape", "goodbye", "politely", "polite", "excuse myself", "job interview",
                 "interview", "row", "argument", "argue", "fell out", "ignoring", "break up",
                 "group chat", "unsubscribe", "mute",
                 "dying to", "everyone keeps", "film", "films", "movie", "movies", "series",
                 "binge", "episode", "episodes", "telly", "netflix",
                 "over me", "talks over", "talking over", "talked over",
                 "interrupts me", "interrupting me", "interrupt me", "interrupted me",
                 "ignores me", "ignoring me", "undermines me", "undermining me",
                 "shouts at me", "shouting at me", "yells at me", "yelling at me",
                 "takes credit", "taking credit")),
    entry("end-a-conversation-leave",
          (("conversation", "chat", "talking", "talk", "nattering", "small talk",
            "phone call", "call with", "speaking to", "chatting",
            "leave a party", "leave the party", "leaving a party", "leave early",
            "leaving early", "end a conversation", "end the conversation", "end a chat",
            "exit a conversation", "get out of a conversation", "slip away", "bow out",
            "say goodbye", "get off the phone", "getting off the phone", "get off a call",
            "get off this call",
            "get off a phone call", "get off the call", "get off the call politely",
            "off a phone call"),
           ("end", "ends", "ending", "finish", "finishing", "politely", "polite", "get away",
            "get out of", "escape", "leave", "leaving", "stop", "stuck", "wont stop", "won't stop",
            "get off", "getting off", "hang up", "hanging up", "ring off",
            "gracefully", "excuse myself", "end it", "cut it short",
            "wrap it up",
            "leave a party", "leave the party", "leaving a party",
            "slip away", "slipping away", "end a chat", "end the chat", "end a conversation",
            "end the conversation", "exit a conversation", "get out of a conversation",
            "make my excuses", "bow out", "say goodbye", "get going"),
           ("goodbye", "goodbyes", "bye", "excuses", "early", "slip away", "bow out",
            "head off", "go home", "get going", "sign off",
            "end", "ends", "ending")),
          "Close it with a reason and a warm line rather than fading out: name the thing you have "
          "to get to, say one true thing about the conversation, then go. \"I'm going to have to "
          "head off - I'm so glad you told me about the job\" or \"Right, I'd better get on, but "
          "it was good to catch up.\" Give the reason first, because people hear the reason as "
          "respect, and keep it about the time rather than the person. If someone is mid-ramble, "
          "wait for a full stop and step in with their name; if you are on the phone, stand up and "
          "say you have to go. End with something that opens the next time - \"next week?\", "
          "\"text me when you hear\" - so it reads as a pause and not a brush-off.",
          ask=("conversation", "conversations", "chat", "chats", "chatting", "talk", "talking",
               "small talk", "nattering", "phone", "call", "calls", "speaking to", "party",
               "parties", "goodbye", "goodbyes", "bye", "excuses", "bow out", "slip away",
               "head off", "go home", "get going", "sign off", "visit", "guests", "guest"),
          guard=lambda understood: not said_in_a_language(understood),
          avoid=TALKING_IS_NOT_A_CHAT + (
                 "spanish", "espanol", "español", "french", "francais", "français", "italian",
                 "german", "deutsch", "welsh", "cymraeg", "irish", "gaeilge", "gaelic",
                 "translate", "translation", "what does",
                 "argument", "argue", "row", "fell out", "ignoring", "not replying", "quiet",
                 "overthinking", "overthink", "over thinking", "replaying", "replay",
                 "going round in my head", "goes round in my head", "dwell", "dwelling",
                 "ruminating", "ruminate", "cant stop thinking", "can't stop thinking",
                 "stopped speaking to me", "stopped talking to me", "stopped texting me",
                 "isnt speaking to me", "isn t speaking to me", "isnt talking to me",
                 "isn t talking to me", "wont speak to me", "won t speak to me",
                 "wont talk to me", "won t talk to me", "havent spoken to me",
                 "haven t spoken to me", "hasnt spoken to me", "not speaking to me",
                 "not talking to me", "not on speaking terms",

                 "party", "parties", "a do", "gathering", "drinks", "dinner", "barbecue",
                 "bbq", "celebration", "host", "night out", "leaving do",
                 "break up", "breakup", "broke up", "dumped", "divorce", "dating", "date",
                 "flirting", "crush", "shy", "nervous", "anxious", "bad caller",
                 "a girl i like", "a boy i like", "someone i like", "somebody i like",
                 "ask her out", "ask him out", "ask them out", "fancy", "fancies",
                 "feelings", "my feelings", "emotions", "how i feel", "money", "parents",
                 "my parents", "his parents", "her parents",
                 "cold caller", "scam", "voicemail", "email", "letter", "text", "message",
                 "wrong number", "job", "shift", "hospital", "country", "flat", "house",
                 "tenant", "landlord",
                 "in spanish", "in french", "in italian", "in german", "in portuguese",
                 "in greek", "in turkish", "in welsh", "in japanese", "in chinese",
                 "in mandarin", "in dutch", "in polish", "in russian", "in arabic",
                 "translate", "translation",
                 "talk to my son about", "talk to my daughter about", "talk to my child about",
                 "talk to my kid about", "talk to my children about", "talk to my kids about",
                 "talk to my teenager about", "talk to my boy about", "talk to my girl about",
                 "speak to my son about", "speak to my daughter about",
                 "talk to him about", "talk to her about", "talk to them about",
                 "work", "office", "school", "term", "annual leave", "time off", "holidays",
                 "workload", "workloads", "workloads of", "my workload",
                 "group chat", "group message", "group conversation", "whatsapp", "telegram",
                 "signal", "messenger", "instagram", "facebook", "the group", "group",
                 "leave the group", "exit group", "unsubscribe", "mute", "muted",
                 "notifications",
                 "keep going", "keep it going", "keep a conversation going",
                 "keep the conversation going", "keep talking", "nothing to say",
                 "run out of things", "awkward silence", "small talk", "conversation starter",
                 "start a conversation", "start the conversation", "keep a chat going",
                 "keep the chat going", "keep chatting", "chat going", "stranger", "strangers",
                 "someone new", "new people", "nothing to say", "things to say",
                 "say no", "saying no", "say yes", "no without", "without sounding",
                 "sounding like", "turn down", "turn them down", "refuse",
                 "keep a conversation going", "keep the conversation going", "keep talking",
                 "keep a chat going", "keep the chat going", "start a conversation",
                 "start the conversation", "conversation starter", "things to say",
                 "nothing to say", "make conversation", "talk to people", "talk to anyone",
                 "small talk", "make small talk", "making small talk", "mingle", "mingling",
                 "networking", "networking event", "know nobody", "knows nobody",
                 "party", "parties", "a do", "gathering", "drinks", "dinner",
                 "awkward silences", "silences",
                 "start a difficult", "start the difficult", "start a hard", "start a awkward",
                 "have a difficult conversation", "have a hard conversation",
                 "have the difficult conversation", "handle a difficult conversation",
                 "handle a hard conversation", "bring up a difficult conversation",
                 "bring up a hard conversation",
                 "confront", "confronting", "confrontation",
                 "have it out", "bring it up"), bias=1),
    entry("make-my-excuses",
          (("make my excuses", "made my excuses", "making my excuses"),
           ("leave", "leaving", "go", "going", "head off", "get away", "slip away", "exit")),
          "Close it with a reason and a warm line rather than fading out: name the thing you have "
          "to get to, say one true thing about the time, then go. \"I'm going to have to head "
          "off - I'm so glad we got to talk\" or \"I'd better get on, but it was really good to "
          "catch up.\" Have your reason ready in one line because the next question is always "
          "why, and don't apologise twice; leaving when you said you would is kinder than "
          "drifting about waiting for a gap.",
          ask=("how do i", "how to", "what do i say", "what should i say", "what can i say",
               "ways to", "way to"),
          avoid=("party", "parties", "a do", "gathering", "drinks", "dinner", "barbecue",
                 "bbq", "celebration", "night out", "wedding", "funeral", "meeting",
                 "interview", "date", "phone", "call", "calls", "work", "office", "school",
                 "boss", "landlord", "customer", "client", "because i", "for being late",
                 "are rubbish", "always", "never")),
    entry("hard-conversation",
          (("difficult conversation", "hard conversation", "awkward conversation",
            "tricky conversation", "uncomfortable conversation", "have it out",
            "bring something up", "bring it up", "confront", "confronting", "confrontation",
            "tell them how i feel", "tell her how i feel", "tell him how i feel",
            "how i feel", "say how i feel", "how i really feel",
            "feelings", "my feelings", "emotions", "my emotions", "open up", "opening up",
            "share my feelings", "share how i feel"),
           ("how", "do i", "should", "can", "what", "start", "handle", "say", "tell", "approach",
            "friend", "friends", "mate", "sister", "brother", "partner", "husband", "wife",
            "boyfriend", "girlfriend", "mum", "dad", "mother", "father", "flatmate", "someone",
            "about something", "nervous", "dread", "awkward")),
          "Ask for ten minutes at a calm time, then say it in one sentence with one example: "
          "\"when you cancelled on Friday it felt like I didn't matter\" lands, while \"you "
          "always cancel\" starts a fight. Say what you want to change rather than what they did "
          "wrong, let them answer once without interrupting, and finish by agreeing what happens "
          "next time.",
          avoid=("end a conversation", "end the conversation", "end a chat", "leave a party",
                 "dizzy", "dizziness", "light headed", "lightheaded", "faint", "fainting",
                 "nauseous", "nausea", "vomit", "sick", "queasy", "shaky", "weak",
                 "breathless", "short of breath", "chest pain", "palpitations", "pins and needles",
                 "headache", "headaches", "migraine", "sore", "ache", "aching", "pain", "hurts",
                 "hurt", "tired", "exhausted", "sleepy", "bloated", "constipated", "itchy",
                 "rash", "cramp", "cramps", "swollen", "numb", "stiff", "stressed", "anxious",
                 "low", "down", "depressed", "nervous about the", "panic",
                 "overthinking", "overthink", "over thinking", "replaying", "replay",
                 "going round in my head", "goes round in my head", "in my head",
                 "dwell", "dwelling", "ruminating", "ruminate", "cant stop thinking",
                 "can't stop thinking", "keep thinking about",
                 "food", "eating", "ate", "meal", "meals", "diet", "weight", "calories",
                 "guilty about food", "guilt about food", "binge", "bingeing",
                 "tired", "exhausted", "exhausting", "no energy", "always sleepy", "sleepy",
                 "fatigue", "fatigued", "worn out", "run down", "lethargic",
                 "say goodbye", "leave early", "get away", "politely",
                 "end", "ends", "ending", "finish", "finishing", "get out of", "excuse myself",
                 "bow out", "walk away", "cut it short", "stop talking", "wind it up",
                 "argument", "argue", "row", "shouting", "fell out", "not talking",
                 "appraisal", "pay rise", "redundancy", "resign", "dismissal", "grievance",
                 "word it", "what do i say", "what should i say", "draft", "email", "text",
                 "message",
                 "for him", "for her", "for them", "have feelings", "caught feelings",
                 "in love", "crush", "attracted"),
          guard=_names_a_person_and_is_not_a_deed),
    entry("say-where-the-line-is",
          (("boundaries", "boundary", "set limits", "limits with", "clear limits", "limits on",
            "draw the line", "the line is", "put my foot down", "stand up for myself",
            "stand up to", "keeps doing it", "does not respect", "doesnt respect",
            "wont respect", "won't respect", "walks all over", "takes advantage"),
           ("partner", "husband", "wife", "boyfriend", "girlfriend", "fiance", "fiancee",
            "flatmate", "flat mate", "housemate", "roommate", "friend", "friends", "mate",
            "sister", "brother", "sibling", "colleague", "coworker", "co worker", "brother in law",
            "sister in law", "in law", "in laws", "family", "someone", "him", "her", "them",
            "people")),
          ("Name the one thing, in a sentence, and say what you will do rather than what they "
           "must stop: \"I'm not lending money again\" lands where \"you take advantage of me\" "
           "starts a fight. Pick the boundary that matters most this week, say it once when "
           "nothing is being argued about, and expect to say it twice before it holds. Then keep "
           "the consequence yourself - a limit nobody follows through on is a suggestion - and "
           "let the smaller stuff go, because five boundaries kept beat twenty announced."),
          bias=1,
          avoid=("mum", "mother", "dad", "father", "parents", "parent", "stepmum", "stepdad",
                 "nana", "gran", "grandma", "grandad", "mother in law", "mother-in-law",
                 "child", "children", "kid", "kids", "son", "daughter", "toddler", "teenager",
                 "baby", "boss", "manager", "landlord", "tenant", "neighbour", "neighbor",
                 "dog", "cat", "sleep", "bedtime", "rent", "money", "deposit", "contract",
                 "work hours", "overtime", "nights")),
    entry("turn-down-a-drink",
          (("refuse a drink", "refuse a glass", "refuse wine", "refuse alcohol", "refuse booze",
            "refuse another", "refuse the drink", "refuse drinks", "refusing a drink",
            "turn down a drink", "turn down a glass", "turn down drinks",
            "turned down a drink", "turning down a drink",
            "say no to a drink", "say no to drinks", "say no to alcohol", "say no to wine",
            "say no to the drink", "say no to another drink", "say no to booze",
            "saying no to a drink", "decline a drink", "decline the drink", "decline drinks",
            "declining a drink",
            "not drink at", "not drink when", "not drink with", "not drink and",
            "not drink in front", "not drinking",
            "without drinking", "avoid drinking", "stopped drinking", "giving up drinking",
            "non drinker", "non-drinker", "teetotal", "sober", "keep buying me",
            "keeps buying me", "keeps buying", "buying me", "buys me", "buy me"),
           ("drink", "drinks", "drinking", "wine", "beer", "pint", "pints", "shot",
            "shots", "alcohol", "booze", "lager", "cider", "prosecco", "cocktail",
            "cocktails", "spirits", "vodka", "gin", "whisky", "whiskey", "a round",
            "rounds", "glass", "pub", "party", "wedding", "christening", "after work",
            "work do", "night out", "hen do", "stag do", "meal", "dinner")),
          "Have the line ready before the glass arrives: 'Not for me, thanks - I'm on the lime "
          "and soda.' Four words, said with a smile, and then ask them something, because a "
          "reason at a table is an invitation to be talked round. Keep a soft drink in your hand "
          "- people top up a full glass far less - and if a round lands in front of you anyway, "
          "leave it or pass it on rather than argue. When someone presses, use the same sentence "
          "again, then name it once, quietly and only to them: 'I don't drink - it's boring, but "
          "it's easier if you don't buy me one.' Two no's from the same person is not rude; it is "
          "what stops the third.",
          avoid=("how much", "how many units", "units", "cut down", "cutting down", "reduce",
                 "give up", "quit", "stopping", "stop drinking", "withdrawal", "shakes",
                 "liver", "alcoholic", "alcoholism", "dependent", "addiction", "help me stop",
                 "am i drinking", "too much", "my husband", "my wife", "my partner", "my dad",
                 "my mum", "my son", "my daughter", "my friend drinks", "buy a", "buying a",
                 "cheapest", "price of", "calories", "syns", "units in",
                 "my cat", "my dog", "my pet", "my puppy", "my kitten", "cat is", "dog is",
                 "cat has", "dog has", "cat wont", "dog wont", "kitten", "puppy", "vet",
                 "hamster", "rabbit", "guinea pig", "parrot", "fish tank", "litter tray",
                 "horse", "horses", "pony", "ponies", "donkey", "donkeys", "goat", "goats",
                 "sheep", "cow", "cows", "livestock", "stable", "trough",
                 "rat", "rats", "mouse", "mice", "gerbil", "gerbils", "degu", "degus",
                 "chinchilla", "chinchillas", "ferret", "ferrets", "hedgehog", "hedgehogs",
                 "budgie", "budgies", "tortoise", "tortoises", "lizard", "snake",
                 "pudding", "puddings", "dessert", "desserts", "cake", "cakes", "seconds",
                 "second helping", "another helping", "a helping of", "portion", "food",
                 "chips", "sweets", "chocolate", "biscuits", "left out", "left behind",
                 "chips", "sweets", "chocolate", "biscuits", "left out", "left behind",
                 "excluded", "everyone else", "second helping", "another helping",
                 "invite", "invited", "invitation", "invitations", "bridesmaid", "wedding day",
                 "stag", "hen party",
                 "water", "hydrat",
                 "excluded", "the only one not", "everyone else"),
          bias=1),
]

ENTRIES += [
    entry("polite-distance",
          (("ignore someone", "ignoring someone", "ignore him", "ignore her", "ignore them",
            "avoid someone", "avoiding someone", "avoid him", "avoid her", "avoid them",
            "avoid a neighbour", "avoid my neighbour", "avoid a colleague", "avoid my colleague",
            "avoid my in laws", "avoid my in-laws", "avoid a person", "dodge someone",
            "dodge a neighbour", "dodge my neighbour", "dodge him", "dodge her", "dodging him",
            "brush off", "brush them off", "brush him off", "brush her off", "sidestep someone",
            "evade someone", "get away from someone", "keep someone at arm", "at arms length"),
           ("rude", "politely", "polite", "without being", "nicely", "discreetly", "kindly",
            "how do i", "how to", "without upsetting", "at work", "neighbour", "neighbor",
            "colleague", "in law", "in laws", "someone")),
          "Don't blank them - be brief, dull and busy, which is easier to keep up than avoidance "
          "and gives them nothing to push against. Answer in a sentence, ask nothing back, do not "
          "laugh at the jokes, and keep your hands occupied or your coat on. \"I can't stop, I'm "
          "just heading in\" works every time, and stepping away while you say it ends the "
          "exchange. If it is someone you cannot move away from, sit at the end of the row and "
          "arrive a minute late rather than making a thing of it.",
          avoid=("ignore my", "ignore him", "ignore the", "ignoring my", "text", "message",
                 "call", "email", "notification", "warning light", "error", "dog", "baby",
                 "toddler", "child", "customer complaint", "ignore a",
                 "question", "questions", "answering", "answering the")),
    entry("decline-a-date-kindly",
          (("second date", "third date", "another date", "asked me out again",
            "dont want to see them again", "don't want to see them again",
            "dont want to see him again", "don't want to see him again",
            "dont want to see her again", "don't want to see her again",
            "see them again", "tell someone i dont want", "tell them i dont want",
            "ask me out again", "asked me out", "asks me out", "wants to meet again",
            "wants to see me again", "wants a second date", "dont want a second date",
            "don't want a second date", "turn him down", "turn her down", "turn them down",
            "let him down", "let her down", "let them down", "end it after one date",
            "after the first date", "had one date", "went on one date", "one date and",
            "not interested in him", "not interested in her", "not interested in them",
            "no spark", "no chemistry", "didnt feel a spark", "didn't feel a spark"),
           ("nicely", "polite", "politely", "without hurting", "without being mean", "not mean",
            "how", "what do i say", "what should i say", "what to say", "words", "text",
            "message", "reply", "respond", "ghost", "ghosting", "ignore", "badly", "kind")),
          ("Say it plainly, kindly and early - a text the same evening or the next day is not "
           "rude, and leaving it unanswered is: \"I enjoyed meeting you, but I'm not feeling a "
           "romantic connection, so I don't want to lead you on.\" Keep it about you rather than "
           "about them, because \"you're not my type\" invites an argument and \"no spark\" does "
           "not. No long explanation, no apology for the feeling, and no offer of friendship you "
           "do not mean. Then do not reply to the pushback."),
          ask=("how", "what", "say", "said", "saying", "text", "message", "reply", "words",
               "nicely", "polite", "politely", "him", "her", "them", "someone")),
]

ENTRIES.append(entry(
    "bot-can-i-trust-you",
    (("trust", "trusts", "rely on", "count on"),
     ("you", "u", "chatbot", "bot", "your advice", "your answer", "your judgement",
      "your judgment", "this chatbot")),
    "Yes, for everyday questions: I give you my best answer and say when I am not sure. Check "
    "anything that matters - a diagnosis, money, a legal deadline - with someone qualified, "
    "because I can be wrong.",
    ask=("trust", "rely on", "count on"),
    avoid=("trust fund", "trust him", "trust her", "trust them", "trustworthy", "trust a",
           "trust my", "trust the", "trust it")))

ENTRIES.append(entry(
    "bot-keeps-a-secret",
    (("keep", "keeps", "keeping", "hold"),
     ("secret", "secrets", "between us", "to yourself")),
    "Yes - it stays in this chat. Nothing is written down and nothing carries over, so nobody "
    "else reads it and it is gone when we finish. If it is something a person needs to act on, "
    "though, tell someone who can.",
    ask=("you", "your", "u", "can i", "could i", "will you", "would you"),
    avoid=("surprise", "surprises", "birthday", "present", "gift", "keep it from", "keeping it from")))
ENTRIES.append(
    entry("midlife-crisis",
          (("midlife crisis", "mid-life crisis", "middle age crisis", "mid life crisis",
            "midlife", "middle aged", "middle age"),
           ("what is", "whats", "what does", "mean", "am i having", "having one", "signs",
            "symptoms", "why", "when", "age", "cope", "deal with", "husband", "wife", "partner",
            "mum", "dad", "he", "she", "my", "feel")),
          ("A midlife crisis is the shake-up people often have roughly between 40 and 55, when "
           "the shape of a life stops matching the person in it and the changes come in a rush: a "
           "new car, a sudden hobby, a job left, a marriage questioned. It is not an illness and "
           "it is not inevitable - the research says most people's wellbeing rises through midlife "
           "- but the sense of time running out is real, and it is usually about mortality rather "
           "than about youth. The useful move is to name what is actually missing (freedom, "
           "friendship, a body that works, work that matters) and change that one thing rather "
           "than the whole life at once."),
          avoid=("menopause", "perimenopause", "hot flushes", "period", "hormone", "testosterone",
                 "birthday", "40th", "50th")))
