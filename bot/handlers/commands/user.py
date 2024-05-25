from aiogram import Bot, types, F
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery
from aiogram.fsm.context import FSMContext
import yookassa

from bot.handlers.tools import is_email
from bot.tools.fsm import User
from bot.tools.keyboards import inline
from bot.tools.database.utils import (
    add_user,
    orm_get_user,
    orm_get_user_coin,
    check_pay_status,
    orm_set_pay_status_true,
    orm_set_pay_status_false
)


def register_user_handlers(dp):
  dp.message.register(add_name, User.name)
  dp.message.register(add_surname, User.surname)
  dp.message.register(add_middle_name, User.middle_name)
  dp.message.register(add_number, User.number)
  dp.message.register(add_email, User.email)
  dp.callback_query.register(catalog, F.data == 'catalog')
  dp.callback_query.register(personal_area, F.data == 'personal_area')
  dp.callback_query.register(payment, F.data == 'payment')
  dp.callback_query.register(list_of_selected_lawyers, F.data == 'list_of_selected_lawyers')
  dp.callback_query.register(pay, F.data == 'pay')
  dp.pre_checkout_query.register(pre_checkout_query)
  dp.callback_query.register(return_to_main_menu_from_pay, F.data == 'return_to_main_menu_from_pay')
  dp.callback_query.register(return_to_main_menu, F.data == 'return_to_main_menu')
  dp.callback_query.register(my_lawyers, F.data == 'my_lawyers')
    
    
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
        await callback.message.edit_text(f"Ваш личный кабинет:\n\n{user_info}", reply_markup=inline.menu_in_personal_area)

    else:
        await callback.message.answer("Пользователь не найден.", reply_markup=inline.menu_in_personal_area)

    
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
    await callback.message.answer("Ваша оплата отменена, используйте меню ниже чтобы вернуться в меню оплаты или выберите нужный пункт", reply_markup=inline.main_menu)


async def return_to_main_menu(callback:CallbackQuery):
    await callback.answer("Переход в главное меню")
    await callback.message.edit_text("Вы в главном меню. Воспользуйтесь кнопками ниже ", reply_markup=inline.main_menu)


async def my_lawyers(callback: CallbackQuery):
    await callback.answer("Список Юристов из Каталога")
    pay_status =  await check_pay_status(callback.from_user.id)
    if pay_status == "Услуги успешно оплачены":
        await callback.message.edit_text("Мои Юристы:\nЮрист 1: ФИО ОПЫТ КЛАССИФИКАЦИЯ ОПИСАНИЕ ФОТО\nЮрист 2: ФИО ОПЫТ КЛАССИФИКАЦИЯ ОПИСАНИЕ ФОТО\nЮрист 3: ФИО ОПЫТ КЛАССИФИКАЦИЯ ОПИСАНИЕ ФОТО", reply_markup=inline.main_menu_in_my_lawyers)      
    else:
        await callback.message.edit_text("Мои Юристы:\nЮрист 1: ФИО ОПЫТ КЛАССИФИКАЦИЯ ОПИСАНИЕ ФОТО\nЮрист 2: ФИО ОПЫТ КЛАССИФИКАЦИЯ ОПИСАНИЕ ФОТО\nЮрист 3: ФИО ОПЫТ КЛАССИФИКАЦИЯ ОПИСАНИЕ ФОТО", reply_markup=inline.payment_layers)
