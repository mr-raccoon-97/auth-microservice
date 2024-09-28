from typing import Callable
from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from server.adapters.setup import UnitOfWork as UOW
from server.adapters.setup import Database
from server.adapters.users import Users
from server.settings import Settings
from server.endpoints import router, users_port
from logging import getLogger, basicConfig, INFO

basicConfig(level=INFO)
logger = getLogger(__name__)

settings = Settings()
database = Database(settings)

async def lifespan(api: FastAPI):
    logger.info('Setting up database')
    await database.setup()
    yield
    logger.info('Tearing down database')
    await database.teardown()

    logger.info('Stopping queue listener')

async def users() -> Users:
    async with UOW(database) as uow:
        return Users(uow.database)

api = FastAPI(lifespan=lifespan)
api.include_router(router)
api.dependency_overrides[users_port] = users
api.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])