import datetime
import math
import re
import string

from ..memory.when import the_plan
from .geography import (carries_it_out_of_britain, country_extreme, crosses_a_border,
                        region_extreme)
from ..compose import pick
from .lookup import (a_price_not_a_loan, a_weight, entry, not_the_flat_of_something_made,
                     not_the_flat_you_live_in, tokens)

ANSWERS = ("geography-and-travel", "nature-and-weather")

REGIONS = ("africa", "europe", "asia", "america", "americas", "north america",
           "south america", "central america", "caribbean", "oceania", "australia",
           "uk", "britain", "england", "scotland", "wales", "ireland", "china", "india",
           "france", "italy", "spain", "germany", "egypt",
           "antarctica")

FLIGHT = ("plane", "planes", "flight", "flying", "airport", "security", "hand luggage",
          "carry on", "carry-on", "on board", "cabin bag")

FLIGHT_THREAD = frozenset({"plane", "planes", "flight", "flights", "flying", "fly",
                           "flew", "airport", "airports", "security", "security-check",
                           "boarding", "gate", "cabin", "luggage"})

FLIGHT_FOOD = ("Yes: solid food is fine to take through security and on the plane, so sandwiches "
               "and fruit are no problem. Only liquids are limited to 100ml containers in a clear "
               "bag, and there's a bin before security for anything over.")

FLIGHT_LIQUIDS = ("Only containers of 100ml or less, all fitting in one clear plastic bag, can go "
                  "through security. Fill an empty bottle after security, or ask for water on the "
                  "plane.")


_TICKET_LOST = re.compile(r"\b(lost|lose|losing|left|left it|forgot|forgotten)\b")
_TICKET_CHANGE = re.compile(r"\b(change|changed|changing|amend|amended|alter|altering|"
                            r"missed|earlier|later|different train|another train|wrong train)\b")
_TICKET_VALID = re.compile(r"\b(valid|any train|any time|off peak|restriction|restricted)\b")
_TICKET_PRINT = re.compile(r"\b(print|printed|paper|phone|mobile|app|e ticket|eticket|"
                           r"barcode|screenshot)\b")


def _a_ticket_already_bought(memory, understood):
    said = ((str((understood or {}).get("clean") or "") + " "
             + str((understood or {}).get("text") or "")).lower())
    if _TICKET_LOST.search(said):
        return ("Tell the train company as soon as you know: with an e-ticket you can show the "
                "confirmation again, and most operators will let you travel on the booking "
                "reference and the card you paid with. A paper ticket is rarely replaced, so "
                "photograph it when you buy it, and if it is lost at the station go to the ticket "
                "office before boarding rather than after.")
    if _TICKET_CHANGE.search(said):
        return ("It depends which ticket it is: an advance ticket can usually be changed up to "
                "the departure for a set fee (about £10 on most operators) plus any difference in "
                "fare, and an off-peak or anytime ticket needs no change at all, because it is "
                "already good for any train in its band. If the train is cancelled, your ticket "
                "is valid on the next one, and on a later one if you decide not to wait.")
    if _TICKET_PRINT.search(said):
        return ("An e-ticket on your phone is enough at almost every gateline now: have it open "
                "and the brightness up before you reach the barrier, and screenshot it in case "
                "signal drops. Print it only if the operator asks you to or you are crossing a "
                "border, where a paper copy is easier to show.")
    return ("Check the ticket's own restriction: an advance ticket is only good for the train it "
            "names, while an off-peak or anytime ticket is valid on any train in its band, so a "
            "different time is usually fine on those. If you are on the wrong train with an "
            "advance, speak to the guard before the ticket check rather than after it.")

JOURNEY_MODES = (
    "ferry", "ferries", "boat", "boats", "crossing", "crossings", "sailing", "sailings",
    "train", "trains", "rail", "railway", "railcard", "coach", "coaches", "national express",
    "megabus", "bus", "buses",
)

_FERRY_ASK = re.compile(r"\b(ferry|ferries|boat|boats|crossing|crossings|sailing|sailings|"
                        r"channel|dover|calais|holyhead|dublin|isle of wight)\b")
_COACH_ASK = re.compile(r"\b(coach|coaches|megabus|national express|bus|buses)\b")
_SEAT_ASK = re.compile(r"\b(seat|seats|reservation|reserve)\b")


def _book_a_journey(memory, understood):
    said = ((str((understood or {}).get("clean") or "") + " "
             + str((understood or {}).get("text") or "")).lower())
    if _FERRY_ASK.search(said):
        return ("Book the ferry as soon as the dates are fixed: foot passengers can usually buy "
                "on the day, but a car needs booking ahead and a summer weekend sailing sells "
                "out. Book with the operator itself rather than a resale site, and take the "
                "flexible ticket if the price is close, because a missed sailing with a car is "
                "the expensive way to learn. Turn up an hour before with a car and 30 minutes on "
                "foot, with the booking reference to hand.")
    if _COACH_ASK.search(said):
        return ("Book the coach two or three weeks ahead: the cheapest seats are the first to go "
                "and a seat bought on the day can cost two or three times as much. Pick the seat "
                "when the site offers it, be at the stop 15 minutes early because coaches leave "
                "on time, and take the luggage rules seriously - one case in the hold is usual "
                "and anything extra is paid for at the stop.")
    if _SEAT_ASK.search(said) and not _FERRY_ASK.search(said):
        return ("Reserve the seat when you book the ticket: on most trains a reservation is free "
                "with an advance ticket and a few pounds on a walk-up fare, and it is worth having "
                "on any long trip. Friday evening and Sunday afternoon trains are the busiest, so "
                "a booked seat there is the difference between sitting and standing.")
    return ("Book the train as soon as the date is fixed: advance singles tied to one train are "
            "usually about half the walk-up fare, and they go on sale around 12 weeks ahead. A "
            "railcard pays for itself in one or two long journeys, and check the price of two "
            "singles as well as a return - two advances are often cheaper than one return.")


def _the_booking_is_behind_them(understood):
    words = understood.get("words") if isinstance(understood, dict) else None
    if isinstance(words, (list, tuple)) and words:
        low = " " + " ".join(str(word) for word in words).lower() + " "
    else:
        low = " " + str((understood or {}).get("clean") or "").lower() + " "
    return " booked " not in low


_THE_TRIP_IN_THE_LINE = re.compile(
    r"\b(?:holiday|holidays|holidaymaker|trip|trips|travel|travelling|traveling|flight|flights|"
    r"fly|flying|hotel|hotels|abroad|away|resort|resorts|villa|cruise|airport|city\s+break|"
    r"beach|abroad|all\s+inclusive|package|packages|tour|tours|itinerary|hotel\s+and\s+flight|"
    r"flights\s+and\s+hotel|transfer|transfers|operator|operators|atol|booking)\b", re.I)


def _a_trip_to_arrange(understood):
    text = (understood or {}).get("clean") or ""
    if not text:
        words = (understood or {}).get("words") or ()
        text = " ".join(str(word) for word in words)
    return bool(_THE_TRIP_IN_THE_LINE.search(str(text).lower()))


def _in_a_flight_thread(memory):
    if not isinstance(memory, dict):
        return False
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns:
        return False
    last = turns[-1]
    if not isinstance(last, dict):
        return False
    said = " ".join(str(last.get(key) or "") for key in ("user", "bot"))
    return any(word in FLIGHT_THREAD for word in tokens(said))


TIP_US = ("In the US, tip 18 to 20% in restaurants (on the bill before tax), a dollar or two a "
          "drink at the bar, and 2 to 5 dollars a day for hotel housekeeping: staff there are paid "
          "by tips, so leaving nothing reads as a complaint.")

TIP_EUROPE = ("In most of Europe service is usually included and 5 to 10% is plenty for good "
              "service - round up in cafes and leave about a euro a drink at the bar.")

TIP_TAXI = ("For a taxi, round the fare up to the next note in most places and leave about 10% "
            "in the US; in Japan you tip nothing, and where there is no meter agree the fare before "
            "you get in.")

TIP_JAPAN = ("In Japan you don't tip at all: staff are paid properly and leaving money can cause "
             "offence, or a flustered chase down the street to give it back.")

TIP_ELSEWHERE = ("Where you are not sure, 10% is a safe default in a sit-down restaurant, "
                 "nothing is expected in a cafe, and a coin or two a day is plenty for hotel "
                 "housekeeping if the room has been done well.")


def _travel_advice(memory, understood):
    place = _place_in(memory, understood, WATER)
    if not place:
        return None
    return (f"For {place.title()} the Foreign Office travel advice is the page to read before you "
            f"book: it says which areas to avoid and what has changed lately, and it is the page "
            f"your insurer reads too. Insurance can be void in an area it advises against. Take the "
            f"embassy number with you.")


_US_PLACE = (r"\b(america|american|usa|states|new york|nyc|florida|california|vegas|"
             r"las vegas|los angeles|san francisco|miami|chicago|boston|seattle|washington|"
             r"texas|hawaii|orlando|brooklyn|manhattan|hollywood)\b")
_EUROPE_PLACE = (r"\b(france|paris|italy|rome|spain|portugal|greece|germany|europe|netherlands|"
                 r"amsterdam|london|lisbon|barcelona|madrid|berlin|munich|florence|venice|"
                 r"athens|crete|malta|cyprus|croatia|dubrovnik|prague|vienna|zurich|geneva|"
                 r"brussels|copenhagen|stockholm|oslo|helsinki|warsaw|budapest|istanbul|"
                 r"britain|england|scotland|wales|ireland|dublin)\b")


def _tipping(memory, understood):
    clean = understood.get("clean", "")
    if any(word in clean for word in ("taxi", "cab", "uber", "driver", "minicab")):
        return TIP_TAXI
    if any(word in clean for word in ("japan", "japanese", "tokyo", "kyoto")):
        return TIP_JAPAN + " In the US it is the opposite, 18 to 20%."
    if (re.search(_US_PLACE, clean) or re.search(r"\bin (the )?us\b", clean)):
        return TIP_US + " Most of Europe includes service instead."
    if re.search(_EUROPE_PLACE, clean):
        return TIP_EUROPE + " The US is the big exception."
    if any(word in clean for word in ("hotel", "housekeeping", "porter", "concierge", "bellboy",
                                      "maid", "room service", "tour guide", "tour", "excursion",
                                      "walking tour", "coach driver", "mover", "movers",
                                      "removal men", "man and van")):
        from .lifeadmin import _tipping as _the_uk_tip
        said = _the_uk_tip(memory, understood)
        if said:
            return said
    return TIP_ELSEWHERE


LONDON_AIRPORTS = (
    (("heathrow",), "From Heathrow the Elizabeth line is 30 minutes to Paddington for about 13 "
                    "pounds, the Piccadilly line about an hour for about 5.60, and the Heathrow "
                    "Express 15 minutes to Paddington for about 25."),
    (("gatwick",), "From Gatwick the train to Victoria takes 30 to 40 minutes: the Gatwick Express "
                   "is about 20 pounds, the ordinary Southern or Thameslink train about half that "
                   "and only ten minutes slower."),
    (("stansted",), "From Stansted the Stansted Express runs to Liverpool Street in about 47 "
                    "minutes for around 20 pounds, and a coach to Victoria is cheaper but slower."),
    (("luton",), "From Luton the shuttle bus runs to Luton Airport Parkway, then a fast train to "
                 "St Pancras takes about 25 minutes - book the bundle and it is cheaper."),
)


A_DEADLINE_NEED = re.compile(r"\b(?:i|we)\s+(?:need|needs|have|has|have got|got|want|wants|"
                             r"must)\b[^.!?]{0,40}?\b(?:get|be|make it|arrive)\b[^.!?]{0,20}?"
                             r"\b(?:for|by|before)\s+\d{1,2}(?:[.:]\d\d)?\s*(?:am|pm)?", re.I)

GROUND_TRANSPORT = re.compile(r"\b(?:bus|buses|coach|coaches|national express|megabus|train|"
                              r"trains|tube|underground|oyster|travelcard|travel card|driving|"
                              r"drive|parking|congestion charge|ulez)\b")
AIRPORT_WORD = re.compile(r"\b(?:airport|airports|heathrow|gatwick|stansted|luton|london city|"
                          r"city airport|southend|flight|flights|fly|flying|terminal)\b")


def _london_airport(memory, understood):
    clean = understood.get("clean", "")
    if GROUND_TRANSPORT.search(clean) and not AIRPORT_WORD.search(clean):
        return None
    if A_DEADLINE_NEED.search(clean):
        return None
    for names, answer in LONDON_AIRPORTS:
        if any(name in clean for name in names):
            return (answer + " A black cab is the expensive option: the train beats it into the "
                    "centre every time.")
    return ("London City is the closest airport to the centre: about 25 minutes to Bank on the "
            "DLR. Of the big four, Heathrow is the quickest into town - the Elizabeth line takes "
            "30 minutes to Paddington for about 13 pounds.")


def _flight_followup(answer):
    def reply(memory, understood):
        return answer if _in_a_flight_thread(memory) else None
    return reply

CAPITALS = {
    "australia": "Canberra, not Sydney: it was purpose-built as the compromise between Sydney and "
                 "Melbourne.",
    "canada": "Ottawa, not Toronto.",
    "brazil": "Brasília, not Rio, and a planned city built in four years.",
    "turkey": "Ankara, not Istanbul.",
    "switzerland": "Bern, the de facto capital; Switzerland has no official one.",
    "united states": "Washington DC, not New York.",
    "usa": "Washington DC, not New York.",
    "america": "Washington DC, not New York.",
    "netherlands": "Amsterdam, though the government sits in The Hague.",
    "france": "Paris.",
    "spain": "Madrid.",
    "portugal": "Lisbon.",
    "italy": "Rome.",
    "germany": "Berlin, since reunification in 1990.",
    "japan": "Tokyo.",
    "china": "Beijing.",
    "india": "New Delhi, not Mumbai.",
    "russia": "Moscow.",
    "new zealand": "Wellington, not Auckland.",
    "norway": "Oslo.",
    "sweden": "Stockholm.",
    "denmark": "Copenhagen.",
    "finland": "Helsinki.",
    "greece": "Athens.",
    "ireland": "Dublin.",
    "poland": "Warsaw.",
    "austria": "Vienna.",
    "belgium": "Brussels.",
    "hungary": "Budapest.",
    "czechia": "Prague.",
    "czech republic": "Prague.",
    "south korea": "Seoul.",
    "mexico": "Mexico City.",
    "argentina": "Buenos Aires.",
    "south africa": "Pretoria, though the parliament sits in Cape Town and the courts in "
                    "Johannesburg.",
    "afghanistan": "Kabul.",
    "albania": "Tirana.",
    "algeria": "Algiers.",
    "andorra": "Andorra la Vella.",
    "angola": "Luanda.",
    "antigua and barbuda": "Saint John's.",
    "armenia": "Yerevan.",
    "azerbaijan": "Baku.",
    "bahamas": "Nassau.",
    "bahrain": "Manama.",
    "bangladesh": "Dhaka.",
    "barbados": "Bridgetown.",
    "belarus": "Minsk.",
    "belize": "Belmopan, not Belize City.",
    "benin": "Porto-Novo, though the government sits in Cotonou.",
    "bhutan": "Thimphu.",
    "bolivia": "Sucre is the constitutional capital; La Paz is where the government sits.",
    "bosnia and herzegovina": "Sarajevo.",
    "bosnia": "Sarajevo.",
    "botswana": "Gaborone.",
    "brunei": "Bandar Seri Begawan.",
    "bulgaria": "Sofia.",
    "burkina faso": "Ouagadougou.",
    "burma": "Naypyidaw, not Yangon, which was the capital until 2006.",
    "burundi": "Gitega, since 2019; Bujumbura was the capital before that.",
    "cambodia": "Phnom Penh.",
    "cameroon": "Yaounde.",
    "cape verde": "Praia.",
    "central african republic": "Bangui.",
    "chad": "N'Djamena.",
    "chile": "Santiago.",
    "colombia": "Bogota.",
    "comoros": "Moroni.",
    "congo": "Two countries share the name: Brazzaville for the Republic of the Congo, Kinshasa "
             "for the Democratic Republic of the Congo.",
    "costa rica": "San Jose.",
    "cote d'ivoire": "Yamoussoukro, not Abidjan.",
    "croatia": "Zagreb.",
    "cuba": "Havana.",
    "cyprus": "Nicosia.",
    "democratic republic of the congo": "Kinshasa.",
    "djibouti": "Djibouti.",
    "dominica": "Roseau - not Santo Domingo, which is the Dominican Republic's capital.",
    "dominican republic": "Santo Domingo.",
    "dr congo": "Kinshasa.",
    "ecuador": "Quito.",
    "el salvador": "San Salvador.",
    "equatorial guinea": "Malabo.",
    "eritrea": "Asmara.",
    "estonia": "Tallinn.",
    "eswatini": "Mbabane for the administration, Lobamba for the parliament; the country was "
                "called Swaziland until 2018.",
    "ethiopia": "Addis Ababa.",
    "fiji": "Suva.",
    "gabon": "Libreville.",
    "gambia": "Banjul.",
    "georgia": "Tbilisi - the country's capital. The US state of Georgia has Atlanta.",
    "ghana": "Accra.",
    "grenada": "St George's.",
    "guatemala": "Guatemala City.",
    "guinea": "Conakry.",
    "guinea-bissau": "Bissau.",
    "guyana": "Georgetown.",
    "haiti": "Port-au-Prince.",
    "holland": "Amsterdam, though the government sits in The Hague.",
    "honduras": "Tegucigalpa.",
    "indonesia": "Jakarta, though the government is moving to a new capital, Nusantara, in Borneo.",
    "iran": "Tehran.",
    "iraq": "Baghdad.",
    "israel": "Jerusalem, which Israel calls its capital; most countries keep their embassies in "
              "Tel Aviv because the status is disputed.",
    "ivory coast": "Yamoussoukro, not Abidjan, which is the biggest city.",
    "jamaica": "Kingston.",
    "jordan": "Amman.",
    "kazakhstan": "Astana, which was called Nur-Sultan from 2019 to 2022.",
    "kiribati": "South Tarawa.",
    "kuwait": "Kuwait City.",
    "kyrgyzstan": "Bishkek.",
    "laos": "Vientiane.",
    "latvia": "Riga.",
    "lebanon": "Beirut.",
    "lesotho": "Maseru.",
    "liberia": "Monrovia.",
    "libya": "Tripoli.",
    "liechtenstein": "Vaduz.",
    "lithuania": "Vilnius.",
    "luxembourg": "Luxembourg City.",
    "madagascar": "Antananarivo.",
    "malawi": "Lilongwe.",
    "malaysia": "Kuala Lumpur, though the government sits in Putrajaya.",
    "maldives": "Male.",
    "mali": "Bamako.",
    "malta": "Valletta.",
    "marshall islands": "Majuro.",
    "mauritania": "Nouakchott.",
    "mauritius": "Port Louis.",
    "micronesia": "Palikir.",
    "moldova": "Chisinau.",
    "monaco": "Monaco itself - the country is one city.",
    "mongolia": "Ulaanbaatar.",
    "montenegro": "Podgorica.",
    "mozambique": "Maputo.",
    "myanmar": "Naypyidaw, not Yangon, which was the capital until 2006.",
    "namibia": "Windhoek.",
    "nauru": "Yaren, where the government sits; Nauru has no official capital.",
    "nepal": "Kathmandu.",
    "nicaragua": "Managua.",
    "niger": "Niamey.",
    "north korea": "Pyongyang.",
    "north macedonia": "Skopje.",
    "oman": "Muscat.",
    "pakistan": "Islamabad, not Karachi.",
    "palau": "Ngerulmud, a purpose-built capital; the biggest town is Koror.",
    "panama": "Panama City.",
    "papua new guinea": "Port Moresby.",
    "paraguay": "Asuncion.",
    "peru": "Lima.",
    "philippines": "Manila, not Quezon City, which is the bigger city.",
    "qatar": "Doha.",
    "romania": "Bucharest.",
    "rwanda": "Kigali.",
    "saint kitts and nevis": "Basseterre.",
    "saint lucia": "Castries.",
    "saint vincent and the grenadines": "Kingstown.",
    "samoa": "Apia.",
    "american samoa": "Pago Pago, on Tutuila - a US territory of its own, not Samoa, whose capital is Apia.",
    "guam": "Hag\u00e5t\u00f1a, a US territory in the Pacific.",
    "puerto rico": "San Juan, a US territory, not a state.",
    "bermuda": "Hamilton, a British territory - not Hamilton, Ontario.",
    "san marino": "San Marino.",
    "sao tome and principe": "Sao Tome.",
    "saudi arabia": "Riyadh.",
    "senegal": "Dakar.",
    "serbia": "Belgrade.",
    "seychelles": "Victoria.",
    "sierra leone": "Freetown.",
    "singapore": "Singapore itself - the country is one city.",
    "slovakia": "Bratislava.",
    "slovenia": "Ljubljana.",
    "solomon islands": "Honiara.",
    "somalia": "Mogadishu.",
    "south sudan": "Juba.",
    "sri lanka": "Sri Jayawardenepura Kotte, though Colombo is the one everyone names.",
    "sudan": "Khartoum.",
    "suriname": "Paramaribo.",
    "swaziland": "Mbabane for the administration and Lobamba for the parliament; the country is "
                 "called Eswatini now.",
    "syria": "Damascus.",
    "taiwan": "Taipei.",
    "tajikistan": "Dushanbe.",
    "tanzania": "Dodoma, not Dar es Salaam, which is the biggest city.",
    "thailand": "Bangkok.",
    "timor-leste": "Dili.",
    "togo": "Lome.",
    "tonga": "Nuku'alofa.",
    "trinidad and tobago": "Port of Spain.",
    "tunisia": "Tunis.",
    "turkmenistan": "Ashgabat.",
    "tuvalu": "Funafuti.",
    "uae": "Abu Dhabi, not Dubai.",
    "uganda": "Kampala.",
    "ukraine": "Kyiv.",
    "united arab emirates": "Abu Dhabi, not Dubai.",
    "united kingdom": "London.",
    "uk": "London.",
    "britain": "London.",
    "great britain": "London, though Great Britain is the island, not the country: the UK is the four nations together.",
    "uruguay": "Montevideo.",
    "uzbekistan": "Tashkent.",
    "vanuatu": "Port Vila.",
    "vatican city": "Vatican City, which is the whole country.",
    "venezuela": "Caracas.",
    "vietnam": "Hanoi, not Ho Chi Minh City.",
    "washington": "Olympia if you mean the state, Washington DC if you mean the city - the two "
                  "are different, and neither is New York.",
    "yemen": "Sanaa.",
    "zambia": "Lusaka.",
    "zimbabwe": "Harare.",
    "northern ireland": "Belfast, not Dublin - Dublin is the capital of the Republic of Ireland.",
    "new south wales": "Sydney, not Canberra - Canberra is the capital of the country.",
    "queensland": "Brisbane, not Canberra - Canberra is the capital of the country.",
    "south australia": "Adelaide, not Canberra - Canberra is the capital of the country.",
    "western australia": "Perth, not Canberra - Canberra is the capital of the country.",
    "tasmania": "Hobart, not Canberra - Canberra is the capital of the country.",
    "victoria": "Melbourne, not Canberra - Canberra is the capital of the country.",
    "northern territory": "Darwin, not Canberra - Canberra is the capital of the country.",
    "scotland": "Edinburgh, not London - London is the capital of the UK.",
    "wales": "Cardiff, not London - London is the capital of the UK.",
    "new york state": "Albany, not New York City - the city is not the capital of the state.",
    "new york": "Albany, not New York City - the city is not the capital of the state.",
    "california": "Sacramento, not Los Angeles or San Francisco.",
    "texas": "Austin, not Houston or Dallas.",
    "florida": "Tallahassee, not Miami.",
    "illinois": "Springfield, not Chicago.",
    "pennsylvania": "Harrisburg, not Philadelphia.",
    "michigan": "Lansing, not Detroit.",
    "missouri": "Jefferson City, not St Louis or Kansas City.",
    "maryland": "Annapolis, not Baltimore.",
    "alaska": "Juneau, not Anchorage.",
    "washington state": "Olympia, not Seattle - and not Washington DC, which is a different city.",
    "ohio": "Columbus.",
    "arizona": "Phoenix.",
    "colorado": "Denver.",
    "nevada": "Carson City, not Las Vegas.",
    "oregon": "Salem, not Portland.",
    "utah": "Salt Lake City.",
    "massachusetts": "Boston.",
    "north carolina": "Raleigh.",
    "south carolina": "Columbia.",
    "tennessee": "Nashville.",
    "virginia": "Richmond.",
    "minnesota": "St Paul, not Minneapolis.",
    "wisconsin": "Madison, not Milwaukee.",
    "indiana": "Indianapolis.",
    "kentucky": "Frankfort, not Louisville.",
    "oklahoma": "Oklahoma City.",
    "iowa": "Des Moines.",
    "kansas": "Topeka, not Wichita.",
    "nebraska": "Lincoln, not Omaha.",
    "idaho": "Boise.",
    "maine": "Augusta, not Portland.",
    "new mexico": "Santa Fe, not Albuquerque.",
    "hawaii": "Honolulu.",
    "alabama": "Montgomery.",
    "arkansas": "Little Rock.",
    "connecticut": "Hartford.",
    "delaware": "Dover.",
    "louisiana": "Baton Rouge, not New Orleans.",
    "mississippi": "Jackson.",
    "montana": "Helena.",
    "new hampshire": "Concord.",
    "new jersey": "Trenton.",
    "north dakota": "Bismarck.",
    "rhode island": "Providence.",
    "south dakota": "Pierre.",
    "vermont": "Montpelier.",
    "west virginia": "Charleston.",
    "wyoming": "Cheyenne.",
    "england": "London.",
    "morocco": "Rabat, not Casablanca.",
    "egypt": "Cairo.",
    "kenya": "Nairobi.",
    "nigeria": "Abuja, not Lagos.",
    "iceland": "Reykjavík.",
}

CITIES = {
    "lisbon": ("Alfama on foot and the 28 tram, Belém for the tower and the custard tarts, and "
               "LX Factory or Time Out Market for lunch. May is warm and busy, so book the tower "
               "and the popular restaurants ahead."),
    "rome": ("the Colosseum with a timed ticket, the Pantheon, and Trastevere in the evening for "
             "dinner. Book the Vatican museums online, and carry a refillable bottle: the "
             "fountains are free."),
    "florence": ("the Duomo climb, the Uffizi (book a slot), and the Oltrarno side of the river "
                 "for food. Two days is enough for those three if you don't queue for everything."),
    "paris": ("walk the Île de la Cité to the Marais, pick one big museum rather than three, and "
              "eat in a market street rather than by the Eiffel Tower. Book the Louvre or Orsay "
              "timed entry online."),
    "barcelona": ("the Gothic Quarter, the Sagrada Família (book weeks ahead), and the beach at "
                  "Barceloneta for half a day. Eat lunch at 2pm like locals; the good places open "
                  "then."),
    "madrid": ("the Prado, the Retiro park and the tapas streets around Plaza Mayor. Dinner "
               "starts late here, so plan on eating at 9pm or later."),
    "amsterdam": ("the Jordaan on foot, the Rijksmuseum and a canal walk at dusk. Book Anne Frank "
                  "House tickets online weeks ahead; they sell out completely."),
    "berlin": ("the Wall memorial and East Side Gallery, Museum Island, and Kreuzberg for food. "
               "It's a big, spread-out city, so buy a day travel ticket."),
    "prague": ("the Old Town at 7am before the crowds, Charles Bridge early, and the castle on the "
               "hill. Beer is cheaper than water, but change money at a bank, not a kiosk."),
    "vienna": ("the Ringstrasse, one grand coffee house and the Naschmarkt. Book the Spanish "
               "Riding School or a concert only if you're sure: they are pricey."),
    "edinburgh": ("the Royal Mile and the castle, Arthur's Seat for the view, and Leith for food. "
                  "In December it's dark by 4pm and the Christmas market fills the centre."),
    "london": ("pick one area a day rather than criss-crossing: South Bank, the museums in South "
               "Kensington, and the markets in the East End. The Tube is quickest; walking between "
               "central stops is often as fast."),
    "dublin": ("a walk through Trinity College and the Book of Kells, the Guinness Storehouse, and "
               "pubs away from Temple Bar for music. Book the Book of Kells online."),
    "porto": ("the river walk to Ribeira, a port cellar tour in Gaia, and the Lello bookshop early "
              "or late. The trams are the nicest way to see the city."),
    "seville": ("the Alcázar (book ahead), the cathedral and oranges everywhere in the streets of "
                "Santa Cruz. In high summer it is 40C, so sightsee before 11am and after 7pm."),
    "copenhagen": ("Nyhavn for the picture, Tivoli if it's open, and the food market at Torvehallerne. "
                   "Bikes are the real way to get around; hire one."),
    "stockholm": ("Gamla Stan, the Vasa ship museum, and a ferry out to one of the islands. "
                  "Everything is walkable in the centre."),
    "athens": ("the Acropolis first thing with a timed ticket, the Acropolis Museum, and the Plaka "
               "in the evening. It is hot and shadeless up there, so take water and a hat."),
    "istanbul": ("Hagia Sophia, the Blue Mosque and the Grand Bazaar on the old side, and a ferry "
                 "across to Asia for lunch. Buy an Istanbulkart for the trams and ferries."),
    "new york": ("pick two neighbourhoods a day: the High Line and Chelsea, the Lower East Side, "
                 "and Brooklyn across the bridge. Book the big attractions online and walk a lot."),
    "tokyo": ("one district a day: Shibuya and Shinjuku, Asakusa and Ueno, and Tsukiji or "
              "Toyosu for breakfast. Get a Suica card for the trains and carry cash for small "
              "places."),
    "kyoto": ("Fushimi Inari at 7am before the crowds, the bamboo grove early too, and Gion at "
              "dusk. Buses are slow and packed: the subway plus walking is better."),
    "reykjavik": ("the harbour and Hallgrímskirkja, and use the city as a base for the Golden "
                  "Circle. Book the Blue Lagoon ahead and don't rinse the cave water off in the "
                  "showers."),
    "venice": ("get lost in Cannaregio and Dorsoduro away from St Mark's, cross the Grand Canal "
               "on the traghetto, and go early or late. Day-trippers leave by 5pm and the city "
               "feels completely different."),
    "boston": ("walk the Freedom Trail, eat in the North End, and cross to Cambridge for a "
               "half-day. The T is small and easy."),
    "bath": ("the Roman baths and the Pump Room, the Royal Crescent and the Circus, and a walk "
             "along the canal. It is small enough for a day, and the baths sell timed tickets "
             "that are worth booking the night before."),
    "ljubljana": ("the riverside cafes and the Triple Bridge, the castle on the hill for the "
                  "view, and a walk through Tivoli park. It is small and flat, so a day covers "
                  "it before you head out to Lake Bled."),
    "krakow": ("the main square and the cloth hall, Wawel castle, and Kazimierz for food and "
               "bars. Book Auschwitz-Birkenau a few days ahead and take the early bus: it is a "
               "full half-day."),
    "budapest": ("the parliament and the Danube bank, the thermal baths (Szechenyi or Gellert), "
                 "and the ruin bars in the old Jewish quarter. Buy a travel card for the trams "
                 "and metro; the city is long, not wide."),
    "brussels": ("the Grand Place, the comic-strip museum and the art nouveau houses, with the "
                 "waffles and fries people come for. Two days covers it, and Bruges or Ghent is "
                 "an hour away by train."),
    "milan": ("the Duomo and its roof terraces, the Last Supper (book weeks ahead) and the "
              "Navigli canals in the evening. Most people use it as a base: Lake Como is an hour "
              "by train."),
    "naples": ("the archaeology museum first, then pizza in the old town, and Pompeii or "
               "Herculaneum on a day trip by train. It is loud and fast, so keep bags in front "
               "of you and use the metro rather than the buses."),
    "munich": ("Marienplatz and the English Garden, the beer halls, and a day out to "
               "Neuschwanstein or Dachau if you have the time. The trains are excellent; buy a "
               "day ticket rather than singles."),
    "zurich": ("the old town on both sides of the river, a boat on the lake and the view from "
               "Uetliberg. Everything is expensive, so eat lunch from a bakery or a supermarket "
               "counter and save the restaurants for one evening."),
    "oslo": ("the opera house roof you can walk on, the Vigeland park and the fjord boats. It "
             "is compact but pricey: buy a seven-day transport pass, and take the train to Bergen "
             "if you have three days."),
    "helsinki": ("the cathedral square, the market hall and the design district, with a ferry "
                 "to Suomenlinna for half a day. In summer the evenings are light until "
                 "midnight, so eat late."),
    "tallinn": ("the walled old town, the viewing platforms on Toompea, and the cafes in "
                "Kalamaja. A day covers the old town; take a ferry to Helsinki or a bus to Riga "
                "if you have longer."),
    "dubrovnik": ("walk the city walls early or after 5pm once the cruise crowds have gone, "
                  "then the cable car for the view. Take water and a hat up there, and swim off "
                  "the rocks by the Buza gate."),
    "marrakech": ("the Jemaa el-Fna at dusk, the Bahia palace and the Ben Youssef school, and a "
                  "hammam. Agree taxi prices before you get in, and buy in the souks slowly: the "
                  "first price is never the price."),
    "santorini": ("Oia for the sunset once, but stay in Imerovigli or Pyrgos so you can sleep, "
                  "and take a boat out to the volcano. Book months ahead for July and August, or "
                  "come in May or September for the same light and half the people."),
    "valencia": ("the City of Arts and Sciences, the old town round the cathedral, and the "
                 "beach a short tram ride away. This is the home of paella, so eat it at lunch, "
                 "not in the evening."),
    "granada": ("the Alhambra first (book weeks ahead, it sells out), then the Albaicin at "
                "sunset from the San Nicolas viewpoint, with free tapas with drinks. Two nights "
                "is right: one is not enough for both."),
    "san sebastian": ("the two beaches, the pintxos bars in the old town, and the walk up Monte "
                      "Igueldo for the view. Eat standing at the bar: one or two pintxos a place, "
                      "then move on."),
    "san francisco": ("the Golden Gate on foot or by bike, the ferry building, and one "
                      "neighbourhood properly rather than five badly. Layers matter: the fog "
                      "rolls in and the temperature drops ten degrees by the water."),
    "chicago": ("the architecture boat tour, the Art Institute and the river walk, then deep "
                "dish once for the experience. The Loop is walkable and the trains from O'Hare "
                "run all night."),
    "los angeles": ("pick two areas and expect to drive between them: Venice or Santa Monica, "
                    "the Griffith observatory at sunset, and one studio tour if you want one. It "
                    "is far bigger than it looks on a map."),
    "toronto": ("the islands for the skyline view, Kensington market and the Distillery "
                "district, and the St Lawrence market for lunch. The streetcars work well, and "
                "Niagara Falls is a day trip by train."),
    "sydney": ("the harbour walk from the Opera House to Mrs Macquarie's chair, the Bondi to "
               "Coogee coastal path, and the ferry to Manly. Use the ferries as sightseeing: the "
               "Opal card caps the day."),
    "singapore": ("the hawker centres for every meal, Gardens by the Bay in the evening, and "
                  "the southern ridges walk. It is hot and humid all year, so walk early and "
                  "save the air-conditioned museums for midday."),
    "bangkok": ("the Grand Palace and Wat Pho early, the river boats rather than taxis, and "
                "street food in Chinatown at night. April and May are the hottest months, and "
                "from June the rain comes in short afternoon bursts."),
    "dubai": ("the old creek and its abra boats, the desert at sunset, and one tall building "
              "rather than three. From June to September it is over 40C and people live indoors; "
              "November to March is the season."),
    "cape town": ("Table Mountain first thing if the cloud is off it, the Cape Point drive, and "
                  "Bo-Kaap and the V&A for the afternoon. The wind and cloud decide your plan, "
                  "so keep the mountain day flexible."),
    "mexico city": ("the Zocalo and the Templo Mayor, the Frida Kahlo house in Coyoacan, and "
                    "the food markets. It sits at 2,240m, so take the first day slowly, and use "
                    "the metro in the day and taxis at night."),
    "havana": ("the old town in the morning, the Malecon at sunset, and a 1950s car once for "
               "the ride rather than the tour. Bring cash: foreign cards often do not work, so "
               "take enough for the whole trip."),
    "buenos aires": ("Recoleta and the cemetery, San Telmo on a Sunday for the market, and a "
                     "steak and a tango show in the evening. People eat at 10pm, so shift your "
                     "day later or you will be dining alone."),
    "rio de janeiro": ("Copacabana and Ipanema for the beach, Sugarloaf and Christ the Redeemer "
                       "early before the crowds, and Santa Teresa for the afternoon. Take nothing "
                       "valuable to the beach and use the metro after dark."),
    "hanoi": ("the old quarter on foot with a pho stop, Hoan Kiem lake in the morning, and a "
              "coffee on a balcony over the traffic. Cross the road by walking steadily: the "
              "mopeds go round you, not through you."),
    "manchester": ("the Northern Quarter for food and records, the Museum of Science and Industry "
                   "in the old station, and a tram out to Salford Quays for the Lowry and the "
                   "Imperial War Museum North. Book the Old Trafford or Etihad tour ahead."),
    "liverpool": ("the Albert Dock and the two cathedrals, the Cavern and the Beatles Story if you "
                  "want the music, and the ferry across the Mersey for the skyline. The Walker and "
                  "the World Museum are free."),
    "birmingham": ("the canals round Brindleyplace, the museum and art gallery, and a curry in the "
                   "Balti Triangle rather than the middle of town. The library roof is free and "
                   "has the best view in the city."),
    "leeds": ("the Victoria Quarter and Kirkgate Market in the centre, then Headingley or Chapel "
              "Allerton for dinner. The Royal Armouries is free, and so are the city's galleries."),
    "sheffield": ("the Winter Garden and the Peace Gardens, then Kelham Island for food and a "
                  "brewery tap. The Peak District is half an hour by bus, which is the reason "
                  "most people go."),
    "newcastle": ("the Quayside and the Millennium Bridge, Grainger Town for the arcades, and the "
                  "Baltic in Gateshead for the view. The metro to Tynemouth is a good half day at "
                  "the coast."),
    "nottingham": ("the castle and the Trip to Jerusalem, which is built into the rock, then "
                   "Hockley for food and shops. Wollaton Hall and its deer park are free and a "
                   "good hour."),
    "bristol": ("the harbourside and the SS Great Britain, the Clifton Suspension Bridge, and "
                "Wapping Wharf or Stokes Croft for food. It is a walking city; the buses are the "
                "weak point."),
    "brighton": ("the pier and the pebble beach, the Lanes for shops and the North Laine for food. "
                 "The i360 is the view and the South Downs are a short bus ride."),
    "york": ("the Minster, the Shambles and the city walls, which take an hour and cost nothing. "
             "Book the Minster and the Jorvik ahead in summer."),
    "glasgow": ("Kelvingrove and the Burrell Collection, the Necropolis for the view, and the West "
                "End for food. The subway is a single loop and gets you round the centre."),
    "cardiff": ("the castle in the middle of town, the old arcades for covered shopping streets, "
                "and Cardiff Bay for the waterfront. The national museum is free."),
    "belfast": ("the Titanic museum on the old slipway, the Cathedral Quarter for pubs, and a black "
                "taxi tour if you want the history. The Giant's Causeway is a day out north."),
    "cork": ("the English Market for lunch, St Anne's tower for the bells, and a pint in the old "
             "town. Kinsale and Cobh are short bus or train trips."),
    "galway": ("the Latin Quarter for pubs and buskers, the Claddagh walk along the water, and a "
               "day on Inishmore or in Connemara. Book the Aran ferry ahead in summer."),
}


WHERE_TO_GO = {
    "spain": ("Spain",
               "Barcelona for a city and a beach in one trip. Seville for the Alcázar and "
               "the tapas. Madrid for the museums, with Toledo a short train ride away."),
    "italy": ("Italy",
               "Rome for the ancient city and the Vatican. Florence for the art you can walk "
               "between. Naples and the Amalfi coast for pizza and sea."),
    "france": ("France",
               "Paris for the museums and the food. Lyon for the best eating in the country. "
               "Provence for small towns and markets, and don't rush it."),
    "portugal": ("Portugal",
               "Lisbon for trams, tarts and the river. Porto for the port cellars and the "
               "bookshop. The Algarve for beaches and cliffs."),
    "greece": ("Greece",
               "Athens for the Acropolis and street food. Santorini for the view. Naxos for "
               "beaches and cheaper rooms."),
    "japan": ("Japan",
               "Tokyo for the city and the food. Kyoto for temples and old streets. Osaka "
               "for eating, with a rail pass once you visit more than one."),
    "netherlands": ("The Netherlands",
               "Amsterdam for the canals and the museums. Haarlem or Delft as a quieter "
               "base. The country is small, so everywhere is easy to reach."),
    "germany": ("Germany",
               "Berlin for the history and the nightlife. Munich for beer gardens and the "
               "Alps. The Rhine and Mosel valleys for small wine towns."),
    "ireland": ("Ireland",
               "Dublin for a city break. Galway and the Burren if you fly into Shannon. "
               "The west is the trip."),
    "scotland": ("Scotland",
               "Edinburgh for the castle and the Old Town. The Highlands for lochs and "
               "mountains. A car helps north of the cities."),
    "england": ("England",
               "London for the museums and the markets. Bath for the Roman baths. The Lake "
               "District for hills and walking."),
    "turkey": ("Turkey",
               "Istanbul for mosques, bazaars and the ferries up the Bosphorus. Cappadocia "
               "for the balloon flights at sunrise. The coast if you want to swim."),
    "morocco": ("Morocco",
               "Marrakech for the medina and the food. Fes for the crafts and the old city. "
               "Essaouira for the coast and the wind."),
    "croatia": ("Croatia",
               "Split for a Roman palace and ferries to the islands. Dubrovnik for the "
               "walls, early before the crowds. Zadar for quieter evenings."),
    "iceland": ("Iceland",
               "Reykjavik for the city. The south coast to Vik for waterfalls and black-sand "
               "beaches. The ring road takes longer than most people think."),
    "norway": ("Norway",
               "Oslo for the museums and the opera house. The train to Bergen for the "
               "fjords, because the journey is half the point. Tromsø in winter for the "
               "northern lights."),
    "thailand": ("Thailand",
               "Bangkok for temples and street food. Chiang Mai for the north. A flight "
               "south for the islands."),
    "mexico": ("Mexico",
               "Mexico City for the food and the museums. Oaxaca for markets and mezcal. "
               "Tulum if you mainly want the beach."),
    "united states": ("The States",
               "New York for a first trip. San Francisco and the coast for California. "
               "Chicago for food and the lake in summer."),
    "india": ("India",
               "Delhi for the history. Jaipur and Jodhpur for Rajasthan. Kerala for the "
               "backwaters, and one region rather than criss-crossing the country."),
    "australia": ("Australia",
               "Sydney for the harbour and the beaches. Melbourne for food, with the Great "
               "Ocean Road from there. Flying between the cities is normal."),
    "egypt": ("Egypt",
               "Cairo for the pyramids and the museum. Luxor for the temples and the Valley "
               "of the Kings. Aswan for a slower stretch by the river."),
    "canada": ("Canada",
               "Toronto and Montreal for cities. Banff and Jasper for the Rockies. Vancouver "
               "if you want sea and mountains together."),
    "czechia": ("Czechia",
               "Prague for the old town and the castle. Český Krumlov for a smaller, quieter "
               "base. Brno for wine and fewer tourists."),
    "hungary": ("Hungary",
               "Budapest for the baths, the ruin bars and the parliament. The Danube bend if "
               "you want a break from the city. Lake Balaton in summer."),
    "poland": ("Poland",
               "Kraków for the old town, with Auschwitz as a sobering trip out. Warsaw for "
               "the rebuilt city and the museums. Gdańsk for the coast."),
    "austria": ("Austria",
               "Vienna for the palaces and the coffee houses. Salzburg for the old town and "
               "the hills. Innsbruck for the Alps."),
    "switzerland": ("Switzerland",
               "Zurich or Lucerne as a base. The Bernese Oberland for the mountain trains. A "
               "rail pass pays off fast."),
    "belgium": ("Belgium",
               "Brussels briefly, for the Grand Place and the museums. Bruges for the "
               "canals, and Ghent for the same with fewer people. Both are short train rides "
               "from Brussels."),
    "sweden": ("Sweden",
               "Stockholm for the islands and the museums. The archipelago in summer. "
               "Gothenburg for a second city."),
    "denmark": ("Denmark",
               "Copenhagen for the city and the food. Aarhus for a second city. Malmö is a "
               "train ride over the bridge."),
    "finland": ("Finland",
               "Helsinki for the design and the saunas. Lapland in winter for the snow and "
               "the northern lights. A summer cabin by a lake in the other season."),
    "new zealand": ("New Zealand",
               "Queenstown and the southern lakes for the mountains. The North Island for "
               "beaches and volcanoes. Pick one island rather than trying both."),
    "china": ("China",
               "Beijing for the Wall and the Forbidden City. Xi'an for the terracotta army. "
               "Shanghai for a city you can walk."),
    "vietnam": ("Vietnam",
               "Hanoi for the old quarter and the food. Hoi An and the coast by train or a "
               "short flight south. Ha Long Bay for limestone islands and a boat."),
    "dubai": ("Dubai",
               "A short trip: the old creek and the souks in the morning. The desert in the "
               "evening. One big mall, and the marina at night."),
    "singapore": ("Singapore",
               "The hawker centres first. Gardens by the Bay after dark. A walk round Tiong "
               "Bahru for the old flats and the coffee."),
    "cape town": ("Cape Town",
               "Table Mountain on a clear morning. The Cape peninsula drive. The winelands "
               "for the wine farms, and a car to do any of it."),
    "cuba": ("Cuba",
               "Havana for the old town and the cars. Viñales for tobacco country. Take "
               "cash, because cards barely work."),
    "argentina": ("Argentina",
               "Buenos Aires for the food and the nightlife. Mendoza for wine. Patagonia if "
               "you have the time."),
    "brazil": ("Brazil",
               "Rio for the beaches and the views. The Pantanal for wildlife. Salvador for "
               "music and the old town."),
}

COUNTRY_ALIASES = {
    "usa": "united states",
    "the states": "united states",
    "america": "united states",
    "us": "united states",
    "uk": "england",
    "great britain": "england",
    "britain": "england",
    "holland": "netherlands",
    "czech republic": "czechia",
    "uae": "dubai",
}


COUNTS_AS_A_THING = re.compile(
    r"\b(?:a|an|some|any|another|one|no|every|this|that|these|those|my|your|our|their|his|"
    r"her|its|roast|roasted|frozen|whole|raw|stuffed|cooked|leftover|defrosted|fresh|"
    r"smoked)\s+$", re.I)
COUNTS_AS_A_TRIP = re.compile(
    r"\s+(?:holiday|holidays|vacation|vacations|trip|trips|break|breaks|getaway|getaways|"
    r"week|weeks|weekend|weekends|fortnight|resort|resorts|flight|flights|hotel|hotels|"
    r"hostel|hostels|tour|tours|guide|guides|map|maps|visa|visas|beach|beaches|city|"
    r"coast|island|islands|airport|airports|transfer|transfers|excursion|excursions|"
    r"adventure|adventures)\b", re.I)


ALSO_A_THING = frozenset({"turkey", "china", "jersey", "guinea", "chile"})


def _a_thing_not_a_place(clean, name):
    if str(name or "").strip().lower() not in ALSO_A_THING:
        return False
    low = " " + " ".join(str(clean or "").lower().split()) + " "
    found_a_thing = False
    for match in re.finditer(r"\b" + re.escape(name.lower()) + r"\b", low):
        if COUNTS_AS_A_THING.search(low[:match.start()]):
            if COUNTS_AS_A_TRIP.match(low[match.end():]):
                return False
            found_a_thing = True
        else:
            return False
    return found_a_thing

TRIP_WORDS = re.compile(
    r"\b(?:trip|trips|holiday|holidays|travel\w*|visit\w*|flying|flights?|honeymoon|abroad|"
    r"somewhere|city break|weekend (?:away|in)|a week in|fortnight|beach\w*|going away|"
    r"get away|day out|get(?:ting)? to|where (?:should|shall|do|can) i go)\b", re.I)


A_FACT_OF_THE_COUNTRY = re.compile(r"\bcapital\b", re.I)


def _the_country_was_the_question(memory, name):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return False
    last = turns[-1]
    said = last.get("user") if isinstance(last, dict) else None
    if not isinstance(said, str) or not said.strip():
        return False
    if TRIP_WORDS.search(said):
        return False
    if not A_FACT_OF_THE_COUNTRY.search(said):
        return False
    before = _find_in(said, WHERE_TO_GO) or _find_in(said, COUNTRY_ALIASES)
    if not before or before == name:
        return False
    return True


def _where_to_go(memory, understood):
    clean = understood.get("clean", "")
    name = _find_in(clean, WHERE_TO_GO) or _find_in(clean, COUNTRY_ALIASES)
    if not name:
        return None
    if _a_thing_not_a_place(clean, name):
        return None
    if _us_is_a_pronoun(clean, name):
        return None
    if not TRIP_WORDS.search(clean) and _the_country_was_the_question(memory, name):
        return None
    country = COUNTRY_ALIASES.get(name, name)
    label, body = WHERE_TO_GO[country]
    return f"{label}: {body}"


_US_AS_A_PLACE = re.compile(r"\bthe\s+us\b", re.I)


def _us_is_a_pronoun(clean, name):
    if str(name or "").strip().lower() != "us":
        return False
    return not _US_AS_A_PLACE.search(str(clean or ""))


def _country_trip(memory, understood):
    clean = understood.get("clean", "")
    name = _find_in(clean, WHERE_TO_GO) or _find_in(clean, COUNTRY_ALIASES)
    if _us_is_a_pronoun(clean, name):
        return None
    label, body = WHERE_TO_GO[COUNTRY_ALIASES.get(name, name)]
    return f"{label}: {body}"


COUNTRY_TRIP_WORDS = ("going to", "going", "off to", "heading to", "heading off to", "fly to",
                      "flying to", "flew to", "trip to", "travel to", "travelling to",
                      "traveling to", "holiday in", "holidays in", "visiting", "visit to",
                      "week in", "fortnight in", "honeymoon in", "booked to", "we are in",
                      "im in",
                      "see in", "visit in", "in a week", "for a week",
                      "in a fortnight", "for a fortnight")

PACKING_WORDS = ("pack", "packs", "packing", "packed", "suitcase", "suitcases", "luggage",
                 "clothes", "clothing", "wear", "wearing", "jumper", "jumpers", "coat",
                 "coats", "jacket", "jackets", "shoes", "trainers", "toiletries",
                 "swimwear", "bikini", "hand luggage", "carry on")

NOT_A_COUNTRY_TRIP = ("live in", "living in", "move to", "moving to", "emigrate", "residency",
                      "work in", "working in", "job in", "jobs in", "study in", "driving",
                      "drive", "car hire", "hire car", "licence", "insurance", "visa",
                      "safe", "safety", "dangerous", "crime", "hospital", "doctor", "school",
                      "schools", "how much", "cost", "costs", "money", "currency", "weather",
                      "expensive", "cheap", "cheaper", "cheapest", "pricey", "affordable",
                      "costly", "dear", "prices", "price", "budget", "luxury", "spend",
                      "worth it",
                      "enough", "cover it", "cut it", "go far",
                      "too hot", "too cold", "best time", "what month", "when to go",
                      "time difference", "plug", "adaptor", "adapter", "water", "tap water",
                      "jab", "jabs", "vaccine", "vaccinations", "malaria", "pet", "dog", "cat",
                      "how long to fly", "how long is the flight", "flight time",
                      "hours in the air", "how long does it take to fly")
NOT_A_COUNTRY_TRIP += PACKING_WORDS

CLIMATES = {
    "mediterranean": {1: (8, 15), 2: (9, 16), 3: (11, 18), 4: (12, 20), 5: (15, 24), 6: (19, 29),
                      7: (22, 32), 8: (22, 32), 9: (19, 28), 10: (15, 23), 11: (11, 18),
                      12: (9, 15)},
    "temperate": {1: (1, 7), 2: (1, 8), 3: (3, 11), 4: (5, 15), 5: (8, 19), 6: (11, 22),
                  7: (13, 24), 8: (13, 24), 9: (11, 20), 10: (8, 15), 11: (4, 10), 12: (2, 7)},
    "hot-summer": {1: (0, 4), 2: (-1, 5), 3: (3, 10), 4: (8, 17), 5: (13, 23), 6: (17, 27),
                   7: (19, 29), 8: (18, 28), 9: (14, 23), 10: (8, 16), 11: (3, 9), 12: (1, 5)},
}
CITY_CLIMATE = {
    "lisbon": "mediterranean", "rome": "mediterranean", "florence": "mediterranean",
    "barcelona": "mediterranean", "madrid": "mediterranean", "athens": "mediterranean",
    "seville": "mediterranean", "istanbul": "mediterranean", "venice": "mediterranean",
    "porto": "mediterranean", "paris": "temperate", "amsterdam": "temperate",
    "london": "temperate", "edinburgh": "temperate", "dublin": "temperate",
    "berlin": "temperate", "copenhagen": "temperate", "stockholm": "temperate",
    "reykjavik": "temperate", "new york": "temperate", "boston": "temperate",
    "prague": "hot-summer", "vienna": "hot-summer", "budapest": "hot-summer",
}
MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6, "july": 7,
    "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "jun": 6, "jul": 7, "aug": 8, "sep": 9,
    "sept": 9, "oct": 10, "nov": 11, "dec": 12,
}


CITY_COUNTRY = {"rome": "italy", "venice": "italy", "florence": "italy", "milan": "italy",
                "naples": "italy", "paris": "france", "lisbon": "portugal", "porto": "portugal",
                "barcelona": "spain", "madrid": "spain", "seville": "spain", "athens": "greece",
                "santorini": "greece", "crete": "greece", "tokyo": "japan", "kyoto": "japan",
                "bangkok": "thailand", "istanbul": "turkey", "dubai": "dubai",
                "reykjavik": "iceland", "oslo": "norway", "bergen": "norway",
                "edinburgh": "scotland", "marrakech": "morocco", "mexico city": "mexico",
                "sydney": "australia", "melbourne": "australia", "delhi": "india",
                "mumbai": "india", "split": "croatia", "dubrovnik": "croatia", "zadar": "croatia"}


CITY_BEST_TIME = {
    "london": "May, June and September: 18-22C and the long evenings. July and August are warm "
              "and crowded, and November to February is grey, wet and dark by 4.30pm.",
    "edinburgh": "May, June and September: 15-20C, and daylight until nearly 11pm in June; August "
                 "is the Festival and the Fringe, which is either why you go or when to avoid. "
                 "November to February is dark by 4pm.",
    "bath": "May to September for the baths, the crescent and the canal; April and October are "
            "quieter and still fine. December is the Christmas market, which is the busiest "
            "weekend of the year.",
    "dublin": "May, June and September: 16-20C and the longest days. July and August are the "
              "driest and busiest, and November to February is wet, with dark by 4.30pm.",
    "amsterdam": "April to June and September: 15-22C and the canals at their best, with the "
                 "tulips at Keukenhof in late April. July and August are the busiest, and "
                 "November to February is cold, wet and dark early.",
    "brussels": "May, June and September: 17-22C, and the Grand Place flower carpet in mid-August "
                "every second year. July and August are warm and quiet at weekends, and winter "
                "is grey and wet.",
    "paris": "April to June and September to early October: 18-24C and the parks at their best. "
             "July and August are hot and many small restaurants close, and November to February "
             "is grey and cool.",
    "munich": "May to September: 20-25C, beer gardens and the Alps an hour away; late September "
              "is Oktoberfest, which doubles hotel prices. December brings the Christmas markets.",
    "zurich": "May to September for the lake, the old town and the mountain railways, at 22-26C in "
              "midsummer. December to February is cold and clear, which is when the Alps look "
              "their best.",
    "berlin": "May to September: 20-25C, outdoor cafes, the lakes, and the city at its most "
              "relaxed. July and August are the warmest and busiest, and November to February is "
              "grey and cold.",
    "prague": "April to June and September: 15-22C and the old town before the crush. July and "
              "August are busy and 25C+, and December is cold with the Christmas markets.",
    "vienna": "April to June and September: 18-24C, and the ball season runs January to March. "
              "July and August are hot and the opera houses close, and December has the markets.",
    "budapest": "April to June and September: 20-26C, and the thermal baths are good in cool "
                "weather too. July and August are 30C+, and December brings the Christmas "
                "markets along the Danube.",
    "krakow": "May to September: 20-25C and the main square at its best; April and October are "
              "quiet and still fine. December to February is cold with snow and a Christmas "
              "market.",
    "ljubljana": "May, June and September: 20-26C, and Lake Bled is warm enough to swim from "
                 "June. July and August are the busiest, and winter is cold and quiet.",
    "copenhagen": "May to August: 18-22C, long days, and the harbour baths open from June. July "
                  "is the busiest and the jazz festival, and November to February is dark by "
                  "4pm and cold.",
    "stockholm": "May to August: 18-23C and light until late, with midsummer at the end of June. "
                 "The archipelago is best from July to mid-August, and winter is dark with short "
                 "days.",
    "helsinki": "June to August: 18-23C with almost no night, and the archipelago ferries "
                "running. January and February are the coldest, with the best chance of snow, "
                "and December is dark.",
    "tallinn": "June to August: 18-22C, the old town at its best and white nights in June. "
               "December to February is cold and snowy, and the Christmas market is one of the "
               "prettiest in Europe.",
    "reykjavik": "June to August gives midnight sun, open highland roads and puffins; February and "
                 "March are best for the northern lights. November is dark, wet and icy, so it is "
                 "the one month I would skip.",
    "oslo": "May to September: 18-23C, and the fjord islands are a ferry ride from the centre. "
            "June has the longest days, and November to February is cold and dark, with skiing an "
            "hour out of town.",
    "bergen": "May to September: 15-19C and the fjord trips running, with light until late in June "
              "and July. It rains most of the year, so pack a shell whatever the month.",
    "rome": "April, May, late September and October: 20-26C and the ruins walkable. July and "
            "August are 30C+ with the fountains as the only relief, and August means half the "
            "restaurants shut.",
    "venice": "April, May, late September and October: 18-24C, warm, not crowded and everything "
              "open. July and August are hot and packed, and November to January brings acqua "
              "alta.",
    "florence": "April to June and September to October: 20-28C and the galleries without the "
                "August crush. July and August are 30C+ and busy, and winter means cool days and "
                "short queues.",
    "milan": "April to June and September: 20-27C and the aperitivo season. July and August are "
             "hot and humid and the city half empties, and January is cold with the sales on.",
    "naples": "April to June and September: 22-27C, with the ferries to Capri and the Amalfi "
              "coast running. July and August are hot and busy, and November to March is quiet "
              "and wet.",
    "lisbon": "May, June and September: warm and dry with fewer people. July and August are hot "
              "and busy with the tourists, and November to February is wet, though milder than "
              "the north.",
    "porto": "May, June and September: 18-24C and dry, with the Douro valley at its best and the "
             "vines in leaf. July and August are warm and busy, and November to March is wet and "
             "grey.",
    "valencia": "April to June and September to October: 20-26C, and the sea still swimmable in "
                "October. July and August are 30C+ and busy, and March is Las Fallas if you want "
                "the crowds.",
    "granada": "April to June and September to October: 18-28C, and the Alhambra bookable without "
               "a fight. July and August are 35C+ inland, and winter is cold up at the Alhambra.",
    "san sebastian": "June to September: 20-24C for the beach and the pintxos, with the film "
                     "festival at the end of September. July and August are the busiest, and the "
                     "rest of the year is wet.",
    "barcelona": "May, June and September: 22-27C, the sea warm enough to swim and the terraces "
                 "full. August is hot and packed, and November to February is cool with some "
                 "rain.",
    "madrid": "April, May, June and September: 20-28C and dry, with the terraces out and the "
              "Prado quiet. July and August are 35C+ and the city empties, and winter is cold and "
              "clear.",
    "seville": "March to May and October: 20-28C and the orange trees in flower or in fruit, with "
               "Semana Santa and the April fair the peak. July and August are 40C+, so people "
               "live at night.",
    "athens": "April, May, October and early November: 20-26C and the sites walkable. July and "
              "August are 35C+ and the Acropolis is a scramble by 10am, and the islands are at "
              "their best in June and September.",
    "santorini": "May, June, September and early October: 24-27C, warm sea and no crush. July and "
                 "August are 30C+ with the cruise crowds landing mid-morning, and many hotels "
                 "close from November to March.",
    "crete": "May, June, September and early October: 24-28C and the sea warm, and the Samaria "
             "gorge opens in May. July and August are 30C+ and busy, and winter is mild on the "
             "south coast.",
    "split": "May, June, September and early October: 22-27C, with the ferries to Hvar and Brac "
             "running. July and August are the peak and the old town is packed by day, and many "
             "islands shut from October.",
    "dubrovnik": "May, June, September and early October: 22-27C and the city walls walkable. "
                 "July and August are the peak and the cruise ships fill the old town by 10am, "
                 "and winter is quiet.",
    "zadar": "May, June and September: 22-27C and the sea warm enough to swim, with the Kornati "
             "islands as a day trip. July and August are busy, and winter is quiet.",
    "istanbul": "April, May, September and October: 18-25C and dry, and the Bosphorus ferries at "
                "their best. July and August are hot and humid, and December to February is cold "
                "and wet.",
    "tokyo": "Late March to April for the blossom, and October to November for the autumn colour "
             "and the clearest skies. June is the rainy season, August is hot and humid, and the "
             "New Year week closes many places.",
    "kyoto": "Late March to early April for the blossom, and mid-November for the maples. July "
             "and August are hot and humid, and the New Year week is the busiest of the year.",
    "bangkok": "November to February: dry, warm and clear, which is why it is the season. March "
               "to May is hot and hazy, and June to October is the monsoon with short, heavy "
               "afternoon rain.",
    "hanoi": "October to December: 20-26C, dry and clear. January to March is cool and damp with "
             "drizzle, and May to September is hot and wet, with the heaviest rain in July and "
             "August.",
    "singapore": "Any month works: it is 30C and humid all year, with rain in short bursts. "
                 "February to April is the driest, November to January the wettest, and the haze "
                 "can arrive in September.",
    "dubai": "November to March, when it is 20-30C and you can be outside. From June to "
             "September it is over 40C, so people live in air conditioning and the hotel prices "
             "fall.",
    "marrakech": "March to May and October to November: 20-28C by day, cool at night, no extreme "
                 "heat. July and August are 40C+ in the city, and the desert is cold at night all "
                 "year.",
    "cape town": "November to March: dry, 25-28C, the beaches and the Table Mountain cableway at "
                 "their best. July and August are wet and windy, which is the whale season in "
                 "Hermanus.",
    "havana": "November to April: dry and 24-28C. May to October is hot and wet, and August to "
              "October is hurricane season, though the rain usually comes in short afternoon "
              "storms.",
    "buenos aires": "March to May and September to November: 18-25C and the parks at their best. "
                    "December to February is hot and humid and the city empties in January, and "
                    "July and August are cool and damp.",
    "rio de janeiro": "December to March is hot, 28-32C, and Carnival falls in February or early "
                      "March. May to October is cooler and drier, and the sea is still warm in "
                      "September.",
    "mexico city": "March to May: dry, warm and clear, before the rains. June to October is the "
                   "wet season with short afternoon storms, and December to February is dry with "
                   "cold nights.",
    "sydney": "September to November and March to May: 20-26C, warm without the scorch. December "
              "to February is 30C+ and the beaches are packed, and June to August is mild, with "
              "whale watching.",
    "melbourne": "March to May and September to November: 18-24C, and the city is at its best in "
                 "autumn. December to February is hot and changeable, and winter is cold and "
                 "football.",
    "delhi": "October to March: dry and cooler, 15-25C. April to June is brutally hot at 40C+, "
             "and the monsoon runs July to September with flooding in some years.",
    "mumbai": "November to February: dry, 25-30C and the most comfortable. March to June is hot "
              "and humid, and the monsoon runs June to September with heavy rain.",
    "new york": "May to June and September to October: mild and walkable at 20-26C. July and "
                "August are hot and humid, January and February are cold with snow, and the "
                "Christmas weeks are the most expensive of the year.",
    "boston": "May, June, September and October: 18-26C, and October for the foliage. July and "
              "August are hot and humid, and January and February are cold with snow.",
    "chicago": "May, June and September: 20-27C and the lakefront at its best. July and August "
               "are hot and humid, and January and February are brutal with the wind off the "
               "lake.",
    "san francisco": "September and October: the warmest, clearest months at 18-24C. July and "
                     "August are foggy and cool, and the rain comes November to March.",
    "los angeles": "March to May and September to November: 20-26C and clear. June to August is "
                   "warm but the marine layer can sit all day at the beaches, and winter is mild "
                   "with the odd storm.",
    "toronto": "May to June and September to October: 18-25C. July and August are hot and humid, "
               "and December to March is cold with snow.",
}

REGION_BEST_TIME = {
    "cornwall": "May, June and September: 16-20C, the coast path at its best and the lanes still "
                "quiet. July and August are the warmest weeks and the busiest by a long way, and "
                "October is mild and much emptier, with the Atlantic at its biggest.",
    "devon": "May, June and September: 16-20C, both coasts open and the beaches half empty. Late "
             "July and August are the school-holiday crush on the sand and the roads, and October "
             "is still mild if you do not mind a shower.",
    "lake district": "May, June and September for long clear days at 15-20C; September is the "
                     "quietest dry-ish month and the fells are at their best. July and August "
                     "bring the crowds to Windermere and the passes, and November to February is "
                     "wet, dark and often icy on the tops.",
    "norfolk": "May to September: the Broads and the north Norfolk coast at 18-22C, and the seal "
               "trips running. July and August fill the coastal villages, and October to March is "
               "quiet, cheap and cold, with huge skies and good birdwatching.",
    "yorkshire": "May to September: 16-20C, the Dales and the moors dry and open, and the coast "
                 "best in June and September. The towns are busy at half term and in August, and "
                 "the moors are bleak from November to February.",
}

WHEN_TO_GO = {**CITY_BEST_TIME, **REGION_BEST_TIME}

BEST_TIME = {
    "iceland": "June to August gives midnight sun, open highland roads and puffins; February and "
                "March are best for the northern lights. November is dark, wet and icy, so it is "
                "the one month I would skip.",
    "greece": "May, June, September and early October: warm sea, open tavernas and no crush. August "
              "is 35C and the islands are packed, and many small hotels close from November to "
              "March.",
    "spain": "April to June and September to October, when it is 20-28C and the coast is quiet. "
             "July and August are 35C+ inland and busy on the coast; the north stays green and "
             "cooler in summer.",
    "italy": "April, May, late September and October: warm, not crowded, everything open. July and "
             "August are hot and packed, and August in the cities means half the restaurants shut.",
    "portugal": "May, June and September: warm and dry with fewer people. July and August are hot "
                "and busy on the Algarve, and the north is wet from November to February.",
    "croatia": "June and September: the sea is warm and the coast is not yet rammed. July and "
               "August are the peak, and many islands shut down entirely from October.",
    "turkey": "May, June and September for the coast, and April or October for Istanbul. July and "
              "August are hot and crowded, and the coast is quiet and mild in winter.",
    "japan": "Late March to April for the blossom, or October to November for the autumn colour. "
             "June is the rainy season, August is hot and humid, and the New Year week is the "
             "busiest travel period of the year.",
    "thailand": "November to February: dry, warm and clear. March to May is hot and hazy, and June "
                "to October is the monsoon, when the islands get rough seas and some boats stop.",
    "dubai": "November to March, when it is 20-30C and you can be outside. From June to September "
             "it is over 40C, so people live in air conditioning and the hotel prices fall.",
    "new york": "May to June and September to October: mild and walkable. July and August are hot "
                "and humid, January and February are cold with snow, and the Christmas weeks are "
                "the most expensive of the year.",
    "norway": "June to August for the fjords, the midnight sun and the coastal ferries. The "
              "northern lights need September to March and a clear, dark sky, and much of the "
              "mountain roads close in winter.",
    "scotland": "May to September for the Highlands, the islands and the long evenings. Midges "
                "are worst in July and August, and November to February has very short days.",
    "morocco": "March to May and September to November: warm days, cool nights, no extreme heat. "
               "July and August are 40C+ inland, and the desert is cold at night all year.",
    "mexico": "November to April is the dry season, which is why it is the busy one. May to "
              "October is hot and wet, with rain usually in short afternoon storms.",
    "australia": "September to November and March to May for the south: warm, not scorching. "
                 "December to February is 35C+ in Sydney and Melbourne, and the north is tropical "
                 "wet season then.",
    "india": "October to March for most of the country: dry and cooler. April to June is "
             "brutally hot in the north, and the monsoon runs June to September.",
    "usa": "It depends where: May and September for the northeast, spring and autumn for the "
           "southwest, and June to September for the national parks and mountains. Avoid the "
           "July 4th week and Thanksgiving for flights.",
}

AIRPORT_TRANSFER = {
    "fiumicino": "the Leonardo Express to Termini is 32 minutes and \u20ac14, or a regional train to "
                 "Trastevere and the metro for less. A taxi is a flat \u20ac55 to the centre.",
    "lisbon airport": "the metro (red line) into town is 20 minutes for about \u20ac2 with a Viva "
                      "card; a taxi is 15-20 minutes and \u20ac15-20. Uber works too.",
    "charles de gaulle": "the RER B into the centre is 35 minutes and about \u20ac11.80; a taxi is a "
                         "flat \u20ac56 to the right bank. Orly has the Orlyval plus RER, and a "
                         "tram now too.",
    "barcelona airport": "the Aerobus to Plaza Catalunya is 35 minutes and about \u20ac7.50; the "
                         "train to Sants is cheaper and slower. A taxi is a flat \u20ac35.",
    "amsterdam airport": "the train to Centraal is 15-20 minutes and about \u20ac6; buy the ticket "
                         "from the machine before the gates, not on board.",
    "dublin airport": "the Aircoach or the 747 bus to the centre is about \u20ac7-10 and 30-45 "
                      "minutes; a taxi is \u20ac25-30. There is no train link yet.",
    "edinburgh airport": "the tram or the 100 bus to the centre is about 30 minutes and \u00a36.50; "
                         "a taxi is \u00a325-30. The tram stops at Haymarket and Princes Street.",
    "jfk": "the AirTrain plus the subway is about \u20ac10 and 60-75 minutes; the LIRR from Jamaica "
            "is faster. A yellow cab is a flat fare to Manhattan, plus tolls and tip.",
    "berlin airport": "the FEX or S9 train to Hauptbahnhof is 30 minutes and about \u20ac4.40; a "
                      "taxi is \u20ac40-50.",
    "porto airport": "the metro line E to the centre is 30 minutes for about \u20ac2 with an "
                     "Andante card; a taxi is 20-25 minutes and \u20ac20-25.",
    "dubrovnik airport": "the Atlas shuttle to the old town is about \u20ac8 and 30-40 minutes, "
                         "timed to the flights; a taxi is \u20ac40-50. There is no train.",
    "krakow airport": "the train to the main station is 20 minutes for about 12 zloty, and bus "
                      "252 runs too; a taxi is 25-30 minutes and 70-90 zloty.",
    "budapest airport": "bus 100E to Deak Ferenc ter is 30 minutes for about 900 forint, and no "
                        "metro reaches the airport; a taxi is 25-30 minutes and about 10,000 "
                        "forint.",
    "venice airport": "the ATVO bus to Piazzale Roma is 20 minutes and \u20ac10, and the Alilaguna "
                      "boat to San Marco is 75 minutes and \u20ac15; a water taxi is \u20ac100+.",
    "copenhagen airport": "the metro to Kongens Nytorv is 15 minutes and about 30 kroner, and the "
                          "train also runs to the central station; a taxi is 250-300 kroner.",
    "athens airport": "metro line 3 to Syntagma is 40 minutes and \u20ac9, and the X95 bus is "
                      "\u20ac5.50 and slower; a taxi is 35-45 minutes and \u20ac40.",
    "seville airport": "the EA airport bus to the centre is 35 minutes and \u20ac4; a taxi is 20 "
                       "minutes and about \u20ac25. There is no train link.",
    "florence airport": "the T2 tram to Santa Maria Novella is 20 minutes and \u20ac1.50; a taxi "
                        "is 20 minutes and about \u20ac25.",
    "marrakech airport": "bus 19 to the medina is 30 minutes and 30 dirham; a taxi should be about "
                         "100 dirham, and agree the price before you get in.",
    "naples airport": "the Alibus to the central station and the port is 20-25 minutes and "
                      "\u20ac5; a taxi is about \u20ac25, agreed first.",
    "madrid airport": "the metro line 8 to Nuevos Ministerios is about \u20ac5 and 40 minutes; the "
                      "Cercanias train to Atocha is faster. A taxi is a flat \u20ac33.",
    "prague airport": "bus 119 to the metro at Nadrazi Veleslavin is 15 minutes and 40 koruna, "
                      "then the metro, or the Airport Express bus to the main station in about "
                      "40 minutes; a taxi is 30 minutes and 500-600 koruna, and agree the price "
                      "first.",
    "istanbul airport": "the metro or the Havaist bus to the centre is about \u20ac2-5 and takes "
                        "40-60 minutes; a taxi is much more and the traffic is bad.",
    "lisbon": "the metro (red line) into town is 20 minutes for about \u20ac2 with a Viva card; a "
               "taxi is 15-20 minutes and \u20ac15-20.",
    "rome": "from Fiumicino the Leonardo Express to Termini is 32 minutes and \u20ac14; the regional "
             "train plus metro is cheaper. A taxi is a flat \u20ac55.",
    "paris": "from Charles de Gaulle the RER B is 35 minutes and about \u20ac11.80; from Orly the "
              "Orlyval plus RER, or the tram. A taxi from CDG is a flat \u20ac56 to the right bank.",
    "vienna airport": "the S-Bahn S7 to Wien Mitte is 25 minutes for about \u20ac4.60, and the City "
                      "Airport Train is 16 minutes and \u20ac14.90. A taxi is a flat \u20ac40.",
    "zurich airport": "the train to the main station is 10 to 12 minutes for about 7 francs, and "
                      "it runs every few minutes. A taxi is 30 to 40 francs and slower.",
    "munich airport": "the S-Bahn S1 or S8 to the centre is 40 minutes on a normal city ticket, "
                      "about \u20ac13; a taxi is \u20ac70 or more and no quicker in traffic.",
    "frankfurt airport": "the S-Bahn S8 or S9 to the main station is 15 minutes and about "
                         "\u20ac6.50; a taxi is 25 minutes and \u20ac35-40.",
    "stockholm airport": "the Arlanda Express to the central station is 20 minutes and about "
                         "320 kronor, and the commuter train is 40 minutes and cheaper; the "
                         "express is the most expensive way. A taxi is 45 minutes and 500 "
                         "kronor or more.",
    "oslo airport": "the Flytoget to the central station is 20 minutes for about 240 kroner, and "
                    "the Vy regional train is slower and half the price. A taxi is 45 minutes "
                    "and very expensive.",
    "helsinki airport": "the I or P train to the central station is 30 minutes for about "
                        "\u20ac4.10, and it is the same ticket as the city trams.",
    "tokyo airport": "Haneda is the quick one: the monorail to Hamamatsucho is 20 minutes for "
                     "about 500 yen, and the Keikyu line goes to Shinagawa. From Narita the "
                     "Skyliner to Ueno is 41 minutes and about 2,570 yen.",
    "kyoto": "Kansai airport is 75 minutes away on the Haruka train, which is the easiest way; a "
              "taxi is not worth the price.",
    "brussels airport": "the train to the central station is 20 minutes and about \u20ac11, and "
                        "it runs four times an hour. From Charleroi the bus to Midi takes an "
                        "hour.",
    "bangkok airport": "the Airport Rail Link from Suvarnabhumi to Phaya Thai is 30 minutes for "
                       "45 baht, and the metro joins it there. A taxi with tolls is 40 to 60 "
                       "minutes and 400 to 500 baht.",
    "singapore airport": "the MRT to the city is 30 to 40 minutes for about S$2, changing at "
                         "Tanah Merah. A taxi is 20 to 30 minutes and S$20-30 with the airport "
                         "surcharge.",
    "hanoi airport": "bus 86 to the old quarter is 45 minutes for 35,000 dong, and a Grab or a "
                     "taxi is about 350,000 dong and 40 minutes.",
    "cape town airport": "an Uber or a taxi to the centre is 20 to 30 minutes and about 250 "
                         "rand. There is a train, but not one to take with bags.",
    "mexico city airport": "the metro line 5 is the cheap way and slow with luggage; a taxi from "
                           "the official stand inside the terminal is 30 to 45 minutes and "
                           "about 250 pesos.",
    "havana airport": "a taxi to the old town is 25 to 30 minutes and about 25 dollars or the "
                      "same in euros; the airport bus is not worth the wait.",
    "buenos aires airport": "Ezeiza is 45 minutes by taxi and about 30 dollars, and bus 8 is the "
                            "cheap way but slow. Aeroparque is in the city itself.",
    "rio airport": "Galeao is 30 to 50 minutes by taxi, and the BRT bus to the centre is cheaper "
                   "and takes about an hour. Santos Dumont is in the city.",
    "sydney airport": "the Airport Link train to Central is 13 minutes for about 20 Australian "
                      "dollars. A taxi is 25 to 35 dollars and slower in the morning peak.",
    "toronto airport": "the UP Express to Union station is 25 minutes for about 12 Canadian "
                       "dollars and runs every 15 minutes.",
    "chicago airport": "the CTA Blue Line from O'Hare runs all night, 45 minutes for $5. A taxi "
                       "is 40 to 60 minutes and $50 or more with the tip.",
    "boston airport": "the Silver Line SL1 bus from the terminals takes about 20 minutes for a "
                      "normal subway fare, and the water taxi across the harbour is the fun way.",
    "san francisco airport": "BART to the city is 30 minutes for about $10. A taxi is 25 to 40 "
                             "minutes and $50 or more.",
    "los angeles airport": "the FlyAway bus to Union Station is about 45 minutes and $10; a taxi "
                           "or a rideshare is 30 to 60 minutes and $50 or more, depending on the "
                           "traffic.",
}

AIRPORT_NAME = {
    "dubrovnik": "Dubrovnik (DBV) is 20km south-east, and the Atlas shuttle to the old town is "
                 "about \u20ac8 and 30-40 minutes, timed to the flights; a taxi is \u20ac40-50.",
    "krakow": "Krakow John Paul II (KRK) is 11km west, and the train to the main station is 20 "
              "minutes for about 12 zloty; a taxi is 70-90 zloty.",
    "budapest": "Budapest Ferenc Liszt (BUD) is 16km south-east, and bus 100E to Deak Ferenc ter "
                "is 30 minutes for about 900 forint; a taxi is about 10,000 forint.",
    "venice": "Venice has two: Marco Polo (VCE) for most flights, 13km north, and Treviso (TSF) "
              "for budget ones, 40km away. From Marco Polo the ATVO bus to Piazzale Roma is 20 "
              "minutes and \u20ac10.",
    "athens": "Athens (ATH) is 20km east, and metro line 3 to Syntagma is 40 minutes and \u20ac9; "
              "a taxi is \u20ac40.",
    "copenhagen": "Copenhagen (CPH) is 8km south-east, and the metro to Kongens Nytorv is 15 "
                  "minutes for about 30 kroner.",
    "florence": "Florence (FLR) is 5km north-west and small, and the T2 tram to Santa Maria "
                "Novella is 20 minutes for \u20ac1.50; a taxi is about \u20ac25.",
    "seville": "Seville (SVQ) is 10km north-east, and the EA bus to the centre is 35 minutes for "
               "\u20ac4; there is no train link.",
    "london": "London City (LCY) is the closest to the centre: about 25 minutes to Bank on the "
              "DLR. London has five, though, and which one suits depends where you are going: "
              "Heathrow (LHR) for most long-haul, Gatwick (LGW) for charters and short-haul, City "
              "itself if you are staying in the east. From Heathrow the Piccadilly line is an "
              "hour and about \u00a35-6.",
    "rome": "Rome has two: Fiumicino (FCO), the main one, 30km south-west, and Ciampino (CIA) "
            "for budget flights, 15km east. From Fiumicino the Leonardo Express is 32 minutes to "
            "Termini for \u20ac14.",
    "lisbon": "Lisbon Humberto Delgado (LIS) is 7km north of the centre, and the red metro line "
              "takes 20 minutes for about \u20ac2 with a Viva card.",
    "porto": "Porto Francisco Sa Carneiro (OPO) is 11km north-west, and the metro line E to the "
             "centre takes about 30 minutes for \u20ac2; a taxi is \u20ac25-30.",
    "paris": "Paris has two: Charles de Gaulle (CDG) for most long-haul, 25km north-east, and "
             "Orly (ORY) to the south for domestic and short-haul. The RER B from CDG is 35 "
             "minutes and about \u20ac11.80.",
    "barcelona": "Barcelona El Prat (BCN) is 12km south-west, and the Aerobus to Plaza Catalunya "
                 "is 35 minutes and about \u20ac7.50.",
    "madrid": "Madrid-Barajas (MAD) is 12km north-east, and the metro line 8 into the centre is "
              "about \u20ac5 and 40 minutes; a taxi is a flat \u20ac33.",
    "amsterdam": "Amsterdam Schiphol (AMS) is 15km south-west, and the train to Centraal is "
                 "15-20 minutes for about \u20ac6.",
    "dublin": "Dublin (DUB) is 10km north, and the Aircoach or the 747 bus to the centre is about "
              "\u20ac7-10 and 30-45 minutes; there is no train link yet.",
    "edinburgh": "Edinburgh (EDI) is 13km west, and the tram or the 100 bus to the centre takes "
                 "about 30 minutes for \u00a36.50.",
    "new york": "New York has three: JFK for most international flights, Newark (EWR) for many "
                "too, and LaGuardia (LGA) for domestic. From JFK the AirTrain plus the subway is "
                "about $10 and 60-75 minutes.",
    "berlin": "Berlin Brandenburg (BER) is 25km south-east, and the FEX or S9 train to "
              "Hauptbahnhof is 30 minutes for about \u20ac4.40.",
    "prague": "Prague Vaclav Havel (PRG) is 15km west, and bus 119 to the metro, or the Airport "
              "Express to the main station, is about \u20ac1.50-2.50.",
    "istanbul": "Istanbul has two: IST on the European side, the main one, and SAW on the Asian "
                "side for budget flights. From IST the metro or the Havaist bus is 40-60 minutes.",
    "milan": "For Milan it is Malpensa (MXP) for long-haul, 50km north-west, or Linate (LIN) for "
             "short-haul, 7km east. The Malpensa Express to the centre is 50 minutes.",
    "dubai": "Dubai International (DXB) is 5km from the centre, and the metro red line reaches "
             "most of the city for a few dirhams.",
    "vienna": "Vienna (VIE) is 18km south-east, and the S-Bahn S7 to Wien Mitte is 25 minutes "
               "for about \u20ac4.60; the City Airport Train is 16 minutes and \u20ac14.90. A taxi is "
               "a flat \u20ac40.",
    "stockholm": "Stockholm Arlanda (ARN) is 40km north, and the Arlanda Express is 20 minutes "
                 "and about 320 kronor; the commuter train takes 40 minutes and costs less. "
                 "Bromma (BMA) is close to the city but only for domestic flights.",
    "tokyo": "Tokyo has two: Haneda (HND), 20km south and the convenient one, and Narita (NRT), "
             "60km east, which most long-haul flights use. From Haneda the monorail to "
             "Hamamatsucho is 20 minutes for about 500 yen.",
    "brussels": "Brussels (BRU) is 12km north-east, and the train to the central station is 20 "
                "minutes for about \u20ac11. Charleroi (CRL) is the budget airport, 60km south, and "
                "the bus into town takes an hour.",
    "munich": "Munich (MUC) is 38km north-east, and the S-Bahn S1 or S8 to the centre is 40 "
              "minutes for about \u20ac13; a taxi is \u20ac70 or more.",
    "zurich": "Zurich (ZRH) is 12km north, and the train to the main station is 10 to 12 minutes "
              "for about 7 francs, which is the easiest airport transfer in Europe.",
    "oslo": "Oslo Gardermoen (OSL) is 47km north, and the Flytoget is 20 minutes for about 240 "
            "kroner; the Vy regional train is slower and about half the price.",
    "helsinki": "Helsinki-Vantaa (HEL) is 20km north, and the I or P train to the central "
                "station is 30 minutes for about \u20ac4.10.",
    "tallinn": "Tallinn (TLL) is 4km from the centre, so it is a tram or a short taxi rather than "
               "a transfer: tram 4 gets you in for the price of a city ticket.",
    "reykjavik": "Keflavik (KEF) is the airport people mean, 50km south-west, and the Flybus to "
                 "the city is 45 minutes for about 3,500 kroner. Reykjavik (RKV) is a small city "
                 "airport for domestic flights only.",
    "boston": "Boston Logan (BOS) is 6km east, and the Silver Line SL1 bus from the terminals "
              "takes about 20 minutes for a normal subway fare; the water taxi across the harbour "
              "is the fun way in.",
    "san francisco": "San Francisco (SFO) is 21km south, and BART to the city is 30 minutes for "
                     "about $10. Oakland (OAK) is across the bay and often cheaper.",
    "los angeles": "Los Angeles (LAX) is 30km south-west and the one people mean; the FlyAway "
                   "bus to Union Station is about 45 minutes. Hollywood Burbank (BUR) is closer "
                   "for domestic flights.",
    "chicago": "Chicago O'Hare (ORD) is 27km north-west, and the CTA Blue Line runs all night, "
               "45 minutes for $5. Midway (MDW) is nearer the city and on the Orange Line.",
    "toronto": "Toronto Pearson (YYZ) is 27km north-west, and the UP Express to Union station is "
               "25 minutes for about 12 Canadian dollars.",
    "sydney": "Sydney (SYD) is 8km south, and the Airport Link train to Central is 13 minutes "
              "for about 20 Australian dollars; a taxi is 25 to 35.",
    "singapore": "Singapore Changi (SIN) is 20km east, and the MRT to the city is 30 to 40 "
                 "minutes for about S$2. Allow an hour there before your flight: the Jewel "
                 "waterfall is inside the airport.",
    "bangkok": "Bangkok has two: Suvarnabhumi (BKK), the main one 30km east, and Don Mueang "
               "(DMK), 25km north, for budget flights. From Suvarnabhumi the Airport Rail Link "
               "is 30 minutes for 45 baht.",
    "hanoi": "Hanoi (HAN) is 35km north, and bus 86 to the old quarter is 45 minutes for 35,000 "
             "dong; a taxi or a Grab is about 350,000 dong and 40 minutes.",
    "cape town": "Cape Town (CPT) is 20km east, and a taxi or an Uber to the centre is 20 to 30 "
                 "minutes and about 250 rand. There is a train, but not one to take with bags.",
    "mexico city": "Mexico City (MEX) is 13km east, and the metro line 5 is cheap and slow; a taxi "
                   "from the official stand inside the terminal is 30 to 45 minutes and about "
                   "250 pesos.",
    "havana": "Havana (HAV) is 15km south of the city, and a taxi to the old town is 25 to 30 "
              "minutes and about 25 dollars or the same in euros; the airport bus is not worth "
              "the wait.",
    "buenos aires": "Buenos Aires has two: Ezeiza (EZE), 30km south, for long-haul, and "
                    "Aeroparque (AEP) in the city for domestic flights. From Ezeiza a taxi is "
                    "45 minutes and about 30 dollars; bus 8 is the cheap way.",
    "rio de janeiro": "Rio has two: Galeao (GIG), 20km north, for international flights, and "
                      "Santos Dumont (SDU) in the city for the Sao Paulo shuttle. From Galeao a "
                      "taxi is 30 to 50 minutes.",
    "naples": "Naples (NAP) is 6km north-east, and the Alibus to the central station and the "
              "port is 20 minutes for \u20ac5; a taxi is about \u20ac25, and agree the price first.",
    "valencia": "Valencia (VLC) is 9km west, and metro line 3 or 5 to the centre is 20 minutes "
                "for about \u20ac5.",
    "granada": "Granada (GRX) is 17km west and small, and the airport bus to the centre is 40 "
               "minutes for \u20ac3. Most people fly to Malaga instead and take the bus, which is "
               "two hours.",
    "santorini": "Santorini (JTR) is 6km from Fira, and the bus meets the flights; a taxi is 20 "
                 "to 30 euros. It is a small airport with a short runway, so summer flights are "
                 "often delayed.",
    "san sebastian": "San Sebastian (EAS) is 20km east at Hondarribia and has very few flights, "
                     "so most people fly to Bilbao (75 minutes by bus) or Biarritz (40 "
                     "minutes).",
    "ljubljana": "Ljubljana (LJU) is 25km north, and the airport bus to the centre is 30 "
                 "minutes for about \u20ac4; a taxi is \u20ac25 to \u20ac30.",
    "kyoto": "Kyoto has no airport of its own: fly into Osaka Kansai (KIX), which is 75 minutes "
             "away on the Haruka train, or into Tokyo and take the shinkansen.",
    "bath": "Bath has no airport: Bristol (BRS) is 30km west, and the Flyer bus runs to Bath in "
            "55 minutes. By train, come into Bath Spa from Bristol Temple Meads.",
}

DAY_TRIPS = {
    "london": "Bath (80 minutes by train), Oxford and Cambridge (about an hour), and Brighton "
              "(an hour) for the sea. Book the train a week ahead and you halve the fare.",
    "edinburgh": "Glasgow (50 minutes by train from Waverley), Stirling for the castle (50 "
                 "minutes), and North Berwick (35 minutes) for the beach and the boat out to the "
                 "Bass Rock. St Andrews is about 90 minutes by train and bus, and worth the day "
                 "for the ruins and the beach rather than the golf.",
    "paris": "Versailles (40 minutes on the RER C), Chartres for the cathedral, and Giverny for "
              "Monet's garden from April to October. Go early: the first trains are the quietest.",
    "rome": "Ostia Antica for the Roman ruins (30 minutes on the metro and train), Tivoli for the "
             "villa gardens, and Orvieto for the cathedral. Pompeii is two hours each way, so it "
             "is a full day.",
    "lisbon": "Sintra for the palaces (40 minutes by train), Cascais for the beach (40 minutes "
               "on the same line), and Obidos for the walled town (an hour by bus from Lisbon's "
               "Campo Grande, and no train goes there). Buy the train ticket at the machine and "
               "go before 9am.",
    "barcelona": "Montserrat (an hour by train and cable car), Girona (40 minutes) and Sitges "
                  "for the beach (40 minutes). Girona plus Figures makes a good full day.",
    "amsterdam": "Haarlem (15 minutes), Utrecht (25 minutes) and the Zaanse Schans windmills "
                  "(40 minutes). Keukenhof is worth it only in tulip season, mid-March to mid-May.",
    "madrid": "Toledo (30 minutes by train), Segovia (30 minutes) and El Escorial. Toledo and "
               "Segovia both deserve a full day rather than an afternoon.",
    "munich": "Neuschwanstein (two hours by train and bus), Salzburg (90 minutes) and the "
               "Bavarian lakes. Buy a Bayern ticket: it covers the regional trains for a group.",
    "edinburgh": "Glasgow (50 minutes by train), Stirling for the castle, and North Berwick for "
                 "the beach and the seabird centre. The Highlands need a car or a full day tour.",
    "dublin": "Howth for the cliff walk (30 minutes on the DART), Malahide castle, and Glendalough "
               "in the Wicklow mountains, which needs a car or a bus tour.",
    "berlin": "Potsdam for Sanssouci (30 minutes by train) and Sachsenhausen, which is a heavy "
               "half-day and worth it. Both are covered by the Berlin ABC travel card.",
    "tokyo": "Nikko for the shrines and Kamakura for the Buddha (both about two hours), or Hakone "
              "for a view of Fuji if the sky is clear. Go on a weekday: the weekend trains are "
              "packed.",
    "leeds": "York (25 minutes by train), the Yorkshire Dales (an hour by car) and Harrogate for "
              "a spa afternoon. Manchester is 50 minutes by train if you want a city.",
    "florence": "Pisa (an hour by train) for the tower, Siena (90 minutes) for the square, and "
                "Lucca for the walls and the bikes. Fiesole is 30 minutes by bus for the view "
                "back over Florence.",
    "venice": "Verona (an hour by train) for the arena, Padua for the Scrovegni chapel, and the "
              "islands in the lagoon: Murano for glass and Burano for the coloured houses, on a "
              "vaporetto day pass.",
    "naples": "Pompeii and Herculaneum (40 minutes on the Circumvesuviana), the Amalfi coast by "
              "ferry or bus, and Ischia for a slower island day. Vesuvius is a bus and a walk "
              "from Ercolano.",
    "seville": "Cordoba for the mosque-cathedral (45 minutes by train), Ronda for the gorge and "
               "the bridge, and Jerez for the sherry bodegas. Granada is three hours by bus, so "
               "it wants a night.",
    "porto": "The Douro valley by train to Pinhao for the vineyards, Braga and Guimaraes for the "
             "churches and the old town, and Aveiro for the canals. The Douro line is the "
             "scenic one, so sit on the right.",
    "athens": "Cape Sounion for the temple at sunset, Delphi for the ruins (two and a half hours "
              "by bus), and Aegina or Hydra by ferry for an island day. The fast ferries are "
              "worth the extra.",
    "istanbul": "The Princes' Islands by ferry (an hour and a half) where there are no cars, "
                "Bursa for the Ottoman tombs, and the Bosphorus village of Anadolu Kavagi at "
                "the mouth of the Black Sea.",
    "prague": "Kutna Hora for the bone church and the silver mines (an hour by train), Karlstejn "
              "for the castle, and Cesky Krumlov, which is three hours each way so it wants a "
              "night.",
    "vienna": "Bratislava (an hour by train), the Wachau valley by boat for the vineyards and "
              "Durnstein, and Baden for the spa. The Einfach-Raus ticket covers a group on the "
              "regional trains.",
    "brussels": "Bruges (an hour by train) for the canals, Ghent (35 minutes) for the old port, "
                "and Leuven for the university town. Book Bruges ahead in summer, it fills up.",
    "copenhagen": "Roskilde for the cathedral and the Viking ships (25 minutes), Malmo across "
                  "the bridge (35 minutes) for a cheaper lunch, and the Louisiana museum up the "
                  "coast, which is the best half-day of the lot.",
    "stockholm": "The archipelago by ferry from Stromkajen, Uppsala for the cathedral and the "
                 "Vikings (40 minutes by train), and Drottningholm by boat for the palace "
                 "theatre.",
    "split": "Hvar by catamaran (an hour) for the old town and the lavender, Trogir (30 minutes "
             "by bus) for the walled centre, and Krka for the waterfalls, which needs a car or "
             "a tour.",
    "dubrovnik": "Mostar in Bosnia (two and a half hours by bus) for the bridge, Montenegro for "
                 "Kotor and the bay, and the Elaphiti islands by boat. Take your passport for "
                 "Mostar and Montenegro.",
    "ljubljana": "Lake Bled (an hour by bus) for the island church, Postojna for the caves and "
                 "the castle, and Skocjan for the bigger cave, which is the one to pick if you "
                 "only do one.",
    "bath": "Stonehenge (an hour by bus) with a booked slot, Lacock for the village and the "
            "abbey, and Bradford-on-Avon for the canal and the tithe barn, 15 minutes by train.",
    "marrakech": "The Atlas mountains and Ourika valley (an hour by car), Essaouira for the "
                 "seafront and the fish (two and a half hours by bus), and Ait Benhaddou, which "
                 "is a long day or a night on the way to the desert.",
    "bangkok": "Ayutthaya for the ruined temples (an hour and a half by train), Kanchanaburi for "
               "the bridge over the River Kwai, and the floating market at Damnoen Saduak, "
               "which needs a very early start.",
    "hanoi": "Halong Bay for the boats (two and a half hours by bus, and a night on the water "
             "is better than a day), Ninh Binh for the river rowing boats, and Sapa by night "
             "train for the rice terraces.",
    "bristol": "Bath (15 minutes by train), Wells for the cathedral, and the Mendips or the Gower "
                "if you have a car. Cardiff is 50 minutes by train.",
    "manchester": "the Peak District (40 minutes by train to Edale), Liverpool (50 minutes) and "
                   "Chester for the walls and the rows. York is 90 minutes.",
    "glasgow": "Loch Lomond (40 minutes by train), Stirling for the castle, and Edinburgh in an "
                "hour. The islands need a ferry and a full day.",
    "liverpool": "Chester (40 minutes by train), the Wirral coast, and Manchester in under an "
                  "hour. North Wales is a longer day by train.",
    "birmingham": "Stratford-upon-Avon (40 minutes by train), Warwick castle and the Cotswolds by "
                  "car. The Black Country museum is a good wet-day half-day.",
    "new york": "Beacon for Dia:Beacon (80 minutes on Metro-North), Philadelphia (90 minutes on "
                "Amtrak) and the Hamptons by the LIRR. The Jersey shore is a longer day.",
    "chicago": "Milwaukee (90 minutes on Amtrak), the Indiana Dunes for the beach (an hour by "
               "train and bus) and the Baha'i temple at Wilmette, which is free and half a day "
               "on the Purple line.",
    "san francisco": "Muir Woods and Sausalito (ferry, then a shuttle you book ahead), Napa by "
                     "car, and Santa Cruz over the hill. Yosemite is four hours, so it wants a "
                     "night.",
    "los angeles": "Santa Monica and Malibu down the coast, Disneyland in Anaheim (an hour by "
                   "car) and Catalina island by ferry from Long Beach. Almost all of it needs a "
                   "car.",
    "boston": "Salem for the witch museum (30 minutes by train), Concord and Lexington for the "
              "revolution, and Providence (an hour on Amtrak). Cape Cod is 90 minutes by car.",
    "toronto": "Niagara Falls (two hours by train or bus, and the falls are free), "
               "Niagara-on-the-Lake for the wineries on the same trip, and Stratford for the "
               "Shakespeare festival.",
    "sydney": "The Blue Mountains (two hours by train), the Hunter Valley for wine (three hours, "
              "better on a tour) and Manly or Watsons Bay by ferry for a beach day close in.",
    "singapore": "Johor Bahru across the causeway (the bus queue is long at weekends), Batam by "
                 "ferry, and Malacca, which is three and a half hours each way. The Botanic "
                 "Gardens and the southern ridges are free and in the city.",
    "dubai": "Abu Dhabi for the grand mosque and the Louvre (90 minutes by car or bus), the "
             "desert for a dune drive, and Hatta for the mountains and the kayaks. The Abu Dhabi "
             "bus leaves from Al Ghubaiba.",
    "cape town": "The Cape of Good Hope and the Boulders Beach penguins, which is a full day by "
                 "car, Stellenbosch and Franschhoek for wine (an hour), and Hermanus for whales "
                 "from June to November.",
    "mexico city": "Teotihuacan for the pyramids (an hour by bus from the north terminal), "
                   "Puebla and Cholula (two hours by bus), and Taxco for silver, which is a long "
                   "day.",
    "havana": "Vinales for the tobacco valley (three hours by bus, better with a night), the "
              "beach at Santa Maria del Mar (30 minutes by taxi), and Matanzas for the river and "
              "the poets.",
    "buenos aires": "Tigre for the delta boats (an hour by train), Colonia in Uruguay by ferry "
                    "(an hour, and take your passport), and San Antonio de Areco for the gaucho "
                    "town.",
    "rio de janeiro": "Petropolis for the imperial palace (90 minutes by bus), Niteroi for the "
                      "museum and the beaches across the bay, and Buzios, which is three hours "
                      "and wants a night.",
    "budapest": "Szentendre for the artist town and the Danube bend (40 minutes on the H5 "
                "train), Esztergom for the basilica, and Lake Balaton, which is two hours and "
                "wants a night.",
    "krakow": "Auschwitz-Birkenau (90 minutes by bus, and book a timed entry), the Wieliczka "
              "salt mine (30 minutes by train) and Zakopane for the mountains (two hours). "
              "Auschwitz is a heavy half-day, not a sight.",
    "milan": "Lake Como for Bellagio (an hour by train to Como, then a boat), Bergamo for the "
             "old town (50 minutes) and Turin (an hour on the fast train). The Last Supper needs "
             "booking weeks ahead.",
    "zurich": "Lucerne (45 minutes by train), the Rhine Falls (an hour) and Interlaken for the "
              "mountains (two hours). A travel pass covers the trains and the boats.",
    "oslo": "The fjord by boat from the city hall pier, Drobak for the fortress and the old "
            "town (an hour by bus), and Bergen by train, which is the best rail journey in the "
            "country and wants a night.",
    "helsinki": "Suomenlinna by ferry (15 minutes on the same ticket as the trams), Porvoo for "
                "the wooden old town (an hour by bus) and Tallinn by ferry (two hours, and take "
                "your passport).",
    "tallinn": "Lahemaa national park for the manors and the coast (an hour by bus), Tartu (two "
               "and a half hours) and Helsinki by ferry in two hours.",
    "reykjavik": "The Golden Circle - Thingvellir, Geysir and Gullfoss - is the full day out and "
                 "needs a car or a tour, the Blue Lagoon is 45 minutes by bus and booked ahead, "
                 "and Snaefellsnes is a very long day.",
    "santorini": "Oia for the sunset and Akrotiri for the Minoan town under the ash are the day, "
                 "and both are 20 to 30 minutes by bus from Fira; boats to Thirasia and the "
                 "volcano leave from the old port.",
    "valencia": "The Albufera for the rice fields and the lagoon (30 minutes by bus), Sagunto "
                "for the Roman theatre, and Requena for the wine. The City of Arts is in the "
                "city, not a day out.",
    "granada": "The Alhambra is the day, not a detour: book a timed ticket weeks ahead. The "
               "Alpujarras villages are an hour and a half by bus, and Cordoba is two and a "
               "half hours by train, so it wants a night.",
    "san sebastian": "Bilbao for the Guggenheim (an hour and a quarter by bus), Saint-Jean-de-Luz "
                     "across the French border (40 minutes) and Getaria for the txakoli wine. "
                     "Hondarribia is 25 minutes by bus.",
    "kyoto": "Nara for the deer and the great Buddha (45 minutes by train), Osaka (30 minutes) "
             "and Hikone for the castle on Lake Biwa. Fushimi Inari and Arashiyama are in Kyoto, "
             "so go at dawn instead.",
}

DAY_TRIP_PLACES = {
    "abu dhabi": "dubai", "ait benhaddou": "marrakech", "akrotiri": "santorini",
    "auschwitz-birkenau": "krakow", "aveiro": "porto", "ayutthaya": "bangkok",
    "baden": "vienna", "beacon": "new york", "bergamo": "milan",
    "bilbao": "san sebastian", "bradford-on-avon": "bath", "braga": "porto",
    "bratislava": "vienna", "brighton": "london", "bruges": "brussels",
    "burano": "venice", "bursa": "istanbul", "buzios": "rio de janeiro",
    "cambridge": "london", "cape sounion": "athens", "cascais": "lisbon",
    "cesky krumlov": "prague", "chartres": "paris", "chester": "manchester",
    "cholula": "mexico city", "concord": "boston", "cordoba": "seville",
    "delphi": "athens", "drobak": "oslo", "durnstein": "vienna",
    "el escorial": "madrid", "essaouira": "marrakech", "esztergom": "budapest",
    "franschhoek": "cape town", "getaria": "san sebastian", "geysir": "reykjavik",
    "ghent": "brussels", "girona": "barcelona", "giverny": "paris",
    "glasgow": "edinburgh", "guimaraes": "porto", "haarlem": "amsterdam",
    "halong bay": "hanoi", "harrogate": "leeds", "hatta": "dubai",
    "herculaneum": "naples", "hermanus": "cape town", "hikone": "kyoto",
    "howth": "dublin", "interlaken": "zurich", "ischia": "naples",
    "jerez": "seville", "kamakura": "tokyo", "kanchanaburi": "bangkok",
    "karlstejn": "prague", "krka": "split", "kutna hora": "prague",
    "lacock": "bath", "lake balaton": "budapest", "lake bled": "ljubljana",
    "lake como": "milan", "leuven": "brussels", "lexington": "boston",
    "liverpool": "manchester", "loch lomond": "glasgow", "lucca": "florence",
    "lucerne": "zurich", "malacca": "singapore", "matanzas": "havana",
    "milwaukee": "chicago", "montenegro": "dubrovnik", "montserrat": "barcelona",
    "muir woods": "san francisco", "nara": "kyoto", "neuschwanstein": "munich",
    "niagara falls": "toronto", "niagara-on-the-lake": "toronto", "nikko": "tokyo",
    "ninh binh": "hanoi", "niteroi": "rio de janeiro", "north berwick": "edinburgh",
    "obidos": "lisbon", "oia": "santorini", "orvieto": "rome",
    "osaka": "kyoto", "ostia antica": "rome", "oxford": "london",
    "padua": "venice", "petropolis": "rio de janeiro", "philadelphia": "new york",
    "pisa": "florence", "pompeii": "naples", "porvoo": "helsinki",
    "postojna": "ljubljana", "potsdam": "berlin", "providence": "boston",
    "puebla": "mexico city", "requena": "valencia", "ronda": "seville",
    "roskilde": "copenhagen", "sachsenhausen": "berlin", "sagunto": "valencia",
    "salem": "boston", "salzburg": "munich", "santa monica": "los angeles",
    "sausalito": "san francisco", "segovia": "madrid", "siena": "florence",
    "sintra": "lisbon", "sitges": "barcelona", "skocjan": "ljubljana",
    "stellenbosch": "cape town", "stirling": "edinburgh", "stonehenge": "bath",
    "stratford": "toronto", "stratford-upon-avon": "birmingham", "szentendre": "budapest",
    "tartu": "tallinn", "taxco": "mexico city", "teotihuacan": "mexico city",
    "the albufera": "valencia", "the blue mountains": "sydney", "tigre": "buenos aires",
    "tivoli": "rome", "toledo": "madrid", "trogir": "split",
    "turin": "milan", "uppsala": "stockholm", "utrecht": "amsterdam",
    "verona": "venice", "versailles": "paris", "vinales": "havana",
    "wells": "bristol", "york": "leeds", "zakopane": "krakow",
}

SITE_NOTES = {
    "pompeii": "Give Pompeii most of a day: it is 66 hectares and there is no shade, so go at "
               "opening time, take water and wear shoes with grip. Book a timed ticket and the "
               "train from Naples on the Circumvesuviana; the audioguide is worth it and the "
               "walk to the amphitheatre is the quiet half.",
    "herculaneum": "Herculaneum takes two or three hours rather than a day, and the woodwork, "
                   "frescoes and upper floors survived in a way Pompeii's did not, so it is the "
                   "better visit if you have one afternoon. It is the same train line as Pompeii, "
                   "one stop closer to Naples, and the site is small enough to see in one go.",
    "vesuvius": "Vesuvius is a bus up from Ercolano and a steep 20-minute walk from the car park, "
                "with the crater rim roped off. Go on a clear morning, take a jacket because it is "
                "cold and windy at the top, and check the bus times for the way back: the last "
                "one leaves early.",
    "alhambra": "The Alhambra is a half day and the Nasrid palaces need a timed slot booked weeks "
                "ahead, in the morning if you can. Take your passport or ID card: it is checked "
                "against the ticket, and people are turned away without it.",
    "colosseum": "The Colosseum together with the Forum and Palatine is one ticket and most of a "
                 "day, so start early and take water. Book the timed entry and the underground or "
                 "arena add-on if you want them, because they sell out first.",
    "stonehenge": "Stonehenge is two hours at most, and the stones are seen from a path rather "
                  "than walked among. Book a timed slot including the shuttle from the visitor "
                  "centre, and pair it with Avebury or Salisbury if you are driving that far.",
    "eiffel tower": "The Eiffel Tower wants a booked time slot and two to three hours with the "
                    "queues and the lifts, or 45 minutes if you walk up to the second floor. The "
                    "stairs are cheaper and shorter, and the last lift up is around 11pm.",
    "vatican museums": "The Vatican Museums and the Sistine Chapel are three hours at a fast "
                       "walk and half a day at a normal one, so book the first entry of the day. "
                       "Cover your shoulders and knees, and note the chapel is silent with no "
                       "photographs.",
    "sagrada familia": "The Sagrada Familia needs a timed ticket bought online, and an hour and a "
                       "half inside. Add the tower lift if you want it - it is a separate ticket - "
                       "and go in the morning when the east windows are lit.",
    "auschwitz": "Auschwitz-Birkenau is a heavy half day, five or six hours with the bus, and the "
                 "timed entry must be booked ahead. Go with a guide, take tissues, and plan "
                 "something gentle for afterwards.",
}

SITE_ALIASES = {
    "vatican": "vatican museums",
    "the vatican": "vatican museums",
    "sistine chapel": "vatican museums",
}

ROUTE_BETWEEN = {
    ("naples", "sorrento"): "Naples to Sorrento: the Circumvesuviana train from Napoli Garibaldi "
                            "takes about an hour and costs a few euros, and it is crowded with "
                            "luggage at commuter times. The fast ferry from Molo Beverello is "
                            "35 to 45 minutes and pleasanter, but it runs only in season.",
    ("naples", "amalfi"): "Naples to the Amalfi coast: the season ferry from Molo Beverello to "
                          "Amalfi or Positano is the pretty way and takes 75 minutes; the SITA "
                          "bus from Sorrento or Salerno is cheaper and slower, and the coast road "
                          "is the part that jams in summer. A car is a liability in August.",
    ("sorrento", "amalfi"): "Sorrento to Amalfi: the SITA bus along the coast road is about 90 "
                            "minutes and the ferry is 25, but the ferry runs from spring to "
                            "October only. Sit on the left of the bus going east for the view, "
                            "and buy the ticket before you queue.",
    ("rome", "pompeii"): "Rome to Pompeii: the fast train to Naples takes 70 minutes, then the "
                         "Circumvesuviana to Pompeii Scavi, so about two and a half hours door "
                         "to door and a long day. Herculaneum is the same trip and half the "
                         "walking.",
    ("naples", "pompeii"): "Naples to Pompeii: the Circumvesuviana from Napoli Garibaldi to "
                           "Pompeii Scavi takes 35 to 40 minutes and drops you at the site gate. "
                           "Get off at Pompeii Scavi, not Pompei town, and keep your bag in front "
                           "of you on the train.",
    ("florence", "pisa"): "Florence to Pisa: the regional train from Santa Maria Novella takes "
                          "about an hour and the tower is a 20-minute walk from Pisa Centrale. "
                          "Book the tower climb separately and go early, because the slots are "
                          "timed and the station is far from the airport side.",
    ("london", "paris"): "London to Paris: the Eurostar from St Pancras is two hours twenty to "
                         "the Gare du Nord, city centre to city centre, and the cheapest fares go "
                         "on sale months ahead. Check in 75 to 90 minutes before, and the coach "
                         "is cheaper but a whole day.",
}

GET_TO = {
    "amalfi coast": "Getting to the Amalfi coast: fly to Naples, then the ferry from Molo "
                    "Beverello to Amalfi or Positano in season, or the Circumvesuviana train to "
                    "Sorrento and the SITA bus along the coast. A private transfer is the only "
                    "sensible option with heavy luggage.",
    "cinque terre": "Getting to the Cinque Terre: trains from Pisa or Genoa run to La Spezia, "
                    "then the local line stops at each village. Parking is almost impossible in "
                    "the villages, so leave the car at La Spezia or Levanto.",
    "machu picchu": "Getting to Machu Picchu: fly or bus to Cusco, then the train from Poroy or "
                    "Ollantaytambo to Aguas Calientes, then the bus up. The Inca Trail needs a "
                    "permit booked months ahead with a licensed operator, and entry tickets are "
                    "timed.",
    "great barrier reef": "Getting to the reef: fly to Cairns or Port Douglas and take a day boat "
                          "from the marina, or go out from Airlie Beach in the Whitsundays. Book "
                          "two days ahead, take the seasickness tablets before you board.",
    "isle of skye": "Getting to Skye: drive over the bridge from Kyle of Lochalsh, or take the "
                    "train to Kyle and the bus, or the ferry from Mallaig to Armadale. Book "
                    "accommodation months ahead for summer and expect single-track roads.",
}

CITY_TRANSIT = {
    "london": "Tap a contactless card or phone on the bus and the Tube and it charges the cheapest "
              "fare of the day, with a daily cap, so a paper travelcard rarely beats it. Buses are "
              "a flat £1.75 and take no cash.",
    "paris": "Get a Navigo Easy card and load ten tickets: a single is €2.15 and ten is cheaper, "
              "and it covers the Metro inside the city. Keep the ticket until you are out of the "
              "gate, because inspectors fine on the spot.",
    "rome": "A ticket is €1.50 and lasts 100 minutes on the metro and the buses, validated in the "
            "machine on board. There are only two metro lines, so walk the centre and take a bus "
            "for the rest.",
    "milan": "A €2.20 ticket covers 90 minutes of metro, trams and buses, and you can tap a bank "
             "card at the metro gate. The centre is small enough to walk, the metro is for the "
             "outer bits.",
    "florence": "Walk: the historic centre is 20 minutes across and a car is a liability. A bus "
                "ticket is €1.50 for 90 minutes, from a tabacchi or the app rather than the driver.",
    "venice": "The vaporetto is the road here: a single is €9.50 and a 24-hour pass about €25, so "
              "the pass pays off after two rides. Walk between the Rialto and San Marco and take "
              "the boat for the islands.",
    "naples": "A ticket is €1.10 and lasts 90 minutes on the metro, the buses and the funicular, "
              "bought at a tabacchi. Metro line 1 is worth riding for the art in the stations.",
    "barcelona": "A T-casual card is ten rides for about €12.50 but it is one person only: for "
                 "two or more of you the T-familiar is eight rides over 30 days and can be passed "
                 "back over the gate. The metro reaches nearly everything and runs late.",
    "madrid": "A ten-ride Metrobus card is the cheapest way to ride the metro and the buses, about "
              "€1.20 a trip, and the centre is walkable anyway. The metro is fast and air "
              "conditioned.",
    "seville": "Walk: the centre is flat and 20 minutes across. Beyond that a bus ticket is €1.40 "
               "and the tram crosses the old town, and bikes are easy to hire on the cycle lanes.",
    "valencia": "A metro ticket is €1.50 and gets you from the old town to the City of Arts; the "
                "centre itself is walkable and the old river bed is now a park you can walk "
                "through.",
    "granada": "Walk the centre and take a bus up the hill for the Alhambra: a ticket is €1.40 and "
               "the C30 and C32 go from the Plaza Nueva. Taxis are cheap for the station.",
    "san sebastian": "Everything is walkable: the two beaches are 15 minutes apart. A bus ticket "
                     "is about €2 for the ride out to Monte Igueldo, and there is a funicular for "
                     "the view.",
    "lisbon": "Get a Viva Viagem card from the machine and load it: a single is €1.85 and a "
              "24-hour pass €6.80. Tram 28 is beautiful and pickpocketed, so ride it early or "
              "take the metro instead.",
    "porto": "An Andante card covers the metro and the buses at about €1.60 a trip, plus 60 cents "
             "for the card itself. The historic tram is a separate €3.50 and worth doing once.",
    "amsterdam": "Tap in and out with a contactless card or an OV-chipkaart: a trip inside the "
                 "city is about €3.40 and forgetting to tap out costs you. The trams go "
                 "everywhere and the centre is small.",
    "berlin": "A single AB ticket is €3.50 and a 24-hour ticket about €10, so the day ticket wins "
              "after three rides. There are no ticket gates and the inspectors do fine, so "
              "validate before you board.",
    "munich": "A single is €3.90 and a day ticket for the inner zone about €8.60; the U-Bahn and "
              "S-Bahn are the way round and both run late. Validate the ticket before you get on.",
    "prague": "A 30-minute ticket is 30 crowns and a 90-minute one 40, from a machine or the app, "
              "and you stamp it on the first ride. The trams are the best sightseeing in the city.",
    "vienna": "A single is €2.40 and a 48-hour pass about €14, which is what a weekend wants. The "
              "U-Bahn is fast, the Ringstrasse is a 40-minute walk, and you validate the ticket "
              "once.",
    "budapest": "A single is 350 forints and a 24-hour ticket about 2,500, from the machine, "
                "validated before you board. Tram 2 along the Danube is the best ride in the "
                "city and costs the same as any other.",
    "krakow": "The old town and the castle are walkable; a 20-minute bus or tram ticket is 4 "
              "zloty from a machine, and the airport train is separate. The trams are old and "
              "cheap.",
    "istanbul": "Get an Istanbulkart from the machine and top it up: a ride is about 20 lira on "
                "the card and nearly double as a single, and one card covers several people. The "
                "trams and the ferries go where the traffic will not.",
    "athens": "A ticket is €1.20 and lasts 90 minutes on the metro, the trolleybuses and the "
              "trams; the airport line is separate. The centre under the Acropolis is walkable "
              "and the hills are not.",
    "dublin": "A Leap card takes about 30% off, so a bus or tram ride is €2 on it rather than the "
              "cash fare. The centre is 20 minutes across on foot and the DART follows the coast.",
    "edinburgh": "Lothian buses are a flat £2 and you tap a card, with no change given. The old "
                 "town and the new town are 15 minutes apart on foot, and the tram is only worth "
                 "it for the airport.",
    "copenhagen": "Tickets are by zone and a 24-hour city pass is about 90 kroner; a bike is what "
                  "everyone actually uses and most of the centre is a five-minute ride. The "
                  "harbour bus is a cheap boat trip.",
    "stockholm": "A single on the SL is about 39 kronor and a 72-hour pass about 270; the T-bana "
                 "is the way round and the old town is walkable. Tickets are cashless, so buy on "
                 "the app or tap a card.",
    "oslo": "A single on Ruter is about 40 kroner and a 24-hour ticket about 120; the trams and "
            "the metro are clean and the centre is walkable. Buy on the app before boarding.",
    "helsinki": "A ticket inside the city is about €3 and a day ticket €9, and the trams cover "
                "the centre on their own. The ferry to Suomenlinna runs on the same ticket.",
    "reykjavik": "The centre is walkable and a bus ticket is about 630 kronur, needed only for "
                 "the pools and the outer suburbs. Tours collect from stops near the hotels "
                 "rather than the door, so check which stop is yours.",
    "zurich": "Buy by zone on the ZVV app or at a machine: a trip across the city is about 4.30 "
              "francs and there are no barriers. The trams go everywhere and run to the minute.",
    "brussels": "A single on the metro, tram or bus is €2.60 and you tap a bank card at the gate. "
                "The Grand Place is 20 minutes from most of the centre on foot.",
    "new york": "Tap a contactless card or phone on the turnstile: a subway ride is $2.90 whatever "
                "the distance and trains run all night. Take the express where there is one, "
                "because the local stops every block.",
    "chicago": "A Ventra card or a contactless tap is $2.50 a ride on the L and the buses, and "
               "most L lines run all night. The loop is walkable and the L is for everything "
               "outside it.",
    "boston": "A CharlieCard is $2.40 a ride on the T and contactless works at the gates too. The "
              "subway covers the centre and the Freedom Trail is a walk between the stops.",
    "san francisco": "Tap a Clipper card or a phone on Muni: $2.50 buys 90 minutes on the buses "
                     "and the metro. BART is a separate fare for the airport, and the hills are "
                     "real, so take the cable car once.",
    "los angeles": "A TAP card is $1.75 a ride and a day caps at about $5, and the metro is fine "
                   "for Hollywood and Santa Monica. The traffic is the reason to plan, so stay "
                   "near where you are going.",
    "toronto": "A PRESTO tap is about $3.30 for two hours of streetcars, buses and subway. The "
               "centre is walkable and the PATH tunnels keep you out of the weather.",
    "mexico city": "The metro is 5 pesos a ride on a card from the machine, fast and very "
                   "crowded at rush hour. Uber is cheap and easier at night, and the pink line "
                   "covers most of the centre.",
    "tokyo": "Get a Suica or Pasmo card, or add one to your phone: a metro ride is about 180 yen "
             "and the machines take cash. Trains stop around midnight, so plan the last one.",
    "kyoto": "Buses are a flat 230 yen and the subway is only two lines, so the bus does the "
             "temples. Tap an IC card, and walk the Gion and Higashiyama side rather than ride.",
    "osaka": "An ICOCA card or a phone covers the metro and the private lines, about 190 yen a "
             "ride. The loop line gets you round the centre and Dotonbori is walkable.",
    "seoul": "A T-money card is about 1,400 won a ride and works on the metro, the buses and in "
             "taxis. The metro is cheap, clean, signed in English and the fastest way across the "
             "city.",
    "bangkok": "Get a Rabbit card for the BTS Skytrain: a ride is 17 to 45 baht and it goes over "
               "the traffic rather than through it. The metro is a separate ticket, and the river "
               "boats are the cheapest way along the Chao Phraya.",
    "singapore": "Tap a contactless card on the MRT and the buses: a trip is about S$2 and the "
                 "system is spotless. It stops around midnight, and a taxi or Grab after that.",
    "hong kong": "Get an Octopus card: it pays for the MTR, buses, ferries and shops, and a ride "
                 "is about HK$10 to 20. The MTR is the fastest way anywhere and the Star Ferry is "
                 "the cheapest sightseeing.",
    "sydney": "Tap on and off with a bank card or an Opal: a city trip is about A$4, and the "
              "train from the airport is a separate A$19. The ferries are the best value "
              "sightseeing in the city.",
    "melbourne": "A myki card or a contactless card covers trams, trains and buses at about A$5 "
                 "for two hours, and the tram zone in the centre is free. Trams run through the "
                 "night at weekends.",
    "dubai": "A Nol card covers the metro and the buses, and a ride is about 3 to 7.5 dirham. "
             "The metro is driverless and clean and goes to the malls; taxis are cheap by "
             "European standards.",
    "cape town": "There is no useful metro for visitors: use Uber or a MyCiTi bus, which is "
                 "about 8 rand a trip on a card, and hire a car for the Winelands and the Cape. "
                 "Agree the fare before you get in a taxi.",
    "vancouver": "A Compass card or a contactless tap covers the SkyTrain, the buses and the "
                 "SeaBus, and a trip inside the city is about C$3.15. The SkyTrain from the "
                 "airport costs a few dollars more, and the centre is walkable.",
    "marrakech": "Small taxis are the way round: 20 to 30 dirham inside the city, agreed before "
                 "you get in. The medina is walkable and a guide the first day is money well "
                 "spent.",
}

DAILY_BUDGET = {
    "spain": (45, 80, "eating at the bar and using trains rather than taxis is the difference"),
    "portugal": (40, 75, "the north is cheaper than the Algarve, and lunch is half the price of "
                          "dinner"),
    "italy": (55, 95, "coffee standing at the bar and one big meal at lunch keeps it down"),
    "greece": (45, 80, "the islands cost more than the mainland, mostly because of the ferries"),
    "france": (65, 110, "Paris is the top of that range; anywhere else is nearer the bottom"),
    "croatia": (50, 90, "July and August roughly double the accommodation, not the food"),
    "turkey": (30, 60, "the lira works in your favour if you change money there, not at home"),
    "japan": (60, 110, "the rail pass is a big fixed cost on top of these daily numbers"),
    "thailand": (30, 60, "street food and local buses keep it at the bottom of that range"),
    "dubai": (70, 130, "alcohol is the thing that pushes it up, and it is only sold in hotels"),
    "new york": (90, 160, "the city tax and the tip on every bill are what people forget"),
    "iceland": (90, 150, "petrol and eating out; the supermarkets are the way to keep food down"),
    "morocco": (30, 55, "a riad is cheap for what it is, and eating where locals do is cheaper"),
    "mexico": (30, 60, "the peso goes far outside the resort areas"),
    "australia": (70, 120, "it is a long way from anywhere, so food and fuel both cost more"),
    "lisbon": (45, 80, "eating at the bar and using the metro rather than taxis is the difference"),
    "porto": (40, 70, "it is cheaper than Lisbon and the portions are bigger"),
    "rome": (55, 95, "coffee standing at the bar and one big meal at lunch keeps it down"),
    "venice": (70, 120, "the water buses add up, so buy a multi-day pass once you are there"),
    "florence": (55, 95, "stay outside the centre and walk in: the hotels halve in price"),
    "paris": (65, 110, "lunch from a bakery and the metro rather than taxis is the difference"),
    "barcelona": (50, 85, "the menu del dia at lunch is half the price of the same meal at night"),
    "madrid": (45, 80, "tapas at the bar with a drink is cheaper than a sit-down dinner"),
    "amsterdam": (60, 100, "hire a bike rather than trams, and eat away from the canal belt"),
    "prague": (35, 65, "eat and drink away from the old town square and it halves"),
    "berlin": (50, 85, "it is cheaper than the rest of western Europe, especially eating out"),
    "edinburgh": (55, 90, "August doubles the hotel prices because of the festival"),
    "dublin": (60, 100, "the hotels are the expensive part, so book early"),
    "tokyo": (70, 120, "convenience store breakfast and a rail pass change the total completely"),
    "london": (65, 110, "the tube and eating away from the centre is what keeps it down"),
    "new york": (90, 160, "the city tax and the tip on every bill are what people forget"),
    "dubrovnik": (55, 95, "the old town is the top of that range and the walls are paid for"),
    "split": (40, 75, "it is the ferry port as much as a city, so eating inland costs less"),
    "athens": (40, 75, "the ruins are the cost here, not the food: lunch in a taverna is cheap"),
    "krakow": (30, 60, "the old town is the pricey part and the tram takes you out of it"),
    "budapest": (30, 60, "the baths and the ruin bars are where the money goes"),
    "seville": (45, 80, "tapas at the bar is the whole trick, and it is what locals do"),
    "valencia": (45, 80, "the beach is free and it is cheaper than Barcelona for the same food"),
    "vienna": (55, 95, "coffee and cake add up, and the transport pass is worth it"),
    "zurich": (95, 160, "everything is dear, so a supermarket lunch and the lake save the most"),
    "brussels": (55, 90, "the centre near the Grand Place is where the prices double"),
    "copenhagen": (70, 120, "bikes rather than taxis, and lunch from a bakery rather than a cafe"),
    "stockholm": (65, 110, "alcohol is the shock: eat and drink where people live, not in Gamla Stan"),
    "istanbul": (30, 60, "the tourist quarter is the dear part, and the ferries are cheap"),
    "bangkok": (25, 55, "street food is a few pounds a meal, and the skytrain beats the traffic"),
    "singapore": (60, 110, "hawker centres keep food cheap and hotels are what pushes it up"),
    "cape town": (35, 70, "the rand helps, and the wine is cheaper than the food"),
    "sydney": (70, 120, "coffee and transport are dear, and the beaches cost nothing"),
    "san francisco": (90, 160, "the hotel tax and the tip are the parts people forget"),
    "orlando": (70, 130, "the park tickets are the cost, not the meals"),
    "marrakesh": (25, 55, "haggling in the souk is expected, and a riad is cheap for what it is"),
}

TRIP_UNITS = (("weekend", 2), ("long weekend", 3), ("a week", 7), ("one week", 7),
              ("two weeks", 14), ("fortnight", 14), ("a month", 30), ("four nights", 4),
              ("three nights", 3), ("two nights", 2), ("five nights", 5))


CITY_DAYS = {
    "amsterdam": 2, "athens": 2, "bangkok": 3, "barcelona": 3, "bath": 1, "berlin": 3,
    "boston": 2, "brussels": 2, "budapest": 2, "buenos aires": 3, "cape town": 4, "chicago": 2,
    "copenhagen": 2, "dubai": 3, "dublin": 2, "dubrovnik": 2, "edinburgh": 2, "florence": 2,
    "granada": 2, "hanoi": 3, "havana": 2, "helsinki": 2, "istanbul": 3, "krakow": 2,
    "kyoto": 3, "lisbon": 3, "ljubljana": 1, "london": 4, "los angeles": 3, "madrid": 3,
    "marrakech": 2, "mexico city": 3, "milan": 2, "munich": 2, "naples": 2, "new york": 4,
    "oslo": 2, "paris": 4, "porto": 2, "prague": 3, "reykjavik": 3, "rio de janeiro": 3,
    "rome": 3, "san francisco": 2, "san sebastian": 2, "santorini": 2, "seville": 2,
    "singapore": 3, "stockholm": 2, "sydney": 3, "tallinn": 1, "tokyo": 4, "toronto": 2,
    "valencia": 2, "venice": 2, "vienna": 3, "zurich": 2,
}

_PLUG_GROUPS = (
    (("G", "three square pins", ""),
     ("uk", "england", "scotland", "wales", "ireland", "malta", "cyprus", "singapore",
      "hong kong", "malaysia", "uae", "dubai", "saudi arabia", "qatar", "kuwait", "bahrain",
      "kenya", "nigeria", "ghana")),
    (("C and E", "two round pins", ""),
     ("france", "germany", "spain", "portugal", "greece", "netherlands", "belgium", "austria",
      "poland", "czechia", "hungary", "croatia", "slovenia", "slovakia", "romania", "bulgaria",
      "estonia", "latvia", "lithuania", "luxembourg", "turkey", "morocco", "tunisia", "egypt",
      "iceland", "norway", "sweden", "finland", "russia", "south korea", "indonesia",
      "vietnam", "thailand", "cambodia", "nepal")),
    (("C and J", "two round pins, with a third offset one in some sockets", ""),
     ("switzerland",)),
    (("C and K", "two round pins, with a third one in some sockets", ""), ("denmark",)),
    (("C, F and L", "two round pins, and the old three-in-a-row socket", ""), ("italy",)),
    (("C and H", "two round pins, with a third one in some sockets", ""), ("israel",)),
    (("A and B", "two flat pins", ""),
     ("usa", "america", "the states", "canada", "taiwan", "philippines")),
    (("A and B", "two flat pins", "The supply is 100 volts, half of ours, so check anything with "
     "a motor or a heating element."), ("japan",)),
    (("A and B", "two flat pins", "The supply is 127 volts, so check anything with a motor."),
     ("mexico",)),
    (("I", "two slanted flat pins", ""),
     ("australia", "new zealand", "argentina", "fiji", "china")),
    (("C, D and M", "three fat round pins", ""),
     ("india", "south africa", "sri lanka", "bangladesh", "pakistan")),
    (("C and N", "two round pins", ""), ("brazil",)),
)
PLUG_TYPES = {place: plug for plug, places in _PLUG_GROUPS for place in places}

WATER_OK = ("uk", "england", "scotland", "wales", "ireland", "france", "spain", "portugal",
            "italy", "germany", "austria", "switzerland", "netherlands", "belgium", "denmark",
            "sweden", "norway", "finland", "iceland", "greece", "croatia", "slovenia", "poland",
            "czechia", "malta", "cyprus", "usa", "america", "the states", "canada", "australia",
            "new zealand", "japan", "south korea", "singapore", "uae", "chile",
            "argentina", "south africa", "israel", "hungary", "slovakia", "estonia", "latvia",
            "lithuania", "bulgaria", "romania")
WATER_NO = ("mexico", "india", "nepal", "bangladesh", "pakistan", "sri lanka", "thailand",
            "vietnam", "cambodia", "laos", "indonesia", "philippines", "malaysia", "china",
            "egypt", "morocco", "tunisia", "turkey", "kenya", "nigeria", "ghana", "tanzania",
            "zanzibar", "peru", "bolivia", "colombia", "brazil", "cuba", "jamaica",
            "dominican republic", "hanoi", "bangkok", "marrakech", "mexico city", "istanbul",
            "dubai")
WATER = {place: True for place in WATER_OK}
WATER.update({place: False for place in WATER_NO})

TAP_WATER_HOME = (
    "Tap water from the mains is safe to drink without boiling it, and it is tested far more "
    "often than anything in a bottle: in the UK the results are published by the water company, "
    "and bottled water is not held to a higher standard. Run the cold tap for half a minute "
    "first, because water that has sat in the pipes overnight picks up the taste of them, and "
    "fill a bottle from the cold tap to carry round. Only a notice from your water company to "
    "boil it means boiling.")
TAP_WATER_HOME_BROWN = (
    "Brown or yellow water is usually a burst main nearby, or rust shaken out of old iron pipes: "
    "run the cold tap for two minutes, and ring your water company if it does not clear, because "
    "they flush the main for free. If your house is old, ask them whether the supply pipe is "
    "lead, and never drink from the hot tap.")
TAP_WATER_HOME_TASTE = (
    "A taste or smell of chlorine is the disinfectant that keeps the water safe, and it fades if "
    "you let a jug stand in the fridge for an hour. A metallic taste is usually old pipes, so run "
    "the cold tap for a minute first, ask your water company whether the supply pipe is lead, and "
    "never drink from the hot tap.")
TAP_WATER_GENERAL = (
    "Tap water is fine in most of southern Europe and in Australia; in Mexico, most of "
    "Africa, India and much of South-East Asia it is not, so drink bottled or filtered "
    "water and skip ice from street stalls. Use bottled water for brushing your teeth if "
    "you are unsure, and eat fruit you peel yourself for the first few days.")


JET_EAST = ("asia", "japan", "china", "hong kong", "singapore", "thailand", "vietnam", "bali",
            "indonesia", "malaysia", "korea", "seoul", "tokyo", "beijing", "shanghai", "dubai",
            "india", "delhi", "mumbai", "sri lanka", "maldives", "australia", "sydney",
            "melbourne", "new zealand", "auckland", "fiji", "south africa", "cape town")
JET_WEST = ("america", "the states", "usa", "us", "canada", "new york", "boston", "chicago",
            "florida", "miami", "california", "los angeles", "san francisco", "seattle",
            "hawaii", "mexico", "cuba", "brazil", "rio", "argentina", "buenos aires", "peru",
            "chile", "colombia", "iceland", "reykjavik")

JET_EAST_KEYS = ("east", "eastwards", "forward", "ahead") + JET_EAST
JET_WEST_KEYS = ("west", "westwards", "back") + JET_WEST

TIME_ZONES = {
    "london": (0, 0), "dublin": (0, 0), "edinburgh": (0, 0), "lisbon": (0, 0), "reykjavik": (0, 0),
    "marrakech": (0, 0), "paris": (1, 1), "berlin": (1, 1), "madrid": (1, 1), "rome": (1, 1),
    "amsterdam": (1, 1), "brussels": (1, 1), "vienna": (1, 1), "prague": (1, 1),
    "copenhagen": (1, 1), "stockholm": (1, 1), "oslo": (1, 1), "zurich": (1, 1), "lagos": (1, 1),
    "tunis": (1, 1), "athens": (2, 2), "helsinki": (2, 2), "cairo": (2, 2), "cape town": (2, 2),
    "tel aviv": (2, 2), "amman": (2, 2), "istanbul": (3, 3), "moscow": (3, 3), "nairobi": (3, 3),
    "qatar": (3, 3), "dubai": (4, 3), "abu dhabi": (4, 3), "delhi": (5.5, 4.5),
    "mumbai": (5.5, 4.5), "sri lanka": (5.5, 4.5), "bangkok": (7, 6), "hanoi": (7, 6),
    "singapore": (8, 7), "hong kong": (8, 7), "beijing": (8, 7), "shanghai": (8, 7),
    "bali": (8, 7), "kuala lumpur": (8, 7), "perth": (8, 7), "tokyo": (9, 8), "seoul": (9, 8),
    "sydney": (11, 9), "melbourne": (11, 9), "fiji": (12, 11), "auckland": (13, 11),
    "new york": (-5, -5), "boston": (-5, -5), "toronto": (-5, -5), "miami": (-5, -5),
    "havana": (-5, -5), "bogota": (-5, -5), "lima": (-5, -5), "chicago": (-6, -6),
    "mexico city": (-6, -6), "los angeles": (-8, -8), "san francisco": (-8, -8),
    "seattle": (-8, -8), "vancouver": (-8, -8), "honolulu": (-10, -10), "rio": (-3, -4),
    "sao paulo": (-3, -4), "buenos aires": (-3, -3), "santiago": (-4, -4),
    "uk": (0, 0), "the uk": (0, 0), "britain": (0, 0), "england": (0, 0), "scotland": (0, 0),
    "wales": (0, 0), "ireland": (0, 0), "portugal": (0, 0), "morocco": (0, 0), "iceland": (0, 0),
    "france": (1, 1), "germany": (1, 1), "italy": (1, 1), "spain": (1, 1), "holland": (1, 1),
    "netherlands": (1, 1), "belgium": (1, 1), "austria": (1, 1), "switzerland": (1, 1),
    "czech republic": (1, 1), "czechia": (1, 1), "denmark": (1, 1), "sweden": (1, 1),
    "norway": (1, 1), "croatia": (1, 1), "poland": (1, 1), "hungary": (1, 1), "nigeria": (1, 1),
    "finland": (2, 2), "greece": (2, 2), "egypt": (2, 2), "israel": (2, 2), "jordan": (2, 2),
    "turkey": (3, 3), "kenya": (3, 3), "qatar": (3, 3), "uae": (4, 3), "oman": (4, 3),
    "india": (5.5, 4.5), "thailand": (7, 6), "vietnam": (7, 6), "china": (8, 7),
    "singapore": (8, 7), "malaysia": (8, 7), "indonesia": (8, 7), "japan": (9, 8),
    "south korea": (9, 8), "new zealand": (13, 11), "fiji": (12, 11), "mexico": (-6, -6),
    "cuba": (-5, -5), "peru": (-5, -5), "colombia": (-5, -5), "chile": (-4, -4),
    "argentina": (-3, -3), "florida": (-5, -5), "california": (-8, -8), "texas": (-6, -6),
}

MULTI_ZONES = {
    "australia": ("Sydney and Melbourne are eleven hours ahead of the UK in winter and nine in "
                  "summer, Perth eight and seven, so it depends where you land"),
    "america": ("New York is five hours behind the UK, Chicago six, Los Angeles and San Francisco "
                "eight, so it depends which side you are on"),
    "usa": ("New York is five hours behind the UK, Chicago six, Los Angeles and San Francisco "
            "eight, so it depends which side you are on"),
    "canada": ("Toronto is five hours behind the UK and Vancouver eight, so it depends which end"),
    "brazil": ("Rio and Sao Paulo are three hours behind the UK in winter and four in summer"),
    "russia": ("Moscow is three hours ahead of the UK all year; the far east runs to nine"),
}


_TIME_ZONE_SHAPE = ("time difference", "time zone", "whats the time", "what time is it",
                    "what is the time", "the time in", "local time", "hours ahead", "hours behind",
                    "ahead of us", "behind us", "how many hours ahead", "clock in")

CITY_AREA = {
    "rome": ("Monti for the Colosseum on foot and quiet nights, Trastevere for restaurants and "
             "cobbles, or Prati for the Vatican and a calmer evening"),
    "paris": ("Le Marais for the centre and cafes, Saint-Germain for the classic postcard, or "
              "Canal Saint-Martin for cheaper nights and a younger crowd"),
    "london": ("Bloomsbury to walk to most of it, the South Bank for the river and theatres, or "
               "Shoreditch for bars and a late night"),
    "barcelona": ("the Eixample for a grid that is easy to walk and safe at night, Gracia for a "
                  "village feel, or El Born for tapas and narrow streets"),
    "madrid": ("La Latina for tapas on the doorstep, Malasana for going out, or Salamanca for "
               "somewhere smart and quiet"),
    "lisbon": ("Alfama for the old streets and the views but steep and noisy, Baixa and Chiado to "
               "be in the middle of it, or Principe Real for quiet and smart"),
    "amsterdam": ("the Jordaan for canals and quiet, De Pijp for the food market and locals, or "
                  "the centre if you want everything on foot and do not mind noise"),
    "berlin": ("Mitte for the centre and the museums, Kreuzberg for nightlife and grit, or "
               "Prenzlauer Berg for cafes and families"),
    "vienna": ("the Innere Stadt to walk to the palaces and concerts, Leopoldstadt for the Prater "
               "and cheaper rooms, or Neubau for small shops and cafes"),
    "prague": ("Vinohrady for leafy streets and local restaurants, Mala Strana for quiet and "
               "pretty, or the Old Town for the middle of it and the noise"),
    "budapest": ("District V for the centre, District VII for the ruin bars and the noise, or the "
                 "Buda side for quiet and the views"),
    "copenhagen": ("Norrebro for food and a local feel, Vesterbro for bars near the meatpacking "
                   "district, or Indre By to be in the middle"),
    "stockholm": ("Sodermalm for bars and views, Gamla Stan for the postcard and the crowds, or "
                  "Ostermalm for somewhere smarter"),
    "oslo": ("Grunerlokka for cafes and the river, the centre for the harbour and the station, or "
             "Majorstuen for quiet"),
    "helsinki": ("Kallio for bars and cheaper rooms, the Design District for the centre on foot, "
                 "or Kamppi for the transport hub"),
    "dublin": ("Portobello for quiet and locals, St Stephen's Green to be central, or Temple Bar "
               "for the pubs and the noise that comes with them"),
    "edinburgh": ("the New Town for Georgian calm and everything on foot, the Old Town for the "
                  "Royal Mile and tourists, or Leith for the food"),
    "venice": ("Cannaregio for local life and canals, Dorsoduro for art and quiet, or San Marco "
               "for the middle of it and the day trippers"),
    "florence": ("Santa Croce for the centre and a lively square, Oltrarno for artisans and "
                 "quiet, or around Santa Maria Novella for the station"),
    "naples": ("Chiaia for the seafront and somewhere smart, the Centro Storico for food and "
               "chaos, or Vomero for the hill and a calm night"),
    "milan": ("Brera for chic and central, the Navigli for canals and nightlife, or Porta Romana "
              "for quieter streets"),
    "athens": ("Koukaki for the museum and local tavernas, Plaka for under the Acropolis, or "
               "Exarchia if you want the edgier side"),
    "istanbul": ("Sultanahmet for the sights on foot and quiet nights, Beyoglu for going out, or "
                 "Kadikoy on the Asian side for food and locals"),
    "marrakech": ("a riad inside the medina for the atmosphere, Gueliz for modern hotels and "
                  "quiet, or the Kasbah for the sights"),
    "seville": ("Santa Cruz for narrow streets and the Alcazar, Triana for ceramics and locals, "
                "or the Alameda for bars"),
    "porto": ("Ribeira for the river and the crowds, Cedofeita for shops and cafes, or Bonfim for "
              "local streets and cheaper rooms"),
    "new york": ("Midtown for the sights and the noise, the Lower East Side for food and bars, or "
                 "Brooklyn for cheaper rooms and 20 minutes on the train"),
    "san francisco": ("the Mission for food and the sun, North Beach for Italian and the wharf, "
                      "or SoMa for the middle of it"),
    "los angeles": ("Santa Monica for the beach, Hollywood for the sights and grit, or Downtown "
                    "for the arts and the bars"),
    "chicago": ("River North to walk to the lake and the galleries, Wicker Park for bars, or the "
                "Loop for the trains"),
    "tokyo": ("Shinjuku for the transport and the nightlife, Asakusa for the old town and quiet, "
              "or Shibuya if you want to be in the middle of it"),
    "kyoto": ("Kawaramachi for the centre and dinner, Gion for the old streets, or Arashiyama for "
              "quiet and the bamboo"),
    "singapore": ("Chinatown for food and value, Marina Bay for the sights, or Orchard for "
                  "shopping"),
    "bangkok": ("Sukhumvit for hotels and food, the riverside for views and boats, or Khao San for "
                "the backpacker end"),
    "sydney": ("Surry Hills for cafes and bars, Circular Quay for the harbour on the doorstep, or "
               "Bondi for the beach"),
    "dubai": ("Dubai Marina for the beach and towers, Downtown for the Burj and the malls, or "
              "Deira for the souks and lower prices"),
    "reykjavik": ("101 downtown to walk to everything, or Laugavegur for the shops and bars and a "
                  "short walk to the harbour"),
    "mexico city": ("Roma and Condesa for leafy streets and cafes, Centro for the sights, or "
                    "Coyoacan for quiet"),
    "toronto": ("King West for bars and the centre, Kensington Market for food and a local feel, "
                "or the Distillery District for cobbles"),
    "boston": ("Back Bay for the shopping and the river, Beacon Hill for the postcard streets, or "
               "the North End for Italian food"),

    "bath": ("the centre by the Abbey to walk to the baths and the shops, or the Royal Crescent "
             "end for Georgian streets and quiet"),
    "ljubljana": ("the old town by the river for cafes and everything on foot, or Tivoli park "
                  "side for green and quiet"),
    "krakow": ("the Old Town for the square and the sights on foot, or Kazimierz for bars, food "
               "and a local feel"),
    "munich": ("the Altstadt for the beer halls and the sights, Schwabing for a student feel and "
               "the English Garden, or near the station for day trips"),
    "zurich": ("the Niederdorf for the old town on foot, or the west side near the river for "
               "bars and cheaper rooms"),
    "tallinn": ("the old town for the walls and the square, or Kalamaja for wooden houses and "
                "cafes and a short walk in"),
    "dubrovnik": ("inside the walls for the postcard and the noise, or Lapad and Babin Kuk for "
                  "beaches and calmer nights and a bus into town"),
    "santorini": ("Imerovigli or Pyrgos for the view without the crowds, or Oia for the sunset "
                  "and the people who come to see it"),
    "valencia": ("the Carmen for the old town and bars, or the beach end for sand and the tram"),
    "granada": ("the Albaicin for the views and the old streets, or the centre near the cathedral "
                "for tapas on the doorstep"),
    "san sebastian": ("the old town for pintxos on the doorstep, or Gros for the surf beach and "
                      "quieter nights"),
    "cape town": ("the city bowl for the restaurants and the mountain, Camps Bay for the beach, "
                  "or Stellenbosch if you want the wine farms"),
    "havana": ("Habana Vieja for the old streets on foot, or Vedado for 1950s hotels and a local "
               "evening"),
    "buenos aires": ("Palermo for restaurants and going out, Recoleta for the grand streets, or "
                     "San Telmo for the old quarter"),
    "rio de janeiro": ("Ipanema for the beach and the bars, or Santa Teresa for the old streets "
                       "on the hill"),
    "hanoi": ("the old quarter for the street food and the lake on foot, or the French quarter "
              "for quieter nights"),
}

WHERE_TO_STAY = ("where should i stay", "where shall i stay", "where do i stay", "where to stay",
                 "where should we stay", "best area to stay", "area to stay", "which area",
                 "what area", "where is good to stay", "best place to stay", "good area",
                 "neighbourhood", "neighborhood", "part of town", "which part",
                 "a hotel", "a hostel", "somewhere to stay", "a place to stay",
                 "accommodation", "places to stay", "hotels to stay", "a bed for the night",
                 "where should i sleep", "where can i sleep", "where do i sleep",
                 "where should we sleep", "where shall we sleep", "where should i kip",
                 "somewhere to sleep", "a place to sleep",
                 "where do we stay", "where can we stay", "where can i stay",
                 "where could i stay", "where should i stay the night",
                 "area should i stay", "area to stay in", "area do i stay")

AMBIGUOUS_PLACES = ("bath", "split", "cork")
_PLACE_SHAPE = (r"\b(?:go|goes|going|went|get|getting|travel|travelling|traveling|trip|holiday|"
                r"visit|visiting|stay|staying|fly|flying|from|in|near|see|seeing)\s+(?:to\s+)?%s\b")


def _worth_a_visit(text, name):
    name = re.escape(name)
    return re.search(r"(?<![a-z])" + name + r"\s+(?:is\s+)?worth"
                     r"|\bis\s+" + name + r"\s+worth"
                     r"|\bworth\s+(?:visiting|seeing|going to)\s+" + name + r"\b", text) is not None


def _names_place(text, name):
    if name not in AMBIGUOUS_PLACES:
        return True
    if re.search(_PLACE_SHAPE % re.escape(name), text) is not None:
        return True
    return _worth_a_visit(text, name)


def _find_in(text, table):
    for name in sorted(table, key=len, reverse=True):
        if re.search(r"(?<![a-z])" + re.escape(name) + r"(?![a-z])", text) and _names_place(text, name):
            return name
    return None


CAPITAL_WORD = re.compile(r"\bcapitals?\b")


def _capital(memory, understood):
    said = understood.get("clean", "") or ""
    if not CAPITAL_WORD.search(said):
        return None
    country = _find_in(said, CAPITALS)
    if not country:
        return None
    return f"{CAPITALS[country]}"


def _place_in(memory, understood, table):
    clean = understood.get("clean", "")
    name = _find_in(clean, table)
    if name:
        if table is WHERE_TO_GO and _a_thing_not_a_place(clean, name):
            return None
        return name
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return None
    for turn in reversed(turns[-2:]):
        if not isinstance(turn, dict):
            continue
        name = _find_in(str(turn.get("user") or "").lower(), table)
        if name:
            return name
    return None


SEASON_MONTHS = {"spring": {3, 4, 5}, "summer": {6, 7, 8}, "high summer": {7, 8},
                 "autumn": {9, 10, 11}, "fall": {9, 10, 11}, "winter": {12, 1, 2}}
SEASON_NOUNS = ("spring", "summer", "autumn", "fall", "winter")
_MONTH_IN_TEXT = re.compile(
    r"(?:^|(?<=in )|(?<=for )|(?<=until )|(?<=from )|(?<=to )|(?<=by )|(?<=early )"
    r"|(?<=late )|(?<=mid ))(%s)\b" % "|".join(sorted(MONTHS, key=len, reverse=True)))
_SEASON_IN_TEXT = re.compile(r"\b(%s)\b" % "|".join(SEASON_NOUNS))


AMBIGUOUS_MONTHS = frozenset(("may", "march", "fall"))


def _time_terms(text, loose=False):
    if not isinstance(text, str) or not text.strip():
        return set(), set()
    low = " ".join(text.lower().split())
    words = set(tokens(low))
    months = {MONTHS[match.group(1)] for match in _MONTH_IN_TEXT.finditer(low)}
    if loose:
        months |= {number for word, number in MONTHS.items()
                   if word in words and word not in AMBIGUOUS_MONTHS}
    for word, number in MONTHS.items():
        if len(word) > 3 and re.search(r"\b%s\b" % word.capitalize(), text):
            months.add(number)
    seasons = {match.group(1) for match in _SEASON_IN_TEXT.finditer(low)}
    if "high summer" in low:
        seasons.add("high summer")
    for match in _MONTH_RANGE.finditer(low):
        months |= _between(MONTHS[match.group(1)], MONTHS[match.group(2)])
    return months, seasons


_MONTH_RANGE = re.compile(
    r"\b(%s)\s*(?:to|-|–|until|till|through)\s*(%s)\b"
    % ("|".join(sorted(MONTHS, key=len, reverse=True)),
       "|".join(sorted(MONTHS, key=len, reverse=True))))


def _between(first, last):
    months, number = set(), first
    for _ in range(12):
        months.add(number)
        if number == last:
            break
        number = number % 12 + 1
    return months


def _when_said(memory, understood):
    months, seasons = _time_terms(understood.get("clean", ""), loose=True)
    planned = the_plan(memory)
    if planned:
        planned_months, planned_seasons = _time_terms(planned, loose=True)
        if planned_months or planned_seasons:
            return months | planned_months, seasons | planned_seasons
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if isinstance(turns, list):
        for turn in reversed(turns[-2:]):
            if isinstance(turn, dict):
                more_months, more_seasons = _time_terms(str(turn.get("user") or ""), loose=True)
                months |= more_months
                seasons |= more_seasons
    return months, seasons


def _season_fits(sentence, when):
    stated_months, stated_seasons = when
    if not stated_months and not stated_seasons:
        return True
    months, seasons = _time_terms(sentence)
    if not months and not seasons:
        return True
    if months & stated_months:
        return True
    for season in seasons:
        if SEASON_MONTHS[season] & stated_months:
            return True
        if not stated_months and season in stated_seasons:
            return True
    return False


def _without_the_season(text, when):
    if not isinstance(text, str):
        return text
    sentences = re.split(r"(?<=[.!?]) ", text.strip())
    if len(sentences) < 2 or _season_fits(sentences[-1], when):
        return text
    return " ".join(sentences[:-1])


_WORTH_ASK = re.compile(r"\bworth (?:visiting|going|a visit|it)\b")
_EAT_ASK = re.compile(
    r"(?<![a-z])(?:eat|eats|eating|ate|food|foods|dinner|dine|dining|lunch|breakfast|"
    r"restaurant|restaurants|dish|dishes|cuisine|menus?|street food)(?![a-z])", re.I)


FOLLOW_MARKS = ("there", "that city", "this city", "also", "too", "what about", "and ",
                "anything else", "any more")


CHEAP_EATS = {
    "rome": "In Rome the cheap meal is pizza al taglio, sold by weight and eaten standing, or a "
            "panino from a bakery counter; supplì and a slice of pizza bianca are a couple of "
            "euros. Eat in Testaccio or Trastevere rather than beside a monument, and take your "
            "coffee standing at the bar, where it costs a third of the table price.",
    "paris": "In Paris the cheap lunch is a bakery one: a jambon-beurre is about five euros, and "
             "a market street such as Rue Cler or Rue Mouffetard does the same for less. The plat "
             "du jour at a neighbourhood bistro is half the evening price, tap water is free and "
             "normal, and a picnic on the quays beats a table by the Eiffel Tower.",
    "barcelona": "In Barcelona the cheat code is the menú del día at lunch: three courses and a "
                 "drink for around twelve to fifteen euros, in the Eixample or Gràcia, not on Las "
                 "Ramblas. Standing at a bar with tapas and a vermut costs a few euros a round, "
                 "and the Boqueria's back stalls are cheaper than its front ones.",
    "madrid": "In Madrid the menú del día at lunch is the cheap meal, and tapas around La Latina "
              "or Lavapiés are a few euros each, with the drink included in most bars. Standing "
              "at the bar is cheaper than a table, and dinner starts late, so lunch is the meal "
              "to spend on.",
    "lisbon": "In Lisbon a bifana or a pastel de nata at a counter costs a couple of euros, and "
              "the prato do dia at lunch in Alfama or Graça is the full cheap meal. Drink at a "
              "kiosk rather than a terrace, and the Time Out Market is the easy one-stop version.",
    "florence": "In Florence the cheap meal is a panino from a busy shop (a big one is about six "
                "euros), pizza al taglio, or a trattoria across the river in the Oltrarno; a "
                "table on a piazza with a view is the expensive version of the same food.",
    "amsterdam": "In Amsterdam the cheap meal is a broodje from a bakery, a portion of chips with "
                 "mayonnaise, or the market at Albert Cuypstraat; a supermarket picnic in the "
                 "Vondelpark costs less than a café lunch, and tap water is free if you ask.",
}

def _place_in_the_plan(memory, table):
    user = memory.get("user") if isinstance(memory, dict) else None
    if not isinstance(user, dict):
        return None
    current = the_plan(memory)
    if isinstance(current, str) and current.strip():
        name = _find_in(current.lower(), table)
        if name:
            return name
        if _find_in(current.lower(), CITIES):
            return None
    plans = user.get("plans")
    if not isinstance(plans, list):
        plans = [user.get("plan")]
    for plan in reversed([one for one in plans if isinstance(one, str) and one.strip()]):
        name = _find_in(plan.lower(), table)
        if name:
            return name
    return None


def _cheap_eats(memory, understood):
    clean = (understood.get("clean") or understood.get("text") or "").lower()
    city = next((one for one in CHEAP_EATS if one in clean), None)
    if not city:
        city = _place_in_the_plan(memory, CHEAP_EATS)
    if city:
        return CHEAP_EATS[city]
    if "eat there" in clean:
        return None
    return ("Three habits make any city cheap to eat in: take the fixed lunch rather than "
            "dinner - menu del día, plat du jour, prato do dia, Mittagsmenü - which is the same "
            "kitchen at half the price; eat where people work and shop, at a market hall, a "
            "bakery counter or a busy bar, rather than where they sightsee; and stand up to eat, "
            "because pizza by the slice, a kebab, a bowl of noodles at a counter or a picnic "
            "from a supermarket costs a fraction of a table with a view. Coffee and breakfast at "
            "a bar, and tap water in a bottle you refill, save the rest.")

def _guide(memory, understood):
    clean = understood.get("clean", "")
    if _WORTH_ASK.search(clean) and any(_time_terms(clean, loose=True)):
        return None
    if BOOK_ASK.search(clean):
        return None
    if _EAT_ASK.search(clean) and _find_in(clean, CHEAP_EATS):
        return None
    city = _find_in(clean, CITIES)
    if not city:
        if SIGHTSEEING_ASK.search(clean):
            return _guide_next(memory, understood)
        return None
    body = _without_the_season(CITIES[city], _when_said(memory, understood))
    if _already_guided(memory, city) and understood.get("asks"):
        said = (understood.get("plain") or understood.get("text") or clean).lower()
        if _said_before_in_the_chat(memory, clean, understood):
            return f"In {city.title()}: {body}"
        if _find_in(said, CITIES) == city and _asked_for_the_guide_before(memory, city, clean):
            return f"In {city.title()}: {body}"
        return _about_city(city, memory, clean, understood)
    return f"In {city.title()}: {body}"


NOT_THE_ASK_WORDS = frozenset("""the a an in to for at of on and or but it its there here this
    that these those do does did i we me my us you your should could would can what whats
    trip""".split())


def _the_ask_words(text):
    words = set()
    for word in str(text or "").lower().replace("?", " ").replace(",", " ").split():
        word = word.strip(string.punctuation)
        if len(word) < 3 or not word.isalpha():
            continue
        if word in NOT_THE_ASK_WORDS or word in CITIES:
            continue
        words.add(word)
    return words


def _said_before_in_the_chat(memory, clean, understood=None):
    said = understood if isinstance(understood, dict) else {}
    mine = _the_ask_words(said.get("text") or said.get("plain") or clean) - _the_plan_words(memory)
    if not mine:
        return False
    for turn in (memory.get("turns") or []):
        if not isinstance(turn, dict) or not turn.get("bot"):
            continue
        if _the_ask_words(turn.get("user")) - _the_plan_words(memory) == mine:
            return True
    return False


def _the_plan_words(memory):
    user = memory.get("user") if isinstance(memory, dict) else None
    if not isinstance(user, dict):
        return frozenset()
    plans = [str(one) for one in ([user.get("plan")] + list(user.get("plans") or [])) if one]
    words = frozenset()
    for plan in plans:
        words = words | _the_ask_words(plan)
    return words


STAYS_THERE = re.compile(r"\b(?:stay|stays|staying|stayed|nights?|days?)\b", re.I)


def _the_lines_said(memory, understood):
    said = [understood.get("clean") or ""]
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in reversed((turns or [])[-2:]):
        if isinstance(turn, dict):
            said.append(str(turn.get("user") or ""))
    return said


def _lines_about(place, said):
    return [line.lower() for line in said if line and str(place) in line.lower()]


def _a_trip_to(place, memory, understood):
    from ..memory.topics import LIVES_THERE, going_there
    said = _the_lines_said(memory, understood)
    low = _lines_about(place, said)
    if any(_lives_in(place, line) for line in low):
        return False
    if any(STAYS_THERE.search(line) for line in low):
        return True
    if any(going_there(place, line) for line in said
           if line and str(place) in line.lower()):
        return True
    from ..memory.topics import LIVES_THERE
    if ASKS_A_LENGTH.search(understood.get("clean") or ""):
        turns = memory.get("turns") if isinstance(memory, dict) else None
        since = [str((turn or {}).get("user") or "").lower()
                 for turn in reversed((turns or [])[-3:]) if isinstance(turn, dict)]
        if any(str(place) in line for line in since) and not any(
                str(place) in line[found.end():found.end() + 40]
                for line in since for found in LIVES_THERE.finditer(line)):
            return True
    return False


A_JOURNEY_OR_A_BAG = re.compile(
    r"\b(?:flight|flights|fly|flying|train|trains|bus|coach|drive|driving|journey|"
    r"walk|walking|ferry|transfer|queue|wait|pack|packing|clothes|suitcase|luggage|"
    r"case)\b")

ASKS_A_LENGTH = re.compile(
    r"\b(?:how long|how many days|how many nights|how much time|enough time|too long|"
    r"too short|days in|nights in)\b", re.I)


def _lives_in(place, line):
    from ..memory.topics import LIVES_THERE
    for match in LIVES_THERE.finditer(str(line or "").lower()):
        if str(place) in str(line or "").lower()[match.end():match.end() + 40]:
            return True
    return False


def _stay_length(memory, understood):
    clean = understood.get("clean", "")
    if A_JOURNEY_OR_A_BAG.search(clean):
        return None
    stated = re.search(r"\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|a few|"
                       r"a couple of|several)\s+(?:full\s+)?(?:days|nights|day|night)\b", clean)
    asking = re.search(r"\b(?:enough|too long|too short|too much|worth it|worth|do i need|"
                       r"should i|should we|do we need)\b", clean)
    if stated and not asking:
        return None
    if not asking and not re.search(r"\b(?:how long|how many days|how many nights|how much time)\b",
                                    clean):
        return None
    place = _place_in(memory, understood, CITY_DAYS)
    if not place:
        return _country_stay_length(memory, understood)
    if not _a_trip_to(place, memory, understood):
        if not (_find_in(clean, CITY_DAYS)
                and re.search(r"\b(?:in|at|to see|to visit|around|for)\s+"
                              + re.escape(place), clean)):
            return None
        said = _the_lines_said(memory, understood)
        if any(_lives_in(place, line) for line in _lines_about(place, said)):
            return None
    return _stay_days(place)


def _the_places_the_country_card_names(country):
    body = WHERE_TO_GO.get(country, ("", ""))[1].lower()
    found = []
    for name in CITY_DAYS:
        found_at = re.search(r"(?<![a-z])" + re.escape(name) + r"(?![a-z])", body)
        if found_at:
            found.append((found_at.start(), name))
    return [name for _, name in sorted(found)]


def _country_stay_length(memory, understood):
    clean = understood.get("clean", "")
    if A_JOURNEY_OR_A_BAG.search(clean):
        return None
    country = _place_in(memory, understood, WHERE_TO_GO)
    if not country:
        return None
    if _place_in(memory, understood, CITY_DAYS):
        return None
    if re.search(r"\b(?:there|that city|this city|the city)\b", clean, re.I):
        return None
    typed = str(understood.get("text") or "").lower()
    if typed and str(country) not in typed:
        return None
    if not (_a_trip_to(country, memory, understood)
            or (ASKS_A_LENGTH.search(clean) and str(country) in clean.lower())):
        return None
    from ..memory.topics import LIVES_THERE
    if any(str(country) in clean[found.end():found.end() + 40]
           for found in LIVES_THERE.finditer(clean)):
        return None
    places = _the_places_the_country_card_names(country)
    if not places:
        return None
    label = WHERE_TO_GO[country][0]
    if len(places) == 1:
        return _stay_days(places[0])
    words = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten")
    first, second = places[0], places[1]
    text = (f"{label}: {first.title()} {_full_days(CITY_DAYS[first])}, "
            f"{second.title()} {words[CITY_DAYS[second] - 1]}, so "
            f"{words[sum(CITY_DAYS[name] for name in (first, second)) - 1]} days in all with the "
            f"journey between them")
    if len(places) > 2 and places[2] in CITY_DAYS:
        text += f", and a day or two more for {places[2].title()}"
    return text + "."


def _full_days(count):
    words = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten")
    if count == 1:
        return "one full day"
    if count < len(words):
        return words[count - 1] + " full days"
    return str(count) + " full days"


def _stay_days(place):
    days = CITY_DAYS[place]
    words = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten")
    length = "One full day" if days == 1 else f"{words[days - 1].title()} full days"
    text = (f"{length} in {place.title()}, not counting the day you arrive or the day you fly "
            f"home: that covers the main sights at a normal pace, with time to sit down for lunch")
    if place in DAY_TRIPS:
        text += ", and a day more if you want one of the day trips"
    return text + "."


def _stay_there(memory, understood):
    clean = understood.get("clean", "")
    if _find_in(clean, CITY_DAYS):
        return None
    place = _place_in(memory, understood, CITY_DAYS)
    if not place or not _a_trip_to(place, memory, understood):
        return None
    return _stay_days(place)


def _adapter(memory, understood):
    clean = understood.get("clean", "")
    place = _place_in(memory, understood, PLUG_TYPES)
    if not place:
        return None
    letter, shape, note = PLUG_TYPES[place]
    if letter == "G":
        return (f"{place.title()} uses the same three square pins as the UK, so what you bring "
                f"from home fits. Take an adapter only for anything with a European plug on it, "
                f"and check that the voltage is the same, which it is in most of these places.")
    text = f"In {place.title()} the sockets are type {letter}, {shape}, so a UK plug needs an adapter"
    if note:
        text += ". " + note
    return text.rstrip(".") + (
        ". Phone and laptop chargers handle 100 to 240 volts; hairdryers and straighteners "
        "often do not, so look at the label before you pack them.")


_HILL = re.compile(r"\b(?:hike|hiking|hill|hills|mountain|mountains|fell|munro|ridge|trek|trekking|coast path|rambl"
                    r"|summit|peak|dales|moors?)\b")


def _city_pack(memory, understood):
    clean = understood.get("clean", "")
    if not re.search(r"\b(?:cold|winter|snow|snowing|freezing|december|january|february|"
                     r"november)\b", clean):
        return ("Take what you can walk in all day and layer: one pair of comfortable shoes, a "
                "warm mid-layer for the evening, a light waterproof you can fold into a bag, and "
                "a small day bag. One evening outfit is enough, plus a charger and your tickets.")
    return ("Pack for 2 to 8C, wind and rain: a waterproof coat with a hood, warm layers you can "
            "take off indoors, and shoes you can walk a hill in. It gets dark around 4pm in "
            "December, so a small torch and plans for the afternoon indoors help.")


def _hike_day(memory, understood):
    clean = understood.get("clean", "")
    if (re.search(r"\b(?:every day|everyday|daily|most days|each day)\b", clean)
            and not _HILL.search(clean)):
        return ""
    water = ("half a litre an hour of walking is the working rule, so two litres for a half day "
             "out and three or four for a full one, more in heat or on a climb, and carry it since "
             "a stream is not safe to drink but a tap or a cafe will fill you up")
    food = ("about 60g of carbohydrate an hour - sandwiches, oatcakes, nuts, dried fruit, a "
            "flapjack - eaten little and often rather than as one big lunch, with something salty "
            "for what you sweat out")
    if (not re.search(r"\b(?:how much|how many|how long)\b", clean)
            and re.search(r"\b(?:pack|packing|packed|bring|take|carry|wear|kit|bag|rucksack|backpack)\b",
                          clean)
            and re.search(r"\b(?:what|which|anything|need|should)\b", clean)):
        kit = ("Layers, a waterproof, and the water and food: base layer, fleece, a shell you "
               "can get into in the wind, spare socks; half a litre an hour, so two litres for a "
               "half day; 60g of carbohydrate an hour. Add a map or a charged phone with the "
               "route, a torch, hat and gloves, a blister kit, and a foil blanket.")
        if re.search(r"\b(?:pack|packing|packed|bring|carry|wear|kit|bag|rucksack|backpack)\b",
                     clean):
            return kit + " Leave the jeans and the cotton at home."
    if (re.search(r"\b(?:eat|eating|ate|food|snack|snacks|lunch|fuel|energy|hungry|"
                  r"carb|carbs|carbohydrate)\b", clean)
            and not re.search(r"\b(?:water|drink|drinking|liquid|litre|litres)\b", clean)):
        return (food[0].upper() + food[1:] + ". For the drink, " + water + ".")
    return (water[0].upper() + water[1:] + ". For food, aim at " + food + ".")


def _tap_water(memory, understood):
    clean = understood.get("clean", "")
    if re.search(r"\b(?:liquids|bottle|bottles|hand luggage|cabin bag|security|plane|flight|"
                 r"fountain|how much|more water|enough water|glasses|dehydrat|hot water|"
                 r"boil|watering|water the|water my|water it|water them|bill|leak|pressure|"
                 r"heater|plant|plants|houseplant|houseplants|leaves|leaf)\b", clean):
        return None
    if not re.search(r"\b(?:tap|safe|drink|drinking|ice|okay|ok|fine|stomach|ill)\b", clean):
        return None
    place = _place_in(memory, understood, WATER)
    city = None
    if not place:
        city = _place_in(memory, understood, CITY_COUNTRY)
        country = CITY_COUNTRY.get(city or "", "")
        if country in WATER:
            place = country
    if not place:
        if re.search(r"\b(?:abroad|holiday|holidays|trip|travelling|traveling|travel)\b", clean):
            return TAP_WATER_GENERAL
        if not re.search(r"\b(?:tap|taps|mains|bottled|safe|water company|water supply)\b", clean):
            return None
        if re.search(r"\b(?:brown|yellow|orange|rust|rusty|gritty)\b", clean):
            return TAP_WATER_HOME_BROWN
        if re.search(r"\b(?:smell|smells|smelled|taste|tastes|tasted|chlorine|metallic|"
                     r"lead|discoloured|discolored)\b", clean):
            return TAP_WATER_HOME_TASTE
        return TAP_WATER_HOME
    label = (city or place).title()
    if WATER[place]:
        return (f"Tap water in {label} is safe to drink: it is treated, the restaurants serve it, "
                f"and a refillable bottle saves money all week. Bottled is only worth it if the "
                f"plumbing in an old building makes the taste odd.")
    return (f"In {label}, drink bottled or filtered water, and skip the ice from street "
            f"stalls: the local water upsets visitors far more than locals. Use bottled for "
            f"brushing your teeth, and eat fruit you peel yourself for the first few days.")


_CLOCK_AFTER = re.compile(r"\b(?:at|is|by|around|about|for|before)\s+(\d{1,2})(?:[:.](\d{2}))?"
                          r"\s*(am|pm)?\b")
_CLOCK_MERIDIEM = re.compile(r"\b(\d{1,2})(?:[:.](\d{2}))?\s*(am|pm)\b")
_LENGTH_SAID = re.compile(r"\b(\d{1,2}|an?|one|two|three|four)\s*(?:hours?|hrs?)\b")
_LENGTH_MINS = re.compile(r"\b(\d{1,3})\s*(?:minutes?|mins?)\b")
_LEAVE_SAID = re.compile(
    r"\b(?:leave|leaves|leaving|left|set off|setting off|sets off|set out|head off|heads off|"
    r"drive|driving|coming from|get going)\b")
_FLIGHT_SAID = re.compile(
    r"\b(?:flight|flights|fly|flies|flying|departs?|departure|takes? off|take off|takeoff|"
    r"boarding|board|gate|landing|lands)\b")
_DRIVE_SAID = re.compile(
    r"\b(?:drive|driving|journey|taxi|cab|train|bus|tube|ride|commute|to the airport|"
    r"get to the airport|get there|from home|away|takes?)\b")
_SMALL_COUNT = {"one": 1, "two": 2, "three": 3, "four": 4}


def _clock_pairs(text):
    found, seen = [], set()
    for pattern in (_CLOCK_AFTER, _CLOCK_MERIDIEM):
        for match in pattern.finditer(text):
            hour, minute = int(match.group(1)), int(match.group(2) or 0)
            meridiem = (match.group(3) or "").lower()
            if hour > 23 or minute > 59 or (hour > 12 and not meridiem and not match.group(2)):
                continue
            if re.match(r"\s*(?:hours?|minutes?|mins?|days?|weeks?|nights?)\b",
                        text[match.end():]):
                continue
            key = (hour, minute, meridiem)
            if key in seen:
                continue
            seen.add(key)
            head = text[max(0, match.start() - 34):match.start()]
            tail = text[match.end():match.end() + 26]
            near_head = head[-16:]
            if _LEAVE_SAID.search(near_head) and not re.search(r"\b(?:miss|make|catch)\b",
                                                              near_head):
                role = "leave"
            elif _FLIGHT_SAID.search(near_head) or _FLIGHT_SAID.search(tail[:16]):
                role = "flight"
            else:
                role = "leave" if _nearest(_LEAVE_SAID, head, tail) >= 0 else "flight"
            if meridiem:
                hour = hour % 12 + (12 if meridiem == "pm" else 0)
            found.append({"hour": hour, "minute": minute, "meridiem": meridiem,
                          "role": role,
                          "sep": ":" if ":" in (match.group(0) or "") else "."})
    return found


def _nearest(pattern, head, tail):
    best = -1
    for match in pattern.finditer(head):
        distance = len(head) - match.start()
        if best < 0 or distance < best:
            best = distance
    for match in pattern.finditer(tail):
        distance = match.start() + 1
        if best < 0 or distance < best:
            best = distance
    return best


def _length_said(text):
    if re.search(r"\b(?:an?\s+hour|hour)\s+and\s+a\s+half\b", text):
        return 90
    if re.search(r"\bhalf\s+an?\s+hour\b", text):
        return 30
    hours = _LENGTH_SAID.search(text)
    if hours:
        word = hours.group(1)
        count = 1 if word in ("a", "an") else (int(word) if word.isdigit()
                                                 else _SMALL_COUNT.get(word, 0))
        if count:
            after = text[hours.end():hours.end() + 20]
            more = re.search(r"\b(?:and\s*)?(\d{1,2})\s*(?:minutes?|mins?)\b", after)
            return count * 60 + (int(more.group(1)) if more else 0)
    minutes = _LENGTH_MINS.search(text)
    if minutes:
        return int(minutes.group(1))
    return None


_NUMBER_WORD = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
                "ten", "eleven", "twelve")


def _long_said(minutes):
    if minutes < 60:
        return f"{minutes} minutes"
    hours, extra = divmod(minutes, 60)
    base = "an hour" if hours == 1 else f"{_NUMBER_WORD[hours - 1] if hours <= 12 else hours} hours"
    if not extra:
        return base
    if extra == 30:
        return ("an hour and a half" if hours == 1
                else f"{_NUMBER_WORD[hours - 1]} and a half hours")
    if extra == 15:
        return ("an hour and a quarter" if hours == 1
                else f"{_NUMBER_WORD[hours - 1]} and a quarter hours")
    return f"{base} and {extra} minutes"


def _at_a_time(clock, minutes):
    total = (int(clock["hour"]) * 60 + int(clock["minute"]) + minutes) % (24 * 60)
    return total // 60, total % 60


def _a_flight(clock_said, noun=""):
    digits = re.match(r"\d+", str(clock_said))
    hour = int(digits.group(0)) if digits else 0
    article = "an" if hour in (8, 11, 18) else "a"
    return f"{article} {clock_said}" + (f" {noun}" if noun else "")


def _a_clock(hour, minute, clock):
    if clock.get("meridiem"):
        return _clock(hour, minute)
    if clock.get("sep") == ":":
        return f"{hour % 24:02d}:{minute:02d}"
    tail = f".{minute:02d}" if minute else ""
    return f"{hour % 24 or 12}{tail}"


def _airport_early(memory, understood):
    clean = understood.get("clean", "")
    text = clean.lower()
    long_haul = re.search(r"\b(?:long haul|long-haul|transatlantic|usa|america|the states|"
                          r"canada|australia|new zealand|japan|china|asia|dubai|south africa|"
                          r"long flight)\b", text)
    bag = re.search(r"\b(?:checked bag|checked luggage|bag to check|suitcase|hold bag|"
                    r"check a bag|checked in bag|check my bag|check a suitcase|bag drop|"
                    r"hold luggage|check luggage)\b", text)
    hand = re.search(r"\b(?:hand luggage|cabin bag|carry on|carry-on|no bag|no luggage|"
                     r"hand baggage)\b", text)
    if long_haul:
        lead, lead_said = 180, "three hours before departure"
    elif hand and not bag:
        lead, lead_said = 90, "ninety minutes before departure"
    else:
        lead, lead_said = 120, "two hours before departure"
    if hand and not bag:
        closes = ("The gate closes 20 to 30 minutes before the flight, so being through security "
                  "45 minutes before it is the deadline that matters.")
        shuts = "The gate shuts 20 to 30 minutes before the flight."
    else:
        closes = ("The bag drop closes 45 to 60 minutes before the flight and the gate 20 to 30, "
                  "so the bag drop is the real deadline, not the departure time.")
        shuts = "Bag drop shuts 45 to 60 minutes before the flight and the gate 20 to 30."
    clocks = _clock_pairs(text)
    leaving = next((one for one in clocks if one["role"] == "leave"), None)
    flying = next((one for one in clocks if one["role"] != "leave"), None)
    drive = _length_said(text) if _DRIVE_SAID.search(text) else None
    says_before = re.search(r"(?:before|ahead of)\s+(?:my|the|our|a|departure|boarding)\b", text)
    planned = (None if drive is not None or not says_before
               else _length_said(text))
    if re.search(r"\b(?:land|lands|landing|arrive at the other|get in at)\b", text) and not \
            re.search(r"\b(?:airport|before|leave|early)\b", text):
        return ""
    if _FLIGHT_LENGTH_ASK.search(text):
        return _flight_length(memory, understood)
    if re.search(r"\b(?:connecting|connection|connections|layover|stopover|transit|"
                 r"change planes|changing planes)\b", text):
        if planned is not None:
            said = _long_said(planned)
            if planned >= 90:
                return (f"{said[0].upper() + said[1:]} at Heathrow is comfortable if both flights "
                        f"are on one ticket: the bag goes through and the walk and security again "
                        f"are 30 to 60 minutes. The shortest connection airlines sell there is 60 "
                        f"to 90 minutes.")
            return (f"{said[0].upper() + said[1:]} is under what I would want between flights at "
                    f"Heathrow: 60 to 90 minutes is the usual minimum on one ticket, and that "
                    f"leaves nothing for a late first leg. If the first flight is late the airline "
                    f"has to move you on, but only when both legs are on one booking.")
        return ("Allow 60 to 90 minutes at Heathrow between flights on one ticket, and two "
                "hours if they are separate bookings or you have to collect a bag and check it "
                "again. A "
                "late first leg is what breaks a connection, so one ticket is worth paying a "
                "little more for.")
    if re.search(r"\b(?:cancel|cancelled|canceled|cancelling|refund|refunds|compensation|"
                 r"delay|delayed|voucher)\b", text):
        return ""
    if re.search(r"\b(?:book|books|booking|booked|cheap|cheaper|cheapest|price|prices|"
                 r"fare|fares|deal|deals|cost)\b", text):
        return ""
    if re.search(r"\b(?:food|foods|snack|snacks|eat|eating|meal|meals|sandwich|sandwiches|"
                 r"lunch|picnic|drink|drinks)\b", text) and re.search(
            r"\b(?:take|bring|carry|pack|eat)\b", text):
        return ""
    if re.search(r"\b(?:cruise|ferry|ferries|boat|ship|train|trains|rail|eurostar|coach|"
                 r"bus|hotel|hostel|campsite|airport transfer|transfer)\b", text):
        return ""
    if not clocks and re.search(r"\b(?:miss|missed|missing|misses)\b.*\b(?:flight|plane)\b",
                               text) and re.search(
            r"\b(?:what happens|what do i do|missed|too late|no.?show|rebook|refund|claim|"
            r"compensation|rebooked)\b", text):
        return ""
    if re.search(r"\b(?:gate|gates|boarding)\b", text) and not re.search(
            r"\bboarding (?:pass|passes|card)\b", text):
        if flying is not None:
            shut = _a_clock(*_at_a_time(flying, -25), flying)
            board = _a_clock(*_at_a_time(flying, -40), flying)
            return (f"For {_a_flight(_a_clock(flying['hour'], flying['minute'], flying), 'flight')}"
                    f" the gate shuts about {shut} and boarding starts around {board}: be in the "
                    f"departure lounge before that, which means through security an hour ahead.")
        return ("Boarding starts about 40 minutes before departure and the gate shuts 20 to 30 "
                "minutes before it, so be through security and in the departure lounge an hour "
                "ahead. The gate's clock is the one that costs you the seat if you miss it.")
    if re.search(r"\bcheck(?:ing)?[ -]?in\b|\bcheckin\b", text) and not re.search(
            r"\b(?:what time should i leave|leave home)\b", text):
        if re.search(r"\bhow long\b", text) and re.search(r"\b(?:take|takes|queue|wait)\b",
                                                             text):
            return ("Ten to twenty minutes at the desk with your bag ready and the documents out, "
                    "and more like half an hour at six in the morning. The desk shuts 45 to 60 "
                    "minutes before departure, so the queue is not what makes you late.")
        return ("Check in online as soon as it opens - 24 to 48 hours before the flight at most "
                "airlines, and the pass appears in their app - and then the airport is only bag "
                "drop and security. The desk shuts 45 to 60 minutes before departure, and 90 "
                "minutes on some long-haul flights.")
    if planned is not None:
        said = _long_said(planned)
        if planned >= lead + 45:
            return (f"That is plenty: {lead_said} is the safe rule, so {said} leaves room for the "
                    f"bag queue and a coffee. {shuts}")
        if planned >= lead:
            return (f"That is about right: {lead_said} is the rule, and "
                    f"{'that' if planned == lead else said} works as long as the bag queue is "
                    f"short. {shuts}")
        if planned >= lead - 30:
            return (f"That is tight: {said} is under the {_long_said(lead)} I would allow, so a "
                    f"queue at the bags or at security is what makes you late. {shuts}")
        return (f"Too tight unless you have no bag to drop and a boarding pass already: {said} "
                f"leaves nothing for the queue at security, and {lead_said} is the safe rule. "
                f"{shuts}")
    if leaving is not None and flying is not None:
        road = drive if drive is not None else 30
        leave_at = leaving["hour"] * 60 + leaving["minute"]
        fly_at = flying["hour"] * 60 + flying["minute"]
        if not leaving["meridiem"] and flying["meridiem"]:
            while fly_at - leave_at - road > 12 * 60:
                leave_at += 12 * 60
            leaving = dict(leaving, hour=(leave_at // 60) % 24,
                           meridiem="am" if (leave_at // 60) % 24 < 12 else "pm")
        gap = fly_at - leave_at - road
        if gap < -720:
            gap += 24 * 60
        said_flight = _a_clock(flying["hour"], flying["minute"], flying)
        there = _a_clock(*_at_a_time(leaving, road), leaving)
        sides = (f"with {_long_said(road)} on the road" if drive is not None
                 else "with a half-hour drive")
        if gap >= lead + 60:
            earlier = _a_clock(*_at_a_time(flying, -(lead + road)), flying)
            return (f"You are early: leaving at "
                    f"{_a_clock(leaving['hour'], leaving['minute'], leaving)} {sides} puts you at "
                    f"the airport for {there}, {_long_said(gap)} before "
                    f"{_a_flight(said_flight, 'flight')}, so {earlier} would still be there "
                    f"{_long_said(lead)} ahead. {shuts}")
        if gap >= lead:
            return (f"That works: leaving at "
                    f"{_a_clock(leaving['hour'], leaving['minute'], leaving)} {sides} gets you "
                    f"there for {there}, {_long_said(gap)} before "
                    f"{_a_flight(said_flight, 'flight')}. {shuts}")
        if gap >= lead - 30:
            return (f"Cutting it fine: {there} is only {_long_said(gap)} before "
                    f"{_a_flight(said_flight, 'flight')} and I would allow {_long_said(lead)}. "
                    f"Leave half an hour earlier if you have a bag to drop. {shuts}")
        return (f"That is too late for {_a_flight(said_flight, 'flight')}: {there} leaves "
                f"{_long_said(gap)} at the airport, and bag drop shuts 45 to 60 minutes before "
                f"departure. Leave by "
                f"{_a_clock(*_at_a_time(flying, -(lead + road)), flying)} at the latest.")
    if leaving is not None:
        if drive is not None:
            there = _a_clock(*_at_a_time(leaving, drive), leaving)
            head = (f"Leaving at {_a_clock(leaving['hour'], leaving['minute'], leaving)} with "
                    f"{_long_said(drive)} on the road puts you at the airport for {there}, ")
        else:
            there = _a_clock(*_at_a_time(leaving, 30), leaving)
            head = (f"Leaving at {_a_clock(leaving['hour'], leaving['minute'], leaving)} puts you "
                    f"at the airport for {there} if the drive is about half an hour, ")
        suits = _a_clock(*_at_a_time(leaving, (drive if drive is not None else 30) + lead), leaving)
        return (f"{head}which is {_long_said(lead)} before {_a_flight(suits, 'flight')} - about "
                f"right. A "
                f"longer drive needs a later flight. {shuts}")
    if flying is not None:
        said = _a_clock(flying["hour"], flying["minute"], flying)
        there = _a_clock(*_at_a_time(flying, -lead), flying)
        if drive is not None:
            home = _a_clock(*_at_a_time(flying, -(lead + drive)), flying)
            return (f"For {_a_flight(said, 'flight')}, be at the airport by {there}: "
                    f"{lead_said} is the safe rule, and with {_long_said(drive)} on the road that "
                    f"means leaving home around {home}. {shuts}")
        home = _a_clock(*_at_a_time(flying, -(lead + 30)), flying)
        return (f"For {_a_flight(said, 'flight')}, be at the airport by {there}: "
                f"{lead_said} is the safe rule. Work back from that for the drive - half an hour "
                f"on the road means leaving home around {home}. {shuts}")
    if re.search(r"\b(?:leave home|leave the house|leave my house|leaving home|set off|"
                 r"set out|get going|need to leave|should i leave|when do i leave|"
                 r"leave for the airport|leaving for the airport|head off)\b", text):
        return (f"{lead_said[0].upper() + lead_said[1:]} at the airport, and the drive comes on "
                f"top: half an hour on the road means leaving home {_long_said(lead + 30)} before "
                f"the flight. {shuts}")
    return (f"{lead_said[0].upper() + lead_said[1:]} is the safe rule. {closes} "
            f"Add half an hour at a big airport in the early morning or on a Friday.")


FLIGHT_HOURS = {
    "ireland": 1.25, "france": 1.5, "belgium": 1.25, "netherlands": 1.25, "germany": 1.75,
    "switzerland": 1.75, "austria": 2, "italy": 2.5, "spain": 2.5, "portugal": 2.75,
    "croatia": 2.5, "greece": 4, "turkey": 4, "morocco": 3.5, "iceland": 3, "norway": 2,
    "sweden": 2.25, "denmark": 1.75, "finland": 3, "poland": 2.25, "czechia": 2, "hungary": 2.5,
    "egypt": 5, "dubai": 7, "south africa": 11, "india": 9, "thailand": 12, "china": 11,
    "japan": 12, "usa": 8, "america": 8, "canada": 8, "mexico": 11, "australia": 21,
    "new zealand": 25, "scotland": 1.25, "england": 1, "wales": 1,
    "northern ireland": 1.25, "jersey": 1, "guernsey": 1, "isle of man": 1, "luxembourg": 1.25,
    "slovenia": 2.5, "slovakia": 2.5, "estonia": 3, "latvia": 3, "lithuania": 3, "cyprus": 4.5,
    "malta": 3.25, "tunisia": 3, "albania": 3, "bulgaria": 3.25, "romania": 3.25,
    "cabo verde": 6, "cape verde": 6, "gambia": 6, "senegal": 6, "nigeria": 6.5, "ghana": 6.5,
    "kenya": 8.5, "tanzania": 9, "rwanda": 8.5, "uganda": 8.5, "ethiopia": 8, "namibia": 10.5,
    "zimbabwe": 11, "botswana": 11, "zambia": 11, "mozambique": 11, "madagascar": 12,
    "mauritius": 12, "seychelles": 10.5, "jamaica": 10, "barbados": 8.5, "antigua": 8.5,
    "st lucia": 8.5, "saint lucia": 8.5, "cuba": 9.5, "dominican republic": 9,
    "trinidad": 10, "bahamas": 9,
    "qatar": 6.5, "saudi arabia": 6.5, "bahrain": 6.5, "kuwait": 6.5, "oman": 7.5,
    "israel": 4.75, "jordan": 5, "lebanon": 4.5, "russia": 4,
    "sri lanka": 11.5, "maldives": 10.5, "nepal": 10.5, "pakistan": 8.5, "bangladesh": 10,
    "singapore": 13, "malaysia": 13, "hong kong": 12.5, "vietnam": 12, "cambodia": 12.5,
    "indonesia": 16, "philippines": 15, "south korea": 11.5, "taiwan": 13.5,
    "brazil": 11.5, "argentina": 13.5, "chile": 14.5, "peru": 12.5, "colombia": 10.5,
    "costa rica": 11.5, "panama": 11,
}
AIR_HOURS_CITY = {
    "florida": "usa", "california": "usa", "texas": "usa", "hawaii": "usa", "nevada": "usa",
    "new england": "usa", "new york": "usa", "new york city": "usa", "orlando": "usa",
    "miami": "usa", "key west": "usa", "las vegas": "usa", "los angeles": "usa",
    "san francisco": "usa", "boston": "usa", "chicago": "usa", "washington": "usa",
    "seattle": "usa", "denver": "usa", "new orleans": "usa", "san diego": "usa",
    "atlanta": "usa", "houston": "usa", "dallas": "usa", "philadelphia": "usa",
    "phoenix": "usa", "nashville": "usa", "austin": "usa", "honolulu": "usa",
    "toronto": "canada", "vancouver": "canada", "montreal": "canada", "calgary": "canada",
    "quebec": "canada", "banff": "canada", "nova scotia": "canada",
    "cancun": "mexico", "tulum": "mexico", "playa del carmen": "mexico", "los cabos": "mexico",
    "havana": "cuba", "montego bay": "jamaica", "kingston": "jamaica", "bridgetown": "barbados",
    "punta cana": "dominican republic", "nassau": "bahamas",
    "benidorm": "spain", "malaga": "spain", "alicante": "spain", "palma": "spain",
    "ibiza": "spain", "majorca": "spain", "mallorca": "spain", "menorca": "spain",
    "tenerife": "spain", "lanzarote": "spain", "fuerteventura": "spain",
    "gran canaria": "spain", "costa del sol": "spain", "valencia": "spain",
    "bilbao": "spain", "san sebastian": "spain", "granada": "spain", "cordoba": "spain",
    "girona": "spain", "murcia": "spain", "almeria": "spain", "cadiz": "spain",
    "santiago de compostela": "spain", "salou": "spain", "costa brava": "spain",
    "faro": "portugal", "algarve": "portugal", "madeira": "portugal", "funchal": "portugal",
    "lagos": "portugal", "coimbra": "portugal", "evora": "portugal", "sintra": "portugal",
    "azores": "portugal", "the azores": "portugal",
    "pisa": "italy", "bologna": "italy", "turin": "italy", "palermo": "italy",
    "catania": "italy", "sicily": "italy", "sardinia": "italy", "cagliari": "italy",
    "olbia": "italy", "verona": "italy", "sorrento": "italy", "amalfi": "italy",
    "capri": "italy", "positano": "italy", "taormina": "italy", "tuscany": "italy",
    "lake como": "italy", "genoa": "italy", "bari": "italy", "rimini": "italy",
    "matera": "italy", "lecce": "italy", "the dolomites": "italy", "dolomites": "italy",
    "corfu": "greece", "rhodes": "greece", "kos": "greece", "zakynthos": "greece",
    "kefalonia": "greece", "mykonos": "greece", "halkidiki": "greece",
    "thessaloniki": "greece", "heraklion": "greece", "chania": "greece", "zante": "greece",
    "skiathos": "greece", "skopelos": "greece", "naxos": "greece", "paros": "greece",
    "milos": "greece", "lefkada": "greece", "kalamata": "greece", "mykonos island": "greece",
    "antalya": "turkey", "dalaman": "turkey", "bodrum": "turkey", "marmaris": "turkey",
    "izmir": "turkey", "fethiye": "turkey", "side": "turkey", "belek": "turkey",
    "alanya": "turkey", "kusadasi": "turkey", "cappadocia": "turkey", "goreme": "turkey",
    "larnaca": "cyprus", "paphos": "cyprus", "limassol": "cyprus", "ayia napa": "cyprus",
    "protaras": "cyprus", "north cyprus": "cyprus", "valletta": "malta", "gozo": "malta",
    "sliema": "malta",
    "nice": "france", "lyon": "france", "marseille": "france", "bordeaux": "france",
    "toulouse": "france", "corsica": "france", "ajaccio": "france", "bastia": "france",
    "disneyland paris": "france", "cannes": "france", "antibes": "france",
    "avignon": "france", "montpellier": "france", "nantes": "france",
    "strasbourg": "france", "lille": "france", "grenoble": "france",
    "chamonix": "france", "biarritz": "france", "normandy": "france", "brittany": "france",
    "dordogne": "france", "provence": "france", "loire valley": "france",
    "saint tropez": "france", "monaco": "france",
    "pula": "croatia", "hvar": "croatia", "zagreb": "croatia", "rovinj": "croatia",
    "sibenik": "croatia", "makarska": "croatia", "trogir": "croatia", "korcula": "croatia",
    "brac": "croatia", "vis": "croatia",
    "amsterdam": "netherlands", "rotterdam": "netherlands", "the hague": "netherlands",
    "eindhoven": "netherlands", "utrecht": "netherlands", "brussels": "belgium",
    "bruges": "belgium", "ghent": "belgium", "antwerp": "belgium", "leuven": "belgium",
    "berlin": "germany", "munich": "germany", "frankfurt": "germany", "cologne": "germany",
    "hamburg": "germany", "dusseldorf": "germany", "stuttgart": "germany",
    "nuremberg": "germany", "dresden": "germany", "heidelberg": "germany",
    "bavaria": "germany", "black forest": "germany", "leipzig": "germany",
    "vienna": "austria", "salzburg": "austria", "innsbruck": "austria",
    "hallstatt": "austria", "graz": "austria", "kitzbuhel": "austria",
    "zurich": "switzerland", "geneva": "switzerland", "basel": "switzerland",
    "bern": "switzerland", "lucerne": "switzerland", "interlaken": "switzerland",
    "zermatt": "switzerland", "lausanne": "switzerland", "grindelwald": "switzerland",
    "st moritz": "switzerland", "davos": "switzerland",
    "dublin": "ireland", "cork": "ireland", "galway": "ireland", "shannon": "ireland",
    "belfast": "northern ireland", "edinburgh": "scotland", "glasgow": "scotland",
    "aberdeen": "scotland", "inverness": "scotland", "the highlands": "scotland",
    "isle of skye": "scotland", "skye": "scotland", "st andrews": "scotland",
    "london": "england", "manchester": "england", "cornwall": "england",
    "newquay": "england", "bristol": "england", "birmingham": "england",
    "liverpool": "england", "leeds": "england", "newcastle": "england",
    "york": "england", "bath": "england", "oxford": "england", "cambridge": "england",
    "the cotswolds": "england", "cotswolds": "england", "lake district": "england",
    "brighton": "england", "torquay": "england", "isle of wight": "england",
    "snowdonia": "wales", "pembrokeshire": "wales", "cardiff": "wales",
    "anglesey": "wales", "brecon beacons": "wales",
    "copenhagen": "denmark", "stockholm": "sweden", "gothenburg": "sweden",
    "helsinki": "finland", "rovaniemi": "finland", "lapland": "finland",
    "tromso": "norway", "stavanger": "norway", "akureyri": "iceland",
    "prague": "czechia", "budapest": "hungary", "krakow": "poland", "warsaw": "poland",
    "gdansk": "poland", "wroclaw": "poland", "bratislava": "slovakia",
    "tallinn": "estonia", "riga": "latvia", "vilnius": "lithuania",
    "bucharest": "romania", "sofia": "bulgaria", "varna": "bulgaria",
    "burgas": "bulgaria", "plovdiv": "bulgaria", "tirana": "albania",
    "ljubljana": "slovenia", "lake bled": "slovenia", "bled": "slovenia",
    "casablanca": "morocco", "fez": "morocco", "tangier": "morocco", "agadir": "morocco",
    "essaouira": "morocco", "rabat": "morocco", "cairo": "egypt",
    "sharm el sheikh": "egypt", "hurghada": "egypt", "luxor": "egypt",
    "tunis": "tunisia", "hammamet": "tunisia", "djerba": "tunisia", "sousse": "tunisia",
    "cape town": "south africa", "johannesburg": "south africa", "durban": "south africa",
    "nairobi": "kenya", "mombasa": "kenya", "zanzibar": "tanzania",
    "dar es salaam": "tanzania", "addis ababa": "ethiopia", "lagos": "nigeria",
    "accra": "ghana", "banjul": "gambia", "dakar": "senegal", "sal": "cape verde",
    "boa vista": "cape verde", "praia": "cape verde", "port louis": "mauritius",
    "windhoek": "namibia", "harare": "zimbabwe", "kigali": "rwanda",
    "abu dhabi": "dubai", "doha": "qatar", "riyadh": "saudi arabia",
    "jeddah": "saudi arabia", "muscat": "oman", "manama": "bahrain",
    "amman": "jordan", "petra": "jordan", "aqaba": "jordan", "tel aviv": "israel",
    "jerusalem": "israel", "eilat": "israel", "beirut": "lebanon",
    "osaka": "japan", "hiroshima": "japan", "sapporo": "japan", "okinawa": "japan",
    "seoul": "south korea", "busan": "south korea", "beijing": "china",
    "shanghai": "china", "macau": "hong kong", "taipei": "taiwan",
    "phuket": "thailand", "chiang mai": "thailand", "koh samui": "thailand",
    "krabi": "thailand", "pattaya": "thailand", "kuala lumpur": "malaysia",
    "penang": "malaysia", "langkawi": "malaysia", "borneo": "malaysia",
    "bali": "indonesia", "jakarta": "indonesia", "lombok": "indonesia",
    "hanoi": "vietnam", "ho chi minh city": "vietnam", "da nang": "vietnam",
    "hoi an": "vietnam", "siem reap": "cambodia", "phnom penh": "cambodia",
    "colombo": "sri lanka", "male": "maldives", "kathmandu": "nepal",
    "delhi": "india", "mumbai": "india", "goa": "india", "kerala": "india",
    "jaipur": "india", "agra": "india", "taj mahal": "india",
    "bangalore": "india", "chennai": "india", "kolkata": "india", "karachi": "pakistan",
    "islamabad": "pakistan", "lahore": "pakistan", "dhaka": "bangladesh",
    "brisbane": "australia", "perth": "australia", "adelaide": "australia",
    "cairns": "australia", "gold coast": "australia", "hobart": "australia",
    "auckland": "new zealand", "wellington": "new zealand", "christchurch": "new zealand",
    "queenstown": "new zealand", "rio de janeiro": "brazil", "sao paulo": "brazil",
    "buenos aires": "argentina", "santiago": "chile", "lima": "peru", "bogota": "colombia",
    "san jose": "costa rica", "panama city": "panama",
}
_FLIGHT_LENGTH_ASK = re.compile(
    r"\b(?:how long(?:'s| is) (?:the |a |my )?flight|how long does (?:the |a )?flight take|"
    r"how long to fly|how many hours (?:is|does|to) (?:a |the |my )?flight|"
    r"how many hours to fly|how long is the plane|is it a long flight|is it a long plane|"
    r"long flight to|flight time to|how long will (?:the |my )?flight take|"
    r"how long (?:does|do) it take to (?:fly|get)(?= to (?!the airport|an airport|the "
    r"terminal))|how long to fly to)\b")


_STARTS_AT = re.compile(
    r"\b(?:from|out of|leaving|leave|depart(?:ing)? from|fly out of|flown? out of)\s+$")


def _a_place_the_flight_starts_at(named, clean, memory):
    texts = [clean]
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in (turns or [])[-3:]:
        if isinstance(turn, dict):
            texts.append(str(turn.get("user") or "").lower())
    for text in texts:
        match = re.search(r"(.{0,24})\b" + re.escape(named), text)
        if match and _STARTS_AT.search(match.group(1)):
            return True
    return False


def _a_place_said_after(named, clean):
    return _find_in(clean.split(named, 1)[-1], AIR_HOURS_CITY)


def _the_destination_in_the_turns(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in reversed((turns or [])[-3:]):
        if not isinstance(turn, dict):
            continue
        found = _find_in(str(turn.get("user") or "").lower(), AIR_HOURS_CITY)
        if found and not _a_place_the_flight_starts_at(found, "", {"turns": [turn]}):
            return found
    return None


def _flight_length(memory, understood):
    clean = understood.get("clean", "") or ""
    named = _place_in(memory, understood, AIR_HOURS_CITY)
    if named and _a_place_the_flight_starts_at(named, clean, memory):
        named = (_a_place_said_after(named, clean)
                 or _place_in_the_plan(memory, AIR_HOURS_CITY)
                 or _the_destination_in_the_turns(memory))
    country = AIR_HOURS_CITY.get(named or "", "")
    if country in FLIGHT_HOURS:
        return _flight_hours_said(named.title(), FLIGHT_HOURS[country])
    city = _place_in(memory, understood, CITY_COUNTRY) or _place_in(memory, understood, CITIES)
    country = CITY_COUNTRY.get(city or "", "")
    if country in FLIGHT_HOURS:
        return _flight_hours_said(city.title(), FLIGHT_HOURS[country])
    place = _place_in(memory, understood, FLIGHT_HOURS)
    if place in FLIGHT_HOURS:
        return _flight_hours_said(place.title(), FLIGHT_HOURS[place])
    return ("The airline's timetable has the exact time, and the booking shows it to the minute. "
            "As a rule the air time is two to four hours across Europe, seven to eight to the "
            "east coast of America, and eleven to thirteen to Asia.")


def _flight_hours_said(name, hours):
    in_the_air = _long_said(int(hours * 60))
    if hours >= 20:
        return (f"To {name} it is {in_the_air} in the air from the UK even non-stop, and a day of "
                f"it with a stop: book a night flight if you can sleep on a plane, and the return "
                f"leg is longer still.")
    return (f"About {in_the_air} in the air from the UK to {name}, plus the airport at both ends, "
            f"so half a day door to door. The booking shows the exact time.")


def _my_flight_time(memory, understood):
    clean = understood.get("clean", "")
    if re.search(r"\b(?:land|lands|landing)\b", clean):
        return ("The landing time is on your ticket and in the airline's app, and it is the local "
                "time where you land rather than the time back home. It moves with the flight, so "
                "the live arrival time in the app is the one to trust on the day.")
    if re.search(r"\b(?:gate|terminal)\b", clean):
        return ("The gate and terminal are on your boarding pass and in the airline's app, and "
                "they can change on the day: the app and the departure boards after security are "
                "the "
                "ones to trust, and the gate is worth checking once more when you sit down.")
    told = _flight_told(memory)
    if told:
        clock, day = told
        said = _a_clock(clock["hour"], clock["minute"], clock)
        there = _a_clock(*_at_a_time(clock, -120), clock)
        return (f"You told me your flight is at {said}{day}, so be at the airport by {there}: two "
                f"hours before departure is the safe rule. The drive comes on top, so half an "
                f"hour on the road means leaving home at "
                f"{_a_clock(*_at_a_time(clock, -150), clock)}.")
    return ("I can't see your booking, so I can't look it up: the time is on your ticket and in "
            "the airline's app, in the local time of the airport you fly from. Tell me the time "
            "and I'll work back to when you need to leave.")


_DAY_SAID = re.compile(r"\b(?:on\s+)?(monday|tuesday|wednesday|thursday|friday|saturday|"
                       r"sunday|tomorrow|tonight|this morning|this evening)\b")


def _flight_told(memory):
    held = _the_plan_told(memory)
    if held:
        return held
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in reversed(list(turns or [])[-3:]):
        if not isinstance(turn, dict):
            continue
        said = str(turn.get("user") or "").lower()
        if not _FLIGHT_SAID.search(said):
            continue
        clock = next((one for one in _clock_pairs(said) if one["role"] == "flight"), None)
        if clock is None:
            continue
        day = _DAY_SAID.search(said)
        return clock, (f" on {day.group(1).title()}" if day else "")
    return None


def _the_plan_told(memory):
    user = memory.get("user") if isinstance(memory, dict) else None
    if not isinstance(user, dict):
        return None
    plans = user.get("plans")
    if not isinstance(plans, list):
        plans = [user.get("plan")]
    for plan in reversed([one for one in plans if isinstance(one, str) and one.strip()]):
        low = plan.lower()
        if not _FLIGHT_SAID.search(low):
            continue
        clock = next((one for one in _clock_pairs(low) if one["role"] == "flight"), None)
        if clock is None:
            continue
        day = _DAY_SAID.search(low)
        return clock, (f" on {day.group(1).title()}" if day else "")
    return None


def _clock(hour, minute=0):
    hanging = "am" if hour % 24 < 12 else "pm"
    twelve = hour % 12 or 12
    tail = f".{minute:02d}" if minute else ""
    return f"{twelve}{tail}{hanging}"


def _uk_summer(day=None):
    day = day or datetime.datetime.now(datetime.timezone.utc).date()
    if 4 <= day.month <= 9:
        return True
    if day.month in (3, 10):
        last = day.replace(day=28) + datetime.timedelta(days=4)
        last_sunday = last - datetime.timedelta(days=last.weekday() + 1)
        return day >= last_sunday if day.month == 3 else day < last_sunday
    return False


def _now_there(hours):
    here = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        hours=1 if _uk_summer() else 0)
    there = here + datetime.timedelta(hours=hours)
    return _clock(there.hour, there.minute), _clock(here.hour, here.minute)


_WHEN_IT_IS = re.compile(
    r"\b(?:what(?:'s|\s+is)?\s+the\s+time|what\s+time\s+is\s+it|whats\s+the\s+time|what\s+time\s+is\s+it\s+there|"
    r"the\s+time\s+(?:now|please|there)|got\s+the\s+time|have\s+you\s+got\s+the\s+time|"
    r"know\s+the\s+time|what\s+o'?clock|"
    r"(?:do|did|can|could|would)\s+you\s+(?:have|know|tell\s+me|give\s+me)\s+the\s+time|"
    r"tell\s+me\s+the\s+time)\b")
_TIME_OF_DAY = re.compile(
    r"\b(?:what|which)\s+time\s+(?:do|does|did|should|shall|will|would|can|could|must)\b|"
    r"\b(?:to|for)\s+(?:take|takes|"
    r"taking|go|going|leave|leaves|leaving|start|starts|starting|finish|finishes|finishing|end|ends|"
    r"ending|eat|eating|bed|sleep|sleeping|wake|waking|shut|shuts|shutting|open|opens|opening|"
    r"close|closes|closing|call|calling|ring|ringing)\b|\b(?:pills?|tablets?|medication|meds|dose|"
    r"insulin|appointment|kick\s*off|kickoff|sunrise|sunset|shift|bus|train|ferry|flight|meeting|"
    r"match|game|film|movie|show|class|lesson|interview|closes?|opens?)\b")


_HOW_OFTEN = re.compile(
    r"\b(?:all|most|half|some|much|none|part|lots?|a\s+lot|any)\s+(?:of\s+)?the\s+time\b", re.I)
_TIME_TO_DO_SOMETHING = re.compile(r"\bthe\s+time\s+to\s+\w+")
_clock_here_doc = None


def _the_clock_here(memory, understood):
    clean = understood.get("clean", "")
    if not _WHEN_IT_IS.search(clean):
        return None
    if _HOW_OFTEN.search(clean):
        return None
    if _TIME_TO_DO_SOMETHING.search(clean):
        return None
    if _TIME_OF_DAY.search(clean):
        return None
    if _place_in(memory, understood, TIME_ZONES) or _find_in(clean, MULTI_ZONES):
        return None
    here = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        hours=1 if _uk_summer() else 0)
    return (f"It is {_clock(here.hour, here.minute)} here, on the UK clock - if you are somewhere "
            f"else your own clock is the one to trust.")


_NOT_WHERE_ASKS = frozenset(("when", "how_long", "how_much", "how", "steps", "yesno", "why"))


def _asks_where(understood):
    asks = (understood or {}).get("asks") or ()
    return not any(ask in _NOT_WHERE_ASKS for ask in asks)


def _where_to_stay(memory, understood):
    if not _asks_where(understood):
        return None
    place = _place_in(memory, understood, CITY_AREA)
    if not place:
        return None
    return f"Stay in {CITY_AREA[place]}."


TOWN_STAY = (
    "Book close to the middle of town and a street or two back from the main road: the station, "
    "the food and the evening are then walkable, and the rooms just off the front are quieter and "
    "cheaper. At the seaside that means a street back from the front rather than the front itself. "
    "Look at the map for a bar or a through road under the window, check the last bus or train if "
    "you will be out late, and book somewhere with free cancellation so you can move if the area "
    "is not what you hoped.")


_NOT_WHERE_ASKS = frozenset(("when", "how_long", "how_much", "how", "steps", "yesno", "why"))


_A_CAR_NIGHT = re.compile(
    r"\b(?:in|inside)\s+(?:my|the|our|his|her)\s+(?:car|van|motorhome|camper|campervan|truck)\b"
    r"|\b(?:tent|camping|tourer|caravan|motorhome|campervan|camper)\b")


_A_SHIFT_WORK = re.compile(
    r"\bshift(?:s|work|work\s+pattern)?\b|\bon nights?\b|\bworking nights?\b|\bwork nights?\b"
    r"|\bnight\s*worker\b|\bday\s+shift\b")


_A_FLIGHT_WORD = re.compile(
    r"\b(?:airport|airports|terminal|flight|flights|flying|heathrow|gatwick|stansted|luton)\b")


_A_STAY_ASK = re.compile(
    r"\b(?:where|which)\b[^.!?]{0,30}\b(?:stay|staying|sleep|sleeping|kip|hotel|book|night)\b"
    r"|\b(?:hotel|hotels|place|somewhere|room)\b[^.!?]{0,25}\b(?:near|at|by|close to|around)\b"
    r"[^.!?]{0,20}\b(?:airport|terminal|heathrow|gatwick|stansted|luton)\b")


_A_STAY_PLACE_ASK = re.compile(
    r"\b(?:where|which)\b[^.!?]{0,30}\b(?:stay|staying|sleep|sleeping|kip|hotel|book|night)\b"
    r"|\b(?:area|place|somewhere|part of town|neighbourhood|neighborhood|district)\b[^.!?]{0,20}"
    r"\b(?:to stay|stay in|staying in|to sleep|for the night)\b"
    r"|\b(?:hotel|hotels|b&b|hostel|guest house|place|somewhere|room)\b[^.!?]{0,25}"
    r"\b(?:near|at|by|close to|around|in)\b[^.!?]{0,20}"
    r"\b(?:airport|terminal|heathrow|gatwick|stansted|luton|beach|sea|seafront|centre|center|"
    r"station|town|city|old town|harbour|marina|lake|coast)\b")


def _a_night_near_the_airport(understood):
    clean = (understood or {}).get("clean", "") or ""
    return bool(_A_STAY_ASK.search(clean))


def _a_town_stay(memory, understood):
    if _place_in(memory, understood, CITY_AREA):
        return None
    return TOWN_STAY


def _a_town_stay_line(understood):
    if any(ask in _NOT_WHERE_ASKS for ask in ((understood or {}).get("asks") or ())):
        return False
    if _A_FLIGHT_WORD.search((understood or {}).get("clean", "") or ""):
        return False
    if _A_CAR_NIGHT.search((understood or {}).get("clean", "") or ""):
        return False
    if _A_SHIFT_WORK.search((understood or {}).get("clean", "") or ""):
        return False
    if not _A_STAY_PLACE_ASK.search((understood or {}).get("clean", "") or ""):
        return False
    return _find_in(understood.get("clean", "") or "", CITY_AREA) is None


def _time_zone(memory, understood):
    clean = understood.get("clean", "")
    if re.search(r"\b(fly|flight|flying|flights|drive|driving|walk|walking|train|bus|queue|"
                 r"check in|checking|passport|shops|dinner|kick off|kickoff|lunch|sunrise|"
                 r"sunset|tablets|bed|check out|checkout)\b", clean):
        return None
    place = _place_in(memory, understood, TIME_ZONES)
    if place is None:
        wide = _find_in(clean, MULTI_ZONES)
        if wide is None:
            return None
        return f"{wide.title()} has more than one clock: {MULTI_ZONES[wide]}."
    winter, summer = TIME_ZONES[place]
    name = place.title()

    def size(hours):
        whole = int(abs(hours))
        word = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
                "eleven", "twelve", "thirteen", "fourteen")
        if abs(hours) != whole:
            return f"{word[whole - 1]} and a half hours"
        return f"{word[whole - 1]} hour" if whole == 1 else f"{word[whole - 1]} hours"

    gap = summer if _uk_summer() else winter
    given = re.search(r"\b(\d{1,2})(?:[:.](\d{2}))?\s*(am|pm)\b", clean)
    if given and re.search(r"\bhere\b", clean):
        hour = int(given.group(1)) % 12 + (12 if given.group(3) == "pm" else 0)
        minute = int(given.group(2) or 0)
        there_given = _clock(hour + int(gap), minute + (30 if gap % 1 else 0))
        return (f"{given.group(1)}{':' + given.group(2) if given.group(2) else ''}"
                f"{given.group(3)} here is {there_given} in {name}.")
    there, here = _now_there(gap)
    if winter == 0 and summer == 0:
        if place in ("uk", "the uk", "britain", "england", "scotland", "wales"):
            return f"It is {here} here, and the same clock in the UK."
        return (f"{name} runs on the same clock as the UK, so it is {there} there now and "
                f"{here} here.")
    asked_how_far = re.search(r"hours|difference|ahead|behind|zone", clean)
    if winter == summer:
        if asked_how_far:
            return (f"{name} is {size(winter)} {'ahead of' if winter > 0 else 'behind'} the UK all "
                    f"year, so it is {there} there now and {here} here.")
        return f"It is {there} in {name} now, and {here} here."
    if asked_how_far:
        return (f"{name} is {size(winter)} ahead of the UK in winter and {size(summer)} in summer, "
                f"because its clocks do not move when ours do: it is {there} there now and {here} "
                f"here.")
    way = "ahead of" if winter > 0 else "behind"
    return (f"It is {there} in {name} now, and {here} here: {name} is "
            f"{size(summer) if _uk_summer() else size(winter)} {way} us at the moment.")


BOOK_ASK = re.compile(r"\b(?:book|booking|booked|reserve|reserving|reservation)\b", re.I)
BOOK_NOT_THE_TRIP = re.compile(
    r"\b(?:restaurant|table|dinner|lunch|breakfast|meal|show|concert|gig|cinema|film|"
    r"appointment|doctor|dentist|haircut|taxi|cab|car|van|hire|tour|tickets? for)\b", re.I)
_LONG_MONTH = ("january", "february", "march", "april", "may", "june", "july", "august",
               "september", "october", "november", "december")


def _plan_month(memory):
    mine = memory.get("user") if isinstance(memory, dict) else None
    plan = str((mine or {}).get("plan") or "").lower()
    for name in sorted(MONTHS, key=len, reverse=True):
        if re.search(r"\b" + name + r"\b", plan):
            return _LONG_MONTH[MONTHS[name] - 1]
    return None


def _when_to_book(memory):
    window = ("six to eight weeks ahead for short-haul and two to four months for long-haul, "
              "with Tuesday and Wednesday usually the cheapest days to fly")
    month = _plan_month(memory)
    if not month:
        return "Book " + window + "."
    earlier = _LONG_MONTH[(MONTHS[month] - 3) % 12]
    return ("For a trip in " + month.title() + ", book by mid-" + earlier.title() + ": " + window
            + ".")


def _best_time(memory, understood):
    clean = understood.get("clean", "")
    if _WORTH_ASK.search(clean) and not any(_time_terms(clean, loose=True)):
        return None
    if BOOK_ASK.search(clean) and not BOOK_NOT_THE_TRIP.search(clean):
        return _when_to_book(memory)
    city = _place_in(memory, understood, WHEN_TO_GO)
    if city:
        return f"For {city.title()}: {WHEN_TO_GO[city]}"
    place = _place_in(memory, understood, BEST_TIME)
    if not place:
        return None
    return f"For {place.title()}: {BEST_TIME[place]}"

REGION_DAYS = {
    "cornwall": ("St Ives for the beach and the Tate, Padstow for the food and the Camel trail, "
                 "the Eden Project's two biomes near St Austell, the Minack theatre cut into the "
                 "cliff above Porthcurno, and Tintagel for the Arthur legend. The coast path "
                 "between St Ives and Padstow is the day out that beats all of them."),
    "devon": ("Dartmoor for the ponies and the tors, the South West Coast Path in either "
              "direction, Torquay and Paignton for the sand and the steam train to Dartmouth, "
              "and Exeter for the cathedral and the quay. Salcombe and Woolacombe are the two "
              "beaches people drive for."),
    "lake district": ("Windermere for the steamer and the low walks, Keswick for Catbells, which "
                      "is the best short climb in the country, Dove Cottage in Grasmere for the "
                      "Wordsworth, and the Honister pass for the slate mine. Scafell Pike is the "
                      "hill, and the Ullswater steamer is the easy day."),
    "norfolk": ("The Broads by boat from Wroxham, the seal trip from Blakeney Point, Holkham for "
                "the beach behind the pines, Sandringham if they like the royal houses, and "
                "Norwich for the cathedral and Elm Hill. Cromer for crab and the pier."),
    "yorkshire": ("Malham Cove and Gordale Scar in the Dales, Whitby for the abbey and the "
                  "Dracula steps, Robin Hood's Bay for the village at the bottom of the hill, "
                  "the North Yorkshire Moors railway from Pickering, and York for the Minster "
                  "and the Shambles."),
    "scotland": ("Edinburgh for the castle and Arthur's Seat, then the Highlands: Glencoe for "
                 "the glen, Skye for the Quiraing and the Fairy Pools, Glenfinnan for the "
                 "viaduct, and the Cairngorms for a hill day. A car is what makes it, since the "
                 "trains only reach the edges."),
    "wales": ("Snowdonia for Snowdon by the Pyg track and Betws-y-Coed for the slate, "
              "Pembrokeshire for the coast path and the beaches at Barafundle and Whitesands, "
              "and the Brecon Beacons for the waterfalls walk. Cardiff for the castle and the "
              "bay if the weather turns."),
    "peak district": ("Mam Tor and the Great Ridge for the classic day, Chatsworth for the "
                      "house and the garden, Dovedale for the stepping stones, and Bakewell for "
                      "the pudding. Edale is the station if you come by train."),
    "cotswolds": ("Bourton-on-the-Water for the river running through the village, Castle Combe "
                  "for the street everyone photographs, Chipping Campden and Broadway for the "
                  "stone, and the Slaughters for a walk between them. It is a place for driving "
                  "and stopping rather than one long walk."),
    "isle of wight": ("The Needles and Alum Bay, Shanklin and Ventnor for sand and the coastal "
                      "path, Carisbrooke Castle, and the cycle path that goes round the island. "
                      "It is small enough for a long weekend."),
    "dorset": ("The Jurassic Coast: Lulworth Cove and Durdle Door for the walk, Chesil Beach "
               "and Portland, Swanage for the steam train to Corfe Castle, and Studland for the "
               "sand. The fossil beaches are west of Charmouth."),
    "northumberland": ("Hadrian's Wall at Housesteads and Vindolanda, Alnwick Castle and the "
                       "garden, Bamburgh and its beach, and Lindisfarne across the causeway at "
                       "low tide. The dark skies park is the evening."),
}

REGION_BEACHES = {
    "cornwall": ("Porthmeor at St Ives for surf and a town behind it, Kynance Cove on the "
                 "Lizard for the water, and Sennen or Watergate Bay for space. Car parks are "
                 "full by ten in August, so go early or go in the evening."),
    "devon": ("Woolacombe for surf and sand that goes on, Blackpool Sands near Dartmouth for "
              "the shelter and the cafe, and Bantham for the walk to the village. The Exmouth "
              "end is sand and shallow, which is the one for small children."),
    "norfolk": ("Holkham for the pines and the space, Wells-next-the-sea for the beach huts "
                "and the pine walk, and Cromer for the pier and the crabs."),
    "yorkshire": ("Whitby for sand and the abbey above it, Robin Hood's Bay for rock pools at "
                  "low tide, and Filey for the long flat one that suits children."),
    "wales": ("Barafundle in Pembrokeshire for the walk down through the woods, Whitesands "
              "near St Davids for surf, and Tenby for a harbour and a town. The coast path "
              "links them if you want a leg of it."),
    "dorset": ("Studland for sand and the nature reserve behind it, Weymouth for the long "
               "shallow bay, and Charmouth for fossils at low tide after a storm."),
    "northumberland": ("Bamburgh for the castle above the sand, Embleton for the dunes, and "
                       "Alnmouth for a village at the end of the beach."),
    "isle of wight": ("Sandown and Shanklin for sand and a promenade, Compton Bay for surf "
                      "and the cliffs, and Bembridge for rock pools when the tide is out."),
}

REGION_NAMES = {
    "isle of wight": "on the Isle of Wight",
    "peak district": "the Peak District",
    "cotswolds": "the Cotswolds",
    "lake district": "the Lake District",
}


def _region_lead(region):
    named = REGION_NAMES.get(region)
    if named:
        return named[0].upper() + named[1:] if named.startswith("on") else f"In {named}"
    return f"In {region.title()}"


REGION_TOWNS = {
    "st ives": "cornwall", "padstow": "cornwall", "newquay": "cornwall",
    "falmouth": "cornwall", "penzance": "cornwall", "tintagel": "cornwall",
    "st austell": "cornwall", "kynance": "cornwall", "porthcurno": "cornwall",
    "torquay": "devon", "dartmouth": "devon", "salcombe": "devon", "woolacombe": "devon",
    "ilfracombe": "devon", "paignton": "devon", "dartmoor": "devon",
    "keswick": "lake district", "windermere": "lake district", "ambleside": "lake district",
    "coniston": "lake district", "grasmere": "lake district", "kendal": "lake district",
    "ullswater": "lake district",
    "cromer": "norfolk", "wroxham": "norfolk", "hunstanton": "norfolk",
    "blakeney": "norfolk", "holkham": "norfolk",
    "whitby": "yorkshire", "malham": "yorkshire", "ripon": "yorkshire",
    "scarborough": "yorkshire", "skipton": "yorkshire", "hawes": "yorkshire",
    "helmsley": "yorkshire",
    "highlands": "scotland", "skye": "scotland", "glencoe": "scotland",
    "fort william": "scotland", "inverness": "scotland", "oban": "scotland",
    "cairngorms": "scotland", "edinburgh": None,
    "snowdonia": "wales", "pembrokeshire": "wales", "brecon": "wales",
    "betws-y-coed": "wales", "barafundle": "wales", "anglesey": "wales",
    "mam tor": "peak district", "bakewell": "peak district", "buxton": "peak district",
    "dovedale": "peak district", "chatsworth": "peak district", "edale": "peak district",
    "bourton-on-the-water": "cotswolds", "castle combe": "cotswolds",
    "chipping campden": "cotswolds", "moreton-in-marsh": "cotswolds",
    "shanklin": "isle of wight", "ventnor": "isle of wight",
    "lulworth": "dorset", "durdle door": "dorset", "swanage": "dorset",
    "bamburgh": "northumberland", "alnwick": "northumberland",
    "lindisfarne": "northumberland", "housesteads": "northumberland",
}

REGION_TOWNS = {name: region for name, region in REGION_TOWNS.items() if region}

REGION_PLACES = dict({name: name for name in REGION_DAYS}, **REGION_TOWNS)

_DAYS_ASK = ("what should we do", "what should i do", "what can we do", "what is there to do",
             "whats there to do", "what is there", "whats there", "things to do", "thing to do",
             "things to see", "anything to do", "worth a visit", "worth visiting",
             "where should we go", "day trips", "day trip", "must see", "must do",
             "what to see", "what to do", "best beach", "best beaches", "good beach",
             "good beaches", "which beach", "a beach", "beaches", "beach")

_A_BEACH = re.compile(r"\bbeach(?:es)?\b", re.I)


def _region_days(memory, understood):
    clean = str((understood or {}).get("clean") or "").lower()
    if any(re.search(r"\b%s\b" % re.escape(name), clean) for name in MONTHS):
        return None
    named = _find_in(clean, REGION_PLACES)
    if not named:
        return None
    region = REGION_PLACES[named]
    if _A_BEACH.search(clean):
        return REGION_BEACHES.get(region)
    return f"{_region_lead(region)}: {REGION_DAYS[region]}"


_ARRIVAL_KINDS = ("station", "train station", "railway station", "coach station", "bus station",
                  "port", "ferry port", "terminal", "metro", "tram", "bus stop", "ferry",
                  "platform", "interchange", "land", "new city")

_ARRIVING_ASK = ("how do i get", "how do i go", "how to get", "how will i get", "best way",
                 "best to get", "get to my hotel", "get to the hotel", "to the hotel",
                 "to my hotel", "into town", "to the centre", "to the city centre", "city centre",
                 "to the town", "get to town", "where do i get", "is there a bus", "is there a train",
                 "is there a metro", "is there a tram", "is there a taxi", "how do i use",
                 "how do i plan", "get around", "getting around", "get round", "getting round",
                 "arrive at", "arriving at", "land at", "landing at", "which station",
                 "what station", "closest station", "nearest station", "which stop",
                 "last train", "last metro", "last bus", "travel card", "day ticket",
                 "how much is a taxi", "what does a taxi cost", "taxi cost", "taxi fare")

_ARRIVAL_LATE = ("late", "late at night", "night", "midnight", "dark", "after 10", "after 11",
                 "10pm", "11pm", "12pm", "1am", "00:", "22:", "23:")

_ARRIVAL_ABOUT = ("get around", "getting around", "get round", "getting round", "metro",
                  "tram", "subway", "underground", "bus pass", "travel card", "day ticket",
                  "metro card", "contactless", "how do i use", "how do i plan", "ticket machine")

_ARRIVAL_FARE_ASK = ("how much is a taxi", "what does a taxi cost", "taxi cost", "taxi fare",
                     "how much for a taxi", "what will a taxi cost")

_ARRIVAL_FARE = (
    "From the main station to the centre a taxi is usually 15 to 25 euros in a European city and "
    "5 to 15 in a smaller town, and the official rank outside the main exit charges the meter or "
    "the fixed fare: check the posted figure or the app price before you get in. The metro, tram "
    "or express bus is 2 to 5 euros for the same trip, so take that with a case you can wheel and "
    "keep the taxi for a late arrival or a lot of luggage.")

_ARRIVAL_PICK = ("which station", "what station", "closest station", "nearest station",
                 "which stop", "closest to", "nearest to", "closest one")

_ARRIVAL_TOWN = (
    "From the main station, take the metro, tram or airport-style express bus and leave the taxi "
    "for the "
    "cases and the late hour: in most European cities the ride from the main station to the centre "
    "is 2 to 5 euros and a taxi is 15 to 25. Buy the ticket at the machine or on the app before "
    "you board, walk to the official rank outside the main exit rather than taking an offer from "
    "someone inside, and have the address written down or on the phone screen.")

_ARRIVAL_LATE_NOTE = (
    "Check the last metro or bus before you travel - in most cities it is between half eleven and "
    "half twelve - and if it has gone, take the rank outside the station or ring the hotel and ask "
    "them to book a car, rather than getting in with someone who offers. Tell the hotel you will "
    "be late so they hold the room and give you the door code, and keep 20 euros of cash on you "
    "for the ride.")

_ARRIVAL_ABOUT_NOTE = (
    "Tap a contactless bank card or your phone if the city takes it, and you pay the local fare "
    "with no ticket to buy or validate; otherwise get a day or three-day travel card from the "
    "machine, which usually pays off after three or four rides. Validate the ticket or tap in at "
    "the start of every journey, because an unvalidated one counts as no ticket, and keep the same "
    "card for the way back so the daily cap applies.")

_ARRIVAL_PICK_NOTE = (
    "Pick the station named for the part you are staying in - the old town, the centre, the "
    "harbour - rather than the city's biggest one, and put both on a route planner before you "
    "book: the walk from the door to the hotel is the figure that decides it. A station with the "
    "city name plus a district in its name is usually the one closest to the old town.")


_FARES_ASK = ("cheap", "cheaper", "cheapest", "advance", "railcard", "save money", "save on",
              "best price", "cheapest way to", "how much is a train ticket",
              "how much are train tickets", "how much is a rail ticket")
_FARES_GOING_SOMEWHERE = ("to the centre", "to the city centre", "city centre", "into town",
                          "to the town", "to the hotel", "to my hotel", "from the station",
                          "from the airport", "which station", "what station", "last train",
                          "last metro", "last bus", "get to my hotel", "get to the hotel")


def _arriving(memory, understood):
    clean = (understood.get("clean") or "").lower()
    if any(w in clean for w in _FARES_ASK) and not any(w in clean for w in _FARES_GOING_SOMEWHERE):
        return None
    if "airport" in clean or "flight" in clean or "fly" in clean:
        return None
    if any(k in clean for k in _ARRIVAL_FARE_ASK):
        return _ARRIVAL_FARE
    if any(k in clean for k in _ARRIVAL_PICK):
        return _ARRIVAL_PICK_NOTE
    if any(k in clean for k in _ARRIVAL_ABOUT):
        return _ARRIVAL_ABOUT_NOTE
    if any(k in clean for k in _ARRIVAL_LATE):
        return _ARRIVAL_LATE_NOTE
    return _ARRIVAL_TOWN

_AIRPORT_TO_THE_AIRPORT = (
    "to the airport", "to the airport for", "for an early flight", "early flight", "early morning "
    "flight", "get to the airport", "getting to the airport", "airport in the morning",
    "before my flight", "before an early flight", "at 5am", "at 6am", "at 4am")
_AIRPORT_CHEAPEST = ("cheapest", "cheaper", "cheap way", "budget", "least expensive", "save money",
                     "cheapest way")
_AIRPORT_FASTEST = ("best way", "quickest", "fastest", "easiest", "best", "quick")
_AIRPORT_TRAIN = ("is there a train", "train from", "train to", "metro", "subway", "rail",
                  "is there a bus", "bus from", "underground")
_AIRPORT_HOTEL = ("my hotel", "the hotel", "hotel from", "to the hotel")
_AIRPORT_PORT = ("the port", "to the port", "cruise port", "cruise", "the ship", "my ship",
                 "to the ship")

_AIRPORT_WAY_IN = (
    "Check the airport's own website before you fly, on its 'to and from the airport' page: it lists "
    "the official ways into the centre with the price and the running time, which saves guessing at "
    "a machine after a flight. In most cities the train or metro is the quickest and cheapest way in, "
    "so follow the signs for trains or rail rather than the taxi rank; the airport bus or shuttle is "
    "cheaper and slower, and a taxi is the most expensive and the easiest with luggage or after dark. "
    "Buy the ticket before you board, and ignore anyone inside the terminal offering a taxi.")
_AIRPORT_CHEAPEST_REPLY = (
    "The cheapest way in is nearly always the train, the metro or the airport bus, and which of the "
    "three depends on the airport: its own 'to and from' page lists every option with the price, and "
    "it is worth a look before you fly. If the train or metro goes near where you are staying, take "
    "it; if not, take the bus to the main station and carry on from there. A taxi is the last choice "
    "for the money, and the most expensive thing you can do is accept a lift from someone who "
    "approaches you inside the terminal.")
_AIRPORT_FASTEST_REPLY = (
    "Fastest is the train or metro where there is one, because a taxi sits in the same traffic as "
    "everyone else: an airport express train, where a city has one, is quickest of all for a few "
    "euros more, and the metro is close behind. Take a taxi only if you land late, have heavy bags, "
    "or the railway does not run at that hour - and then the official rank or a car booked on an app, "
    "not anyone offering you a ride indoors.")
_AIRPORT_TRAIN_REPLY = (
    "Most big airports have a train or metro into the centre, and the airport's own website says so "
    "under 'to and from the airport', with the platform, the price and the last train of the night - "
    "check that last one before you book a late flight. Where there is a station sign, follow it: it "
    "is almost always cheaper than a taxi, and the ride is usually 15 to 40 minutes. Smaller airports "
    "run a bus to the nearest station instead, and a few have no rail link at all, in which case the "
    "shuttle bus or the official taxi rank is the way in.")
_AIRPORT_HOTEL_REPLY = (
    "Use the hotel's own directions, because they name the station or stop nearest the door and "
    "hotels write that down better than anyone: an email to them gets you the answer before you fly. "
    "Then take the train or bus into the centre and walk from the station, or hop in a short taxi from "
    "there if it is far. A taxi all the way from the airport is the easiest with luggage, so check the "
    "price first and take it from the official rank.")
_AIRPORT_PORT_REPLY = (
    "A cruise port is usually some way from the airport, and the simple answer is the transfer the "
    "cruise line sells: it is priced per person and it waits for the plane if the flight is late, "
    "which no taxi will. If you would rather make your own way, the port's own website lists the "
    "terminal and the local buses, and a taxi is worth it if there are two or more of you with "
    "luggage - agree the price before you get in, because port taxis know you have a ship to catch.")
_AIRPORT_EARLY_REPLY = (
    "Sort the journey the night before rather than on the morning: at 5am the first train often has "
    "not started, so it is a taxi booked in advance, a lift, or a hotel at the airport, and an airport "
    "hotel is worth its price for a flight before about 7am. Work backwards from the departure time - "
    "be there two hours before a short-haul flight and three before a long-haul one, add the journey, "
    "and let the drive take 30 minutes more than the map says at that hour. Check the night rate and "
    "any drop-off charge when you book, because both cost more at that time.")
_AIRPORT_SLEEP_REPLY = (
    "It is allowed in most airports and nobody minds, but be ready for it: the seats before security "
    "are the bright, busy ones, and the quiet corners are past security, which you cannot reach until "
    "check-in opens. For a layover over four hours a pod or an airport hotel is worth the money, and "
    "for a short one a hoodie or a scarf as a pillow, an eye mask, and something to drink gets you a "
    "couple of hours. Keep your bag looped round an arm, set two alarms, and find out where your gate "
    "is before you settle.")


def _airport_without_a_city(understood):
    words = [str(word).lower() for word in (understood.get("words") or ())]
    text = " ".join(words)

    def has(options):
        return any(option in words or option in text for option in options)

    if "to the airport" in text or "to the terminal" in text:
        if "from the airport" not in text:
            return None
    if has(_AIRPORT_PORT):
        return _AIRPORT_PORT_REPLY
    if has(_AIRPORT_HOTEL):
        return _AIRPORT_HOTEL_REPLY
    if has(_AIRPORT_CHEAPEST):
        return _AIRPORT_CHEAPEST_REPLY
    if has(_AIRPORT_TRAIN):
        return _AIRPORT_TRAIN_REPLY
    if has(_AIRPORT_FASTEST):
        return _AIRPORT_FASTEST_REPLY
    return _AIRPORT_WAY_IN


def _airport(memory, understood, general=True):
    clean = understood.get("clean", "")
    place = _place_in(memory, understood, AIRPORT_TRANSFER)
    if not place and "airport" in clean:
        for name in sorted(AIRPORT_TRANSFER, key=len, reverse=True):
            if name.replace(" airport", "") in clean:
                place = name
                break
    if not place:
        return _airport_without_a_city(understood) if general else None
    return f"From {place.title()}: {AIRPORT_TRANSFER[place]}"


_TAXI_TROUBLE = ("scam", "scammed", "ripped", "rip off", "rip-off", "overcharged", "overcharge",
                 "meter", "rigged", "cheat", "cheated")

_TAXI_WARNING = ("Use the official rank at the airport rather than anyone who approaches you inside, "
                 "and check the app price or the posted fare before you get in. Insist on the meter, "
                 "or agree the total first, and keep small notes so you are not waiting for change.")


def _taxi_abroad(memory, understood):
    clean = understood.get("clean") or ""
    if any(word in clean for word in _TAXI_TROUBLE):
        return _TAXI_WARNING
    return _airport(memory, understood, general=False) or _TAXI_WARNING


def _city_airport(memory, understood):
    city = _place_in(memory, understood, AIRPORT_NAME)
    if not city:
        return None
    return AIRPORT_NAME[city]

def _two_places(clean):
    names = sorted({name for pair in ROUTE_BETWEEN for name in pair}, key=len, reverse=True)
    return [name for name in names if re.search(r"\b%s\b" % re.escape(name), clean)]


def _route_between(memory, understood):
    names = _two_places(understood.get("clean", ""))
    for first in names:
        for second in names:
            if first == second:
                continue
            for pair in ((first, second), (second, first)):
                if pair in ROUTE_BETWEEN:
                    return ROUTE_BETWEEN[pair]
    return None


def _get_to(memory, understood):
    clean = understood.get("clean", "")
    for place in sorted(GET_TO, key=len, reverse=True):
        if re.search(r"\b%s\b" % re.escape(place), clean):
            return GET_TO[place]
    return None


SITE_WORDS = tuple(sorted(set(SITE_NOTES) | set(SITE_ALIASES), key=len, reverse=True))


def _site_note(memory, understood):
    clean = understood.get("clean", "")
    for site in SITE_WORDS:
        if re.search(r"\b%s\b" % re.escape(site), clean):
            return SITE_NOTES[SITE_ALIASES.get(site, site)]
    return None


def _day_trip(memory, understood):
    city = _place_in(memory, understood, DAY_TRIPS)
    if not city:
        return None
    return f"Day trips from {city.title()}: {DAY_TRIPS[city]}"


def _clauses(line):
    pieces, piece, depth = [], "", 0
    text = " " + line + " "
    at = 0
    while at < len(text):
        word = text[at]
        depth += (word == "(") - (word == ")")
        if word == "," and depth <= 0:
            pieces.append(piece)
            piece = ""
            at += 1
            continue
        join = text[at:at + 5].lower()
        if join == " and " and depth <= 0:
            after = text[at + 5:at + 30].strip(" ,").lower()
            after = " ".join(after.split()[:2])
            if any(after == name or after.startswith(name + " ")
                   for name in DAY_TRIP_PLACES):
                pieces.append(piece)
                piece = ""
                at += 5
                continue
        piece += word
        at += 1
    pieces.append(piece)
    tidy = []
    for piece in pieces:
        piece = re.sub(r"^\s*(?:and|plus)\s+", "", piece).strip(" ,")
        if piece:
            tidy.append(piece)
    return tidy


def _day_trip_clause(line, place):
    pieces = _clauses(line)
    for place_at, piece in enumerate(pieces):
        if not re.search(r"(?<![a-z])" + re.escape(place) + r"(?![a-z])", piece.lower()):
            continue
        said = piece
        for more in pieces[place_at + 1:]:
            if " for " in said.lower() or "(" in said:
                break
            said += " and " + more
        return said
    return ""


def _place_named_in_the_chat(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return None
    for turn in reversed(turns[-2:]):
        if not isinstance(turn, dict):
            continue
        place = _find_in(str(turn.get("user") or "").lower(), DAY_TRIP_PLACES)
        if place:
            return place
    return None


def _day_trip_place(memory, understood):
    clean = understood.get("clean", "")
    way = re.search(r"\bhow (?:do|can|would|should) (?:i|we|you) get\b|\bhow to get\b"
                    r"|\bhow far\b|\bhow long does it take\b", clean)
    place = _find_in(clean, DAY_TRIP_PLACES)
    if not place and way:
        place = _place_named_in_the_chat(memory)
    if not place:
        return None
    city = DAY_TRIP_PLACES[place]
    in_hand = _place_in(memory, understood, CITIES) or _place_in_the_plan(memory, CITIES)
    if in_hand and in_hand != city:
        return None
    first, _, rest = DAY_TRIPS[city].partition(". ")
    clause = _day_trip_clause(first, place)
    if not clause:
        return None
    how_long = re.search(r"\(([^)]*)\)", clause)
    if way and not how_long:
        return _without_the_season(f"Day trips from {city.title()}: {DAY_TRIPS[city]}",
                                   _when_said(memory, understood))
    if way:
        journey = how_long.group(1).split(",")[0].strip()
        if " from " in journey.lower():
            said = f"{place.title()}: {journey}."
        else:
            said = f"{place.title()}: {journey} from {city.title()}."
    else:
        said = f"Day trips from {city.title()}: {clause}."
    if rest and not way and not re.search(r"\b(bus|coach|car|drive|ferry)\b", clause):
        said += " " + rest
    return _without_the_season(said, _when_said(memory, understood))


TRANSIT_CARDS = {
    "oyster card": "london",
    "navigo easy": "paris",
    "navigo card": "paris",
    "suica card": "tokyo",
    "pasmo card": "tokyo",
    "octopus card": "hong kong",
    "opal card": "sydney",
    "presto card": "toronto",
    "myki card": "melbourne",
    "clipper card": "san francisco",
    "t-money card": "seoul",
    "nol card": "dubai",
    "andante card": "porto",
    "viva viagem": "lisbon",
    "ov-chipkaart": "amsterdam",
    "icoca card": "osaka",
    "charliecard": "boston",
    "ventra card": "chicago",
    "compass card": "vancouver",
    "metrobus card": "madrid",
}

_TRANSIT_WORDS = ("get around", "getting around", "get about", "getting about", "get round",
                  "getting round", "around town", "metro", "subway", "underground", "tube",
                  "u-bahn", "tram", "trams", "bus", "buses", "public transport", "transport",
                  "transit", "travelcard", "travel card", "day pass", "metro card",
                  "how do i travel", "how do people travel", "contactless", "top up",
                  "chipkaart", "oyster", "ticket")

CITY_TELLS = {"the tube": "london", "london underground": "london", "tube station": "london"}

CARD_WORDS = ("travel card", "travelcard", "day pass", "metro card", "transit card", "oyster",
              "pass for the", "weekly pass", "monthly pass", "tap in", "contactless")

CARD_NAMES = ("travel card", "travelcard", "day pass", "metro card", "transit card",
              "oyster card", "oyster", "weekly pass", "monthly pass", "tap in")

GENERAL_CARD = ("The rule is the same in most cities: tap a contactless bank card or your phone "
                "if the system takes one, because it charges the cheapest fare and usually caps "
                "the day, and if it does not, buy the stored-value card at a machine in the "
                "station - Oyster in London, Navigo in Paris, Suica in Tokyo. Compare a day or "
                "three-day pass with single tickets before you buy one: it only wins if you make "
                "several journeys a day, and the machines take a card, not always cash.")

_TRANSIT_NOT = ("airport", "flight", "flights", "fly", "flying", "booking", "book a", "hotel",
                "day trip", "day trips", "day out", "worth visiting", "best time", "rent a car",
                "hire a car", "car hire", "parking", "taxi from", "uber from")


def _transit(memory, understood):
    clean = understood.get("clean", "")
    if any(word in clean for word in _TRANSIT_NOT):
        return None
    if not any(word in clean for word in _TRANSIT_WORDS) and not _find_in(clean, TRANSIT_CARDS):
        return None
    city = _place_in(memory, understood, CITY_TRANSIT)
    if not city:
        city = _place_in_the_plan(memory, CITY_TRANSIT)
    if not city:
        city = _find_in(clean, TRANSIT_CARDS)
        city = TRANSIT_CARDS[city] if city else None
    if not city:
        tell = _find_in(clean, CITY_TELLS)
        city = CITY_TELLS[tell] if tell else None
    if not city or city not in CITY_TRANSIT:
        if _find_in(clean, CARD_WORDS):
            return GENERAL_CARD
        return None
    return f"In {city.title()}: {CITY_TRANSIT[city]}"


def _already_guided(memory, city):
    turns = memory.get("turns") or []
    guide = (CITIES.get(city) or "")[:40].lower()
    for turn in turns:
        if not isinstance(turn, dict):
            continue
        if guide and guide in (turn.get("bot") or "").lower():
            return True
    return False


def _asked_for_the_guide_before(memory, city, clean):
    body = (CITIES.get(city) or "")[:40].lower()
    for turn in memory.get("turns") or []:
        if not isinstance(turn, dict):
            continue
        said = (turn.get("user") or "").lower()
        if not said:
            continue
        if _find_in(said, CITIES) != city:
            continue
        if body and body in (turn.get("bot") or "").lower():
            return True
    return False


def _guided_off_a_question(memory, city):
    body = (CITIES.get(city) or "")[:40].lower()
    for turn in memory.get("turns") or []:
        if not isinstance(turn, dict):
            continue
        said = (turn.get("user") or "").lower().strip()
        if not said or _find_in(said, CITIES) != city:
            continue
        if not (_A_QUESTION_OPENS.match(said) or "?" in said):
            continue
        if body and body in (turn.get("bot") or "").lower():
            return True
    return False


DETAIL_PARTS = (
    (("food", "eat", "eating", "dinner", "lunch", "breakfast", "restaurant", "restaurants",
      "meal", "meals", "drink", "drinks", "bar", "bars", "tapas", "coffee", "market",
      "markets", "nightlife", "club", "clubs"),
     ("food", "eat", "eating", "dinner", "lunch", "breakfast", "restaurant", "restaurants",
      "meal", "meals", "drink", "drinks", "bar", "bars", "tapas", "coffee", "market",
      "markets", "nightlife", "club", "clubs")),
    (("museum", "museums", "gallery", "galleries", "art", "arts", "sight", "sights",
      "sightseeing", "see", "visit", "castle", "cathedral", "ruins", "history", "park"),
     ("museum", "museums", "gallery", "galleries", "art", "sights", "castle", "cathedral",
      "colosseum", "palace", "abbey", "church", "park", "view", "walk")),
    (("shop", "shops", "shopping", "buy", "souvenir", "souvenirs", "present", "presents"),
     ("shop", "shops", "shopping", "market", "markets", "souvenir", "souvenirs")),
)


ASKING_ONLY = frozenset("""see sight sights sightseeing visit visited miss anything something
somewhere worth goto go""".split())
_EATING_WORDS = frozenset(DETAIL_PARTS[0][0])


def _detail_line(city, clean):
    words = set(clean.split())
    if words & _EATING_WORDS and city in CHEAP_EATS:
        return CHEAP_EATS[city]
    for asked, said in DETAIL_PARTS:
        if not (words & set(asked)) - ASKING_ONLY:
            continue
        for sentence in CITIES[city].split(". "):
            if set(sentence.lower().split()) & set(said):
                sentence = sentence.rstrip(".")
                return f"In {city.title()}: {sentence}."
    return None


_A_QUESTION_OPENS = re.compile(
    r"^\s*(?:and\s+|so\s+|but\s+)?(?:what|how|where|when|which|who|why|can|could|should|"
    r"would|do|does|did|is|are|was|were|will|any|tell|recommend|suggest|give|show)\b")


WHICH_FIRST = re.compile(
    r"\bwhat\b[^.?!]{0,30}\b(?:see|do|visit)\b[^.?!]{0,20}\bfirst\b"
    r"|\bwhere (?:should|shall|do|would) (?:i|we) (?:start|begin)\b"
    r"|\bfirst thing (?:to (?:see|do)|i should|we should)\b"
    r"|\bwhat(?:'s| is) the first thing\b", re.I)


_IN_A_CITY = re.compile(r"^\s*in ([a-z][a-z .'-]{1,20}):", re.I)


def a_city_card_is_in_front(card):
    found = _IN_A_CITY.match(str(card or ""))
    if not found:
        return False
    return found.group(1).strip().lower() in CITIES


WHICH_ONE_FIRST = re.compile(r"\b(?:see|do|visit)\b[^.?!]{0,20}\bfirst\b", re.I)

_A_PLACE_OPENS = ("the ", "a ", "an ", "one ", "two ", "three ", "some ", "my ", "your ")


def asks_which_one_first(text):
    return bool(WHICH_ONE_FIRST.search(str(text or "")))


def _the_first_thing(city):
    sights = CITIES.get(city) or ""
    head = sights.split(". ")[0].rstrip(".")
    items = [part.strip() for part in head.split(",") if part.strip()]
    items = [part[4:] if part.lower().startswith("and ") else part for part in items]
    if not items:
        return None
    rest = f", then {items[1]}" if len(items) > 1 else ""
    first = items[0]
    if first[:1].isupper() or first.lower().startswith(_A_PLACE_OPENS):
        return f"Start with {first}{rest}."
    return f"{first[:1].upper() + first[1:]}{rest}."


def _about_city(city, memory, clean, understood=None):
    if WHICH_FIRST.search(clean):
        first = _the_first_thing(city)
        if first:
            return first
    detail = _detail_line(city, clean)
    if detail:
        return detail
    if _already_guided(memory, city):
        if (understood is not None and not understood.get("asks")
                and not _A_QUESTION_OPENS.match(clean)):
            return "In %s: %s" % (city.title(),
                                  _without_the_season(CITIES[city],
                                                      _when_said(memory, understood or {})))
        next_thing = _the_next_card_about(city, memory, clean)
        if next_thing:
            return next_thing
        return None
    return f"In {city.title()}: {CITIES[city]}"


MORE_PLACES = frozenset("""trip trips else other others another further afield nearby outside
countryside around surrounding surroundings excursion excursions""".split())


SEEING = frozenset("see seeing saw sight sights sightseeing visit visiting visited miss "
                   "missed seen".split())


def _wants_more_places(clean):
    words = set(clean.split())
    if words & MORE_PLACES:
        return True
    return bool(re.search(r"\bday\s+(?:trip|trips|out)\b", clean))


def _the_stay_is_long(memory, city):
    fills = CITY_DAYS.get(city, 3)
    for turn in memory.get("turns") or []:
        if not isinstance(turn, dict):
            continue
        said = (turn.get("user") or "").lower()
        days = next((count for phrase, count in sorted(TRIP_UNITS, key=lambda item: -len(item[0]))
                     if phrase in said), None)
        if days is None:
            more = re.search(r"\b(\d{1,2}|%s)\s+(?:days|nights)\b"
                             % "|".join(_NUMBER_WORD), said)
            if more:
                word = more.group(1)
                days = int(word) if word.isdigit() else _NUMBER_WORD.index(word) + 1
        if days and days >= max(2, 2 * fills):
            return True
    return False


def _said_in_this_chat(memory, text):
    head = text[:40].lower()
    for turn in memory.get("turns") or []:
        if isinstance(turn, dict) and head and head in (turn.get("bot") or "").lower():
            return True
    return False


def _the_next_card_about(city, memory, clean):
    place = CITY_COUNTRY.get(city, city)
    cards = []
    areas = (f"In {city.title()}: by area, {CITY_AREA[city]}." if city in CITY_AREA else None)
    day_trips = (f"Day trips from {city.title()}: {DAY_TRIPS[city]}"
                 if city in DAY_TRIPS else None)
    if _wants_more_places(clean) or _the_stay_is_long(memory, city):
        cards += [day_trips, areas]
    elif set(clean.split()) & SEEING:
        cards += [areas, day_trips]
    else:
        cards += [day_trips, areas]
    if city in CITY_TRANSIT:
        cards.append(f"In {city.title()}: {CITY_TRANSIT[city]}")
    if city in WHEN_TO_GO:
        cards.append(f"For {city.title()}: {WHEN_TO_GO[city]}")
    elif place in BEST_TIME:
        cards.append(f"For {city.title()}: {BEST_TIME[place]}")
    if city in CITY_CLIMATE and city in CLIMATES:
        cards.append(f"For {city.title()}: {CLIMATES[CITY_CLIMATE[city]]}")
    if city in DAILY_BUDGET:
        low, high, note = DAILY_BUDGET[city]
        cards.append(f"{city.title()} is about \u00a3{low} to \u00a3{high} a day per person on the "
                     f"ground, room aside. {note[0].upper() + note[1:]}.")
    for card in cards:
        if card and not _said_in_this_chat(memory, card):
            return card
    return None


def _guide_followup(memory, understood):
    clean = understood.get("clean", "")
    if _find_in(clean, CITIES):
        return None
    if not any(mark in clean for mark in FOLLOW_MARKS):
        return None
    city = _place_in(memory, understood, CITIES)
    if not city and SIGHTSEEING_ASK.search(clean):
        city = _the_place_held(memory)
    if not city:
        return None
    if (_already_guided(memory, city) and SIGHTSEEING_ASK.search(clean)
            and _guided_off_a_question(memory, city)):
        return f"In {city.title()}: {CITIES[city]}"
    return _about_city(city, memory, clean, understood)


SIGHTSEEING_ASK = re.compile(
    r"\b(?:what|which|where)\s+(?:should|could|can|must|do)\s+(?:i|we|you)\s+"
    r"(?:see|visit|not miss)\b"
    r"|\bwhat(?:'s| is| are)\s+worth\s+seeing\b"
    r"|\bwhat(?:'s| is| are)\s+there\s+to\s+(?:see|visit)\b")


def _the_place_held(memory):
    held = (memory.get("user") or {}).get("places") if isinstance(memory, dict) else None
    if isinstance(held, list) and held:
        newest = " ".join(str(held[-1] or "").lower().split())
        if newest in CITIES:
            return newest
    return _city_they_are_going_to(memory)


def _guide_next(memory, understood):
    clean = understood.get("clean", "")
    if len([word for word in clean.split() if word.isalpha()]) > 8:
        return None
    if _find_in(clean, CITIES):
        return None
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return None
    last = turns[-1] if isinstance(turns[-1], dict) else {}
    said = str(last.get("bot") or "").lower()
    for city in CITIES:
        if f"in {city}:" in said:
            return _about_city(city, memory, clean, understood)
    city = _city_they_are_going_to(memory)
    if not city and SIGHTSEEING_ASK.search(clean):
        city = _the_place_held(memory)
    if city and not _already_guided(memory, city):
        return f"In {city.title()}: {CITIES[city]}"
    if city:
        return _about_city(city, memory, clean, understood)
    return None


GOING_TO_A_PLACE = re.compile(
    r"\b(?:going|go|off|heading|fly(?:ing)?|flying|travell?ing|trip|holiday|weekend|break|"
    r"visiting|visit|staying|renting|booked|booking|flight)\b"
    r"|\b(?:\d+|a|an|one|two|three|four|five|six|seven|eight|nine|ten|a\s+few|a\s+couple\s+of)\s+"
    r"(?:days?|nights?|weeks?|weekends?|fortnight)\b")


def _city_they_are_going_to(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return None
    for turn in reversed(turns[-2:]):
        if not isinstance(turn, dict):
            continue
        said = str(turn.get("user") or "").lower()
        city = _find_in(said, CITIES)
        if city and GOING_TO_A_PLACE.search(said):
            return city
    return None


_CARRY_MONEY = ("Take two cards from different banks and a little local cash, and always pay in the "
                "local currency when the terminal offers to convert you - the \"pay in pounds\" "
                "option adds 3 to 5%. Use a bank ATM rather than a currency kiosk, and tell your "
                "bank you are travelling if it still asks.")

_KEEP_SAFE = ("Split it, so one loss is not the whole trip: a card and a day's cash on you, a second "
              "card in the hotel safe or packed separately, and a note of both card numbers and "
              "your bank's lost-card number somewhere offline. Carry a small amount in a front "
              "pocket or a zipped bag rather than a back pocket, use bank ATMs in daylight, and a "
              "money belt only if you will really wear it. If a card goes, freeze it in the app "
              "and ring the bank straight away, and check the phone before you fly: roaming on, "
              "a roaming pass for that country, and the bank app logged in, because that is how "
              "most of us pay now.")

_CARRY_SHORT = ("Take two cards from different banks and a little local cash, and pay in the local "
                "currency when the terminal offers to convert you.")


def _money_abroad(memory, understood):
    clean = (understood.get("clean") or "").lower()
    if re.search(r"\b(?:safe|safely|safety|stolen|theft|pickpocket|pickpockets|money belt|"
                 r"robbed|lose|lost|keep (?:my )?(?:money|cash|card))\b", clean):
        return _KEEP_SAFE
    if re.search(r"\bhow much\b", clean):
        rate = _trip_budget(memory, understood)
        if rate:
            return rate + " " + _CARRY_SHORT
    return _CARRY_MONEY


def _trip_budget(memory, understood):
    import re as _re
    clean = understood.get("clean", "")
    cost_word = _re.search(r"\b(?:how much|cost|costs|costing|expensive|pricey|afford|budget|"
                           r"spend|spending|will that|does that|go far|saved|money|cheap|"
                           r"inexpensive|affordable)\b", clean)
    if _re.search(r"\b(?:flight|flights|fly|flying|hotel|hotels|accommodation|apartment|"
                  r"villa|hostel|ticket|tickets|deal|deals|package|insurance|car hire)\b", clean):
        return None
    quality = _re.search(r"\b(?:warm|cold|hot|good|bad|big|small|deep|strong|quick|fast|early|"
                         r"late|cheap|safe|close|near|light|heavy|bright|tall|old|fit|well|"
                         r"soon|long|clear|loud|quiet|tidy)\s+enough\b", clean)
    amount = _re.search(r"[\u00a3$\u20ac]|\b\d{2,}\b", clean)
    if not cost_word and not amount and (quality or not _re.search(r"\benough\b", clean)):
        return None
    if not cost_word and not amount and _re.search(
            r"\b(?:days|nights|how long|too long|too short)\b", clean):
        return None
    place = _place_in(memory, understood, DAILY_BUDGET)
    if not place:
        return None
    days = next((count for phrase, count in sorted(TRIP_UNITS, key=lambda item: -len(item[0]))
                 if phrase in clean), None)
    low, high, note = DAILY_BUDGET[place]
    if days is None:
        return (f"{place.title()} is about \u00a3{low} to \u00a3{high} a day per person on the "
                f"ground, room aside. {note[0].upper() + note[1:]}.")
    low_total, high_total = low * days, high * days
    amount = next((int(m.replace(",", "")) for m in _re.findall(r"\d[\d,]*", clean)
                   if 50 <= int(m.replace(",", "")) <= 20000), None)
    if amount is None:
        return (f"{days} days in {place.title()} usually costs about \u00a3{low_total} to "
                f"\u00a3{high_total} per person on the ground, room aside. "
                f"{note[0].upper() + note[1:]}.")
    if amount >= high_total:
        verdict = "That is comfortable"
    elif amount >= low_total:
        verdict = "That works if you are careful"
    else:
        verdict = "That is tight"
    return (f"{verdict}: {days} days in {place.title()} usually costs about \u00a3{low_total} to "
            f"\u00a3{high_total} per person on the ground, room aside, and you have "
            f"\u00a3{amount}. {note[0].upper() + note[1:]}.")


def _month_in_the_chat(memory):
    user = memory.get("user") if isinstance(memory, dict) else None
    texts = []
    if isinstance(user, dict):
        texts.append(str(user.get("the_plan") or ""))
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if isinstance(turns, list):
        for turn in reversed(turns[-4:]):
            if isinstance(turn, dict):
                texts.append(str(turn.get("user") or ""))
    for text in texts:
        text = text.lower()
        found = next((number for name, number in sorted(MONTHS.items(), key=lambda item: -len(item[0]))
                      if name in text), None)
        if found:
            return found
    return None


def _weather(memory, understood):
    clean = understood.get("clean", "")
    city = (_find_in(clean, CITY_CLIMATE) or _place_in(memory, understood, CITY_CLIMATE)
            or _place_in_the_plan(memory, CITY_CLIMATE))
    month = next((number for name, number in sorted(MONTHS.items(), key=lambda item: -len(item[0]))
                  if name in clean), None)
    if month is None:
        month = _month_in_the_chat(memory)
    if not city or not month:
        return None
    low, high = CLIMATES[CITY_CLIMATE[city]][month]
    name = next((word for word, number in sorted(MONTHS.items(), key=lambda item: -len(item[0]))
                 if number == month and len(word) > 3), "May")
    return (f"{name.title()} in {city.title()} is usually about {low} to {high}C, and I can't see a "
            f"live forecast from here. Take a layer either way: evenings are cooler than the "
            f"afternoon, and a light rain jacket covers most days.")


def _cheap_trains(memory, understood):
    text = understood.get("clean") or ""
    if re.search(r"\brail ?cards?\b", text):
        return ("A railcard costs about £30 and takes a third off most fares, so it pays for itself "
                "in two or three trips. Get the one for your age or your area (a Two Together card "
                "covers two named people travelling together) and load it as a digital card in the "
                "train company app.")
    return ("Book as early as you can: advance singles usually go on sale about twelve weeks ahead "
            "and are the cheapest fares. Travelling off-peak (in the UK, after 9:30am) avoids the "
            "peak price, a railcard pays for itself in a couple of trips, and a split-ticket site "
            "can cut the fare further by buying the same journey as two shorter tickets.")


def _suitcase_protect(memory, understood):
    text = (understood.get("clean") or "").lower()
    broken = ("broke", "broken", "cracked", "damaged", "snapped", "torn", "ripped",
              "came back", "came off", "fell off")
    keeping = ("how do i keep", "keep it from", "from being", "stop", "prevent", "protect",
               "avoid", "not get", "without")
    if any(word in text for word in broken) and not any(word in text for word in keeping):
        return ("If the airline did it, report it at the baggage desk before you leave the airport "
                "and photograph the damage there: the report number is what a claim needs, and "
                "under the Montreal rules the airline pays for repair or replacement. If it broke "
                "at home, a luggage repair shop fits new wheels, straps and zip pulls for far less "
                "than a new case.")
    return ("Do not fill it until it splits: a zip bursts from the inside, so leave a hand's width "
            "of give and put the heavy things at the wheel end. A luggage strap takes the strain "
            "off the zip, a hard shell or a padded cover protects what is fragile, and anything "
            "breakable goes in the middle wrapped in clothes. Photograph it open and closed before "
            "check-in, because that is what an airline asks for when you claim for the damage.")


def _flight_extras(memory, understood):
    text = (understood.get("clean") or "").lower()
    if "legroom" in text or "leg room" in text or "exit row" in text:
        return ("Extra legroom earns its money on a flight over about four hours, or if you are "
                "tall; on a two-hour hop it buys very little. An exit row has the most space of all, "
                "but the seat next to you may not recline, the bags have to go in the overhead "
                "locker, and you have to be able and willing to open the door and help - so read the "
                "airline's rules before you pay.")
    if "priority" in text or "speedy" in text:
        return ("Priority boarding is worth paying for when you are travelling with only a cabin "
                "bag on a full flight: it gets you on early enough to find space overhead, and a bag "
                "that gets gate-checked is one you wait for at the carousel at the other end. With a "
                "checked bag in the hold there is nothing to win, so keep the money.")
    return ("Choosing your seat is worth paying for when you are travelling with somebody and want "
            "to sit together, or you want a window to sleep against; most airlines seat a child next "
            "to a parent for free, so a family does not need to buy it. On a short flight with an "
            "aisle seat left over anyway, save the money.")


def _passport_lost(memory, understood):
    text = understood.get("clean") or ""
    if any(phrase in text for phrase in ("last year", "years ago", "a while ago", "long ago")) \
            or re.search(r"\b(?:19|20)\d{2}\b", text):
        return ("A passport reported lost stays cancelled even if it turns up, so you can't fly on "
                "it. Apply for a new one now and ask for an urgent appointment if the trip is "
                "close; take your old passport number and a police report if you have one.")
    return ("Report it to the local police and get a written report, then contact your embassy or "
            "consulate for an emergency travel document. Take the police report, a passport photo "
            "and any copy of the old passport. In most of Europe this takes a day or two; tell your "
            "airline and travel insurer as well, and keep the report for the insurance claim.")


_CABIN_RULES = (
    (r"\b(?:power banks?|batter(?:y|ies)|lithium|vapes?|e-?cigarettes?)\b",
     "Power banks and spare batteries go in the cabin bag and never in the hold, with the "
     "terminals taped or each one in its own bag; a vape goes in the cabin too, and its liquid "
     "has to fit in the 100ml bag."),
    (r"\b(?:laptops?|tablets?|ipads?|kindle|phones?|mobiles?|cameras?|hairdryers?|straighteners?|"
     r"chargers?|headphones?|e-?readers?)\b",
     "Electronics are fine in the cabin bag: a laptop, tablet, phone, camera, charger or "
     "hairdryer all go through security, though the laptop comes out of the bag into its own "
     "tray. A lithium battery is the only part that matters, and it stays with you in the cabin."),
    (r"\b(?:wine|beer|spirits|alcohol|whisky|whiskey|gin|vodka|rum)\b",
     "In the cabin bag only 100ml is allowed, so a bottle of wine goes in the suitcase, or buy it "
     "in the duty-free shop after security and keep the receipt and the sealed bag for the "
     "connection. Check your destination's duty-free allowance before you buy more than a couple."),
    (r"\b(?:disposable razors?|razors?|shaving|shave|shaver)\b",
     "A disposable or cartridge razor is fine in the cabin bag; loose blades are not, since they "
     "have to be in a cartridge, and a cut-throat razor goes in the hold."),
    (r"\b(?:scissors|scissor|nail scissors|craft scissors)\b",
     "Scissors are allowed in the cabin bag with blades under 6cm, which covers nail and most "
     "small craft scissors; a longer pair goes in the hold."),
    (r"\b(?:tweezers|nail clippers|clippers|nail file)\b",
     "Tweezers and nail clippers are fine in the cabin bag - they are on nobody's banned list."),
    (r"\b(?:knife|knives|penknife|pen knife|pocket knife|swiss army|multi ?tool|blades?)\b",
     "A knife or penknife is not allowed in the cabin: any blade over 6cm, and every folding "
     "pocket knife, goes in the hold, and a multi-tool with a blade goes with it. A blade that "
     "matters to you is worth putting in the suitcase rather than arguing at the tray."),
    (r"\b(?:corkscrew|bottle opener|waiter.s friend)\b",
     "A corkscrew is not allowed in the cabin bag in the UK, and a bottle opener with a blade on "
     "it is the same thing to a scanner: both go in the hold."),
    (r"\b(?:screwdrivers?|tools?|hammer|spanner|wrench|pliers|drill bits?|allen keys?)\b",
     "Tools go in the hold: a screwdriver, pliers, a spanner or a hammer will be taken off you at "
     "security. A small screwdriver for glasses is usually let through, but pack it rather than "
     "count on it."),
    (r"\b(?:lighters?|matches|lighter fluid|zippo)\b",
     "One disposable lighter can go on you, not in the cabin bag and not in the hold; matches are "
     "one small box on you. Lighter fuel and refillable lighters with fuel in them are not allowed "
     "at all, so leave them at home."),
    (r"\b(?:deodorant|perfume|aftershave|toothpaste|shampoo|shower gel|sun ?cream|sunscreen|"
     r"hand gel|hand sanitiser|make ?up|moisturiser|hairspray|spray|contact lens solution)\b",
     "Anything liquid, gel, paste or aerosol - deodorant, perfume, toothpaste, sun cream - has to "
     "go in the 100ml clear bag, so buy the travel size or decant it into a small bottle. A "
     "roll-on and a solid stick are not liquids and are easier to carry."),
    (r"\b(?:food|sandwiches?|snacks?|fruit|bananas?|apples?|oranges?|cheese|cake|chocolate|"
     r"biscuits?|crisps|nuts|chewing gum|sweets|milk|baby milk|breast milk)\b",
     "Food is fine in the cabin bag - sandwiches, fruit, cheese, cake, even a banana. Only "
     "liquids are limited, so a yoghurt or a drink still has to be 100ml, and there is a bin "
     "before security for anything over."),
    (r"\b(?:liquid|liquids|toiletries|100ml|100 ml)\b",
     "Only containers of 100ml or less, all fitting in one clear plastic bag, can go through "
     "security. Fill an empty bottle after security, or ask for water on the plane."),
    (r"\b(?:water bottles?|bottles?|water|drinks?|juice|squash)\b",
     "A bottle is fine through security as long as it is empty: fill it at a fountain after the "
     "checkpoint, or ask for water on the plane."),
)
_CABIN_NOT_ALLOWED = (
    "{yes}knives and penknives, tools, scissors with blades over 6cm, a corkscrew, more than "
    "100ml of liquid, lighters with fuel in them, and fireworks or flammables. Clothes, books, "
    "food, chargers and a laptop all go in the cabin bag. Power banks and spare batteries are the "
    "other way round - cabin bag only, never the hold. The rules are set per country, so a long "
    "connection is worth checking, and the airline's own page lists what it will not carry."
)
_CABIN_YES = ("Yes, unless it is one of the short banned list: ", "")
_CABIN_LIST = ("What is banned is a short list: ", "Below is the short banned list: ")
_IN_THE_HOLD_ITSELF = (
    "A bag goes in the hold as your checked bag: 20 to 23kg is the usual limit, and it is around "
    "£20 to £45 each way if you book it online with the ticket rather than at the desk. Keep the "
    "power banks, spare batteries and anything with a lithium cell in the cabin bag, not the hold."
)
_IN_THE_HOLD = (
    "In the suitcase it can go: the hold has no 100ml rule and no blade rule, and it is the cabin "
    "bag that is searched. Pack it so it cannot move - clothes round it, nothing sharp against the "
    "shell - and keep batteries, power banks and anything with a lithium cell out of the hold."
)


def _cabin_named(text):
    for pattern, sentence in _CABIN_RULES:
        if re.search(pattern, text):
            return sentence
    return None


def _cabin_guard(understood):
    text = (understood.get("clean") or "").lower()
    if re.search(r"\b(?:pack|packs|packing|packed)\b", text) and not _cabin_named(text):
        return False
    return True


_A_PAY_ASK_AT_HOME = re.compile(
    r"\bhow\s+much\s+(?:will|would|should|do|does|did)\s+(?:i|we)\s+(?:take|bring)\s+home\b"
    r"|\b(?:will|would|do|does|did)\s+(?:i|we)\s+(?:take|bring)\s+home\b"
    r"|\b(?:take|bring)\s+home\s+(?:mean|means|pay|after\s+tax|before\s+tax|net|gross)\b"
    r"|\bwhat\s+(?:does|do)\s+(?:that\s+|it\s+)?(?:mean\s+for\s+)?(?:my\s+|the\s+)?"
    r"(?:take|bring)\s+home\b"
    r"|\bwhat\s+does\s+(?:\w+\s+){0,4}mean\b.{0,24}\b(?:take|bring)s?\s+home\b"
    r"|\bmean\s+for\s+my\s+(?:take|bring)\s+home\b"
    r"|\b(?:take|bring)\s+home\s+(?:meaning|definition|defined)\b"
    r"|\bwhat\s+is\s+(?:my\s+|the\s+|a\s+)?(?:take|bring)\s+home\b"
    r"|\b(?:explain|define|meaning\s+of)\s+(?:the\s+|my\s+|a\s+)?(?:take|bring)\s+home\b"
    r"|\b(?:i|we)\s+(?:take|bring|takes|brings|took|brought)\s+home\s+"
    r"(?:\d|\u00a3|about|around|roughly|nearly)\b", re.I)
_A_GOODS_WORD = re.compile(
    r"\b(?:wine|wines|beer|beers|spirits|whisky|whiskey|vodka|gin|rum|alcohol|"
    r"cigarettes?|cigs?|tobacco|baccy|perfume|gifts?|presents?|souvenirs?|chocolates?|"
    r"coffee|tea|clothes|booze)\b", re.I)
_A_CUSTOMS_WORD = re.compile(
    r"\b(?:duty[- ]free|customs|allowance|allowances|limit|limits|declare|declaring|declared|"
    r"red\s+channel|green\s+channel|border|airport|abroad|overseas|back\s+from|home\s+from|"
    r"france|spain|portugal|greece|italy|ireland|germany|holland|belgium)\b", re.I)


def _not_a_wage(understood):
    text = (understood.get("clean") or "")
    if not _A_PAY_ASK_AT_HOME.search(text):
        return True
    return bool(_A_GOODS_WORD.search(text) or _A_CUSTOMS_WORD.search(text))


GUARD_FOLDS = {"duty-free": _not_a_wage}


def _cabin_rules(memory, understood):
    text = (understood.get("clean") or "").lower()
    if re.search(r"\bhow (?:much|many)\b.{0,20}\b(?:liquid|liquids|water|drink|drinks|ml)\b",
                 text):
        return FLIGHT_LIQUIDS
    if re.search(r"\bhow (?:much|many|big|large|heavy)\b.{0,30}\b(?:luggage|baggage|bags?|"
                 r"cabin bag|kilos?|kg|weight)\b", text):
        return ""
    if re.search(r"\b(?:take (?:it |them |my \w+ )?out|out at security|out of my bag|"
                 r"out of the bag)\b", text):
        return ""
    named = _cabin_named(text)
    if named and named.startswith(("Power banks", "In the cabin bag only 100ml")):
        return named
    hold = re.search(r"\b(?:suitcase|hold|checked bag|checked in luggage|checked luggage|"
                     r"holdall)\b", text)
    if hold and not named:
        return _IN_THE_HOLD_ITSELF
    if hold:
        return _IN_THE_HOLD
    if named:
        return named
    banned = re.search(r"\bnot allow|banned|prohibit|forbidden|cannot take|can.t take|"
                       r"not take|what can.t i|what can i not|what am i not", text)
    if banned:
        return _CABIN_NOT_ALLOWED.format(yes=_CABIN_LIST[0])
    if re.search(r"\b(?:cabin bag|cabin bags|hand luggage|hand baggage|carry ?on|carry ?ons|"
                 r"luggage|baggage|backpack|suitcase|bag)\b", text):
        return ""
    return _CABIN_NOT_ALLOWED.format(yes=_CABIN_YES[0])


_MONTH_PICKS = {
    "january": (
        "the Canaries for 20C and real sun, the Alps for snow, or Seville for a city break in "
        "warmth, and the first week of January is the cheapest week of the year to fly"),
    "february": (
        "the Canaries or Cape Verde for proper sun, Venice for carnival, or Marrakesh for 20C "
        "days, and half term is the one week to book around"),
    "march": (
        "Marrakesh or Seville at about 20C, Rome and Florence before the queues start, or "
        "Lanzarote for reliable sun"),
    "april": (
        "Lisbon or Andalusia at 20C, Sicily before the heat arrives, or the tulips in the "
        "Netherlands, and Easter moves the prices"),
    "may": (
        "Greece or Croatia before the crowds, the Algarve, or the Italian lakes, with the sea "
        "warm enough in the south by the end of the month"),
    "june": (
        "the Greek islands, the Algarve or the Baltic cities, and the first half of the month "
        "is quieter and cheaper than the second"),
    "july": (
        "Scotland or the Alps for cool walking, Norway and Denmark for cities, or the Atlantic "
        "coast of Portugal for a sea breeze - the Mediterranean is at its hottest now"),
    "august": (
        "Scotland, Ireland, the Alps or Norway: the Mediterranean is at its busiest, hottest "
        "and priciest, and Italian and Spanish towns close up at midday"),
    "september": (
        "Greece, Croatia or Italy, because the sea is at its warmest now and the families have "
        "gone home, so the same room costs less"),
    "october": (
        "Cyprus or Crete for 24C and a sea you can still swim in, the Canaries for the most "
        "reliable sun, or Seville and Marrakesh for warm cities without the crowds"),
    "november": (
        "the Canaries, Egypt or Cape Verde for sun, or Rome, Prague and Budapest for cheap "
        "cities without queues"),
    "december": (
        "the Canaries or Cape Verde for sun, the Alps for snow, or any big European city for "
        "the Christmas markets - book before the middle of the month"),
}
_MONTH_SUN = {
    "january": ("the Canaries for 20C, Cape Verde for 25C, or Egypt for 22C and a sea you can "
                "swim in"),
    "february": ("the Canaries, Cape Verde or Egypt, all about 20 to 25C, and the Red Sea coast "
                 "is the warmest water"),
    "march": ("Lanzarote or the other Canaries for 20C, Marrakesh for 22C, or Dubai if you want "
              "30C in the shade"),
    "april": ("the Algarve or Andalusia for 22C, Malta for 20C, or the Canaries to be sure of it"),
    "may": ("Greece, Cyprus or southern Spain, 24-27C, with the sea warming up and the prices "
            "before the school holidays"),
    "june": ("the Greek islands, Croatia or Sicily, 27-30C and the sea warm enough to swim"),
    "july": ("the Algarve, Croatia or the Greek islands, 28-31C, with the sea at its warmest"),
    "august": ("Portugal, Croatia or Greece, 28-31C and reliably dry, or the Baltic if 30C is too "
               "much"),
    "september": ("Greece, Croatia or southern Italy, 26-29C, with the sea at its warmest now the "
                  "schools are back"),
    "october": ("Cyprus, Crete or the Canaries, 24-26C, and the sea is still swimmable"),
    "november": ("the Canaries, Egypt or Cape Verde, and the Red Sea is the warmest of the three"),
    "december": ("the Canaries or Cape Verde for 25C, Egypt for 22C, or the Caribbean if you want "
                 "guaranteed heat"),
}
_MONTH_SUN_ASK = ("sun", "sunny", "hot", "warm", "beach", "swim", "swimming", "heat", "tan",
                  "sunshine", "sea")

_MONTH_VERDICT = {
    "january": ("good for sun or snow and the cheapest, quietest month of the year, but the "
                "Mediterranean is cold and half shut"),
    "february": ("still low season, so cheap and quiet, with real sun only a few hours south "
                 "and half term the week everyone else books"),
    "march": ("spring arriving while the prices are still low, though the Mediterranean is "
              "mild rather than warm and Easter moves the cost"),
    "april": ("one of the best months for southern Europe - warm, quiet and cheaper than May - "
              "with Easter the week to book around"),
    "may": ("warm without the crowds, with the sea warm enough in the south by the end of it "
            "and the school holidays still a month away"),
    "june": ("the sweet spot before the schools break up: hot, long days and prices that have "
             "not caught up with July"),
    "july": ("high season, so hot, busy and priced for it, and the Mediterranean coast is at "
             "its fullest"),
    "august": ("the busiest, hottest and priciest month of the year, so go north, go high or go "
               "early"),
    "september": ("the best month of the year for most of Europe: the sea at its warmest, the "
                  "families gone and the rooms cheaper"),
    "october": ("still warm in the south with the crowds gone, though the north turns wet and "
                "some hotels shut for the winter"),
    "november": ("cheap and quiet with short days, and real sun only in the Canaries, Egypt or "
                 "the Cape Verde islands"),
    "december": ("cold at home and festive in the cities, with sun a few hours south and the "
                 "Christmas weeks to book early"),
}


_MONTH_ASK = ("where", "go", "going", "holiday", "away", "break", "week", "trip", "travel",
              "visit", "somewhere", "destination", "escape", "sun", "hot", "warm",
              "recommend", "suggest", "idea", "ideas", "good place", "best place", "good",
              "worth", "ok", "okay", "wise", "sensible",
              "nice", "nice in", "nice weather", "any good", "good in", "worth visiting",
              "worth going")

_MONTH_NOT_A_PLACE = ("book", "booking", "booked", "flight", "flights", "fly", "airfare",
                      "cheapest", "expensive", "price", "prices", "cost", "costs", "how much",
                      "much does", "spending", "spending money", "budget for",
                      "fare", "fares", "refund", "insurance", "visa")

_MONTH_NOT_A_PLACE_RE = re.compile(
    r"\b(?:%s)\b" % "|".join(re.escape(word) for word in _MONTH_NOT_A_PLACE))

_WHERE_IN_THE_LINE = ("where", "which", "anywhere", "somewhere", "best place", "good place",
                      "nice place", "recommend", "suggest", "idea", "options", "worth",
                      "should", "shall", "could we", "can we", "do you think", "what about",
                      "how about", "want", "need", "fancy", "would like", "i'd like", "id like",
                      "thinking of", "thinking about", "looking for", "considering", "wondering",
                      "hoping", "planning", "keen", "interested", "hot enough", "warm enough")
_SAYS_THEIR_OWN_PLAN = re.compile(
    r"\b(?:i|im|i'm|i am|i've|ive|we|we're|we are|we've|weve|were|he|he's|she|she's|they|"
    r"they're|you|you're|my|our|his|her|their)\b", re.I)


_ABOUT_A_TRIP = re.compile(
    r"\b(?:going|go|goes|went|holiday|holidays|trip|trips|travel|travelling|traveling|fly|flying|"
    r"flight|flights|booked|vacation|getaway|honeymoon|city break|staying|visiting|visit|abroad)\b"
    r"|\b(?:im|i'm|i am|we are|we're|were|we've|we have|i've|ive)\s+(?:away|off)\b", re.I)


def _a_report_of_their_own(clean, month):
    at = re.search(r"\b%s\b" % re.escape(month), clean)
    if not at:
        return False
    start = 0
    for edge in re.finditer(r"[,;:!?](?:\s|$)|\.(?:\s|$)", clean):
        if edge.end() <= at.start():
            start = edge.end()
        elif edge.start() >= at.end():
            return bool(_SAYS_THEIR_OWN_PLAN.search(clean[start:edge.start()]))
    return bool(_SAYS_THEIR_OWN_PLAN.search(clean[start:]))


def _named_place(text, table):
    found = []
    for name in sorted(table, key=len, reverse=True):
        if re.search(r"\b%s\b" % re.escape(name), text) and _names_place(text, name):
            found.append(name)
    return found


_MONTH_WORSE = re.compile(
    r"\b(hot|hotter|hottest|packed|crowded|busy|busiest|wet|wettest|grey|rain|rainy|rains|cold|"
    r"coldest|freezing|closed|shut|avoid|peak|worst|humid|storm|hurricane|mosquitoes|insects|"
    r"dark|pricey|expensive|heat)\b", re.IGNORECASE)


_MONTH_ASKED = True
_A_CLAUSE_VERB = re.compile(
    r"\b(?:is|are|was|were|gives|give|gets|get|has|have|holds|means|brings|sees|closes|runs|"
    r"run|makes|make|leaves|leave)\b")


def _a_month_for_a_place(name, window, month):
    asked = _MONTH_ASKED
    if isinstance(window, tuple):
        window = window[-1]
    label = name if name[:1].isupper() else name.capitalize()
    clauses = [part for part in re.split(r"(?<=[.;])\s+", window) if part.strip()]
    short = month[:3]
    month_here = re.compile(r"\b(?:%s|%s)\b" % (re.escape(month), re.escape(short)),
                            re.IGNORECASE)
    verdict = ("Yes, ", "No, ") if asked else ("", "")
    if clauses and month_here.search(clauses[0]):
        return f"{verdict[0]}{month.capitalize()} is in the good window for {label}: {window}"
    if any(month_here.search(part) and _MONTH_WORSE.search(part) for part in clauses[1:]):
        if _A_CLAUSE_VERB.search(re.split(r"[;.:]", window)[0]):
            return f"{verdict[1]}{month.capitalize()} is not the best month for {label}. {window}"
        return (f"{verdict[1]}{month.capitalize()} is not the best month for {label}. "
                f"The window is {window}")
    return f"{label}: {window}"


_AN_OPEN_ASK = frozenset("""
where somewhere anywhere else ideas idea recommend recommends suggestion suggest destination
inspiration options decide choose
""".split())


def _the_place_in_the_chat(memory, table):
    said = []
    user = memory.get("user") or {}
    for key in ("plan", "plans", "places", "city"):
        value = user.get(key)
        if isinstance(value, str):
            said.append(value)
        elif isinstance(value, (list, tuple)):
            said.extend(str(item) for item in value if item)
    text = " ".join(said).lower()
    if not text:
        return None
    return _find_in(text, table)
_AT_HOME = {
    "cornwall": "coast", "devon": "coast", "dorset": "coast", "norfolk": "coast",
    "suffolk": "coast", "sussex": "coast", "kent": "coast", "isle of wight": "coast",
    "pembrokeshire": "coast", "anglesey": "coast", "gower": "coast", "newquay": "coast",
    "st ives": "coast", "torquay": "coast", "bournemouth": "coast", "brighton": "coast",
    "blackpool": "coast", "scarborough": "coast", "whitby": "coast", "skegness": "coast",
    "great yarmouth": "coast", "bamburgh": "coast", "tenby": "coast", "aberystwyth": "coast",
    "brixham": "coast", "padstow": "coast", "exmouth": "coast", "falmouth": "coast",
    "lake district": "country", "peak district": "country", "yorkshire dales": "country",
    "yorkshire": "country", "cotswolds": "country", "the cotswolds": "country",
    "snowdonia": "country", "brecon beacons": "country", "cumbria": "country",
    "northumberland": "country", "dartmoor": "country", "exmoor": "country",
    "new forest": "country", "the highlands": "country", "highlands": "country",
    "isle of skye": "country", "harrogate": "country", "ludlow": "country",
}
_UK_NATIONS = ("england", "scotland", "wales", "northern ireland")

_WEEKS_AT_HOME = {
    "peak": ("it is the most expensive and the busiest week or two of the year there, so book "
             "the place to stay now, because the good ones go first. Set off early and travel on "
             "a weekday if you can, book any table, boat or attraction you actually want at "
             "least a week ahead, and keep one wet-day plan in your pocket."),
    "shoulder": ("outside the school holidays it is quieter and a good deal cheaper. Some cafes, "
                 "boat trips and attractions keep weekend hours at the edges of the season, so "
                 "check anything you have your heart set on before you book, and keep one "
                 "wet-day plan."),
    "quiet": ("it is the cheapest and quietest time to go, but the days are short and a lot of "
              "places shut after the school holidays, so check what is open before you book and "
              "plan one thing a day rather than a list. Take waterproofs and boots, and treat a "
              "walk as the plan rather than the filler."),
}
_BY_KIND = {
    "coast": ("Pick your beaches by the tide times rather than by the car park, and swim where "
              "there is a lifeguard."),
    "country": ("The car parks at the popular walks are full by ten, so go early or later in the "
                "afternoon, and take a waterproof even on a fine forecast."),
}
_MONTH_SEASON = {
    "january": "quiet", "february": "quiet", "march": "quiet",
    "april": "shoulder", "may": "shoulder", "june": "shoulder",
    "july": "peak", "august": "peak",
    "september": "shoulder", "october": "shoulder",
    "november": "quiet", "december": "quiet",
}

def _a_week_at_home(name, month, kind):
    label = " ".join(word.capitalize() for word in name.split())
    season = _MONTH_SEASON.get(month, "shoulder")
    said = [f"{label} in {month.capitalize()}: {_WEEKS_AT_HOME[season]}"]
    if kind == "coast":
        said.append(_BY_KIND["coast"])
        if month == "september":
            said.append("The sea is at its warmest of the year in September.")
    else:
        said.append(_BY_KIND["country"])
    return " ".join(said)


_A_TRIP_NAMED = re.compile(
    r"\b(?:holiday|holidays|trip|trips|honeymoon|vacation|getaway|break away|flight|flights|fly|"
    r"flying|abroad|city break|weekend away|booked|booking|staying|stay in|travel|travelling|"
    r"traveling|destination|sightseeing|cruise)\b", re.I)


def _month_destination(memory, understood):
    global _MONTH_ASKED
    clean = understood.get("clean", "")
    topics = set((understood or {}).get("topics") or ()) - {"small-talk"}
    asks_a_place = any(word in _AN_OPEN_ASK for word in clean.split())
    ask_clause = " ".join((understood or {}).get("focus") or ())
    asks_the_month = bool(ask_clause) and any(
        re.search(r"\b%s\b" % re.escape(name), ask_clause) for name in MONTHS)
    if (topics and not (topics & set(ANSWERS)) and not asks_a_place
            and not asks_the_month and not _A_TRIP_NAMED.search(clean)):
        return None
    _MONTH_ASKED = (understood or {}).get("kind") == "question" or "?" in clean
    month = None
    found = []
    for name in sorted(MONTHS, key=len, reverse=True):
        match = re.search(r"\b%s\b" % re.escape(name), clean)
        if match:
            found.append((match.start(), match.end(), name))
            if month is None:
                month = name
    if not month:
        return None
    if _MONTH_NOT_A_PLACE_RE.search(clean):
        return None
    found.sort()
    if len(found) > 1:
        between = clean[found[0][1]:found[1][0]]
        if re.search(r"\bor\b|\bvs\b|versus|/", between):
            return None
    for table in (WHEN_TO_GO, BEST_TIME):
        for name in _named_place(clean, table):
            return _a_month_for_a_place(name, table[name], month)
    if not any(word in _AN_OPEN_ASK for word in clean.split()):
        for table in (BEST_TIME, WHEN_TO_GO):
            in_hand = _the_place_in_the_chat(memory, table)
            if in_hand:
                return _a_month_for_a_place(in_hand, table[in_hand], month)
    for name in _named_place(clean, _AT_HOME):
        return _a_week_at_home(name, month, _AT_HOME[name])
    for table in (CITY_COUNTRY, AIR_HOURS_CITY):
        for name in _named_place(clean, table):
            if table[name] in _UK_NATIONS:
                return _a_week_at_home(name, month, "country")
    if not any(word in _AN_OPEN_ASK for word in clean.split()):
        in_hand = _the_place_in_the_chat(memory, _AT_HOME)
        if in_hand:
            return _a_week_at_home(in_hand, month, _AT_HOME[in_hand])
        for table in (CITY_COUNTRY, AIR_HOURS_CITY):
            in_hand = _the_place_in_the_chat(memory, table)
            if in_hand and table[in_hand] in _UK_NATIONS:
                return _a_week_at_home(in_hand, month, "country")
    for table in (WHERE_TO_GO, COUNTRY_ALIASES, CITIES, CAPITALS):
        if _named_place(clean, table):
            return None
    if _a_report_of_their_own(clean, month) and not any(word in clean
                                                        for word in _WHERE_IN_THE_LINE):
        if not _ABOUT_A_TRIP.search(clean):
            return None
        return (f"Where are you going in {month.capitalize()}? Tell me the place and I'll say what "
                f"the weather does there and what a day costs.")
    if "ski" in clean or "snow" in clean:
        return (f"In {month.capitalize()}: the Alps for snow, with a resort at 1,500m or above "
                f"for the best chance of it, and book the transfer with the room.")
    if month in _MONTH_SUN and any(word in clean.split() for word in _MONTH_SUN_ASK):
        return f"{month.capitalize()}: {_MONTH_SUN[month]}."
    picks = _MONTH_PICKS[month]
    return f"{month.capitalize()}: {picks}."


def _month_names():
    return tuple(sorted(MONTHS, key=len, reverse=True))


_A_MONTH_POINTED_AT = ("that one", "those dates", "those weeks", "the same", "the month",
                       "year", "month", "season", "time", "trip", "holiday", "week",
                       "away")
_A_MONTH_FAULT_ASK = ("too hot", "too cold", "too cool", "too wet", "too busy", "too crowded",
                      "too quiet", "too damp", "too rainy", "too windy", "rain", "raining",
                      "rains", "wet", "chilly", "muggy")
_A_TIME_VERDICT_ASK = ("good time", "good time to go", "good time of year", "good time to visit",
                       "worth it", "worth going", "worth a visit", "any good", "good idea",
                       "a good month", "good month", "bad time", "too hot", "too cold",
                       "too wet", "too busy", "rainy", "rain much", "sunny enough")
_A_VERDICT_FILLER = frozenset("""
    is are was were be been am do does did the a an of to in on at for with about it that this
    these those there then so and but or we us our i my me you your they them he she his her
    good time year month season day days worth going go goes visit visiting trip holiday week
    weeks away any much too hot cold wet busy rainy sun sunnier sunny nice ok okay fine idea
    really still think sounds sound going then instead make difference much
""".split())
_MONTH_LOOKS_BACK = 4
_A_MONTH_OF_A_TRIP = re.compile(
    r"\b(?:week|weeks|weekend|weekends|break|holiday|holidays|trip|trips|travel|travelling|"
    r"traveling|abroad|getaway|honeymoon|fly|flying|flight|flights|visit|visiting|stay|staying|"
    r"days|away|time off|city break|somewhere"
    r"|going to|go to|goes to|went to|heading to|off to|flying to|travel to)\b", re.I)


def _the_month_named_in(text):
    low = " ".join(str(text or "").lower().split())
    if not low:
        return None
    words = set(low.split())
    for match in _MONTH_IN_TEXT.finditer(low):
        return match.group(1)
    for name in _month_names():
        if name in AMBIGUOUS_MONTHS:
            continue
        if name in words:
            return name
    return None


def _the_month_in_the_chat(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return None
    said = []
    for turn in turns[-_MONTH_LOOKS_BACK:]:
        text = str((turn if isinstance(turn, dict) else {}).get("user") or "").lower()
        if text:
            said.append(text)
    for text in reversed(said):
        if not _A_MONTH_OF_A_TRIP.search(text):
            continue
        month = _the_month_named_in(text)
        if month:
            return month
    return None


def _the_verdict_on(month, memory, clean):
    for table in (BEST_TIME, WHEN_TO_GO):
        in_hand = _the_place_in_the_chat(memory, table)
        if in_hand:
            return _a_month_for_a_place(in_hand, table[in_hand], month)
    in_hand = _the_place_in_the_chat(memory, _AT_HOME)
    if in_hand:
        return _a_week_at_home(in_hand, month, _AT_HOME[in_hand])
    if any(word in str(clean or "").split() for word in _MONTH_SUN_ASK):
        return f"{month.capitalize()}: {_MONTH_SUN[month]}."
    if any(ask in str(clean or "").lower() for ask in _A_MONTH_FAULT_ASK):
        return f"{month.capitalize()} is {_MONTH_VERDICT[month]}."
    return f"Yes, for the place it suits. {month.capitalize()} is {_MONTH_VERDICT[month]}."


def _a_month_verdict_pointed_at(memory, understood):
    clean = str((understood or {}).get("clean") or "")
    if any(re.search(r"\b%s\b" % re.escape(name), clean.lower()) for name in MONTHS):
        return None
    if any(word for word in clean.split()
           if len(word) > 2 and word.strip(".,!?'") not in _A_VERDICT_FILLER):
        return None
    month = _the_month_in_the_chat(memory)
    if not month:
        return None
    return _the_verdict_on(month, memory, clean)


_PLAN_TALK = ("plan", "planning", "planned", "organise", "organising", "organize", "organizing",
              "put together", "help me", "give me", "want to", "need to", "best way",
              "figure out", "good", "great", "suggest", "recommend", "ideas",
              "start planning", "starting to plan", "start to plan", "where to start",
              "get started", "getting started")
_PLAN_SHAPE = ("trip", "trips", "holiday", "vacation", "time away", "days away", "week away",
               "two weeks", "itinerary", "city break")

_TRIP_LENGTH = (
    (re.compile(r"\b(?:three|3)\s+weeks?\b|\b(?:20|21)\s+days\b"), "three weeks", 21),
    (re.compile(r"\b(?:two|2)\s+weeks?\b|\b(?:14|13|12|11|10)\s+days\b|\bten days\b"),
     "two weeks", 14),
    (re.compile(r"\b(?:one|1)\s+week\b|\ba week\b|\b(?:seven|7)\s+days\b"
                r"|\b(?:five|5)\s+days\b|\b(?:six|6)\s+days\b"), "a week", 7),
    (re.compile(r"\bweekend\b|\b(?:two|2|three|3)\s+nights\b"), "a weekend", 3),
)

_TRIP_WORD = re.compile(
    r"\b(?:trip|trips|holiday|holidays|vacation|vacations|itinerary|travel|travelling|traveling"
    r"|travelled|traveled|away|abroad|fly|flying|flight|flights|hotel|hotels|hostel"
    r"|backpacking|honeymoon|city break|nights?|road trip|visiting|visit|tour|tours)\b", re.I)

_DAYS_WORD = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}


def _trip_plan(memory, understood):
    text = str(understood.get("clean") or understood.get("text") or "").lower()
    city = _find_in(text, CITY_DAYS)
    length = None
    for pattern, name, _nights in _TRIP_LENGTH:
        if pattern.search(text):
            length = name
            break
    place = _find_in(text, BEST_TIME)
    if length and not place and not _TRIP_WORD.search(text):
        return None
    if ("holiday" in text or "holidays" in text) and not length and not place:
        return None
    if length == "three weeks":
        shape = ("Three weeks is slow travel: pick a region and give each of two or three places a "
                 "week, so the trip has a rhythm instead of a list.")
    elif length == "two weeks":
        shape = ("Two or three bases for two weeks, with a travel day between them. More than that "
                 "and you spend the trip moving.")
    elif length == "a weekend":
        shape = "A weekend is one neighbourhood walked properly, not two cities."
    elif length == "a week":
        shape = ("One base and two or three day trips beats three cities in a week, because the day "
                 "you move is a day you lose.")
    else:
        shape = ("Work out how many nights you have first, then give each place at least three of "
                 "them: a base with day trips beats a list of cities, because every move costs you "
                 "half a day.")
    rest = ("Book the first two nights and the last night only, keep one day free in the middle, "
            "and sleep near the airport on the way home.")
    if city:
        days = CITY_DAYS[city]
        return f"{city.capitalize()} wants about {_DAYS_WORD[days]} full days. {rest}"
    if place:
        window = BEST_TIME[place].split(". ")[0].rstrip(".")
        return f"{shape} For {place.capitalize()} the window is {window}. {rest}"
    return f"{shape} {rest}"

HOLIDAY_ASK = ("where should i go", "where can i go", "where do i go", "where to go",
               "where should we go", "where can we go", "where would you go",
               "where would you recommend", "where do you recommend", "where do you suggest",
               "where would you suggest", "where shall i go", "where could i go",
               "suggest somewhere", "recommend somewhere", "anywhere youd recommend",
               "anywhere you would recommend", "somewhere to go", "where should i head",
               "i want a holiday", "i need a holiday", "i fancy a holiday", "want a holiday",
               "need a holiday", "holiday ideas", "ideas for a holiday", "suggest a holiday",
               "recommend a holiday", "i want to go away", "want to go away", "where would be good",
               "where is good", "where would be nice", "somewhere i can go",
               "how far can i go", "how far can i get", "how far will i get",
               "how far will that get me", "how far would i get", "how far will",
               "how far would", "how far does",
               "how far does it go", "how far will 300 pounds go",
               "ideas for", "any ideas for", "suggestions for", "some ideas for",
               "what could i do", "where could we go", "where shall we go")
HOLIDAY_SHAPE = ("holiday", "holidays", "vacation", "break", "short break", "trip", "travel",
                 "week away", "week abroad", "getaway", "abroad", "in the sun", "somewhere warm",
                 "honeymoon", "weekend away", "day trip", "city break",
                 "pounds", "quid", "euros", "dollars", "budget",
                 "sun", "ski", "skiing", "snowboard", "snow", "walking", "hiking", "beach",
                 "few days", "couple of days", "for a few days", "a week somewhere",
                 "anniversary",
                 "staycation", "staycations", "holiday at home", "holidays at home",
                 "holiday in this country", "holiday in the uk", "break at home")
HOLIDAY_WANTS = (
    (("honeymoon", "romantic", "anniversary", "just the two of us"),
     "Santorini and the Amalfi coast are the postcard picks, and both are heaving in July and "
     "August: Italy's lakes or Puglia give you the same views and food with fewer people. For a "
     "beach honeymoon with guaranteed sun, the Maldives from January to April, or Zanzibar if "
     "you want something less built up."),
    (("toddler", "baby", "kids", "children", "child", "family", "teenager", "teenagers"),
     "With small children a short flight and a shallow beach beat a better destination: Menorca "
     "is the quietest of the Balearics, the Algarve has the sand and the short transfer, and a "
     "Center Parcs avoids the flight altogether. Book somewhere with a pool and a kitchen, and "
     "go in late May or September rather than the school summer, when it is warm but not 35C."),
    (("weekend", "two nights", "long weekend", "few days"),
     "For a weekend the travel time is the whole trip, so pick somewhere under two hours door to "
     "door: Bath, York, the Cotswolds or the Norfolk coast at home, or Bruges, Lille or Amsterdam "
     "by train. Two nights is the right length, the train three or four weeks ahead is the cheap "
     "fare, and a room in the middle beats one with a car park."),
    (("cheap", "budget", "afford", "money", "cost", "broke", "save", "pounds", "quid",
      "euros", "dollars", "spare"),
     "The cheapest sun is the Algarve or the Costa Blanca outside July and August: May, June and "
     "late September cost half the school-holiday price, and flights booked six to eight weeks "
     "ahead are the other half. Albania and Bulgaria's Black Sea coast are the best-value "
     "beaches in Europe, and Prague, Krakow and Budapest the cheap city breaks."),
    (("quiet", "peaceful", "relaxing", "chill", "chilled", "calm", "restful", "escape it all",
      "away from crowds", "not too busy"),
     "Quiet comes from the place rather than the country: the north coast of Menorca and the "
     "Aran Islands are empty in June, the Alentejo and inland Andalucia have the heat without "
     "the resorts, and the Cotswolds, Northumberland or the far north of Scotland do it without "
     "a flight. Go in May, June or September - the same place in August is the crowd."),
    (("beach", "beaches", "seaside", "coast", "sand", "sandy", "by the sea"),
     "Pick a stretch of coast rather than a town: the Norfolk coast, Pembrokeshire, Cornwall and "
     "the Northumberland coast are the easy ones at home, and the Algarve or the Costa Blanca "
     "give you warm water outside July and August. The beach a ten-minute walk from the car park "
     "is empty by ten, and the one with the car park and the cafe is not."),
    (("city", "city break", "museums", "food", "restaurants", "culture", "shopping"),
     "Pick by what you want from a city: Lisbon for food and a short flight, Seville for heat and "
     "tapas, Prague or Budapest for grand streets at low prices, Copenhagen for design and "
     "cycling. Two nights is enough for any of them, and flying Tuesday to Thursday costs less "
     "than a weekend."),
    (("ski", "snow", "skiing", "snowboard"),
     "A resort at 1,500m or above is what makes the snow reliable, and January and March are "
     "cheaper than February half-term for the same mountain. The French Alps have the highest "
     "villages, Austria the better-value lift passes, and Italy the cheapest of the big three. "
     "Book the transfer with the room, because a separate one is where the money goes."),
    (("walking", "walk", "hike", "hiking", "mountains", "cycling", "outdoors"),
     "The Dolomites in late June or September for the big views and the huts, the Julian Alps for "
     "the same with fewer people, and the Lake District or the Peak District if you want a short "
     "break without a flight. Book the huts and the popular villages early, and carry the map on "
     "paper."),
    (("sun", "sunny", "warm", "hot", "beach", "beaches", "swim", "swimming", "tan"),
     "For real sun at any time of year, the Canaries are the safe pick and the water is warmest "
     "from late summer into October. Greece in June or September gives you 28C without the "
     "August crowds, and from November to March the short-haul sun is the Canaries, Cape Verde "
     "or Egypt, with the Red Sea the one to swim in."),
    (("uk", "britain", "england", "scotland", "wales", "staycation", "at home", "no flight"),
     "In the UK: Cornwall and the Pembrokeshire coast for beaches, the Lake District for walking, "
     "Northumberland for empty country and dark skies, and Edinburgh or Bath for a city. Book the "
     "coast two months ahead for a school holiday, and take the train where you can, because the "
     "drive is the part that eats the weekend."),
)
HOLIDAY_NOT = (tuple(MONTHS) + tuple(WHERE_TO_GO)
               + tuple(word for word in COUNTRY_ALIASES if word not in ("uk", "britain"))
               + tuple(CITIES)
               + ("what could i do with", "what can i do with", "what should i do with",
                  "what shall i do with", "what do i do with", "what to do with",
                  "what would i do with", "what can we do with", "what should we do with")
               + ("petrol", "diesel", "fuel", "tank", "tankful", "charge", "miles", "per litre",
                  "litre", "gallons", "mpg",
                  "my day off", "on a day off", "day to myself", "free time", "afternoon off")
               + ("when should i go", "when to go", "best time", "best month", "pack", "packing",
                  "suitcase", "luggage", "hotel", "hotels", "flights", "flight", "visa",
                  "how much", "insurance", "travelling with"))


CHEAPER_TRIP = ("The date is most of the price: a week either side of the school holidays, "
                "flying Tuesday or Wednesday rather than Friday, and booking the flight and the "
                "room together six to eight weeks ahead all come off the same trip. Then take "
                "hand luggage only, use the bus rather than the airport taxi, eat breakfast from "
                "a supermarket, and pay for one big thing a day instead of a package of five - "
                "that is where a week's money actually goes.")

_TRIP_IN_LINE = ("holiday", "holidays", "vacation", "week away", "getaway", "trip",
                 "a break", "city break", "abroad")


def _holiday_costs(memory, understood):
    clean = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if not any(re.search(r"\b%s\b" % re.escape(word), clean) for word in _TRIP_IN_LINE):
        return None
    return CHEAPER_TRIP

_A_LENGTH_ONLY = ("a few days", "few days", "couple of days", "a couple of days",
                  "day trip", "day trips", "day out", "day outs", "afternoon out")
_A_VAGUE_ASK = ("ideas", "idea", "suggestions", "suggestion", "what could i do",
                "what can i do", "what should i do")
_A_PRICE = ("pounds", "quid", "euros", "dollars", "budget", "cheap", "afford", "save up",
            "spare", "money")


def _a_shortlist_question(understood):
    clean = ((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if any(re.search(r"\b" + re.escape(word) + r"\b", clean) for word in _A_PRICE):
        return True
    if not any(re.search(r"\b" + re.escape(word) + r"\b", clean) for word in _A_VAGUE_ASK):
        return True
    return not any(re.search(r"\b" + re.escape(word) + r"\b", clean)
                   for word in _A_LENGTH_ONLY)

def _where_no_place(memory, understood):
    clean = (understood.get("clean") or understood.get("text") or "").lower()
    for words, reply in HOLIDAY_WANTS:
        if any(re.search(r"\b%s\b" % re.escape(word), clean) for word in words):
            return reply
    return ("Two things decide it: how long you have, and whether you want sun or a city. With a "
            "week and a wish for sun, the Canaries, Greece or southern Spain; with a long "
            "weekend, Lisbon, Porto, Prague or Edinburgh; with children, a short flight to "
            "Menorca or the Algarve. Tell me the month and I will be more use than that.")


_WANT_TRIP_SAID = (
    "want to go", "wanted to go", "want to go away", "want to get away", "want to go somewhere",
    "want a few days", "want a couple of days", "want a week", "want a few weeks",
    "want a weekend away", "want a break away", "want a trip", "want to book a trip",
    "fancy a few days", "fancy going", "fancy a week", "fancy a weekend away",
    "week in the sun", "days in the sun", "cheap week", "cheap holiday", "week away",
    "somewhere warm", "somewhere quiet", "somewhere sunny", "somewhere hot",
    "somewhere with a beach", "somewhere near the sea", "somewhere by the sea",
    "stag do", "stag weekend", "hen do", "hen weekend",
    "the lads want", "my mates want", "the girls want", "my friends want",
    "thinking of going", "thinking about going")
_PLACE_FILLER = frozenset("""
    the a an some any my our your his her their this that it
    somewhere anywhere nowhere everywhere there here abroad away travelling traveling
    to in into on at for with by about off from near around go going get getting fly flying
    book booked stay live move travel take going
""".split())
_NOT_A_PLACE = frozenset("""
    gym bed sleep work school college
    university class classes lesson lessons doctor doctors dentist hospital surgery toilet loo
    bathroom kitchen shop shops supermarket pub pubs cinema theatre church mosque prison home
    house town back out outside running walk swim swimming gymnasium office meeting
    park parks playground allotment allotments tip dump library bank market pool marina pier
    seafront promenade station airport petrol pharmacy garage salon barbers hairdresser
""".split())
_PLACE_ENDS = frozenset("""
    on at for in with next this that and or but then after before during from so of i we my our
    it is was would will can could should to a an the mates friends lads girls kids children
    family
""".split())
_SOMEONE_ELSE = frozenset("her his their she he".split())
_SOMEONE_WANTS = re.compile(
    r"\b(?:son|sons|daughter|daughters|kid|kids|child|children|toddler|teenager|teenagers|"
    r"mum|mom|dad|nan|gran|granny|grandad|grandma|niece|nephew|boy|girl|boyfriend|girlfriend)"
    r"\b[^.!?]{0,28}?\b(?:wants|want to|wanted to|would like|fancies|is keen|hoping)")
_NOT_A_TRIP_EVENT = frozenset("""
    party parties wedding weddings funeral funerals christening christenings christening
    birthday birthdays dinner disco gig gigs concert concerts match matches game games
    appointment appointments interview interviews exam exams service barbecue bbq reunion
""".split())
_NO_TRIP_WANTED = re.compile(
    r"\b(?:don'?t|dont|do not|doesn'?t|does not|didn'?t|did not)\s+(?:really\s+|actually\s+)?"
    r"(?:want|wanna|fancy|plan|intend)\s*(?:to\s+)?(?:go|going|be|come|travel)\b"
    r"|\bcan'?t face\b|\bcant face\b|\bdread(?:ing)?\b|\bnot going\b"
    r"|\bwould rather not go\b|\bno way i'?m going\b")
_TRIP_GO = re.compile(
    r"\b(?:go|goes|going|went|get|getting|got|fly|flying|flew|week|weeks|weekend|days|trip\s+to"
    r"|break)\s+(?:to|in|into)\s+(.{0,40})")


def _trip_place(clean):
    match = _TRIP_GO.search(str(clean or "").lower())
    if not match:
        return ""
    tail = match.group(1)
    for place in sorted(AIR_HOURS_CITY, key=len, reverse=True):
        if re.search(r"\b%s\b" % re.escape(place), tail):
            return place
    words = [word for word in re.findall(r"[a-z][a-z-]*", tail)
             if word not in _PLACE_FILLER]
    if not words or words[0] in _NOT_A_PLACE or words[0] in _TRIP_SHAPE:
        return ""
    name = [words[0]]
    for word in words[1:3]:
        if word in _PLACE_ENDS or word in _NOT_A_PLACE:
            break
        name.append(word)
    return " ".join(name)


_WANT_TRIP_SHAPE = (
    "away", "trip", "trips", "holiday", "holidays", "vacation", "week", "weeks", "weekend",
    "days", "sun", "warm", "quiet", "abroad", "getaway", "go to", "go somewhere", "days away",
    "week away", "weekend away", "in the sun", "stag", "hen")
_TRIP_SHAPE = frozenset("""
    away trip trips holiday holidays vacation week weeks weekend days sun sunny warm hot quiet
    abroad getaway beach beaches ski skiing snowboard city-break break-away stag hen
""".split())
_TRIP_OTHER_ROW = ("pack", "packing", "packed", "suitcase", "luggage", "what to bring",
                   "insurance", "passport", "visa", "flight", "flights", "hotel", "hotels",
                   "how much", "cost", "costs", "price", "checklist", "what do i need",
                   "booked", "already booked", "meal", "meals", "dinner", "dinners", "food",
                   "shop", "shopping", "recipe", "menu", "cook", "cooking",
                   "eat", "eating", "eat out", "eating out", "restaurant", "restaurants",
                   "cafe", "cafes", "coffee", "drink", "drinks", "lunch", "breakfast",
                   "takeaway", "near me", "hostel", "hostels", "airbnb", "book a table",
                   "table for",
                   "to stay", "place to stay", "somewhere to stay", "staying in", "staying near",
                   ) + tuple(MONTHS)
_STAG_DO = (
    "Treat it as one city, two nights and one big thing booked ahead: Budapest, Krakow and Prague "
    "are the cheap three, Lisbon, Porto and Barcelona the ones with better weather, and anywhere "
    "in the sun is cheaper in May and September than in July. Book the rooms as a block, put the "
    "activity or the meal in the diary before anyone books a flight, and collect the money up "
    "front - the group chat will not pay you back afterwards.")


_A_REFUSAL = re.compile(
    r"\b(?:don'?t|do not|doesn'?t|didn'?t|would rather not)\s+want\s+to\s+go\b"
    r"|\bget(?:ting)?\s+out\s+of\s+(?:going\s+to\s+)?(?:the\s+|a\s+|my\s+|our\s+)?"
    r"(?:works?\s+)?(?:christmas\s+|leaving\s+|office\s+|staff\s+)?(?:do|party|night out|"
    r"meal|dinner|drinks|wedding|barbecue|bbq)\b"
    r"|\b(?:do|did)\s+i\s+have\s+to\s+go\b"
    r"|\bcan'?t\s+(?:come|make it|be there)\b"
    r"|\bmake\s+my\s+excuses\b|\bback\s+out\s+of\b"
    r"|\bhow\s+(?:to|do|can|should|would)\s+(?:i\s+)?(?:politely\s+|nicely\s+|tactfully\s+)?"
    r"(?:decline|refuse|turn\s+(?:(?:it|them|that|one)\s+)?down|say\s+no\s+to)\b", re.I)


def _a_trip_is_wanted(understood):
    clean = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    words = set(re.findall(r"[a-z']+", clean))
    if _A_REFUSAL.search(clean):
        return False
    if re.search(r"\bstag\b|\bhen (?:do|weekend|night)\b", clean):
        return True
    if words.intersection(_SOMEONE_ELSE) or _SOMEONE_WANTS.search(clean):
        return False
    if _NO_TRIP_WANTED.search(clean):
        return False
    if words.intersection(_NOT_A_PLACE) or words.intersection(_NOT_A_TRIP_EVENT):
        return False
    place = _trip_place(clean)
    known = list(WHERE_TO_GO) + list(COUNTRY_ALIASES) + list(CITIES)
    if place and not any(re.search(r"\b%s\b" % re.escape(word), clean) for word in known):
        return True
    if words.intersection(_TRIP_SHAPE):
        return not re.search(r"\b(?:go|going|get|getting)\s+(?:home|back|in|out)\b", clean)
    return False


def _want_a_trip(memory, understood):
    clean = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if _A_REFUSAL.search(clean):
        return None
    if re.search(r"\bstag\b|\bhen (?:do|weekend|night)\b", clean):
        return _STAG_DO
    known = list(WHERE_TO_GO) + list(COUNTRY_ALIASES) + list(CITIES)
    if any(re.search(r"\b%s\b" % re.escape(word), clean) for word in known):
        return None
    place = _trip_place(clean)
    if place:
        name = place.title()
        return (name + " for a few days: fix the dates and pick one base, then book the flight "
                "and the room together six to eight weeks ahead, and agree the one thing you "
                "all want to do before anything else. The rest is food and wandering, and for "
                "a group that is the part that goes wrong - one person books, everyone pays "
                "into one pot, and keep the time on the ground to two or three nights.")
    return _where_no_place(memory, understood)


_WARM_WEEK = (
    "light cotton tops and shorts, one long-sleeved layer and a light waterproof, plus swimwear, "
    "a hat, high-factor sun cream and shoes you can walk in. Take two pairs of shoes at most and "
    "one smarter outfit if you plan to eat out; everything else can be washed.")


_FOOD_TO_CARRY = ("food", "foods", "snacks", "snack", "lunch", "dinner", "breakfast", "meal",
                  "meals", "picnic", "dish", "dishes", "something to eat", "anything to eat",
                  "cook", "cooking", "bake", "baking", "recipe", "recipes", "drinks")


def _not_a_food_to_carry(understood):
    line = understood or {}
    clean = str(line.get("clean") or line.get("text") or "").lower()
    words = set(re.findall(r"[a-z']+", clean))
    if not words.intersection(_FOOD_TO_CARRY):
        return True
    carry = ("bring", "brings", "bringing", "take", "takes", "taking", "carry", "food",
             "eat", "make", "makes", "cook", "bake")
    return not any(word in words for word in carry)


def _warm_week_pack(memory, understood):
    clean = str((understood or {}).get("clean") or (understood or {}).get("text") or "")
    months, seasons = _time_terms(clean, loose=True)
    if months & {6, 7, 8} or seasons & {"summer", "high summer"}:
        return ("For a warm summer week: " + _WARM_WEEK.replace(
            "one long-sleeved layer and a light waterproof, plus",
            "one long-sleeved layer for air conditioning and a light waterproof for a "
            "thunderstorm, plus"))
    if months & {5, 9, 10}:
        return ("For a warm week out of high summer: " + _WARM_WEEK.replace(
            "one long-sleeved layer and a light waterproof, plus",
            "one long-sleeved layer and a light waterproof, as May and October evenings turn "
            "cool even in Spain or Italy, plus"))
    return "For a warm week: " + _WARM_WEEK


def _cold_drinks(memory, understood):
    said = str(understood.get("clean") or understood.get("text") or "").lower()
    if any(word in said for word in ("quick", "quickly", "fast", "in a hurry", "right now",
                                     "asap", "hurry", "minutes")):
        return ("Fastest is a bucket or a big bowl of cold water with ice in it and a good "
                "handful of salt: salt makes the water colder than ice alone, and a bottle "
                "or a glass drops to fridge-cold in about 15 minutes. No ice? Wet a tea "
                "towel, wring it out, wrap the bottle and stand it in the freezer for 10 to "
                "15 minutes, or stand the glass in iced water and stir.")
    return ("Chill it in the fridge first, then a cool bag or box with a frozen ice block or "
            "a bag of ice at the bottom and the drinks on top - ice above them, not under, "
            "since cold sinks. Fill bottles right to the top and keep the bag shut and out of "
            "the sun; a wrapped bottle holds the cold far longer than a bare one. For a "
            "party, chill half the bottles and freeze the other half: the frozen ones keep "
            "the box cold and thaw by the time you need them.")

_YES_THE_WINDOW = " is in the good window for "
_NO_THE_WINDOW = " is not the best month for "


def _the_window_is_read(memory, window):
    said = str(window or "").strip().lower()
    first = re.split(r",? when |,? and (?:the|it) |\. ", said)[0].strip(" .;,")
    if len(first.split()) < 4:
        return False
    turns = [turn for turn in ((memory or {}).get("turns") or []) if isinstance(turn, dict)]
    for turn in turns[-5:]:
        if first in str(turn.get("bot") or "").lower():
            return True
    return False


def _the_same_verdict_was_given(memory, tail):
    said_tail = str(tail or "").strip().lower()
    if not said_tail:
        return False
    turns = [turn for turn in ((memory or {}).get("turns") or []) if isinstance(turn, dict)]
    return any(said_tail in str(turn.get("bot") or "").lower() for turn in turns[-5:])


def _a_month_verdict_once(memory, understood):
    here = ""
    if isinstance(memory, dict):
        here = str((memory.get("understood") or {}).get("clean") or "")
    if (here and _the_month_of({"clean": here}) is None
            and any(ask in here for ask in _A_TIME_VERDICT_ASK)):
        month = _the_month_of(understood)
        if month:
            return _the_verdict_on(month, memory, here)
    said = _month_destination(memory, understood)
    if not said:
        return None
    if said.startswith("Yes, ") and _YES_THE_WINDOW in said:
        head, _, window = said.partition(": ")
        if not _the_window_is_read(memory, window):
            return said
        label = head.split(_YES_THE_WINDOW, 1)[1]
        tail = _YES_THE_WINDOW + label
        return head + (" too." if _the_same_verdict_was_given(memory, tail) else ".")
    if said.startswith("No, ") and _NO_THE_WINDOW in said:
        marker = next((one for one in (". The window is ", ". ") if one in said), "")
        head, _, rest = said.partition(marker) if marker else (said, "", "")
        if not rest or not _the_window_is_read(memory, rest):
            return said
        label = head.split(_NO_THE_WINDOW, 1)[1]
        tail = _NO_THE_WINDOW + label
        return head + (" either." if _the_same_verdict_was_given(memory, tail) else ".")
    label, _, window = said.partition(": ")
    if not window or not _the_window_is_read(memory, window):
        return said
    month = _the_month_of(understood)
    first = re.split(r",? when |\. ", window)[0].split(":")[0].strip(" .;,")
    names_a_month = any(re.search(r"\b%s\b" % re.escape(name), first.lower())
                        for name in MONTHS)
    if month and names_a_month:
        outside = "is not in the window for " + label
        if _the_same_verdict_was_given(memory, outside):
            return f"No, {month.capitalize()} {outside} either."
        return f"No, {month.capitalize()} {outside}: {first}."
    return said


def _the_month_of(understood):
    clean = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    for name in sorted(MONTHS, key=len, reverse=True):
        if re.search(r"\b%s\b" % re.escape(name), clean):
            return name
    return None
_A_WAY_THERE = re.compile(r"\b(?:get to|get from|getting to|getting from|way to get|way from|"
                          r"how do i get|how do you get|way there)\b")
_AN_EATING = re.compile(r"\b(?:eat|eats|eating|food|foods|meal|meals|restaurant|restaurants|"
                        r"lunch|dinner|breakfast|snack|snacks|menu|menus|dining)\b")


_VALUE_EATING = re.compile(r"\b(?:good value|value for money|cheap eats|cheapest eats)\b")


def _a_way_there_needs_no_eating(understood):
    clean = (understood.get("clean") or "").lower()
    return bool(_AN_EATING.search(clean) or _VALUE_EATING.search(clean))


def _a_weight_is_the_kitchen(understood):
    return not a_weight(understood)


_A_PLANE = re.compile(r"\b(?:flight|flights|fly|flying|plane|planes|air fare|airfare)\b")
_A_WAY_ON_THE_GROUND = re.compile(r"\b(?:train|trains|rail|railway|coach|coaches|bus|buses|"
                                  r"drive|driving|car|cars)\b")


def _a_comparison_needs_two_ways(understood):
    clean = (understood.get("clean") or "").lower()
    if not _A_PLANE.search(clean):
        return True
    return bool(_A_WAY_ON_THE_GROUND.search(clean))
def _a_place_it_might_not_be_safe(memory, understood):
    clean = str((understood or {}).get("clean") or "").lower()
    city = _find_in(clean, CITIES)
    if not city:
        turns = memory.get("turns") if isinstance(memory, dict) else None
        for turn in reversed((turns or [])[-3:] if isinstance(turns, list) else []):
            if not isinstance(turn, dict):
                continue
            city = (_find_in(str(turn.get("user") or "").lower(), CITIES)
                    or _find_in(str(turn.get("bot") or "").lower(), CITIES))
            if city:
                break
    if not city:
        return None
    return (f"Nobody can promise {city.title()} is safe, and anyone selling that is selling "
            f"something. What keeps you out of trouble there is the ordinary kit: busy, lit "
            f"streets, more so after dark, the metro or a licensed taxi rather than a shortcut, "
            f"the phone out of sight and the bag in front of you, and the two or three streets "
            f"the hotel desk tells you to avoid - they know this week's answer better than any "
            f"guide. Keep the hotel's address on you and the local emergency number in your "
            f"phone.")
_TRAINS_FOR = re.compile(
    r"\b(to|need to|have to|got to|going to|how long to|weeks to|time to|how to|back to)"
    r"\s+train\b"
    r"|\btrain(?:ing|ed)?\s+(?:for|hard|harder|again|towards|up for)\b"
    r"|\btrain(?:ing|ed)\s+(?:twice|three|four|every|each|most|more)\b")


_A_TREATMENT_AT_HOME = re.compile(
    r"\b(threadworms?|worms?|nits|head ?lice|lice|scabies|chickenpox|measles|mumps|"
    r"hand foot and mouth|conjunctivitis|norovirus|stomach bug|sick bug|rash|fever|temperature|"
    r"cold|flu|cough|vomit\w*|diarrhoea|diarrhea|infect\w*|isolat\w*|contagious|catching|"
    r"unwell|ill)\b")
_A_JOURNEY_SAID = re.compile(
    r"\b(holiday|holidays|abroad|trip|trips|travel|travelling|traveling|flight|flights|fly|"
    r"flying|airport|overseas|border|passport|passports|visa|destination|resort)\b")


def _a_journey_not_a_treatment(understood):
    text = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if _A_JOURNEY_SAID.search(text):
        return True
    return not _A_TREATMENT_AT_HOME.search(text)


def _a_journey_not_training(understood):
    text = (understood or {}).get("clean") or ""
    return not _TRAINS_FOR.search(text)


def _a_coach_is_a_journey(understood):
    sense = (understood or {}).get("sense") or {}
    return sense.get("coach") not in ("teacher", "furniture")


def _the_journey_in_the_line(understood):
    return _a_journey_not_training(understood) and _a_coach_is_a_journey(understood)

_TRAFFIC_SITUATIONS = (
    (("aquaplan", "hydroplan", "standing water", "puddle"),
     "Aquaplaning: ease off the accelerator, keep the wheel straight and do not brake until the "
     "tyres bite again. Then put the lights on, slow right down and leave twice the gap until the "
     "road has drained."),
    (("tailgat", "tailgater", "behind me", "right behind", "close behind", "up behind",
      "on my bumper", "bumper"),
     "Someone on your bumper: slow down gradually so there is room for both of you to stop, and let "
     "them past at the first chance you get. Never brake-check them - it turns a nuisance into a "
     "crash."),
    (("fog", "foggy"),
     "In fog: dipped headlights on, fog lights only once you cannot see more than about 100 metres, "
     "and drop to a speed you could stop at inside the distance you can see. Keep well back, because "
     "the car in front can stop sooner than you can see."),
    (("heavy rain", "raining", "rain", "wet road", "wet roads"),
     "In heavy rain: dipped headlights on, double the gap and lift off where the water gathers, "
     "because standing water is where aquaplaning starts. Slow down before a bend, not in it."),
    (("skid", "sliding", "slides"),
     "If the car slides: ease off the accelerator and steer where you want to go, and do not stamp "
     "on the brake - that is usually what started it. Then slow down and keep the wheel steady until "
     "the tyres grip again."),
    (("smart motorway", "red x", "red cross", "hard shoulder"),
     "On a smart motorway the red X means the lane is closed because somebody is in it, so obey it "
     "and expect the limit to drop with it. If you break down, get out on the left, behind the "
     "barrier, and call 999 from the nearest orange marker."),
    (("overtak", "overtaking"),
     "Overtaking: get past and back in with a gap you could pull into, rather than sitting alongside "
     "a lorry where the driver cannot see you. Leave four seconds in front and behind."),
    (("slip road", "merging", "merge", "join a motorway", "joining a motorway",
      "join the motorway", "joining the motorway", "merge onto", "merging onto"),
     "Joining the motorway: use the slip road to build up to the speed of the traffic and slot into a "
     "gap rather than stopping at the end of it. Move over a lane if you can to let somebody in."),
)

_JAM_REPLY = (
    "Traffic that crawls is a gap problem: count four seconds to the car in front and brake early "
    "and gently, so the person behind has time to do the same - most jams are made by that "
    "accordion, not by the crash. Stay in one lane where you can and watch the brake lights two "
    "cars ahead rather than the one in front. Add twenty minutes before you set off and plan a stop "
    "every two hours, which is what keeps the last hour the same as the first.")


def _drive_in_traffic(memory, understood):
    text = " ".join([str(understood.get("clean") or "").lower()]
                    + [str(word).lower() for word in (understood.get("words") or [])])
    for words, reply in _TRAFFIC_SITUATIONS:
        if any(word in text for word in words):
            return reply
    return _JAM_REPLY


FOOD_IN = {
    "spain": ("Tapas at the bar - two or three plates between you - paella in Valencia and "
              "pintxos in San Sebasti\u00e1n. Jam\u00f3n and pimientos de Padr\u00f3n are the "
              "cheap way in."),
    "italy": ("Rome for cacio e pepe or carbonara, Naples for pizza and Bologna for rag\u00f9, "
              "with a coffee standing at the bar. Order the house wine; it is cheaper than water "
              "in some places."),
    "france": ("A bakery lunch, steak-frites in Paris and a bouchon in Lyon, with cider and cream "
               "in Normandy. The fixed-price lunch menu is where the value is."),
    "portugal": ("Past\u00e9is de nata and grilled sardines in Lisbon, a francesinha in Porto and "
                 "cataplana on the Algarve. Look for the prato do dia, a set lunch with wine for "
                 "very little."),
    "greece": ("Souvlaki, grilled octopus and a proper village salad: tomato, cucumber, onion and "
               "a slab of feta, no lettuce. Eat where the menu is short and the bread is fresh."),
    "turkey": ("Bal\u0131k ekmek - fish in bread - by the water in Istanbul, a breakfast of "
               "cheese, olives and menemen, and pistachio baklava in the south-east."),
    "morocco": ("Tagine, couscous on a Friday and mint tea poured from a height, with the evening "
                "food stalls in Marrakech the easy start. Bread and olives come with everything."),
    "egypt": ("Koshari from a street shop - rice, lentils and pasta with tomato sauce - ful "
              "medames for breakfast, and grilled fish by the Red Sea."),
    "japan": ("Sushi at a counter and a bowl of ramen in Tokyo, takoyaki and okonomiyaki in Osaka, "
              "tofu and kaiseki in Kyoto. Convenience-store food is genuinely good and cheap."),
    "thailand": ("Street food is the point: pad thai, som tam and moo ping, cooked in front of "
                 "you where it is busy. Say \"not spicy\" clearly, and eat breakfast at the "
                 "market."),
    "india": ("Dosa, idli and coconut curries in the south; butter chicken, chaat and tandoori "
              "bread in the north. Breakfast is the meal to try first."),
    "mexico": ("Tacos al pastor from a stand, tamales for breakfast and mole in Oaxaca, with the "
               "salsa on the side so you choose the heat."),
    "croatia": ("Grilled fish and black risotto on the coast, \u0107evapi inland, and a konoba "
                "with a short menu is the best bet. Pizza is everywhere and usually good."),
    "germany": ("Bratwurst from a stand, a proper schnitzel and rye bread with everything; in "
                "Bavaria a pretzel and a cold beer counts as lunch."),
    "netherlands": ("Bitterballen with a beer, raw herring with onions from a stall, and a "
                    "stroopwafel warm off the iron."),
    "ireland": ("Fish and chips, a full Irish breakfast, and brown bread with smoked salmon; "
                "chowder on the west coast."),
    "scotland": ("Fish and chips, a full Scottish breakfast, haggis with neeps and tatties, and "
                 "seafood in Oban or on the west coast."),
    "england": ("Fish and chips, a Sunday roast and a proper curry house; in London the markets "
                "are better eating than the streets around the sights."),
    "iceland": ("Lamb soup, skyr and a hot dog with everything from the stand in Reykjav\u00edk, "
                "with fish straight off the boat. It is expensive, so eat one good meal a day."),
    "poland": ("Pierogi, a bowl of \u017curek sour rye soup and kielbasa off a grill, with "
               "pierogi shops the cheapest full meal in town."),
    "vietnam": ("Ph\u1edf for breakfast in Hanoi, b\u00e1nh m\u00ec from a cart and fresh spring "
                "rolls down the middle of the country. Eat where the stools are small and the "
                "queue is long."),
    "china": ("Go regional: dim sum in Guangzhou and Hong Kong, hand-pulled noodles in Xi'an and "
              "a Sichuan hotpot in Chengdu. Order several dishes and share them."),
    "belgium": ("Mussels with chips, a waffle from a stall and frites with mayonnaise; the beer "
                "is the point, and every bar has its own glass."),
    "austria": ("Wiener schnitzel, a sausage from a stand and a slice of Sachertorte, with coffee "
                "and cake an entire afternoon."),
    "tunisia": ("Couscous on a Friday, a brik with an egg inside and harissa with everything, "
                "usually with bread and olives first."),
    "cuba": ("Ropa vieja, black beans with rice and a strong coffee; the paladares - private "
             "restaurants - beat the state ones."),
    "canada": ("Poutine in Quebec, salmon on the west coast and a proper diner breakfast; "
               "portions are big, so order less than you think."),
    "australia": ("Fish and chips on the coast, a meat pie and a flat white; the coffee is what "
                  "people miss when they leave."),
    "usa": ("Go regional: barbecue in Texas or Kansas City, a po'boy in New Orleans, pizza by the "
            "slice in New York, tacos in Los Angeles."),
    "argentina": ("Beef is the point: a parrilla grilled over coals with chimichurri, empanadas "
                  "from a bakery and a mate to carry round. Order the bife de chorizo and share "
                  "it, and eat late: nowhere is busy before nine."),
    "brazil": ("A kilo restaurant at lunch, where you pay by weight, is the cheap way in; feijoada "
               "on a Saturday, p\u00e3o de queijo and a\u00e7a\u00ed from a corner shop, and "
               "churrasco for a proper dinner."),
    "peru": ("Ceviche at lunch, never in the evening, with leche de tigre on the side; lomo saltado "
             "and a quinoa soup in the Andes. Lima is worth a whole day of eating."),
    "south korea": ("Barbecue you cook at the table, with lettuce leaves and a dozen little dishes "
                    "that come free; then fried chicken with beer, and street stalls for tteokbokki "
                    "and hotteok."),
    "lebanon": ("Mezze is the meal: hummus, tabbouleh, fattoush and grilled halloumi, then kibbeh "
                "and a plate of mixed grill. Order several small plates and share."),
    "israel": ("Hummus with a runny egg for breakfast, sabich and falafel in pita, and a market "
               "lunch of cheeses, olives and bread. Salads come with everything."),
    "nigeria": ("Jollof rice with fried plantain, a bowl of egusi with pounded yam and suya off a "
                "night grill. Eat where the queue is local and the pepper is not toned down."),
    "kenya": ("Nyama choma - grilled goat or beef - with kachumbari, plus ugali and sukuma wiki; "
              "in Mombasa the coast gives you biryani and coconut curries."),
    "south africa": ("A braai is the meal: grilled meat, a pap and relish on the side. Then bunny "
                     "chow in Durban, biltong from a butcher and a bobotie."),
    "wales": ("Cawl, the lamb and leek broth, with bread and cheese; Welsh rarebit on toast, "
              "laverbread for breakfast in the valleys, and Welsh cakes warm from the griddle."),
    "new zealand": ("A meat pie from a dairy, fish and chips on the beach and a h\u0101ngi if you "
                    "get invited; lamb is the dinner and the flat white is the coffee."),
    "sweden": ("Meatballs with lingonberry, pickled herring at midsummer and a kanelbulle with "
               "coffee; lunch is often a buffet table of salads and bread."),
    "denmark": ("Sm\u00f8rrebr\u00f8d - open sandwiches - for lunch, a hot dog from a stand and "
                "pastry from a proper bakery. New Nordic tasting menus cost a lot; the bakeries "
                "do not."),
    "norway": ("Salmon and cod, a brown cheese on toast for breakfast and a waffle with jam; "
               "eating out is very expensive, so the supermarket deli counter is how people "
               "lunch."),
    "switzerland": ("Fondue and raclette, r\u00f6sti with a fried egg and a plate of b\u00fcndner "
                    "fleisch; the supermarkets and bakery lunch are the only cheap meals."),
    "russia": ("Borscht with sour cream, pelmeni with butter and a blini from a street kiosk; a "
               "stolovaya canteen is cheap and filling, and the tea comes with everything."),
    "singapore": ("A hawker centre is the answer: chicken rice, laksa and char kway teow from "
                  "different stalls, all cheap. Order with tissue packets on the table to claim "
                  "a seat."),
    "malaysia": ("Nasi lemak for breakfast, char kway teow and laksa from the hawkers, and "
                 "roti canai at any hour; the food courts are where the good cheap eating is."),
    "indonesia": ("Nasi goreng and satay from a warung, rendang in Padang and gado-gado; eat where "
                  "the warung is busy and the price list is on the wall."),
    "philippines": ("Lechon for a celebration, adobo and sinigang at home, and halo-halo in the "
                    "heat; the malls have the air conditioning and the food halls."),
    "pakistan": ("Nihari and haleem for breakfast in Lahore, chaat from a stall and a plate of "
                 "biryani at lunch; the grill houses do seekh kebab and naan fresh from the "
                 "tandoor."),
    "sri lanka": ("Rice and curry, several dishes at once, with hoppers for breakfast and kottu "
                  "off a hotplate at night; the fish curry on the coast is the one to order."),
}
_FOOD_WORDS = ("food like", "dishes like", "cuisine like", "food",
               "foods", "eat", "eating", "dish", "dishes", "cuisine", "cuisines",
               "local food", "street food", "speciality", "specialities", "specialty",
               "specialties", "what do they eat", "what to eat", "restaurant", "restaurants",
               "menu", "what about food")
_FOOD_SHAPE = ("what", "about", "there", "should", "shall", "can", "could", "do", "does",
               "where", "best", "try", "local", "in", "good", "nice", "any", "the", "like")
_FOOD_NOT_A_TRIP = (
    "cook", "cooking", "cooked", "make", "made", "making", "recipe", "recipes", "bake", "baked",
    "baking", "oven", "fridge", "freezer", "supermarket", "shopping list", "meal plan",
    "meal prep", "batch", "leftovers", "tonight", "dinner tonight", "for dinner", "for tea",
    "for lunch", "for breakfast", "with rice", "with pasta", "with chicken", "in the oven",
    "live in", "i live", "we live", "moved to", "move to", "i'm from", "im from", "grew up",
    "my home", "back home", "at home in", "lived in", "living in", "have lived", "live here",
    "moved here", "here for years",
    "safe", "unsafe", "ill", "sick", "sickness", "hygiene", "hygienic", "avoid", "avoiding",
    "tap water", "ice in", "food poisoning", "stomach", "dodgy", "risky",
    "customs", "declare", "duty free", "take food", "bring food", "bring back", "bring home",
    "take into", "bring into", "allowed in", "allowance", "import", "food into", "ham",
    "cheese back", "meat into", "milk into")
FOOD_ADJECTIVES = {
    "spanish": "spain", "italian": "italy", "french": "france", "greek": "greece",
    "turkish": "turkey", "moroccan": "morocco", "portuguese": "portugal",
    "english": "england", "scottish": "scotland", "irish": "ireland", "american": "usa",
    "cuban": "cuba",
    "egyptian": "egypt", "tunisian": "tunisia", "polish": "poland", "croatian": "croatia",
    "icelandic": "iceland", "thai": "thailand", "vietnamese": "vietnam", "chinese": "china",
    "japanese": "japan", "indian": "india", "mexican": "mexico", "austrian": "austria",
    "belgian": "belgium", "canadian": "canada", "australian": "australia",
    "argentinian": "argentina", "argentine": "argentina", "brazilian": "brazil",
    "peruvian": "peru", "korean": "south korea", "lebanese": "lebanon", "israeli": "israel",
    "nigerian": "nigeria", "kenyan": "kenya", "south african": "south africa",
    "welsh": "wales", "swedish": "sweden", "danish": "denmark", "swiss": "switzerland",
    "russian": "russia", "singaporean": "singapore", "malaysian": "malaysia",
    "indonesian": "indonesia", "filipino": "philippines", "pakistani": "pakistan",
    "sri lankan": "sri lanka", "norwegian": "norway", "zealand": "new zealand",
}
_A_COUNTRY = tuple(FOOD_IN) + ("britain", "holland") + tuple(FOOD_ADJECTIVES)


def _not_a_plate(clean):
    return any(re.search(r"(?<![a-z])" + re.escape(word) + r"(?![a-z])", clean)
               for word in _FOOD_NOT_A_TRIP)


def _food_there(memory, understood):
    clean = str(understood.get("clean") or understood.get("text") or "").lower()
    if _not_a_plate(clean):
        return None
    if _find_in(clean, CHEAP_EATS):
        return None
    place = _find_in(clean, FOOD_IN)
    if not place:
        place = FOOD_ADJECTIVES.get(_find_in(clean, FOOD_ADJECTIVES) or "", "")
    if not place:
        city = _find_in(clean, CITY_COUNTRY)
        place = CITY_COUNTRY.get(city or "", "")
    if not place:
        city = _place_in(memory, understood, CITY_COUNTRY)
        place = CITY_COUNTRY.get(city or "", "")
        if not place:
            place = _place_in(memory, understood, FOOD_IN)
        if place and not _a_trip_to(place, memory, understood):
            return None
    if place not in FOOD_IN:
        return None
    if re.search(r"(?<![a-z])(?:from|born in|raised in|grew up in)\s+(?:the\s+)?"
                 + re.escape(place), clean):
        return None
    name = "the USA" if place == "usa" else place.title()
    return f"In {name}: {FOOD_IN[place]}"


_ESSENTIALS_ASK = ("essentials", "checklist", "what do i need", "what will i need", "do i need",
                   "will i need", "what do we need", "must i have", "have to have",
                   "what do i have to get", "what do i need to get", "what do i need to sort out",
                   "need anything", "need something", "need to sort",
                   "need for a trip", "need for the trip", "need for a holiday",
                   "need for the holiday", "need for a week in", "need before i go")


def _trip_essentials(memory, understood):
    text = ("Sort the paperwork first: anywhere abroad, that is a passport with six months left on "
            "it when you come back, travel insurance taken out the day you book rather than the day "
            "you fly, and your booking, policy and passport photo page saved on your phone so they "
            "work with no signal.")
    place = _place_in(memory, understood, PLUG_TYPES)
    if place:
        letter, shape, note = PLUG_TYPES[place]
        bits = []
        if letter != "G":
            bits.append(f"{place.title()} uses type {letter} sockets, so British plugs need an "
                        f"adapter")
        if place in WATER:
            if WATER[place]:
                bits.append("the tap water is fine to drink")
            else:
                bits.append("the tap water is not safe to drink, so bottled or filtered")
        if bits:
            text += " " + "; ".join(bits) + "."
    return text


_A_WALK_IS_SAID = re.compile(r"\b(walk|walks|walking|walked|stroll|strolls|strolling|"
                             r"path|paths|route|routes|rambl\w*|ramble|ramble)\b", re.IGNORECASE)


def _not_the_flat_the_ground(understood):
    if isinstance(understood, dict):
        said = understood.get("text") or understood.get("clean") or ""
        if not said:
            said = " ".join(understood.get("words") or ())
        if not not_the_flat_of_something_made(understood):
            return False
        if _A_WALK_IS_SAID.search(str(said)):
            return True
    return not_the_flat_you_live_in(understood)
def _a_visit_to_a_home(understood):
    care = (understood or {}).get("care_home") if isinstance(understood, dict) else None
    return isinstance(care, dict) and str(care.get("shape") or "") == "bring"


_A_TIME_LEFT = re.compile(
    r"\b(\d{1,3}|a|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s*"
    r"(months?|weeks?|days?)\b", re.I)
_A_VALIDITY_WORD = re.compile(r"\bvalid\b|\bexpir|\bruns? out\b|\bleft\b|\benough\b"
                              r"|\bfly\b|\bflying\b|\btravel\b|\btrip\b|\bget in\b"
                              r"|\bget in to\b|\benter\b", re.I)
_UNDER_SIX = re.compile(r"\b(?:under|less than|fewer than|not)\s+(?:six|6)\b"
                        r"|\bshort of six\b", re.I)
_ABOUT_THE_PASSPORT = re.compile(r"passports?|visas?|valid|expir\w*|renew\w*|enough"
                                 r"|left|remaining|runs?\b", re.I)
_ABOUT_THE_JOURNEY = re.compile(r"\bfly|\bflying|\btravel|\btrip\b|\bholiday|\bgo\b|\bgoing\b"
                               r"|\bget in\b|\benter\b|\baway\b|\babroad\b", re.I)
_NEAR_ENOUGH = 6
_NUMBER_WORDS = {"a": 1, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
                 "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12}


def _the_time_left(said):
    words = said.split()
    marks = [i for i, word in enumerate(words) if _ABOUT_THE_PASSPORT.search(word)]
    if not marks:
        marks = [i for i, word in enumerate(words) if _ABOUT_THE_JOURNEY.search(word)]
    if not marks:
        return None
    best = None
    for match in _A_TIME_LEFT.finditer(said):
        first = len(said[:match.start()].split())
        last = first + len(match.group(0).split()) - 1
        away = min(abs(mark - word) for mark in marks for word in (first, last))
        if away > _NEAR_ENOUGH:
            continue
        if best is None or away < best[0]:
            best = (away, match.group(1), match.group(2).lower())
    if best is None:
        return None
    return best[1], best[2]


def _the_passport_verdict(understood):
    said = understood.get("text") or understood.get("clean") or "" \
        if isinstance(understood, dict) else ""
    said = " ".join(str(said).lower().replace("\u2019", "'").split())
    if not _A_VALIDITY_WORD.search(said):
        return ""
    too_little = "No - that is too little time left"
    if _UNDER_SIX.search(said):
        return too_little
    match = _the_time_left(said)
    if not match:
        return ""
    token, unit = match
    count = int(token) if token.isdigit() else _NUMBER_WORDS.get(token, 99)
    if unit.startswith("day"):
        return too_little
    if unit.startswith("week") and count < 26:
        return too_little
    if unit.startswith("month") and count < 6:
        return too_little
    return ""


ENTRIES = [

    entry("food-in-the-country", (_FOOD_WORDS, _FOOD_SHAPE + _A_COUNTRY),
          _food_there,
          avoid=_FOOD_NOT_A_TRIP,
          bias=1),

    entry("where-in-month",
          (_month_names(), _MONTH_ASK),
          _a_month_verdict_once,
          avoid=("pack", "packing", "packed", "suitcase", "luggage", "what to bring",
                 "what to wear", "bring", "wear", "going to", "we are going", "we're going",
                 "im going", "i'm going", "nights", "night in", "booked", "booking", "book a",
                 "flights", "flight", "hotel"),
          bias=1),
    entry("month-verdict-followup",
          (_A_MONTH_POINTED_AT, _A_TIME_VERDICT_ASK),
          _a_month_verdict_pointed_at,
          avoid=("book", "booking", "booked", "flight", "flights", "fly", "flying", "price",
                 "prices", "cost", "costs", "how much", "cheap", "cheapest", "expensive",
                 "visa", "insurance", "hotel", "hotels"),
          bias=4),
    entry("plan-a-trip", (_PLAN_TALK, _PLAN_SHAPE), _trip_plan,
          avoid=("passport", "insurance", "checklist", "before i go", "before we go",
                 "need to do", "what do i need", "prescriptions", "jabs", "visa",
                 "where do i start", "do i start", "do first", "with kids", "with a baby",
                 "with a toddler", "with children", "abroad", "city break", "with a dog",
                 "with dogs", "with my dog", "with a pet", "with pets"),
          bias=1),

    entry("capital-city", (("capital", "capital city"),
                           tuple(CAPITALS) + ("of", "country")), _capital, bias=1,
          avoid=("gains", "tax", "taxes", "punishment", "death penalty", "letters",
                 "letter", "capitalise", "capitalize", "capitalism", "investment", "invest",
                 "investor", "business", "businesses", "start up", "startup", "fund",
                 "funding", "pension", "mortgage", "loan", "venture", "social capital",
                 "human capital", "how much")),
    entry("city-guide", (tuple(CITIES),
                         ("days", "day", "weekend", "week", "see", "miss", "visit", "going",
                          "trip", "holiday", "things to do", "to do in", "do in", "what should we",
                          "what should i", "what can we", "recommend", "recommendations",
                          "restaurants", "restaurant", "eat", "food", "museum", "museums",
                          "bars", "nightlife", "itinerary", "guide", "worth",
                          "what about", "how about", "thoughts on", "what do you think of",
                          "what do you reckon to",
                          "where do i start", "where to start", "where should i start")),
          _guide, explain=True,
          avoid=("jet lag", "jetlag", "lag", "hot bath", "bubble bath", "bath bomb",
                 "take a bath", "have a bath", "bath mat", "bathtub", "bath tub", "bathroom",
                 "clean the bath", "clean my bath", "soak", "shower", "enough", "afford",
                 "budget", "cost", "costs", "how much", "per day",
                 "pack", "packing", "suitcase", "luggage", "what to bring", "what to wear",
                 "bring", "wear",
                 "best time", "good time", "time to visit", "time of year", "best season",
                 "what month", "which month", "best month", "month to visit",
                 "when should i go", "when should we go", "when to go", "too hot", "too cold",
                 "rainy season", "monsoon",
                 "day trip", "day trips", "day out", "nearby",
                 "how many days", "how many nights", "how long", "how much time", "enough time",
                 "too long", "too short", "worth staying", "days do i need", "days should",
                 "days should i", "nights do i need",
                 "planning a trip", "planning our trip", "planning the trip",
                 "booked a trip", "booked flights"),
          bias=2),
    entry("city-cheap-eats", (tuple(CHEAP_EATS) + tuple(CITIES) + ("eat there",),
                             ("eat", "eating", "eats", "food", "foods", "restaurant",
                              "restaurants", "lunch", "dinner", "cheap", "cheaply", "cheapest",
                              "good value", "street food", "market", "markets", "meal", "meals",
                              "breakfast", "snack", "snacks", "where to eat", "where should i eat",
                              "where can i eat", "places to eat", "something to eat")),
          _cheap_eats, bias=2, guard=_a_way_there_needs_no_eating,
          avoid=("cost", "costs", "price", "prices", "how much", "expensive", "afford", "budget",
                 "tip", "tipping", "service charge", "book", "booking", "reservation",
                 "vegetarian", "vegan", "gluten", "gluten free", "allergy", "allergic", "halal",
                 "kosher", "diet", "food poisoning", "ill", "sick", "tummy", "stomach",
                 "dog", "cat", "toddler", "baby", "kids menu", "high chair", "water", "tap water",
                 "wine", "beer", "coffee", "breakfast in", "hotel breakfast",
                 "flight", "flights", "fly", "flying", "airline", "airlines", "airfare",
                 "airport", "ticket", "tickets", "book a flight", "cheap flights",
                 "get there", "how do i get there", "getting there", "travel to",
                 "how do i get", "way to get", "way from", "get to", "get from", "getting from",
                 "train", "trains", "coach", "coaches", "bus", "buses", "drive", "driving")),
    entry("airport-parking",
          (("airport parking", "parking at the airport", "park at the airport",
            "park the car at the airport", "parking for the airport", "airport car park",
            "airport carpark", "long stay parking", "long stay car park", "park and ride",
            "park and fly", "meet and greet parking"),
           ("worth", "cheaper", "cheapest", "cheap", "cost", "costs", "how much", "should i",
            "better", "taxi", "train", "bus", "compare", "book", "booking", "pre book",
            "prebook", "long stay", "week", "weeks", "days", "or", "pay", "paying", "parking")),
          ("Pre-book it: the price at the barrier is often two or three times the pre-booked "
           "price for the same space, and the cheapest of all is usually a park-and-ride a few "
           "minutes out with a shuttle. Compare the total against the alternatives before you "
           "choose, because a week of parking often costs about what a taxi costs each way, and "
           "for two or three days the taxi, the train or a lift from a friend usually wins. Check "
           "the drop-off charge too, since many airports now charge for the kiss-and-fly lane."),
          bias=2,
          avoid=("terminal", "gate", "flight",
                 "flights", "delay", "delayed", "cancelled", "canceled", "lost", "stuck",
                 "check in", "checkin", "bag drop", "luggage", "baggage", "suitcase",
                 "transfer", "into the city", "to the city", "from the airport")),
    entry("country-trip", (tuple(WHERE_TO_GO) + tuple(COUNTRY_ALIASES), COUNTRY_TRIP_WORDS),
          _country_trip,
          avoid=tuple(CITIES) + NOT_A_COUNTRY_TRIP),
    entry("country-where-to-go",
          (("where should i go", "where should we go", "where do i go", "where to go",
            "where would you go", "where should i head", "where should i go in",
            "where should we go in", "where do i go in", "where to go in",
            "where would you go in", "where should i head in",
            "where should i visit in", "where to visit in", "where should we visit in",
            "where in", "where abouts in", "what city should i visit in",
            "what cities should i visit in", "which city should i visit in",
            "which cities should i visit in", "which city in", "which cities in",
            "what city in", "what cities in", "what should i visit in",
            "best city in", "best cities in", "best place in", "best places in",
            "best place to go", "best places to go", "best city to go", "best cities to go",
            "where would you recommend", "where do you recommend", "where would you suggest",
            "where do you suggest",
            "what about", "how about", "thoughts on", "what do you think of",
            "what do you reckon to", "anywhere in", "anywhere else in",
            "cities in", "places in"),
           tuple(WHERE_TO_GO) + tuple(COUNTRY_ALIASES)),
          _where_to_go,
          avoid=tuple(CITIES) + ("best time", "best month", "when should i go", "when to go",
                                 "too hot", "too cold", "month", "weather in", "visa",
                                 "how much money", "water",
                                 "move to", "moving to", "live in", "living in", "place to live", "to live",
                                 "living costs", "emigrate",
                                 "residency", "driving", "drive", "car hire", "hire car",
                                 "licence", "insurance", "safety", "safe", "dangerous",
                                 "crime", "school", "schools", "job", "jobs", "work in",
                                 "hospital", "doctor")),
    entry("holiday-costs",
          (("costs down", "cost down", "cost of a holiday down", "keep the cost", "cut the cost",
            "cut costs", "reduce the cost", "cheaper", "spend less", "less money on",
            "on a budget", "a budget holiday", "holiday on a budget",
            "money off a holiday", "money off the holiday", "money off my holiday",
            "money off our holiday", "money off a trip", "money off the trip",
            "bring the cost", "cheapest way to book", "keep it cheap"),
           ("how", "what", "should", "would", "could", "can", "do", "make", "keep", "get",
            "down", "we", "us", "i")),
          _holiday_costs,
          avoid=("save up", "saving up", "how much", "how far", "where can i go",
                 "where should i go", "where should we go", "when should i go", "best time",
                 "train", "trains", "rail", "by rail", "coach", "coaches", "bus", "buses",
                 "drive", "driving", "by car", "car", "cars", "petrol", "diesel", "fly",
                 "flying", "flight", "flights", "airport", "commute", "commuting",
                 "season ticket", "parking"),
          guard=a_price_not_a_loan,
          bias=2),
    entry("where-no-place", (HOLIDAY_ASK, HOLIDAY_SHAPE), _where_no_place,
          avoid=HOLIDAY_NOT, guard=_a_shortlist_question, bias=1),
    entry("want-a-trip", (_WANT_TRIP_SAID, _WANT_TRIP_SHAPE), _want_a_trip,
          avoid=_TRIP_OTHER_ROW,
          guard=_a_trip_is_wanted, bias=1),
    entry("city-followup", (("there", "that city"),
                            ("what should we do", "what should we see", "what should i do",
                             "what should i see", "what can i see", "what should i visit",
                             "what is there to see", "what is there to visit",
                             "what can we do", "recommend", "recommendations", "what about",
                             "anything else", "must see", "must do", "worth seeing",
                             "where should we eat", "what should we visit")),
          _guide_followup),
    entry("city-next", (("see", "visit", "eat", "miss", "walk", "stay"),
                        ("what", "should", "we", "i", "anything", "worth", "must", "now")),
          _guide_next,
          avoid=("there", "day trip", "day trips", "days", "weekend", "budget", "cost", "costs",
                 "how long", "how many days", "how many nights", "how much time", "nights",
                 "my son", "my daughter", "my kid", "my kids", "my child", "my children",
                 "toddler", "year old", "years old", "month old", "months old",
                 "how much", "pack", "packing", "airport", "flight", "hotel", "train",
                 "else", "another", "too",
                 "my streak", "the streak", "streak", "my habit", "my diet", "no sugar",
                 "my routine", "my resolution")),
    entry("city-detail", (("museums", "museum", "restaurants", "restaurant", "food", "bars",
                           "nightlife", "sights", "sightseeing", "shops", "shopping"),
                          ("there", "also", "too", "worth", "recommend", "what about", "any",
                           "should we", "can we", "anything")),
          _guide_followup),
    entry("city-best-time", (tuple(BEST_TIME) + tuple(CITY_COUNTRY) + tuple(WHEN_TO_GO),
                             ("best month", "best months", "best time", "when should i go",
                              "when to go", "when should we go", "when should you go",
                              "what month", "which month", "good time to go", "best season",
                              "good month", "best time of year", "what time of year",
                              "worth visiting", "worth a visit",
                              "worth going", "too hot", "too cold", "rainy season", "monsoon",
                              "time to visit", "good time", "time of year", "month to visit")),
          _best_time,
          bias=1),
    entry("region-days",
          (tuple(REGION_PLACES), _DAYS_ASK),
          _region_days,
          avoid=("best time", "best month", "when should i go", "when to go", "pack", "packing",
                 "suitcase", "hotel", "hotels", "cottage", "how long", "how many days",
                 "days in", "nights in", "cost", "costs", "how much", "budget", "price",
                 "flights", "flight", "train", "drive", "driving", "parking", "weather",
                 "rain", "rains", "raining", "pregnant", "dog", "dogs", "recipe", "recipes",
                 "pasty", "pastry", "pudding", "cook", "cooking", "bake", "baking",
                 "how do i get", "how do i get to", "get to", "how to get", "getting to",
                 "how far", "ferry", "ferries", "train", "bus", "drive", "driving"),
          bias=1),
    entry("city-stay", (tuple(CITY_DAYS),
                        ("how long", "how many days", "how many nights", "days should",
                         "days in", "nights in", "worth staying", "long should i stay",
                         "long should we stay", "enough time", "too long", "too short",
                         "how many days do i need", "how much time", "days", "nights")),
          _stay_length,
          avoid=("roast", "roasted", "roasting", "oven", "bake", "baked", "baking", "boil",
                 "boiled", "boiling", "steam", "steamed", "fry", "fried", "frying", "grill",
                 "grilled", "sprout", "sprouts", "florets", "recipe", "recipes", "sauce",
                 "soup", "side dish", "air fryer"),
          guard=_a_weight_is_the_kitchen),
    entry("country-stay-length", (tuple(WHERE_TO_GO),
                                  ("how long", "how many days", "how many nights",
                                   "how long should", "how long do", "days should", "days in",
                                   "nights in", "how much time", "how many days do we need",
                                   "enough time", "too long", "too short", "days", "nights")),
          _country_stay_length,
          avoid=("roast", "roasted", "roasting", "oven", "bake", "baked", "baking", "boil",
                 "boiled", "boiling", "steam", "steamed", "fry", "fried", "frying", "grill",
                 "grilled", "recipe", "recipes", "sauce", "soup", "stuffing", "thaw", "thawed",
                 "defrost", "freezer", "cook", "cooked", "cooking", "dinner", "christmas",
                 "thanksgiving", "sandwich", "salad", "spice", "spices",
                 "renewal", "renewals", "renew", "renewing", "passport", "licence", "license",
                 "application", "applying", "paperwork", "post it off", "delivered",
                 "delivery estimate", "refund", "claim form", "probate", "mortgage offer",
                 "planning permission", "referral", "waiting list"),
          guard=_a_weight_is_the_kitchen,
          bias=1),
    entry("city-stay-followup", (("there", "that city", "this city", "the city"),
                                 ("how long", "how many days", "how many nights", "enough time",
                                  "too long", "too short", "days", "nights", "stay", "spend")),
          _stay_there,
          avoid=("toddler", "baby", "newborn", "child", "children", "kid", "kids", "son",
                 "daughter", "wakes", "waking", "wake up", "bedtime", "nap", "naps", "sleep",
                 "slept", "asleep", "4am", "5am", "6am", "every morning")),
    entry("airport-arrival", (("airport", "airports", "flight", "flights", "plane", "planes",
                               "fly", "flying", "flight's",
                               "boarding", "check in", "check-in", "checkin", "departure",
                               "gate"),
                              ("how early", "how long before", "what time", "when should",
                               "get to the airport", "arrive at the airport", "leave for the "
                               "airport", "before my flight", "before the flight", "hours before",
                               "how long do i need", "enough time", "too early", "enough",
                               "hours", "minutes", "how long", "leave at", "set off", "set out",
                               "miss my flight", "make my flight", "in time", "plenty of time",
                               "what time do i", "when do i", "when is", "how early do i",
                               "when does", "when do", "when will",
                               "leaving home", "leave home", "leaving at", "leaves at",
                               "leaving for the airport", "leave for the airport", "long flight",
                               "flight time", "how many hours", "is it a long")),
          _airport_early,
          avoid=("what time is my flight", "when is my flight", "what time is our flight",
                 "when is our flight", "what time do i fly", "when do i fly",
                 "what time am i flying", "when am i flying", "what time does my flight land",
                 "what gate", "which gate",
                 "when do we fly", "when do we fly out", "when do we leave", "when are we flying",
                 "what time is the flight", "what time is our flight", "what time do we fly",
                 "what time are we flying", "what time do we leave"),
          ask=("how early", "how long", "what time", "when", "should", "do i need", "need to be",
               "enough", "too early", "advice", "hours", "minutes", "is it worth", "will i",
               "if i", "is it", "can i", "leave at", "leaving at", "leaves at", "set off",
               "setting off", "set out", "in time", "leave home", "leaving home",
               "leave the house", "leaving the house")),
    entry("my-flight-time", (("flight", "flights", "plane", "flying", "boarding pass", "land",
                              "lands", "landing"),
                             ("what time is my", "when is my", "what time is the", "when is the",
                              "what time does my", "when does my", "what time do i fly",
                              "when do i fly", "what time am i flying", "when am i flying",
                              "when do we fly", "when do we fly out", "what time do we fly",
                              "when are we flying", "what time are we flying",
                              "when do we leave", "what time do we leave",
                              "what time is our flight", "when is our flight",
                              "what terminal", "which terminal", "what gate", "which gate",
                              "what time does the flight land", "what time does it land",
                              "what time do we land", "what time will we land",
                              "what time do i land", "when do we land", "when does the flight "
                              "land", "when do i land")),
          _my_flight_time),
    entry("airport-to-city", (tuple(AIRPORT_TRANSFER) + ("airport",),
                              ("to the centre", "to central", "city centre", "into town",
                               "to the city", "from the airport", "airport to", "transfer",
                               "get to", "get from", "how do i get", "cheapest way", "taxi",
                               "train from", "bus from")),
          _airport,
          avoid=("closest airport", "nearest airport", "which airport", "what airport",
                 "how early", "how long before", "how many hours before", "how soon",
                 "what time should i", "when should i get", "get there", "arrive at the airport",
                 "get around", "getting around", "get round", "getting round", "around town",
                 "airport to fly into", "airport do i", "airport should i", "airport closest",
                 "which london airport", "airport is closest", "airport is nearest",
                 "airport near the", "airport nearby",
                 "scam", "scammed", "ripped off", "rip off", "overcharge", "overcharged",
                 "meter", "rigged", "cheated", "ripped me",
                 "expensive", "how much is a taxi", "fare",
                 "how much", "cost", "costs", "price", "prices", "fares", "advance",
                 "flights", "flight", "airline", "airlines", "fare", "fares", "deal", "deals",
                 "book", "booking", "compare",
                 "how early", "how long before", "before my flight", "before the flight",
                 "what time should i", "arrive at the airport")),
    entry("arriving-into-town", (tuple(_ARRIVAL_KINDS) + ("train", "coach", "bus"),
                                 tuple(_ARRIVING_ASK)),
          _arriving,
          avoid=("pack", "packing", "what to take", "what should i take", "what do i need for a",
                 "hotel to stay", "which hotel", "best hotel", "cheap hotel", "book a hotel",
                 "where to stay", "price", "prices", "cheapest fare", "tickets to",
                 "how early", "how long before", "should i book", "worth visiting", "what to see",
                 "airport transfer", "from the airport", "parking", "left luggage", "lost property",
                 "journey", "long journey", "hours on the",
                 "by coach", "by train", "by bus", "by rail", "by car", "by plane",
                 "a train to", "a coach to", "a bus to", "coach to", "train to",
                 "overnight coach", "overnight train", "between two cities", "how long does",
                 "ticket", "tickets", "railcard", "advance", "off-peak", "off peak",
                 "fares", "cheap train", "cheaper train", "cheapest train",
                 "train times", "timetable", "train prices",
                 "refund", "refunds", "refunded", "money back", "compensation", "claim",
                 "claims", "complain", "complaint", "delay", "delayed", "cancelled",
                 "canceled", "missed", "miss the", "last bus", "last train", "last coach",
                 "last tram", "stranded", "did not turn up", "didnt turn up",
                 "no bus came")),
    entry("city-airport", (tuple(AIRPORT_NAME),
                           ("closest airport", "nearest airport", "which airport", "what airport",
                            "airport to fly into", "fly into", "airport do i", "airport should i",
                            "airport is closest")),
          _city_airport),
    entry("city-day-trip", (tuple(DAY_TRIPS),
                            ("day trip", "day trips", "day out", "nearby", "near here",
                             "close to", "what else")),
          _day_trip, bias=2),
    entry("city-transit", (tuple(CITY_TRANSIT) + tuple(TRANSIT_CARDS) + CARD_NAMES,
                           ("get around", "getting around", "get about", "getting about",
                            "around town", "get round", "getting round",
                            "metro", "subway", "underground", "tube", "u-bahn", "tram", "trams",
                            "bus", "buses", "public transport", "transport", "transit",
                            "travelcard", "travel card", "day pass", "oyster", "metro card",
                            "how do i travel", "how do people travel",
                            "card", "cards", "pass", "top up", "contactless", "chipkaart")),
          _transit,
          avoid=("airport", "flight", "flights", "fly into", "train to", "train from",
                 "train ticket", "book", "booking", "hotel", "day trip", "day trips",
                 "worth visiting", "best time to go", "car hire", "rent a car", "hire a car",
                 "bus to", "bus from",
                 "cheapest", "cheap", "flight", "flights", "airline", "compare", "deal"),
          bias=1),
    entry("trip-budget", (tuple(DAILY_BUDGET),
                          ("enough", "enough for", "will that be enough", "is that enough",
                           "budget",
                           "budget for", "cost", "costs", "afford", "money", "spend",
                           "spending", "expensive", "pricey", "will that do", "will that cover",
                           "cheap", "cheaper", "inexpensive", "affordable", "worth it",
                           "does that cover", "go far", "saved", "pounds", "euros", "dollars",
                           "how much is a week", "how much is a weekend", "how much is a trip",
                           "how much for a week", "how much for a weekend", "much is a week",
                           "much is a fortnight", "much is ten days", "much is five days",
                           "much is four days", "much is three days", "much is two weeks",
                           "spending money", "spending cash")),
          _trip_budget,
          bias=1,
          avoid=("train", "trains", "flight", "flights", "ticket", "tickets", "fare", "fares",
                 "hotel", "hotels", "insurance", "passport", "visa",
                 "send money", "sending money", "send some money", "transfer", "transferring",
                 "remittance", "rent", "rents", "mortgage", "salary", "wage", "wages",
                 "cost of living", "live in", "lives in", "living in", "moved to",
                 "moving to", "exchange rate", "currency",
                 "money should i take", "cash should i take", "money to take", "cash to take",
                 "how much cash", "take in cash",
                 "carry", "carrying", "carried", "money belt", "safe", "safely", "stolen",
                 "wallet", "pickpocket")),
    entry("pack-cold-city", (("pack", "packing", "take", "wear", "clothes", "bring",
                              "carry"),
                             ("cold", "winter", "december", "january", "february", "november")),
          ("Pack for 2 to 8C, wind and rain: a waterproof coat with a hood, warm layers you can "
           "take off indoors, and shoes you can walk a hill in. It gets dark around 4pm in "
           "December, so a small torch and plans for the afternoon indoors help."),
          ask=("pack", "packing", "take", "taking", "wear", "wearing", "bring", "carry",
               "coat", "clothes", "suitcase", "luggage", "shoes", "boots"),
          avoid=("ill", "illness", "sick", "symptom", "fever", "cough", "sore throat", "medicine",
                 "vitamin", "vitamins", "supplement", "supplements", "vaccine", "jab", "dose",
                 "tablet", "tablets", "medication",
                 "ibuprofen", "paracetamol", "antibiotic", "antibiotics", "doctor", "pharmacy",
                 "cold sore", "cold sores", "herpes", "lip", "lips",
                 "shower", "bath", "sauna", "beer", "drink", "day off", "wedding", "funeral",
                 "interview", "party",
                 "inhaler", "insulin", "statin", "statins", "prescription", "hayfever",
                 "hay fever", "chest infection",
                 "lunch", "lunchbox", "lunch box", "packed lunch", "sandwich", "sandwiches",
                 "food", "leftovers", "meal",
                 "got a cold", "have a cold", "caught a cold", "catch a cold", "my cold",
                 "cold and flu", "head cold", "chesty", "runny nose",
                 "blocked nose", "sneezing", "sniffles", "the flu", "got flu", "have flu",
                 "store", "storing", "storage", "put away", "pack away", "packed away",
                 "moth", "moths", "cedar", "loft", "under the bed"), bias=1),
    entry("pack-city-break", (("city break", "city trip", "citybreak"),
                              ("pack", "packing", "take", "taking", "wear", "wearing", "bring",
                               "carry", "clothes", "coat", "shoes", "boots", "bag", "case")),
          _city_pack,
          avoid=("money", "budget", "spending", "cash", "cost", "hotel", "flight", "flights"),
          bias=1),
    entry("train-journey-packing", (("train", "trains", "rail", "railway",
                                     "coach trip", "coach journey", "by coach", "on a coach",
                                     "on the coach", "coach for", "trip on a coach",
                                     "coach to", "bus journey", "bus trip"),
                                    ("pack", "packing", "take", "bring", "need", "wear", "bag",
                                     "journey", "journeys", "ride", "trip", "tips", "advice",
                                     "hours", "for hours")),
          "Tickets first, with a screenshot as well as the app, because signal in a tunnel is not "
          "a plan. Then water and a snack, a layer you can take off, a charger and headphones, "
          "and your seat reservation if you have one. On a long journey add a pillow, a book and a "
          "spare top for a delay, and keep the bag small enough to lift overhead yourself.",
          ask=("train", "trains", "rail", "railway", "coach trip", "coach journey",
               "by coach", "on a coach", "on the coach", "coach for", "trip on a coach",
               "coach to", "bus journey", "bus trip"),
          guard=_the_journey_in_the_line,
          avoid=("train set", "train sets", "potty", "toilet", "toilet training", "model",
                 "train a week", "train every day", "train each day", "training for",
                 "how many hours", "should i train", "i train", "hours a week",
                 "how long", "how far", "what time", "how much is", "how much does",
                 "pack for", "packing for", "how do i pack", "what do i pack",
                 "with a toddler", "with a baby", "with my son", "with my daughter",
                 "my son", "my daughter", "my kids", "my children",
                 "pushchair", "pushchairs", "buggy", "buggies", "pram", "prams",
                 "stroller", "wheelchair", "mobility scooter",
                 "how long to train", "long to train", "how long to practice",
                 "good for a", "good for the", "good for my", "that one good", "is that one",
                 "is this one", "would that one", "would this one",
                 "how much", "cost", "price", "fare", "fares", "ticket price", "delay", "delayed",
                 "cancelled", "cancellation", "strike", "strikes", "refund", "seat reservation only",
                 "dog", "cat", "bike", "bicycle")),
    entry("city-weather", (("weather", "too cold", "too hot", "too wet", "too windy",
                            "too rainy", "too warm", "warm enough", "cold enough", "hot enough",
                            "cold in", "warm in", "hot in", "rainy in", "rain in"),
                           ("like", "usually", "month", "warm", "cold", "rain",
                            "go", "going", "visit", "visiting", "trip", "holiday", "there",
                            "time to", "worth")),
          _weather, bias=1),

    entry("jet-lag-east", (("jet lag", "jetlag"), JET_EAST_KEYS),
          ("Fly east and your body has to run ahead, so shift your bedtime 30 minutes earlier for "
           "a few nights before you go, then get out in morning light at the other end. Skip "
           "caffeine after midday there and stay up until at least 10pm local."), bias=1),
    entry("jet-lag-west", (("jet lag", "jetlag"), JET_WEST_KEYS),
          ("Flying west stretches your day, so go to bed an hour later than usual for the last two "
           "or three nights before you go, then sleep in a little at the other end and get "
           "afternoon daylight. Stay up to 10pm local on night one rather than napping, which is "
           "what leaves you awake at 3am."), bias=1),
    entry("jet-lag-baby", (("jet lag", "jetlag"),
                           ("baby", "babies", "toddler", "kid", "kids", "child", "children",
                            "newborn")),
          ("Keep the baby on their usual routine and move it by an hour a night once you land, "
           "feed on local meal times, and get them out in morning daylight: light does the work. "
           "A night flight that lands in the evening is easier than one that lands at noon, and "
           "plan one quiet day at the other end."), bias=1),
    entry("time-there", (("time difference", "time zone", "whats the time", "what time is it",
                          "what is the time", "the time in", "local time", "hours ahead",
                          "hours behind", "ahead of us", "behind us", "how many hours ahead",
                          "same time", "clock in", "morning or evening", "day or night",
                          "awake yet", "asleep yet"),
                         tuple(TIME_ZONES) + tuple(MULTI_ZONES)),
          _time_zone),
    entry("time-here", (("what time is it", "whats the time", "what is the time",
                         "the time now", "got the time", "know the time", "what oclock",
                         "what o'clock",
                         "tell me the time", "the time please", "have the time", "the time"),
                        ("time", "clock", "oclock", "o'clock", "now", "here")),
          _the_clock_here),
    entry("body-clock-travel", (("body clock", "internal clock", "time zone", "sleep clock"),
                         ("reset", "shift", "fix", "adjust", "all over", "wrong", "out of", "back",
                          "sort")),
          ("Fix it with light and meals rather than willpower: get outside in the morning, keep "
           "the evening dim, eat at the new meal times and move bedtime 30 minutes a night rather "
           "than all at once. No long naps, and no caffeine after lunch while it settles.")),
    entry("jet-lag", (("jet lag", "jetlag"), ("over", "cure", "fix", "avoid", "better", "help",
                                              "deal", "dealing", "tired", "sleep", "survive",
                                              "stop", "prevent", "preventing", "getting",
                                              "beat", "reduce", "less", "worse")),
          ("Get daylight as soon as you can after landing, eat at local meal times, and keep "
           "caffeine to the local morning. Sleeping on arrival makes it worse; a short 20-minute "
           "nap before 3pm is the most you want.")),
    entry("eiffel-steps", (("eiffel tower", "eiffel"), ("steps", "stairs", "climb", "walk up",
                                                         "how many")),
          "674 steps to the second floor and 1,665 to the top. Most people walk up to the second "
          "floor (10 to 15 minutes and no queue) and take the lift from there; the stairs above "
          "the second floor are for the very keen."),
    entry("airport-security", (("security", "scanner", "pat-down"),
                               ("happens", "like", "through", "expect", "first", "what",
                                "take out", "laptop", "shoes", "belt", "liquids")),
          ("You put your bag in a tray, take out laptops and liquids (100ml in a clear bag), and "
           "walk through a scanner, sometimes with a pat-down. It takes ten minutes and nobody "
           "minds how nervous you are, so just follow what the staff say and give yourself two "
           "hours before the flight."),
          avoid=("sandwich", "sandwiches", "food", "snack", "snacks", "lunch", "picnic",
                 "bottle", "bottles", "water", "liquid", "liquids", "100ml",
                 "closest", "nearest", "into",
                 "screen", "monitor", "keyboard", "clean", "cleaning", "cracked", "repair",
                 "printer", "phone", "tv", "television", "password",
                 "code", "codes", "text", "texts", "texting", "message", "messages", "sms",
                 "otp", "pin", "pins", "login", "log-in", "account", "account", "hacked", "spam"),
          bias=1),
    entry("flight-food", (("sandwiches", "food", "snacks", "snack", "packed lunch",
                           "packed lunches", "lunch", "lunches", "meal", "meals", "picnic",
                           "fruit", "crisps", "chocolate", "leftovers"), FLIGHT),
          FLIGHT_FOOD, bias=1),
    entry("flight-liquids", (("liquids", "liquid", "bottle", "water", "100ml", "100 ml",
                              "clear bag", "liquid rules"), FLIGHT), FLIGHT_LIQUIDS, bias=1),
    entry("flight-food-followup", (("sandwiches", "snacks"), ("take", "bring", "own", "allowed")),
          _flight_followup(FLIGHT_FOOD), bias=-2),
    entry("flight-liquids-followup", (("liquids", "bottle", "water", "drink"),
                                      ("take", "bring", "own", "allowed")),
          _flight_followup(FLIGHT_LIQUIDS), bias=-2),
    entry("flight-nervous", (("never", "first time", "nervous", "scared"), ("flown", "flying",
                                                                           "flight", "plane")),
          ("It's genuinely a safe way to travel, and the first flight is mostly boring: check in, "
           "security, wait, board, sit. Tell the cabin crew it's your first time if you're "
           "nervous; they're used to it and always look after you.")),
    entry("plane-recline", (("recline", "reclining"), ("seat", "plane", "ok", "rude", "ever")),
          ("Leaning back is fine and nobody thinks worse of you, but do it slowly and check behind "
           "you, because it can land on someone's laptop. Avoid mealtimes if you can, and don't "
           "keep it back for the whole flight in the front row of economy.")),
    entry("flight-extras",
          (("priority boarding", "priority boarding pass", "speedy boarding", "extra legroom",
            "legroom", "seat selection", "choose my seat", "pick my seat", "pay for a seat",
            "exit row", "extra leg room"),
           ("worth", "worth it", "pay", "paying", "paid", "extra", "should i", "is it", "buy")),
          _flight_extras, bias=1,
          avoid=("refund", "cancel", "compensation", "delay", "delayed", "lost", "hotel",
                 "car hire", "hire car", "insurance", "lounge", "fast track", "fast-track")),
    entry("long-flight", (("long flight", "long flights", "10 hour flight",
                           "12 hour flight", "twelve hour flight", "fourteen hour flight",
                           "overnight flight", "night flight", "8 hour flight",
                           "how do i survive the flight", "survive a flight",
                           "comfortable flight", "flight comfortable"),
                          ("how", "tips", "advice", "make", "get through", "survive", "cope",
                           "comfortable", "better",
                           "what can i do", "what to do", "what do i do", "pass the time",
                           "keep busy", "keep occupied", "entertain", "keep a child busy",
                           "keep the kids busy")),
          "Book the seat you can sleep in if it is overnight, then treat it as a day with no work "
          "in it: water instead of the wine, a proper meal before you board rather than the tray, "
          "and stand up every couple of hours to walk to the back. Compression socks and shoes "
          "with room in them are worth more than any gadget; an eye mask, earplugs and a spare "
          "toothbrush turn the last three hours into a rest. Put a change of clothes, your "
          "medicines and a charger in the bag under the seat, and set your watch to the new time "
          "when you board.",
          avoid=("cheap", "cheapest", "cheaper", "fares", "price", "prices", "deal", "deals",
                 "book", "booking", "swollen", "swelling", "clot", "dvt", "calf", "leg pain",
                 "afraid", "scared", "fear of flying", "panic", "anxious", "turbulence",
                 "delayed", "delay", "cancelled", "compensation", "jet lag", "snore",
                 "baby", "toddler", "child", "kids", "dog", "pet", "luggage lost", "lost bag",
                 "wear", "wearing", "clothes", "clothing", "pack", "packing", "take", "bring",
                 "luggage", "bad for you", "bad for me", "healthy", "unhealthy", "safe",
                 "dangerous", "pregnant", "pregnancy", "dvt risk",
                 "how do i sleep", "sleep on a", "sleep on the", "get to sleep", "fall asleep"),
          bias=1),
    entry("flight-tips", (("cheap", "cheapest", "tips"), ("flights", "flight", "flying")),
          ("Be flexible on dates and airports and book eight to six weeks ahead for Europe, longer "
           "for long-haul. Tuesday and Wednesday flights are usually cheapest, and luggage fees "
           "often close the gap between budget and full-service airlines.")),
    entry("cheap-trains", (("train", "trains", "rail", "railcard", "railcards", "rail card"),
                           ("cheap", "cheaper", "cheapest", "advance", "early", "book", "ticket",
                            "tickets", "save", "worth", "get", "pay", "pays", "much", "cost",
                            "costs")),
          _cheap_trains,
          avoid=("toy", "toys", "set", "sets", "model", "models", "wooden", "gym", "exercise",
                 "workout", "trainer", "trainers", "at home",
                 "train a week", "train a month", "train each week", "train every week",
                 "train twice", "train three", "train four", "how much should i train",
                 "how often should i train", "how many times a week should i train",
                 "run a week", "run each week", "run every week",
                 "a book for", "book for the", "books for the", "something to read", "reading",
                 "or the train", "or a train", "or the bus", "or a bus", "or the coach",
                 "or a coach", "or drive", "or park", "or walk", "or cycle",
                 "refund", "refunds", "money back", "delay repay", "cancelled", "canceled",
                 "delayed", "compensation")),
    entry("passport-lost", ("passport", ("lost", "lose", "losing", "stolen", "missing", "left")),
          _passport_lost, bias=1,
          avoid=("at home", "in my bag", "in my other", "back at", "in the hotel", "at the hotel",
                 "before i fly", "left it at",
                 "months left", "weeks left", "days left", "left on it", "valid", "expires",
                 "expiring", "runs out", "six months", "enough time")),
    entry("passport-left-behind", ("passport", ("at home", "forgot", "forgotten", "left it",
                                                "in the hotel", "at the hotel", "back at",
                                                "left behind", "on the kitchen table")),
          ("Tell the airline desk as soon as you know - the booking is still yours, so they can "
           "usually move you to a later flight, and someone can bring the passport to the airport "
           "if there is time. If it is at a hotel, ask them to hold it and courier it to you; a "
           "photo of it will not get you through security.")),
    entry("passport-valid", ("passport", ("valid", "still valid", "valid for", "six months",
                                          "enough time", "months left", "weeks left", "runs out",
                                          "expires", "expiring", "fly", "travel in",
                                          "days left", "days to go", "weeks to go",
                                          "travel with", "travel on", "fly with", "get in on")),
          ("Most countries want six months left on your passport beyond the day you plan to "
           "return, and some also want it issued within the last ten years. Check your "
           "destination's rule on its embassy site before you book: if you are close to the "
           "line, renew first rather than risk being turned away at the airport."),
          lead=("yesno", _the_passport_verdict),
          avoid=("lost", "stolen", "missing", "renew", "how long",
                 "expired", "has expired", "ran out", "out of date")),
    entry("passport-safe",
          (("passport", "passports", "travel documents", "id card"),
           ("safe", "keep it safe", "keep safe", "keep my passport", "keep it",
            "where should i keep", "where to keep", "where do i keep", "carry", "on me",
            "inside pocket", "money belt", "beach", "pickpocket", "pickpockets",
            "hotel safe", "with me", "protect")),
          ("Carry it on you, in a zipped inside pocket or a money belt, and not in a back pocket or "
           "an open beach bag. Put a photo of the ID page in your own email: it makes a replacement "
           "far quicker and it costs nothing. A hotel safe is fine while you are in the room, but "
           "keep the passport with you on travel days. If it is taken, report it to the police and "
           "go to your embassy for an emergency travel document."),
          avoid=("lost", "lose", "losing", "stolen", "missing", "left", "forgot",
                 "forgotten", "valid", "expires", "expiring", "runs out", "renew",
                 "renewal", "apply", "how long", "how much", "visa", "photo booth",
                 "change my name", "child", "baby")),

    entry("suitcase-protect",
          (("suitcase", "suitcases", "luggage", "baggage", "checked bag", "checked luggage",
            "hold bag", "holdall", "hold luggage"),
           ("protect", "damaged", "damage", "burst", "bursting", "bursts", "zip", "zips",
            "zipper", "strap", "cracked", "broken", "scratched", "wheel", "wheels",
            "thrown about", "rough handling", "airline broke", "came back broken",
            "zip bursting", "zip burst", "zip broke", "zip broken", "zip split",
            "replacement wheels", "lost wheel", "broken wheel")),
          _suitcase_protect,
          avoid=("zip file", "file", "files", "folder", "computer", "laptop", "password",
                 "pack", "packing", "what should i pack", "what to pack", "lost", "missing",
                 "never arrived", "delayed", "delayed flight", "tracker", "airtag",
                 "hand luggage", "carry on", "carry-on"),
          bias=1),

    entry("packing-a-car-journey",
          (("what should i take", "what do i take", "what should i pack", "what do i pack",
            "what do i need", "what should i bring", "what do i bring", "pack", "packing",
            "take with me", "bring with me"),
           ("car journey", "car trip", "long drive", "long car journey", "long journey",
            "drive down", "driving down", "in the car", "motorway", "driving holiday")),
          "Water and snacks that do not crumble, so nobody is eating crumbs at 70mph: a refillable "
          "bottle each, fruit, and something savoury in a tub. Then a phone cable and a power bank, "
          "the breakdown and insurance details, a blanket or a spare layer each, wet wipes and a "
          "bag for rubbish, sunglasses, and cash or a card for parking and toilets. Plan a stop "
          "every two hours, and put the first night's bag where you can reach it.",
          avoid=("weekend", "two nights", "three nights", "week away", "a week", "fortnight",
                 "flight", "flying", "plane", "airport", "hand luggage", "carry on", "carry-on",
                 "cabin bag", "moving house", "move house", "removal", "won't start", "wont start",
                 "battery", "flat tyre", "puncture", "overheat", "breakdown cover cost")),
    entry("packing-a-flight",
          (("what should i take", "what do i take", "what should i pack", "what do i pack",
            "what do i need", "what should i bring", "what do i bring", "pack", "packing",
            "take with me", "bring with me", "forgot to pack"),
           ("flight", "plane", "airport", "flying", "long flight", "flight bag", "holiday flight")),
          "Passport, the boarding pass on the phone and a screenshot of it, because the airport "
          "wifi is not a plan. Chargers and a power bank go in the cabin bag, not the hold, and so "
          "do medicines in their original boxes with the repeat slip. Liquids are 100ml each in "
          "one clear bag; a spare layer, an empty bottle to fill after security and a snack get "
          "you through a delay. Put one change of clothes in the cabin bag in case the suitcase "
          "takes a later flight.",
          avoid=("hand luggage", "carry on", "carry-on", "cabin bag", "allowance", "how many ml",
                 "100ml", "liquid rules", "how much does", "car", "car journey", "long drive",
                 "week", "weekend", "train", "ferry", "moving house")),
    entry("packing-weekend", (("pack", "packing"),
                              ("weekend", "trip", "break", "days", "city") + tuple(CITIES)),
          ("For two or three nights: one change of clothes plus a layer, one pair of comfortable "
           "walking shoes, toiletries in a bag, phone charger and any tickets. Roll clothes to fit "
           "more in, and leave the \"just in case\" outfit at home."),
          avoid=("house", "moving", "move", "moved", "flat", "home", "boxes", "removals",
                 "plates", "crockery", "mugs", "fragile",
                 "smoke", "smoked", "smoker", "smokers", "smoking", "cigarette", "cigarettes",
                 "cigs", "nicotine", "vape", "vaping")),
    entry("packing-week", (("pack", "packing", "suitcase", "what should i take",
                            "what do i take", "what should i bring", "what do i bring"),
                           ("week", "week away", "a week", "two weeks", "10 days", "ten days",
                            "fortnight", "days away", "long trip", "holiday")),
          ("For a week: five tops, three bottoms, two layers, one pair of shoes you can walk in "
           "and one smarter pair, plus a waterproof, swimwear if there is water, chargers and any "
           "tickets. Plan to wash once on day three or four - a hostel or a launderette - and you "
           "can halve the clothes. Roll everything, put the first night's things on top, and "
           "leave the \"just in case\" outfit at home."),
          avoid=("cold", "snow", "ski", "skiing", "winter", "december", "january", "february",
                 "november", "march", "hand luggage", "carry on", "carry-on", "cabin bag",
                 "weekend", "two nights", "three nights", "baby", "toddler", "kids", "children",
                 "wedding", "funeral", "interview", "dress code", "party", "work", "office",
                 "spain", "italy", "greece", "portugal", "turkey", "croatia", "france",
                 "canaries", "mallorca", "sicily", "cyprus", "malta", "summer", "beach", "sun",
                 "hot", "warm", "moving", "move", "house", "plates", "crockery", "hospital",
                 "medicine", "medication", "insulin", "inhaler", "epipen", "tablets",
                 "scotland", "scottish", "edinburgh", "glasgow", "highlands", "iceland",
                 "reykjavik", "norway", "oslo", "sweden", "stockholm", "finland", "helsinki",
                 "ireland", "dublin", "denmark", "copenhagen", "greenland", "faroe", "wales",
                 "snowdonia")),

    entry("keep-drinks-cold",
          (("drinks", "a drink", "my drink", "the drink", "water", "water bottle", "bottle",
            "bottles", "a can", "the can", "cans", "juice", "fizzy", "cola", "lemonade", "beer", "wine",
            "keep it cold", "keep them cold", "keep it cool", "keep them cool",
            "keep it chilled", "keep it cold overnight",
            "white wine", "rose", "prosecco", "cool bag", "cool box", "cooler", "flask"),
           ("cold", "cool", "chill", "chilled", "icing", "ice", "ice pack", "ice block",
            "cooler", "picnic", "beach", "car", "car journey", "journey", "day out", "party",
            "barbecue", "bbq", "hot day", "heatwave", "summer", "warm", "travel",
            "water cold", "water stays cold", "water cool", "keep water cold",
            "keep my water cold", "cold water bottle", "on a walk", "long walk", "hike")),
          _cold_drinks,
          bias=3,
          ask=("how", "what", "best", "keep", "stay", "stop", "make", "get", "should", "can i",
               "tips", "advice", "way"),
          avoid=("cold rice", "cold pizza", "cold chicken", "cold pasta", "cold potatoes",
                 "cold noodles", "cold soup", "cold curry", "leftover", "leftovers",
                 "left over", "left in the fridge", "from last night", "yesterdays",
                 "gone off", "gone bad", "out of date", "expire", "expiry", "sell by", "use by",
                 "radiator", "radiators", "heating", "central heating", "boiler", "hot water",
                 "hot tap", "hot taps", "thermostat", "immersion", "towel rail",
                 "cool box", "coolbox", "cooler box", "cool bag", "cooler bag", "chiller bag",
                 "chiller box", "picnic bag", "picnic box", "ice box",
                 "get warm", "getting warm", "to get warm", "cant get warm", "can't get warm",
                 "never warm", "feel cold", "feeling cold", "im cold", "i am cold", "so cold",
                 "shivering", "freezing", "keep warm", "stay warm", "warm up", "warming up",
                 "hands are cold", "feet are cold", "cold hands", "cold feet",
                 "best water bottle", "best bottle", "buy", "buying", "recommend",
                 "recommendation",
                 "off milk", "sour", "smells", "fridge not cold", "not cold enough", "freezer",
                 "freeze the", "can i freeze", "milk", "formula", "breast milk", "baby",
                 "how long does", "how long can", "how long will",
                 "how much water", "how much should i drink", "how much to drink",
                 "how much liquid", "how many litres", "how many liters", "how much do i drink",
                 "ruin", "ruined", "claim", "claims", "refund", "money back", "compensat",
                 "who pays", "insurance", "insured", "wasted", "spoiled", "spoilt", "thawed",
                 "power cut", "power went off", "everything inside", "all the food",
                 "haggle", "haggling", "bargain", "bargaining", "negotiate", "negotiating",
                 "money off", "discount", "discounts", "new car", "new cars", "buy a car",
                 "buying a car", "car finance", "test drive", "dealer", "dealership",
                 "for sale", "price", "prices", "salesperson", "sales target",
                 "passport", "passports", "visa", "boarding pass",
                 "drive it", "drive my car", "drive the car", "can i drive", "drive home",
                 "wont start", "won't start", "not starting", "overheating", "overheated",
                 "breakdown", "broken down", "flat battery", "smoke", "steam",
                 "run", "running", "jog", "jogging", "exercise", "gym", "train", "training",
                 "work out", "workout", "swim", "swimming", "cycle", "cycling", "football",
                 "play", "playing", "sick", "ill", "illness", "fever", "temperature",
                 "fabric softener", "fabric conditioner", "softener", "conditioner",
                 "laundry", "washing machine", "washing", "wash", "clothes", "towels")),

    entry("camping-kit", (("camping", "campsite", "camp site", "wild camp", "wild camping",
                           "tent", "under canvas"),
                          ("pack", "packing", "need", "take", "taking", "bring", "gear", "kit",
                           "list", "first time", "what should i", "what do i")),
          ("Tent with its pegs and a mallet, a sleeping bag and a mat - a foam or inflatable one, "
           "not just the tent floor - a head torch, a stove with fuel and a lighter, and a water "
           "container. Take warm layers and a waterproof even in summer, boots you can walk in, "
           "bin bags, a small first-aid kit with blister plasters, and food in a cool box. Book "
           "the pitch ahead and check the site's rules on fires, dogs and arrival time."),
          bias=1, guard=_not_a_food_to_carry,
          avoid=("day hike", "hiking", "walk", "walking", "festival", "beach", "garden",
                 "back garden", "backyard", "kids", "children", "toddler", "baby")),

    entry("camping-with-kids",
          (("camping", "campsite", "camp site", "tent", "under canvas"),
           ("kids", "children", "childs", "child's", "child", "toddler", "toddlers", "baby",
            "babies", "family", "son", "daughter", "boys", "girls", "little ones",
            "kid", "boy", "girl", "grandchildren", "grandchild", "grandkids", "grandson",
            "granddaughter", "niece", "nephew", "teen", "teens", "teenager", "teenagers")),
          ("A tent and bags for everyone, plus what small children need on a campsite: a mat each, "
           "because they feel every root, warm layers and a hat for the night even in July, and a "
           "full change of clothes kept in the car so a wet sleeping bag is not the end of the "
           "trip. Take a torch each, wet wipes, a bin bag for wet things, breakfast that needs no "
           "cooking, and something to do after dark. Pitch in daylight, close to the toilets but "
           "not beside them, and let them run about before bed so they sleep."),
          ask=("pack", "packing", "need", "take", "taking", "bring", "gear", "kit", "list",
               "what should i", "what do i", "what to bring", "first time"),
          bias=2,
          avoid=("hole", "holes", "leak", "leaking", "pole", "poles", "broke", "broken",
                 "repair", "fix", "book", "booking", "price", "cost", "how much", "where",
                 "dog", "dogs", "pitch up", "won't go up", "wont go up")),

    entry("camping-with-children",
          (("camping", "campsite", "camp site", "wild camp", "wild camping", "tent",
            "under canvas"),
           ("pack", "packing", "need", "take", "taking", "bring", "kit", "gear", "list",
            "what should i", "what do i", "what do we")),
          ("Tent, sleeping bags and mats for everyone, a torch each so nobody is in the dark "
           "alone, and one full change of clothes per child per day plus two spare sets: that is "
           "what wet weather costs. Add wellies and a waterproof, wipes and nappy bags, a sun hat "
           "and cream, snacks and a water bottle each, their own pillow or blanket, Calpol and "
           "plasters, and a bag for wet things. Pitch near the toilets, take a mallet, and put "
           "the tent up at home once before you go."),
          ask=("kids", "kid", "children", "child", "toddler", "baby", "family", "families", "son",
               "daughter", "boys", "girls", "with the kids", "with kids", "little ones"),
          bias=2,
          avoid=("safe", "safety", "is it ok", "ok to", "too cold", "too young", "months old",
                 "weeks old", "cry", "crying", "feed", "feeding", "bottle", "garden",
                 "back garden", "backyard", "festival", "beach")),

    entry("festival-kit", (("festival", "festivals", "glastonbury", "reading festival",
                            "download festival", "camping festival"),
                           ("pack", "packing", "need", "bring", "gear", "kit", "list",
                            "what should i take", "what do i take", "what to take")),
          ("Ticket and ID, some cash because card readers fail in fields, a small tent with its "
           "pegs and a mallet, a sleeping bag and mat, earplugs and a power bank. Wellies, a "
           "waterproof and warm layers for the nights, plus sun cream and a hat for the days, wet "
           "wipes, toilet roll, blister plasters and bin bags; leave glass at home. Pack so you "
           "can carry it from the car park, and put your name on the tent bag."),
          bias=1,
          avoid=("day trip", "day out", "kids", "children", "toddler", "baby", "garden")),

    entry("car-journey-kids", (("car", "drive", "journey", "plane", "flight", "train", "ferry",
                                "road trip", "long drive", "long journey", "long flight"),
                               ("kids", "children", "toddler", "baby", "child", "them",
                                "busy", "occupied", "entertained")),
          ("Leave at nap time or early if you can, plan a stop or a walk about every two hours, "
           "and pack snacks, water, sunshades and a tablet with films downloaded. A surprise bag "
           "of small new things to hand out one at a time is the trick for the last hour."),
          avoid=("driving me mad", "drive me mad", "drives me mad", "drive you mad",
                 "driving me crazy", "drive me crazy", "driving me up the wall",
                 "drive me up the wall", "drives me up the wall", "driving me insane",
                 "driving us mad", "drives us mad")),
    entry("car-sick", (("car", "motion"), ("sick", "sickness", "nausea", "dizzy", "vomit")),
          "Sit in the front seat, look at the horizon rather than a screen, and keep the air cool with the window down a little. Eat something plain beforehand, and stop for ten minutes if you feel bad.",
    ),
    entry("where-to-stay-there", (("where should we stay", "where should i stay", "where do i stay",
                                   "where to stay", "best place to stay", "where shall we stay"),
                                  ("stay", "sleep", "sleeping", "hotel", "area", "neighbourhood",
                                   "neighborhood", "part of town")),
          _where_to_stay, bias=1),
    entry("where-to-stay", (WHERE_TO_STAY,
                            tuple(CITY_AREA) + ("there", "that city", "the city", "this city")),
          _where_to_stay,
          bias=2),
    entry("where-to-stay-anywhere", (WHERE_TO_STAY,
                                     ("stay", "staying", "hotel", "hotels", "hostel", "b&b",
                                      "guest house", "caravan", "area", "town", "village",
                                      "seaside", "coast", "beach", "district", "in", "near",
                                      "somewhere", "accommodation",
                                      "sleep", "sleeping", "kip", "crash")),
          _a_town_stay,
          bias=3, guard=_a_town_stay_line,
          avoid=("hospital", "ward", "sister", "brother", "mum", "dad", "mother", "father",
                 "friend", "friends", "relative", "in laws", "funeral", "wedding", "work",
                 "office", "airport", "stopover", "layby", "service station", "prison",
                 "uni", "university", "student", "hostel dorm")),
    entry("a-night-near-the-airport",
          (("airport", "airport hotel", "terminal", "departure", "departures", "check in desk",
            "heathrow", "gatwick", "stansted", "luton airport", "liverpool airport", "prestwick",
            "flight", "flights", "flying",
            "early flight", "early start", "dawn flight", "red eye"),
           ("stay", "staying", "night", "sleep", "hotel", "hotels", "accommodation", "book",
            "booking", "near", "before", "overnight", "stop over", "stopover")),
          "For a night before an early flight, book an airport hotel with a shuttle and check the "
          "first and last shuttle times before you pay - a 4am shuttle that stops at 11pm is the "
          "usual trap, and so is a \"5 minutes from the terminal\" that is five minutes by car "
          "on a road with no pavement. A town two or three stops away on the train, or a "
          "park-and-fly with the transfer included, is usually about half the price; add up the "
          "transfer, the parking and the extra hour and pick on the total. Take the flexible rate "
          "if the flight is early, and get the shuttle time in writing.",
          bias=2, guard=_a_night_near_the_airport,
          avoid=("queue", "queues", "security", "liquids", "laptop", "duty free", "lost",
                 "delayed", "delay", "cancelled", "cancel", "compensation", "baggage",
                 "hand luggage", "food", "eat", "coffee", "shops", "parking cost",
                 "how long", "what time", "get to", "get from", "transfer to")),

    entry("trip-essentials",
          (_ESSENTIALS_ASK,
           ("trip", "holiday", "travel", "travelling", "going away", "time away", "abroad",
            "week away", "fly", "flying", "flight", "holidays",
            "before i go", "before we go", "before i fly", "before we fly")),
          _trip_essentials,
          bias=1,
          avoid=("yellow card", "yellow fever", "certificate", "card",
                 "insurance", "cover", "ghic", "ehic",
                 "visa", "visas", "evisa", "esta", "etias", "entry requirements", "jab", "jabs",
                 "vaccine", "vaccines", "vaccination", "malaria", "yellow fever", "passport expired",
                 "passport expires", "renew", "renewing", "driving", "drive", "licence", "car hire",
                 "currency", "cash", "money", "cost", "costs", "cheap", "how much", "price",
                 "adapter", "adaptor", "plug", "plugs", "sockets", "charging", "pack", "packing",
                 "suitcase", "clothes", "wear", "bring", "take", "weather", "when to go",
                 "best time", "flight", "flights", "flying", "hotel", "hotels", "where to stay",
                 "house", "moving", "move", "moving house")),
    entry("plug-country", (tuple(PLUG_TYPES),
                           ("adapter", "adaptor", "plug", "plugs", "socket", "sockets", "voltage",
                            "charger", "chargers")),
          _adapter, bias=1,
          avoid=("cash", "money", "currency", "spend", "budget", "much", "cost", "safe", "water",
                 "visa", "flight", "flights", "hotel", "train",
                 "difference between", "part of the uk", "british isles", "same as britain")),
    entry("travel-adapter", (("adapter", "plug", "sockets", "charger"),
                             ("europe", "abroad", "travel", "voltage", "uk", "italy", "france",
                              "spain", "greece", "portugal", "usa", "america")),
          ("Europe and many other countries use two round pins, the UK uses three square ones, and "
           "the US uses flat pins, so take a universal adapter. Check the voltage on your chargers: "
           "phone and laptop chargers handle 100-240V fine; hairdryers often don't.")),
    entry("travel-insurance", (("insurance", "travel insurance", "ehic", "ghic", "health card"),
                               ("travel", "abroad", "holiday", "trip", "worth", "get", "need",
                                "card", "ghic", "ehic", "ghic card", "ehic card", "health card",
                                "what does the ghic", "what is the ghic", "what does the ehic",
                                "what is the ehic")),
          ("Take the free GHIC card for state healthcare in the EU and pair it with proper travel "
           "insurance: the card covers treatment, not getting you home. Buy insurance when you "
           "book so cancellation is included."),
          avoid=("car", "cars", "vehicle", "van", "motorbike", "driving", "drive", "pet", "pets",
                 "dog", "cat", "phone", "home", "house", "contents", "buildings", "boiler",
                 "life insurance", "breakdown", "dental", "business", "excess", "claim",
                 "claims", "renewal", "quote", "cheaper", "reduce the price",
                 "national insurance", "ni number", "insurance number",
                 "claimed", "claiming", "wont pay", "won't pay", "not paying",
                 "refused", "refuses", "rejected", "payout", "pay out",
                 "insurer", "wont cover", "won't cover")),
    entry("japan-rail-pass", (("rail pass", "jr pass"), ("japan", "worth", "need", "buy")),
          ("It's only worth it for long-distance trips: two or more shinkansen journeys make a "
           "7-day pass pay, but for Tokyo and Kyoto alone it usually doesn't. Buy it before you "
           "travel, and reserve seats for the busy holiday weeks.")),
    entry("japan-blossom", (("cherry blossom", "blossom", "sakura"), ("japan", "tokyo", "kyoto",
                                                                     "when", "season", "march")),
          ("Late March to early April, moving north as the season goes: Tokyo usually peaks around "
           "the end of March, Kyoto a few days later. Book accommodation months ahead, and be "
           "flexible, because a cold spring can delay it by a week or two."),
          avoid=("tree", "trees", "hedge", "hedgerow", "shrub", "bush", "plant", "flower",
                 "flowers", "white")),
    entry("edinburgh-winter", (("edinburgh",), ("december", "winter", "pack", "cold", "christmas")),
          ("Pack for 2 to 8C, wind and sideways rain: a waterproof coat, warm layers, and shoes "
           "you can walk up a hill in. It's dark by 4pm, so plan indoor things for the afternoon "
           "and take a torch for Arthur's Seat.")),

    entry("pack-it-tight",
          (("pack", "packing", "packed", "fit", "squeeze", "cram"),
           ("tightly", "tight", "more in", "everything in", "fit everything", "fit it all",
            "no room", "rucksack", "backpack", "suitcase", "case", "hand luggage", "carry on",
            "holdall", "bag")),
          "Roll everything and stand the rolls on end like books on a shelf: a case is a box, and "
          "packing flat leaves a third of it empty. Shoes go heel to toe along the spine with "
          "socks and chargers inside them, the heavy end goes at the wheels, and whatever you "
          "might want out goes on top. In a rucksack the weight sits high and close to your back "
          "rather than at the bottom, with the waterproof and a change of clothes at the top. Wear "
          "the bulky shoes and the coat on the day.",
          ask=("how do i pack", "how to pack", "how do i fit", "how can i fit", "pack it",
               "pack more", "pack everything", "fit everything", "fit it all", "tightly", "tight",
               "squeeze", "cram", "in one bag", "rucksack", "backpack", "no room"),
          avoid=("for a week", "for two weeks", "for the weekend", "what should i", "how many",
                 "light", "list", "checklist",
                 "hospital", "maternity", "labour", "labor bag", "birth", "funeral", "flight bag",
                 "school bag", "nappy bag", "diaper bag", "changing bag", "hospital bag"),
          bias=1),

    entry("packing-light", ("packing", "light", "carry", ("list")),
          ("Lay everything out and take half the clothes and twice the money: three tops, two "
           "bottoms, one warm layer and shoes you can walk in covers a week. Roll clothes, keep a "
           "change in your hand luggage, and buy anything you forget when you arrive.")),
    entry("rail-ticket-help", (("train ticket", "train tickets", "rail ticket", "rail tickets",
                                "my ticket", "my train ticket", "advance ticket",
                                "off peak ticket", "return ticket", "single ticket",
                                "ticket", "tickets"),
                               ("lost", "lose", "losing", "left", "left it", "forgot",
                                "forgotten", "change", "changed", "changing", "amend", "amended",
                                "alter", "valid", "any train", "another train", "wrong train",
                                "missed", "earlier", "later", "different train", "print",
                                "printed", "phone", "mobile", "app", "e ticket", "eticket")),
          _a_ticket_already_bought,
          avoid=("refund", "refunds", "delay", "delayed", "cancel", "cancelled", "compensation",
                 "delay repay", "claim", "expenses", "receipt", "policy", "mileage", "price",
                 "prices", "cost", "cheap", "cheaper", "cheapest", "how much", "when do",
                 "go on sale", "book", "booking", "booked", "advance fare", "railcard",
                 "season ticket", "watch", "film", "cinema", "concert", "match", "parking",
                 "parking ticket", "speeding", "fine"),
          bias=1),

    entry("book-a-journey", (JOURNEY_MODES + ("seat", "seats", "reservation"),
                             ("book", "booked", "booking", "reserve", "reservation",
                              "reservations", "seat", "seats", "ahead", "advance",
                              "in advance", "need to", "have to", "must i", "do i need",
                              "early", "now or", "turn up", "on the day",
                              "on sale", "go on sale", "goes on sale", "when do", "when should",
                              "when can i", "how far",
                              "book a coach", "book coach", "book the coach", "book a train",
                              "book a ferry", "book the ferry", "book a ticket", "book tickets")),
          _book_a_journey,
          avoid=("price", "prices", "cost", "how much", "much",
                 "delay", "delayed", "cancel", "cancelled", "missed", "refund", "pack",
                 "packing", "what should i take", "luggage", "suitcase", "already booked",
                 "ive booked", "i have booked", "we booked", "just booked",
                 "book to read", "books to read", "what book", "which book", "reading",
                 "novel", "novels", "audiobook", "kindle",
                 "table", "tables", "restaurant", "meal", "hotel", "room", "rooms", "taxi",
                 "haircut", "viewing", "appointment", "doctor", "dentist", "garage", "mot",
                 "parking",
                 "receipt", "receipts", "claim", "claims", "claiming", "expense", "expenses",
                 "reimburse", "reimbursement", "tax back", "mileage"),
          bias=1),
    entry("book-a-flight",
          (("flight", "flights", "fly", "flying", "airfare", "airfares", "plane ticket"),
           ("book", "booked", "booking", "how do i book", "reserve", "buy", "purchase",
            "which site", "what site", "compare", "direct")),
          "Compare on a search site, then book on the airline's own site, because a booking agent's "
          "cheap fare usually costs more once its card fee and its no-changes rule are counted. "
          "Before you pay, add the baggage for each person and pick the seats: the headline fare "
          "often leaves both out, and that is where a cheap ticket stops being cheap. Pay by "
          "credit card if the fare is over £100, which gives you section 75 cover if the airline "
          "fails, and check every passenger's passport has six months left on it.",
          bias=1, guard=_the_booking_is_behind_them,
          avoid=("cheap", "cheaper", "cheapest", "deal", "deals", "when to", "how early",
                 "how far ahead", "advance", "bag", "bags", "baggage", "luggage", "delay",
                 "delayed", "cancel", "cancelled", "boarding", "gate", "check in", "checkin",
                 "my flight", "our flight", "boarding pass", "missed", "change", "refund",
                 "seat", "seats", "legroom", "extra legroom", "jet lag", "jetlag",
                 "nervous", "scared", "afraid", "sick", "ill", "food", "liquids", "water",
                 "airport", "parking", "transfer", "passport", "visa", "insurance",
                 "just", "already",
                 "when", "wait", "waiting", "now or", "best time", "cheapest time", "cheapest",
                 "how soon", "how long before", "ahead",
                 "i want to", "i'd like to", "i would like to",
                 "what books", "which books", "good books for", "books for a flight",
                 "book to read", "books to read",
                 "read", "reading", "to read", "novel", "novels", "audiobook",
                 )),
    entry("cheap-flights",
          (("flight", "flights", "fly", "flying", "airfare", "airfares", "plane ticket"),
           ("cheap", "cheaper", "cheapest", "book", "booking", "price", "prices", "deal",
            "deals", "much", "cost", "early", "advance", "ahead", "when")),
          ("Book six to eight weeks ahead for short-haul and two to four months for long-haul, and be "
           "flexible about the day: Tuesday and Wednesday are usually cheapest. Search one way at a "
           "time, and check the airport transfer before you commit to a bargain."),
          ask=("cheap", "cheaper", "cheapest", "cheaply", "when", "how early", "how far ahead",
               "price", "prices", "deal", "deals", "compare", "save", "cost", "much",
               "best time", "how far in advance", "advance"),
          avoid=("sick", "ill", "illness", "cold", "colds", "flu", "covid", "germs", "catch",
                 "catching", "scared", "afraid", "nervous", "anxious", "panic", "turbulence",
                 "delay", "delayed", "cancel", "cancelled", "lost luggage", "legroom",
                 "jet lag", "jetlag", "travel sick", "travel sickness",
                 "when is my flight", "when is our flight", "what time is my flight",
                 "what time is our flight", "what time do i fly", "when do i fly",
                 "what time am i flying", "when am i flying", "what time is the flight",
                 "when is the flight",
                 "boarding", "boards", "board the", "gate", "gates", "departure",
                 "pregnant", "pregnancy", "weeks pregnant", "trimester", "midwife", "due date",
                 "split", "splitting", "share", "sharing", "halves", "who pays", "who owes",
                 "each pay", "chip in", "between us", "cost of the flights",
                 "cost of flights", "pay for the flights")),
    entry("longest-river", ("longest", "river", "world"),
          region_extreme("river",
                         "The Nile, at about 6,650 km, is usually called the longest, with the "
                         "Amazon a close second and carrying far more water. Which one wins depends "
                         "on where you say the Amazon starts."),
          avoid=("china", "india",
                 "france", "italy", "spain", "germany", "egypt",
                 "how many rivers", "number of rivers", "count rivers",
                 "bridge", "bridges", "tunnel", "tunnels", "wall", "walls", "road", "roads",
                 "motorway", "motorways", "causeway", "pier", "piers", "coastline",
                 "border", "borders", "railway", "railways", "flight", "flights")),
    entry("biggest-country", ("country", "biggest", "area", ("largest", "world", "by size",
                                                             "by area", "size")),
          country_extreme("area", "Russia, at about 17 million square km, nearly twice the size of "
                                  "Canada in second place. China and the United States come next."),
          avoid=("uk", "britain", "england", "scotland", "wales", "ireland", "china", "india",
                 "france", "italy", "spain", "germany", "egypt",
                 "island", "islands", "lake", "lakes", "desert", "mountain", "river",
                 "ocean", "sea", "city", "continent", "continents",
                 "animal", "animals", "creature", "creatures", "whale", "elephant",
                 "bird", "fish", "shark", "dinosaur", "insect",
                 "how many countries", "number of countries",
                 "countries have", "countries with", "countries without",
                 "smallest", "smallest by", "least", "fewest",
                 "population", "populous", "people live", "most people")),
    entry("altitude-sickness", ("sickness", "altitude", "avoid", ("mountain")),
          ("Go up slowly: above 3,000m, sleep no more than 500m higher than the night before, and "
           "take a rest day every third day. Drink plenty, skip alcohol, and if you get a bad "
           "headache with nausea, go down rather than waiting it out.")),
    entry("driving-abroad", ("driving", "abroad", "permit", ("europe", "international")),
          ("You need your licence, insurance and usually a warning triangle, hi-vis vest and "
           "breathalyser kit; check whether your insurer covers abroad or you need a green card. An "
           "international driving permit costs a few pounds and is worth having in some countries, so "
           "check yours before you go.")),
    
    entry("driving-in-traffic",
          (("traffic", "traffic jam", "traffic jams", "gridlock", "motorway", "motorways",
            "red x", "red cross", "someone", "somebody", "a car", "car", "behind me",
            "behind", "bumper",
            "tailgating",
            "tailgated", "tailgate", "tailgates", "tailgaters", "overtaking",
            "aquaplaning", "hydroplaning", "standing water", "skidding", "skidded",
            "fog", "foggy", "driving in fog", "driving in the fog", "drive in fog",
            "heavy rain", "rain", "smart motorway",
            "lane", "lanes", "stop start", "stop-start", "morning traffic", "rush hour"),
           ("how do i", "how can i", "how to", "how should i", "what should i do",
            "what do i do", "what should i", "should i", "tips", "tip", "advice", "advise",
            "best way", "safest", "safe", "deal with", "cope with", "handle", "drive",
            "driving", "drove", "learn", "help", "any", "mean", "means",
            "tailgating", "tailgated", "tailgate", "tailgates", "tailgater", "tailgaters",
            "behind", "bumper")),
          _drive_in_traffic,
          ask=("drive", "driving", "drove", "traffic", "motorway", "aquaplaning", "skidding",
               "overtaking", "tailgate", "tailgates", "tailgated", "tailgating",
               "tailgaters", "merging", "slip road", "stay safe"),
          avoid=("pack", "packing", "what should i take", "what do i take", "plan", "planning",
                 "route", "stops", "overnight", "how long", "how far", "cost", "price", "fuel",
                 "insurance", "breakdown", "towing", "caravan", "trailer", "licence", "license",
                 "provisional", "test", "lessons", "abroad", "europe", "france",
                 "automatic", "manual", "gearbox", "clutch", "hill start", "parking", "reverse",
                 "three point turn", "3 point turn",
                 "overheat", "overheats", "overheating", "overheated", "coolant",
                 "radiator", "temperature light", "temperature gauge", "steam", "steaming",
                 "smoking", "smoke", "warning light", "engine light",
                 "ice", "icy", "black ice", "snow", "snowy", "snowing", "frost", "frosty",
                 "gritted", "gritting", "hail", "hailstones",
                 "swim", "swimming", "swam", "pool", "beach", "sea", "lido", "run",
                 "running", "jog", "jogging", "cycle", "cycling", "dog", "dogs", "cat",
                 "cats", "pet", "pets", "baby", "babies",
                 "train", "trains", "bus", "coach", "plane", "flight", "holiday",
                 "is there", "is it busy", "delays", "delayed", "cancelled", "closed",
                 "kids", "children", "child", "baby", "toddler",
                 "check traffic", "check the traffic", "check the roads", "before i leave",
                 "before we leave", "live", "how busy", "will it be busy",
                 "heating", "radiator", "radiators", "put the heating on", "washing",
                 "washing out", "wash", "umbrella", "umbrellas", "coat", "coats",
                 "barbecue", "bbq", "garden", "lawn", "hanging out", "dry the washing")),
    
    entry("fly-with-medicine", (("insulin", "inhaler", "inhalers", "epipen", "epi-pen", "epipens",
                                 "medication", "medications", "medicine", "medicines",
                                 "prescription", "prescriptions", "syringe", "syringes", "pills",
                                 "statins", "tablets", "paracetamol", "ibuprofen", "aspirin",
                                 "antihistamine", "antihistamines", "antibiotics", "epilepsy",
                                 "injection", "injections", "letter", "letters", "airline",
                                 "airlines", "flying with"),
                                ("letter", "letters", "note", "fit to fly"),
                                ("fly", "flying", "flight", "flights", "plane", "planes",
                                 "airport", "abroad", "travel", "travelling", "traveling",
                                 "holiday", "carry", "pack", "packing", "hand luggage",
                                 "carry on", "carry-on", "security", "suitcase", "bag", "bags")),
          ("Carry it in your hand luggage, never the hold, in its original box with the pharmacy "
           "label on it. Liquids over 100ml, insulin and anything injected need a doctor's letter "
           "or a copy of the prescription to get through security, and insulin travels in a cool "
           "bag but never touching ice. Pack a few days extra in case you are delayed, and check "
           "the country's rules for controlled medicines a couple of weeks ahead."), bias=1,
          avoid=("dog", "dogs", "cat", "cats", "puppy", "puppies", "kitten", "kittens",
                 "pet", "pets", "rabbit", "ferret", "hamster", "budgie", "parrot",
                 "cancelled", "canceled", "cancel", "refund", "refunds", "money back",
                 "compensation", "compensated", "rights", "delayed", "delay", "claim",
                 "rebook", "rebooking", "stranded", "missed my flight",
                 "damaged", "damage", "smashed", "ripped", "torn", "dented", "destroyed",
                 "broke", "broken",
                 "lost my bag", "lost my bags", "lost my luggage", "lost my suitcase",
                 "lost my case", "bag never arrived", "bags never arrived",
                 "luggage never arrived", "suitcase never arrived", "bag didnt arrive",
                 "bag didn't arrive", "luggage didnt arrive", "luggage didn't arrive",
                 "bag went missing", "luggage went missing", "suitcase went missing")),
    entry("pack-hand-luggage", (("pack", "packing", "suitcase", "bag"),
                                ("hand luggage", "carry on", "carry-on", "one bag", "small bag",
                                 "cabin bag", "capsule")),
          ("For a week in a carry-on: two tops, one warm layer, one pair of trousers you can wear "
           "twice, and shoes you have already walked a mile in - then take a third of it out. Roll "
           "clothes instead of folding, take travel sizes, and plan to wash once. It also saves the "
           "wait at the belt."),
          ask=("pack", "packing", "packed", "what to take", "what should i take", "what do i take",
               "what to bring", "what should i bring", "what do i bring", "fit in", "fit into",
               "light", "lightly", "minimal"),
          avoid=("insulin", "inhaler", "inhalers", "epipen", "epi-pen", "medication", "medicine",
                 "medicines", "prescription", "syringe", "pills", "statins", "tablets")),
    entry("pack-cool-country", (("pack", "packing", "what should i take", "what to take",
                                 "what clothes", "which clothes", "wear", "bring"),
                                ("scotland", "scottish", "edinburgh", "glasgow", "highlands",
                                 "iceland", "reykjavik", "norway", "oslo", "sweden", "stockholm",
                                 "finland", "helsinki", "ireland", "dublin", "denmark",
                                 "copenhagen", "greenland", "faroe", "wales", "snowdonia")),
          ("Take a warm mid layer and a waterproof shell, plus long sleeves rather than vests - "
           "even in June the evenings drop to about 8C. Add a hat and gloves if you are going "
           "high or out on the water, and midge repellent for anywhere damp and windless in high "
           "summer."),
          avoid=("how long", "how far", "drive", "driving", "flight", "flights", "fly", "train",
                 "coach", "ferry", "cost", "cheap", "hotel", "hotels", "stay in", "days in",
                 "weekend in", "weather like", "when to go", "best time")),
    entry("pack-warm-week", (("pack", "packing", "suitcase", "wear in", "wear to", "bring to",
                              "what should i take", "what should i wear",
                              "what clothes should i take", "what clothes do i take",
                              "what clothes to take", "what clothes should i bring",
                              "what clothes do i bring", "what clothes should i pack",
                              "what clothes should i wear"),
                             ("spain", "italy", "greece", "portugal", "turkey", "croatia",
                              "france", "canaries", "mallorca", "sicily", "cyprus", "malta",
                              "october", "september", "may", "june", "july", "august", "summer",
                              "warm", "hot", "beach", "sun", "sunshine")),
          _warm_week_pack, guard=_not_a_food_to_carry,
          bias=1,
          avoid=("cold", "snow", "ski", "skiing", "winter", "december", "january", "february",
                 "march", "november", "rain", "wet", "hand luggage", "carry on", "carry-on",
                 "pack light", "first time", "baby", "toddler", "kids", "children", "wedding",
                 "funeral", "interview", "dress code", "party", "work", "office",
                 "scotland", "scottish", "edinburgh", "glasgow", "highlands", "iceland",
                 "reykjavik", "norway", "sweden", "finland", "denmark", "copenhagen", "oslo",
                 "stockholm", "helsinki", "ireland", "dublin", "england", "wales", "britain",
                 "uk", "london", "cornwall", "devon", "yorkshire", "lake district", "alps",
                 "greenland", "canada", "new zealand", "estonia", "latvia", "lithuania",
                 "poland", "russia", "germany", "netherlands", "belgium", "austria",
                 "switzerland", "czech", "prague")),
    entry("london-airport", (("heathrow", "gatwick", "stansted", "luton", "london city", "london"),
                             ("closest", "nearest", "central london", "into london", "to london",
                              "get to london", "transfer", "which airport", "how do i get",
                              "how do i",
                              "get to", "getting to", "get from", "cheapest", "cheap", "cheaper",
                              "best way", "way to get", "early flight", "early in the morning",
                              "taxi")),
          _london_airport),
    entry("london-car-or-train",
          (("london", "the city", "central london", "into london"),
           ("drive", "driving", "car", "by car", "train", "by train", "parking",
            "which is", "better", "or train", "or drive", "cheaper", "worth", "should i")),
          "Take the train into the centre: parking runs twenty to thirty pounds for a day, the "
          "congestion charge is on top of that, and then you are still looking for a space. Drive "
          "only if you are heading somewhere outside the centre or carrying things - and then "
          "park at a Tube or rail station on the edge and finish by train. Book the train two or "
          "three weeks ahead and it is usually cheaper than the fuel plus parking.",
          avoid=("airport", "heathrow", "gatwick", "stansted", "luton", "flight", "flights",
                 "how long", "how far", "how many hours", "journey", "duration", "timetable",
                 "fly", "coach", "coaches", "megabus", "national express", "hotel",
                 "what is there to do", "visit",
                 "bus", "buses", "tube", "oyster", "travelcard", "travel card")),

    entry("tipping-abroad", (("tip", "tipping", "gratuity"),
                             ("america", "american", "usa", "the us", "in us", "states",
                              "japan", "japanese", "tokyo", "kyoto", "europe", "france",
                              "paris", "spain", "italy", "rome", "portugal", "greece",
                              "germany", "netherlands", "amsterdam", "mexico", "thailand",
                              "turkey", "dubai", "india", "canada", "australia", "ireland",
                              "abroad", "overseas",
                              "new york", "nyc", "las vegas", "vegas", "los angeles",
                              "san francisco", "miami", "chicago", "boston", "seattle",
                              "washington", "texas", "hawaii", "orlando", "florida",
                              "california", "toronto", "vancouver", "sydney", "melbourne",
                              "brisbane", "perth", "auckland", "bali", "phuket", "singapore",
                              "hong kong", "seoul", "lisbon", "barcelona", "madrid", "berlin",
                              "munich", "florence", "venice", "athens", "crete", "malta",
                              "cyprus", "croatia", "dubrovnik", "prague", "vienna", "zurich",
                              "geneva", "brussels", "copenhagen", "stockholm", "oslo",
                              "helsinki", "warsaw", "budapest", "istanbul", "egypt", "morocco",
                              "brazil", "argentina", "peru", "cuba", "jamaica", "barbados",
                              "maldives", "sri lanka", "vietnam", "cambodia", "malaysia",
                              "indonesia", "philippines", "qatar", "israel", "jordan", "kenya",
                              "iceland", "norway", "sweden", "denmark", "finland", "poland",
                              "czech", "austria", "switzerland", "belgium",
                              "hotel", "housekeeping", "porter", "concierge", "bellboy",
                              "room service", "tour guide", "tour", "excursion", "walking tour",
                              "coach driver", "mover", "movers", "removal men")),
          _tipping,
          avoid=("any tips", "tips for", "tips on", "tips to", "a few tips", "some tips",
                 "hairdresser", "barber", "haircut", "barista")),
    entry("money-abroad", (("money", "cash", "currency", "card", "cards", "atm", "spending money",
                            "spending cash"),
                           ("abroad", "travelling", "travel", "holiday", "exchange", "change",
                            "safe", "safely", "safety", "stolen", "theft", "pickpocket",
                            "pickpockets", "money belt", "fee", "fees",
                            "commission", "local currency",
                            "take", "bring", "carry", "carrying", "with me", "spain",
                            "italy", "rome", "france", "paris", "greece", "portugal", "turkey",
                            "croatia", "germany", "netherlands", "japan", "thailand", "mexico",
                            "america", "usa", "europe")),
          _money_abroad,
          avoid=("send", "sends", "sending", "sent", "transfer", "transfers", "transferring",
                 "wire", "wiring", "job", "jobs", "job offer", "promotion", "promoted",
                 "career", "salary", "employer", "boss", "pay cut", "offer letter",
                 "interview",
                 "online", "website", "websites", "internet", "phishing", "shopping online",
                 "travel card", "travelcard", "oyster", "bus pass", "railcard", "season ticket",
                 "bring home", "brings home", "bringing home", "brought home",
                 "take home", "takes home", "taking home", "took home",
                 "earn", "earns", "earning", "earned", "wage", "wages", "payslip", "payslips",
                 "after tax", "before tax", "monthly pay", "payday",
                 "sd card", "sd cards", "memory card", "memory cards", "micro sd", "microsd",
                 "sim card", "sim cards", "storage card", "flash card", "usb stick",
                 "hard drive", "ssd")),
    entry("send-money-abroad", (("send", "sends", "sending", "sent", "transfer", "transfers",
                                 "transferring", "wire", "wiring", "remit"),
                                ("money", "cash", "euros", "dollars", "pounds", "funds",
                                 "abroad", "overseas", "spain", "france", "italy",
                                 "poland", "romania", "portugal", "turkey", "nigeria", "india",
                                 "australia", "canada", "usa", "america", "brazil", "pakistan",
                                 "bangladesh", "philippines", "ireland", "germany",
                                 "netherlands", "japan", "china", "kenya", "ghana",
                                 "south africa", "new zealand", "dubai", "uae", "jamaica",
                                 "morocco", "egypt", "sri lanka", "nepal", "vietnam",
                                 "thailand", "mexico", "zimbabwe", "uganda")),
          ("Use a transfer app such as Wise or Revolut for a normal amount: you get the real "
           "exchange rate and pay a small fee, and it lands in their bank account in a day or two. "
           "Compare the fee and the rate together, because a \"no fee\" transfer usually carries a "
           "worse rate, and use your own bank for large sums where you want the paper trail."),
          avoid=("parcel", "parcels", "package", "packages", "letter", "post office", "flowers",
                 "email", "text", "message", "gift")),
    entry("taxi-abroad", (("taxi", "cab", "uber", "ride hailing", "driver"),
                          ("abroad", "airport", "ripped", "overcharge", "price", "fare", "meter",
                           "scam", "safe", "expensive", "cost", "costs")),
          _taxi_abroad, bias=1,
          avoid=("or the train", "or a train", "or the bus", "or a bus", "or drive", "or park",
                 "or cycle", "or walk", "should i get a taxi", "is it cheaper")),
    entry("visa-check", (("visa", "entry requirements", "evisa"),
                         ("need", "required", "apply", "how do i", "do i", "get", "check")),
          ("It depends on your passport and where you are going, and the rules change often, so "
           "check the destination's official government site - with a UK passport, the gov.uk "
           "travel advice page links to it. Most tourist visas are applied for online a few days "
           "ahead; some countries charge a small fee on arrival instead.")),
    entry("baby-on-plane", (("baby", "babies", "infant", "toddler", "newborn"),
                            ("plane", "flight", "flying", "long haul", "take off", "travel",
                             "travelling", "traveling", "holiday", "abroad", "trip")),
          ("Ask for a bassinet seat at booking if they are under two: it is free on most airlines "
           "and gives you a bed and floor space. Feed or offer a dummy at take-off and landing "
           "for the ears, pack twice the nappies you think you need, and take a change of "
           "clothes for yourself as well as for them.")),
    entry("delay-repay",
          (("delay", "delayed", "late"),
           ("repay", "delay repay", "delayrepay", "compensation for the delay",
            "money back for the delay")),
          "Delay Repay is the train operators' scheme: on most of them you can claim from 15 "
          "minutes late, and some pay from 30. Claim on the operator's own site within 28 days, "
          "with the ticket or booking reference and the time you actually arrived, and it comes "
          "back as cash, a voucher or a free ticket depending on the operator.",
          avoid=("flight", "flights", "airline", "plane", "hotel", "holiday", "faulty",
                 "broken", "shop", "item", "online order", "train", "trains", "rail",
                 "railway", "refund", "cancelled", "cancel")),
    entry("flight-delay-claim", (("delay", "delayed", "cancelled", "cancellation", "compensation",
                                 "complain", "complaining", "complaint", "complain about"),
                                 ("flight", "plane", "airline", "claim", "owed", "entitled")),
          ("Under UK and EU rules you are owed 220 to 520 pounds per person when a flight arrives "
           "three hours or more late, unless the cause was extraordinary (weather, air traffic "
           "control, a security alert). Claim from the airline yourself with the booking reference "
           "and boarding pass; you usually have up to six years."),
          avoid=("train", "trains", "rail", "railway", "railcard", "tube", "underground",
                 "bus", "coach", "ferry", "tram", "cruise", "package holiday", "hotel",
                 "luggage", "baggage", "parcel", "delivery",
                 "royal mail", "post office", "postal", "parcelforce", "courier", "evri",
                 "dpd", "yodel", "letter", "letters", "package",
                 "delay repay", "repay", "minutes late", "hours late")),
    entry("denied-boarding",
          (("overbooked", "overbooking", "denied boarding", "denied",
            "bumped off", "bumped from", "bumped me", "bumped to a later flight", "bump me",
            "no seat", "seats were full", "seats full", "over sold", "oversold",
            "volunteered", "volunteer"),
           ("flight", "flights", "plane", "airline", "airlines", "airport", "boarding",
            "rights", "compensation", "claim", "owed", "entitled", "what can i", "gate")),
          "You are owed a choice on the spot: a full refund of the ticket, or a new flight as "
          "soon as one is available, plus 220 to 520 pounds per person in cash, not a voucher. "
          "While you wait the airline pays for meals and two calls, and a hotel if the new "
          "flight is the next day. Ask for the reason in writing and keep the boarding pass; if "
          "they refuse, complain to the CAA - you have up to six years.",
          ask=("overbooked", "overbooking", "denied boarding", "denied",
               "bumped off", "bumped from", "bumped me", "bumped to a later flight", "bump me",
               "no seat", "seats were full", "seats full", "over sold", "oversold",
               "volunteer", "volunteered"),
          avoid=("train", "trains", "rail", "railway", "tube", "underground", "bus", "coach",
                 "ferry", "tram", "cruise", "hotel", "hotels", "luggage", "baggage",
                 "parcel", "delivery", "restaurant", "concert", "ticket for")),
    entry("hotel-refund",
          (("refund", "refunds", "money back", "cancel", "cancelling", "cancelled", "called off"),
           ("hotel", "hotels", "booking.com", "room", "rooms", "accommodation", "guest house",
            "airbnb", "b and b")),
          "Check the rate you booked: a flexible rate is free to cancel up to a stated day, "
          "usually 24 to 48 hours before, and a saver rate is usually non-refundable - that is why "
          "it was cheaper. Cancel in the app rather than by phone so you have the confirmation, and "
          "if the hotel cancels on you, ask for a room of the same standard or a full refund plus "
          "the cost of a replacement if nothing is left.",
          avoid=("flight", "flights", "airline", "train", "trains", "faulty", "broken", "shop",
                 "item", "online order")),
    entry("train-refund",
          (("refund", "refunds", "money back", "delay repay", "compensation", "compensated",
            "cancelled", "canceled", "delayed", "missed", "late", "running late",
            "minutes late", "hours late"),
           ("train", "trains", "rail", "railway", "railcard", "journey", "operator",
            "commute")),
          "Two different claims. Before you travel, a refund is usually allowed less than an admin "
          "fee (up to £10) on an unused ticket, and advance tickets are often non-refundable but "
          "changeable. For a late train, Delay Repay pays out from 15 minutes late on most "
          "operators - claim on the operator's site within 28 days with your ticket and the delay.",
          avoid=("flight", "flights", "airline", "plane", "faulty", "broken", "shop", "item",
                 "online order", "hotel", "holiday", "luggage",
                 "concert", "gig", "festival", "theatre", "theater", "cinema", "match",
                 "season ticket", "event", "show")),
    entry("event-ticket-refund",
          (("refund", "refunds", "money back", "cancel", "cancelled", "canceled", "cancelling",
            "resell", "resale", "exchange", "swap",
            "postponed", "postponement", "rescheduled", "reschedule", "moved to",
            "new date", "new venue", "venue changed", "cancelled the gig"),
           ("concert", "gig", "gigs", "festival", "theatre", "theater", "cinema", "match",
            "stadium", "show", "comedy", "musical", "opera", "ballet", "event")),
          "Go back to whoever sold you the ticket - the box office or the agency, not the venue - "
          "because their terms decide it, and a ticket is usually non-refundable if you simply "
          "cannot go. If the show is cancelled or moved you are owed the face value back, and "
          "whether the booking fee comes too depends on the seller; ask for a refund rather than a "
          "credit note. If you just cannot make it, some sellers run an official resale or ticket "
          "exchange, which gets you more than nothing.",
          avoid=("train", "trains", "rail", "railway", "flight", "flights", "airline", "plane",
                 "bus", "coach", "ferry", "hotel", "parking", "season ticket", "loyalty",
                 "resell", "resale", "reselling", "sell", "selling", "sold", "give my ticket",
                 "pass on", "transfer"),
          bias=1),
    entry("ticket-refund-general",
          (("refund", "refunds", "money back", "cancel", "cancelled", "canceled", "cancelling"),
           ("ticket", "tickets")),
          "Tell me what the ticket is for and I will be exact, because the rules differ: a train "
          "is a refund less a small admin fee, a flight follows the fare's own rules, and a gig or "
          "theatre ticket is the seller's terms. What is the same everywhere is that if the "
          "company cancels on you, you are owed your money back.",
          avoid=("train", "trains", "rail", "railway", "railcard", "flight", "flights", "flying",
                 "airline", "airlines", "plane", "airport", "bus", "coach", "ferry", "tram",
                 "hotel", "concert", "gig", "festival", "theatre", "theater", "cinema", "match",
                 "stadium", "show", "event", "comedy", "musical", "opera", "ballet",
                 "parking", "season ticket", "lottery", "raffle")),

    entry("resell-ticket",
          (("resell", "resale", "reselling", "sell", "selling", "sold", "sell out",
            "give my ticket", "give my tickets", "give it to a friend", "give them to a friend",
            "pass on", "pass my ticket", "transfer", "transferring", "name change",
            "get rid of my ticket", "hand over"),
           ("ticket", "tickets", "seat", "seats")),
          "Sell it back through the seller, not on social media: the box office, the agent's own "
          "fan-to-fan resale, or a face-value site, because a ticket sold in a Facebook group can "
          "be refused at the door when the name does not match. Most tickets are "
          "non-transferable, so read the terms first and ask for a name change in writing if they "
          "allow one. Sell at or below face value and keep the sale inside the platform, so the "
          "buyer is covered and you cannot be blamed for a ticket that does not scan. An unused "
          "advance train ticket can sometimes be changed for a fee instead, which is often worth "
          "more than reselling it.",
          avoid=("expenses", "expense", "receipt", "receipts", "mileage", "claim back",
                 "reimburse", "car", "phone", "laptop", "house", "shares", "stocks", "season ticket",
                 "railcard", "advance ticket")),

    entry("flight-cancelled-refund",
          (("refund", "refunds", "money back", "reimbursed", "reimbursement", "cancelled",
            "canceled", "cancel", "cancelling"),
           ("flight", "flights", "airline", "airlines", "plane", "booking", "holiday")),
          "A cancellation is your choice of a full refund or a replacement flight, and the airline "
          "has to pay the money back within seven days - ask in writing with the booking reference "
          "and keep it. You may also be owed 220 to 520 pounds per person if they told you less "
          "than 14 days before, unless the cause was extraordinary like weather or air traffic "
          "control. Do not accept a voucher if you would rather have the cash.",
          avoid=("owed", "am i owed", "entitled", "faulty", "broke", "broken", "kettle",
                 "train", "trains", "rail", "railway",
                 "bus", "coach", "ferry", "tram", "hotel", "package holiday", "luggage",
                 "baggage", "parcel", "delivery", "shop", "online order", "sale",
                 "compensation", "compensated", "claim compensation",
                 "rights", "what am i entitled", "am i entitled",
                 "my manager", "my boss", "my employer", "annual leave", "day off", "days off",
                 "rota", "shift", "shifts", "my job", "called in",
                 "by work", "because of work", "work cancelled", "work has cancelled",
                 "work said no", "my work",
                 "concert", "gig", "festival", "theatre", "theater", "cinema", "match",
                 "season ticket", "event", "show",
                 "course", "courses", "class", "classes", "lesson", "lessons", "member",
                 "membership", "club", "gym", "school", "nursery", "subscription"),
          bias=1),
    entry("flight-change",
          (("change", "changes", "cancel", "cancelling", "cancelled", "refund", "refunded",
            "move", "postpone", "switch", "amend"),
           ("my flight", "my flights", "the flight", "flight date", "the date", "my booking",
            "the booking", "my fare", "flight")),
          ("Ring the airline as soon as you know: a cheap fare is usually changeable for a fee plus "
           "any difference in fare, and often not refundable at all, so ask before you cancel. "
           "Flexible fares cost more on the day but pay for themselves once plans move. If the "
           "reason is illness or a bereavement, check your travel insurance before you ring."),
          avoid=("train", "trains", "rail", "railway", "tube", "bus", "coach", "ferry",
                 "hotel", "booking.com", "hire car", "car hire", "rental", "name", "address",
                 "password", "booking reference", "seat", "currency", "money", "appointment",
                 "compensation", "compensated", "claim", "claiming", "owed", "entitled",
                 "delay", "delayed", "rights", "eu261")),
    entry("missed-flight",
          (("missed", "miss my flight", "miss the flight",
            "missed my flight", "missed the flight", "miss my plane", "miss the plane",
            "missed my plane", "missed the plane", "miss a flight", "missed a flight",
            "missing my flight", "missing the flight", "missing a flight",
            "missing my plane", "missing the plane", "missed our flight",
            "miss our flight", "missing our flight",
            "too late for my flight", "too late for the flight", "no show", "no-show",
            "late for my flight", "late for the flight"),
           ("flight", "flights", "plane", "planes", "airline", "airlines", "boarding",
            "check in", "check-in", "departure", "gate")),
          ("A no-show usually voids the ticket, so ring the airline the moment you know rather than "
           "at the airport: many will move you to a later flight for a fee, and a flexible fare may "
           "let you do it free. Check the check-in closing time, which is often 45 to 60 minutes "
           "before departure, and see whether your insurance covers the reason you were late."),
          avoid=("will i", "if i leave", "if i set off", "how early", "how long before",
                 "what time should i", "leave at", "set off", "traffic on the way",
                 "check in online", "bag drop", "too early", "get there",
                 "bag", "bags", "baggage", "suitcase", "suitcases", "luggage", "holdall",
                 "rucksack", "backpack", "carousel")),
    entry("flight-not-taken",
          (("didnt take", "didn't take", "did not take", "didnt use", "didn't use",
            "did not use", "didnt go", "didn't go", "did not go", "couldnt take",
            "couldn't take", "could not take", "couldnt go", "couldn't go",
            "could not go", "not going to take", "decided not to go"),
           ("flight", "flights", "plane", "planes", "airline", "airlines", "flying")),
          ("The fare is usually gone, but the tax and the airport charges come back: ask the airline "
           "in writing with the booking reference and most refund those even on a non-refundable "
           "ticket, often 30 to 60 pounds on a short-haul. Ring them before departure if you can, "
           "because many will move you to a later flight for a fee, and check whether your travel "
           "insurance covers the reason you could not go."),
          bias=1),
    entry("missed-connection",
          (("miss my connecting flight", "missed my connecting flight", "miss the connecting flight",
            "missed connecting flight", "miss a connection",
            "missed a connection", "miss the connection", "missed the connection",
            "miss my connection", "missed my connection", "connecting flight"),
           ("what", "what happens", "what do i do", "what should i do", "who pays", "hotel",
            "rebook", "next", "now", "entitled", "compensation", "help", "late", "delayed")),
          "Go straight to the airline's desk or app before the next one closes: when both legs are "
          "on one ticket the airline has to put you on the next available seat, and pay for a hotel "
          "and meals if the wait is overnight. On two separate tickets the second one is a no-show "
          "and nobody owes you a seat, so ring that airline and ask anyway. Keep every receipt.",
          avoid=("delay pay", "compensation for", "how much compensation", "ehic", "insurance")),

    entry("plane-seat",
          (("seat", "seats", "sit", "sitting"),
           ("best", "better", "window", "aisle", "middle", "pick", "choose", "legroom",
            "exit row", "on a plane", "on the plane", "on a flight", "on a long flight")),
          ("Take an aisle seat if you get up, want to stretch a leg out, or are tall; a window if "
           "you want to sleep against the wall and not be climbed over. The middle seat is the one "
           "to avoid. An exit row buys legroom but no bag under the seat in front."),
          avoid=("train", "trains", "rail", "railway", "tube", "underground", "bus", "coach",
                 "ferry", "boat", "theatre", "theater", "cinema", "concert", "stadium",
                 "restaurant",
                 "sit up", "sit ups", "plank", "planks", "squat", "squats", "crunch",
                 "crunches", "press up", "deadlift", "workout", "gym")),
    entry("sleep-on-a-plane",
          (("sleep", "sleeping", "get some sleep", "fall asleep"),
           ("plane", "planes", "flight", "flights", "flying", "red eye", "red-eye",
            "night flight", "overnight flight", "long haul")),
          ("Set your watch to the time where you are going as soon as you board, and sleep to that "
           "clock rather than the one at home. Earplugs and an eye mask do more than any gadget, "
           "and skip the wine: it helps you drop off and wakes you at 3am. Book an aisle or window "
           "seat, keep the shoes loose, and take the coffee at the end, not the start.")),
    entry("business-class",
          (("business class", "first class", "premium economy", "club class"),
           ("worth", "worth it", "better", "upgrade", "cost", "pay", "cheap", "cheaper")),
          ("On a long overnight it buys sleep, and that is usually the whole point: a flat bed and "
           "a lounge shower on an eight-hour flight is worth more than on a two-hour hop. On a "
           "daytime short-haul it buys a bigger seat and a meal, which is rarely worth the money. "
           "Look at premium economy before you decide."),
           avoid=("post", "posts", "postage", "post office", "postbox", "post box", "letter",
                  "letters", "parcel", "parcels", "stamp", "stamps", "envelope", "envelopes",
                  "royal mail", "signed for", "recorded delivery", "special delivery", "delivery",
                  "duty free", "customs",
                  "degree", "degrees", "university", "uni", "honours", "honors", "bachelor",
                  "bsc", "msc", "grade", "grades", "gpa", "undergraduate", "graduate",
                  "dissertation", "thesis", "exam", "exams", "pass mark", "classification")),
    entry("travel-advice-abroad",
          (("safe to travel", "safe to visit", "safe to go", "is it safe in", "travel advice",
            "travel warning", "travel advisory", "foreign office", "advisory"),
           tuple(sorted(WATER))),
          _travel_advice),
    entry("vape-on-a-plane",
          (("vape", "vapes", "vaping", "e-cigarette", "e-cigarettes", "ecig", "ecigs", "e cig",
            "vape pen", "eliquid", "e-liquid", "nicotine"),
           ("plane", "planes", "flight", "flights", "fly", "flying", "airport", "security",
            "hand luggage", "carry on", "cabin", "hold", "luggage", "bag", "bags", "abroad",
            "allowed", "take")),
          "Vapes travel in your hand luggage, never in the hold: the device and any spare "
          "batteries in the cabin, and the liquid in the 100 ml bag. Do not use it on the plane or "
          "in the terminal, including the toilets, because most airlines treat it as smoking. A "
          "few countries ban them completely, so check the arrival country's rules as well as "
          "your airline's own.",
          avoid=("smoking", "quit", "stop smoking", "cigarette", "cigarettes", "give up",
                 "withdrawal", "nicotine patch", "price", "cost", "where to buy", "cheapest",
                 "hospital", "ward", "hospice", "clinic", "care home", "the ward",
                 "found", "found a vape", "my daughter", "my daughters", "my son", "my sons",
                 "my child", "my children", "my kid", "my kids", "teenager", "teen", "school bag",
                 "schoolbag", "backpack", "rucksack",
                 "train", "tube", "bus", "coach", "ferry", "pub", "restaurant", "festival",
                 "concert", "gig", "school", "work", "office", "in the building"),
          bias=2),

    entry("duty-free",
          (("duty free", "duty-free", "customs allowance", "duty free allowance", "bring back",
            "bring home", "declare at customs", "goods allowance",
            "customs limit", "alcohol allowance", "tobacco allowance",
            "bring", "brings", "bringing", "brought",
            "take back", "takes back", "taking back", "took back",
            "take home", "takes home", "taking home", "took home"),
           ("uk", "home", "britain", "england", "alcohol", "wine", "spirits", "cigarettes",
            "tobacco", "limit", "allowance", "how much", "what can i", "back")),
          ("Coming into the UK you can bring 4 litres of spirits, 18 litres of wine or 42 litres of "
           "beer, 200 cigarettes, and other goods - perfume and gifts count here - up to 390 "
           "pounds, all per person. Anything above "
           "that you declare in the red channel and pay duty on. Keep the receipts, and note that "
           "the person carrying it must own it."),
          bias=2,
          guard=lambda understood: not _a_visit_to_a_home(understood),
          avoid=("through security", "security", "hand luggage", "cabin bag", "cabin bags",
                 "keeps borrowing", "keeps taking", "borrows my", "borrowing my", "borrowed my",
                 "lends out", "never brings it back", "never bring them back",
                 "never brings them back", "never gives it back", "never give them back",
                 "banned", "confiscated", "scanner", "scanned", "liquid", "liquids",
                 "cheese", "cheeses", "meat", "meats", "ham", "bacon", "sausage", "sausages",
                 "milk", "butter", "cream", "yoghurt", "yogurt", "eggs", "food", "foods",
                 "sandwich", "sandwiches", "fruit", "vegetables", "veg", "plants", "plant",
                 "seeds", "flowers", "bulbs", "potato", "potatoes", "my dog", "my cat", "pets",
                 "medicine", "medicines", "prescription", "cash", "how much money", "currency",
                 "take home pay", "net pay", "my pay", "payslip", "pay slip", "wages",
                 "salary", "income", "tax code",
                 "restaurant", "restaurants", "cafe", "cafes", "café", "the pub", "pub lunch",
                 "cinema", "theatre", "theater", "gig", "concert", "festival", "party",
                 "wedding", "birthday", "barbecue", "bbq", "picnic", "office", "at work",
                 "to work", "school", "college", "university", "hospital", "ward", "appointment",
           "library", "libraries", "into the library", "the canteen", "staff room",
           "hotel room", "my hotel", "the hotel", "in the hotel", "airbnb", "campsite",
                 "football", "match", "church", "funeral",
                 "pay", "payslip", "payslips", "salary", "wage", "wages", "rise", "raise",
                 "promotion", "overtime", "bonus", "tax code", "take home pay", "net pay",
                 "income tax", "national insurance", "employer", "employment",
                 "a month", "per month", "monthly", "a year", "per year", "a week", "per week",
                 "weekly", "an hour", "hourly", "after tax", "before tax", "gross")),
    entry("weekend-away",
          (("weekend away", "weekend break", "city break", "night away", "nights away",
            "mini break", "short break", "cheap weekend", "getaway", "days away",
            "couple of nights away", "two nights away"),
           ("cheap", "cheaper", "budget", "plan", "planning", "book", "booking", "where",
            "idea", "ideas", "afford", "organise", "organize")),
          ("Go the weekend after a bank holiday, or in the shoulder season, and book the train "
           "three or four weeks ahead with a railcard - it usually costs less than the petrol. "
           "Stay one town out from the famous one and travel in: a twenty-minute train is a few "
           "pounds and the same room is half the price. Two nights is plenty for a city, so pick "
           "one area to walk and one thing to go inside for, and eat the big meal at lunch, when "
           "set menus are cheapest. Two nights for two, with travel and a room, is about £250."),
          ask=("weekend away", "weekend break", "city break", "night away", "nights away",
               "mini break", "short break", "cheap weekend", "getaway", "days away",
               "couple of nights away", "two nights away"),
          avoid=("flights to", "cheap flights", "which city", "best city", "in the world",
                 "meal", "meals", "dinner", "dinners", "cook", "cooking", "food", "recipe",
                 "recipes", "lunch", "breakfast", "shop", "shopping", "supermarket")),

    entry("cheap-accommodation",
          (("cheap", "cheaper", "cheapest", "cheaply", "budget", "afford", "affordably"),
           ("accommodation", "hotel", "hotels", "somewhere to stay", "place to stay", "a bed",
            "guesthouse", "hostel", "hostels", "lodging", "room for the night")),
          ("Book direct with a small hotel or guesthouse once you know roughly where you want to "
           "be: a phone call often beats the price on the booking site, and it is the cheapest way "
           "in small towns. Hostels and apart-hotels win for a week, and a kitchen saves more than "
           "a lower nightly rate. Look at the total with tax and breakfast, not the headline."),
          avoid=("where should i stay", "which area", "best area", "where to stay",
                 "neighbourhood", "neighborhood", "rent", "mortgage", "buy", "flights", "flight")),

    entry("hotel-booking-when",
          (("hotel", "hotels", "guesthouse", "guest house", "b&b", "hotel room", "a room",
            "rooms", "wedding guests", "wedding rooms", "the wedding party",
            "rooms for a wedding"),
           ("when should i book", "when do i book", "when to book", "how early", "how far in",
            "how far ahead", "how long before", "in advance", "weeks before", "months before",
            "book early", "book ahead", "last minute", "block of rooms", "for a wedding",
            "guests", "how many rooms")),
          ("Book the room as soon as the date is fixed if it is a weekend, a city or a wedding - "
           "four to six weeks ahead is enough for most trips, and three months or more for a "
           "popular place in summer or a bank holiday. Midweek and January are where last-minute "
           "hunting pays. If a booking site shows less than the hotel's own site, ring the desk: "
           "they usually match it, and the direct terms are better."),
          avoid=("how many guests", "how many people", "guest list", "number of guests",
                 "how many to invite", "catering", "caterer", "the venue", "menu",
                 "complain", "complaint", "complaints", "dirty", "clean", "cleaned", "cleaning",
                 "bed bugs", "noise", "noisy", "rude staff", "cockroach", "cockroaches",
                 "cheap hotel", "cheap hotels", "cheaper hotel", "cheaper hotels", "cheaper room",
                 "cheap room", "cheapest", "budget", "somewhere to stay", "place to stay",
                 "cancel", "cancelled", "canceled", "refund", "refunded", "wifi", "wi-fi",
                 "address", "parking", "dog", "pets", "breakfast included",
                 "give", "giving", "as a gift", "as a present", "gift", "gifts",
                 "song", "songs", "music", "playlist", "band", "bands", "dj", "first dance",
                 "aisle", "register", "hymn", "hymns",
                 "present", "presents", "envelope", "how much money",
                 "wear", "wearing", "outfit", "outfits", "dress", "dresses", "jumpsuit",
                 "jumpsuits", "hat", "hats", "fascinator", "shoes", "heel", "heels", "suit",
                 "sock", "socks", "tie", "ties", "waistcoat", "braces", "cufflinks",
                 "suits", "tie", "colour", "color", "dress code", "black tie",
                 "put on", "putting on", "clothes")),

    entry("tap-water-abroad", (("water", "tap water", "ice"),
                               ("safe", "drink", "drinking", "ok", "okay", "fine",
                                "abroad", "holiday",
                                "brown", "rusty", "chlorine", "tastes", "taste", "smells of",
                                "bottled", "mains")),
          _tap_water, bias=2,
          avoid=("more water", "enough water", "glasses", "hydrated", "dehydrated",
                 "how much water", "litres", "liters",
                 "with meals", "with food", "with my meal", "with a meal", "during meals",
                 "before a meal", "before meals", "after a meal", "after meals", "while eating",
                 "float", "floats", "density", "freeze", "freezes", "frozen",
                 "tooth", "teeth", "gums", "gum", "enamel", "dentist", "dentists",
                 "twinge", "toothache", "hurts to drink", "hurts when i drink",
                 "pots", "pot pots", "plant pots", "plants", "garden",
                 "water the plants", "while im away", "while i am away", "greenhouse")),

    entry("baggage-allowance",
          (("luggage", "baggage", "cabin bag", "hand luggage", "checked bag", "hold bag",
            "suitcase", "rucksack", "backpack", "backpacks", "daypack", "day pack",
            "bag", "bags",
            "ryanair", "easyjet", "easy jet", "jet2", "wizz", "wizz air", "british airways",
            "tui", "aer lingus", "vueling", "norwegian", "loganair"),
           ("allowance", "limit", "how much", "how many", "weight", "size", "kg", "heavy",
            "take", "pack", "checked", "cabin", "hold", "big", "large", "how big", "how large",
            "dimensions", "measurements", "weigh", "weighing", "biggest",
            "ok", "okay", "fine", "allowed", "suitable", "too heavy", "overweight", "excess",
            "over", "problem", "hand", "carry", "on the plane", "on a plane")),
          "Check the airline's own allowance on your booking: a cabin bag is usually around 55 x 40 "
          "x 20 cm and 7 to 10 kg, and a checked bag around 20 to 23 kg. Weigh the bag at home, "
          "because excess weight at the airport is expensive and adding a bag online beforehand is "
          "much cheaper. On a connecting flight the strictest airline's limit applies.",
          ask=("allowance", "limit", "how much", "how many", "weight", "size", "kg", "heavy",
               "big", "large", "how big", "how large", "dimensions", "measurements", "weigh",
               "weighing", "biggest", "what", "can i", "can we", "is there", "does",
               "ok", "okay", "allowed", "fine", "suitable", "count", "counts", "too heavy",
               "overweight", "excess", "over", "problem",
               "hand", "luggage", "baggage", "backpack", "rucksack", "carry"),
          avoid=("cost", "price", "buy", "sale", "lost", "stolen", "damaged", "delayed",
                 "data", "phone", "mobile", "razor", "liquid", "liquids", "medicine",
                 "medication", "knife", "scissors", "battery", "batteries", "lighter",
                 "security", "train", "coach", "bus", "ferry", "cruise")),
    entry("cabin-bag-rules",
          (("hand luggage", "cabin bag", "carry on", "carry-on", "hand baggage", "cabin",
            "on the plane", "on a plane", "on board", "through security", "at security",
            "the plane", "plane", "fly with", "take on the plane", "suitcase", "hold",
            "checked bag", "holdall"),
           ("take", "taking", "bring", "bringing", "carry", "carrying", "allowed", "allow",
            "permitted", "not allowed", "cant take", "can't take", "cannot take", "can i get",
            "am i allowed", "prohibited", "banned", "forbidden", "confiscated", "in my bag",
            "my bag", "pack", "packing", "put in", "go in", "goes in", "bring back",
            "razor", "razors", "scissors", "tweezers", "penknife", "knife", "corkscrew",
            "lighter", "matches", "power bank", "power banks", "battery", "batteries",
            "screwdriver", "tools", "deodorant", "perfume", "toothpaste", "sun cream",
            "medicine", "tablets", "food", "sandwiches", "bottle", "liquid", "vape",
            "nail scissors", "clippers", "multi tool", "swiss army")),
          _cabin_rules, bias=2, guard=_cabin_guard,
          ask=("take", "bring", "carry", "allowed", "banned", "not allowed", "can i",
               "am i", "pack", "put"),
          avoid=("size", "big", "large", "how big", "how large", "dimensions", "measurements",
                 "backpack", "backpacks", "rucksack", "rucksacks", "daypack", "day pack",
                 "is a bag", "my bag ok", "bag allowed",
                 "weight", "weigh", "weighing", "heavy", "allowance", "limit", "kg", "kilo",
                 "kilos", "kilogram", "how much does", "how many kilos",
                 "lost", "damaged", "delayed", "buy", "cheap", "cost", "price", "sale",
                 "repair", "wheel", "zipper", "zip", "handle", "lock", "padlock", "straps",
                 "train", "coach", "bus", "ferry", "cruise", "moving house",
                 "vape", "vapes", "vaping", "e-cigarette", "e-cigarettes", "ecig", "ecigs",
                 "eliquid", "e-liquid", "nicotine",
                 "medicine", "medicines", "medication", "medications", "insulin", "inhaler",
                 "inhalers", "epipen", "epi-pen", "epipens", "tablets", "pills", "prescription",
                 "paracetamol", "ibuprofen", "aspirin", "painkillers", "antihistamine",
                 "hayfever", "hay fever", "antibiotics", "inhalers",
                 "food", "sandwich", "sandwiches", "snack", "snacks", "lunch", "picnic",
                 "shoes", "shoe", "belt", "boots", "scanner", "pat-down", "pat down", "trays",
                 "tray",
                 "pram", "prams", "pushchair", "pushchairs", "buggy", "stroller", "car seat",
                 "toddler", "toddlers", "infant", "infants", "newborn", "newborns",
                 "dog", "dogs", "cat", "cats", "pet", "pets", "rabbit", "hamster", "bird",
                 "parrot", "wheelchair", "mobility scooter", "crutches",
                 "guitar", "violin", "cello", "instrument", "instruments", "drums", "keyboard",
                 "bike", "bikes", "bicycle", "surfboard", "skis", "ski", "snowboard",
                 "paddleboard", "kayak")),
    entry("flight-bag-fee",
          (("checked bag", "checked bags", "checked baggage", "hold bag", "hold luggage",
            "checked luggage", "checked in bag", "bag in the hold", "baggage fee", "bag fee",
            "bag fees", "extra bag", "second bag", "suitcase in the hold"),
           ("cost", "costs", "price", "priced", "how much", "pay", "paying", "paid", "fee",
            "fees", "charge", "charged", "worth", "cheaper", "cheapest", "add a bag",
            "book a bag", "cost to", "how much does", "how much is", "put a bag",
            "extra luggage", "baggage")),
          "Booked online with the ticket, a 23kg bag is usually £20 to £45 each way on a budget "
          "airline, and £50 to £65 if you add it at the airport desk. A heavier bag costs more again, "
          "so weigh it at home. Compare that with a fare that includes a bag before you book: the "
          "cheap headline fare plus a suitcase often costs more than the fare that already has one.",
          bias=2,
          avoid=("reusable", "allowance", "how many kilos", "how much weight", "how heavy",
                 "how big", "how large", "size", "dimensions", "weight limit", "carrier", "supermarket", "for life", "shopping", "plastic bag",
                 "bin bag", "dog", "poo", "leaf", "leaves", "vacuum", "hoover", "storage",
                 "sleeping bag", "tea bag", "beans", "lentils", "pulses", "rice")),
    entry("car-hire",
          (("hire a car", "hire car", "rent a car", "rental car", "car hire", "car rental"),
           ("cost", "cheap", "how much", "book", "insurance", "deposit", "young driver",
            "age", "fuel", "abroad", "one way", "worth",
            "credit card", "debit card", "without a card", "no card", "card",
            "cost to hire", "cost of hiring", "cost of hire", "price of hire")),
          "Book early and compare the total with insurance included, not the headline daily rate. "
          "Check the excess and whether your own policy or a credit card already covers it. Pay the "
          "deposit on a credit card: it is usually a few hundred pounds or euros held on the card and "
          "released when you return the car. Photograph every panel before you drive off, return it "
          "full-to-full, and remember that a young or second driver usually costs extra.",
          avoid=("buy", "buying", "sell", "selling", "lease", "leasing", "my own car", "repair",
                 "breakdown", "parking", "mot", "tax")),
    entry("an-easy-walk",
          (("walk", "walks", "walking", "stroll", "strolls", "outing", "day out",
            "somewhere to go", "where can we go", "where can i go", "place to walk",
            "somewhere flat", "flat walk", "easy walk"),
           ("flat", "level", "easy", "gentle", "accessible", "wheelchair", "wheelchairs",
            "mobility", "scooter", "cant walk", "can't walk", "cannot walk", "walk far",
            "walking far", "slow walker", "bad knees",
            "bad hip", "bad back", "elderly", "keep up", "tires", "tired", "manage",
            "can manage", "manageable", "slow", "slowly", "steady", "pensioner", "nan",
            "granny", "grandma", "grandad", "buggy friendly")),
          "Go for a canal towpath, a country park or a flat riverside path: wide, level, benches "
          "along it and nothing to climb over, which is what a short walk needs. Check the surface "
          "and the slope on the site's own page before you set off, because a walk advertised as "
          "circular can still hide a stile or a flight of steps, and ring ahead if someone uses a "
          "wheelchair - big attractions, National Trust and English Heritage places among them, "
          "lend one for free if it is booked a day or two in advance. For someone who tires "
          "quickly, plan a there-and-back of half a mile with a seat at the turning point and pace "
          "it bench to bench rather than by distance. A stick helps if a hip or knee is the "
          "trouble: the handle wants to reach the crease of the wrist with the arm hanging down, "
          "it goes in the hand opposite the sore side, and the tip gets a new ferrule once it has "
          "gone smooth.",
          avoid=("dog", "dogs", "puppy", "pram", "pushchair", "baby", "toddler", "calories",
                 "pedometer", "marathon", "parkrun", "race", "km", "miles", "water",
                 "waterproof", "boots", "jacket", "pack",
                 "hurts", "hurt", "ache", "aches", "aching", "pain", "painful", "sore",
                 "injury", "injured", "is it safe", "is it ok", "ok to walk", "should i walk",
                 "good for", "bad for", "make it worse", "damage",
                 "holiday", "holidays", "away", "abroad", "trip", "trips", "flight", "flights",
                 "hotel", "hotels", "airport", "airports", "plane", "planes", "rollator",
                 "passenger", "abroad"),
          ask=("how much", "how far", "how long", "what should i", "what do i", "what can i",
               "what to take", "what to wear", "what to bring", "what can we do",
               "where can i", "where can we", "where should", "where is", "is there a",
               "is there any", "are there", "anywhere", "somewhere", "can we go", "can i go",
               "can i take", "can we take", "we need", "i need", "looking for", "is it ok",
               "flat walk", "easy walk", "gentle walk", "short walk", "level walk",
               "accessible walk", "slow walk", "a walk", "day out", "outing",
               "things to do"),
          guard=_not_the_flat_the_ground,
          bias=2),
    entry("hike-day", (("hike", "hiking", "hillwalk", "hill walk", "hill walking", "fell walk",
                        "trek", "trekking", "rambling", "ramblers", "day walk", "long walk",
                        "walks in the hills", "mountain walk", "munro", "ridge walk", "coast path",
                        "walking", "walk", "walked"),
                       ("water", "drink", "eat", "food", "snack", "snacks", "lunch", "carry",
                        "pack", "take", "bring", "fuel", "energy", "hungry", "kilos", "weight",
                        "how much water", "how much food", "how much liquid",
                        "litre", "litres", "liter", "liters", "how many litres",
                        "how much to drink")),
          _hike_day,
          avoid=("dog", "puppy", "pram", "pushchair", "baby", "toddler", "flight", "flying",
                 "airport", "hand luggage", "shop", "supermarket", "toilet", "nap", "sleep",
                 "bill", "meter", "leak", "boiler", "kettle", "plant", "plants", "bath",
                 "cant walk", "can't walk", "cannot walk", "cant walk far", "walking far",
                 "mobility", "wheelchair", "disabled", "sticks", "slow walker"),
          ask=("how much", "how many", "what should i", "what do i need", "what to take",
               "what to bring", "what do i take", "what do i bring", "what should i take",
               "what should i bring", "what to pack", "should i take", "should i bring",
               "need to", "snack", "snacks", "food", "eat", "water",
               "drink", "drinking", "carry"),
          bias=1,
          slips=("hikeing", "hikingg", "hikeing", "hikin", "hikes", "hiike", "hikey", "hikking",
                 "treking", "trecking", "rennwalking", "ramblin", "hillwalking")),
    entry("ill-on-a-plane", (("plane", "planes", "flight", "flights", "flying", "fly", "flew",
                              "airplane", "aeroplane", "cabin"),
                             ("sick", "ill", "cold", "bug", "sniffles", "cough", "germs",
                              "catch", "avoid", "pick up")),
          "Wipe the tray table, the armrest and the seat-back pocket, which are cleaned rarely, and "
          "keep your hands off your face: the germs in a cabin come from the surfaces more than the "
          "air, which is filtered. Drink water rather than alcohol or coffee, take a window seat "
          "away from the aisle, and wear a mask on a packed winter flight, which is the single "
          "biggest thing you can do.",
          avoid=("travel sick", "travel sickness", "motion", "dizzy", "nauseous", "sick bag",
                 "vomit", "throw up", "ears", "jet lag", "jetlag", "scared", "afraid", "nervous")),

    entry("lost-luggage",
          (("suitcase", "suitcases", "bag", "bags", "luggage", "baggage", "case", "rucksack"),
           ("didnt arrive", "didn't arrive", "did not arrive", "hasnt arrived", "hasn't arrived",
            "never arrived", "not arrived", "went missing", "is missing", "gone missing",
            "lost", "lost my bag", "stolen", "left behind", "delayed", "was delayed",
            "still not here", "still hasnt arrived", "on the carousel")),
          ("Report it at the airline's desk in the baggage hall before you leave, with the bag tag "
           "and your boarding pass, and do not go home without a written report and a reference "
           "number: that number is what every later claim and refund hangs on. Ask what they will "
           "pay for clothes and toiletries in the meantime and keep every receipt. Most bags turn "
           "up within 24 to 48 hours; if it has not after 21 days, claim for it as lost."),
          ask=("what do i do", "what should i do", "what happens", "where do i", "how do i",
               "can i claim", "claim", "compensation", "report", "help", "now", "anything",
               "is it", "will i", "do i get", "who do i"),
          avoid=("allowance", "limit", "how much", "weight", "kg", "cabin", "hand luggage",
                 "pack", "carry on", "data", "phone", "razor", "liquids", "lock", "padlock",
                 "on holiday", "pickpocket", "pickpocketed", "robbed", "mugged", "wallet",
                 "passport", "money", "damaged", "damage", "torn", "broken zip")),
    entry("travel-sickness",
          (("travel sick", "travel sickness", "motion sickness", "car sick", "carsick",
            "carsickness", "sea sick", "seasick", "seasickness", "motion sick",
            "sick in the car", "sick on the boat", "sick on a boat", "sick on the ferry",
            "sick on the plane", "sick on the bus", "dizzy in the car"),
           ("what can i", "what helps", "how do i", "prevent", "avoid", "stop", "help",
            "medicine", "tablets", "tablet", "give", "child", "children", "kid", "kids",
            "toddler", "my son", "my daughter", "pills", "bands")),
          ("Sit facing forward, as far forward and as low as you can, look at the horizon rather "
           "than a screen or a book, and get fresh air: those four do more than anything you can "
           "buy. Eat something plain before you go, not a big meal, and stop when you can. For a "
           "child ask a pharmacist which antihistamine suits their age and weight, and give it an "
           "hour before you set off, because the doses are not the adult ones."),
          avoid=("fever", "temperature", "vomiting", "diarrhoea", "diarrhea", "not eating",
                 "chest", "asthma", "breathing", "rash", "croup", "ear infection")),
    entry("coach-travel",
          (("coach", "coaches", "megabus", "national express", "flixbus", "bus"),
           ("book", "booking", "cheap", "cheaper", "cheapest", "cost", "how much", "how long",
            "luggage", "bags", "to ", "from ", "overnight", "airport")),
          ("Coaches are the cheapest way between two cities: booked two or three weeks ahead a "
           "long trip is often under 20 pounds when the train is over 60, and the overnight coach "
           "saves a hotel night as well. Book on the operator's own site or app, take the ticket "
           "on your phone, and put the big bag in the hold, which is included but has to be tagged. "
           "Arrive 15 minutes early: coaches leave on time and do not wait."),
          ask=("book", "booking", "cheap", "cheaper", "cheapest", "cost", "how much", "how long",
               "to ", "from ", "overnight", "is it", "can i", "should i",
               "which is better", "which one", "vs", "versus", "compare", "difference",
               "or the train", "than the train", "train or"),
          avoid=("tour bus", "sightseeing bus", "hop on", "school bus", "double decker",
                 "seat belt", "driving", "park", "parking", "route", "timetable", "live",
                 "running late", "cancelled",
                 "child", "children", "kids", "kid", "my son", "my daughter", "under 5s",
                 "under fives", "5 year old", "4 year old", "child fare", "child ticket",
                 "complain", "complaint", "complaints", "report", "driver", "drivers",
                 "bus driver", "bus company", "bus operator", "rude", "shouted",
                 "left my bag", "lost property", "left it on", "left something on",
                 "which bus", "what bus", "bus route", "routes", "bus stop", "bus number",
                 "track", "tracking", "live times", "how often", "how far", "nearest",
                 "wheelchair", "pram", "pushchair", "mobility scooter", "school run")),
    entry("stay-well-abroad",
          (("avoid", "not get", "dont get", "don't get", "prevent", "stay well", "not catch",
            "get sick", "got sick", "food poisoning", "delhi belly", "bad stomach",
            "tummy bug", "stomach bug", "runs", "diarrhoea", "diarrhea",
            "safe to eat", "is it safe", "worth eating"),
           ("abroad", "on holiday", "travelling", "traveling", "in mexico", "in india",
            "in egypt", "in thailand", "in turkey", "in morocco", "in peru", "in kenya",
            "in bali", "there", "street food", "eating out", "ice", "salad", "fruit",
            "water")),
          ("Eat where it is busy and freshly cooked, and have it hot: a queue and a hotplate are "
           "better signs than a clean table. Have bottled or filtered water and the ice made from "
           "it, peel your own fruit, and skip the raw salad that a kitchen has washed in tap water. "
           "Carry rehydration sachets and a hand gel, and check the vaccinations and malaria advice "
           "for that country about six weeks before you go."),
          avoid=("pregnant", "pregnancy", "baby", "toddler", "child", "children", "asthma",
                 "allergy", "allergies", "tablet", "tablets", "medicine", "medication",
                 "insurance", "compensation", "flu", "covid", "vaccine", "vaccination",
                 "drink the water", "drinking water", "tap water", "water safe",
                 "hot water", "running out of hot water", "run out of hot water", "boiler",
                 "stopcock", "immersion", "cylinder", "radiator", "radiators", "heating",
                 "kettle", "shower", "bath", "plumber", "tank", "no hot water",
                 "card", "cards", "wallet", "cash", "money", "atm", "atm machine", "currency",
                 "euros", "dollars", "pounds", "bank", "pay by card",
                 "lentils", "chickpeas", "quinoa", "rice", "pasta", "spaghetti", "noodles",
                 "greens", "water runs clear", "runs clear")),
    entry("departure-check-in",
          (("check in", "checking", "check-in", "arrive", "get there", "be there", "how early",
            "how long before", "how late"),
           ("cruise", "ferry", "boat", "eurostar", "tunnel", "le shuttle", "port", "terminal",
            "coach station", "train station", "station")),
          ("Check your operator's own figure the day before, because it is the one that counts: a "
           "cruise wants you at the terminal two to three hours before, a ferry an hour with a car "
           "and about thirty minutes on foot, and Eurostar asks for 75 to 90 minutes. Boarding "
           "closes before departure and a ship or a coach will not wait, so aim to be there early "
           "and take a book rather than cutting it fine."),
          ask=("how early", "how long before", "how late", "what time", "when should", "should i",
               "do i need", "check in", "checking", "arrive"),
          avoid=("airport", "flight", "plane", "fly", "bag drop", "hotel", "check out",
                 "checkout", "hand luggage", "online check in")),
    entry("flight-check-in",
          (("check in", "checking in", "check-in", "checkin", "boarding pass"),
           ("flight", "flights", "plane", "airline", "airport", "flying", "easyjet", "ryanair",
            "jet2", "online", "app", "before")),
          ("Check in online as soon as it opens, usually 24 to 48 hours before a short-haul flight "
           "and up to 72 on some, and save the boarding pass into your phone wallet as well as "
           "your email: a screenshot works when the signal does not. Have your passport details "
           "to hand. If you are checking a bag, drop it before the airline's cut-off, which is "
           "usually 45 to 60 minutes before departure and a full two hours at some airports, and "
           "if you would rather check in at the desk, get there about three hours before the "
           "flight: the desks close on that same timetable, queue and all."),
          ask=("how do i", "how to", "how can i", "what do i", "do i", "should i", "can i",
               "where do i", "when do i", "when should", "what time",
               "check in", "check-in", "checkin", "checking in"),
          avoid=("hotel", "check out", "checkout", "cruise", "ferry", "eurostar", "campsite",
                 "holiday cottage", "airbnb", "villa", "car hire", "hire car", "self catering",
                 "guest house", "bed and breakfast", "how much", "cost", "price", "fee", "fees",
                 "weight", "weigh", "allowance", "hand luggage", "cabin bag", "extra"),
          ),
    entry("stopover-jet-lag",
          (("stopover", "stop over", "layover", "connecting flight", "connecting", "change planes",
            "breaks up", "break up"),
           ("jet lag", "jetlag", "jet-lagged", "body clock", "tired", "sleep", "help", "better",
            "worse", "should i", "worth it")),
          ("A stopover only helps if you can sleep in a bed: a night in a hotel halfway resets you "
           "gently, while a four-hour wait in an airport at 3am just breaks the journey. If you "
           "are stopping anyway, take the wait in daylight at the far end and set your watch to "
           "the destination as you board the last flight, then sleep on that leg if it is night "
           "there."),
          avoid=("flight cancelled", "missed my connection", "short connection", "bag",
                 "luggage", "hotel near", "airport hotel")),
    entry("layover-meaning",
          (("layover", "layovers", "a layover", "stopover", "stop over", "stopovers",
            "connecting flight", "connecting flights", "my connection", "our connection",
            "flight connection", "connection flight", "connection time", "connection at",
            "connection between flights", "how long is my connection",
            "how long does a connection", "connection need", "connection needs",
            "how long between flights", "connection tight", "time between flights",
            "transit at the airport", "airside transit"),
           ("what", "whats", "what is", "mean", "means", "explain", "difference", "different",
            "vs", "versus", "how long", "counts as")),
          ("A layover, or a connection, is the wait at an airport between two flights, and a "
           "stopover is the same thing when it is long enough to leave the airport, usually a "
           "night or more. A connection under about two hours on the same ticket is the airline's "
           "problem if the first flight is late, so the risk is a tight change, not a long wait. "
           "On two separate tickets you are on your own for a missed second flight, so leave "
           "three hours or more."),
          avoid=("missed my connection", "short connection", "jet lag", "body clock", "sleep",
                 "hotel near", "airport hotel", "bag", "luggage")),
    entry("flexible-ticket",
          (("flexible ticket", "flexible tickets", "flexi ticket", "flex fare", "flexible fare",
            "change my flight", "change the date"),
           ("what", "whats", "mean", "means", "worth", "cost", "how much", "does it",
            "difference", "explain", "refundable", "should i")),
          ("A flexible ticket is the fare that lets you change the date, usually for no fee or a "
           "small one, where a cheap fare charges £30 to £70 plus any fare difference to change "
           "and often nothing back if you cancel. It is worth it when the date might move: work, "
           "a hospital appointment, a family thing. Check whether the fare is changeable or "
           "refundable, because they are not the same, and buy the cheaper ticket plus travel "
           "insurance when the difference is more than the change fee."),
          avoid=("how do i change", "how can i change", "my flight was cancelled", "cancel my")),
    entry("visa-timing",
          (("esta", "visa", "evisa", "e-visa", "entry permit", "etias", "entry requirements",
            "tourist card", "visa waiver"),
           ("need", "apply", "how long", "how much", "cost", "when", "before", "do i",
            "still", "valid", "how many days", "how early")),
          ("Apply on the country's own government site, never a paid lookalike, and apply early: "
           "an ESTA for the USA is valid two years and should be done at least 72 hours before you "
           "fly, while a visa for most countries is a few weeks, so start six to eight weeks out. "
           "Check the entry rules for your own passport and any country you change planes in, and "
           "keep the approval on your phone and printed."),
          avoid=("passport renew", "passport expire", "renew my passport", "driving licence",
                 "insurance", "job", "work permit", "student visa for my course", "university")),
    entry("package-or-diy",
          (("package holiday", "package deal", "package", "all inclusive", "book a package",
            "diy", "do it myself", "book it myself", "separately"),
           ("cheaper", "worth it", "better", "should i", "or", "which", "protect", "protection",
            "atol", "flights and hotel", "hotel and flights", "risk")),
          ("A package buys you protection and less admin: the flights, the transfer and the hotel "
           "are one booking, and if the operator fails you are covered and brought home. Booking it "
           "yourself is usually cheaper, especially for a city break where you want a flat rather "
           "than a hotel, but you carry the risk - so book the flight on a credit card and check "
           "the hotel's own cancellation terms. For a beach week with children, the package "
           "usually wins on the day something goes wrong."),
          avoid=("parcel", "delivery", "courier", "my package", "package arrived", "software",
                 "install", "python"),
          guard=_a_trip_to_arrange),
    entry("pram-on-a-plane",
          (("pram", "pushchair", "buggy", "stroller", "travel system", "car seat"),
           ("plane", "planes", "flight", "flights", "fly", "flying", "airline", "airlines",
            "airport", "gate", "hand luggage", "hold", "cabin", "check in", "checking in",
            "ryanair", "easyjet", "jet2", "tui", "british airways")),
          ("Almost every airline carries a pushchair free, but it goes in the hold rather than the "
           "cabin: keep it until the aircraft door, where it is tagged and taken down the steps, "
           "and pick it up on the jetty or at the baggage belt at the other end. A car seat can fly "
           "with you if you bought it a seat, and a bag over the pushchair saves the fabric. Ask "
           "for the airline's own rule in writing if you are checking it in at the desk."),
          avoid=("pram wheels", "pram tyre", "second hand pram", "which pram should i buy",
                 "pram for sale", "buggy board")),

    entry("pushchair-on-the-bus",
          (("pushchair", "pushchairs", "pram", "prams", "buggy", "buggies", "stroller",
            "strollers", "travel system"),
           ("bus", "buses", "coach", "coaches", "train", "trains", "tube",
            "underground", "tram", "trams", "metro", "public transport", "on the bus",
            "on a bus", "on the coach", "on the train", "double decker")),
          ("On a bus or a coach it travels folded, so have it down and the child out of it before "
           "the doors open: a driver can refuse a pushchair that is still open, and the space by "
           "the door belongs to a wheelchair user first. On trains and the underground a folded "
           "pushchair is free and goes in the luggage rack, and most stations have a lift, so use "
           "that rather than the escalator. For a coach trip the buggy goes in the hold - tell the "
           "driver at the door so it is not loaded under the luggage."),
          avoid=("pram wheels", "pram tyre", "which pram should i buy", "pram for sale",
                 "buggy board", "second hand pram", "sling", "car seat", "cot", "carrycot")),

    entry("travel-with-a-baby",
          (("travel", "travelling", "traveling", "fly", "flying", "flight", "plane", "holiday",
            "abroad", "long journey", "trip", "airport"),
           ("baby", "babies", "infant", "newborn", "toddler", "month old", "months old",
            "year old")),
          ("Book the leg around their nap, feed or give a dummy at take-off and landing so their "
           "ears clear, and take a sling for the airport and a change of clothes in your hand "
           "luggage. Most airlines fly a baby from about two weeks old, on your lap or in a booked "
           "bassinet seat, and a pushchair goes free in the hold. In the car they need their own "
           "car seat, rear-facing until they are 15 months, and a stop every couple of hours."),
          avoid=("crying", "cries", "screams", "wont sleep", "won't sleep", "teething", "feeding",
                 "milk", "formula", "nappy", "nappies", "vaccine", "vaccinations", "jab", "colic",
                 "car seat", "car seats", "which car seat", "pram", "pushchair", "buggy", "sling",
                 "sleep", "routine", "temperature", "fever", "sick", "reflux", "weaning",
                 "cot", "moses basket", "baby monitor",
                 "bus", "buses", "coach", "coaches", "tram", "trams", "tube", "underground",
                 "bus fare", "bus pass", "train ticket", "child fare", "school bus",
                 "fly spray", "insect spray", "bug spray", "mosquito spray", "wasp spray",
                 "air freshener", "aerosol", "the spray",
                 "camping", "campsite", "camp site", "camp", "tent", "tents", "under canvas"),
          bias=3),

    entry("family-trip",
          (("kids", "children", "child", "family", "the kids", "my son", "my daughter",
            "toddlers", "teenagers", "teens", "under 16", "under 5", "school age",
            "family holiday", "family holidays", "family trip", "kids holiday",
            "holiday with the kids", "kids abroad", "children abroad"),
           ("holiday", "holidays", "abroad", "spain", "france", "greece", "portugal", "italy",
            "turkey", "cyprus", "canaries", "trip", "travel with children",
            "sort anything", "need to sort", "what do i need", "do i need")),
          ("Four things, all before you book: a passport each, because a child's lasts five years "
           "and takes a few weeks to arrive, so do not book flights until it is in your hand; a "
           "free GHIC card each for Europe, one per person; seats together, so ask when you book, "
           "since a child under 12 is meant to sit with their adult; and travel insurance that "
           "names every child. If you are crossing a border without the other parent, take a "
           "signed letter from them saying you have their permission. Photograph every passport "
           "and keep the pictures on your phone."),
          avoid=("plane", "planes", "flight", "flights", "flying", "fly", "airport", "ears",
                 "take-off", "take off", "baby", "babies", "infant", "newborn", "pram",
                 "pushchair", "car seat", "booster", "car", "cars", "driving", "bus", "coach",
                 "train", "ferry", "cruise", "sleepover", "staying over", "stay over", "babysit",
                 "bedtime", "routine", "school", "term time", "unauthorised", "fine", "fines",
                 "sick", "ill", "fever", "diarrhoea", "vaccine", "vaccinations", "jab", "jabs",
                 "measles", "chickenpox", "insurance", "ghic", "ehic", "cost", "costs",
                 "how much", "cheap", "cheaper", "budget", "where to stay", "hotel", "hostel",
                 "suncream", "sunburn", "nappies", "nappy", "milk", "food", "dog", "cat", "pet",
                 "pets", "divorce", "custody", "court order", "access", "compass",
                 "pack", "packs", "packing", "packed", "what to pack", "suitcase", "luggage",
                 "good for kids", "good with kids", "good for children", "good with children",
                 "better for kids", "best for kids", "good for families", "good for a family",
                 "where should we go", "which is better", "which is best",
                 "passport", "passports", "visa", "visas", "renew", "renewing", "renewed",
                 "runs out", "run out", "expires", "expiring", "photo", "photos",
                 "checklist",
                 "pub", "wedding", "cinema", "park", "swimming", "soft play", "restaurant",
                 "birthday party", "funeral", "church", "school run",
                 "cornwall", "devon", "wales", "scotland", "england", "yorkshire", "norfolk",
                 "suffolk", "dorset", "sussex", "kent", "cumbria", "lake district", "seaside",
                 "butlins", "haven", "pontins", "caravan", "camping", "campsite", "holiday club",
                 "holiday camp", "day trip", "weekend trip", "in the uk", "staycation",
                 "without the kids", "without children", "without my kids", "no kids",
                 "adults only", "grown ups"),
          guard=_a_journey_not_a_treatment,
          bias=1),

    entry("pet-travel",
          (("dog", "dogs", "cat", "cats", "puppy", "kitten", "pet", "pets", "rabbit",
            "ferret", "hamster", "guinea pig", "budgie", "parrot", "tortoise", "snake"),
           ("abroad", "france", "spain", "italy", "ireland", "europe", "travel",
            "travelling", "traveling", "travel with", "fly", "flying", "plane", "ferry",
            "tunnel", "pet passport", "rabies", "vaccination", "microchip",
            "out of the country", "another country")),
          ("For most of Europe the order is fixed: microchip first, then a rabies vaccination at "
           "least 21 days before you travel, then the paperwork - an EU pet passport or an animal "
           "health certificate from your own vet - and a tapeworm treatment for a dog on the way "
           "back from some countries. Check both countries' own rules, and the ferry or airline's, "
           "because each has its own kennel or cabin booking. Start six weeks out: the 21 days "
           "catches people, and nothing can be backdated."),
          avoid=("puppy food", "dog food", "cat food", "my dog is sick", "my cat is sick",
                 "dog training", "dog bark", "cat litter", "dog insurance", "vet bill",
                 "dog in the car", "car sick", "dog ate", "cat ate", "flea", "worming",
                 "separation anxiety", "boarding kennel", "put my dog", "put my cat",
                 "fly spray", "insect spray", "bug spray", "mosquito spray", "wasp spray",
                 "air freshener", "aerosol", "the spray"),
          bias=1),
    entry("intercity-cheapest",
          (("cheapest way", "cheapest", "cheaper", "cheap way", "get to", "getting to",
            "travel to", "train or coach", "coach or train", "drive or train", "how do i get from",
            "which is better", "which is cheaper", "which one is better", "whats better",
            "what's better"),
           ("from", "train", "trains", "coach", "coaches", "bus", "buses", "plane", "flight",
            "flying", "driving", "london", "manchester", "edinburgh", "glasgow", "birmingham",
            "leeds", "bristol", "cardiff", "newcastle", "liverpool", "paris", "amsterdam",
            "berlin", "rome", "madrid", "barcelona", "dublin", "city", "town")),
          ("The coach is nearly always the cheapest and the train the fastest, and the price gap "
           "is all in how early you book: a coach booked a fortnight ahead is often a fiver, while "
           "a walk-up train fare on the day can be ten times that. Book a fixed-time train twelve "
           "weeks out for the cheap tiers, compare one change against a through train, and count "
           "the cost of getting to and from the stations before you decide."),
          ask=("cheapest", "cheaper", "cheap way", "which is cheaper", "which is better",
               "compare", "best way", "worth it", "train or coach", "coach or train",
               "drive or train", "or train", "or coach"),
          guard=_a_comparison_needs_two_ways,
          avoid=("airport", "car park", "parking", "my car", "driving licence",
                 "how do i get to sleep", "how do i get to work", "promotion", "get to know"),
          bias=1),

    entry("route-between",
          (("how do i get", "how to get", "best way", "get from", "getting from", "travel from",
            "how do i travel", "how to travel", "train or", "ferry or", "bus or", "drive or",
            "how far", "how long does it take to get"),
           tuple(sorted({name for pair in ROUTE_BETWEEN for name in pair}))),
          _route_between,
          avoid=("airport", "flight", "flights", "fly into", "hotel", "hostel", "day trip",
                 "day trips", "worth visiting", "best time", "where to stay", "get around",
                 "getting around", "car hire", "rent a car", "hire a car"),
          bias=2),
    entry("get-to-place",
          (("how do i get to", "how do i get", "how to get to", "how do i reach", "getting to",
            "how do you get to", "best way to get to", "how do i travel to"),
           tuple(sorted(GET_TO))),
          _get_to,
          avoid=("airport", "hotel", "hostel", "day trip", "worth visiting", "best time",
                 "where to stay", "get around", "getting around"),
          bias=1),
    entry("site-worth-visiting",
          (SITE_WORDS,
           ("worth visiting", "worth it", "worth seeing", "should i visit", "should we visit",
            "is it worth", "how long", "how much time", "do i need a ticket", "book",
            "booking", "tickets", "ticket", "visit", "see",
            "worth", "enough", "days", "whole day", "long", "take")),
          _site_note,
          avoid=tuple(sorted(CITIES)) + ("flight", "hotel", "airport", "restaurant", "get from"),
          bias=1),
    entry("city-safe-in-the-day",
          (("safe", "unsafe", "dangerous", "risky", "danger", "crime", "dodgy",
            "is it safe", "is it dangerous", "is it risky", "safe there", "safe enough",
            "safe to walk", "much crime"),
           tuple(CITIES) + ("there", "the streets", "the area", "the city", "the centre",
                            "the center", "tourist", "tourists", "worth visiting", "trip",
                            "holiday")),
          _a_place_it_might_not_be_safe,
          avoid=("tap water", "the water", "water", "ice", "salad", "food", "eat", "tap",
                 "sun", "sunburn", "swim", "jellyfish", "pregnant", "vaccine", "malaria",
                 "jab", "mosquito", "insurance", "at night", "after dark", "night", "evening",
                 "walking back", "walk back", "on my own", "by myself", "alone",
                 "walk around", "walking around", "walk about", "walking about", "get around",
                 "getting around", "walk home", "walking home",
                 "travel to", "travel advice", "foreign office"),
          bias=1),
    entry("day-trip-place",
          (tuple(sorted(DAY_TRIP_PLACES)),
           ("worth it", "worth visiting", "worth seeing", "worth going", "is it worth",
            "should i visit", "should we visit", "what is there", "what's there",
            "how do i get", "how do we get", "how do you get", "how to get", "how far",
            "day trip", "day out")),
          _day_trip_place,
          avoid=tuple(sorted(CITIES)) + ("flight", "hotel", "hostel", "airport", "restaurant",
                                         "get from", "where to stay", "best time"),
          bias=1),
    entry("day-trip-way",
          (("how do i get there", "how do we get there", "how do you get there",
            "how do we get to it", "how do i get to it", "how far is it", "how far is that",
            "how long does it take to get there"),
           ("there", "it", "that")),
          _day_trip_place,
          avoid=tuple(sorted(CITIES)) + ("flight", "hotel", "airport"),
          bias=1),
    entry("city-night-safety",
          (("safe", "unsafe", "dangerous", "risky", "ok to walk", "fine to walk"),
           ("at night", "after dark", "walk around", "walking around", "walk back",
            "walking back", "on my own", "by myself", "alone", "night", "evening")),
          ("Use the habits that work in any city after dark: stay on the busy, lit streets, take a "
           "licensed taxi or the metro rather than a shortcut, keep the phone out of sight and the "
           "bag in front of you, and ask the hotel desk which two or three streets to avoid - they "
           "know this week's answer better than any guide. Carry a card with the hotel address."),
          avoid=("tap water", "drink the water", "water", "ice", "salad", "food", "eat", "street "
                 "food", "tap", "sun", "sunburn", "swim", "jellyfish", "pregnant", "vaccine",
                 "malaria", "jab", "mosquito", "insurance", "at night in", "hotel room",
                 "walk the dog", "walk my dog", "neighbourhood", "which area", "where should i "
                 "stay",
                 "drive", "driving", "driver", "car", "cars", "van", "motor", "motorway",
                 "road", "roads", "lane", "lanes", "parking", "headlights", "towing",
                 "trailer"),
          bias=1),
    entry("child-bus-travel",
          (("child", "children", "kids", "kid", "my son", "my daughter", "school child",
            "school children", "under 5", "under five", "under 5s", "under fives",
            "under-fives", "5 year old", "4 year old",
            "school bus", "school buses", "school travel", "school transport", "school run",
            "family", "families",
            "get to school", "gets to school", "getting to school", "get to school and back",
            "to school and back", "travel to school", "journey to school",
            "bus to school", "coach to school"),
           ("bus", "buses", "coach", "coaches", "tram", "trams", "ferry", "ferries",
            "fare", "fares", "child fare", "ticket", "tickets", "season ticket", "bus pass",
            "school bus", "school travel", "school transport", "free travel", "travel free",
            "travels free", "travel for free", "ride free", "rides free", "rides for free",
            "goes free", "go free", "pay on the bus", "pay on buses", "on the bus",
            "on the coach",
            "get to school", "gets to school", "getting to school", "to school and back",
            "travel to school", "journey to school", "get the bus to school",
            "catch the bus to school", "bus to school", "coach to school")),
          "Under-fives usually travel free on local buses with a paying adult, and 5 to 15 pay a "
          "child fare, often about half: the operator's own page gives the age and the price for "
          "your area. Free travel to school is a council decision and it turns on distance - "
          "usually over 2 miles for a child under 8 and over 3 miles for an 8 to 16 year old going "
          "to the nearest suitable school, or closer if the route is unsafe to walk. Ask the "
          "council's school travel team; a 16 to 18 year old in full-time education usually needs "
          "a council or operator discount card instead.",
          avoid=("pensioner", "pensioners", "over 60", "over 65", "older person", "retired",
                 "freedom pass", "concessionary", "disabled", "train", "trains", "railcard",
                 "flight", "flights", "plane", "airport", "car seat", "hotel", "abroad",
                 "holiday abroad", "travel insurance", "school place", "school admission",
                 "school admissions",
                 "bullied", "bullying", "being bullied", "bullies", "picked on", "picks on",
                 "mean to", "horrible to", "unkind to", "nasty to",
                 "passed out", "passing out", "pass out", "faint", "faints", "fainted",
                 "fainting", "collapsed", "collapse", "collapses", "passed away",
                 "unwell", "poorly", "feeling ill", "feels ill", "felt ill", "being sick",
                 "was sick", "got sick", "threw up", "vomited", "diarrhoea", "diarrhea",
                 "temperature", "fever", "hospital", "ambulance", "111", "999", "a&e",
                 "seizure", "convulsion", "allergic reaction",
                 "not get on", "not get in", "not board", "not go", "crowded",
                 "wont get on", "won't get on", "wont get in", "won't get in", "wont go",
                 "won't go", "wont board", "won't board", "refuses to go", "refuses to get on",
                 "refusing to go", "refusing to get on", "refused to go", "refused to get on",
                 "scared of the bus", "scared of the school bus", "afraid of the bus",
                 "scared of school", "afraid of school", "school refusal", "anxious about school",
                 "anxious about the bus", "hates the bus", "hates school", "wont leave the house",
                 "won't leave the house",
                 "phone", "phones", "mobile", "mobiles", "iphone", "smartphone", "tablet",
                 "ipad", "wallet", "purse", "handbag", "backpack", "school bag", "rucksack",
                 )),
    entry("travel-cheaply",
          (("travel cheaply", "travel cheap", "travelling cheap", "traveling cheap",
            "travel on a budget", "travel around europe", "travelling around europe",
            "traveling around europe", "touring europe", "tour europe", "see europe",
            "get around europe", "europe on a budget", "cheap travel", "cheap holiday",
            "cheap trip", "backpacking", "backpack", "interrail", "eurail",
            "cheap places to go", "budget trip"),
           ("cheap", "cheaply", "cheapest", "budget", "save", "afford", "europe", "european",
            "hostel", "hostels", "train", "trains", "coach", "how", "ways", "tips")),
          "Take the train or the coach between cities instead of flying, book a month or two "
          "ahead, and stay in hostels or travel out of season: May, June and late September cost "
          "about half what August does. Eat where people work - market stalls, bakeries, a "
          "supermarket lunch - and choose one small town over a second capital. Cheapest weeks "
          "are midweek city breaks, Tuesday to Thursday.",
          bias=1,
          avoid=("flight", "flights", "airfare", "meal", "meals", "dinner", "cook", "cooking",
                 "recipe", "food shop", "week of", "meal plan", "hotel in", "which hotel",
                 "hiking", "hike", "hill", "walking boots", "rucksack", "pack a", "packing a",
                 "pack my", "how do i pack", "suitcase", "carry on")),
]
ENTRIES.append(entry(
    "pick-a-hotel",
    (("hotel", "hotels", "guesthouse", "guest house", "b&b", "bed and breakfast", "hostel",
      "place to stay", "somewhere to stay"),
     ("decent", "good", "choose", "choosing", "pick", "picking", "find", "finding", "best",
      "book", "booking", "which", "how do i", "safe", "recommend",
      "where should i", "avoid", "trust", "reviews", "worth it", "village", "city",
      "town", "night", "nights", "weekend", "holiday", "trip")),
    "Book from the hotel's own site once you know the name, then check three things: the last "
    "two months of reviews only (owners change, and old praise is stale), the map for the walk "
    "to the station or the old town, and the small print for a city tax and the cancellation "
    "date. A room away from the lift or the road is worth asking for in the booking notes, "
    "and ring the desk for anything that matters - they answer faster than the site.",
    avoid=("when should i book", "when do i book", "when to book", "how far in advance",
           "how far ahead", "how early", "weeks before", "months before", "book for a wedding",
           "block of rooms", "wedding guests",
           "complain", "complaint", "refund", "wifi", "wi-fi", "address", "cancel", "cancel my",
           "noise", "noisy", "dirty", "bed bugs", "reviews said", "left something",
           "cheapest flight", "flights", "airport", "dog", "parking", "pet",
           "cheap", "cheaper", "cheapest", "price", "prices", "cost", "budget", "deal", "deals",
           "discount", "how much",
           "job", "jobs", "work at", "work in", "working in", "staff", "vacancy", "vacancies",
           "hiring", "apply", "application", "interview", "career", "cv", "rota", "shift"),
    ask=("decent", "good", "choose", "choosing", "pick", "picking", "find", "finding", "best",
         "book", "booking", "which", "how do i", "where should i", "recommend", "trust",
         "worth it", "avoid", "safe")))


def _read_timetable(memory, understood):
    return pick([
        "Read a timetable by column, not by line: each column is one journey, so run your finger "
        "down it to see the time at your stop and the one after. Times after noon are often in "
        "24-hour form (17:40 is 5:40 in the evening), the small letters beside a time are "
        "explained in the key at the bottom - S for schooldays, NS for not Sundays - and Sunday "
        "and bank holiday services have their own table with the last bus much earlier. The "
        "operator's app or the display at the stop is the only thing that knows about today's "
        "delays.",
        "Find your stop's row first and read across it: the minutes are printed under the hour, "
        "so a column is one bus and a row is one stop. The letters next to a time are notes - "
        "schooldays only, not Saturdays, bank holidays - and there is usually a separate table "
        "for Sunday. Be at the stop five minutes early, because a bus that comes every half hour "
        "is the one you cannot afford to miss, and check live times on the operator's app before "
        "you set off: the printed table is the plan, not what is happening.",
    ], memory)


ENTRIES.append(entry(
    "read-a-timetable",
    (("timetable", "timetables", "time table", "bus times", "train times", "bus schedule",
      "train schedule", "departure board", "departures", "last bus", "next bus", "next train",
      "last train", "24 hour clock", "24-hour clock"),
     ("read", "reading", "how", "when", "what time", "next", "last", "which", "catch",
      "work out", "understand", "sunday", "night", "evening", "morning", "app")),
    _read_timetable,
    ask=("read", "reading", "how do i", "how do you", "how to", "understand", "work out",
         "explain", "what does", "mean"),
    avoid=("school", "exam", "exams", "class", "classes", "study", "revision",
           "book", "novel", "holiday read", "gym", "workout", "medication", "dose", "feed"),
    bias=1))


ENTRIES.append(entry(
    "left-luggage",
    (("luggage", "bags", "baggage", "bag", "suitcase", "suitcases", "rucksack", "holdall",
      "backpack", "cases"),
     ("hotel", "hotels", "hostel", "hostels", "guest house", "guesthouse", "reception",
      "front desk", "apartment", "apartments", "airbnb", "villa", "check out", "checkout",
      "check-out", "check in", "check-in", "left luggage", "luggage room", "concierge",
      "holiday let", "rental", "reception desk")),
    "Most hotels hold your bags free at reception, both before check-in and after you check out: "
    "ask them to tag them with your name and ask what time the desk closes, so you are back "
    "before then. Keep the passport, the money and anything you would hate to lose in your day "
    "bag rather than the big case, and if the hotel will not help, a station left-luggage desk or "
    "a locker is a few pounds for the day.",
    avoid=("allowance", "how much", "how many", "weight", "kg", "cabin", "hand luggage",
           "carry on", "carry-on", "lost", "lose", "stolen", "missing", "damaged", "damage",
           "unattended", "carousel", "platform", "taxi", "boot of", "left behind", "forgot",
           "pick up", "collect it from the airport"),
    bias=2))

ENTRIES.append(entry(
    "cabin-bag",
    (("suitcase", "suitcases", "cabin bag", "hand luggage", "carry on", "carry-on", "rucksack",
      "backpack", "holdall", "bag", "bags", "luggage"),
     ("how big", "how large", "how much can", "what size", "size", "dimensions", "cm",
      "centimetres", "centimeters", "too big", "too large", "fit", "fits", "fitting", "measure",
      "under the seat", "on the plane", "on board", "in the cabin", "onto the plane")),
    "The usual cabin limit is 55 x 40 x 20 cm including the wheels and the handle, plus one small "
    "bag under the seat at about 40 x 30 x 15 cm, and 7 to 10 kg in total - so yes, a rucksack or "
    "a small case comes on with you, as long as it fits the sizer at the gate. A soft bag squeezes "
    "into it and a hard case does not, so leave a centimetre of slack and weigh it at home.",
    avoid=("bin", "bin bag", "rubbish", "vacuum", "hoover", "tea bag", "dog", "sleeping bag",
           "freezer", "freezer bag", "ziplock", "zip lock", "food bag", "sugar", "flour",
           "compost", "peat", "cement", "sand", "soil", "potatoes", "charcoal", "ice", "food",
           "sandwich", "sandwiches", "drink", "drinks", "liquid", "liquids", "razor", "lighter",
           "medicine", "medication", "knife", "scissors", "battery", "batteries", "power bank",
           "phone", "laptop", "data", "baby", "pram", "pushchair", "damaged", "lost", "stolen",
           "missing", "delayed", "airport", "hotel", "flight"),
    bias=1))

ENTRIES.append(entry(
    "extra-bag-cost",
    (("extra bag", "extra luggage", "extra suitcase", "checked bag", "checked luggage",
      "bag to check", "add a bag", "add luggage", "second bag", "hold bag", "hold luggage",
      "put a case in the hold"),
     ("cost", "costs", "price", "prices", "how much", "pay", "fee", "fees", "charge", "charges",
      "expensive", "cheaper", "cheapest", "worth it")),
    "Book the bag with the ticket rather than at the airport: a checked bag is usually about £15 "
    "to £40 each way online and £40 to £65 at the desk, and on a short trip a 10 kg cabin bag with "
    "priority is often the cheaper way to take a case. Weigh it at home on the bathroom scales - a "
    "few kilos over is charged at the airport rate however you booked.",
    avoid=("allowance", "how big", "size", "dimensions", "kg can", "how many kg", "weight limit",
           "lost", "stolen", "missing", "damaged", "buy", "buying", "recommend", "which bag",
           "which suitcase", "hotel", "food", "pram", "pushchair", "carrier bag", "plastic bag",
           "5p", "5 pence", "shop", "supermarket", "charge for bags"),
    bias=2))

ENTRIES.append(entry(
    "pickpockets-abroad",
    (("pickpocket", "pickpockets", "pickpocketing", "pickpockets in", "thieves", "thief",
      "muggers",
      "wallet", "wallets", "purse", "money belt"),
     ("avoid", "avoiding", "stop", "prevent", "safe", "safety", "keep my", "protect", "careful",
      "watch out", "beware", "tips", "how do i", "what should i", "scared", "worried",
      "abroad", "holiday", "trip", "city", "cities", "rome", "paris", "barcelona", "madrid",
      "lisbon", "prague", "amsterdam", "naples", "athens", "istanbul", "berlin", "dublin",
      "london", "new york", "venice", "florence", "budapest", "brussels", "vienna")),
    ("Keep the phone out of a back pocket and the bag across your body with the zip in front, "
     "and split the cash into two places so one theft is not the whole trip. Never leave a phone "
     "on a cafe table or a bag on the back of a chair, carry a copy of the passport rather than "
     "the passport itself, and if someone bumps into you in a crowd, check your pocket at once - "
     "the bump is the trick."),
    bias=1,
    avoid=("wallet was", "wallet stolen", "wallet gone", "purse was", "phone was",
           "was stolen", "got stolen", "snatched", "bag was", "robbed", "mugged",
           "passport", "insurance", "report")))

ENTRIES.append(entry(
    "away-with-someone-who-cannot-walk-far",
    (("cant walk far", "can't walk far", "cannot walk far", "cant walk", "can't walk",
      "cannot walk", "struggles with walking", "struggles to walk", "struggle walking",
      "not good on their feet", "cant walk much", "wheelchair", "wheelchairs", "rollator",
      "walking stick", "walking frame", "mobility scooter", "mobility", "disabled",
      "bad knees", "hip replacement", "knee replacement", "slow walker", "gets tired walking",
      "special assistance", "airport assistance", "help at the airport", "passenger assist",
      "help getting on the train", "help on the train", "help onto the train",
      "book assistance", "assistance booked", "airport special assistance"),
     ("holiday", "holidays", "away", "trip", "travel", "abroad", "city break", "day out",
      "get around", "getting around", "get about", "see", "visit", "day", "hotel",
      "flight", "flights", "train", "coach", "bus", "plane", "planes", "airport",
      "airports", "fly", "flying", "museum", "gallery", "how")),
    ("Plan for half the walking and twice the sitting: one or two things a day with a cafe or a "
     "bench between them, and a taxi or the hop-on bus for the long hops rather than marching "
     "between sights. Check step-free access before you book, because most museums, galleries and "
     "cathedrals publish it, ask the hotel for a room near the lift, and book help ahead on trains "
     "and at the airport - it is free, UK rail's Passenger Assist takes bookings up to 24 hours "
     "ahead and airports usually want 48. A folding wheelchair or rollator can be hired locally "
     "for a week for less than a day's car hire, a lot of places let a carer in free, and a "
     "folding stool in a bag turns an unplanned stop into a rest. Skip the walking tour and the "
     "climb, and book the view from a roof terrace or a cafe instead."),
    avoid=("flight socks", "compression", "dvt", "blood clot", "swollen ankles", "insurance",
           "visa", "passport", "jet lag", "pram", "pushchair", "dog", "puppy", "how many steps",
           "step target", "10,000", "10000", "knees hurt", "hip hurts", "doctor"),
    bias=2))


FAMILY_VERDICT = {
    "amsterdam": (
        "Amsterdam is easy with children: everything is close, the trams take a pram, and "
        "NEMO and the science museum are built for them. The bikes are the thing to watch - "
        "keep on the pavement side and hold hands at the crossings."),
    "athens": (
        "Athens is fine with older children and hard work with a toddler: the Acropolis is a "
        "stony climb with little shade and the pavements are narrow. Go at opening time, give "
        "the afternoon to the National Garden, and take taxis rather than walk the long "
        "blocks."),
    "bangkok": (
        "Bangkok is hot and loud and better with children than people expect: the river boats "
        "are the day out, the malls have play areas and aquariums, and taxis are cheap. "
        "Traffic is the enemy, so plan around the skytrain and the boats."),
    "barcelona": (
        "Barcelona is one of the easiest cities in Europe with children: the beach is on the "
        "metro, the Gothic Quarter is flat, and the Boqueria is a free hour of noise and "
        "fruit. The Sagrada Familia sells out, so book weeks ahead."),
    "bath": (
        "Bath is a good day out rather than a week: the Roman Baths run a family trail with "
        "an audio guide for children, and the baths, the abbey and the river are all within a "
        "mile. It is fine with a pram in the centre and steep on the hills out of it."),
    "berlin": (
        "Berlin works well with children and costs less than most of western Europe: the zoo "
        "is one of the best anywhere, the Technikmuseum has trains and planes to climb on, "
        "and the parks have playgrounds. It is spread out, so buy a day travel ticket."),
    "boston": (
        "Boston is a good family city: the Freedom Trail is a walk with stories in it, the "
        "harbour and the science museum fill a day, and the T takes a stroller. It is compact "
        "and walkable, which is the whole point of it with children."),
    "brussels": (
        "Brussels is underrated with children: the Grand Place, the comic strip museum and "
        "the Atomium are close, and the waffles do a lot of the work. Two days is enough, and "
        "it is an easy stop on a longer trip."),
    "budapest": (
        "Budapest is good with children who like water: the thermal baths take families, and "
        "Margaret Island is a park with pools, bikes and a musical fountain. The trams and "
        "metro are cheap and frequent."),
    "buenos aires": (
        "Buenos Aires is a big, late city with children: the parks and the zoo in Palermo are "
        "the easy days, and the buses and taxis are cheap. Dinner starts at nine or later, so "
        "plan an afternoon snack that counts as their meal."),
    "cape town": (
        "Cape Town is excellent with children if you have a car: the beaches, the cable car, "
        "the penguins at Boulders and the aquarium fill a week. The townships and the "
        "mountain roads are not a wander, so plan the drives in daylight."),
    "chicago": (
        "Chicago is a very good family city: the museums on the lakefront, the beach in "
        "summer, and the trains are easy with a stroller. The winter wind off the lake is the "
        "reason to go between May and September."),
    "copenhagen": (
        "Copenhagen is about as good as it gets for small children: Tivoli, the Little "
        "Mermaid on a flat seafront walk, and the harbour buses for the price of a metro "
        "ticket. It is flat, and prams go everywhere."),
    "dubai": (
        "Dubai is easy for families and hot for most of the year: the malls have indoor play, "
        "aquariums and a ski slope, so it works in August when nothing outdoors does. "
        "Anything outdoors belongs to the morning, and the good things need booking."),
    "dublin": (
        "Dublin is a two-day city with children: the Natural History Museum, the Phoenix Park "
        "and the zoo sit close together and cost little. The Guinness tour is not one for "
        "them, so split up or skip it."),
    "dubrovnik": (
        "Dubrovnik is beautiful and hard with a pram: the old town is all steps and the walls "
        "are a long, hot walk with no shade. Go at opening time or after five, and take the "
        "cable car for the view instead of walking the walls."),
    "edinburgh": (
        "Edinburgh is a good family city if you pace the hills: the castle is a climb but "
        "there is a lift up from the esplanade, the museum is free and built for children, "
        "and the Royal Mile is short. In August the festival makes it crowded and expensive."),
    "florence": (
        "Florence with children is one big sight a day and a lot of ice cream: the Duomo "
        "climb suits older ones and the Boboli gardens have space to run. The Uffizi is a "
        "hard sell under ten, so take them to the Palazzo Vecchio instead."),
    "granada": (
        "Granada is worth it with children for the Alhambra alone - book months ahead and go "
        "at opening time, because there is little shade. The city is hilly and the tapas come "
        "free with a drink, which makes dinner easy and early."),
    "hanoi": (
        "Hanoi is exciting and full-on with children: the scooters make crossing the road an "
        "event, and the old quarter is loud. The water puppet theatre and the parks are the "
        "easy wins, and a hotel with a pool earns its money."),
    "havana": (
        "Havana is a city of old cars, music and heat, and children tend to love the first "
        "two: the Malecon, the squares and the museums are cheap. Take the heat seriously and "
        "carry water, and expect the food to be plainer than the city suggests."),
    "helsinki": (
        "Helsinki is calm and easy with children: the ferries to the islands, the zoo on its "
        "own island, and playgrounds everywhere in a small, walkable centre. It is expensive, "
        "and the winter dark is the reason to go between May and September."),
    "istanbul": (
        "Istanbul is good with children who can walk: the ferries are the best value day out "
        "in the city, and the tram between Sultanahmet and the bazaar takes a pram. The "
        "bazaars are crowded and pushy, so go early in the day."),
    "krakow": (
        "Krakow is a good value family city: the main square is flat and car-free, the dragon "
        "under the castle breathes fire every few minutes, and the salt mine is a half day "
        "out. The camps nearby are not for young children."),
    "kyoto": (
        "Kyoto is quiet and beautiful and hard work with small children: the temples ask for "
        "quiet and the buses are packed. The monkey park and the bamboo grove suit them, and "
        "a stroller is more trouble than it is worth on temple steps."),
    "lisbon": (
        "Lisbon is good with children if you take the trams and the funicular rather than "
        "walk the hills: the castle, the aquarium and Belem fill two easy days. The pavements "
        "are slippery when wet, and the hills are real."),
    "ljubljana": (
        "Ljubljana is a small, gentle city with children: the centre is car-free, the river "
        "has cafes on it, and the castle funicular saves the climb. It is a good two-day stop "
        "on the way to the lakes or the coast."),
    "london": (
        "London is one of the best cities in the world with children: free museums, the "
        "parks, and a ride on the top deck of a bus is a day out on its own. The tube is not "
        "step-free everywhere, so check the station before planning a pram route."),
    "los angeles": (
        "Los Angeles is a driving city, so plan days out rather than wanders: the beach, the "
        "studios and the theme parks are each a half day with a car. Without one it is hard "
        "work with children."),
    "madrid": (
        "Madrid is good with children and cheap to eat: the Retiro has a lake with rowing "
        "boats and a playground, and the museums are free in the evenings. Dinner starts "
        "late, so plan a proper late-afternoon snack."),
    "marrakech": (
        "Marrakech is a lot with small children: the souks are hot, crowded and full of "
        "scooters, and the food is not always what they will eat. The gardens, the "
        "horse-drawn calèche rides and a pool at the hotel make it work."),
    "mexico city": (
        "Mexico City is huge and rewarding with children: the parks, the anthropology museum "
        "and the boats at Xochimilco fill days, and the metro is cheap. It is high up, so "
        "take the first day slowly, and eat where it is busy."),
    "milan": (
        "Milan is a short family stop rather than a holiday: the Duomo, the castle park and "
        "the science museum are close, and the trams take a pram. Two days, then on to the "
        "lakes."),
    "munich": (
        "Munich is easy and safe with children: the English Garden, the Deutsches Museum and "
        "the beer gardens, where children are welcome and there is usually a playground. The "
        "trains out to the lakes and the castles are part of the trip."),
    "naples": (
        "Naples is loud and fast and children tend to love it: the pizza is cheap, the "
        "seafront is a flat walk, and Pompeii and Herculaneum are a short train away. Traffic "
        "is the thing to watch and the pavements are narrow."),
    "new york": (
        "New York is great with children who can keep going: the parks, the Natural History "
        "Museum and the Staten Island ferry are cheap days out. Most subway stations have no "
        "lift, so plan the stroller around buses and taxis."),
    "oslo": (
        "Oslo is small, safe and expensive: the ferries, the opera house roof you can walk "
        "on, and the sculpture park are the easy days out, and the trams take a pram. A week "
        "of self-catering takes the edge off the prices."),
    "paris": (
        "Paris is good for families if you pick one thing a day: the Luxembourg gardens have "
        "boats and a playground, and the big museums are free for under-18s in the EU. Lunch "
        "is the easy meal out - restaurants are friendlier at midday than at eight."),
    "porto": (
        "Porto is a good short family break: the riverfront is flat, the boats and the old "
        "tram are the day out, and the port cellars are a walk across the bridge. The climb "
        "back up from the river is steep."),
    "prague": (
        "Prague is good value with children: the castle, the river and the old town are close "
        "together, the trams are cheap, and the toy museum is a good wet-afternoon stop. The "
        "cobbles are hard on a pram."),
    "reykjavik": (
        "Reykjavik is a good family base if you drive: the swimming pools are the thing, "
        "heated and outdoor and everywhere, and the whales, the glaciers and the golden "
        "circle are day trips from it. It is expensive, so an apartment helps."),
    "rio de janeiro": (
        "Rio is wonderful with children in the right places: the beaches, the cable car up "
        "Sugar Loaf and the botanical garden are the easy days. Take advice on which areas to "
        "walk and which to take a taxi through, and swim where the locals do."),
    "rome": (
        "Rome works with children if you keep the days short: the Colosseum and the Forum are "
        "one morning, the Pantheon and a gelato another, and the fountains give you free "
        "water. The cobbles are hard on a pram and the summer heat is real, so spring or "
        "autumn."),
    "san francisco": (
        "San Francisco is a good family city: the cable cars, the sea lions at Pier 39 and "
        "the science museum fill three days, and it is all close. The hills are steep and the "
        "summer fog makes it colder than people expect."),
    "san sebastian": (
        "San Sebastian is a seaside city built for families: the beach curls round the bay in "
        "the middle of town, the promenade is flat, and the old town tapas bars take children "
        "at the early end of the evening. It is a city for eating and swimming rather than "
        "for sights."),
    "santorini": (
        "Santorini is a honeymoon island more than a family one: the villages are steps and "
        "cliff paths with no shade, and the beaches are black stones. With children a resort "
        "with a pool on a flatter island works far better."),
    "seville": (
        "Seville is good with children from March to May: the Alcazar has gardens to run in, "
        "the Plaza de Espana has rowing boats, and the tapas are cheap and served early "
        "enough for them. July and August are too hot to sightsee with children."),
    "singapore": (
        "Singapore is one of the easiest cities in Asia with children: it is safe, the metro "
        "is step-free and air-conditioned, and the zoo, the aquarium and the gardens fill "
        "days. It is expensive, and the heat puts the outdoor plans in the morning."),
    "stockholm": (
        "Stockholm is lovely with children in summer: the ferries between the islands, the "
        "Vasa ship and the open-air museum at Skansen, and prams go everywhere. Winter is "
        "dark and cold, so go between May and September."),
    "sydney": (
        "Sydney is a great family city: the beaches, the ferry to Manly, the zoo on the "
        "harbour and the parks, most of it free or cheap. It is spread out, so plan each day "
        "around one beach or one ferry."),
    "tallinn": (
        "Tallinn is a good short family break: the old town is small and walkable, the towers "
        "and walls are climbable, and the ferries to Helsinki take two hours. Two days is "
        "plenty, and it is cheap by western European standards."),
    "tokyo": (
        "Tokyo is easier with children than people expect: the trains are safe and punctual, "
        "lifts and toilets are everywhere, and there is a small park on every block. The "
        "trains are packed at rush hour, so plan around eight in the morning and six at "
        "night."),
    "toronto": (
        "Toronto is a good, manageable family city: the islands by ferry, the aquarium, the "
        "science centre and the hockey museum fill days, and the subway takes a stroller. It "
        "is clean and English-speaking, which makes the first day easy."),
    "valencia": (
        "Valencia is a good family city that most people skip: the City of Arts and Sciences "
        "has an aquarium and a science museum built for children, and the old town is flat. "
        "The beach is a tram ride from the centre."),
    "venice": (
        "Venice with children is a day of boats and bridges: the water bus is the day out, St "
        "Mark's square has pigeons and space, and there are no cars to worry about. A pram is "
        "the problem - bridges with steps come every hundred metres, so a carrier is better."),
    "vienna": (
        "Vienna is quietly excellent with children: the zoo at Schonbrunn, the Prater's old "
        "ferris wheel and a playground in every park, with a metro that takes a pram "
        "everywhere. The cafes take children, and lunch is cheap at midday."),
    "zurich": (
        "Zurich is clean, safe and expensive with children: the lake boats, the zoo and the "
        "outdoor swimming baths are the days out, and the trams take a pram. A Swiss pass and "
        "a supermarket lunch keep the cost down."),
}

FAMILY_ASK = ("families", "family", "kids", "children", "child", "toddler", "toddlers", "baby",
              "babies", "teenagers", "teens", "young children", "small children")


_GUIDE_ASK = re.compile(
    r"\b(?:what|where)\s+(?:should|could|can|shall|do|to)\s+(?:we|i|you)?\s*"
    r"(?:do|see|go|visit|eat)\b|\bthings\s+to\s+do\b|\bwhat(?:'s|\s+is)\s+there\s+to\s+do\b"
    r"|\bitinerary\b|\bsights\b|\bwhat\s+to\s+(?:do|see)\b|\bwhere\s+to\s+go\b", re.I)


def _a_verdict_not_a_guide(understood):
    text = " " + " ".join(str((understood or {}).get("text") or "").lower().split()) + " "
    return not _GUIDE_ASK.search(text)


def _the_family_verdict(memory, understood):
    city = _place_in(memory, understood, FAMILY_VERDICT)
    if not city:
        return None
    return FAMILY_VERDICT[city]


ENTRIES.append(entry(
    "a-city-good-for-families",
    (tuple(FAMILY_VERDICT), FAMILY_ASK),
    _the_family_verdict,
    avoid=("hotel", "hotels", "apartment", "apartments", "flight", "flights", "plane", "airport",
           "cheap", "cheapest", "cost", "price", "budget", "insurance", "visa", "passport",
           "school", "schools", "move", "moving", "live", "living", "relocate", "rent", "job",
           "nursery", "childcare", "vaccine", "vaccines", "pushchair", "pram"),
    guard=_a_verdict_not_a_guide,
    bias=2))
ENTRIES.append(entry(
    "is-it-good-for-families",
    (("good for families", "good for kids", "good for children", "good for a family",
      "family friendly", "family-friendly", "kid friendly", "child friendly", "suitable for kids",
      "suitable for families", "family holiday", "family trip", "family break",
      "holiday with kids", "with kids", "with children"), FAMILY_ASK),
    _the_family_verdict,
    avoid=("hotel", "hotels", "apartment", "apartments", "flight", "flights", "cheap", "cheapest",
           "cost", "price", "budget", "insurance", "visa", "school", "schools", "move", "moving",
           "live", "living", "relocate", "rent", "job", "childcare", "vaccine", "pushchair",
           "pram", "toddler won't", "tantrum", "bedtime", "car seat"),
    guard=_a_verdict_not_a_guide,
    bias=3))
ENTRIES.append(entry(
    "hotel-overbooked-steps",
    (("hotel", "hotels", "guesthouse", "guest house", "b&b", "bed and breakfast", "hostel",
      "hotel room", "hotel rooms", "room booking", "our booking", "my booking"),
     ("overbooked", "over booked", "double booked", "double-booked", "no room", "no rooms",
      "full", "turned away", "walked", "lost my booking", "cant find my booking",
      "can't find my booking", "no record", "not on the list", "gave my room away",
      "gave our room away")),
    "Ring the booking site or the hotel's own number straight away, then ask in this order: a "
    "comparable room nearby at their cost including the taxi, or a full refund for the night plus "
    "what you pay for the replacement. Walking a guest to another hotel is standard practice, so "
    "say the word \"walk\" and ask them to confirm it in writing before you leave the desk.",
    avoid=("choose", "choosing", "which hotel", "best hotel", "where to stay", "cheap",
           "cheaper", "cheapest", "price", "cost", "how much", "dirty", "noise", "noisy",
           "complain", "complaint", "cancel my", "cancellation", "wifi", "wi-fi", "shelf",
           "wardrobe", "pack", "packing", "what to take"),
    ask=("overbooked", "over booked", "double booked", "double-booked", "no room", "no rooms",
         "full", "turned away", "walked", "lost my booking", "no record", "gave my room away",
         "gave our room away"),
    bias=2))

def _comes_across_a_border(understood):
    line = str(understood.get("clean") or understood.get("text") or "").lower()
    return crosses_a_border(line) and not carries_it_out_of_britain(line)


ENTRIES.append(entry(
    "customs-food",
    (("cheese", "ham", "meat", "sausages", "sausage", "bacon", "dairy", "milk", "butter",
      "yoghurt", "sandwich", "sandwiches", "pate", "salami", "chorizo", "food"),
     ("bring back", "bringing back", "take back", "bringing", "into the uk", "into britain",
      "into england", "back home", "home", "customs", "declare", "allowed", "import",
      "from france", "from spain", "from italy", "from portugal", "from germany",
      "from greece", "from ireland", "from the eu", "from europe")),
    "Not meat or dairy: since 2021 you cannot bring ham, sausages, bacon, cheese, milk or butter "
    "into Great Britain from the EU, even for yourself, and a ham sandwich in your bag can be "
    "taken off you. Fish, eggs, fruit, vegetables, bread and cake are fine, and the alcohol "
    "allowance is its own question. If you are not sure, use the red channel and ask.",
    avoid=("cook", "cooking", "recipe", "recipes", "freeze", "frozen", "fridge", "keep fresh",
           "goes off", "allergy", "allergic", "lactose", "vegan", "vegetarian", "calories",
           "how long does", "best before", "use by", "shop", "supermarket", "buy",
           "party", "how much wine", "how many bottles", "hangover", "calories in",
           "wine", "beer", "spirits", "alcohol", "cigarettes", "tobacco", "duty free",
           "to work", "at work", "for work", "office", "lunch", "lunchbox", "picnic",
           "school", "day out", "walk", "hike", "flight meal",
           "restaurant", "restaurants", "cafe", "cafes", "café", "the pub", "pub lunch",
           "cinema", "theatre", "theater", "gig", "concert", "festival", "birthday",
           "barbecue", "bbq", "college", "university", "hospital", "ward", "appointment",
           "hotel room", "my hotel", "the hotel", "in the hotel", "airbnb", "campsite",
           "football", "match", "church", "funeral",
           "into the eu", "into eu", "into europe", "into spain", "into france", "into italy",
           "into germany", "into portugal", "into greece", "into ireland", "into holland",
           "into the netherlands", "into belgium", "into poland", "into the usa", "into america",
           "into canada", "into australia", "into new zealand", "into japan", "into china",
           "into dubai", "into turkey", "into mexico", "into thailand", "into india",
           "to spain", "to france", "to italy", "to germany", "to portugal", "to greece",
           "to ireland", "to holland", "to the eu", "to europe", "to america", "to australia",
           "in spain", "in france", "in italy", "in germany", "in portugal", "in greece",
           "in the eu", "in europe"),
    ask=("bring back", "bringing back", "take back", "bringing", "into the uk", "into britain",
         "back home", "customs", "declare", "allowed", "import"),
    bias=3, guard=_comes_across_a_border))


ENTRIES.append(entry(
    "food-into-the-eu",
    (("meat", "meats", "ham", "sandwich", "sandwiches", "cheese", "milk", "butter", "dairy",
      "yoghurt", "yogurt", "sausages", "sausage", "bacon", "cream", "pate", "salami", "chorizo",
      "food", "foods", "snacks"),
     ("into the eu", "into eu", "to the eu", "into europe", "to europe", "into spain", "to spain",
      "into france", "to france", "into italy", "to italy", "into germany", "to germany",
      "into portugal", "to portugal", "into greece", "to greece", "into holland", "to holland",
      "into the netherlands", "to the netherlands", "into belgium", "to belgium", "into poland",
      "to poland", "into ireland", "to ireland", "into austria", "to austria", "into croatia",
      "to croatia", "into cyprus", "to cyprus", "abroad", "on the ferry", "at the border",
      "through customs", "declare")),
    "No - and a ham sandwich counts. Since Brexit you cannot take any meat, milk, cheese, butter, "
    "yoghurt or cream from Great Britain into the EU, even for yourself, and it is taken off you "
    "at the port with a fine. Eat the sandwich before you board. Fish, eggs, bread, cakes, fruit, "
    "vegetables and sweets are fine, and powdered baby milk, baby food and pet food for a medical "
    "reason are the exceptions. Coming back into the UK you may bring 2kg of meat or dairy per "
    "person, so buy the cheese for the trip home rather than taking it out.",
    avoid=("cook", "cooking", "recipe", "recipes", "freeze", "frozen", "fridge", "keep fresh",
           "goes off", "allergy", "allergic", "lactose", "vegan", "vegetarian", "calories",
           "how long does", "best before", "use by", "shop", "supermarket", "buy",
           "party", "wine", "beer", "spirits", "alcohol", "cigarettes", "tobacco", "duty free",
           "to work", "at work", "for work", "office", "lunch", "lunchbox", "picnic",
           "school", "day out", "walk", "hike", "flight meal", "through security", "security",
           "hand luggage", "cabin bag", "cabin bags", "liquids",
           "restaurant", "restaurants", "cafe", "cafes", "café", "the pub", "pub lunch",
           "cinema", "theatre", "theater", "gig", "concert", "festival", "birthday",
           "barbecue", "bbq", "college", "university", "hospital", "ward", "appointment",
           "hotel room", "my hotel", "the hotel", "in the hotel", "airbnb", "campsite",
           "football", "match", "church", "funeral", "my dog", "my cat", "pets",
           "breastfeeding", "breast feed", "formula", "baby bottle", "sterilise", "sterilize"),
    bias=2))


_EARLY_FLIGHT = ("early flight", "early morning flight", "early flight", "6am", "5am", "4am",
                 "seven am", "6 am", "5 am", "before my flight", "night before", "first thing")
_TO_THE_AIRPORT = (
    "Sort the transfer when you book the flight rather than the day before: check the airport's own "
    "site for the trains, buses and the official taxi rank, then pick the one that gets you there "
    "with slack. Aim to be at the airport two hours before a short-haul flight and three before a "
    "long-haul one, and add the walk from the drop-off to the terminal plus the queue at bag drop. "
    "If someone is driving you, find out the drop-off point and any charge first, because at most big "
    "airports you cannot be dropped at the door.")


def _to_the_airport(understood):
    words = [str(word).lower() for word in (understood.get("words") or ())]
    text = " ".join(words)
    if any(key in words or key in text for key in _EARLY_FLIGHT):
        return _AIRPORT_EARLY_REPLY
    return _TO_THE_AIRPORT


ENTRIES.append(entry(
    "to-the-airport",
    (("airport", "airports", "terminal", "terminals"),
     ("how do i get", "get to", "get there", "to the airport", "travel to the airport",
      "travel to the terminal", "getting to the airport", "for an early flight",
      "early flight", "early morning flight", "night before", "lift to the airport",
      "taxi to the airport")),
    lambda memory, understood: _to_the_airport(understood),
    avoid=("how early", "how long before", "how long", "what time", "when should", "hours before",
           "minutes before", "enough time", "too early", "miss my flight", "make my flight",
           "what gate", "which gate", "parking", "car park", "drop off charge", "pick up",
           "collect someone", "from the airport", "into town", "to the city", "to the centre",
           "airport lounge", "my flight land", "flight delayed", "flight cancelled")))
ENTRIES.append(entry(
    "sleep-at-the-airport",
    (("airport", "airports", "terminal", "terminals", "layover", "stopover"),
     ("sleep", "sleeping", "slept", "overnight", "spend the night", "stay the night",
      "night at the airport", "night in the airport", "sleep at", "sleep in", "kip", "nap",
      "a few hours sleep", "some sleep")),
    lambda memory, understood: _AIRPORT_SLEEP_REPLY,
    avoid=("my son", "my daughter", "my child", "my baby", "my toddler", "bedtime", "night waking",
           "wakes up", "wake up", "insomnia", "can't sleep", "cannot sleep", "cant sleep",
           "jet lag", "on the plane", "on a plane", "in the car", "in a hotel", "at night")))

_PLACE = {
    "london": (51.5, -0.1, "uk"), "manchester": (53.5, -2.2, "uk"),
    "birmingham": (52.5, -1.9, "uk"), "liverpool": (53.4, -3.0, "uk"),
    "leeds": (53.8, -1.5, "uk"), "sheffield": (53.4, -1.5, "uk"),
    "newcastle": (55.0, -1.6, "uk"), "nottingham": (53.0, -1.2, "uk"),
    "bristol": (51.5, -2.6, "uk"), "cardiff": (51.5, -3.2, "uk"),
    "swansea": (51.6, -4.0, "uk"), "edinburgh": (55.9, -3.2, "uk"),
    "glasgow": (55.9, -4.3, "uk"), "aberdeen": (57.1, -2.1, "uk"),
    "inverness": (57.5, -4.2, "uk"), "belfast": (54.6, -5.9, "uk"),
    "derry": (55.0, -7.3, "uk"), "cambridge": (52.2, 0.1, "uk"),
    "oxford": (51.8, -1.3, "uk"), "york": (53.9, -1.1, "uk"),
    "bath": (51.4, -2.4, "uk"), "brighton": (50.8, -0.1, "uk"),
    "southampton": (50.9, -1.4, "uk"), "portsmouth": (50.8, -1.1, "uk"),
    "plymouth": (50.4, -4.1, "uk"), "exeter": (50.7, -3.5, "uk"),
    "norwich": (52.6, 1.3, "uk"), "leicester": (52.6, -1.1, "uk"),
    "coventry": (52.4, -1.5, "uk"), "hull": (53.7, -0.3, "uk"),
    "preston": (53.8, -2.7, "uk"), "blackpool": (53.8, -3.1, "uk"),
    "milton keynes": (52.0, -0.8, "uk"), "reading": (51.5, -1.0, "uk"),
    "luton": (51.9, -0.4, "uk"), "stansted": (51.9, 0.2, "uk"),
    "heathrow": (51.5, -0.5, "uk"), "gatwick": (51.2, -0.2, "uk"),
    "dover": (51.1, 1.3, "uk"), "canterbury": (51.3, 1.1, "uk"),
    "windermere": (54.4, -2.9, "uk"), "keswick": (54.6, -3.1, "uk"),
    "snowdon": (53.1, -4.1, "uk"), "ben nevis": (56.8, -5.0, "uk"),
    "fort william": (56.8, -5.1, "uk"), "st ives": (50.2, -5.5, "uk"),
    "newquay": (50.4, -5.1, "uk"), "dublin": (53.3, -6.3, "ie"),
    "cork": (51.9, -8.5, "ie"), "galway": (53.3, -9.0, "ie"),
    "limerick": (52.7, -8.6, "ie"), "waterford": (52.3, -7.1, "ie"),
    "belfast city": (54.6, -5.9, "ie"), "kerry": (52.2, -9.7, "ie"),
    "sligo": (54.3, -8.5, "ie"), "donegal": (54.7, -8.1, "ie"),
    "paris": (48.9, 2.4, "eu"), "lyon": (45.8, 4.8, "eu"), "marseille": (43.3, 5.4, "eu"),
    "nice": (43.7, 7.3, "eu"), "bordeaux": (44.8, -0.6, "eu"), "toulouse": (43.6, 1.4, "eu"),
    "brussels": (50.8, 4.4, "eu"), "bruges": (51.2, 3.2, "eu"), "ghent": (51.1, 3.7, "eu"),
    "antwerp": (51.2, 4.4, "eu"), "amsterdam": (52.4, 4.9, "eu"),
    "rotterdam": (51.9, 4.5, "eu"), "the hague": (52.1, 4.3, "eu"),
    "eindhoven": (51.4, 5.5, "eu"), "luxembourg": (49.6, 6.1, "eu"),
    "berlin": (52.5, 13.4, "eu"), "munich": (48.1, 11.6, "eu"),
    "hamburg": (53.6, 10.0, "eu"), "frankfurt": (50.1, 8.7, "eu"),
    "cologne": (50.9, 6.9, "eu"), "dusseldorf": (51.2, 6.8, "eu"),
    "stuttgart": (48.8, 9.2, "eu"), "dresden": (51.1, 13.7, "eu"),
    "nuremberg": (49.5, 11.1, "eu"), "heidelberg": (49.4, 8.7, "eu"),
    "madrid": (40.4, -3.7, "eu"), "barcelona": (41.4, 2.2, "eu"),
    "seville": (37.4, -6.0, "eu"), "valencia": (39.5, -0.4, "eu"),
    "malaga": (36.7, -4.4, "eu"), "bilbao": (43.3, -2.9, "eu"),
    "granada": (37.2, -3.6, "eu"), "palma": (39.6, 2.7, "eu"),
    "lisbon": (38.7, -9.1, "eu"), "porto": (41.1, -8.6, "eu"),
    "faro": (37.0, -7.9, "eu"), "rome": (41.9, 12.5, "eu"),
    "milan": (45.5, 9.2, "eu"), "naples": (40.9, 14.3, "eu"),
    "venice": (45.4, 12.3, "eu"), "florence": (43.8, 11.3, "eu"),
    "bologna": (44.5, 11.3, "eu"), "turin": (45.1, 7.7, "eu"),
    "palermo": (38.1, 13.4, "eu"), "vienna": (48.2, 16.4, "eu"),
    "salzburg": (47.8, 13.0, "eu"), "innsbruck": (47.3, 11.4, "eu"),
    "zurich": (47.4, 8.5, "eu"), "geneva": (46.2, 6.1, "eu"),
    "bern": (46.9, 7.4, "eu"), "basel": (47.6, 7.6, "eu"),
    "prague": (50.1, 14.4, "eu"), "budapest": (47.5, 19.0, "eu"),
    "krakow": (50.1, 20.0, "eu"), "warsaw": (52.2, 21.0, "eu"),
    "danzig": (54.4, 18.7, "eu"), "bratislava": (48.1, 17.1, "eu"),
    "ljubljana": (46.1, 14.5, "eu"), "zagreb": (45.8, 16.0, "eu"),
    "dubrovnik": (42.6, 18.1, "eu"), "split": (43.5, 16.4, "eu"),
    "belgrade": (44.8, 20.5, "eu"), "bucharest": (44.4, 26.1, "eu"),
    "sofia": (42.7, 23.3, "eu"), "athens": (38.0, 23.7, "eu"),
    "thessaloniki": (40.6, 23.0, "eu"), "istanbul": (41.0, 29.0, "eu"),
    "copenhagen": (55.7, 12.6, "eu"), "aarhus": (56.2, 10.2, "eu"),
    "oslo": (59.9, 10.8, "eu"), "bergen": (60.4, 5.3, "eu"),
    "stockholm": (59.3, 18.1, "eu"), "gothenburg": (57.7, 12.0, "eu"),
    "helsinki": (60.2, 24.9, "eu"), "reykjavik": (64.1, -21.9, "eu"),
    "tallinn": (59.4, 24.8, "eu"), "riga": (56.9, 24.1, "eu"),
    "vilnius": (54.7, 25.3, "eu"), "kyiv": (50.5, 30.5, "eu"),
    "lviv": (49.8, 24.0, "eu"), "moscow": (55.8, 37.6, "eu"),
    "st petersburg": (59.9, 30.3, "eu"), "malta": (35.9, 14.5, "eu"),
    "valletta": (35.9, 14.5, "eu"), "nicosia": (35.2, 33.4, "eu"),
    "new york": (40.7, -74.0, "us"), "boston": (42.4, -71.1, "us"),
    "washington": (38.9, -77.0, "us"), "philadelphia": (39.95, -75.2, "us"),
    "chicago": (41.9, -87.6, "us"), "detroit": (42.3, -83.0, "us"),
    "cleveland": (41.5, -81.7, "us"), "pittsburgh": (40.4, -80.0, "us"),
    "atlanta": (33.7, -84.4, "us"), "miami": (25.8, -80.2, "us"),
    "orlando": (28.5, -81.4, "us"), "tampa": (28.0, -82.5, "us"),
    "nashville": (36.2, -86.8, "us"), "memphis": (35.1, -90.0, "us"),
    "new orleans": (29.95, -90.1, "us"), "houston": (29.8, -95.4, "us"),
    "dallas": (32.8, -96.8, "us"), "austin": (30.3, -97.7, "us"),
    "san antonio": (29.4, -98.5, "us"), "denver": (39.7, -105.0, "us"),
    "salt lake city": (40.8, -111.9, "us"), "phoenix": (33.4, -112.1, "us"),
    "las vegas": (36.2, -115.1, "us"), "los angeles": (34.1, -118.2, "us"),
    "san diego": (32.7, -117.2, "us"), "san francisco": (37.8, -122.4, "us"),
    "seattle": (47.6, -122.3, "us"), "portland": (45.5, -122.7, "us"),
    "minneapolis": (45.0, -93.3, "us"), "st louis": (38.6, -90.2, "us"),
    "kansas city": (39.1, -94.6, "us"), "indianapolis": (39.8, -86.2, "us"),
    "columbus": (40.0, -83.0, "us"), "baltimore": (39.3, -76.6, "us"),
    "charleston": (32.8, -79.9, "us"), "savannah": (32.1, -81.1, "us"),
    "honolulu": (21.3, -157.9, "us"), "anchorage": (61.2, -149.9, "us"),
    "toronto": (43.7, -79.4, "ca"), "montreal": (45.5, -73.6, "ca"),
    "ottawa": (45.4, -75.7, "ca"), "quebec": (46.8, -71.2, "ca"),
    "vancouver": (49.3, -123.1, "ca"), "calgary": (51.0, -114.1, "ca"),
    "edmonton": (53.5, -113.5, "ca"), "winnipeg": (49.9, -97.1, "ca"),
    "halifax": (44.6, -63.6, "ca"), "banff": (51.2, -115.6, "ca"),
    "mexico city": (19.4, -99.1, "mx"), "cancun": (21.2, -86.8, "mx"),
    "havana": (23.1, -82.4, "other"), "san juan": (18.5, -66.1, "other"),
    "rio de janeiro": (-22.9, -43.2, "other"), "sao paulo": (-23.6, -46.6, "other"),
    "buenos aires": (-34.6, -58.4, "other"), "lima": (-12.0, -77.0, "other"),
    "bogota": (4.7, -74.1, "other"), "santiago": (-33.4, -70.7, "other"),
    "cape town": (-33.9, 18.4, "other"), "johannesburg": (-26.2, 28.0, "other"),
    "durban": (-29.9, 31.0, "other"), "nairobi": (-1.3, 36.8, "other"),
    "lagos": (6.5, 3.4, "other"), "accra": (5.6, -0.2, "other"),
    "casablanca": (33.6, -7.6, "other"), "marrakesh": (31.6, -8.0, "other"),
    "tunis": (36.8, 10.2, "other"), "cairo": (30.0, 31.2, "other"),
    "hurghada": (27.3, 33.8, "other"), "addis ababa": (9.0, 38.7, "other"),
    "zanzibar": (-6.2, 39.2, "other"), "mauritius": (-20.2, 57.5, "other"),
    "dubai": (25.2, 55.3, "other"), "abu dhabi": (24.5, 54.4, "other"),
    "doha": (25.3, 51.5, "other"), "tel aviv": (32.1, 34.8, "other"),
    "jerusalem": (31.8, 35.2, "other"), "ankara": (39.9, 32.9, "other"),
    "tehran": (35.7, 51.4, "other"), "delhi": (28.6, 77.2, "other"),
    "new delhi": (28.6, 77.2, "other"), "mumbai": (19.1, 72.9, "other"),
    "goa": (15.5, 73.8, "other"), "jaipur": (26.9, 75.8, "other"),
    "kolkata": (22.6, 88.4, "other"), "bengaluru": (13.0, 77.6, "other"),
    "kathmandu": (27.7, 85.3, "other"), "colombo": (6.9, 79.9, "other"),
    "bangkok": (13.8, 100.5, "other"), "chiang mai": (18.8, 99.0, "other"),
    "phuket": (7.9, 98.4, "other"), "kuala lumpur": (3.1, 101.7, "other"),
    "singapore": (1.35, 103.8, "other"), "jakarta": (-6.2, 106.8, "other"),
    "bali": (-8.7, 115.2, "other"), "manila": (14.6, 121.0, "other"),
    "hong kong": (22.3, 114.2, "other"), "shanghai": (31.2, 121.5, "other"),
    "beijing": (39.9, 116.4, "other"), "seoul": (37.6, 127.0, "other"),
    "tokyo": (35.7, 139.7, "other"), "osaka": (34.7, 135.5, "other"),
    "kyoto": (35.0, 135.8, "other"), "sapporo": (43.1, 141.4, "other"),
    "taipei": (25.0, 121.5, "other"), "sydney": (-33.9, 151.2, "au"),
    "melbourne": (-37.8, 145.0, "au"), "brisbane": (-27.5, 153.0, "au"),
    "perth": (-31.95, 115.9, "au"), "adelaide": (-34.9, 138.6, "au"),
    "cairns": (-16.9, 145.8, "au"), "hobart": (-42.9, 147.3, "au"),
    "auckland": (-36.8, 174.8, "nz"), "wellington": (-41.3, 174.8, "nz"),
    "christchurch": (-43.5, 172.6, "nz"), "queenstown": (-45.0, 168.7, "nz"),
    "fiji": (-17.7, 178.1, "other"),
}

_FAR_ASKED = ("how far is", "how far are", "how far from", "how far away is",
              "how far away are", "distance from", "distance between", "distance to",
              "the distance", "how long does it take to get", "how long does it take to drive",
              "how long does it take to travel", "how long to drive", "how long is the drive",
              "how long is the journey", "how many miles is", "how many miles from",
              "how many miles between", "how many km is", "how many kilometres is",
              "how far apart")

_ROAD_SPEED = {"gb": 90, "ie": 85, "eu": 90, "na": 95, "au": 95, "nz": 85}

_ROAD_FACTOR, _ROAD_ALLOWANCE = 1.25, 15

_NETWORK_NAME = {"uk": "gb", "ie": "ie", "eu": "eu", "us": "na", "ca": "na", "mx": "na",
                 "au": "au", "nz": "nz"}
_NETWORK_FIX = {"belfast": "ie", "belfast city": "ie", "derry": "ie"}


def _network(place):
    if place in _NETWORK_FIX:
        return _NETWORK_FIX[place]
    code = _PLACE[place][2]
    if code == "other":
        return place
    return _NETWORK_NAME.get(code, code)


def _places_named(said):
    found = []
    for name in sorted(_PLACE, key=len, reverse=True):
        start = 0
        while True:
            at = said.find(name, start)
            if at < 0:
                break
            before = said[at - 1] if at else " "
            after = said[at + len(name):at + len(name) + 1]
            whole = (not before.isalnum()) and (not after.isalnum())
            overlaps = any(lo < at + len(name) and at < hi for lo, hi, _ in found)
            if whole and not overlaps:
                found.append((at, at + len(name), name))
            start = at + 1
    found.sort()
    return [name for _, _, name in found]


def _km(first, second):
    lat1, lon1, _ = _PLACE[first]
    lat2, lon2, _ = _PLACE[second]
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    h = (math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1))
         * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    return 2 * 6371 * math.asin(math.sqrt(h))


def _nearest_five(number):
    return int(round(number / 5.0) * 5)


def _miles(km):
    miles = km * 0.62137
    return _nearest_five(miles) if miles >= 20 else int(round(miles))


def _drive_time(km, group):
    return _duration(km / float(_ROAD_SPEED.get(group, 80)))


def _duration(hours):
    whole = int(hours)
    minutes = int(round((hours - whole) * 60 / 5.0) * 5)
    if minutes == 60:
        whole, minutes = whole + 1, 0
    if whole == 0:
        return "%d minutes" % minutes
    unit = "hour" if whole == 1 else "hours"
    if minutes == 0:
        return "%d %s" % (whole, unit)
    return "%d %s %d minutes" % (whole, unit, minutes)


def _distance_between(memory, understood):
    said = str(understood.get("clean") or understood.get("text") or "").lower()
    if not any(word in said for word in _FAR_ASKED):
        return None
    names = [name for name in _places_named(said) if name != "belfast city"]
    if len(names) < 2:
        return None
    first, second = names[0], names[1]
    if first == second:
        return None
    km = _km(first, second)
    miles = _miles(km)
    said_km = _nearest_five(km)
    net_one, net_two = _network(first), _network(second)
    there = "%s to %s" % (first.title(), second.title())
    road = _nearest_five(km * _ROAD_FACTOR + _ROAD_ALLOWANCE)
    if said_km < 40:
        how = "a taxi or a bus"
        if said_km <= 10:
            how = "a taxi, a bus or about %s on a bike" % _duration(km / 16.0)
        return ("%s is only about %d km (%d miles) apart - closer than most people think, so it "
                "is %s rather than a journey." % (there, said_km, miles, how))
    if net_one == net_two and net_one in _ROAD_SPEED and km <= 1200:
        return ("%s is about %d km (%d miles) in a straight line and roughly %d km (%d miles) by "
                "road, so allow about %s of driving without stops. That is the motorway figure; "
                "town traffic or a slow A-road at either end adds to it."
                % (there, said_km, miles, road, _miles(road),
                   _drive_time(road, net_one)))
    if km <= 1200 and net_one != net_two:
        crossing = {net_one, net_two}
        air = _duration(km / 700.0 + 0.8)
        if crossing == {"gb", "ie"}:
            return ("%s is about %d km (%d miles) in a straight line, with the Irish Sea in "
                    "between: a flight is about %s once the airports are counted, and the ferry "
                    "runs to a timetable rather than a distance." % (there, said_km, miles, air))
        if crossing == {"gb", "eu"}:
            return ("%s is about %d km (%d miles) in a straight line, with the Channel in "
                    "between: the tunnel does take cars, but the Eurostar or a flight of about "
                    "%s beats driving it once the check-in and the parking are counted."
                    % (there, said_km, miles, air))
        return ("%s is about %d km (%d miles) in a straight line, with water in between: a "
                "flight is about %s once the airports are counted, and the ferry runs to a "
                "timetable rather than a distance." % (there, said_km, miles, air))
    if km <= 1200:
        return ("%s is about %d km (%d miles) in a straight line. The road route is longer than "
                "that - allow roughly %s of driving, or take the train, which is usually quicker "
                "between two cities that close."
                % (there, said_km, miles, _drive_time(road, "eu")))
    if km < 3500:
        return ("%s is about %d km (%d miles) in a straight line, so roughly %s in the air once "
                "the climb and the landing are counted - too far to drive in a day."
                % (there, said_km, miles, _duration(km / 800.0 + 1)))
    return ("%s is about %d km (%d miles) in a straight line, which is a long-haul flight of "
            "%.0f hours or more, and nobody drives it."
            % (there, said_km, miles, (km / 850.0) + 2))


ENTRIES.append(entry(
    "far-between-places", (_FAR_ASKED + ("how far", "miles apart", "far apart", "distance"),
                           tuple(sorted(_PLACE)) + ("miles", "km", "kilometres", "kilometers",
                                                    "between", "drive", "driving", "journey")),
    _distance_between,
    avoid=("how far can i go", "how far will", "how much petrol", "fuel", "petrol",
           "on 20 pounds", "how long does it take to boil", "boil",
           "how long does it take to cook", "cook", "how long does it take to charge",
           "charge", "how long does it take to heal", "heal", "how long does it take to arrive",
           "how long does it take to get there", "how long does it take to learn",
           "how long does it take to bake", "how long does it take to digest")))

ENTRIES.append(entry(
    "using-an-adaptor",
    (("adapter", "adaptor", "hairdryer", "hair dryer", "straighteners", "curling tongs",
      "converter", "dual voltage", "electric shaver"),
     ("how do i use", "how to use", "use", "using", "work", "works", "working", "abroad",
      "away", "travel", "holiday", "trip", "voltage", "volts", "converter")),
    "The adapter changes the shape of the pins, not the voltage: put it in the wall socket, plug "
    "your own charger into it, and check the small print on the charger says 100-240V before you "
    "pack it. The things to check are the ones with a motor or a heating element - a hairdryer, "
    "straighteners, a kettle - because a 120V appliance from the US on a 230V supply needs a "
    "converter and not an adapter, while a dual-voltage travel hairdryer is cheaper and safer "
    "than a good converter.",
    bias=1,
    avoid=("type c", "type g", "type e", "type f", "round pins", "square pins", "flat pins",
           "same as the uk", "sockets in"),
))
