from aiogram import Dispatcher

from bots.vsspambot.data.config import ADMIN_COMMANDS, EDIT_COMMANDS
from bots.vsspambot.data.config import flags
from bots.vsspambot.keyboards.inline.guardian_keyboard import not_bot_callback
from bots.vsspambot.keyboards.inline.settings_keyboard import lang_callback
from .inline import button_admin_handler, button_edit_handler, button_language_handler, button_not_bot_handler

admin_commands = [ac.replace('/', '') for ac in ADMIN_COMMANDS.keys()]
edited_commands = [ac.replace('/', '') for ac in EDIT_COMMANDS.keys()]
lang_list = [f'lang:{lang}' for lang in flags.keys()]


def register_handlers_buttons(dp: Dispatcher):
    dp.register_callback_query_handler(button_admin_handler, lambda call: call.data in admin_commands)
    dp.register_callback_query_handler(button_edit_handler, lambda call: call.data in edited_commands)
    dp.register_callback_query_handler(button_language_handler, lang_callback.filter())
    dp.register_callback_query_handler(button_not_bot_handler, not_bot_callback.filter())
