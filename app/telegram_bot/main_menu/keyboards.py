from aiogram.types import InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardBuilder


def main_menu_keyboard():
    # TODO если нету открытых наборов кнопку не показываем
    buttons = [[
        InlineKeyboardButton(text='Тестирование на бюджет',
                             callback_data="main_recruited_budget"),
        InlineKeyboardButton(text='Ввести код',
                             callback_data="main_enter_code")
    ]]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def recruited_budget_keyboard():
    # TODO курсы должны быть динамическими и зависеть от данных в базе
    buttons = [
        [InlineKeyboardButton(text='Создание игр в Roblox(Бюджет)',
                              callback_data="roblox_selection")],
        [InlineKeyboardButton(text='Вернуться в меню',
                              callback_data="menu_callback")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_menu():
    buttons = [
        [InlineKeyboardButton(text='Тренажер', callback_data="main_trainer")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
