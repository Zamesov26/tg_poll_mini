from aiogram.fsm.state import StatesGroup, State


class BaseStates(StatesGroup):
    registration = State()  # Ожидает подтверждения от учителя
    main_menu = State()  # Авторизован может пользоваться
