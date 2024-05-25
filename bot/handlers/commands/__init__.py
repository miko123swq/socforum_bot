from bot.handlers.commands.main import register_main_handlers
from bot.handlers.commands.user import register_user_handlers
from bot.handlers.commands.lawyer import register_lawyer_handlers


def register_handlers(dp):
  register_main_handlers(dp)
  register_user_handlers(dp)
  register_lawyer_handlers(dp)

  




