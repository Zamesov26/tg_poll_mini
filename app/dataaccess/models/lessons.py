from typing import List

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dataaccess.database import Base

lesson_question_association = Table(
    'lesson_question_association',
    Base.metadata,
    Column('lesson_id', Integer, ForeignKey('lessons.id')),
    Column('question_id', Integer, ForeignKey('questions.id'))
)


class Lessons(Base):
    __tablename__ = 'lessons'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    questions: Mapped[List["Questions"]] = relationship(
        secondary=lesson_question_association,
    )
