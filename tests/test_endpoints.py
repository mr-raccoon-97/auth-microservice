import pytest
from typing import AsyncGenerator
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

from server.endpoints import router, users_port

@pytest.fixture
async def client(users) -> AsyncGenerator[AsyncClient, None]:
    api = FastAPI()
    api.include_router(router)
    api.dependency_overrides[users_port] = lambda: users
    async with AsyncClient(transport=ASGITransport(api), base_url="http://test") as client:
        yield client

async def test_users(client: AsyncClient):
    response = await client.post('/users/', json={'id': '123e4567-e89b-12d3-a456-426614174000', 'username': 'user1'})
    assert response.status_code == 201
    response = await client.post('/users/', json={'id': '123e4567-e89b-12d3-a456-426614174000', 'username': 'user1'})
    assert response.status_code == 409
    response = await client.post('/users/', json={'id': '123e4567-e89b-12d3-a456-426614174001', 'username': 'user1'})
    assert response.status_code == 409

async def test_accounts(client: AsyncClient):
    response = await client.post('/users/', json={'id': '123e4567-e89b-12d3-a456-426614174000', 'username': 'user1'})
    assert response.status_code == 201
    response = await client.post('/users/123e4567-e89b-12d3-a456-426614174000/accounts/', json={'id': '123e4567-e89b-12d3-a456-426614174000', 'type': 'type1', 'provider': 'provider1'})
    assert response.status_code == 201
    response = await client.post('/users/123e4567-e89b-12d3-a456-426614174000/accounts/', json={'id': '123e4567-e89b-12d3-a456-426614174000', 'type': 'type1', 'provider': 'provider1'})
    assert response.status_code == 409
    response = await client.post('/users/123e4567-e89b-12d3-a456-426614174001/accounts/', json={'id': '123e4567-e89b-12d3-a456-426614174000', 'type': 'type1', 'provider': 'provider1'})
    assert response.status_code == 404