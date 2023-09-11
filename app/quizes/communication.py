from datetime import datetime

from sqlalchemy.exc import IntegrityError

from app.lessons.services import LessonService
from app.quizes.dao_quizes import QuizService
from app.users.services import UserService


async def send_random_poll(bot, user_id) -> bool:
    attempt = await UserService.get_question_attempt(
        user_id=user_id
    )
    if attempt:
        question = (
            await QuizService.get_question(id=attempt.question.id)).to_poll()

        new_poll = await bot.send_poll(
            chat_id=user_id,
            **question
        )

        await UserService.update(
            user_id,
            data={'attempt_id': attempt.id,
                  'correct_option_id': question['correct_option_id'],
                  'last_message': new_poll.message_id}
        )

        return True

    await UserService.update(user_id, data={})
    return False


async def assign_lesson_questions(user_id, lesson_name):
    lesson = await LessonService.get_lesson(name=lesson_name)
    if not lesson:
        return
    questions = [question.id for question in lesson.questions]
    try:
        await UserService.assign_questions(user_id=user_id,
                                           questions=questions)
    except IntegrityError:
        pass


async def process_poll_answer(user_id, user_answer_id):
    user = await UserService.get_user(user_id=user_id)
    data = {'check_required': True}
    if user.data['correct_option_id'] == user_answer_id:
        data['is_passed'] = True

    data['expectation_date'] = datetime.utcnow()

    await UserService.update_question_attempt(user.data.get('attempt_id'),
                                              **data)
