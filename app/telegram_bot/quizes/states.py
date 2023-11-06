from aiogram.fsm.state import StatesGroup, State


class QuizStates(StatesGroup):
    await_answer = State()  # Ожидаем ответа от пользователя на quiz
