from aiogram import types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.tools.fsm import User, Lawyer
from bot.tools.keyboards import inline
from bot.tools.database.utils import orm_get_user, orm_get_lawyer


def register_main_handlers(dp):
    dp.message.register(cmd_start, CommandStart())
    dp.message.register(cmd_lawyer, Command('lawyer'))


async def cmd_start(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    user = await orm_get_user(telegram_id)
    if user:
        await message.answer('Вы уже зарегистрированы. Воспользуйтесь меню ниже', reply_markup=inline.main_menu)
    else:
        await message.answer('Здравствуйте, это Юрист-бот, прежде чем воспользоваться, пожалуйста, пройдите регистрацию')
        await state.set_state(User.name)
        await message.answer('Введите ваше имя:')


async def cmd_lawyer(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    lawyer = await orm_get_lawyer(telegram_id)
    if lawyer:
        await message.answer('Вы уже зарегистрированы в Личном Кабинете для Юристов. Воспользуйтесь меню ниже', reply_markup=inline.lawyer_main_menu)
    else:
        await message.answer('Здравствуйте, это Юрист-бот для Юристов, прежде чем воспользоваться, пожалуйста, пройдите регистрацию')
        await state.set_state(Lawyer.name)
        await message.answer('Введите ваше имя:')


