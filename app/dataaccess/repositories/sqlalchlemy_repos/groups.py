from app.dataaccess.repositories.sqlalchlemy_repos.base import ISQLAlchemyRepo
from app.dataaccess.models import Groups


class GroupRepo(ISQLAlchemyRepo):
    model = Groups
