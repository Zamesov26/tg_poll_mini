from typing import Optional, Dict, Any

from aiogram.fsm.storage.base import BaseStorage, StorageKey, StateType

from app.dataaccess.services.fsm_data import FSMDataService
from app.dataaccess.utils.unitofwork import IUnitOfWork


class PGStorage(BaseStorage):
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def set_state(self, key: StorageKey,
                        state: StateType = None) -> None:
        await FSMDataService.set_state(self.uow,
                                       bot_id=key.bot_id,
                                       chat_id=key.chat_id,
                                       user_id=key.user_id,
                                       state=state.state)

    async def get_state(self, key: StorageKey) -> Optional[str]:
        return await FSMDataService.get_state(self.uow,
                                              bot_id=key.bot_id,
                                              chat_id=key.chat_id,
                                              user_id=key.user_id)

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        await FSMDataService.set_data(self.uow,
                                      bot_id=key.bot_id,
                                      chat_id=key.chat_id,
                                      user_id=key.user_id,
                                      data=data)

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        return await FSMDataService.get_data(self.uow,
                                             bot_id=key.bot_id,
                                             chat_id=key.chat_id,
                                             user_id=key.user_id)

    async def close(self) -> None:
        pass
