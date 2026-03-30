from datetime import datetime, timedelta

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.schemas.users import UserCreate


async def create_user_repo(session: AsyncSession, user_data: UserCreate) -> User:
    user = User(**user_data.model_dump())
    session.add(user)
    await session.flush()
    await session.refresh(user)
    return user

async def get_users_repo(session: AsyncSession, limit: int, skip: int) -> list[User]:
    result = await session.execute(
        select(User)
        .order_by(User.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    users = result.scalars().all()
    return users

async def lock_user_repo(
        session: AsyncSession,
        days_to_lock: int = 0,
        hours_to_lock: int = 1
    ) -> User | None:
    result = await session.execute(
        select(User)
        .where((User.locktime < func.now()) | (User.locktime.is_(None)))
        .with_for_update(skip_locked=True)
        .limit(1)
    )
    user: User = result.scalar_one_or_none()
    if user is None:
        return None
    user.locktime = datetime.now() + timedelta(days=days_to_lock, hours=hours_to_lock)
    await session.flush()
    await session.refresh(user)
    return user

async def unlock_users_repo(session: AsyncSession) -> int:
    result = await session.execute(
        update(User)
        .where(User.locktime > func.now())
        .values(locktime=func.now())
        .returning(User.id)
    )
    amount_of_users = len(result.scalars().all())
    await session.flush()
    return amount_of_users
