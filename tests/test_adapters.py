import pytest
from uuid import UUID
from server.ports import Users

@pytest.mark.asyncio
async def test_users(users: Users):
    user = users.create(UUID('00000000-0000-0000-0000-000000000000'), 'test')
    await users.add(user)
    user = await users.get(user.id)
    assert user is not None
    assert user.id == UUID('00000000-0000-0000-0000-000000000000')
    assert user.username == 'test'

    user = await users.get_by_username('test')
    assert user is not None
    assert user.id == UUID('00000000-0000-0000-0000-000000000000')
    assert user.username == 'test'

@pytest.mark.asyncio
async def test_accounts(users: Users):
    user = users.create(UUID('00000000-0000-0000-0000-000000000000'), 'test')
    account = users.accounts.create('12345', 'oidc', 'google')
    await users.add(user)
    await users.accounts.add(account, user)

    account = await users.accounts.get('google', '12345')
    assert account is not None
    assert account.id == '12345'
    assert account.type == 'oidc'
    assert account.provider == 'google'