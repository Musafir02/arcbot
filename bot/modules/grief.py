import copy
import re

from ..compose import loss
from ..compose import pick as compose_pick
from ..knowledge import lookup

PRIORITY = 2100
ANSWERS = ("feelings", "grief", "loss")
ANSWERS_INSTEAD = ("feelings", "grief", "loss")

def defers_to(reply, line):
    if not (loss.a_pet_died(line) and loss.asks_about_the_remains(line)):
        return False
    return not loss.names_a_feeling(line) or loss.feeling_about_the_body(line)


DEFERS_TO = defers_to

REMEMBER = 3
SHORT = 16

POSSESSIVE = re.compile(r"\b(?:my|our|his|her|their)\s+$")
SUDDEN = re.compile(r"\b(?:sudden|suddenly|out of the blue|no warning|shock|shocked)\b")
EXPECTED = re.compile(r"\b(?:it was expected|was expected|we knew (?:it|this) was coming|"
                      r"we saw it coming|long illness|not a surprise|no surprise|"
                      r"been ill for (?:a|years|months))\b")
SLEEP = re.compile(r"\b(?:cant|can'?t|couldnt|couldn'?t|cannot|unable to|barely|hardly|not|never)"
                   r"\s+(?:sleep|sleeping|slept|stay asleep|get to sleep|get any sleep)\b|"
                   r"\b(?:havent|haven'?t|hasnt|hasn'?t|hadnt|hadn'?t|didnt|didn'?t)\s+"
                   r"(?:slept|been sleeping|had (?:any |much |much of any )?sleep)\b|"
                   r"\b(?:keep|kept|still)\s+waking\b|\bwaking (?:up )?(?:at|every|in the)\b|"
                   r"\bwoke (?:up )?at\b|\bawake (?:at|all|most of the)\b|"
                   r"\b(?:insomnia|sleepless|lying awake)\b|\b(?:3|4|5)\s?am\b")
GUILT = re.compile(r"\b(?:should have|should've|shouldnt have|blame myself|my fault|regret|"
                   r"if only|wish i (?:had|could|was there)|didn'?t visit|didn'?t go|"
                   r"guilty (?:about|that|for)|so guilty i|more time with)\b")
HARD = re.compile(r"\b(?:it|that|yesterday|today|this morning|the day|last night)\s+"
                  r"(?:was|is|has been|'s been)\s+(?:so |really |very |pretty |just )?"
                  r"(?:hard|tough|awful|horrible|brutal|rough|difficult|shit|hell|"
                  r"the worst)\b")
CRYING = re.compile(r"\b(?:cry|crying|cried|tears|sobbing)\b|\bi broke down\b")
TALK_ABOUT = re.compile(
    r"\b(?:cant|can't|couldnt|couldn't|could not|dont|don't|do not|not able to|not ready to|"
    r"struggl\w* to|hard to|too (?:hard|painful|raw|much) to)\s+(?:really\s+|even\s+|ever\s+)?"
    r"talk(?:ing)?\s+(?:about|of)\s+(?:it|him|her|them|that|this|any of it|any of that)\b")
_LIVING = "|".join(sorted(loss.PEOPLE | loss.PET_WORDS, key=len, reverse=True))
MISSING = re.compile(r"\b(?:miss (?:her|him|them)|i miss my (?:"
                     + _LIVING + r")|think about (?:her|him|them)|"
                     r"(?:the|her|his|their) birthday|anniversary|dreamt? about (?:her|him)|"
                     r"photos? of (?:her|him|them))\b")
TALK_TO_SOMEONE = re.compile(
    r"\b(?:talk|talking|speak|speaking)\s+(?:to|with)\s+(?:" + _LIVING +
    r"|my|our|the|his|her|a|an)\b"
    r"|\babout (?:it|that|this)\s+(?:with|to)\s+(?:" + _LIVING +
    r"|my|our|the|his|her|a|an)\b")
CANT_TALK = re.compile(
    r"\b(?:i|we)\s+(?:still\s+|just\s+|really\s+)?"
    r"(?:cant|can't|couldnt|couldn't|cannot|won't|wont|dont|don't|do not|wouldnt|wouldn't|am not|not)\b"
    r"[^.!?]{0,24}\b(?:talk|talking|speak|speaking|say|saying)\b"
    r"[^.!?]{0,16}\b(?:about (?:it|that|this|him|her|them)|yet|now|today)\b"
    r"|\b(?:its|it's|that's|thats)\s+(?:too\s+(?:soon|raw|early|fresh)|too hard)\b"
    r"|\bnot ready to talk\b|\bcan we not talk about\b|\blets not talk about\b")
SIGNS = re.compile(r"(?:still|keep) (?:look|looking|listen|listening|wait|waiting|expect|expecting) for "
                   r"(?:her|him|them)|(?:still|keep) (?:expect|expecting) (?:her|him|them)|(?:still|keep) (?:talk|talking|say|saying|tell|telling)\b"
                   r"[^.]{0,20}?\b(?:her|him|them)\b|think(?:ing)? i (?:see|hear) (?:her|him)|"
                   r"half expect|hear (?:her|him) voice")
AGE = re.compile(r"\b(?:he|she|it|they)\s+was\s+\d{1,2}\b(?!\s*(?:degrees|miles|kilos|kg|"
                 r"pounds|quid|minutes|hours|days|weeks|months|years|per cent|%))|"
                 r"\baged\s+\d{1,2}\b|\bin (?:her|his) (?:70s|80s|90s)\b")
AGE_NUMBER = re.compile(r"\b(?:he|she|it|they)\s+was\s+(\d{1,2})\b|\baged\s+(\d{1,2})\b|"
                        r"\bin (?:her|his) (\d)0s\b")
SHORT_LIFE = 70
ANIMAL_SPAN = {"dog": 12, "puppy": 12, "cat": 15, "kitten": 15, "rabbit": 8, "bunny": 8,
               "hamster": 2, "guinea": 6, "budgie": 8, "parrot": 40, "horse": 25, "pony": 25,
               "ferret": 8, "rat": 2, "fish": 5, "tortoise": 60, "snake": 15, "lizard": 10,
               "gerbil": 3, "chinchilla": 10, "cockatiel": 15,
               "guinea pig": 6}
BELONGINGS = re.compile(r"\b(?:her|his|their|the)\s+(?:things|stuff|clothes|belongings|flat|"
                        r"house|room|wardrobe|shed)\b|\bpack(?:ing)? (?:it|them|her|his) up\b|"
                        r"\bclear(?:ing)? (?:out|it|them)\b|\bempty(?:ing)? (?:it|them|the)\b")
EULOGY_WRITE = re.compile(r"\b(?:write|writing|wrote|draft|drafting|help|how|start|starting|"
                          r"opening|open|begin|length|long|words|minutes|structure|template|"
                          r"examples?|what do i say|say)\b")
EULOGY = re.compile(r"\b(?:eulogy|eulogies)\b")
ARRANGEMENTS = re.compile(r"\b(?:funeral|burial|cremation|eulogy|coffin|undertaker|"
                          r"funeral director|headstone|graveside|cemetery|order of service)\b")
REGISTER = re.compile(r"\b(?:register (?:the|her|his) death|registration|register office|"
                      r"registrar|death certificate|medical certificate)\b")
COST = re.compile(r"\b(?:cost|costs|price|prices|priced|how much (?:does|is|will|do|are)|"
                  r"expensive|afford|cheap\w*|quote|pay for)\b")
WORK_PRESSURE_REPLIES = (
    "You don't owe anyone the details. \"{Who} died on Tuesday, I won't be in this week\" is "
    "enough for the first message, and a work friend can pass it round so you are not saying it "
    "again and again.",
    "Going back is often harder than the days before it. Ask for a phased return, a shorter week "
    "to start with, and one person to go to when it gets too much: most managers would rather you "
    "asked than quietly struggled.",
    "It is fine to say \"I'd rather not talk about it, but thank you\" and leave it there. People "
    "ask because they care and then run out of words, so give them the line and they will use it.",
)
WORK_REPLIES = (
    "Ask your manager in writing and keep it plain: what has happened, and how many days you "
    "need. Most employers have a bereavement leave policy, and HR has to give you it in a "
    "sentence if you ask.",
    "You don't owe anyone the details. \"{Who} died on Tuesday, I won't be in this week\" is "
    "enough for the first message, and a work friend can send it if a phone call is too much.",
    "Work can wait a week. Say what you can cover before you go and who is picking it up, then "
    "let the rest go - people cover for each other, and this is what that is for.",
)
PROBATE = re.compile(r"\b(?:probate|grant of probate|letters of administration)\b")
PROBATE_REPLIES = (
    "Probate is the court's permission to deal with the estate: you apply to HMCTS with the "
    "will and the death certificate. A straightforward application is usually decided within a "
    "few weeks, and a solicitor takes it on when the estate is large or the family expect a "
    "disagreement.",
    "How long probate takes depends on the estate. One bank and a house is often a few months "
    "from applying to the grant; shares, a business or a dispute take longer. Ask the solicitor "
    "for the likely date in writing at the first meeting, so you have something to plan around.",
    "Not everything needs probate. Joint accounts and anything held in trust usually pass "
    "without it, and banks often release small balances on the certificate alone. The rule of "
    "thumb is a house, or more than one bank, or a will that is not clear - then apply.",
)
PAPERWORK = re.compile(r"\b(?:solicitor|paperwork|(?:the|her|his|their) will|"
                       r"(?:her|his|their) (?:bank|pension|insurance|accounts)|"
                       r"bereavement|the estate)\b")
ARRANGEMENTS_ELSE = re.compile(r"\b(?:wear|wearing|outfit|clothes|suit|dress|shoes|tie|"
                               r"music|songs?|hymns?|flowers?|wreath|bouquet|buffet|"
                               r"sandwiches|catering|reception|wake|drink)\b")
FAMILY = re.compile(r"\b(?:brother|sister|dad|mum|stepdad|stepmum|uncle|aunt|nan|grandad|"
                    r"family|relatives|in-laws|siblings)\b[^.]{0,40}?\b(?:argue|arguing|"
                    r"argument|row|rows|rowing|fight|fighting|falling out|fell out|"
                    r"not talking|won'?t talk)\b")
TELL = re.compile(r"\b(?:who (?:do|should|must|would) (?:i|we) (?:have to |need to |ought to )?"
                  r"(?:tell|notify|inform|ring|contact)"
                  r"|who (?:needs? to know|needs? to be told|has to know|should (?:know|be told))"
                  r"|who to (?:tell|notify|inform)"
                  r"|(?:do|should) (?:i|we) (?:have to |need to )?(?:tell|notify|inform|ring) "
                  r"(?:everyone|everybody|anyone|people|the (?:council|bank|pension|tax office|"
                  r"dwp|hmrc|authorities|employer))"
                  r"|tell us once|who do i inform)\b")
TELLING = re.compile(r"\bhow do i (?:tell|say|break)\b|\bhow to tell\b|\b(?:do|should) i tell\b|"
                     r"\bwhat (?:do|should|can) i tell\b|\bhow do i let .{0,20} know\b")
SAY_TO = re.compile(r"\bwhat (?:do|should|can) i say\b|\bwhat to say\b")
WORK = re.compile(r"\b(?:bereavement leave|compassionate leave|leave from work|"
                  r"(?:ask|tell|ring|call|email) (?:my|the) (?:boss|manager|work|employer|hr)\b|"
                  r"\btell work\b|\bwhat do i tell work\b)")
WORK_WORD = r"\b(?:work|job|boss|manager|office|shift|shifts|colleagues?|team|employer|hr)\b"
WORK_PRESSURE = re.compile(r"(?:(?=.*" + WORK_WORD + r").*?\b(?:back to work|off work|cant face|"
                           r"can't face|cant go back|can't go back|dread|too much|"
                           r"(?:keep|keeps|are) asking|everyone (?:keeps )?asking)\b"
                           r"|\b(?:people|everyone|folks|the team) at work\b)")
ADMIN = re.compile(
    r"\b(?:paperwork|the papers|(?:a|any|one|the|that) forms?|filling in|fill in|"
    r"(?:his|her|their|the) (?:bank|banks|accounts?|pension|pensions|insurance|policies|policy|"
    r"passport|driving licence|licence|mobile|phone contract|utilities|bills?|mortgage|"
    r"tenancy|landlord|affairs)|council tax|(?:his|her|their) (?:benefits?|tax credits)|"
    r"universal credit|hmrc|the dwp|the tax office|dvla|the council|"
    r"(?:cancel|close|stop|sort out|sorted out|sorted|deal with|notify|inform|tell)\b"
    r"[^.]{0,36}?\b(?:subscription\w*|direct debits?|accounts?|pension|insurance|policy|"
    r"doctor'?s (?:surgery|practice)|dentist|the vet|employer|the council|the bank|"
    r"the tax office|his phone|her phone|the phone|the house|the mortgage|the tenancy)\b)\b")
ADMIN_REPLIES = (
    "None of it has to be done this week, and it goes faster by phone than by letter. The bank, "
    "the pension and the council each have a bereavement team: ring one a day, ask them to stop "
    "the letters, and write the reference number down on a single sheet as you go.",
    "One call does most of it: Tell Us Once tells the tax office, the council, the passport "
    "office and the DVLA in one go, and the register office sets it up when the death is "
    "registered. The bank and any pension are their own two calls.",
    "Do it in the order it hurts least: the bank first, because the account keeps running, then "
    "the pension, then the bills. As next of kin you can do all of it on their behalf, and you "
    "don't need probate to tell anybody anything.",
)

PRACTICAL = (TELL, TELLING, SAY_TO, WORK_PRESSURE, WORK, REGISTER, COST, PROBATE, ADMIN,
             PAPERWORK, ARRANGEMENTS, BELONGINGS)

OTHER_PERSON = re.compile(r"\bmy (?:baby|boy|girl|son|daughter|kid|child|toddler|teenager|"
                          r"husband|wife)\b|\b\d{1,2} year old\b")
EMERGENCY = re.compile(r"\b(?:wont wake|cant wake|can'?t wake|unresponsive|not breathing|"
                       r"ambulance|999|911|chest pain|a and e|a&e|temperature|floppy|seizure|"
                       r"overdose|suicidal|bleeding|collapsed)\b")

SUDDEN_REPLIES = (
    "Sudden is the hardest kind — nothing gets you ready for it. It comes in waves for weeks, "
    "so don't be surprised when a good hour turns into a bad one.",
    "That kind of shock takes ages to settle, and there's no doing it faster. Go as slowly as "
    "you can, and let people do the small things for you.",
)
EXPECTED_REPLIES = (
    "Even when you know it's coming, it still lands hard — knowing and being ready are two "
    "different things. There's nothing wrong with being knocked sideways by it.",
    "Expected doesn't make it easier, it just means you spent a long time watching it happen. "
    "That takes it out of you too, so rest when you can.",
)
SLEEP_REPLIES = (
    "Sleep is the first thing to go with this. Don't lie there fighting it: get up, warm drink, "
    "something dull, and go back when you're sleepy.",
    "Hardly sleeping is the usual pattern after a loss, and it does ease. Keep the room cool "
    "and dark, get up rather than lie there, and catch up in the day if you can.",
)
GUILT_REPLIES = (
    "That guilt is a very common part of this, and it is almost never deserved. If it helps, "
    "say out loud what you'd want {who} to say to you now.",
    "Everyone finds something to blame themselves for afterwards. {Who} would not want you "
    "carrying that.",
)
HARD_REPLIES = (
    "It is, and there's no getting round how hard it is. Do less today than you think you "
    "should, and let people bring you things.",
    "It's allowed to be that hard. Nothing about the first days is normal, so don't measure "
    "yourself against anyone else getting through it.",
)
TALK_ABOUT_REPLIES = (
    "You don't have to. Say as much or as little as you want, and I'm here for the parts that "
    "aren't words.",
    "That's alright. Nothing has to be said here - tell me when you want to, and not before.",
)
CRYING_REPLIES = (
    "Crying is the pressure valve, not a setback. Let it come, then get outside for ten minutes "
    "if you can.",
    "That's normal, and better out than held in. It gets further apart, not gone.",
)
MISSING_REPLIES = (
    "That's a big miss, and it doesn't fade quickly. The stories keep {who} close, so go on "
    "telling them.",
    "The dates are the hard ones — the birthday, Christmas, the day itself. Doing one small "
    "thing for {who}, a photo out or a meal they liked, can take the edge off.",
)
CANT_TALK_REPLIES = (
    "That's alright, you don't have to — not now, not with me. I'm here whenever it helps, "
    "and we can talk about anything else in the meantime.",
    "Then we won't. Say as much or as little as you want, and we can leave {who} out of it "
    "for now.",
    "Fair enough. Nothing to explain, and no rush: tell me about something ordinary instead "
    "if that's easier today.",
)
SIGNS_REPLIES = (
    "That's one of the strangest parts — the house keeps the shape of {who}. It eases on its "
    "own, slowly, so don't talk yourself out of it.",
    "Keep going if it helps. Saying goodnight, or talking out loud, is how a lot of people get "
    "through the first year, and it isn't daft.",
)
AGE_REPLIES = (
    "That's a long time together. It's the routines that catch you out more than the big days: "
    "the same chair at the same time, nobody in it.",
    "A good long life still leaves a big hole. Be as sad as you need to be about it.",
)
PET_OLD_REPLIES = (
    "{Age} is a good age for a {animal}, and it still isn't enough. Be as sad as you need to be "
    "about {who}.",
    "That's a long life for a {animal}. It doesn't make the house any quieter, and it isn't "
    "meant to.",
)
PET_YOUNG_REPLIES = (
    "{Age} is no age for a {animal}. Nothing about it is fair, and it's alright to say so out "
    "loud.",
    "{Who} should have had years more than that. It was far too soon, and there is no sense to "
    "be made of it.",
)
YOUNG_AGE_REPLIES = (
    "That's far too young, and there is no sense to be made of it. You don't have to try tonight.",
    "{Who} should have had years more than that. Nothing about it is fair, and it's alright to "
    "say so out loud.",
)
BELONGINGS_REPLIES = (
    "Do a little at a time, and don't do it alone: one drawer with someone there, then stop. "
    "Nothing has to go this week.",
    "You don't have to sort {who}'s things to be doing it right. Pick one small thing, give "
    "the rest a few months, and keep anything you're not sure about.",
)
REGISTER_REPLIES = (
    "The death is registered at the local register office, usually within five days. The "
    "hospital or the funeral director tells you which one; take the medical certificate, and "
    "get several copies of the death certificate while you're there.",
    "You do that at the register office for the area where it happened. Book first, take the "
    "medical certificate, and buy a few extra certificates — every bank and pension will want "
    "one.",
)
COST_REPLIES = (
    "Ask two funeral directors for a written, itemised quote — the coffin and the cars are "
    "where it adds up, and a cremation with no service costs a fraction of a full funeral. "
    "Nothing has to be decided on the first call.",
    "Say what you actually want before they price it: a simple coffin, no cars, family carrying "
    "it. If money is tight there's a funeral expenses payment from the DWP, and the council will "
    "help as a last resort.",
)
ARRANGEMENTS_REPLIES = (
    "Ring the funeral director first — they do the rest of it. Take someone with you to the "
    "meeting, and ask about costs up front.",
    "For the day itself: be early, sit near the back if you might need air, and don't feel you "
    "have to talk to everyone.",
)
PAPERWORK_REPLIES = (
    "The bank and the council want the death certificate, and most places have a bereavement "
    "line that does the telling once. Ask them to do that rather than ringing round yourself.",
    "Probate is only needed if there's a house, savings over the limit or shares. A solicitor "
    "will do a free first call, and it can wait a few weeks.",
)
FAMILY_REPLIES = (
    "That happens in nearly every family, and it's the grief talking as much as anything — "
    "everyone is at a different speed. Split the jobs so you're not doing the same one: you "
    "take the house, they take the paperwork.",
    "It's worth naming it out loud, once, when nobody's tired: \"we're going to snap at each "
    "other and that's fine, but let's not do it over the house\". Then give each other room.",
)
TELLING_REPLIES = (
    "Keep it plain, and say the name: \"{who} died on Tuesday\" is kinder than a soft way round "
    "it. Then let them talk, and don't be afraid to say you don't know what to say either.",
    "Say it once, plainly, and then be quiet with them for a bit. People remember being told "
    "kindly far longer than the exact words.",
)
SAY_TO_REPLIES = (
    "You don't need the right words. Ask about {who}, and let them talk as long as they want; "
    "that does more than anything you could say.",
    "Say the true things: that you're sorry, that you miss {who} too, and that you're around. "
    "Then follow their lead - if they want to laugh about something, laugh.",
    "Ask what the day has been like, and take the answer however it comes. Not filling the "
    "silence is a kindness in itself.",
)
TELL_REPLIES = (
    "Tell Us Once does most of it in one go — the passport, driving licence, HMRC and the "
    "council. The bank and any pension want their own call, and their bereavement line is the "
    "quickest way in.",
    "Start with the people who need to act this week: the employer, the bank, the landlord if "
    "there is one. Everything else can wait until you've had a few days.",
)
COMPANY_REPLIES = (
    "I'm here. Say as much or as little as you like about {who}.",
    "No need to be all right about it with me. If you'd rather talk about something else for a "
    "while, that's fine too.",
)

DOUBT_IT = re.compile(
    r"^(?:and |so |ok(?:ay)?,? )?"
    r"(?:is (?:that|this|it) (?:bad|ok(?:ay)?|all right|alright|wrong|weird|odd|a bad sign)"
    r"|is that how it (?:goes and works|goes|works))"
    r"(?: then)?[\s?.!]*$")
DOUBT_ME = re.compile(
    r"^(?:and |so |ok(?:ay)?,? )?"
    r"(?:am i (?:ok(?:ay)?|all right|alright|normal|going mad|going crazy|losing it|losing my mind)"
    r"|does that make me (?:weird|mad|crazy))"
    r"(?: then)?[\s?.!]*$")
DOUBT_IT_REPLIES = (
    "It is not a bad sign, and there is nothing here you have to fix today. The part worth "
    "keeping an eye on is eating and sleeping.",
    "Not that, no. Grief is not an illness and it does not run to a timetable - the waves get "
    "further apart, they do not stop.",
    "That is grief doing its work, not a weakness. It comes in waves, and the waves get further "
    "apart as time goes on - they do not stop.",
    "It eases slowly, and it does not go in a straight line - a better day is not a setback.",
)
DOUBT_ME_REPLIES = (
    "Nothing about that is wrong with you. Grief is not an illness and it does not run to a "
    "timetable - the waves get further apart, they do not stop.",
    "No, you are not losing it. This is what a death does to a person, and it comes in waves "
    "rather than a straight line down.",
    "You are allowed to be like this. If you are not sleeping or eating at all after a couple of "
    "weeks, that is the point to say it to your GP.",
    "It is not something to be good at. If it helps, the thing to hold on to is that a bad hour "
    "does not undo a good one.",
)


OPEN_ASK = re.compile(r"^(?:so |and |ok(?:ay)?,? )?(?:"
                      r"(?:what|where) (?:do|should|can|could|shall) (?:i|we) "
                      r"(?:do|start|begin|go from here|take on)(?: now| next| first| today)?"
                      r"|what now|now what|what happens now|what next"
                      r"|where do i (?:start|begin)(?: from here)?"
                      r"|how do i (?:get through|deal with|cope with) (?:this|today|it|the day)"
                      r"|(?:i |we )?(?:don'?t|dont|do not) know what to (?:do|say)"
                      r"(?: now| next| first| today)?"
                      r"|(?:i |we )?(?:don'?t|dont|do not) know where to (?:start|begin)"
                      r")(?:\s+then)?\s*[.?!]*$")
OPEN_ASK_REPLIES = (
    "Nothing big, today. Eat something, drink some water, and let one person who knows be with "
    "you. The rest can wait until tomorrow.",
    "Keep it small. One phone call, one meal, and say yes to anybody who offers to help - nobody "
    "expects you to hold it all at once.",
    "You do not have to work anything out today. Take the offers that come, and leave the "
    "decisions until you have slept.",
    "When you have a quiet hour, write down the things only you know about {who}. The admin can "
    "wait a week; the small details are the ones that go.",
    "Pick the one thing that would make tomorrow easier, do that, and let the rest be someone "
    "else's job for now.",
    "Slow is fine. Do the next necessary thing, and if there is someone who can sit with you, "
    "ask them to.",
)


def _words(text):
    text = str(text or "").lower().replace("\u2019", "'")
    return [word.strip(".,!?;:\"'()") for word in text.split() if word.strip(".,!?;:\"'()")]


def _who(words):
    animal = loss.the_animal(" ".join(words))
    if animal:
        return "your " + animal, True
    for word in words:
        singular = word[:-1] if word.endswith("s") and word[:-1] in loss.PET_WORDS else word
        if singular in loss.PEOPLE or singular in loss.PET_WORDS:
            return "your " + singular, singular in loss.PET_WORDS
    return None, False


def _record(text, memory):
    if not isinstance(text, str) or not text.strip():
        return
    clean = " ".join(_words(text))
    if not clean or not loss.reads_as_loss(clean):
        return
    if loss.whose(clean) != "own":
        return
    who, pet = _who(_words(text))
    if not who:
        return
    memory["loss"] = {"who": who, "pet": pet, "turn": len(memory.get("turns") or []),
                       "ahead": loss.is_dying_now(clean)}


THANKS_LINE = re.compile(
    r"^(?:ok(?:ay)?[,.!]?\s*)?(?:(?:thanks|thank you|thankyou|ta)(?:\s+(?:for|so much|very much)"
    r"\s*(?:listening|talking|that|the chat|your help)?)?|(?:im|i'm|i am)\s+(?:ok|okay|fine|"
    r"alright)(?:\s+now)?|ok(?:ay)?)[.!, ]*$")
LOSS_SPEAKERS = ("loss", "grief")


def _still_here(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return False
    return str(turns[-1].get("module") or "") in LOSS_SPEAKERS


def _next_to_the_loss(record, memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return False
    if isinstance(record, dict) and record.get("replied") == len(turns) - 1:
        return True
    if str(turns[-1].get("module") or "") in LOSS_SPEAKERS:
        return True
    previous = " ".join(str(turns[-1].get("user") or "").split())
    if not previous:
        return False
    return bool(loss.reads_as_loss(previous) or FAMILY.search(previous) or GUILT.search(previous)
                or CRYING.search(previous) or SLEEP.search(previous) or HARD.search(previous))


def _remembered(memory):
    record = memory.get("loss")
    if not isinstance(record, dict) or not record.get("who"):
        return None
    if record.get("turn", 0) < len(memory.get("turns") or []) - REMEMBER:
        return None
    return record


def _age(clean):
    match = AGE_NUMBER.search(clean)
    if not match:
        return None
    return int(match.group(1) or match.group(2) or (match.group(3) + "0"))


def _animal(who):
    for word in sorted(ANIMAL_SPAN, key=len, reverse=True):
        if re.search(r"\b" + word + r"\b", who or "", re.I):
            return word
    return None


def _any_animal(who):
    animal = _animal(who)
    if animal:
        return animal
    return "pet" if re.search(r"\b(?:your )?pets?\b", who or "", re.I) else None


def _young(clean, who=""):
    number = _age(clean)
    if number is None:
        return False
    animal = _animal(who)
    if animal:
        return number < ANIMAL_SPAN[animal] * 0.8
    return number < SHORT_LIFE


def _age_pool(clean, who):
    number = _age(clean)
    animal = _animal(who)
    pool = YOUNG_AGE_REPLIES if _young(clean, who) else AGE_REPLIES
    if animal:
        pool = PET_YOUNG_REPLIES if _young(clean, who) else PET_OLD_REPLIES
    filled = []
    for reply in pool:
        reply = reply.replace("{who}", who).replace("{Who}", who[:1].upper() + who[1:])
        reply = reply.replace("{animal}", animal or "").replace("{Age}", _word(number))
        filled.append(reply)
    return filled


def _word(number):
    words = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven",
             8: "Eight", 9: "Nine", 10: "Ten", 11: "Eleven", 12: "Twelve", 13: "Thirteen",
             14: "Fourteen", 15: "Fifteen", 16: "Sixteen", 17: "Seventeen", 18: "Eighteen",
             19: "Nineteen", 20: "Twenty"}
    if number is None:
        return "That"
    return words.get(number, str(number))


def _fill(pool, who):
    return [reply.replace("{who}", who).replace("{Who}", who[:1].upper() + who[1:])
            for reply in pool]


PERSON_ONLY = (REGISTER, COST, PROBATE, PAPERWORK, ARRANGEMENTS, TELL, ADMIN)

ANIMAL_PAPERWORK_REPLIES = (
    "None of that applies to {who}: nothing gets registered and there is no estate to deal "
    "with. Ring the vet who saw them - they arrange the cremation or the burial, and they will "
    "tell you what it costs.",
    "A pet leaves no estate and no paperwork. The vet is the one who arranges the cremation or "
    "the burial, and they will give you the options and the price in one call.",
    "There is nothing official to do for {who}. Tell the vet you would like them to arrange it, "
    "and ask about the ashes and the cost while you are on the phone.",
)


def respond(text, memory):
    words = _words(text)
    if not words or len(words) > SHORT:
        return None
    clean = " ".join(words)
    if OTHER_PERSON.search(clean) or EMERGENCY.search(clean):
        return None
    if lookup.a_colour_is_worn(memory.get("understood") or {}):
        return None
    if loss.FUNERAL.search(clean) and loss.a_part_of_the_day_asked(clean):
        return None
    record = _remembered(memory)
    if not record:
        return None
    if loss.dying_in_the_chat(memory) and (loss.SAY_GOODBYE.search(clean)
                                          or TELLING.search(clean) or SAY_TO.search(clean)):
        return None
    pool = None if SLEEP.search(clean) else _composer_pool(text, memory)
    if pool is not None:
        practical = (_asks(clean) or ADMIN.search(clean)) and any(
            p.search(clean) for p in PRACTICAL)
        if not (practical and (pool is loss.LOSS_REPLIES or WORK.search(clean)
                               or WORK_PRESSURE.search(clean) or TELLING.search(clean)
                               or TELL.search(clean) or ADMIN.search(clean))):
            return None
    if loss.reads_as_loss(clean) and not any(p.search(clean) for p in PRACTICAL):
        return None
    who = record["who"]
    if CANT_TALK.search(clean) and not TALK_TO_SOMEONE.search(clean):
        record["replied"] = len(memory.get("turns") or [])
        return _pick(_fill(CANT_TALK_REPLIES, who), memory, clean)
    if OPEN_ASK.match(clean) and not any(p.search(clean) for p in PRACTICAL) \
            and not _answered_by_the_knowledge_base(text, memory):
        record["replied"] = len(memory.get("turns") or [])
        return _pick(_fill(OPEN_ASK_REPLIES, who), memory, clean)
    next_to_the_loss = _next_to_the_loss(record, memory)
    if next_to_the_loss:
        for doubt, pool in ((DOUBT_IT, DOUBT_IT_REPLIES), (DOUBT_ME, DOUBT_ME_REPLIES)):
            if doubt.match(clean):
                record["replied"] = len(memory.get("turns") or [])
                return _pick(pool, memory, clean)
    for pattern, pool in ((FAMILY, FAMILY_REPLIES), (WORK_PRESSURE, WORK_PRESSURE_REPLIES),
                          (WORK, WORK_REPLIES), (TELL, TELL_REPLIES),
                          (TELLING, TELLING_REPLIES), (SAY_TO, SAY_TO_REPLIES),
                          (REGISTER, REGISTER_REPLIES), (COST, COST_REPLIES),
                          (PROBATE, PROBATE_REPLIES), (PAPERWORK, PAPERWORK_REPLIES),
                          (ADMIN, ADMIN_REPLIES),
                          (ARRANGEMENTS, ARRANGEMENTS_REPLIES),
                          (BELONGINGS, BELONGINGS_REPLIES), (EXPECTED, EXPECTED_REPLIES),
                          (SUDDEN, SUDDEN_REPLIES),
                          (SLEEP, SLEEP_REPLIES), (HARD, HARD_REPLIES),
                          (TALK_ABOUT, TALK_ABOUT_REPLIES), (GUILT, GUILT_REPLIES),
                          (CRYING, CRYING_REPLIES), (AGE, None),
                          (SIGNS, SIGNS_REPLIES), (MISSING, MISSING_REPLIES)):
        if pattern in PERSON_ONLY and _any_animal(who):
            if _the_answer_says_the_animal(text, memory, _any_animal(who)):
                continue
            if pattern.search(clean):
                record["replied"] = len(memory.get("turns") or [])
                return _pick(_fill(ANIMAL_PAPERWORK_REPLIES, who), memory)
        if pattern is ARRANGEMENTS and (ARRANGEMENTS_ELSE.search(clean)
                                        or loss.a_part_of_the_day_asked(clean)):
            continue
        if (pattern is ARRANGEMENTS and EULOGY.search(clean)
                and EULOGY_WRITE.search(clean)):
            continue
        if pattern.search(clean):
            record["replied"] = len(memory.get("turns") or [])
            if pool is None:
                pool = _age_pool(clean, who)
            return _pick(_fill(pool, who), memory)
    if THANKS_LINE.match(clean) and _still_here(memory):
        record["replied"] = len(memory.get("turns") or [])
        return _pick(_fill(COMPANY_REPLIES, who), memory)
    return None


ASK_OPENERS = frozenset(("how", "what", "who", "when", "where", "which", "should", "can",
                         "do", "does", "is", "are", "could", "would", "any", "am"))


def _asks(clean):
    return "?" in clean or (clean.split() or [""])[0] in ASK_OPENERS


def _composer_pool(text, memory):
    try:
        return loss.reply_for(text, memory)
    except Exception:
        return None


def observe(text, memory):
    _record(text, memory)


def _the_answer_says_the_animal(text, memory, animal):
    try:
        from . import answers
        topic = memory.get("topic")
        topic = topic.get("text", "") if isinstance(topic, dict) else ""
        asked = (topic + " " + text).strip() if topic else text
        got = answers.respond(asked, copy.deepcopy(memory))
    except Exception:
        return False
    if isinstance(got, dict):
        got = got.get("reply") or ""
    low = str(got or "").lower()
    if not (("vet" in low) or (bool(animal) and animal in low)):
        return False
    return bool(PET_LOSS.search(low))


PET_LOSS = re.compile(
    r"\b(?:die[ds]?|dying|death|dead|passed away|put (?:down|to sleep)|euthan\w*|cremat\w*|"
    r"ashes|urn|casket|coffin|burial|bur(?:y|ied|ies)|body|remains|paw print|lock of fur|"
    r"last (?:visit|day)|goodbye)\b")


def _answered_by_the_knowledge_base(text, memory):
    try:
        from . import answers
        topic = memory.get("topic")
        topic = topic.get("text", "") if isinstance(topic, dict) else ""
        asked = (topic + " " + text).strip() if topic else text
        return bool(answers.respond(asked, copy.deepcopy(memory)))
    except Exception:
        return False


def _pick(options, memory, seed_text=""):
    try:
        return compose_pick(list(options), memory, seed_text)
    except Exception:
        return options[0]
