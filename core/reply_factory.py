
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    if current_question_id is not None:
        session['answers'] = session.get('answers', {})
        session['answers'][current_question_id] = answer
        session.save()
        return True, ""
    else:
        return False, "No current question found"


def get_next_question(current_question_id):
    for index, question in enumerate(PYTHON_QUESTION_LIST):
        if question['id'] == current_question_id:
            next_index = index + 1
            if next_index < len(PYTHON_QUESTION_LIST):
                return PYTHON_QUESTION_LIST[next_index]['question'], PYTHON_QUESTION_LIST[next_index]['id']
            else:
                return None, None
    return "dummy question", -1


def generate_final_response(session):
    answers = session.get('answers', {})
    total_score = sum(calculate_score(question_id, answer) for question_id, answer in answers.items())
    return f"Your final score is {total_score}. Thank you for participating!"


def calculate_score(question_id, answer):
   
    return len(answer.split())