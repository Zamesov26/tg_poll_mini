from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.dataaccess.database import Base


class Questionnaires(Base):
    __tablename__ = 'questionnaire'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    question: Mapped[str]
    answer: Mapped[Optional[str]]
