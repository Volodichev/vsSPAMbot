from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart, CommandHelp
from aiogram.types import ContentType

from bots.vsspambot.filters import IsPrivate
from .info import command_start_handler, command_help_handler
from .text import command_handler, text_handler


def register_handlers_users_info(dp: Dispatcher):
    dp.register_message_handler(command_start_handler, IsPrivate(), CommandStart())
    dp.register_message_handler(command_help_handler, IsPrivate(), CommandHelp())
    dp.register_message_handler(command_help_handler, IsPrivate(), commands=['info'])

def register_handlers_users_text(dp: Dispatcher):
    dp.register_message_handler(command_handler, IsPrivate(), text_startswith='/', content_types=ContentType.TEXT)
    dp.register_message_handler(text_handler, IsPrivate(), content_types=ContentType.TEXT)
