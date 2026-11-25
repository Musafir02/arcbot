from bot.memory import plan

PRIORITY = 7100


def respond(text, memory):
    if not isinstance(memory, dict):
        return None
    return plan.carry_on(text, memory)
