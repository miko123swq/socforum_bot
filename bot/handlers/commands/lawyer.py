from aiogram import types, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.handlers.tools import is_email
from bot.tools.fsm import User, Lawyer 
from bot.tools.keyboards import inline
from bot.tools.database.utils import (
    add_lawyer,
    orm_get_lawyer,
)


def register_lawyer_handlers(dp):
  dp.message.register(add_lawyer_name, Lawyer.name)
  dp.message.register(add_lawyer_surname, Lawyer.surname)
  dp.message.register(add_lawyer_middle_name, Lawyer.middle_name)
  dp.message.register(add_lawyer_number, Lawyer.number)
  dp.message.register(add_lawyer_email, Lawyer.email)
  dp.message.register(add_lawyer_description, Lawyer.description)
  dp.message.register(add_lawyer_short_description, Lawyer.short_description)
  dp.message.register(add_lawyer_diplomas, Lawyer.diplomas)
  dp.message.register(add_lawyer_experience, Lawyer.experience)
  dp.message.register(add_lawyer_legal_services_section, Lawyer.legal_services_section)
  dp.message.register(add_lawyer_photo, Lawyer.photo)
  dp.callback_query.register(lawyer_personal_area, F.data == 'lawyer_personal_area')


async def add_lawyer_name(message:types.Message, state: FSMContext):
  await state.update_data(name=message.text)
  await state.set_state(Lawyer.surname)
  await message.answer('Введите вашу фамилию: ')


async def add_lawyer_surname(message:types.Message, state:FSMContext):
  await state.update_data(surname=message.text)
  await state.set_state(Lawyer.middle_name)
  await message.answer('Введите ваше отчество: ')


async def add_lawyer_middle_name(message:types.Message, state: FSMContext):
  await state.update_data(middle_name=message.text)
  await state.set_state(Lawyer.number)
  await message.answer('Введите ваш номер телефона: ')


async def add_lawyer_number(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        if message.text.isdigit():
            text = message.text
            if text.startswith('8'):
                text = '7' + text[1:]
                if len(text) == 11:
                    await state.update_data(number=text)
                    await message.answer('Введите ваш почтовый адрес в формате email@example.com')
                    await state.set_state(Lawyer.email)
                else:
                    await message.answer(f'Произошла ошибка. Возможно, вы ввели некорректный номер. '
                                         f'Попробуйте ещё раз.')
            else:
                await message.answer(f'Произошла ошибка. Возможно, вы ввели некорректный номер. '
                                     f'Попробуйте ещё раз.')
        else:
            await message.answer(f'Произошла ошибка. Возможно, вы ввели некорректный номер. '
                             f'Попробуйте ещё раз.')
          

async def add_lawyer_email(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        if is_email(message.text):
            await state.update_data(email=message.text)
            await message.answer("Введите ваше описание профиля")
            await state.set_state(Lawyer.description)
        else:
            await message.answer('Произошла ошибка. Возможно, вы ввели некорректный email. Попробуйте ещё раз.')


async def add_lawyer_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите ваше краткое описание профиля")
    await state.set_state(Lawyer.short_description)


async def add_lawyer_short_description(message: types.Message, state: FSMContext):
    await state.update_data(short_description=message.text)
    await message.answer("Введите ваше образование (Диполмы, Сертификаты)")
    await state.set_state(Lawyer.diplomas)


async def add_lawyer_diplomas(message: types.Message, state: FSMContext):
    await state.update_data(diplomas=message.text)
    await message.answer("Введите ваш опыт работы:")
    await state.set_state(Lawyer.experience)


async def add_lawyer_experience(message: types.Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await message.answer("Введите вашу юридическую специализацию:")
    await state.set_state(Lawyer.legal_services_section)


async def add_lawyer_legal_services_section(message: types.Message, state: FSMContext):
    await state.update_data(legal_services_section=message.text)
    await message.answer("Пришлите ваше фото:")
    await state.set_state(Lawyer.photo)


async def add_lawyer_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    data = await state.get_data()
    data["telegram_id"] = message.from_user.id
    data["telegram_name"] = message.from_user.full_name
    await message.answer("Регистрация Личного Кабинета Юриста прошла успешно\nДля дальнейшего взаимодействия с ботом используйте кнопки ниже", reply_markup=inline.lawyer_main_menu)
    await state.clear()
    await add_lawyer(data)


async def lawyer_personal_area(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    lawyer = await orm_get_lawyer(telegram_id)

    if lawyer:
        lawyer_info = (
            f"Имя: {lawyer.name}\n"
            f"Фамилия: {lawyer.surname}\n"
            f"Отчество: {lawyer.middle_name}\n"
            f"Номер телефона: {lawyer.number}\n"
            f"Email: {lawyer.email}\n"
            f"Описание: {lawyer.description}\n"
            f"Краткое описание: {lawyer.short_description}\n"
            f"Дипломы: {lawyer.diplomas}\n" 
            f"Опыт: {lawyer.experience}\n"
            f"Оказываемые юридические услуги: {lawyer.legal_services_section}\n"
            f"Заработок: {lawyer.earnings}\n"
            f"Список клиентов: {lawyer.clients}\n"
        )

        if lawyer.photo:
            await callback.answer('Вы выбрали личный кабинет')
            await callback.message.answer_photo(photo=lawyer.photo, caption=f"Личный кабинет Юриста:\n{lawyer_info}")
        else:
            await callback.answer('Вы выбрали личный кабинет')
            await callback.message.answer(f"Личный кабинет Юриста:\n{lawyer_info}")
    else:
        await callback.answer()
        await callback.message.answer("Пользователь не найден.")