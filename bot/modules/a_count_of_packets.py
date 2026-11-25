from ..compose import pick
from ..compose.a_count_of_packets import is_a_dose
from ..knowledge.crisis_replies import REPLIES
from . import safety, urgent

PRIORITY = 9000


def respond(text, memory):
    if not is_a_dose(text):
        return None
    if safety.respond(text, memory) or urgent.respond(text, memory):
        return None
    if isinstance(memory, dict):
        memory["safety_case"] = "poison"
        memory["safety_safe"] = False
    return safety._fit(pick(REPLIES["poison"], memory), text, "poison")
