from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import async_session_maker
from app.lessons.models import Lessons
from app.quizes.models import Questions


class LessonService:
    @classmethod
    async def add_lesson(cls, lesson_name):
        async with async_session_maker() as session:
            lesson = Lessons(name=lesson_name)

            session.add(lesson)

            await session.commit()
            await session.refresh(lesson)

            return lesson

    @classmethod
    async def get_lesson(cls, **filters) -> Optional[Lessons]:
        async with async_session_maker() as session:
            stmt = select(Lessons).filter_by(**filters).options(
                selectinload(Lessons.questions))

            result = await session.execute(stmt)
            return result.scalars().one_or_none()

    @classmethod
    async def add_questions_to_lesson(cls,
                                      questions: List[Questions],
                                      lesson: Lessons):
        async with async_session_maker() as session:
            for question in questions:
                lesson.questions.append(question)

            session.add(lesson)
            await session.commit()

    @classmethod
    async def save_lesson(cls, lesson: Lessons):
        async with async_session_maker() as session:
            session.add(lesson)
            await session.commit()
