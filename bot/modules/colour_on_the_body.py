from ..compose import colour_on_the_body

PRIORITY = 350


def respond(text, memory):
    try:
        return colour_on_the_body.reply_for(text, memory) or None
    except Exception:
        return None
