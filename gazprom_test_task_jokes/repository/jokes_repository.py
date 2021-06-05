from abc import ABC
from abc import abstractmethod
from typing import List

from model import Joke


class JokesRepository(ABC):
    INDEX = 'jokes'
    
    @abstractmethod
    async def create(self, username: str, joke: str) -> Joke:
        raise NotImplementedError()
    
    @abstractmethod
    async def read(self, _id: str, username: str) -> Joke:
        raise NotImplementedError()
    
    @abstractmethod
    async def read_all(self, username: str) -> List[Joke]:
        raise NotImplementedError()
    
    @abstractmethod
    async def update(self, _id: str, username: str, joke: str) -> Joke:
        raise NotImplementedError()
    
    @abstractmethod
    async def delete(self, _id: str, username: str) -> None:
        raise NotImplementedError()
