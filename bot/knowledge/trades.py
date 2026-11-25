from .lookup import entry

ANSWERS = ("home-and-diy", "money")

ENTRIES = [entry(
    "trades-out-of-hours",
    (("plumber", "plumbers", "electrician", "electricians", "gas engineer", "gas man",
      "heating engineer", "boiler engineer", "handyman", "locksmith", "roofer", "joiner",
      "drain man", "drainage"),
     ("get", "getting", "find", "finding", "book", "booking", "hire", "hiring", "recommend",
      "recommendation", "weekend", "weekends", "saturday", "sundays", "sunday", "evening",
      "evenings", "tonight", "night", "bank holiday", "out of hours", "emergency", "call out",
      "callout", "near me", "same day", "today")),
    "Book early and ask two questions: the call-out charge and the hourly rate after the first "
    "hour, because a weekend call-out is usually about double the weekday one and the quote over "
    "the phone is what holds them to it. Ring three local firms from eight in the morning and "
    "say what is wrong and when you need someone; the one who can tell you what it probably is "
    "on the phone is the one to book. Anything with water coming through is worth a call "
    "straight away - turn the stopcock off first - and a smell of gas is the free 24-hour gas "
    "emergency line, 0800 111 999, not a plumber.",
    avoid=("fix", "mend", "repair", "unblock", "bleed", "install", "fit it", "myself", "my own",
           "how do i change", "quote", "cost", "charge", "how much", "salary", "training",
           "become a plumber", "become an electrician", "course", "apprenticeship", "what is",
           "what does a", "difference between", "wire a", "socket", "fuse box", "boiler is",
           "boiler makes", "boiler noise", "pressure", "radiator", "leak"))]
