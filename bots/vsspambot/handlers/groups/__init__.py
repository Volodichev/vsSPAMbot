from aiogram import Dispatcher
from aiogram.types import ContentType

from bots.vsspambot.data.config import ADMIN_COMMANDS, CREATOR_COMMANDS, spam_content_types
from bots.vsspambot.filters import ContainsMention, IsGroup
from .admins import (show_language_buttons, command_quarantine_handler, command_creator_handler,
                     command_admin_handler, command_info_handler, show_params_buttons)
from .antispam import custom_spam_handler, spam_handler
from .members import left_chat_member, new_member_handler
from .text import command_handler, text_handler

admin_commands = [ac.replace('/', '') for ac in ADMIN_COMMANDS.keys()]
creator_commands = [ac.replace('/', '') for ac in CREATOR_COMMANDS.keys()]


def register_handlers_admins(dp: Dispatcher):
    dp.register_message_handler(show_params_buttons, IsGroup(), commands=('settings'))
    dp.register_message_handler(command_creator_handler, IsGroup(), commands=creator_commands)
    dp.register_message_handler(command_admin_handler, IsGroup(), commands=admin_commands)
    dp.register_message_handler(command_quarantine_handler, IsGroup(), commands=('quarantine'))
    dp.register_message_handler(command_info_handler, IsGroup(), commands=('info'))
    dp.register_message_handler(show_language_buttons, IsGroup(), commands=('language'))


def register_handlers_antispam(dp: Dispatcher):
    dp.register_message_handler(custom_spam_handler, ContainsMention(), content_types=ContentType.TEXT)
    dp.register_message_handler(spam_handler, IsGroup(), content_types=spam_content_types)


def register_handlers_members(dp: Dispatcher):
    dp.register_message_handler(left_chat_member, IsGroup(), content_types=("left_chat_member"))
    dp.register_message_handler(new_member_handler, IsGroup(), content_types=("new_chat_members"))


def register_handlers_text(dp: Dispatcher):
    dp.register_message_handler(command_handler, IsGroup(), text_startswith='/', content_types=ContentType.TEXT)
    dp.register_message_handler(text_handler, IsGroup(), content_types=ContentType.TEXT)
