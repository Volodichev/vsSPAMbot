from aiogram import Dispatcher
from aiogram.utils.exceptions import BotBlocked

from bots.vsspambot.data.config import ADMIN_COMMANDS, CREATOR_COMMANDS, EDIT_COMMANDS
from bots.vsspambot.filters import IsPrivate
from .errors import error_command_private_handler, error_bot_blocked, errors_handler

creator_commands = [ac.replace('/', '') for ac in CREATOR_COMMANDS.keys()]
admin_commands = [ac.replace('/', '') for ac in ADMIN_COMMANDS.keys()]
admin_commands.extend([ac.replace('/', '') for ac in EDIT_COMMANDS.keys()])
admin_commands.extend(creator_commands)


def register_errors(dp: Dispatcher):
    dp.register_message_handler(error_command_private_handler, IsPrivate(), commands=admin_commands)
    dp.register_errors_handler(error_bot_blocked, exception=BotBlocked)
    dp.register_errors_handler(errors_handler)
