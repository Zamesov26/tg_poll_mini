from app.dataaccess.repositories.sqlalchlemy_repos.base import ISQLAlchemyRepo
from app.dataaccess.models import Users


class UserRepo(ISQLAlchemyRepo):
    model = Users
