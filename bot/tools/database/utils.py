from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from bot.tools.database.engine import engine
from bot.tools.database import models
from .models import User, Lawyer


async def add_user(data):
    async with AsyncSession(engine) as session:  
        new_user = models.User(
            name=data["name"],
            surname=data["surname"],
            middle_name=data["middle_name"],
            number=data["number"],
            email=data["email"],
            telegram_id = data["telegram_id"],
            telegram_name = data["telegram_name"]
        )
        session.add(new_user)
        await session.commit()  


async def orm_get_user(telegram_id: int):
    async with AsyncSession(engine) as session:
        query = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(query)
        return result.scalar()
    
    
async def orm_get_user_coin():
    async with AsyncSession(engine) as session:
        query = select(User.user_coin)
        result = await session.execute(query)
        return result.scalar()
    
            
async def check_pay_status(telegram_id: int):
    async with AsyncSession(engine) as session:
        query = select(User.pay_status).where(User.telegram_id == telegram_id)  
        result = await session.execute(query)
        pay_status = result.scalar()
        if pay_status:
            return "Услуги успешно оплачены"
        else:
            return "Вы еще не оплатили выбранных Юристов"


async def orm_set_pay_status_true():
     async with AsyncSession(engine) as session:
        stmt = update(User).values(pay_status=True)
        await session.execute(stmt)
        await session.commit()


async def orm_set_pay_status_false():
     async with AsyncSession(engine) as session:
        stmt = update(User).values(pay_status=False)
        await session.execute(stmt)
        await session.commit()


#LAWYER
async def add_lawyer(data):
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
            telegram_id = data["telegram_id"],
            telegram_name = data["telegram_name"]
        )
        session.add(new_lawyer)
        await session.commit()  


async def orm_get_lawyer(telegram_id: int):
    async with AsyncSession(engine) as session:
        query = select(Lawyer).where(Lawyer.telegram_id == telegram_id)
        result = await session.execute(query)
        return result.scalar()
