import re

from ..memory import saving
from ..understanding import understand
from . import answers

PRIORITY = 1100

ANSWERS = ("money",)

A_LENGTH_IN_MONTHS = re.compile(
    r"\b(?:is|in|takes|takes\s+about)\s+(?:about\s+)?"
    r"(?:\d[\d,]*|a|an|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s*"
    r"(?:month|months|year|years|week|weeks)\b|\bone\s+pay\s+packet\b", re.I)


def _lower_first(answer):
    text = str(answer or "")
    if not text or not text[0].isupper() or text[:2].isupper():
        return text
    return text[0].lower() + text[1:]


def _the_money_answer(question, memory):
    if not question:
        return ""
    was = memory.get("understood")
    try:
        memory["understood"] = understand(question, memory)
        answer = answers._respond(question, memory) or ""
    finally:
        if was is None:
            memory.pop("understood", None)
        else:
            memory["understood"] = was
    if not answer:
        return ""
    return saving.without_what_was_just_said(answer, memory) or answer


_SEEN = {}


def _the_reply(text, memory):
    try:
        turns = memory.get("turns") or ()
        key = (id(memory), str(text or ""), len(turns),
               str((turns[-1] or {}).get("user") or "") if turns else "")
    except Exception:
        key = None
    if key is not None and key in _SEEN:
        return _SEEN[key]
    reply = _read(text, memory) or ""
    if key is not None:
        if len(_SEEN) > 32:
            _SEEN.clear()
        _SEEN[key] = reply
    return reply


def respond(text, memory):
    if not isinstance(memory, dict):
        return None
    return _the_reply(text, memory) or None


def TAKES_AS_IT_COMES(text, memory):
    if not isinstance(memory, dict):
        return False
    return bool(_the_reply(text, memory))


def _read(text, memory):
    gap = saving.the_gap_left(text, memory)
    if gap:
        return gap
    position = saving.the_pot_position(text, memory)
    if position:
        return position
    more_a_month = saving.the_extra_a_month_asked(text, memory)
    if more_a_month:
        return more_a_month
    same_figure = saving.the_same_figure_a_month(text, memory)
    if same_figure:
        return same_figure
    enough = saving.a_yes_no_about_the_rate(text, memory)
    if enough:
        return enough
    need_a_date = saving.a_rate_with_no_date(text, memory)
    if need_a_date:
        return need_a_date
    raised = saving.a_rate_raised(text, memory)
    if raised:
        return raised
    restated = saving.a_rate_restated(text, memory)
    if restated:
        return restated
    put_in = saving.a_rate_put_in_with_a_verb(text, memory)
    if put_in:
        return put_in
    at_the_chat_rate = saving.a_length_at_the_rate_in_the_chat(text, memory)
    if at_the_chat_rate:
        answer = _the_money_answer(at_the_chat_rate, memory)
        if answer:
            return answer
    no_price = saving.a_length_with_no_price(text, memory)
    if no_price:
        return no_price
    price = saving.a_price_in_an_answer(text, memory)
    if price:
        return price
    a_rate_given = saving.a_rate_for_the_goal(text, memory)
    if a_rate_given:
        return a_rate_given
    if saving.asks_how_long(text):
        length = saving.how_long_it_takes(memory)
        if length:
            return length
    pot_alone = saving.the_pot_said_alone(text)
    if pot_alone:
        whole = saving._the_goal_in_the_chat(memory)
        if whole > pot_alone:
            rest = whole - pot_alone
            answer = _the_money_answer(saving.rate_question_for(rest), memory)
            if answer:
                return ("£%s still to find: %s"
                        % (format(rest, ","),
                           _lower_first(saving.without_the_pot_opener(answer))))
    if saving.asks_about_saving(text) and saving._names_a_goal(text):
        pot, rest = saving.the_pot_and_the_rest(text)
        answer = ""
        if saving._a_rate_said(text)[0] or saving.a_length_was_said(text):
            plain = _the_money_answer(text, memory)
            if plain and A_LENGTH_IN_MONTHS.search(plain):
                answer = plain
        if not answer:
            answer = _the_money_answer(saving.rate_question(text, memory), memory)
        if answer:
            if pot and rest:
                return ("£%s to find on top of the £%s you already have: %s"
                        % (format(rest, ","), format(pot, ","),
                           _lower_first(saving.without_the_pot_opener(answer))))
            return answer
    if saving.asks_the_rate(text, memory):
        answer = _the_money_answer(saving.rate_question(text, memory), memory)
        if answer and saving.said_already(answer, memory):
            other = saving.a_figure_each_week(memory)
            if not other or saving.said_already(other, memory):
                fresh = saving.the_figure_a_week(memory)
                other = _the_money_answer(fresh, memory) if fresh else ""
            if other and not saving.said_already(other, memory):
                answer = other
        if answer:
            return answer
    if saving.is_only_a_date(text):
        settled = saving.a_date_on_a_settled_rate(text, memory)
        if settled:
            return settled
        money_question = saving.rate_question(text, memory)
        if money_question:
            answer = _the_money_answer(money_question, memory)
            if answer:
                return answer
    again = saving.another_sum_asked(text, memory)
    if again:
        fresh = dict(memory)
        fresh.pop("understood", None)
        answer = _the_money_answer(saving.rate_question(again, fresh), fresh)
        if not answer:
            answer = _the_money_answer(again, fresh)
        if answer:
            return answer
    return None

from ..memory import again as _said_before

respond = _said_before.replied(respond)
