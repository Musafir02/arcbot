
from .lookup import entry

ANSWERS = ("money", "work")


NOT_A_BUSINESS = (
    "phone", "mobile", "sim", "broadband", "energy", "gas", "electric", "electricity",
    "water", "gym", "tenancy", "landlord", "rent", "mortgage", "lease", "insurance",
    "car insurance", "pet insurance", "boiler", "council tax", "tv licence", "licence fee",
    "subscription", "streaming", "netflix", "spotify", "train", "parking", "ticket", "flight",
    "employer", "employee", "employees", "boss", "manager", "colleague", "hr", "job offer",
    "job interview", "interview", "redundancy", "notice period", "payslip", "paye", "payroll",
    "apprenticeship", "zero hours", "sick pay", "holiday pay", "maternity", "paternity",
    "refund", "return", "returns", "warranty", "guarantee", "faulty", "shop", "supermarket",
    "online order", "delivery", "parcel", "courier", "takeaway", "restaurant", "hotel",
)

BUSINESS_ASK = (
    "work", "works", "working", "client", "clients", "customer", "customers", "freelance",
    "freelancer", "freelancing", "self employed", "self-employed", "sole trader", "business",
    "businesses", "trade", "trades", "service", "services", "job", "jobs", "project",
    "projects", "rate", "rates", "day rate", "hourly rate", "hourly", "invoice", "invoices",
    "invoicing", "quote", "quotes", "charge", "charging", "contract", "contracts", "vat",
    "company", "limited company", "limited", "ltd", "start up", "startup", "my own",
    "for myself", "on my own", "as a freelancer", "as a sole trader",
)

NOT_THIS = NOT_A_BUSINESS + (
    "universal credit", "benefits", "child benefit", "pip", "esa", "student loan", "student",
    "pension", "pensioner", "graduate", "graduate scheme", "internship", "work experience",
    "cv", "interview", "apprenticeship", "university", "college", "exam", "course",
    "builder", "plumber", "electrician", "roofer", "decorator", "tradesman", "handyman",
    "doctor", "gp", "hospital", "nhs", "dentist", "school", "teacher", "nursery", "council",
    "my ex", "husband", "wife", "partner", "flatmate", "neighbour", "noise",
)

TRADES = ("builder", "plumber", "electrician", "roofer", "decorator", "tradesman", "handyman",
          "plasterer", "carpenter", "joiner", "painter", "landscaper", "locksmith",
          "gas engineer", "heating engineer")
_GOING_ALONE = (
    "my own", "for myself", "self employed", "self-employed", "sole trader", "my own boss",
    "go it alone", "going solo", "go solo", "freelance", "in business", "working for myself",
)
NOT_THIS_ELSEWHERE = tuple(word for word in NOT_THIS if word not in TRADES)


def _a_trade_is_their_own(understood):
    if not isinstance(understood, dict):
        return True
    text = " " + str(understood.get("clean") or understood.get("text") or "").lower() + " "
    if not any(word in text for word in TRADES):
        return True
    return any(word in text for word in _GOING_ALONE)


def _the_start_out_names_no_thing(understood):
    from ..memory.repeat import _starting_out_names_a_thing

    if not isinstance(understood, dict):
        return True
    text = " " + str(understood.get("clean") or understood.get("text") or "").lower() + " "
    if not _starting_out_names_a_thing(text):
        return True
    return any(word in text for word in _GOING_ALONE + (
        "business", "trade", "company", "firm", "shop", "sole trader"))


def _the_person_is_the_row(understood):
    return _a_trade_is_their_own(understood) and _the_start_out_names_no_thing(understood)


ENTRIES = [
    entry("start-a-business",
          (("start a business", "start my own business", "starting a business",
            "start up a business", "set up a business", "set up on my own", "start trading",
            "start working for myself", "work for myself", "be my own boss", "go it alone",
            "start a small business", "small business", "new business",
            "start out on my own", "start out freelance", "start out self employed",
            "start out in business", "start out working for myself", "start out selling",
            "start out",
            "side business", "side hustle", "side hustle", "on the side", "second income",
            "extra income", "start a side", "sell my own", "sell something",
            "start a company", "set up a company",
            "start my own", "set up my own", "my own trade", "my own firm", "my own shop",
            "going self employed", "go self employed", "going solo"),
           ("how do i", "how to", "where do i start", "what do i need", "first steps",
            "start", "starting", "begin", "set up", "should i", "do i need", "need to",
            "thinking of", "thinking about", "considering", "what should i know",
            "is it worth")),
          "Sell something before you register anything: one paying customer tells you more than "
          "a plan, and you can trade as a sole trader from the day you start. Then do three "
          "things in this order - register as a sole trader with HMRC (by 5 October after the "
          "end of your first tax year), open a second bank account so business money is not "
          "mixed with rent and shopping, and keep every receipt and invoice from day one, "
          "because the expenses are what cut the tax bill. Tell HMRC the date you started, not "
          "the date you got round to it. A name, a phone number and one clear service are "
          "enough to begin: a website and a logo can wait until someone is paying you.",
          avoid=NOT_THIS_ELSEWHERE + ("vat", "limited company", "ltd", "incorporate", "franchise",
                                      "licence", "premises", "plan", "business plan",
                                      "market", "marketing", "advertise", "advertising", "grow",
                                      "growing", "scale", "more customers", "more clients"),
          ask=BUSINESS_ASK + ("how do i", "how to", "where do i start", "what do i need",
                              "first steps", "start", "starting", "begin", "set up"),
          guard=_the_person_is_the_row,
          bias=1),

    entry("grow-your-business",
          (("grow my business", "grow the business", "growing my business", "more customers",
            "more clients", "market my business", "marketing", "advertise", "advertising",
            "get more work", "scale up", "expand my business", "bring in more work",
            "win more work", "repeat business", "referrals",
            "scale my business", "scale the business", "scale your business",
            "scaling a business", "scaling my business", "scaling up a business",
            "scaling up in business", "scale a business", "scale it up",
            "grow the company", "growing the company", "expand the business"),
           ("how do i", "how to", "how do", "where do i", "start", "get", "find", "more",
            "should", "best way", "what should", "what is", "whats", "what does", "mean",
            "means", "meaning", "explain")),
          "The cheapest new work is the client you already have: go back to everyone you worked "
          "for in the last year with one specific offer - a set number of hours a month, or the "
          "service you did not offer them last time. A past client is far more likely to say yes "
          "than a stranger. Then ask each happy client for one name and for a review in writing, "
          "and put those words where people actually look. Pick one channel and be there "
          "consistently rather than on four occasionally, and put your prices up 10% on new work "
          "before you think about hiring anyone.",
          avoid=NOT_THIS + ("stock market", "shares", "crypto", "plant", "tomato", "hair",
                            "nails", "garden", "lawn", "child", "baby", "beard",
                            "kettle", "kettles", "limescale", "descale", "descaler", "boiler",
                            "boilers", "shower head", "showerhead", "shower", "washing machine",
                            "dishwasher", "tumble dryer", "radiator", "radiators", "tap water",
                            "water pressure", "central heating", "scale in the", "scale in my",
                            "recipe", "recipes", "cooking", "baking", "oven",
                            "unsubscribe", "mailing list", "newsletter", "newsletters", "inbox",
                            "spam", "junk mail"),
          ask=BUSINESS_ASK + ("how do i", "how to", "how do", "where do i", "start", "get",
                              "find", "more", "should", "best way", "what should",
                              "what is", "whats", "what does", "mean", "means", "meaning",
                              "explain"),
          bias=1),

    entry("price-your-work",
          (("price my work", "price my services", "pricing", "what should i charge",
            "how much should i charge", "how much do i charge", "what do i charge",
            "day rate", "hourly rate", "set my rates", "set my rate", "work out my rate",
            "charge for my time", "charge for my work", "how much is my time worth",
            "price myself", "undercharging", "charge more"),
           BUSINESS_ASK),
          "Start from the money you need, not from what feels cheeky: add up your yearly costs "
          "(tools, insurance, software, travel, a phone) and the income you want to take home, "
          "add about a third on top for tax and quiet weeks, then divide by the days you can "
          "actually bill - about 220 a year if you work full time, and far fewer if you spend "
          "half the week on admin and chasing work. That gives a day rate; an hourly rate is "
          "that divided by six or seven. Then check three people doing the same job and put "
          "yourself in the middle. Quote a fixed price for a fixed job, not hours, and take a "
          "deposit of a third or a half up front.",
          avoid=NOT_THIS + ("how much does it cost", "battery", "boiler", "electricity",
                            "hidden fee", "hidden fees", "hidden charge", "hidden charges",
                            "booking fee", "admin fee", "administration fee", "service fee",
                            "processing fee", "card fee", "surcharge", "extra fee",
                            "extra charge", "handling fee", "convenience fee", "drip pricing",
                            "charged a fee", "charged an extra", "charged me a fee",
                            "at the checkout", "on the bill", "added a charge", "added a fee",
                            "raise my prices", "raise my rates", "put my prices up",
                            "prices up", "price rise", "raising prices", "increase my rates",
                            "increase my prices", "tell clients", "tell a client",
                            "tell my client", "tell my clients",
                            "petrol", "diesel", "taxi", "uber", "delivery", "postage",
                            "how much should i charge my phone", "how much should i tip",
                            "vat", "value added tax"),
          ask=BUSINESS_ASK,
          bias=1),

    entry("going-freelance",
          (("go freelance", "going freelance", "become freelance", "be freelance", "freelancing",
            "go self employed", "go self-employed", "become self employed",
            "become self-employed", "be my own boss", "work for myself", "go it alone",
            "leave my job to", "start freelancing", "start out freelance"),
           ("should", "worth", "is it", "is it worth", "thinking of", "thinking about",
            "considering", "not sure", "ready", "shall", "how do i know", "signs", "advice",
            "pros and cons")),
          "Test it on the money before anything else: work out what you need to live on for a year, add about a third for tax, your own kit and quiet weeks, and check you have one client who will pay it. Most people who last had six months of savings and a signed first job before they left. Start as a sole trader - it is free to register with HMRC, and a limited company can wait until the work is steady.",
          avoid=NOT_THIS + ("pension", "pensions", "sipp", "retire", "retirement", "tax return",
                            "self assessment", "register", "registering", "invoice",
                            "invoice them", "day rate", "first client", "first customer",
                            "chase an invoice", "when do i pay tax"),
          bias=1),

    entry("first-clients",
          (("first client", "first clients", "first customer", "first customers",
            "get clients", "find clients", "win clients", "get customers", "find customers",
            "get work", "find work", "more clients", "get more work", "find more clients",
            "clients from", "customers from"),
           ("how do i", "how to", "where do i", "where", "how do", "start", "starting",
            "first", "get", "find")),
          "The first three clients come from people who already know your work: a former "
          "employer or colleague, a friend who runs something, the local shop, a group you are "
          "already in. Pick one service you can name in a sentence, then tell twenty people "
          "you have started and what you charge - not a general announcement, one message each. "
          "Offer the first job small and priced so saying yes is easy, do it fast and well, "
          "and end every job by asking that client who else needs it. Two happy clients who "
          "recommend you beat any advert you could afford at this stage.",
          avoid=NOT_THIS,
          ask=BUSINESS_ASK + ("how do i", "how to", "where do i", "where", "how do",
                              "start", "starting", "first", "get", "find"),
          bias=1),

    entry("invoice-a-client",
          (("invoice", "invoices", "invoicing", "bill a client", "bill my client",
            "bill the client", "send a bill"),
           ("write", "writing", "written", "how do i", "what should", "what to put",
            "what do i put", "template", "checklist", "need", "needs", "send", "make",
            "include", "say",
            "has to be", "has to", "must be", "must have", "got to be", "goes on")),
          "An invoice needs seven things: your name and address, the client's name and "
          "address, a number of its own (0001, 0002 - never reused), the date, what you did "
          "with the dates you did it, the amount with the payment terms on it, and your bank "
          "details. Add your VAT number once you are registered, and put the terms in words - "
          "\"payment due within 14 days of the invoice date\" - plus what happens if it is "
          "late. Keep the same number series for ever and send it the day the work finishes, "
          "not at the end of the month: an invoice sent a fortnight late is paid a fortnight "
          "late. A PDF named with the number and the client is enough; a template in a word "
          "processor is all most people need.",
          avoid=NOT_THIS + ("energy", "water", "broadband", "council", "hospital", "nhs",
                            "unpaid", "chase", "chasing", "chas", "overdue", "not paid",
                            "not been paid", "hasn't paid", "hasnt paid", "will not pay",
                            "won't pay", "wont pay", "refuses", "owes me", "owe me",
                            "late payment", "late payments", "not paying", "remind",
                            "reminder", "reminders", "still waiting", "never paid",
                            "ignored", "ignoring", "debt", "debtor", "bad debt",
                            "keep", "keeping", "how long", "how many years", "retain",
                            "records", "archive", "shred", "dispose"),
          ask=("invoice", "invoices", "invoicing", "bill a client", "bill my client",
               "bill the client", "send a bill", "what has to be on", "what goes on",
               "on an invoice", "on a invoice", "what should be on"),
          bias=1),

    entry("client-not-paying",
          (("client", "clients", "customer", "customers", "invoice", "invoices", "bill",
            "payment", "payments"),
           ("won't pay", "wont pay", "not paying", "didn't pay", "didnt pay", "hasn't paid",
            "hasnt paid", "refusing to pay", "refuses to pay", "late payment", "late payments",
            "overdue", "not been paid", "still not paid", "never paid", "chase the payment",
            "chasing payment", "owes me", "owe me", "bad debt", "unpaid")),
          "Chase it in writing and in steps, because the paper is what wins later: on the day "
          "it is due, one short email with the invoice attached and a new date; a week later, a "
          "firmer one that says what happens next; after that, a letter before action giving 14 "
          "days. Then use the money claim online, which handles claims up to £10,000 for a fee "
          "that is added to what they owe. A business debt also carries statutory interest at "
          "8% above the Bank of England base rate from the due date, plus a fixed sum of £40 to "
          "£100 depending on the size of the debt - say so in the letter, because it is enough "
          "to make most late payers move. Stop doing new work for them the day the first "
          "payment is missed, and never hand over the finished work before the deposit.",
          avoid=NOT_THIS + ("refund", "shop", "company owes me", "energy", "broadband",
                            "friend", "family", "landlord", "rent", "ex", "loan", "borrow"),
          ask=("client", "clients", "customer", "customers", "invoice", "invoices",
               "business", "freelance", "freelancer", "self employed", "self-employed",
               "sole trader", "contractor", "my work"),
          bias=1),

    entry("vat-registration",
          (("vat", "value added tax", "vat registered", "vat registration", "vat number",
            "vat return", "vat threshold"),
           ("register", "registering", "registration", "do i need", "when", "threshold",
            "how much", "have to", "need to", "charge", "claim", "claim back", "already",
            "over", "go over", "went over",
            "add", "adding", "added", "on top", "include", "including", "included")),
          "Register when your sales go over £90,000 in any rolling twelve months, or when you "
          "think they will in the next thirty days; do it within 30 days of the end of the "
          "month you went over. Registering means you add 20% VAT to your prices and hand it "
          "over, but you also reclaim the VAT on what you buy for the business, so if your "
          "customers are other businesses it usually costs you nothing. Returns are normally "
          "quarterly and have to be filed from digital records. You can ask to deregister if "
          "your sales fall under £88,000.",
          avoid=NOT_THIS + ("car", "van", "fuel", "receipt", "refund", "shop", "price",
                            "how much is vat", "what is vat", "how much vat", "vat rate",
                            "rate of vat", "what rate", "vat on top", "charge vat on"),
          ask=("vat", "value added tax", "vat registered", "vat registration", "vat number",
               "vat return", "vat threshold"),
          bias=1),

    entry("business-bank-account",
          (("business bank account", "business account", "separate bank account",
            "separate account", "second bank account", "bank account for my business",
            "sole trader account", "business banking", "separate business"),
           ("need", "do i", "should i", "open", "how", "worth", "have to", "get",
            "set up", "why")),
          "As a sole trader you do not legally need one, and you should still open one: a "
          "separate account means every payment in is income and every payment out is a cost, "
          "which is most of a tax return done already. Mixing the two is the reason people "
          "spend a weekend with a shoebox. Free business banking for 12 to 18 months is normal "
          "at the moment, so compare two or three before you pick, and check the monthly fee "
          "afterwards and the cost of paying cash in. A second personal account works if no "
          "bank will take you yet. A limited company does have to have its own account.",
          avoid=NOT_THIS + ("switch", "switching", "overdraft", "joint", "savings",
                            "isa", "child", "student", "basic"),
          ask=("business bank account", "business account", "separate bank account",
               "separate account", "second bank account", "bank account for my business",
               "sole trader account", "business banking", "business", "sole trader",
               "self employed", "company", "ltd"),
          bias=1),

    entry("limited-or-sole-trader",
          (("limited company", "limited companies", "ltd", "incorporate", "incorporating",
            "limited or sole trader", "sole trader or limited", "company or sole trader",
            "sole trader or a company", "register a company", "set up a limited company",
            "start a limited company", "start a ltd", "start a limited", "start my own company"),
           ("should i", "which", "difference", "worth", "better", "set up", "become",
            "be a", "choose", "why", "do i need", "when",
            "start", "starting", "how do i",
            "what is", "what does", "mean", "plain english")),
          "A sole trader is the simplest thing that works: you and the business are the same "
          "person, you file a self assessment, your accounts stay private, and if it goes wrong "
          "you are personally on the hook for the debts. A limited company is a separate legal "
          "person, so your own money is mostly protected, but you file accounts at Companies "
          "House where anyone can read them, pay corporation tax on profits (19% to 25%), and "
          "take money out as a salary through payroll and as dividends, which means an "
          "accountant is worth having. It costs about £50 to set one up and a few hundred a "
          "year to run. Most people start as a sole trader and move over when profits are "
          "steady, when they take on a contract with real risk, or when they hire someone.",
          avoid=NOT_THIS + ("company car", "company name", "dissolve", "strike off",
                            "close my company", "company pension", "shares"),
          ask=("limited company", "limited companies", "ltd", "incorporate", "incorporating",
               "limited or sole trader", "sole trader or limited", "company or sole trader",
               "sole trader or a company", "register a company", "set up a limited company",
               "start a limited company", "start a ltd", "start a limited",
               "limited company", "ltd",
               "business", "self employed", "sole trader"),
          bias=1),

    entry("client-contract",
          (("contract", "contracts", "agreement", "write a contract", "simple contract",
            "client agreement", "terms of business", "scope of work", "quote for a job"),
           ("client", "clients", "customer", "customers", "freelance", "freelancer",
            "business", "self employed", "my work", "job", "write", "need", "simple",
            "how do i", "what should")),
          "One page is enough for a one-person business, and six lines cover almost everything: "
          "who you both are, exactly what you will do and by when, what it costs and when it is "
          "paid, what is included and what costs extra, who owns the finished work, and how "
          "either of you can end it. Add what happens if they change their mind - a set hourly "
          "rate for changes is the line that saves the job - and ask for a deposit of a third or "
          "half before you start. A quote they answer with \"yes, go ahead\" in an email is a "
          "contract already, so keep that email; you do not need a solicitor for a job worth a "
          "few hundred pounds, only for premises, staff or work that could hurt someone.",
          avoid=NOT_THIS + ("tenancy", "employment contract", "employment", "workplace",
                            "settlement", "nda", "lease", "mobile", "gym", "wedding",
                            "divorce", "prenup", "marriage"),
          ask=("client", "clients", "customer", "customers", "freelance", "freelancer",
               "business", "self employed", "sole trader", "contractor", "my work",
               "what should be in", "what goes in", "in a contract", "what to put in",
               "what should a contract", "contract template", "contract clauses"),
          bias=1),
]
