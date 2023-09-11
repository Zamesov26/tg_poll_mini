from typing import Optional, Any
from datetime import date

from sqlalchemy import ForeignKey, TIMESTAMP, func, JSON, UniqueConstraint, \
    BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True,
                                    autoincrement=False)
    state: Mapped[Optional[str]]
    name: Mapped[Optional[str]]
    data: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)

    def __str__(self):
        return '(<Users> id={}, name={}, state={})'.format(self.id,
                                                           self.name,
                                                           self.state)

    def __repr__(self):
        return self.__str__()


class UserQuestionAttempts(Base):
    __tablename__ = 'user_question_attempts'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    is_passed: Mapped[bool] = mapped_column(server_default="false",
                                            default=False)
    check_required: Mapped[bool] = mapped_column(server_default="false",
                                                 default=False)
    text_answer: Mapped[Optional[str]]
    expectation_date: Mapped[Optional[date]] = mapped_column(TIMESTAMP)

    __table_args__ = (
        UniqueConstraint('user_id', 'question_id', name='unique_combination'),
    )

    user: Mapped[Users] = relationship()
    question: Mapped["Questions"] = relationship()
