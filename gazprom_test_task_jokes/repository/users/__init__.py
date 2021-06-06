from abc import ABC
from abc import abstractmethod

from models import User


class UsersRepository(ABC):
    INDEX = 'users'
    
    @abstractmethod
    async def create(self, username: str, password: str) -> User:
        raise NotImplementedError()
    
    @abstractmethod
    async def read(self, username: str) -> User:
        raise NotImplementedError()
