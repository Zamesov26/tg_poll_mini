from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, PollAnswer

from app.quizes.communication import send_random_poll, assign_lesson_questions, \
    process_poll_answer, process_text_answer

router = Router()
router.message.filter(
    F.chat.type == "private"
)

message_state = {}
delete_poll = {}


class OrderQuestionnaire(StatesGroup):
    choosing_class = State()
    choosing_has_pc = State()
    choosing_experience = State()
    text_experience_about = State()
    text_expectations = State()
    get_text_expectations = State()


class Quiz(StatesGroup):
    first = State()
    second = State()
    complete = State()


@router.message(Command("roblox"))
async def cmd_food(message: Message, state: FSMContext):
    await message.answer(
        text="Вступительное тестирование состоит из 3х частей:\n"
             "- Анкета\n"
             "- Основы ПК\n"
             "- Логические задачи\n"
             "Обратите внимание, что некоторые вопросы имеют ограничение по времени ответа."
             "Ориентировочное время прохождение: 20 минут",
    )
    active_state_message = await message.answer(
        text="Активный блок: Заполнение Анкеты"
    )
    message_state.update({
        "chat_id": message.chat.id,
        "message_id": active_state_message.message_id
    })

    poll = await message.answer_poll(
        question='В каком вы классе?',
        options=["5", "6", "7", "Нету подходящего варианта"],
        type='regular',
        protect_content=True,
        is_anonymous=False
    )
    delete_poll.update({'message_id': poll.message_id,
                        'chat_id': message.chat.id})
    await state.set_state(OrderQuestionnaire.choosing_class)


@router.poll_answer(OrderQuestionnaire.choosing_class)
async def questionnaire2(message: Message, state: FSMContext):
    global message_state
    # await message.bot.edit_message_text(text='Текст изменен' + str(randint(1, 1000)), **message_state)
    await message.bot.delete_message(**delete_poll)

    poll = await message.bot.send_poll(
        chat_id=message_state.get("chat_id"),
        question='Есть ли у вас компьютер или ноутбук?',
        options=["Да", "Нет"],
        type='regular',
        protect_content=True,
        is_anonymous=False
    )
    delete_poll.update({'message_id': poll.message_id})
    await state.set_state(OrderQuestionnaire.choosing_has_pc)


@router.poll_answer(OrderQuestionnaire.choosing_has_pc)
async def questionnaire3(poll: PollAnswer, state: FSMContext):
    global message_state
    # await message.bot.edit_message_text(text='Текст изменен' + str(randint(1, 1000)), **message_state)
    await poll.bot.delete_message(**delete_poll)

    new_poll = await poll.bot.send_poll(
        chat_id=message_state.get("chat_id"),
        question='Проходили ли вы ранее курсы связанные с программированием?',
        options=["Да", "Нет"],
        type='regular',
        protect_content=True,
        is_anonymous=False
    )
    delete_poll.update({'message_id': new_poll.message_id})
    await state.set_state(OrderQuestionnaire.choosing_experience)


@router.poll_answer(OrderQuestionnaire.choosing_experience)
async def questionnaire4(poll: PollAnswer, state: FSMContext):
    global message_state
    await poll.bot.delete_message(**delete_poll)

    if poll.option_ids[0] == 0:
        await poll.bot.send_message(
            chat_id=message_state.get("chat_id"),
            text='Расскажите об этом опыте подробнее '
                 'с помощью 1 текстового сообщения.'
        )
        await state.set_state(OrderQuestionnaire.text_experience_about)
    else:
        await poll.bot.send_message(
            poll.user.id,
            'Опишите ваши ожидания от курса '
            'с помощью 1 текстового сообщения.')
        await state.set_state(OrderQuestionnaire.get_text_expectations)


@router.message(OrderQuestionnaire.text_experience_about)
async def food_size_chosen(message: Message, state: FSMContext):
    await message.answer('Опишите ваши ожидания от курса'
                         'с помощью 1 текстового сообщения.')
    await state.set_state(OrderQuestionnaire.get_text_expectations)


@router.message(OrderQuestionnaire.get_text_expectations)
async def food_size_chosen(message: Message, state: FSMContext):
    # TODO тут мы принимаем сообщение от пользователя и сохраняем в базу
    await message.answer('Активный блок: Знание основ ПК')

    await assign_lesson_questions(message.from_user.id, 'roblox_exam_1')

    if await send_random_poll(message.bot, message.from_user.id):
        await state.set_state(Quiz.first)
    else:
        print("log: все сломалось не получилось найти вопрос для пользователя")


@router.poll_answer(Quiz.first)
async def quiz_first(poll: PollAnswer, state: FSMContext):
    await process_poll_answer(poll.user.id, poll.option_ids[0])

    if not await send_random_poll(poll.bot, poll.user.id):
        print("вопрос не найден, переходим к следующему блоку")
        await assign_lesson_questions(poll.user.id, 'roblox_exam_2')
        await send_random_poll(poll.bot, poll.user.id)
        await state.set_state(Quiz.second)


@router.message(Quiz.second)
async def quiz_first(message: Message, state: FSMContext):
    print('Принимаем сообщение от пользователя')
    await process_text_answer(message.from_user.id, message)

    if not await send_random_poll(message.bot, message.from_user.id):
        await state.set_state(Quiz.complete)
        await message.bot.send_message(
            message.from_user.id,
            'На этом тестирование окончено.\n'
            'Спасибо за участие, ожидайте ответа.\n'
            'Ориентировочная дата - 20 сентября.'
        )


@router.message(Quiz.complete)
async def expect_response(message: Message, state: FSMContext):
    await message.answer('По всем вопросам обращайтесь ко мне в телеграмм - @Zamesov')
    await state.clear()
