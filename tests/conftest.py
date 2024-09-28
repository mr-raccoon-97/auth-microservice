import pytest
from typing import AsyncGenerator
from server.settings import Settings
from server.adapters.setup import Database, UnitOfWork
from server.adapters.users import Users

@pytest.fixture(scope='session')
def settings() -> Settings:
    return Settings()

@pytest.fixture(scope='function')
async def uow(settings: Settings) -> AsyncGenerator[UnitOfWork, None]:
    database = Database(settings)
    await database.setup()
    transaction = await database.connection.begin()
    async with UnitOfWork(database) as uow:
        yield uow
    await transaction.rollback()
    await database.teardown()

@pytest.fixture(scope='function')
async def users(uow: UnitOfWork) -> Users:
    return Users(uow.session)