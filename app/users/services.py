from datetime import datetime, timedelta
from operator import or_
from typing import List, Optional

from sqlalchemy import select, and_, not_, func, update, insert
from sqlalchemy.orm import selectinload

from app.database import async_session_maker
from app.users.models import Users, UserQuestionAttempts


class UserService:
    @classmethod
    async def add_user(cls,
                       user_id: int,
                       name: str = None,
                       state: str = 'start'):
        async with async_session_maker() as session:
            user = Users(id=user_id, name=name, state=state)

            session.add(user)
            await session.commit()
            await session.refresh(user)

            return user

    @classmethod
    async def update(cls, user_id, **values):
        async with async_session_maker() as session:
            stmt = update(Users) \
                .where(Users.id == user_id) \
                .values(**values)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def get_user(cls, user_id: int) -> Optional[Users]:
        async with async_session_maker() as session:
            stmt = select(Users).filter_by(id=user_id)

            result = await session.execute(stmt)
            return result.scalars().one_or_none()

    @classmethod
    async  def get_users(cls, **filters) -> list[Users]:
        async with async_session_maker() as session:
            stmt = select(Users).filter_by(**filters)

            result = await session.execute(stmt)
            return result.scalars().all()

    @classmethod
    async def assign_questions(cls, user_id: int, questions: List[int]):
        async with async_session_maker() as session:
            for question_id in questions:
                stmt = insert(UserQuestionAttempts).values(
                    user_id=user_id,
                    question_id=question_id
                )
                await session.execute(stmt)
            await session.commit()

    @classmethod
    async def get_question_attempt(cls, user_id: int) -> Optional[UserQuestionAttempts]:
        async with async_session_maker() as session:
            date_now = datetime.now()
            stmt = select(UserQuestionAttempts) \
                .where(and_(UserQuestionAttempts.user_id == user_id,
                            not_(UserQuestionAttempts.is_passed),
                            not_(UserQuestionAttempts.check_required),
                            or_(UserQuestionAttempts.expectation_date.is_(None),
                                UserQuestionAttempts.expectation_date < date_now)
                            )) \
                .order_by(func.random()) \
                .options(selectinload(UserQuestionAttempts.question))

            question = await session.execute(stmt)

            return question.scalars().first()

    @classmethod
    async def update_question_attempt(cls, id_, **values):
        async with async_session_maker() as session:
            stmt = update(UserQuestionAttempts) \
                .where(UserQuestionAttempts.id == id_) \
                .values(**values)
            await session.execute(stmt)
            await session.commit()


