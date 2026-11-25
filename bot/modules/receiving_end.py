from ..compose import receiving_end

PRIORITY = -980


def respond(text, memory):
    understood = memory.get("understood")
    if not isinstance(understood, dict):
        return None
    clean = understood.get("clean") or " ".join(str(text or "").lower().split())
    repaired = understood.get("plain") or clean
    return receiving_end.reply_for(clean, repaired, memory)
