from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.dataaccess.services import UserService
from app.dataaccess.utils.unitofwork import IUnitOfWork
from app.telegram_bot.main_menu.keyboards import main_menu_keyboard, \
    recruited_budget_keyboard, get_menu
from app.telegram_bot.main_menu.services import new_user
from app.telegram_bot.main_menu.states import BaseStates

router = Router()
router.message.filter(
    F.chat.type == "private"
)


@router.message(Command("menu"), BaseStates.registration)
async def in_registration_cmd_start(message: Message):
    await message.answer("Ожидайте вас еще не добавили в группу")


@router.message(Command("start"))
async def cmd_start(message: Message, uow: IUnitOfWork, state: FSMContext):
    user = await UserService.get_by_id(uow, message.from_user.id)
    if not user:
        await new_user(uow, message, state)

    await message.answer(
        'Выберите действие',
        reply_markup=main_menu_keyboard())
    return


@router.callback_query(F.data == "main_enter_code")
async def callback_main_enter_code(callback: CallbackQuery):
    await callback.answer(text='Код не найден')


@router.callback_query(F.data == "main_recruited_budget")
async def callback_main_recruited_budget(callback: CallbackQuery):
    await callback.bot.edit_message_text(
        chat_id=callback.from_user.id,
        text='Выберите курс',
        message_id=callback.message.message_id,
        reply_markup=recruited_budget_keyboard()
    )


@router.callback_query(F.data == "menu_callback")
async def callback_main_menu_callback(callback: CallbackQuery):
    await callback.bot.edit_message_text(
        chat_id=callback.from_user.id,
        text='Выберите действие:',
        message_id=callback.message.message_id,
        reply_markup=main_menu_keyboard()
    )


@router.message(Command("menu"), BaseStates.registration)
async def main_menu_closed(message: Message):
    await message.answer("Ожидайте вас еще не добавили в группу")


@router.message(Command("menu"))
async def main_menu(message: Message):
    await message.answer(
        'Выберите действие',
        reply_markup=get_menu())
