"""
Модуль для создания репозитория пользователей
"""
from datetime import datetime, timedelta

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.database.repositories.base_repo import BaseResourceRepo


class UsersRepo(BaseResourceRepo):
    def get_by_id(self):
        raise AttributeError("method not allowed")

    async def get_by_name(self):
        raise AttributeError("method not allowed")

    async def get_users(
        self,
        session: AsyncSession,
        limit: int, skip: int
    ) -> list[User]:
        """
        Выполняет получение всех записей ресурса

        Подробное описание: Выполняет получение всех записей ресурса с offset-based pagination

        Args:
            session: Объект сессии через который будет происходить получение ресурса
            limit: Количество объектов ресурса, которое хотим получить
        Returns:
            Список полученных объектов ресурса
        Raises:
            SQLAlchemyError: при неудачной попытке подключиться к бд
        """ # noqa: E501
        result = await session.execute(
            select(User)
            .order_by(User.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        users = result.scalars().all()
        return users

    async def lock_user(
        self,
        session: AsyncSession,
        days_to_lock: int = 0,
        hours_to_lock: int = 1
    ) -> User | None:
        """
        Выполняет блокировку первого свободного ресурса и возвращает его

        Подробное описание: Выполняет блокировку первого ресурса,
        у которого locktime больше нынешнего времени и возвращает его

        Args:
            session: Объект сессии через который будет происходить получение ресурса
            days_to_lock: Количество дней, на которое хотим заблокировать ресурс
            hours_to_lock: Количество часов, на которое хотим заблокировать ресурс
        Returns:
            Заблокированный ресурс | None (если свободных ресурсов нет)
        Raises:
            SQLAlchemyError: при неудачной попытке подключиться к бд
        """
        result = await session.execute(
            select(User)
            .where((User.locktime < func.now()) | (User.locktime.is_(None)))
            .with_for_update(skip_locked=True)
            .limit(1)
        )
        user: User = result.scalar_one_or_none()
        if user is None:
            return None
        user.locktime = datetime.now() + timedelta(
            days=days_to_lock,
            hours=hours_to_lock
        )
        await session.flush()
        await session.refresh(user)
        return user

    async def unlock_users(self, session: AsyncSession) -> int:
        """
        Выполняет разблокировку всех ресурсов

        Args:
            session: Объект сессии через который будет происходить получение ресурса
        Returns:
            Количество разблокированных ресурсов
        Raises:
            SQLAlchemyError: при неудачной попытке подключиться к бд
        """
        result = await session.execute(
            update(User)
            .where(User.locktime > func.now())
            .values(locktime=func.now())
            .returning(User.id)
        )
        amount_of_users = len(result.scalars().all())
        await session.flush()
        return amount_of_users

users_repo = UsersRepo(User)
