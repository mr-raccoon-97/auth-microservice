from logging import getLogger
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from server.settings import Settings
    
logger = getLogger(__name__)

class Database:
    def __init__(self, settings: Settings):
        self.engine = create_async_engine(settings.database.dns)
    
    async def setup(self):
        self.connection = await self.engine.connect()
        self.sessionmaker = async_sessionmaker(self.connection, expire_on_commit=False, class_=AsyncSession)

    async def teardown(self):
        await self.connection.close()
        await self.engine.dispose()

class UnitOfWork:
    def __init__(self, database: Database):
        self.database = database

    async def __aenter__(self):
        self.session = self.database.sessionmaker()
        await self.session.begin()
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        if exc_type is None:
            await self.session.commit()
        else:
            await self.session.rollback()
        await self.session.close()