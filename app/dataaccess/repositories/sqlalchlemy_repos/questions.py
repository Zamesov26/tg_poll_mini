from app.dataaccess.repositories.sqlalchlemy_repos.base import ISQLAlchemyRepo
from app.dataaccess.models import Questions


class QuestionRepo(ISQLAlchemyRepo):
    model = Questions
