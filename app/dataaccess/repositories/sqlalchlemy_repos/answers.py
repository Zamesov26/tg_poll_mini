from app.dataaccess.repositories.sqlalchlemy_repos.base import ISQLAlchemyRepo
from app.dataaccess.models import Answers


class AnswerRepo(ISQLAlchemyRepo):
    model = Answers
