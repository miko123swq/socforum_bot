import re
import uuid
from aiogram import Bot, types
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
import yookassa
from yookassa import Payment

from bot.tools.fsm import User, Lawyer
from bot.tools.keyboards import inline
from bot.tools.database.utils import (
    add_user,
    orm_get_user,
    orm_get_user_coin,
    check_pay_status,
    orm_set_pay_status_true,
    orm_set_pay_status_false,
    add_lawyer,
    orm_get_lawyer,
)


async def cmd_start(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    user = await orm_get_user(telegram_id)
    if user:
        await message.answer('Вы уже зарегистрированы. Воспользуйтесь меню ниже', reply_markup=inline.main_menu)
    else:
        await message.answer('Здравствуйте, это Юрист-бот, прежде чем воспользоваться, пожалуйста, пройдите регистрацию')
        await state.set_state(User.name)
        await message.answer('Введите ваше имя:')


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
            

async def add_email(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        if is_email(message.text):
            await state.update_data(email=message.text)
            data = await state.get_data()
            data["telegram_id"] = message.from_user.id
            data["telegram_name"] = message.from_user.full_name
            await message.answer('Спасибо! Ваши данные были успешно сохранены.\nВоспользуйтесь меню ниже.', reply_markup=inline.main_menu)
            await state.clear()
            await add_user(data)  
        else:
            await message.answer('Произошла ошибка. Возможно, вы ввели некорректный email. Попробуйте ещё раз.')


def is_email(text):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    text = str(text)
    if re.match(pattern, text):
        return True
    else:
        return False
    

async def catalog(callback: CallbackQuery):
    await callback.answer("Открытие webapp с Юристами")


async def personal_area(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    user = await orm_get_user(telegram_id)
    user_coin = await orm_get_user_coin()
    pay_status = await check_pay_status(telegram_id)

    if user:
        user_info = (
            f"Имя: {user.name}\n"
            f"Фамилия: {user.surname}\n"
            f"Отчество: {user.middle_name}\n"
            f"Номер телефона: {user.number}\n"
            f"Email: {user.email}\n"
            f"Монеты: {user_coin}\n"
            f"Статус оплаты: {pay_status}" 
        )
        await callback.answer('Вы выбрали личный кабинет')
        await callback.message.answer(f"Ваш личный кабинет:\n\n{user_info}", reply_markup=inline.menu_in_personal_area)

    else:
        await callback.message.answer("Пользователь не найден.")

    
async def payment(callback:CallbackQuery):
    await callback.answer('Оплата')
    await callback.message.edit_text('Выберите нужный пункт из меню "Оплата" ', reply_markup=inline.payment)


async def list_of_selected_lawyers(callback:CallbackQuery):
    await callback.answer("Список Юристов из Каталога")
    await callback.message.edit_text("Ваши Юристы:\nЮрист 1: ФИО ОПЫТ КЛАССИФИКАЦИЯ ОПИСАНИЕ ФОТО\nЮрист 2: ФИО ОПЫТ КЛАССИФИКАЦИЯ ОПИСАНИЕ ФОТО\nЮрист 3: ФИО ОПЫТ КЛАССИФИКАЦИЯ ОПИСАНИЕ ФОТО", reply_markup=inline.payment_layers)


async def pay(callback: CallbackQuery, bot: Bot):
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title='Оплата "Юрист-бот"',
        description='Оплата ваших выбранных Юристов из каталога',
        payload='Payment',
        provider_token='381764678:TEST:85195',
        currency='rub',
        prices=[
            types.LabeledPrice(
                label='Юристы',
                amount=50000
            ),
            types.LabeledPrice(
                label='НДС',
                amount=0
            )
        ],
        max_tip_amount=500,
        suggested_tip_amounts=[100, 200], 
        start_parameter='',
        provider_data=None,
        photo_url='https://tv.ib-bank.ru/files/images/videos/2018-11-30%20SOC-Forum%202018%20intro_tv.jpg',
        photo_size=100,
        photo_width=800,
        photo_height=450,
        reply_markup=inline.main_menu_for_pay,
        need_name=True,
        need_email=True,
        )
    await callback.answer("Оплата")


async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    if pre_checkout_query.total_amount > 0 and pre_checkout_query.currency == "RUB":  
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
        await bot.send_message(chat_id=pre_checkout_query.from_user.id, text="Ваша оплата прошла успешно, чтобы продолжить, нажмите кнопку ниже", reply_markup=inline.return_to_main_menu)
        await orm_set_pay_status_true()
    else:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=False, error_message="Вы не оплатили заказ. Пожалуйста, оплатите заказ, прежде чем продолжить.")
        await orm_set_pay_status_false()


async def return_to_main_menu_from_pay(callback:CallbackQuery):
    await callback.answer("Вы отменили оплату")
    await callback.message.answer("Ваша оплата отменена", reply_markup=inline.main_menu)


async def return_to_main_menu(callback:CallbackQuery):
    await callback.answer("Переход в главное меню")
    await callback.message.edit_text("Вы в главном меню. Воспользуйтесь кнопками ниже ", reply_markup=inline.main_menu)


async def my_lawyers(callback: CallbackQuery):
    await callback.answer("Список Юристов из Каталога")
    pay_status =  await check_pay_status(callback.from_user.id)
    if pay_status == "Услуги успешно оплачены":
        await callback.message.edit_text("Мои Юристы:\nЮрист 1: ФИО ОПЫТ КЛАССИФИКАЦИЯ ОПИСАНИЕ ФОТО\nЮрист 2: ФИО ОПЫТ КЛАССИФИКАЦИЯ ОПИСАНИЕ ФОТО\nЮрист 3: ФИО ОПЫТ КЛАССИФИКАЦИЯ ОПИСАНИЕ ФОТО", reply_markup=inline.main_menu_in_my_lawyers)
        await callback.message.answer("Если вы хотите связаться с оплаченным Юристом, воспользуйтесь кнопкой ниже", reply_markup=inline.message_to_layers)
    else:
        await callback.message.edit_text("Мои Юристы:\nЮрист 1: ФИО ОПЫТ КЛАССИФИКАЦИЯ ОПИСАНИЕ ФОТО\nЮрист 2: ФИО ОПЫТ КЛАССИФИКАЦИЯ ОПИСАНИЕ ФОТО\nЮрист 3: ФИО ОПЫТ КЛАССИФИКАЦИЯ ОПИСАНИЕ ФОТО", reply_markup=inline.payment_layers)


# /LAWYER
async def cmd_lawyer(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    lawyer = await orm_get_lawyer(telegram_id)
    if lawyer:
        await message.answer('Вы уже зарегистрированы в Личном Кабинете для Юристов. Воспользуйтесь меню ниже', reply_markup=inline.lawyer_main_menu)
    else:
        await message.answer('Здравствуйте, это Юрист-бот для Юристов, прежде чем воспользоваться, пожалуйста, пройдите регистрацию')
        await state.set_state(Lawyer.name)
        await message.answer('Введите ваше имя:')


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
    await message.answer(str(data))
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








    




