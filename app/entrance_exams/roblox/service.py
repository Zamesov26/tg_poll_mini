from sqlalchemy import update

from app.database import async_session_maker
from app.entrance_exams.roblox.models import Questionnaire


class QuestionnaireService:
    @classmethod
    async def add_quest(cls,
                        user_id: int,
                        question: str,
                        answer: str = None):
        async with async_session_maker() as session:
            quest = Questionnaire(user_id=user_id, question=question, answer=answer)

            session.add(quest)
            await session.commit()
            await session.refresh(quest)

            return quest

    @classmethod
    async def update(cls, quest_id, **values):
        async with async_session_maker() as session:
            stmt = update(Questionnaire) \
                .where(Questionnaire.id == quest_id) \
                .values(**values)
            await session.execute(stmt)
            await session.commit()
