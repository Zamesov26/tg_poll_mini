from datetime import date
from typing import Optional

from sqlalchemy import ForeignKey, TIMESTAMP, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.dataaccess.database import Base


class UserAttempts(Base):
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

    user: Mapped["Users"] = relationship()
    question: Mapped["Questions"] = relationship()
