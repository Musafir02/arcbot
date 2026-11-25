import re

from .lookup import entry

ANSWERS = ("technology",)

MAC = ("mac", "macs", "macbook", "macbooks", "mac book", "imac", "i mac", "mac os", "macos",
       "osx", "os x", "apple computer", "apple laptop")
PC = ("windows", "pc", "pcs", "desktop", "desktops", "laptop", "laptops", "thinkpad",
      "chromebook", "surface", "computer", "computers", "hard drive", "hard disk", "ssd",
      "disk")

ROOM = ("storage", "space", "full", "free up", "clear", "delete", "disk", "running out",
        "make room", "room", "no space", "space left", "out of space", "no room")
ASK = ("storage", "space", "full", "free up", "clear", "delete", "disk", "room", "running out",
       "out of")
PC_ASK = ("windows", "pc", "pcs", "desktop", "disk", "hard drive", "hard disk", "ssd",
          "computer", "computers", "thinkpad", "chromebook", "surface", "space left",
          "space is left", "no space", "out of space")

CHECK = ("how much", "how full", "how many gb", "how big", "space left", "space is left",
         "no space left", "enough space", "percent", "%")

HOW_MUCH = ("space left", "is left", "left", "shows", "how much", "how full", "how many")

NOT_STORAGE = ("delete an app", "delete apps", "delete a app", "deleting an app", "delete the app",
               "delete my app", "delete an application", "delete the application", "remove an app",
               "removing an app", "uninstall", "uninstalling",
               "calorie", "calories", "kcal", "mac and cheese", "mac n cheese",
               "macaroni and cheese", "macaroni cheese", "macaroni",
               "program", "programs", "uninstalled", "reinstalled",
               "paint a room", "painting a room", "paint the room", "paint a wall",
               "paint the walls", "paint over", "painting over", "decorating", "decorate",
               "roller", "emulsion", "undercoat", "skirting", "wallpaper", "gloss paint")
GLASS = ("condensation", "condensation on", "condensation off", "condensed", "steamed up",
         "steaming up", "steams up", "misted up", "misting up", "fogged up", "fogging up",
         "wet windows", "windows wet", "damp on the windows", "pane", "panes", "squeegee",
         "windscreen", "windshield", "cleaning the windows", "clean the windows",
         "clean windows")
HOUSE = ("living room", "bedroom", "bedrooms", "kitchen", "bathroom", "hallway", "conservatory",
         "floorboards", "wallpaper", "skirting", "no window", "no windows", "windowless",
         "without a window", "bigger window", "curtains", "blinds") + GLASS

PHONE = ("phone", "iphone", "ipad", "android", "tablet", "handset", "sd card", "memory card",
         "usb stick", "usb drive", "external drive", "self storage", "warehouse", "garage",
         "shed", "loft", "attic", "rent")
OTHER = ("battery", "charge", "charging", "charger", "power", "slow", "sluggish", "hot",
         "overheating", "fan", "noisy", "loud", "memory", "ram", "backup", "time machine",
         "broken", "repair", "replace", "buy", "worth", "price", "cost")

MAC_SPACE = (
    "On a Mac: Apple menu > System Settings > General > Storage, click the bar and let it finish "
    "scanning - Photos and old iPhone backups are usually the two biggest. Empty the Bin, clear "
    "the Downloads folder, and turn on Optimise Mac Storage in Photos. A phone backup can be "
    "50GB on its own: Finder > your phone > Manage Backups.")
PC_SPACE = (
    "On Windows: Settings > System > Storage, then Temporary files - Windows Update leftovers and "
    "old installers are usually a few gigabytes. Turn on Storage Sense so they go on their own, "
    "then sort the Apps list by size and move photos and videos to an external drive or OneDrive. "
    "The Downloads folder is the other quiet hog.")
BOTH_SPACE = (
    "On a Mac: Apple menu > System Settings > General > Storage, then empty the Bin and clear "
    "Downloads. On Windows: Settings > System > Storage > Temporary files, and turn on Storage "
    "Sense. Photos, videos and old installers are the biggest three either way.")
BOTH_CHECK = (
    "On a Mac: Apple menu > System Settings > General > Storage. On Windows: Settings > System > "
    "Storage. Both show what is left and what is taking it, biggest first; keep 10 to 20% free.")
MAC_CHECK = (
    "Apple menu > System Settings > General > Storage shows the bar and what is taking it, biggest "
    "first. Keep about 10 to 20% free: below that a Mac slows down and updates refuse to install.")
PC_CHECK = (
    "Settings > System > Storage shows what is left and what is taking it, biggest first. Keep "
    "about 10 to 20% free: below that Windows slows down and updates fail to install.")


SD_CARD_COPY = (
    "Copy things off it before you delete anything: a card that fills up in a camera is often a "
    "confused file table, and bulk deleting on the camera loses shots. Plug the card into a "
    "laptop with a reader, drag the photos and videos to the computer or to Google Photos, then "
    "let the camera format the card from its own menu - not the computer. A bigger card is cheap: "
    "64GB is about a tenner, and take one labelled U3 or V30 if it is for video.")
SD_CARD_BUY = (
    "64GB to 128GB is plenty for photos, and 128GB or more for video, because a minute of 4K is "
    "about 400MB. Look for U3 or V30 on the label - that is a guaranteed write speed, and it is "
    "what 4K video needs - and buy from a shop you trust rather than a marketplace stall, because "
    "fake cards report more room than they have and then lose files. SanDisk, Samsung and Lexar "
    "are the safe names; a card is cheap enough to buy two.")
_BUYING_A_CARD = ("which", "what card", "what sd", "should i buy", "should i get", "recommend",
                  "best card", "best sd", "best memory", "worth buying", "how big", "what size",
                  "which size", "for video", "for a camera", "for my camera", "buying",
                  "bigger", "larger", "bigger card", "bigger sd", "bigger memory",
                  "more space", "more storage", "upgrade", "how much space")
_CARD_INTO_A_DEVICE = ("phone", "iphone", "ipad", "tablet", "android", "samsung", "galaxy",
                       "pixel", "switch", "nintendo", "steam deck", "console", "laptop",
                       "macbook", "computer", "slot", "put in", "put a card", "bigger card",
                       "extra space", "more memory", "adoptable", "expand", "expandable")
_A_CARD_BEING_CHOSEN = ("what size", "which size", "how big", "which card", "what card",
                        "should i buy", "should i get", "recommend", "best card", "need")
_A_CARD_ASK = ("does", "do i", "how do i", "can i", "is there a", "will it", "where")

_CARD_IN_IPHONE = (
    "There is no card slot in an iPhone, so no card goes in it: the room has to come from the "
    "phone or the cloud. Turn on iCloud Photos and Optimise iPhone Storage (Settings > Photos) "
    "and the full-size originals move off while small versions stay on the phone, then delete the "
    "videos you have already watched. If the card is a camera's, a card reader for the charging "
    "port copies the photos across.")
_CARD_IN_ANDROID = (
    "Most Android phones that still have a slot take a microSD card in the SIM tray, but recent "
    "flagships and the Pixel line have dropped it, so check the spec for your exact model first. "
    "If it has one, put the card in with the phone off and then choose: portable storage, where "
    "photos and videos go on the card, or internal storage (Settings > Storage > the card > "
    "Format as internal), where apps install there but the card is tied to that phone. 64GB or "
    "128GB labelled A1 or A2 is the right buy.")
_CARD_IN_TABLET = (
    "An iPad has no card slot, so its room comes from iCloud or from offloading photos and apps. "
    "An Android tablet usually takes a microSD, with the same choice as a phone: portable "
    "storage, or formatted as internal. A USB-C card reader copies a camera's photos across on "
    "either one.")
_CARD_IN_SWITCH = (
    "The Switch takes a microSD card under the kickstand at the back, behind the little flap: "
    "microSD only, not the full-size card a camera uses. 128GB or 256GB labelled U3 or A1 is "
    "plenty - games are 5GB to 15GB each - and after you put it in, Settings > Data Management "
    "moves the games across.")
_CARD_IN_LAPTOP = (
    "If the laptop has its own SD slot, push the card in until it clicks and it shows up as a "
    "drive; if it has none, a USB card reader is a few pounds. A card is for moving photos "
    "around rather than for more room on the laptop itself - for that an external SSD or a bigger "
    "internal drive is the answer. Copy the files across rather than working off the card, then "
    "format it in the camera.")
_DEVICE_OF_THE_CARD = (("switch", "nintendo", "steam deck", "console"),
                       ("iphone",),
                       ("laptop", "macbook", "notebook"),
                       ("ipad", "tablet"),
                       ("phone", "android", "samsung", "galaxy", "pixel", "handset"))
_CARD_IN_DEVICE = {0: _CARD_IN_SWITCH, 1: _CARD_IN_IPHONE, 2: _CARD_IN_LAPTOP,
                   3: _CARD_IN_TABLET, 4: _CARD_IN_ANDROID}


_CARD_NOT_READ = ("wont read", "won't read", "wont work", "won't work", "not reading",
                  "not recognised", "not recognized", "unexpectedly removed",
                  "not detected", "card error", "not showing", "doesnt show", "doesn't show",
                  "not working", "stopped working", "keeps saying", "failed", "corrupt",
                  "damaged", "unreadable", "cant read", "can't read")
_CARD_NOT_READING = (
    "A card the phone cannot read is usually its own file system or its contacts rather than the "
    "phone: take it out, check the gold contacts are clean, and put it back with the phone off. "
    "If another device can read it, copy everything off now and format it in the phone (Settings "
    "> Storage > the card > Format); if nothing reads it, the card has failed and a new one is "
    "the only fix. A card that comes and goes is on its way out, so back it up first.")
_CARD_FULL_IN_A_PHONE = (
    "Copy the photos and videos off it before you delete anything, because that is nearly all "
    "that is on it: plug the phone into a computer and drag them across, or let Google Photos "
    "upload them, then format the card in the phone under Settings > Storage. A bigger card is "
    "the real fix - 64GB or 128GB labelled A1 or A2 - and move the camera's settings so new "
    "photos and video save to the card.")


_NO_SLOT = ("no sd card slot", "no card slot", "no sd slot", "no slot", "doesnt have a slot",
            "doesn't have a slot", "without a card slot")
_NO_CARD_SLOT = (
    "With no card slot the room has to come from the phone or the cloud: turn on Google Photos or "
    "iCloud Photos and let it back up, delete the videos you have watched and offload the apps you "
    "do not use, and let Photos keep small versions rather than originals. If it is photos on a "
    "card you need to move, a USB-C card reader or an OTG drive plugs into the charging port.")


def _the_device_of_the_card(text):
    for index, words in enumerate(_DEVICE_OF_THE_CARD):
        if any(word in text for word in words):
            return _CARD_IN_DEVICE[index]
    return None


def _sd_card(memory, understood):
    text = _text(understood)
    if any(word in text for word in _NO_SLOT):
        return _NO_CARD_SLOT
    if any(word in text for word in _CARD_NOT_READ):
        return _CARD_NOT_READING
    in_a_device = _the_device_of_the_card(text)
    if in_a_device:
        if any(word in text for word in ("full", "no room", "no space", "filled")) and (
                "phone" in text or "android" in text or "samsung" in text or "tablet" in text
                or "galaxy" in text or "pixel" in text):
            return _CARD_FULL_IN_A_PHONE
        return in_a_device
    if any(word in text for word in _BUYING_A_CARD) and not any(
            word in text for word in ("full", "no room", "no space", "running out")):
        return SD_CARD_BUY
    return SD_CARD_COPY


def _text(understood):
    return " ".join(str(part or "") for part in
                    (understood.get("text"), understood.get("clean"))).lower()


def _names_mac(understood):
    text = _text(understood)
    return any(" " + word in " " + text or text.startswith(word) for word in MAC)


def _names_pc(understood):
    text = _text(understood)
    return any(" " + word in " " + text or text.startswith(word)
               for word in PC if word != "disk")


_DISK_WORDS = ("disk", "disc", "hard drive", "hard disk", "ssd", "disk space")


def _names_a_disk(understood):
    text = _text(understood)
    return any(word in text for word in _DISK_WORDS)


def _asking_how_much(understood):
    text = _text(understood)
    return any(word in text for word in CHECK)


def _mac_space(memory, understood):
    if not _names_mac(understood):
        return None
    return MAC_CHECK if _asking_how_much(understood) else MAC_SPACE


def _pc_space(memory, understood):
    if not (_names_pc(understood) or _names_mac(understood) or _names_a_disk(understood)):
        return None
    how_much = _asking_how_much(understood)
    if _names_mac(understood) and not _names_pc(understood):
        return MAC_CHECK if how_much else MAC_SPACE
    if not _names_pc(understood):
        return BOTH_CHECK if how_much else BOTH_SPACE
    return PC_CHECK if how_much else PC_SPACE


SD_CARD = ("sd card", "sdcard", "sd cards", "sd-cards", "micro sd", "microsd", "micro sd card",
           "memory card", "memory cards", "storage card", "flash card", "camera card",
           "photo card", "card in my camera", "card in the camera", "cards in my camera",
           "card for my camera", "card for the camera",
           "card slot", "memory card slot", "sd card slot", "microsd slot", "slot for a card")
SIM_CARD = ("sim card", "sim cards", "simcard", "simcards", "sim")
CARD_ROOM = ("full", "no room", "no space", "space", "storage", "free up", "clear", "delete",
             "copy", "move", "moving", "running out", "out of space", "fill up", "filled up",
             "filling up", "clean up", "sort out", "back up", "backup", "how much", "room left",
             "replace", "bigger", "buy")
SIM_NOT_THIS = ("sim only", "sim-only", "sim deal", "sim deals", "sim contract", "esim", "e-sim",
                "pay monthly", "pay as you go", "tariff", "rolling contract", "cheapest sim",
                "best sim", "which sim", "new sim", "order a sim", "sim free", "sim-free",
                "unlock", "network", "port my number", "switch network", "data plan",
                "upgrade", "cancel", "price", "cost", "cheap", "deal")


_FOOD_NOT_A_MACHINE = ("big mac", "mac and cheese", "mac cheese", "macaroni", "calorie",
                       "calories", "burger", "burgers", "mcdonalds", "mcdonald", "kfc")


def _stands_down_for_food(one):
    if not any(isinstance(part, tuple) and "mac" in part for part in one.key):
        return one
    one.avoid = one.avoid + tuple(word for word in _FOOD_NOT_A_MACHINE
                                  if word not in one.avoid)
    return one


WHERE_I_AM = ("location", "locations", "live location", "my location", "where i am",
              "where im", "where i'm", "where i was", "where i went", "where i've been",
              "where ive been", "whereabouts", "gps", "find me",
              "track my phone", "tracking my phone", "track my location",
              "tracking my location", "see where i am")
SHARE_IT = ("share", "shares", "sharing", "send", "sends", "show", "let them see",
            "let him see", "let her see", "let someone see", "track", "tracking",
            "see where", "sees where", "know where", "knows where", "find where",
            "who can see", "can they see", "can he see", "can she see", "sees my location",
            "knows my location")
NOT_WHERE_I_AM = ("file", "files", "folder", "folders", "screen", "screenshare",
                  "photos", "photo", "pictures", "picture", "album", "document", "documents",
                  "dropbox", "google drive", "onedrive", "icloud", "memory card", "usb",
                  "netflix", "spotify", "streaming", "password", "passwords", "account",
                  "wifi", "wi-fi", "printer", "flat", "house", "room", "rooms", "bill",
                  "bills", "rent", "money", "cost", "costs", "split", "custody", "car",
                  "lift", "ride", "taxi", "cooking", "toilet", "bathroom",
                  "police", "999", "911", "112", "ambulance", "fire brigade", "emergency",
                  "emergency services", "coastguard", "mountain rescue")

_ASKS_TO_STOP_SHARING = re.compile(
    r"\b(?:stop|stops|stopped|stopping|quit|prevent)\b[^.?!;]{0,48}"
    r"\b(?:shar(?:e|es|ed|ing)|send(?:s|ing)?|broadcast\w*|location|gps|found|see|sees|seeing|"
    r"seen|know|knows|knowing|tracked|tracking)\b"
    r"|\b(?:turn|turns|turning|switch|switches|switching|shut|shutting)\b[^.?!;]{0,20}"
    r"\b(?:off|out)\b"
    r"|\b(?:hide|hides|hiding|hidden|disable|disables|disabling|withhold|withholding)\b"
    r"|\b(?:don'?t|dont|do not|not)\s+(?:want\s+(?:to\s+)?)?"
    r"(?:shar(?:e|ing)|be\s+(?:found|seen|tracked))\b"
    r"|\b(?:don'?t|dont|do not|doesn'?t|not)\s+(?:want|wants|wanted|like)\b[^.?!;]{0,40}"
    r"\b(?:see|sees|seeing|know|knows|knowing|find|finds|finding|track|tracks|tracking|"
    r"shar(?:e|ing))\b"
    r"|\bwithout\b[^.?!;]{0,32}\b(?:knowing|seeing|finding\s+out|being\s+seen)\b"
    r"|\b(?:nobody|no\s+one|no-one|anyone|anybody)\b[^.?!;]{0,24}"
    r"\b(?:can|could|should|will|would|must|to)\b[^.?!;]{0,16}"
    r"\b(?:see|sees|know|knows|find|track)\b"
    r"|\bkeep\b[^.?!;]{0,24}\b(?:private|secret|hidden|to\s+myself)\b"
    r"|\bwho\s+(?:else\s+)?(?:can|could)\s+see\b|\bwho\s+sees\b"
    r"|\b(?:privacy|opt out|opting out|unshare|stop sharing)\b", re.IGNORECASE)

def _not_asking_to_stop(understood):
    if not isinstance(understood, dict):
        return True
    said = understood.get("text") or understood.get("clean") or ""
    if not said:
        said = " ".join(understood.get("words") or ())
    return not _ASKS_TO_STOP_SHARING.search(str(said))


_ASKS_HOW_IT_WORKS = re.compile(
    r"\bhow\s+(?:does|do|did|is|are|can)\b[^.?!;]{0,24}"
    r"\b(?:gps|phone|iphone|android|it|this|that|app|maps?|location\s+services?|"
    r"tracking|signal|satellites?)\b[^.?!;]{0,24}"
    r"\b(?:know|knows|work|works|worked|find|finds|track|tracks|get|gets|locate|locates)\b"
    r"|\bwhat\s+is\s+gps\b", re.IGNORECASE)


WHO_KNOWS = ("husband", "wife", "partner", "boyfriend", "girlfriend", "ex", "mum", "mom",
             "mother", "dad", "father", "son", "daughter", "brother", "sister", "boss",
             "friend", "friends", "someone", "somebody", "he", "she", "they", "them",
             "him", "her", "snapchat", "whatsapp", "instagram", "insta", "facebook",
             "messenger", "tiktok", "find my", "google", "life360", "app", "apps")
_ASKS_HOW_THEY_KNOW = re.compile(
    r"\bhow\s+(?:does|do|did|can|could|would|will)\s+(?:my|our|the|this|that|an?)?\s*"
    r"\b(?:" + "|".join(WHO_KNOWS) + r")\b[^.?!;]{0,26}"
    r"\b(?:know|knows|knew|knowing|see|sees|saw|seeing|find|finds|found|found\s+out|"
    r"track|tracks|tracked|tracking|locate|locates|worked\s+out|work\s+out)\b[^.?!;]{0,26}"
    r"\b(?:where\s+(?:i|im|i'?m|we)\s+(?:am|was|is|are|went|go|been|at|now|right\s+now)|"
    r"my\s+location|my\s+whereabouts)\b", re.IGNORECASE)


_ASKS_WHETHER_TO_SHARE = re.compile(
    r"\b(?:should|shall|ought)\s+(?:i|we)\b|"
    r"\bis\s+it\s+(?:safe|wise|ok|okay|alright|a\s+good\s+idea|worth|sensible|risky)\b|"
    r"\bwould\s+it\s+be\b|\bdo\s+(?:i|we)\s+need\s+to\b|\bam\s+i\s+(?:safe|risky|wrong)\b|"
    r"\bbetter\s+to\b|\bany\s+(?:risk|danger)\b",
    re.IGNORECASE)

SHARE_STEPS = (
    "Share it from the app you already message each other in, because then it is live and "
    "they can see you moving. WhatsApp: open the chat, tap the + or the paperclip, choose "
    "Location, then Share live location and pick 15 minutes, 1 hour or 8 hours. iPhone: in "
    "Messages tap the person's name at the top, then Share My Location, or use Find My > "
    "People > Share My Location. Android: Google Maps > your picture > Location sharing > "
    "New share. It keeps updating until you stop it, so stop it when you are there.")


def _the_said(understood):
    if understood is None:
        return ""
    if isinstance(understood, dict):
        for key in ("text", "clean", "norm_text", "plain"):
            if understood.get(key):
                return str(understood[key])
        return " ".join(str(w) for w in (understood.get("words") or ()))
    for key in ("text", "clean", "norm_text", "plain", "said"):
        said = getattr(understood, key, "")
        if said:
            return str(said)
    return str(understood)


def _asks_whether_to_share(understood):
    return bool(_ASKS_WHETHER_TO_SHARE.search(_the_said(understood)))


HOW_THEY_KNOW = (
    "Somebody sees where you are because an app on the phone is sharing it, and sharing "
    "is the default in the ones people use to keep in touch: Find My on an iPhone and "
    "Google's location sharing on Android both keep reporting until they are turned off, "
    "and anyone in a family group, a shared account or a live-location message is already "
    "watching. Look at who is on the list rather than at the phone: on an iPhone Settings "
    "> Privacy & Security > Location Services, and in Google Maps your picture then "
    "Location sharing, both show who can see you and for how long, and each name can be "
    "removed from there. If nobody is on either list, a shared account or a car's app is "
    "the next place to look.")

_ASKS_WHO_CAN_SEE = re.compile(
    r"\b(?:can|could|does|do|did|is|are|has|have)\b[^?.!]{0,30}\b"
    r"(?:see|sees|know|knows|show|shows|reveal|reveals|tell|tells|track|tracking|watch|"
    r"watching)\b[^?.!]{0,25}\bwhere\s+(?:i|we)\s+"
    r"(?:am|are|was|were)\b|"
    r"\bwho\s+can\s+see\b|\bwho\s+sees\b|\bwho\s+knows\s+where\b|"
    r"\b(?:see|sees|know|knows|show|shows)\b[^?.!]{0,20}\bmy\s+(?:location|whereabouts)\b",
    re.IGNORECASE)


_ASKS_FOR_THE_STEPS = re.compile(
    r"\bhow\s+(?:do|can|would|should)\s+i\b|\bhow\s+to\b|\blet\s+(?:them|him|her|someone|"
    r"somebody|my)\b|\bmake\s+(?:them|him|her|it)\b|\bso\s+(?:they|he|she)\s+can\b",
    re.IGNORECASE)


def _asks_who_can_see(understood):
    said = _the_said(understood)
    if _ASKS_FOR_THE_STEPS.search(said):
        return False
    return bool(_ASKS_WHO_CAN_SEE.search(said))


def _format_sharing_where_i_am(memory, understood):
    if _asks_who_can_see(understood):
        return HOW_THEY_KNOW
    if _asks_whether_to_share(understood):
        return (
            "That is yours to weigh, and the setting decides how much they see rather than "
            "whether to trust them: live sharing keeps updating for as long as the timer runs, so "
            "they watch you move and still have it afterwards, while a location sent once says "
            "only where you were at that moment. In WhatsApp tap the + or the paperclip, choose "
            "Location, then Send your current location for the point or Share live location for "
            "15 minutes, 1 hour or 8 hours; Google Maps, your picture then Location sharing, "
            "lists every share you have running and stops any of them.")
    return SHARE_STEPS


def _not_asking_whether_to_share(understood):
    if not isinstance(understood, dict):
        return True
    said = understood.get("text") or understood.get("clean") or ""
    if not said:
        said = " ".join(understood.get("words") or ())
    return not _ASKS_WHETHER_TO_SHARE.search(str(said))


def _not_asking_how_they_know(understood):
    if not isinstance(understood, dict):
        return True
    said = understood.get("text") or understood.get("clean") or ""
    if not said:
        said = " ".join(understood.get("words") or ())
    return not _ASKS_HOW_THEY_KNOW.search(str(said))


def _asks_how_they_know(understood):
    return not _not_asking_how_they_know(understood)


def _not_asking_how_it_works(understood):
    if not isinstance(understood, dict):
        return True
    said = understood.get("text") or understood.get("clean") or ""
    if not said:
        said = " ".join(understood.get("words") or ())
    return not _ASKS_HOW_IT_WORKS.search(str(said))


def _not_a_sharing_ask(understood):
    if _asks_who_can_see(understood):
        return True
    return (_not_asking_to_stop(understood) and _not_asking_how_they_know(understood)
            and _not_asking_how_it_works(understood))


SOCIAL = ("facebook", "fb", "instagram", "insta", "social media", "social", "friend",
          "friends", "someone", "somebody", "him", "her", "them", "my ex", "mum",
          "dad", "brother", "sister", "husband", "wife")
NOT_SOCIAL = ("number", "numbers", "call", "calls", "caller", "text", "texts", "sms",
              "spam", "phone", "iphone", "android", "whatsapp", "email", "e mail",
              "mail", "door", "road", "street", "pip", "drain", "chimney", "sink",
              "toilet", "wall", "garden", "parking", "drive",
              "artery", "arteries", "vein", "veins", "stent", "stents", "sinus",
              "sinuses", "airway", "bowel", "lung", "lungs", "catheter", "nose",
              "ear", "ears", "throat", "pipe", "pipes", "hose", "duct", "ducting",
              "gutter", "gully", "sewer", "filter", "filters",
              "blocked me", "blocks me", "has blocked me", "have blocked me",
              "they blocked me", "he blocked me", "she blocked me", "blocked my number",
              "blocked my account", "got blocked", "been blocked", "i was blocked",
              "i am blocked", "i got blocked")

def _unfriend_or_block(memory, understood):
    if not isinstance(understood, dict):
        return None
    said = understood.get("text") or understood.get("clean") or ""
    if not said:
        said = " ".join(str(w) for w in (understood.get("words") or ()))
    line = str(said).lower()
    unfollow = re.search(r"\bunfollow", line)
    block = re.search(r"\bblock(?:ed|ing)?\b", line)
    unfriend = re.search(r"\b(?:unfriend|defriend|remove (?:a )?friend)", line)
    if unfollow and not unfriend:
        return ("On Facebook open their profile, tap Following, then Unfollow - they are not "
                "told, and it takes their posts out of your feed without ending the "
                "friendship. On Instagram it is the same two taps: their profile, then "
                "Following, then Unfollow. If you want them gone further than that, the ... "
                "menu on their profile has Block, which stops them finding you, messaging you "
                "or seeing anything you post, and you can undo it in Settings > Blocked.")
    if block and not unfriend:
        return ("Blocking stops them finding you, messaging you or seeing anything you post: "
                "open their profile, tap the ... menu, then Block. They are not told, and you "
                "can undo it in Settings > Blocked. Unfriending is the smaller step - Friends, "
                "then Unfriend - which stops the posts but still lets them message you.")
    return ("On Facebook open their profile, tap Friends, then Unfriend - they are not told. "
            "Blocking goes further: the ... menu on their profile, then Block. On Instagram "
            "open their profile, tap Following to Unfollow, or the ... menu to Block. "
            "Unfriending only stops the posts; blocking stops them finding you, messaging you "
            "or seeing anything you post, and you can undo it in Settings > Blocked.")


ENTRIES = [
    entry("share-where-i-am", (WHERE_I_AM, SHARE_IT),
          _format_sharing_where_i_am,
          ask=SHARE_IT,
          bias=1,
          guard=_not_a_sharing_ask,
          avoid=NOT_WHERE_I_AM),

    entry("how-they-know-where-i-am", (WHERE_I_AM, SHARE_IT + (
              "find out where", "finds out where", "found out where", "find where",
              "found where", "knew where", "saw where", "work out where",
              "worked out where", "knows my location")),
          HOW_THEY_KNOW,
          ask=("know where", "knows where", "knew where", "know where i am", "see where",
               "sees where", "saw where", "find where", "find out where", "finds out where",
               "found out where", "found where", "tracking where", "knows my location",
               "worked out where", "work out where"),
          bias=1,
          guard=_asks_how_they_know,
          avoid=NOT_WHERE_I_AM + ("stop", "turn off", "hide", "dont want", "don't want",
                                  "without", "nobody", "no one", "private")),

    entry("unfriend-or-block-on-social",
          (("unfriend", "unfriending", "unfriended", "defriend", "unfollow", "unfollowing",
            "remove a friend", "remove friend", "remove them from my friends", "block",
            "blocking", "blocked"), SOCIAL),
          _unfriend_or_block,
          ask=("unfriend", "unfriending", "unfriended", "defriend", "unfollow", "unfollowing",
               "remove", "block", "blocking", "blocked", "how", "can i", "do i"),
          bias=1,
          avoid=NOT_SOCIAL),
    entry("mac-storage-full", (MAC, ROOM, HOW_MUCH),
          _mac_space,
          ask=MAC,
          bias=2,
          avoid=PHONE + OTHER + HOUSE + ("windows", "pc", "pcs", "desktop", "desktops",
                                 "thinkpad",
                                 "chromebook", "surface",
                                 "wifi", "wi-fi", "signal", "bars", "internet", "broadband",
                                 "loads", "loading", "browser",
                                 "big mac", "big macs") + NOT_STORAGE),
    entry("pc-storage-full", (PC, ROOM, HOW_MUCH),
          _pc_space,
          ask=PC_ASK,
          bias=1,
          avoid=PHONE + OTHER + HOUSE + MAC + NOT_STORAGE),
    entry("ssd-vs-hdd", (("ssd", "ssds", "solid state drive", "solid state", "nvme"),
                         ("hdd", "hdd's", "hard drive", "hard disk", "spinning disk", "disk",
                          "difference", "better", "faster", "slower", "worth", "upgrade",
                          "vs", "versus", "compare", "choose", "buy", "replace")),
          "An SSD has no moving parts, so the machine starts in seconds and apps open at once; a "
          "hard drive is a spinning disc and only wins on price for each gigabyte. For a laptop "
          "the SSD is the one upgrade that makes an old machine feel new - a 500GB one is cheap "
          "now and cloning the old disk across is a job a shop will do in an hour. Buy a big hard "
          "drive only for bulk storage and backups.",
          ask=("difference", "better", "faster", "slower", "worth", "upgrade", "upgrading",
               "upgrad", "vs", "versus",
               "compare", "choose", "buy", "replace", "what", "which", "should"),
          avoid=("space", "full", "free up", "left", "how much", "how many", "storage",
                 "make room", "no room", "running out", "clean up", "delete")),

    entry("sd-card-full",
          (SD_CARD, CARD_ROOM + _CARD_INTO_A_DEVICE + _A_CARD_BEING_CHOSEN),
          _sd_card,
          ask=CARD_ROOM + _CARD_INTO_A_DEVICE + _A_CARD_BEING_CHOSEN + _A_CARD_ASK, bias=3,
          avoid=("credit card", "bank card", "debit card", "payment", "pay", "owe", "debt",
                 "bill", "money", "borrow", "loan", "santander", "barclays", "halifax",
                 "gift card", "voucher", "birthday card", "christmas card", "greeting card",
                 "playing card", "card game", "loyalty card", "store card", "nectar",
                 "clubcard",
                 "format", "formatted", "formatting", "exfat", "fat32", "file system")),
    entry("sim-card-full", (SIM_CARD, CARD_ROOM + ("messages", "texts", "contacts", "numbers")),
          "A sim holds your number, your contacts and your texts, not photos, so what fills it "
          "is old messages. Delete the old texts first, and picture messages go first because "
          "they are big. Copy the contacts to the phone itself or to a Google or Apple account so "
          "they do not live on the card, then back up the texts you want to keep - a new sim "
          "does not bring the old messages with it.",
          ask=CARD_ROOM + ("messages", "texts", "contacts", "numbers"),
          bias=2,
          avoid=SIM_NOT_THIS + ("sim card slot", "sim tray", "no sim", "sim card is not",
                                "insert sim", "sim not working")),
]

ENTRIES = [_stands_down_for_food(one) for one in ENTRIES]
