from ..compose import lead_in

PRIORITY = 320


def respond(text, memory):
    return lead_in.the_answer_the_lead_in_hid(text, memory)
