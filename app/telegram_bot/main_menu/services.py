from app.dataaccess.services import UserService
from app.telegram_bot.main_menu.states import BaseStates


async def new_user(uow, message, state):
    await UserService.create(uow,
                             user_id=message.from_user.id,
                             user_name=message.from_user.full_name)
    # TODO отправить информацию всем админам подписанным на оповещения
    #  дать возможность добавить в какую-то группу или уточнить данные
    await message.bot.send_message(
        1097904939,
        text=f'Новый пользователь @{message.from_user.username}\n'
             f'Имя {message.from_user.full_name}'
    )
    await message.answer("Добро пожаловать, бот создан "
                         "для повторения и закрепления знаний по урокам,"
                         "обратитесь к учителю "
                         "для добавления в группу или введите код.")
    await state.set_state(BaseStates.registration)
