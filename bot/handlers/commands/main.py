import random, re
from aiogram import types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession, As

from bot.tools.fsm import *
from bot.tools.keyboards import inline
from bot.tools.database import models

async def cmd_start(message:types.Message, state: FSMContext):
  await message.answer('Здраствуйте, это Юрист-бот, прежде чем воспользоваться, пожалуйста, пройдите регистрацию')
  await state.set_state(User.name)
  await message.answer('Введите ваше имя: ')



async def add_name(message:types.Message, state: FSMContext):
  await state.update_data(name=message.text)
  await state.set_state(User.surname)
  await message.answer('Введите вашу фамилию: ')


async def add_surname(message:types.Message, state:FSMContext):
  await state.update_data(surname=message.text)
  await state.set_state(User.middle_name)
  await message.answer('Введите ваше отчество: ')


async def add_middle_name(message:types.Message, state: FSMContext):
  await state.update_data(middle_name=message.text)
  await state.set_state(User.number)
  await message.answer('Введите ваш номер телефона: ')


async def add_number(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        if message.text.isdigit():
            text = message.text
            if text.startswith('8'):
                text = '7' + text[1:]
                if len(text) == 11:
                    await state.update_data(number=text)
                    await message.answer('Введите ваш почтовый адрес в формате email@example.com')
                    await state.set_state(User.email)
                else:
                    await message.answer(f'Произошла ошибка. Возможно, вы ввели некорректный номер. '
                                         f'Попробуйте ещё раз.')
            else:
                await message.answer(f'Произошла ошибка. Возможно, вы ввели некорректный номер. '
                                     f'Попробуйте ещё раз.')
        else:
            await message.answer(f'Произошла ошибка. Возможно, вы ввели некорректный номер. '
                             f'Попробуйте ещё раз.')
            

async def add_email(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.chat.type == "private":
        if is_email(message.text):
            await state.update_data(email=message.text)
            data = await state.get_data()
            session.add(User(
                name = data["name"],
                surname = data["surname"],
                middle_name = data["middle_name"],
                number = data["number"],
                email = data["email"],
            ))
            await session.commit()

            await message.answer('Спасибо! Ваши данные были успешно сохранены.')
            await message.answer('Воспользуйтесь меню ниже.', reply_markup=inline.main)
            await state.clear()
        else:
            await message.answer('Произошла ошибка. Возможно, вы ввели некорректный email. '
                                 'Попробуйте ещё раз.')

def is_email(text):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    text = str(text)
    if re.match(pattern, text):
        return True
    else:
        return False



