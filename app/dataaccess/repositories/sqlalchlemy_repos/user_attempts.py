from datetime import datetime
from typing import Optional

from sqlalchemy import select, and_, not_, or_, func
from sqlalchemy.orm import selectinload

from app.dataaccess.models import UserAttempts
from app.dataaccess.repositories.abstract_repos import IUserAttemptRepository
from app.dataaccess.repositories.sqlalchlemy_repos.base import ISQLAlchemyRepo


class UserAttemptRepo(ISQLAlchemyRepo, IUserAttemptRepository):
    model = UserAttempts

    async def get_random_by_user(self, user_id: int) -> Optional[UserAttempts]:
        date_now = datetime.now()
        stmt = select(UserAttempts) \
            .where(and_(UserAttempts.user_id == user_id,
                        not_(UserAttempts.is_passed),
                        not_(UserAttempts.check_required),
                        or_(UserAttempts.expectation_date.is_(
                            None),
                            UserAttempts.expectation_date < date_now)
                        )) \
            .order_by(func.random()) \
            .options(selectinload(UserAttempts.question))

        question = await self.session.execute(stmt)

        return question.scalars().one_or_none()
