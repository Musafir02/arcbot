from .lookup import entry

ANSWERS = ("technology", "home-and-diy", "everyday-help")

_RAISE = ("screen", "monitor", "stand", "riser", "raiser", "laptop stand", "laptop riser", "laptop raiser", "monitor stand", "monitor riser",
          "screen stand", "screen riser",
          "raise my screen", "raise the screen", "screen height", "screen is low",
          "screen too low", "screen quite low", "screen is quite low", "laptop on books",
          "laptop on a box", "screen at eye level")

_ASKING = ("should i", "worth", "worth it", "get", "buy", "need", "any good", "help", "good idea",
           "does it help", "is it better", "which", "stand", "riser", "raiser", "height",
           "low", "too low", "quite low", "hurts", "hurting", "aching", "aching away")

ENTRIES = [
    entry("desk-screen-height", (_RAISE, _ASKING),
          "Yes, if your screen is below eye level: a stand or a pile of books brings the top of the "
          "screen to eye level, an external keyboard and mouse go at elbow height, and that is what "
          "stops the neck craning down all day. A laptop alone is always too low for long sessions, "
          "so the cheap version - box under the laptop, separate keyboard - does most of the job; buy "
          "the stand if you want it to look tidy or to swing up and down.",
          avoid=("battery", "charger", "crash", "won't turn on", "wont turn on", "bulging",
                 "overheating", "fan", "hard drive", "ssd", "ram", "memory upgrade", "spec",
                 "specs", "new laptop", "recommend a laptop",
                 "standing desk", "standing desks", "sit stand", "sit-stand", "sit to stand",
                 "walking pad", "treadmill desk", "desk you stand at",
                 "cracked", "crack", "tv", "telly", "phone", "broken", "flickering", "flicker",
                 "bigger", "larger", "4k", "resolution", "frozen", "black screen",
                 "second monitor", "second screen", "two screens", "two monitors",
                 "dual monitor", "dual screen", "dual monitors", "extra screen",
                 "another monitor", "another screen", "third screen"),
          bias=4),
]
