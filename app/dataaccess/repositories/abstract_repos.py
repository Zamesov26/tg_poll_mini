from abc import abstractmethod, ABC


class IRepository(ABC):
    @abstractmethod
    async def add_one(self, **data):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, **filters):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, **filters):
        raise NotImplementedError

    @abstractmethod
    async def edit_one(self, id_, **values):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id_):
        raise NotImplementedError

    @abstractmethod
    async def delete_all(self, **filters):
        raise NotImplementedError


class ILessonRepository(IRepository, ABC):
    @abstractmethod
    async def delete_question(self, question_id):
        raise NotImplementedError


class IUserAttemptRepository(IRepository, ABC):
    @abstractmethod
    async def get_random_by_user(self, user_id: int):
        raise NotImplementedError
