from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from app.dataaccess.database import Base


class Answers(Base):
    __tablename__ = 'answers'

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey('questions.id'))
    text: Mapped[str]
    is_true: Mapped[bool] = mapped_column(default=False)

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.__str__()
