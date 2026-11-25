
from .lookup import entry

ENTRIES = [
    entry("car-write-off-payout",
          (("written off", "write off", "wrote it off", "wrote off", "total loss", "write-off",
            "cat s", "cat n",
            "wrote my car off", "wrote the car off", "wrote my van off", "write my car off",
            "writing my car off", "wrote mine off", "write it off"),
           ("payout", "pay out", "paid out", "how much", "settlement", "settle", "offer",
            "do i get", "get the money", "market value", "keep the car", "buy it back",
            "salvage", "argue", "appeal", "disagree", "too low", "process", "what now",
            "what happens", "accept")),
          "The insurer settles at the car's market value just before the crash, not what you "
          "paid for it: check their offer against three or four adverts for the same age, "
          "mileage and trim, and send them the links if it is low. Repairs can be offered "
          "instead when they are cheaper and safe. Ask what the salvage is worth if you want to "
          "keep the car - you buy it back, and it usually becomes Cat S or Cat N.",
          avoid=("dealer", "dealership", "forecourt", "sold me", "sold as seen",
                 "what does", "what is cat", "difference between", "mean"),
          bias=2,
          ask=("car", "van", "vehicle", "insurer", "insurance", "payout", "settle", "offer",
               "salvage", "written off", "write off", "total loss")),

    entry("home-office-desk",
          (("home office", "office at home", "desk setup", "desk set up", "wfh",
            "work from home", "working from home", "homeworking"),
           ("need", "buy", "get", "kit", "what do i need", "what should i", "essentials")),
          "Get the chair right first and the rest is cheap: an adjustable one so your feet are "
          "flat and the arms sit at elbow height, the screen top at eye level, a stack of books "
          "or a riser under a laptop, and a lamp beside your writing hand rather than behind "
          "you. A separate keyboard and mouse are the other fix worth paying for.",
          avoid=("council tax", "business rates", "tax", "expenses", "allowance", "claim",
                 "employer", "extension", "convert", "conversion", "loft", "build", "building",
                 "paint", "decorate", "rent", "landlord", "homework", "school", "teacher",
                 "year old", "kids", "children", "child", "revision", "exam", "study",
                 "toddler")),

    entry("hospital-bag-for-an-operation",
          (("hospital", "operation", "surgery", "day case", "day surgery", "admitted",
            "admission", "procedure", "overnight stay"),
           ("take", "bring", "pack", "bag", "need", "what to take", "what should i take",
            "what do i bring", "what to bring", "what do i need", "come in with")),
          "Take your medicines in their boxes, the admission letter, phone and charger, and "
          "loose clothes you can get on one-handed; for a day case add slippers with a back and "
          "a named bag for your clothes. Leave valuables at home, and ask the ward what they "
          "provide before you pack towels and toiletries.",
          avoid=("hospital bag", "maternity", "labour", "birth", "baby", "pregnant",
                 "pregnancy", "visit", "visiting", "gift", "present", "flowers", "should i go",
                 "do i need to go", "a and e", "casualty", "111", "999", "ambulance"),
          bias=2,
          ask=("take", "bring", "pack", "bag", "need", "hospital", "operation", "surgery")),
]
