from aiogram.exceptions import AiogramError
from aiogram import Bot, types, F
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery
from aiogram.fsm.context import FSMContext
import yookassa

from bot import logger

from bot.handlers.tools.email import is_email
from bot.tools.fsm import User
from bot.tools.keyboards.inline import get_inlineMix_btns, main_menu_for_pay
from bot.tools.database.utils import (
    add_user,
    orm_get_user,
    orm_get_user_coin,
    check_pay_status,
    orm_set_pay_status_true,
    orm_set_pay_status_false,
)


def register_user_handlers(dp):
    dp.message.register(add_name, User.name)
    dp.message.register(add_surname, User.surname)
    dp.message.register(add_middle_name, User.middle_name)
    dp.message.register(add_number, User.number)
    dp.message.register(add_email, User.email)
    dp.callback_query.register(catalog, F.data == "catalog")
    dp.callback_query.register(personal_area, F.data == "personal_area")
    dp.callback_query.register(payment, F.data == "payment")
    dp.callback_query.register(
        list_of_selected_lawyers, F.data == "list_of_selected_lawyers"
    )
    dp.callback_query.register(pay, F.data == "pay")
    dp.pre_checkout_query.register(pre_checkout_query)
    dp.callback_query.register(
        return_to_main_menu_from_pay, F.data == "return_to_main_menu_from_pay"
    )
    dp.callback_query.register(return_to_main_menu, F.data == "return_to_main_menu")
    dp.callback_query.register(my_lawyers, F.data == "my_lawyers")


async def add_name(message: types.Message, state: FSMContext):
    try:
        await state.update_data(name=message.text)
        await state.set_state(User.surname)
        await message.answer("Введите вашу фамилию: ")
    except AiogramError as e:
        logger.error("Произошла ошибка в функции add_name: %s", e, exc_info=True)
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте еще раз.")


async def add_surname(message: types.Message, state: FSMContext):
    try:
        await state.update_data(surname=message.text)
        await state.set_state(User.middle_name)
        await message.answer("Введите ваше отчество: ")
    except AiogramError as e:
        logger.error("Произошла ошибка в функции add_surname: %s", e, exc_info=True)
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте еще раз.")


async def add_middle_name(message: types.Message, state: FSMContext):
    try:
        await state.update_data(middle_name=message.text)
        await state.set_state(User.number)
        await message.answer("Введите ваш номер телефона: ")
    except AiogramError as e:
        logger.error("Произошла ошибка в функции add_middle_name: %s", e, exc_info=True)
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте еще раз.")


async def add_number(message: types.Message, state: FSMContext):
    try:
        if message.chat.type == "private":
            if message.text.isdigit():
                text = message.text
                if text.startswith("8"):
                    text = "7" + text[1:]
                if len(text) == 11:
                    try:
                        await state.update_data(number=text)
                        await message.answer(
                            "Введите ваш почтовый адрес в формате email@example.com"
                        )
                        await state.set_state(User.email)
                    except AiogramError as e:
                        logger.error(
                            f"Произошла ошибка при обновлении данных состояния: {e}"
                        )
                        await message.answer(
                            "Произошла внутренняя ошибка. Пожалуйста, попробуйте позже."
                        )

                else:
                    await message.answer(
                        "Произошла ошибка. Номер телефона должен состоять из 11 цифр. "
                        "Попробуйте ещё раз."
                    )
                    logger.error("Некорректный номер телефона")
            else:
                await message.answer(
                    "Произошла ошибка. Введённый текст не является числом. "
                    "Пожалуйста, введите корректный номер телефона."
                )
    except AiogramError as e:
        logger.error(f"Произошла ошибка в функции add_number: {e}")


async def add_email(message: types.Message, state: FSMContext):
    try:
        logger.debug("Зап")
        if message.chat.type == "private":
            if is_email(message.text):
                await state.update_data(email=message.text)
                data = await state.get_data()
                data["telegram_id"] = message.from_user.id
                data["telegram_name"] = message.from_user.full_name
                await message.answer(
                    "Спасибо! Ваши данные были успешно сохранены.\nВоспользуйтесь меню ниже.",
                    reply_markup=get_inlineMix_btns(
                        btns={
                            "Каталог": "catalog",
                            "Личный кабинет": "personal_area",
                            "Оплата": "payment",
                            "Мои Юристы": "my_lawyers",
                        }
                    ),
                )
                await state.clear()
                await add_user(data)
            else:
                await message.answer(
                    "Произошла ошибка. Возможно, вы ввели некорректный email. Попробуйте ещё раз."
                )
                logger.error("Некорректный email")
    except AiogramError as e:
        logger.error(f"Ошибка в функции add_email: {e}")


async def catalog(callback: CallbackQuery):
    try:
        await callback.answer("Открытие webapp с Юристами")
    except AiogramError as e:
        logger.error("Произошла ошибка в функции catalog: %s", e, exc_info=True)
        await callback.message.answer(
            "Произошла ошибка при открытии каталога. Пожалуйста, попробуйте еще раз."
        )


async def personal_area(callback: CallbackQuery):
    try:
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
            await callback.answer("Вы выбрали личный кабинет")
            await callback.message.edit_text(
                f"Ваш личный кабинет:\n\n{user_info}",
                reply_markup=get_inlineMix_btns(
                    btns={
                        "Каталог": "catalog",
                        "Оплата": "payment",
                        "Мои Юристы": "my_lawyers",
                    }
                ),
            )
        else:
            await callback.message.edit_text(
                "Пользователь не найден. Напишите команду /start в диалог с ботом для регистрации профиля или откройте каталог с Юристами нажав на кнопку ниже",
                reply_markup=get_inlineMix_btns(btns={"Каталог": "catalog"}),
            )
            logger.error("Пользователь не найден.")
    except AiogramError as e:
        logger.error("Произошла ошибка в функции personal_area: %s", e, exc_info=True)
        await callback.message.edit_text(
            "Произошла ошибка при открытии личного кабинета. Пожалуйста, попробуйте еще раз."
        )
    except Exception as e:
        logger.error(
            "Непредвиденная ошибка в функции personal_area: %s", e, exc_info=True
        )
        await callback.message.edit_text(
            "Произошла непредвиденная ошибка. Пожалуйста, попробуйте еще раз."
        )


async def payment(callback: CallbackQuery):
    try:
        await callback.answer("Оплата")
        await callback.message.edit_text(
            'Выберите нужный пункт из меню "Оплата" ',
            reply_markup=get_inlineMix_btns(
                btns={
                    "Список выбранных Юристов": "list_of_selected_lawyers",
                    "Оплата юридических услуг": "pay",
                    "Возврат в главное меню": "return_to_main_menu",
                }
            ),
        )
    except AiogramError as e:
        logger.error("Произошла ошибка в функции payment: %s", e, exc_info=True)
        await callback.message.answer(
            "Произошла ошибка при открытии меню оплаты. Пожалуйста, попробуйте еще раз."
        )


async def list_of_selected_lawyers(callback: CallbackQuery):
    try:
        await callback.answer("Список Юристов из Каталога")
        await callback.message.edit_text(
            "Ваши Юристы:\nЮрист 1: ФИО ОПЫТ КЛАССИФИКАЦИЯ ОПИСАНИЕ ФОТО\nЮрист 2: ФИО ОПЫТ КЛАССИФИКАЦИЯ ОПИСАНИЕ ФОТО\nЮрист 3: ФИО ОПЫТ КЛАССИФИКАЦИЯ ОПИСАНИЕ ФОТО",
            reply_markup=get_inlineMix_btns(
                btns={
                    "Оплатить": "pay",
                    "Возврат в главное меню": "return_to_main_menu",
                }
            ),
        )
    except AiogramError as e:
        logger.error(
            "Произошла ошибка в функции list_of_selected_lawyers: %s", e, exc_info=True
        )
        await callback.message.answer(
            "Произошла ошибка при открытии списка выбранных юристов. Пожалуйста, попробуйте еще раз."
        )


async def pay(callback: CallbackQuery, bot: Bot):
    try:
        await bot.send_invoice(
            chat_id=callback.message.chat.id,
            title='Оплата "Юрист-бот"',
            description="Оплата ваших выбранных Юристов из каталога",
            payload="Payment",
            provider_token="381764678:TEST:85195",
            currency="rub",
            prices=[
                types.LabeledPrice(label="Юристы", amount=50000),
                types.LabeledPrice(label="НДС", amount=0),
            ],
            max_tip_amount=500,
            suggested_tip_amounts=[100, 200],
            start_parameter="",
            provider_data=None,
            photo_url="https://tv.ib-bank.ru/files/images/videos/2018-11-30%20SOC-Forum%202018%20intro_tv.jpg",
            photo_size=100,
            photo_width=800,
            photo_height=450,
            reply_markup=main_menu_for_pay,
            need_name=True,
            need_email=True,
        )
        await callback.answer("Оплата")
    except AiogramError as e:
        logger.error("Произошла ошибка в функции pay: %s", e, exc_info=True)
        await callback.message.answer(
            "Произошла ошибка при обработке оплаты. Пожалуйста, попробуйте еще раз."
        )
    except Exception as e:
        logger.error("Непредвиденная ошибка в функции pay: %s", e, exc_info=True)
        await callback.message.answer(
            "Произошла непредвиденная ошибка. Пожалуйста, попробуйте еще раз."
        )


async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    try:
        if pre_checkout_query.total_amount > 0 and pre_checkout_query.currency == "RUB":
            await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
            await bot.send_message(
                chat_id=pre_checkout_query.from_user.id,
                text="Ваша оплата прошла успешно, чтобы продолжить, нажмите кнопку ниже",
                reply_markup=get_inlineMix_btns(
                    btns={
                        "Возврат в главное меню": "return_to_main_menu",
                    }
                ),
            )
            await orm_set_pay_status_true()
        else:
            await bot.answer_pre_checkout_query(
                pre_checkout_query.id,
                ok=False,
                error_message="Вы не оплатили заказ. Пожалуйста, оплатите заказ, прежде чем продолжить.",
            )
            logger.error("Оплата не прошла")
            await orm_set_pay_status_false()
    except AiogramError as e:
        logger.error(
            "Произошла ошибка в функции pre_checkout_query: %s", e, exc_info=True
        )
        await bot.send_message(
            chat_id=pre_checkout_query.from_user.id,
            text="Произошла ошибка при обработке оплаты. Пожалуйста, попробуйте еще раз.",
        )


async def return_to_main_menu_from_pay(callback: CallbackQuery):
    try:
        await callback.answer("Вы отменили оплату")
        await callback.message.answer(
            "Ваша оплата отменена, используйте меню ниже, выберите нужный пункт",
            reply_markup=get_inlineMix_btns(
                btns={
                    "Оплатить услуги Юристов повторно": "pay",
                    "Личный кабинет": "personal_area",
                    "Мои Юристы": "my_lawyers",
                    "Возврат в гланое меню": "return_to_main_menu",
                }
            ),
        )
    except AiogramError as e:
        logger.error(
            "Произошла ошибка в функции return_to_main_menu_from_pay: %s",
            e,
            exc_info=True,
        )
        await callback.message.answer(
            "Произошла ошибка при отмене оплаты. Пожалуйста, попробуйте еще раз."
        )


async def return_to_main_menu(callback: CallbackQuery):
    try:
        await callback.answer("Переход в главное меню")
        await callback.message.edit_text(
            "Вы в главном меню. Воспользуйтесь кнопками ниже ",
            reply_markup=get_inlineMix_btns(
                btns={
                    "Каталог": "catalog",
                    "Личный кабинет": "personal_area",
                    "Оплата": "payment",
                    "Мои Юристы": "my_lawyers",
                }
            ),
        )
    except AiogramError as e:
        logger.error(
            "Произошла ошибка в функции return_to_main_menu: %s", e, exc_info=True
        )
        await callback.message.answer(
            "Произошла ошибка при возврате в главное меню. Пожалуйста, попробуйте еще раз."
        )


async def my_lawyers(callback: CallbackQuery):
    try:
        await callback.answer("Список Юристов из Каталога")
        pay_status = await check_pay_status(callback.from_user.id)
        if pay_status == "Услуги успешно оплачены":
            await callback.message.edit_text(
                "Мои Юристы:\nЮрист 1: ФИО ОПЫТ КЛАССИФИКАЦИЯ ОПИСАНИЕ ФОТО\nЮрист 2: ФИО ОПЫТ КЛАССИФИКАЦИЯ ОПИСАНИЕ ФОТО\nЮрист 3: ФИО ОПЫТ КЛАССИФИКАЦИЯ ОПИСАНИЕ ФОТО",
                reply_markup=get_inlineMix_btns(
                    btns={
                        "Каталог": "catalog",
                        "Личный кабинет": "personal_area",
                        "Написать Юристу": "message_to_lawyers",
                    }
                ),
            )
        else:
            await callback.message.edit_text(
                "Мои Юристы:\nЮрист 1: ФИО ОПЫТ КЛАССИФИКАЦИЯ ОПИСАНИЕ ФОТО\nЮрист 2: ФИО ОПЫТ КЛАССИФИКАЦИЯ ОПИСАНИЕ ФОТО\nЮрист 3: ФИО ОПЫТ КЛАССИФИКАЦИЯ ОПИСАНИЕ ФОТО",
                reply_markup=get_inlineMix_btns(
                    btns={
                        "Оплатить": "pay",
                        "Возврат в главное меню": "return_to_main_menu",
                    }
                ),
            )
    except AiogramError as e:
        logger.error("Произошла ошибка в функции my_lawyers: %s", e, exc_info=True)
        await callback.message.answer(
            "Произошла ошибка при отображении списка выбранных юристов. Пожалуйста, попробуйте еще раз."
        )
