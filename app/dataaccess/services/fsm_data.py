from typing import Optional

from app.dataaccess.models import FSMData, FSMState
from app.dataaccess.utils.unitofwork import IUnitOfWork


class FSMDataService:
    @classmethod
    async def get_state(cls, uow: IUnitOfWork,
                        bot_id, chat_id, user_id) -> Optional[str]:
        async with uow:
            row: FSMState = await uow.fsm_state.find_one(bot_id=bot_id,
                                                         chat_id=chat_id,
                                                         user_id=user_id)
            return row.state if row else None

    @classmethod
    async def set_state(cls, uow: IUnitOfWork,
                        bot_id, chat_id, user_id, state):
        async with uow:
            row: FSMData = await uow.fsm_state.find_one(bot_id=bot_id,
                                                        chat_id=chat_id,
                                                        user_id=user_id)
            if not row:
                row: FSMData = await uow.fsm_state.add_one(bot_id=bot_id,
                                                           chat_id=chat_id,
                                                           user_id=user_id)
            row.state = state
            await uow.add(row)
            await uow.commit()

    @classmethod
    async def get_data(cls, uow, bot_id, chat_id, user_id):
        async with uow:
            row: FSMData = await uow.fsm_data.find_one(bot_id=bot_id,
                                                       chat_id=chat_id,
                                                       user_id=user_id)
            return row.data if row else {}

    @classmethod
    async def set_data(cls, uow: IUnitOfWork,
                       bot_id, chat_id, user_id, data):
        async with uow:
            row: FSMData = await uow.fsm_data.find_one(bot_id=bot_id,
                                                       chat_id=chat_id,
                                                       user_id=user_id)
            if not row:
                row: FSMData = await uow.fsm_data.add_one(bot_id=bot_id,
                                                          chat_id=chat_id,
                                                          user_id=user_id)
            row.data = data
            await uow.add(row)
            await uow.commit()
