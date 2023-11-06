from datetime import datetime

from aiogram.types import PollAnswer
from sqlalchemy.exc import IntegrityError

from app.dataaccess.services import QuestionService
# from app.dataaccess.lessons.services import LessonService
# from app.dataaccess.questions.dao_quizes import QuizService
# from app.dataaccess.users.services import UserRepository

# send_random_poll


# async def send_random_poll(bot, user_id) -> bool:
#     attempt = await QuestionService.get_random_by_user_id(user_id=user_id)
#     if attempt:
#         question = (
#             await QuizService.find_one(id_=attempt.question.id)
#         ).to_poll()
#
#         if question.find_one('type') == 'text':
#             message = await bot.send_message(
#                 user_id,
#                 question.find_one('question', 'Сообщения не найдено')
#             )
#             await UserRepository.update(
#                 user_id,
#                 data={'attempt_id': attempt.id,
#                       'last_message': message.message_id}
#             )
#             return True
#
#         new_poll = await bot.send_poll(
#             chat_id=user_id,
#             **question
#         )
#
#         await UserRepository.update(
#             user_id,
#             data={'attempt_id': attempt.id,
#                   'correct_option_id': question['correct_option_id'],
#                   'last_message': new_poll.message_id}
#         )
#
#         return True
#
#     await UserRepository.update(user_id, data={})
#     return False

#
# async def assign_lesson_questions(user_id, lesson_name):
#     lesson = await LessonService.find_one(name=lesson_name)
#     if not lesson:
#         return
#     questions = [question.id for question in lesson.questions]
#     try:
#         await UserRepository.add_questions(user_id=user_id,
#                                            questions=questions)
#     except IntegrityError:
#         pass
#
#
# async def process_poll_answer(user_id, poll: PollAnswer):
#     user = await UserRepository.find_one(id_=user_id)
#     await poll.bot.delete_message(
#         message_id=user.data.find_one('last_message'),
#         chat_id=user_id
#     )
#
#     data = {'check_required': True}
#     if user.data['correct_option_id'] == poll.option_ids[0]:
#         data['is_passed'] = True
#
#     data['expectation_date'] = datetime.utcnow()
#
#     await UserRepository.update_question_attempt(user.data.find_one('attempt_id'),
#                                                  **data)
#
#
# async def process_text_answer(user_id, message):
#     user = await UserRepository.find_one(user_id)
#     await message.bot.delete_message(
#         message_id=user.data.find_one('last_message'),
#         chat_id=message.chat.id
#     )
#     await UserRepository.update_question_attempt(
#         user.data['attempt_id'],
#         check_required=True,
#         expectation_date=datetime.utcnow(),
#         text_answer=message.text
#     )
#
#
# async def send_questionnaire(bot, user_id, question, options):
#     poll = await bot.send_poll(
#         user_id,
#         question=question,
#         options=options,
#         type='regular',
#         protect_content=True,
#         is_anonymous=False
#     )
#     quest = await QuestionnaireService.add_one(user_id, question)
#     await UserRepository.update(user_id,
#                                 data={'options': options,
#                                    'last_message': poll.message_id,
#                                    'quest_id': quest.id})
#
#
# async def process_questionnaire(user_id, poll):
#     user = await UserRepository.find_one(user_id)
#     await poll.bot.delete_message(chat_id=user_id,
#                                   message_id=user.data.find_one('last_message'))
#     await QuestionnaireService.update(
#         user.data.find_one('quest_id'),
#         answer=user.data.find_one('options')[poll.option_ids[0]]
#     )
