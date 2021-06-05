from abc import ABC
from abc import abstractmethod

from model import User


class UsersRepository(ABC):
    INDEX = 'users'
    
    @abstractmethod
    async def create(self, username: str, password: str) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    async def read(self, username: str) -> User:
        raise NotImplementedError()
