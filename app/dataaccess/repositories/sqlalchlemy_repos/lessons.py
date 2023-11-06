from sqlalchemy import delete

from app.dataaccess.models import Lessons
from app.dataaccess.models.lessons import lesson_question_association

from app.dataaccess.repositories.abstract_repos import ILessonRepository
from app.dataaccess.repositories.sqlalchlemy_repos.base import ISQLAlchemyRepo


class LessonRepo(ISQLAlchemyRepo, ILessonRepository):
    model = Lessons

    async def delete_question(self, question_id):
        stmt = delete(lesson_question_association).filter_by(
            question_id=question_id)
        await self.session.execute(stmt)

