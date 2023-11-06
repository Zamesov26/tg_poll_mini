from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.dataaccess.services import UserService
from app.dataaccess.utils.unitofwork import IUnitOfWork
from app.telegram_bot.quizes.states import QuizStates

# from app.telegram_bot.entrance_exams.roblox.routes import OrderQuestionnaire

# from app.dataaccess.services import UserService
# from app.telegram_bot.entrance_exams.roblox.routes import OrderQuestionnaire
# from app.dataaccess.services import QuestionService

router = Router()
router.message.filter(
    F.chat.type == "private"
)


@router.message(QuizStates.await_answer)
async def main_menu_closed(message: Message):
    await message.answer("У вас есть не отвеченная задача!")


@router.callback_query(F.data == "main_trainer")
async def callback_main_trainer(callback: CallbackQuery, uow: IUnitOfWork):
    async with uow:
        question = uow.user_attempts.get_random_by_user(
            user_id=callback.from_user.id)

        if not question:
            print("Если есть отправляем сообщение меняем статус")
            # question.id ??
            # message_id = poll_service.send_poll()
            # fsm_service.update_state(poll_id)
            return
        else:
            print("не получили")

        await callback.answer()

    # attempt_id = question.id
    # if question.question.type == 'poll':
    #     question = (
    #         await QuestionService.get_question(id=question.question.id)).to_poll()
    #     await UserRepository.update(
    #         user.id,
    #         state='waiting answer poll',
    #         data={'correct_option_id': question.find_one('correct_option_id'),
    #               'attempt_id': attempt_id}
    #     )
    #     print(question)
    #     await message.answer_poll(**question)
    #     return
    # else:
    #     await UserRepository.update(
    #         user.id,
    #         state='waiting answer text',
    #         data={'attempt_id': attempt_id}
    #     )
    #     await UserRepository.update_question_attempt(
    #         attempt_id,
    #         expectation_date=datetime.utcnow()
    #     )
    #     await message.answer(question.question.text)
#
# @router.message(Command("start"))
# async def cmd_start(message: Message, uow: IUnitOfWork, state: FSMContext):
#     user = await UserService.get_by_id(uow, message.from_user.id)
#     if not user:
#         user = await UserService.create(uow,
#                                         user_id=message.from_user.id,
#                                         user_name=message.from_user.full_name)
#         await message.bot.send_message(
#             1097904939,
#             text=f'Новый пользователь @{message.from_user.username}\n'
#                  f'Имя {message.from_user.full_name}'
#         )
#
#         # TODO выдать список для поступления
#         #  либо предложить подобрать программу
#         await message.answer("Добро пожаловать, бот создан "
#                              "для повторения и закрепления знаний по урокам,"
#                              "обратитесь к учителю "
#                              "для добавления в группу или введите код.")
#         await state.set_state(BaseStates.registration)
#         builder = InlineKeyboardBuilder()
#         builder.add(InlineKeyboardButton(text='Пройти отбор',
#                                          callback_data="roblox_selection"))
#         await message.answer(
#             'Открыт набор на бюджетный курс "Создание игр в Roblox"',
#             reply_markup=builder.as_markup())
#         return
#     else:
#         await state.set_state(BaseStates.registration)
#         await message.answer('С возвращением!)')  # TODO Дать какое-то меню
#
# if user.state in ['waiting answer poll', 'waiting answer text']:
#     await message.answer("У вас есть не отвеченная задача")
#     return
#
# question = await UserRepository.get_random_by_user_id(user_id=user.id)
# if not question:
#     await message.answer("Для вас пока нету заданий")
#     return
#
# attempt_id = question.id
# if question.question.type == 'poll':
#     question = (
#         await QuizService.find_one(id_=question.question.id)).to_poll()
#     await UserRepository.update(
#         user.id,
#         state='waiting answer poll',
#         data={'correct_option_id': question.find_one('correct_option_id'),
#               'attempt_id': attempt_id}
#     )
#     print(question)
#     await message.answer_poll(**question)
#     return
# else:
#     await UserRepository.update(
#         user.id,
#         state='waiting answer text',
#         data={'attempt_id': attempt_id}
#     )
#     await UserRepository.update_question_attempt(
#         attempt_id,
#         expectation_date=datetime.utcnow()
#     )
#     await message.answer(question.question.text)

# @router.poll_answer()
# async def poll_handler(poll: PollAnswer):
#     user = await UserRepo.get_user(id_=poll.user.id_)
#     data = {}
#     if user.data['correct_option_id'] == poll.option_ids[0]:
#         data['is_passed'] = True
#     else:
#         data['expectation_date'] = datetime.utcnow() + timedelta(days=1)
#
#     await UserRepo.update_question_attempt(user.data.get('attempt_id'),
#                                               **data)
#     await UserRepo.update(user.id_, state='ready', data={})


# @router.message(F.text)
# async def message_with_text(message: Message):
#     user = await UserRepository.find_one(message.from_user.id)
#     if user.state == 'waiting answer text':
#         await message.answer("Ваш ответ принят, ожидайте "
#                              "проверки преподавателем")
#         await UserRepository.update_question_attempt(
#             user.data.find_one('attempt_id'),
#             check_required=True,
#             expectation_date=datetime.utcnow()
#         )
#         await UserRepository.update(user.id, state='ready', data={})
