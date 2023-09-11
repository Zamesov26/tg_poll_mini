from random import shuffle
from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base

class Questions(Base):
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    type: Mapped[str] = mapped_column(default='quiz')
    img: Mapped[Optional[str]]

    answers: Mapped[List['Answers']] = relationship()

    def to_poll(self):
        options = []
        shuffle(self.answers)
        correct_option_id = 0
        for i in range(len(self.answers)):
            options.append(self.answers[i].text)
            if self.answers[i].is_true:
                correct_option_id = i
        return {
            'question': self.text,
            'options': options,
            'correct_option_id': correct_option_id,
            'protect_content': True,
            'is_anonymous': False,
            'type': self.type
        }

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.__str__()


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
