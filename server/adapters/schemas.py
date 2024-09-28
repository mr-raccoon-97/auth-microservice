from uuid import UUID
from typing import Optional
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Schema(DeclarativeBase):
    pk: Mapped[int] = mapped_column(primary_key=True)

class User(Schema):
    __tablename__ = 'users'
    id: Mapped[UUID] = mapped_column('user_id', unique=True, nullable=False)
    username: Mapped[str] = mapped_column('user_username', unique=True, nullable=False)

class Account(Schema):
    __tablename__ = 'accounts'
    id: Mapped[str] = mapped_column('account_id', nullable=False)
    type: Mapped[str] = mapped_column('account_type', nullable=False)
    provider: Mapped[str] = mapped_column('account_provider', nullable=False)
    user_pk: Mapped[int] = mapped_column(ForeignKey('users.pk'), nullable=False)
    __table_args__ = (UniqueConstraint('account_provider', 'account_id', name='uq_account_provider_id'),)