from ..memory import stands

PRIORITY = 1000


def respond(text, memory):
    return stands.reply_for(text, memory) or stands.change_reply(text, memory)


def takes_as_it_comes(text, memory):
    try:
        return bool(stands.the_figure_asked_about(text, memory)
                    or stands.the_change_asked_about(text, memory))
    except Exception:
        return False


TAKES_AS_IT_COMES = takes_as_it_comes
