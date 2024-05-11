import asyncio
import config
from aiogram import Dispatcher, Bot, Router
from bot.tools.database.engine import create_db, drop_db



bot = Bot(token=config.TOKEN, parse_mode='HTML')
dp = Dispatcher()
router = Router()

def register_handlers():
    from .handlers import commands
    commands.register_handlers(dp)



async def start_bot():
    await create_db()
    register_handlers()
    await bot.delete_webhook(drop_pending_updates=True)
    print('日本の保育園')
    await dp.start_polling(bot)
