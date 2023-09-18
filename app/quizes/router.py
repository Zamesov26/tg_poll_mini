from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, PollAnswer, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.entrance_exams.roblox.routes import OrderQuestionnaire
from app.quizes.dao_quizes import QuizService
from app.users.services import UserService

router = Router()
router.message.filter(
    F.chat.type == "private"
)


@router.message(Command("start"), )
async def cmd_start(message: Message, state: FSMContext):
    user = await UserService.get_user(user_id=message.from_user.id)
    if not user:
        user = await UserService.add_user(user_id=message.from_user.id,
                                   name=message.from_user.full_name,
                                   state='registration')
        await message.bot.send_message(
            1097904939,
            text='Новый пользователь @{}'.format(message.from_user.username)
        )
        await message.answer("Добро пожаловать, бот создан "
                             "для повторения и закрепления знаний по урокам,"
                             "обратитесь к учителю "
                             "для добавления в группу или введите код.")

        await state.set_state(OrderQuestionnaire.registration)
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text='Пройти отбор',
                                         callback_data="roblox_selection"))
        await message.answer(
            'Открыт набор на бюджетный курс "Создание игр в Roblox"',
            reply_markup=builder.as_markup())
        return

    if user.state == 'registration':
        await message.answer("Ожидайте вас еще не добавили в группу")
        return

    if user.state == 'in_work':
        await message.answer("Ведутся работы")
        return

    if user.state in ['waiting answer poll', 'waiting answer text']:
        await message.answer("У вас есть не отвеченная задача")
        return

    question = await UserService.get_question_attempt(user_id=user.id)
    if not question:
        await message.answer("Для вас пока нету заданий")
        return

    attempt_id = question.id
    if question.question.type == 'poll':
        question = (
            await QuizService.get_question(id=question.question.id)).to_poll()
        await UserService.update(
            user.id,
            state='waiting answer poll',
            data={'correct_option_id': question.get('correct_option_id'),
                  'attempt_id': attempt_id}
        )
        print(question)
        await message.answer_poll(**question)
        return
    else:
        await UserService.update(
            user.id,
            state='waiting answer text',
            data={'attempt_id': attempt_id}
        )
        await UserService.update_question_attempt(
            attempt_id,
            expectation_date=datetime.utcnow()
        )
        await message.answer(question.question.text)


# @router.poll_answer()
# async def poll_handler(poll: PollAnswer):
#     user = await UserService.get_user(user_id=poll.user.id)
#     data = {}
#     if user.data['correct_option_id'] == poll.option_ids[0]:
#         data['is_passed'] = True
#     else:
#         data['expectation_date'] = datetime.utcnow() + timedelta(days=1)
#
#     await UserService.update_question_attempt(user.data.get('attempt_id'),
#                                               **data)
#     await UserService.update(user.id, state='ready', data={})


@router.message(F.text)
async def message_with_text(message: Message):
    user = await UserService.get_user(message.from_user.id)
    if user.state == 'waiting answer text':
        await message.answer("Ваш ответ принят, ожидайте "
                             "проверки преподавателем")
        await UserService.update_question_attempt(
            user.data.get('attempt_id'),
            check_required=True,
            expectation_date=datetime.utcnow()
        )
        await UserService.update(user.id, state='ready', data={})
