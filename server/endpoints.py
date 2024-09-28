from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fastapi import status as status_code
from fastapi import HTTPException
from server.schemas import User, Account
from server.ports import Users, users_port

router = APIRouter()
    
@router.post('/users/')
async def add_user(user: User, users: Users = Depends(users_port)):
    if await users.get(user.id):
        raise HTTPException(status_code=status_code.HTTP_409_CONFLICT, detail=f'User with id {user.id} already exists')

    if await users.get_by_username(user.username):
        raise HTTPException(status_code=status_code.HTTP_409_CONFLICT, detail=f'User with username {user.username} already exists')
    
    user = users.create(user.id, user.username)
    await users.add(user)
    return Response(status_code=status_code.HTTP_201_CREATED)


@router.post('/users/{id}/accounts/')
async def add_account_to_user(id: UUID, account: Account, users: Users = Depends(users_port)):
    user = await users.get(id)
    if not user:
        raise HTTPException(status_code=status_code.HTTP_404_NOT_FOUND, detail=f'User with id {id} does not exist')
    
    if await users.accounts.get(account.provider, account.id):
        raise HTTPException(status_code=status_code.HTTP_409_CONFLICT, detail=f'Account from {account.provider} with id {account.id} already exists')

    account = users.accounts.create(account.id, account.type, account.provider)
    await users.accounts.add(account, user)
    return Response(status_code=status_code.HTTP_201_CREATED)