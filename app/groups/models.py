from typing import List, Optional

from sqlalchemy import ForeignKey, Table, Integer, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

user_group_association = Table(
    'user_group_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('group_id', Integer, ForeignKey('groups.id'))
)


class Groups(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    teacher_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    course_id: Mapped[Optional[int]]  # mapped_column(ForeignKey("courses.id"))

    users: Mapped[List["Users"]] = relationship(
        secondary=user_group_association
    )

# class Courses(Base):
#     __tablename__ = 'courses'
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str]
#
#     lessons: Mapped[List["Lessons"]] = relationship(
#         secondary=course_lesson_association
#     )