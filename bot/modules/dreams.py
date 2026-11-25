import re

from ..memory import dream as _dream

PRIORITY = 3000

SOMEONE_DIED = re.compile(
    r"\b(?:died|dying|dead|death|passed (?:away|on)|killed|funeral|buried|gone|"
    r"run over|put (?:him|her|it|them) (?:down|to sleep)|euthanis\w*|euthaniz\w*)\b")
A_FIRE = re.compile(
    r"\b(?:fire|burning|burnt|burned|flames|smoke|flood|flooded|collapsed|crashing down)\b")
A_BREAK_IN = re.compile(r"\b(?:robbed|robbery|burglar|burglars|burgled|intruder|break(?:ing)? in|"
                        r"broke in|broken into|house was broken)\b")
CHASED_OR_FALLING = re.compile(
    r"\b(?:drown\w*|falling|fell|chased|chasing|running away|trapped|stuck|suffocat\w*|"
    r"strangled|being held|can(?:no|')?t move|paralys\w*|crash\w*|accident|"
    r"hit by a (?:car|bus|truck|train)|run over)\b")
ILL_IN_THE_DREAM = re.compile(
    r"\b(?:cancer|tumou?r|stroke|heart attack|dementia|alzheimers|aids|hiv|"
    r"diagnos\w*|ill|dying of|got (?:sick|ill)|terminal)\b")
A_GOOD_ONE = re.compile(
    r"\b(?:fly|flies|flying|flew|float\w*|won|lotto|lottery|holiday|beach|love\w*|kiss\w*|"
    r"my (?:nan|gran|grandma|grandad|mum|dad|dog|cat) (?:was|gave|said|came)|"
    r"laughing|happy|best day|pregnant)\b")
DIED_MYSELF = re.compile(
    r"\bi\s+(?:was\s+)?(?:died|dead|dying|killed|drowned|buried|hanging|hung|"
    r"overdos\w*|killed myself|hurt myself|took my own life)\b|\bmy own (?:death|funeral)\b"
    r"|\b(?:suicide|overdose)\b")
ATTACKED = re.compile(
    r"\b(?:attacking|attacked|attacks me|hurting me|hurt me|beating me|beat me|"
    r"strangling me|stabbed|stabbing|shot|shooting|raped|raping|grabbed me|"
    r"somebody in (?:my|the) (?:house|room)|someone in (?:my|the) (?:house|room)|"
    r"broke into|breaking in|burglar|intruder|following me|chasing me)\b")
TEETH = re.compile(r"\b(?:teeth|tooth|molar|gums)\b")
AN_EX = re.compile(r"\b(?:ex|ex-boyfriend|ex-girlfriend|ex-husband|ex-wife|my ex)\b")
A_BABY = re.compile(r"\b(?:baby|babies|newborn|toddler|pregnant|infant)\b")
PEOPLE_HURT = re.compile(
    r"\b(?:my (?:son|daughter|boy|girl|child|kid|children|mum|mom|mother|dad|father|"
    r"partner|husband|wife|brother|sister|nan|gran|grandma|grandad|friend|niece|nephew)\b)")

DEATH_LINES = (
    "Dreaming that someone died is one of the commonest dreams there is, and it is not a sign "
    "about them: it usually turns up when they have been on your mind, or when something between "
    "you is shifting. They are alive and ordinary this morning, and that is the part to trust.",
    "That dream is not an omen, it is your head working on the person: most people who dream of a "
    "death say the person had been on their mind, or that something with them was changing. "
    "Nothing in the dream is a warning about them.",
)
BREAK_IN_LINES = (
    "A house broken into in a dream is the worry about being safe at home, not a warning that "
    "somebody is coming: it turns up in weeks when the flat, the money or the door has been on "
    "your mind. Check the lock in daylight and leave it there.",
    "Dreaming about a break-in is what the head does with feeling got at, and it is one of the "
    "commonest dreams there is. Nothing in it is going to happen - the door is the same door you "
    "locked last night.",
    "That dream is about safety rather than about burglars: the nights after a scare often bring "
    "it. What usually helps is the dull, practical thing - a light on a timer, a bolt on the door "
    "- rather than going over the dream again.",
)
FIRE_LINES = (
    "A fire in a dream usually reads as worry about the place rather than anything about fire - a "
    "bill, a repair, something you cannot quite keep an eye on. It tends to fade on its own; if "
    "the same one keeps coming back, write it down in the morning.",
    "Dreaming the house is on fire is a stress dream, and the thing behind it is usually a "
    "practical worry rather than any danger - money, a job, a repair waiting on somebody. "
    "Nothing about the house needs doing because of it.",
)
CHASE_LINES = (
    "Being chased, drowning or falling is the standard stress dream, and it usually follows a "
    "stretch where something is out of your hands. A cooler room, less alcohol and half an hour "
    "off the screen before bed take most of the edge off it.",
    "That is the shape a busy week takes in sleep - out of control, no footing, running late. "
    "The dream follows the week rather than the other way round, so it eases when the week does.",
)
TEETH_LINES = (
    "Dreaming your teeth fall out is one of the most reported dreams there is, and it is not "
    "about your teeth: it tends to go with a spell of worry about how you come across, or a "
    "change you cannot control. It stops when that does.",
    "That dream is about being seen, not about your teeth - it is one of the commonest there is "
    "and it clusters in the weeks when somebody is judging you or a change is coming. No dentist "
    "needed.",
)
EX_LINES = (
    "Dreaming about an ex does not mean you want them back: your head digs up whatever is left "
    "unfinished, and it often surfaces when something in your current life is unsettled. It says "
    "more about this week than about them.",
    "An ex in a dream is usually unfinished business rather than a wish - the brain reaches for "
    "an old face when something now feels unresolved. Nothing to act on.",
)
BABY_LINES = (
    "A dream about the baby being hurt is horrible to wake from and very common on broken sleep, "
    "and nothing in it is a warning. The waking every couple of hours is what makes those dreams "
    "so vivid and so hard to shake.",
    "That one comes with the tiredness rather than with any danger: fragmented nights make "
    "frightening dreams much more likely. It gets better as the nights get longer.",
)
GOOD_LINES = (
    "Nothing in a dream is a warning, and that one is the good kind: flying and the people you "
    "love turn up in sleep when things are going alright. Enjoy it and let it go.",
    "That is the sort the brain keeps - flying, a win, somebody you love turning up - and it "
    "usually follows a stretch that felt light. Nothing to do with it but have it.",
)
OWN_DEATH_LINES = (
    "Dying, or being hurt, in a dream is frightening and very common, and it is not a sign about "
    "your health: it tends to come when something in life is ending - a job, a habit, a way of "
    "doing things - rather than anything about the body.",
    "Dreaming your own death reads as a change rather than a warning, and it clusters when "
    "something in the day to day is finishing. Anything about the body belongs to a doctor, not "
    "to a dream.",
)
ATTACK_LINES = (
    "Being attacked in a dream is not a sign of anything coming: it is what a day that felt unsafe "
    "or watched turns into at night. Uneasy sleep makes it more likely, so a door checked and a "
    "proper wind-down before bed does more for it than reading anything into it.",
    "A dream like that follows a stretch of feeling got at rather than any real threat - a "
    "difficult person, a job, a row left hanging. Nothing about it is a warning, and it eases when "
    "the day does.",
)
A_VISIT = re.compile(
    r"\b(?:was|were|is|are)\s+(?:in\s+(?:my|the)\s+room|here|with\s+me|still\s+alive|"
    r"standing\s+(?:there|in))|came\s+to\s+see\s+me|visited\s+me|sat\s+with\s+me|"
    r"spoke\s+to\s+me|said\s+hello|hugged\s+me|holding\s+my\s+hand\b")
VISIT_LINES = (
    "Dreaming that somebody you love is with you is one of the kinder ones, and it usually comes "
    "when they have been on your mind. There is nothing to read into it, and nothing wrong with "
    "enjoying it.",
    "That sort of dream is the good kind: somebody you love, there and ordinary, while you sleep. "
    "It turns up when they are on your mind, and it means nothing more than that.",
)
PEOPLE_HURT_LINES = (
    "Dreaming that somebody you love is hurt is the worry dream almost everybody has, and it is "
    "not a premonition: it turns up in the weeks when you are carrying them in your head. They are "
    "where they were when you went to bed.",
    "That dream is the shape worry takes at night rather than anything coming to them. It is worth "
    "noting what was on your mind about them that day, because that is what the dream was made of.",
)
ILL_LINES = (
    "A dream about being ill frightens people because it names a disease, and it is not a sign "
    "about your body: dreams like that follow a scare, a wait for results, or somebody close being "
    "unwell. Anything you have actually noticed in the day to day is a doctor's question, not a "
    "dream's.",
    "Nothing in a dream diagnoses anything. That one usually comes after a health scare in the "
    "family or a wait for a test, and it fades once the worry does.",
)
PLAIN_LINES = (
    "Dreams like that are usually the brain sorting the day out, and they come on strongest in a "
    "week with something on your mind. Writing it down in the morning is the usual trick for one "
    "that keeps coming back.",
    "Nothing in a dream is a warning - it is the day being filed, and a vivid one usually means a "
    "lot was going on. A pen by the bed and a few lines in the morning take the sting out of the "
    "ones that keep coming back.",
)


SETTLED_LINES = (
    "Then nobody in it is any different for it - a dream is the head clearing, not a message "
    "about them. If the same one keeps coming back, that is worth saying to a GP, because broken "
    "sleep is usually the whole of it.",
    "Good. Dreams like that are the worry being worked through at night, and they ease off when "
    "the worry does. Sleeping badly makes them louder, so a steadier night is the thing that "
    "quiets them.",
    "That is the whole of it, then: a dream, and everyone in it where they were. Worth writing "
    "down if it comes back - the mornings after are what show whether it is a worry to see "
    "someone about or just a run of bad nights.",
)


def _settled(line, choices):
    return choices[sum(ord(c) for c in line) % len(choices)]


def respond(text, memory):
    line = " ".join(str(text or "").lower().split())
    scene = _dream.the_scene(line)
    if scene and not _dream.a_dream_is_not_happening(line):
        return None
    if not scene:
        if _dream.SETTLED_IT.search(line) and _dream.told_in_the_turn_before(memory):
            return _settled(line, SETTLED_LINES)
        return None
    if SOMEONE_DIED.search(line[:line.find(scene)]) or A_FIRE.search(line[:line.find(scene)]):
        return None
    if DIED_MYSELF.search(scene):
        return _settled(line, OWN_DEATH_LINES)
    if ATTACKED.search(scene):
        return _settled(line, ATTACK_LINES)
    if ILL_IN_THE_DREAM.search(scene) and not PEOPLE_HURT.search(scene):
        return _settled(line, ILL_LINES)
    if SOMEONE_DIED.search(scene):
        return _settled(line, DEATH_LINES)
    if TEETH.search(scene):
        return _settled(line, TEETH_LINES)
    if A_FIRE.search(scene):
        return _settled(line, FIRE_LINES)
    if A_BREAK_IN.search(scene):
        return _settled(line, BREAK_IN_LINES)
    if A_BABY.search(scene):
        return _settled(line, BABY_LINES)
    if AN_EX.search(scene):
        return _settled(line, EX_LINES)
    if A_VISIT.search(scene):
        return _settled(line, VISIT_LINES)
    if PEOPLE_HURT.search(scene):
        return _settled(line, PEOPLE_HURT_LINES)
    if CHASED_OR_FALLING.search(scene):
        return _settled(line, CHASE_LINES)
    if A_GOOD_ONE.search(scene):
        return _settled(line, GOOD_LINES)
    return _settled(line, PLAIN_LINES)


def CLAIMS_INSTEAD(text, memory):
    try:
        return bool(respond(text, memory))
    except Exception:
        return False
