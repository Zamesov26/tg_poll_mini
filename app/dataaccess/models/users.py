from typing import Optional, Any

from sqlalchemy import JSON, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.dataaccess.database import Base


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True,
                                    autoincrement=False)
    state: Mapped[Optional[str]]
    name: Mapped[Optional[str]]
    data: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)

    def __str__(self):
        return f'(<Users> id_={self.id}, name={self.name}, state={self.state})'

    def __repr__(self):
        return self.__str__()

