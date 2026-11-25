import re

PRIORITY = 8000
ANSWERS = ("identity", "arcai", "developer")

WHO = re.compile(
    r"\b(?:who are you|what are you|what is your name|who made you|who developed you|"
    r"who created you|who built you|are you (?:chatgpt|gpt|claude|gemini|arcai)|"
    r"who is your developer|tell me about yourself|introduce yourself|are you a chatbot|"
    r"are you a bot|are you a person|are you human)\b",
    re.I,
)
NAME = re.compile(r"\b(?:what is your name|what do people call you|who are you)\b", re.I)
MAKER = re.compile(r"\b(?:who made you|who developed you|who created you|who built you|who is your developer)\b", re.I)


def respond(text, memory):
    line = str(text or "").strip()
    if not WHO.search(line):
        return None
    if MAKER.search(line):
        return "I was developed by Ibrahim Shaikh. I am Arcai."
    if NAME.search(line):
        return "My name is Arcai. I was developed by Ibrahim Shaikh."
    return "I am Arcai, developed by Ibrahim Shaikh."
