from .lookup import entry

ANSWERS = ("home-and-diy", "technology")

_HEAT = ("hot", "warm", "warm to the touch", "hot to the touch", "too hot", "very hot",
         "burning", "burnt", "scorched", "scorch", "smells of burning", "smell of burning",
         "smells like burning", "smells of hot plastic", "smoking", "smoke", "sparks",
         "sparking", "buzzing", "buzzes", "melting", "melted", "overheating")
_HARDWARE = ("plug", "plugs", "plug socket", "socket", "sockets", "wall socket", "mains",
             "cable", "cables", "lead", "leads", "flex", "wire", "wires", "wiring",
             "extension lead", "fuse", "fuses", "dimmer", "light switch")

_NOT_A_WASH = ("temperature", "degrees", "what temperature", "wool", "shrink", "shrunk",
               "stain", "stains", "how do i", "how to", "wash my clothes", "load",
               "sort", "lights", "darks", "wash at", "cheaper", "soap", "detergent",
               "tooth", "teeth", "gum", "gums", "dentist", "mouth", "extraction", "wisdom",
               "filling", "dentures", "dry socket", "bleeding", "blood", "clot", "ache")

ENTRIES = [
    entry("power-hot",
          (_HARDWARE, _HEAT),
          "A plug, socket or cable that is hot, buzzing, scorched or smells of burning is not "
          "safe to keep using: unplug it at the wall, or switch that circuit off, and leave it "
          "off. Warm to the touch is normal for a charger; too hot to hold, crackling, brown "
          "marks, a fishy smell of hot plastic or a fuse that keeps tripping is not, and that "
          "plug or socket needs replacing by an electrician before it is used again. Never open "
          "a socket yourself, and do not just change the fuse and carry on.",
          avoid=_NOT_A_WASH,
          bias=2),
]
