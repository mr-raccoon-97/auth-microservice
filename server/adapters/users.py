from uuid import UUID
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import insert, select, update, delete
from server.adapters.schemas import User
from server.adapters.accounts import Accounts

class Users:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.accounts = Accounts(session)

    def create(self, id: UUID, username: Optional[str] = None) -> User:
        return User(id=id, username=username)
    
    async def add(self, user: User):
        command = insert(User).values(id=user.id, username=user.username).returning(User.pk)
        result = await self.session.execute(command)   
        user.pk = result.scalars().first()
        
    async def get(self, id: UUID) -> Optional[User]:
        command = select(User).where(User.id == id)
        result = await self.session.execute(command)
        return result.scalars().one_or_none()        
    
    async def get_by_username(self, username: str) -> Optional[User]:
        command = select(User).where(User.username == username)
        result = await self.session.execute(command)
        return result.scalars().one_or_none()
        