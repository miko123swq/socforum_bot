from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from bot import logger

from bot.tools.database.engine import engine
from bot.tools.database import models
from .models import User, Lawyer


async def add_user(data):
    try:
        async with AsyncSession(engine) as session:
            new_user = models.User(
                name=data["name"],
                surname=data["surname"],
                middle_name=data["middle_name"],
                number=data["number"],
                email=data["email"],
                telegram_id=data["telegram_id"],
                telegram_name=data["telegram_name"],
            )
            session.add(new_user)
            await session.commit()
    except SQLAlchemyError as e:
        logger.error("Ошибка при добавлении пользователя: %s", e, exc_info=True)


async def orm_get_user(telegram_id: int):
    try:
        async with AsyncSession(engine) as session:
            query = select(User).where(User.telegram_id == telegram_id)
            result = await session.execute(query)
            return result.scalar()
    except SQLAlchemyError as e:
        logger.error(
            "Ошибка при получении пользователя из базы данных: %s", e, exc_info=True
        )
        return None


async def orm_get_user_coin():
    try:
        async with AsyncSession(engine) as session:
            query = select(User.user_coin)
            result = await session.execute(query)
            return result.scalar()
    except SQLAlchemyError as e:
        logger.error(
            "Ошибка при получении количества монет пользователя из базы данных: %s",
            e,
            exc_info=True,
        )
        return None


async def check_pay_status(telegram_id: int):
    try:
        async with AsyncSession(engine) as session:
            query = select(User.pay_status).where(User.telegram_id == telegram_id)
            result = await session.execute(query)
            pay_status = result.scalar()
            if pay_status:
                return "Услуги успешно оплачены"
            else:
                return "Вы еще не оплатили выбранных Юристов"
    except SQLAlchemyError as e:
        logger.error("Ошибка при проверке статуса оплаты: %s", e, exc_info=True)
        return "Произошла ошибка при проверке статуса оплаты"


async def orm_set_pay_status_true():
    try:
        async with AsyncSession(engine) as session:
            stmt = update(User).values(pay_status=True)
            await session.execute(stmt)
            await session.commit()
    except SQLAlchemyError as e:
        logger.error("Ошибка при установке статуса оплаты в 'True': %s", e, exc_info=True)

async def orm_set_pay_status_false():
    try:
        async with AsyncSession(engine) as session:
            stmt = update(User).values(pay_status=False)
            await session.execute(stmt)
            await session.commit()
    except SQLAlchemyError as e:
        logger.error("Ошибка при установке статуса оплаты в 'False': %s", e, exc_info=True)


# LAWYER
async def add_lawyer(data):
    try:
        async with AsyncSession(engine) as session:
            new_lawyer = models.Lawyer(
                name=data["name"],
                surname=data["surname"],
                middle_name=data["middle_name"],
                number=data["number"],
                email=data["email"],
                description=data["description"],
                short_description=data["short_description"],
                diplomas=data["diplomas"],
                experience=data["experience"],
                legal_services_section=data["legal_services_section"],
                photo=data["photo"],
                telegram_id=data["telegram_id"],
                telegram_name=data["telegram_name"],
            )
            session.add(new_lawyer)
            await session.commit()
    except SQLAlchemyError as e:
        logger.error("Ошибка при добавлении юриста в базу данных: %s", e, exc_info=True)


async def orm_get_lawyer(telegram_id: int):
    try:
        async with AsyncSession(engine) as session:
            query = select(Lawyer).where(Lawyer.telegram_id == telegram_id)
            result = await session.execute(query)
            return result.scalar()
    except SQLAlchemyError as e:
        logger.error("Ошибка при получении данных о юристе из базы данных: %s", e, exc_info=True)
        return None  # Вернуть None в случае ошибки, чтобы вызывающий код мог обработать это

