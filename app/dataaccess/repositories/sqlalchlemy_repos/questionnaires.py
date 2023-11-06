from app.dataaccess.repositories.sqlalchlemy_repos.base import ISQLAlchemyRepo
from app.dataaccess.models import Questionnaires


class QuestionnaireRepo(ISQLAlchemyRepo):
    model = Questionnaires
