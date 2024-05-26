from aiogram.exceptions import AiogramError
from aiogram import types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot import logger

from bot.tools.fsm import User, Lawyer
from bot.tools.keyboards.inline import get_inlineMix_btns
from bot.tools.database.utils import orm_get_user, orm_get_lawyer


def register_main_handlers(dp):
    dp.message.register(cmd_start, CommandStart())
    dp.message.register(cmd_lawyer, Command("lawyer"))


async def cmd_start(message: types.Message, state: FSMContext):
    try:
        telegram_id = message.from_user.id
        user = await orm_get_user(telegram_id)
        if user:
            await message.answer(
                "Вы уже зарегистрированы. Воспользуйтесь меню ниже",
                reply_markup=get_inlineMix_btns(
                    btns={
                        "Каталог": "catalog",
                        "Личный кабинет": "personal_area",
                        "Оплата": "payment",
                        "Мои Юристы": "my_lawyers",
                    }
                ),
            )
        else:
            await message.answer(
                "Здравствуйте, это Юрист-бот, прежде чем воспользоваться, пожалуйста, пройдите регистрацию"
            )
            await state.set_state(User.name)
            await message.answer("Введите ваше имя:")
    except AiogramError as e:
        logger.error("Произошла ошибка в функции cmd_start: %s", e, exc_info=True)
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте еще раз.")


async def cmd_lawyer(message: types.Message, state: FSMContext):
    try:
        telegram_id = message.from_user.id
        lawyer = await orm_get_lawyer(telegram_id)
        if lawyer:
            await message.answer(
                "Вы уже зарегистрированы в Личном Кабинете для Юристов. Воспользуйтесь меню ниже",
                reply_markup=get_inlineMix_btns(
                    btns={
                        "Личный кабинет Юриста": "lawyer_personal_area",
                        "Переход на сайт": "catalog",
                    }
                ),
            )
        else:
            await message.answer(
                "Здравствуйте, это Юрист-бот для Юристов, прежде чем воспользоваться, пожалуйста, пройдите регистрацию"
            )
            await state.set_state(Lawyer.name)
            await message.answer("Введите ваше имя:")
    except AiogramError as e:
        logger.error("Произошла ошибка в функции cmd_lawyer: %s", e, exc_info=True)
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте еще раз.")
