from typing import Optional
from sqlalchemy.sql import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from server.adapters.schemas import Account, User

class Accounts:
    def __init__(self, session: AsyncSession):
        self.session = session

    def create(self, id: str, type: str, provider: str) -> Account:
        return Account(id=id, type=type, provider=provider)
    
    async def add(self, account: Account, user: User):
        account.user_pk = user.pk
        command = insert(Account).values(id=account.id, type=account.type, provider=account.provider, user_pk=account.user_pk)
        await self.session.execute(command)

    async def get(self, provider: str, id: str) -> Optional[Account]:
        command = select(Account).where(Account.provider == provider, Account.id == id)
        result = await self.session.execute(command)
        return result.scalars().one_or_none()