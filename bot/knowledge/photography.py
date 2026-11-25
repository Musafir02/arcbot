from .lookup import entry

ANSWERS = ("technology",)

ENTRIES = (
    entry("photo-better", (("photo", "photos", "picture", "pictures", "camera", "photography",
                             "shots"),
                            ("better", "good", "great", "sharper", "sharp", "clear", "nicer",
                             "take", "taking", "improve", "tips", "professional", "like a pro",
                             "blurry", "blurred", "fuzzy", "smudged", "grainy", "come out",
                             "flat", "washed out", "hazy", "muddy", "soft")),
          "Get closer and hold the phone still: brace it against a wall, a table or your chest, "
          "and tap the screen on the person or thing you are shooting so the brightness is set "
          "for that and not for the sky behind. Wipe the lens on your sleeve first, because a "
          "smeared lens is what makes phone photos look flat and hazy. Take three and keep the "
          "sharpest - it costs nothing.",
          bias=1,
          avoid=("storage", "space", "full", "icloud", "cloud", "backup", "back up", "delete",
                 "deleting", "recover", "deleted", "transfer", "print", "printing", "printer",
                 "passport", "security camera", "doorbell", "dashcam", "webcam", "lens for",
                 "which camera", "what camera", "worth", "cost", "price", "buy", "buying",
                 "video call", "video calls", "teams", "zoom", "laptop", "call with",
                 "night", "nights", "at night", "dark", "in the dark", "evening", "low light",
                 "fireworks", "christmas lights", "camera is blurry", "camera blurry",
                 "tv", "telly", "television", "tv screen", "freeview", "sky box",
                 "set top box")),
    entry("photo-screen", (("screen", "screens", "tv", "telly", "television", "monitor"),
                           ("photo", "photos", "picture", "pictures", "photograph",
                            "photographing", "take a picture", "take a photo",
                            "taking a picture", "taking a photo", "snap", "shot of",
                            "capture")),
          "Turn the flash off and light the room from one side, because a bare flash on glass "
          "is just a white rectangle. Rest the phone on something solid, tap the screen to "
          "focus on a crisp corner, and stand a little to one side so the window behind you is "
          "not the thing in the glass. If bands crawl across the picture, that is the panel's "
          "flicker: step back and zoom instead, or film a second and keep a frame.",
          ask=("screen", "screens", "tv", "telly", "television", "monitor", "tablet"),
          avoid=("blurry", "blurred", "fuzzy", "signal", "aerial", "channel", "channels",
                 "no sound", "remote", "netflix", "screenshot", "webcam", "video call",
                 "white screen", "black screen", "cracked", "phone", "iphone", "android",
                 "app", "apps", "settings",
                 "reset", "mode", "picture mode", "brightness", "contrast", "tint", "colour",
                 "color", "source", "hdmi", "retune", "keeps going", "gone dark",
                 "gone funny", "went funny", "dark", "dim",
                 "show", "shows", "programme", "programmes", "episode", "listings",
                 "series")),
    entry("photo-moon-stars",
          (("moon", "stars", "starry sky", "milky way"),
           ("photo", "photos", "photograph", "photographs", "photographing", "photography",
            "picture", "pictures", "pic", "pics", "take", "takes", "taking", "shoot", "shoots",
            "shooting", "capture", "capturing", "snap", "snaps", "snapping", "camera", "phone",
            "how do i get", "how to get", "get a shot", "get the shot", "in a photo")),
          "A phone will not fill the frame with the moon: zoom to 10x or more, rest the phone on "
          "a wall, a fence or a tripod, turn the flash off, then press and hold on the moon until "
          "the focus locks and drag the little sun slider down until the moon is a white disc and "
          "not a glowing blob. A full moon is the worst night for detail - at half you get the "
          "craters along the shadow line. For stars, put the phone on something solid, use night "
          "mode, and give it the full few seconds it asks for.",
          bias=1,
          avoid=("phase", "phases", "moon sign", "full moon party", "moon landing", "moon in",
                 "astrology", "how many", "planet", "planets", "jupiter", "saturn",
                 "mars", "earth", "orbit", "solar system", "made of", "surface", "gravity",
                 "tide", "tides", "crater", "craters", "why does",
                 "far", "how far", "how far away", "distance", "away", "km", "miles",
                 "how old", "age", "how big", "how large", "how heavy", "how much does",
                 "how much is", "weigh", "weighs", "weight", "mass", "diameter", "size",
                 "how many", "what is", "whats", "when was", "when did", "who discovered",
                 "formed", "orbit", "distance from"),
          ),
    entry("phone-selfie",
          (("selfie", "selfies", "photo of myself", "photos of myself", "picture of myself",
            "picture of yourself", "photos of yourself"),
           ("good", "better", "great", "nice", "take", "taking", "how", "tips", "look",
            "flattering", "blurry", "blurred", "grainy", "dark", "come out", "turn out",
            "sharp")),
          "Hold the phone at eye level and a little above, just past arm's length, and turn your "
          "face towards a window or a lamp rather than towards the screen: light on the front of "
          "the face is the whole difference. Tap your face on the screen first, so the camera sets "
          "the brightness for your skin and not for the sky behind you, and take three or four - "
          "one will have your eyes open. Wipe the lens on your sleeve before you start.",
          bias=1,
          avoid=("storage", "space", "delete", "print", "passport", "low light"),
          ),
    entry("portrait-mode",
          (("portrait mode", "portrait", "bokeh", "background blur", "blurry background",
            "blur the background", "depth effect"),
           ("photo", "photos", "camera", "phone", "iphone", "android", "picture", "pictures",
            "use", "turn on", "switch on", "find", "how", "take", "selfie", "where", "worth")),
          "In the camera app it is the row of modes above the shutter: swipe to Portrait and wait "
          "for the yellow box to say Depth effect before you shoot, because a photo taken too "
          "early comes out with no blur. It works best a metre or two from the person with a "
          "plain background behind them, and on most phones you can tap the f-number afterwards "
          "to change how much is blurred. For two people, keep both faces the same distance away.",
          bias=1,
          avoid=("screen", "brightness", "rotate", "rotation", "airplane", "flight mode",
                 "silent", "vibrate", "do not disturb", "data saver", "battery saver",
                 "developer", "recovery"),
          ),
)



OLD_PHOTOS = (
    "Sort first, digitise second, and keep the paper: tip the lot onto a table and pull out the "
    "faces you cannot lose - the ones people will want in fifty years - then photograph each of "
    "those on a phone against a plain background, or use a flatbed scanner for the important "
    "ones. Store the prints in an acid-free box somewhere dry and dark rather than a hot loft, "
    "write the names and dates on the back of the keepers in pencil, and give the duplicates to "
    "the cousins who are in them. Digitising takes a phone app and an afternoon, and a box worth "
    "keeping usually shrinks by two thirds.")

ENTRIES = ENTRIES + (entry(
    "old-photos",
    ((("old photos", "old photo", "old photographs", "old pictures", "old picture",
       "photo album", "photo albums", "old family photos", "old family photographs",
       "family photos", "family photographs", "photos from my parents",
       "boxes of photographs", "box of photographs", "box of family photos",
       "box of old photos",
       "photos to keep", "what photos", "which photos", "photos in a box", "photos in the loft",
       "what do i keep", "what should i keep",
       "photographs", "prints", "negatives", "slides", "box of photos"),
      ("what should i do", "what do i do", "what to do", "store", "storing", "keep",
       "keeping", "get rid", "throw", "throw away", "digitise", "digitize", "scan",
       "scanning", "sort", "organise", "organize", "preserve", "save"))),
    OLD_PHOTOS,
    ask=("photo", "photos", "photograph", "photographs", "picture", "pictures", "album",
         "slides", "negatives", "prints"),
    avoid=("lost", "deleted", "delete", "recover", "icloud", "cloud", "backup", "back up",
           "transfer", "send", "share", "whatsapp", "email", "blurry", "blurred", "dark",
           "quality", "camera", "lens", "shutter", "selfie", "canvas", "frame",
           "how do i take", "better photos", "moon", "stars",
           "how do i scan", "how to scan", "how can i scan", "best way to scan",
           "scan document", "scanner",
           "presentation", "presentations", "slide deck", "slides for", "powerpoint", "keynote",
           "the slides", "my slides", "talk", "speech", "pitch", "webinar", "conference"),
    bias=2),)
