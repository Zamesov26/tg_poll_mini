from aiogram.fsm.state import StatesGroup, State


class OrderQuestionnaire(StatesGroup):
    registration = State()
    start_testing = State()
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
