from abc import ABC, abstractmethod

from app.dataaccess.database import async_session_maker
from app.dataaccess.repositories import sqlalchlemy_repos
from app.dataaccess.repositories import abstract_repos


class IUnitOfWork(ABC):
    users = abstract_repos.IRepository
    user_attempts = abstract_repos.IUserAttemptRepository
    fsm_data = abstract_repos.IRepository
    fsm_state = abstract_repos.IRepository
    lessons = abstract_repos.ILessonRepository
    questions = abstract_repos.IRepository
    answers = abstract_repos.IRepository
    questionnaires = abstract_repos.IRepository

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    @abstractmethod
    async def add(self, item):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def refresh(self, item):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session_factory=async_session_maker):
        self.session_factory = session_factory
        self.session = None

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = sqlalchlemy_repos.UserRepo(self.session)
        self.user_attempts = sqlalchlemy_repos.UserAttemptRepo(self.session)
        self.fsm_data = sqlalchlemy_repos.fsm_data.FSMDataRepo(self.session)
        self.fsm_state = sqlalchlemy_repos.fsm_data.FSMStateRepo(self.session)
        self.lessons = sqlalchlemy_repos.LessonRepo(self.session)
        self.questions = sqlalchlemy_repos.QuestionRepo(self.session)
        self.answers = sqlalchlemy_repos.AnswerRepo(self.session)
        self.questionnaires = sqlalchlemy_repos.QuestionnaireRepo(self.session)

        return await super().__aenter__()

    async def __aexit__(self, *args):
        # await super().__aexit__(*args)
        await self.session.close()

    async def add(self, item):
        self.session.add(item)

    async def commit(self):
        await self.session.commit()

    async def refresh(self, item):
        await self.session.refresh(item)

    async def rollback(self):
        await self.session.rollback()
