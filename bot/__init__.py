import asyncio
import logging

import config

from aiogram import Dispatcher, Bot, Router
from bot.tools.database.engine import create_db, drop_db

logging.basicConfig(
    level=logging.ERROR,
    filename="logging.log",
    format="%(levelname)s - (%(asctime)s): %(message)s (line %(lineno)d) [%(filename)s]",
    datefmt="%d/%m/%Y %H:%M:%S",
    encoding="utf-8",
    filemode="w",
)
logger = logging.getLogger(__name__)

bot = Bot(token=config.TOKEN, parse_mode="HTML")
dp = Dispatcher()
router = Router()


def register_handlers():
    from .handlers import commands

    commands.register_handlers(dp)


async def start_bot():
    await create_db()
    register_handlers()
    await bot.delete_webhook(drop_pending_updates=True)
    print("Starting bot - successfully")
    await dp.start_polling(bot)
