from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from server.schemas import User, Account


class Accounts(ABC):

    @abstractmethod 
    def create(self, id: str, type: str, provider: str) -> Account:
        ...
    
    @abstractmethod
    async def add(self, account: Account, user: User):
        ...

    @abstractmethod
    async def get(self, provider: str, id: str) -> Optional[Account]:
        ...


class Users(ABC):
    accounts: Accounts

    @abstractmethod
    def create(self, id: UUID, username: str) -> User:
        ...

    @abstractmethod
    async def add(self, user: User):
        ...

    @abstractmethod
    async def get(self, id: UUID) -> Optional[User]:
        ...

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        ...


async def users_port() -> Users:
    raise NotImplementedError