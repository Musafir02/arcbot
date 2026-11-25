from ..compose import nearby_one

PRIORITY = -995


def respond(text, memory):
    try:
        return nearby_one.reply_for(text, memory) or None
    except Exception:
        return None
