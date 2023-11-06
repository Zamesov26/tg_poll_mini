from typing import Optional

from sqlalchemy import BigInteger, JSON, Index
from sqlalchemy.orm import mapped_column, Mapped

from app.dataaccess.database import Base


class FSMData(Base):
    __tablename__ = 'fsm_data'

    id: Mapped[int] = mapped_column(primary_key=True)
    bot_id: Mapped[int] = mapped_column(BigInteger)
    chat_id: Mapped[int] = mapped_column(BigInteger)
    user_id: Mapped[int] = mapped_column(BigInteger)

    data: Mapped[Optional[dict]] = mapped_column(JSON, default=dict,
                                                 server_default='{}')

    index_ids = Index('index_fsm_data_ids', bot_id, chat_id, user_id)


class FSMState(Base):
    __tablename__ = 'fsm_state'

    id: Mapped[int] = mapped_column(primary_key=True)
    bot_id: Mapped[int] = mapped_column(BigInteger)
    chat_id: Mapped[int] = mapped_column(BigInteger)
    user_id: Mapped[int] = mapped_column(BigInteger)

    state: Mapped[Optional[str]]

    index_ids = Index('index_fsm_state_ids', bot_id, chat_id, user_id)
